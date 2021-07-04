import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.Random;
import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.TimeUnit;

public class client extends JPanel {

    /* Socket and in-/ output data: */
    private static Socket Socket = null;                        // Socket.
    private static PrintWriter out = null;                      // Out communication.
    private static BufferedReader in = null;                    // In communication.
    private static String address;                              // IP-Address.
    private static int connectionPort = 8989;                   // Port.
    private static graphics drawing = new graphics();           // Temp

    /* Essential Client Data:       */
    private static int pos = 15;                                  // Our X-coordinate.
    private static boolean lose = false;                        // If we have lost.
    private static boolean win = false;                         // If we have won.
    private static int id = -1;                                 // Player unique id to identify us.
    private static boolean choice = false;
    private static Timer timer = new Timer();
    private static boolean askStatus = false;

    // Step 0: Setting up a movement panel (Non-related to the Sockets):
    // Every action listener sends a request to move to the serverThread, that will be accepted or not.
    // In total there are five buttons: One for the dice, two for choice A resp B, one for buying house(s) and one for
    // making trade deals though this might not be used. (Lets see)


    static class Status extends TimerTask {
        public void run() {
            askStatus = true;
        }
    }

    static class movementPanel extends JPanel {
        private JButton DiceButton = new JButton("Slå Tärning");
        private JButton ValAButton = new JButton("Val A");
        private JButton ValBButton = new JButton("Val B");
        private JButton KopButton = new JButton("Köp hus och/eller hotel (du behöver en hel koncern)");
        private JButton ErbjudandeButton = new JButton("Föreslå erbjudande till annan spelare");

        public movementPanel() {


            drawing.setPreferredSize(new Dimension(1500, 700));
            add(drawing);

            // Three subssteps:
            // 1. Declare the listeners.
            // 2. Add the listerners to every button - They map to a request we send to the servr.
            // 3. Add the buttons to the panel.

            DiceListener DiceListener = new DiceListener();
            ValAListener ValAListener = new ValAListener();
            ValBListener ValBListener = new ValBListener();
            KopListener KopListener = new KopListener();
            ErbjudandeListener ErbjudandeListener = new ErbjudandeListener();

            DiceButton.addActionListener(DiceListener);
            ValAButton.addActionListener(ValAListener);
            ValBButton.addActionListener(ValBListener);
            KopButton.addActionListener(KopListener);
            ErbjudandeButton.addActionListener(ErbjudandeListener);


            add(ValAButton);
            add(ValBButton);
            add(KopButton);
            add(DiceButton);
            add(ErbjudandeButton);
        }
    }

    // Listens to the right button.
    static class DiceListener implements ActionListener{
        @Override
        public void actionPerformed(ActionEvent e) {
            if(!choice) {
                Random r = new Random();
                int dice = r.nextInt(12) + 1;           // Random number on the bound [1,12]
                out.println("DICE " + id + " " + dice);
                System.out.println(dice);
            }
        }
    }

    // Listens to the left button.
    static class ValAListener implements ActionListener{
        @Override
        public void actionPerformed(ActionEvent e) {
            if(choice){
                out.println("A " + id);
            }
        }
    }

    // Listens to the up button.
    static class ValBListener implements ActionListener{
        @Override
        public void actionPerformed(ActionEvent e) {
            if(choice){
                out.println("B " + id);
            }
        }
    }

    // Listens to the down button.
    static class KopListener implements ActionListener{
        @Override
        public void actionPerformed(ActionEvent e) {
            if(!choice){

            }
        }
    }

    // Listens to the deactivate button.
    static class ErbjudandeListener implements ActionListener{
        @Override
        public void actionPerformed(ActionEvent e) {
            if(!choice){

            }
        }
    }

    // If the user disconnects etc, we should alert the server.
    // A leave message is sent, alongside the ID of the client:
    public static void leavingProcedure(){
        System.out.println("Client leaving: cya n3rds xd");
        out.println("LEAVE: " + id);
        System.exit(0);
    }

    /* Reads a string from the socket: */
    private static String readLine() throws IOException {
        String str = in.readLine();
        return str;
    }


    /* main */
    /* Step 0: Setting up the socket connection to the server, so we can pass information back and forth. */
    /* Step 1: Setting up the graphical, user interface, buttons and action listeners for these. */
    /* Step 2: Requesting an ID from the server - And then start the game until win or defeat is given. */
    /* Step 3: Playing as the client, passing information back and forth until a status message from the server says otherwise. */
    /* Step 4: Terminate the socket from the client side, also let the server know we are fucking off. */

    public static void main(String[] args) throws IOException{
        // Step 1 - Setting up socket:

        try {
            address = "127.0.0.1";                                                 // Set the ip adress.
        } catch (ArrayIndexOutOfBoundsException e) {
            System.err.println("Missing argument ip-adress");
            System.exit(1);
        }
        try {
            Socket = new Socket(address, connectionPort);
            out = new PrintWriter(Socket.getOutputStream(), true);        // For sending to the socket.
            in = new BufferedReader(new InputStreamReader                         // For recieving from the socket.
                    (Socket.getInputStream()));

        } catch (UnknownHostException e) {
            System.err.println("Unknown host: " +address);
            System.exit(1);
        } catch (IOException e) {
            System.err.println("Couldn't open connection to " + address);
            System.exit(1);
        }


        // Step 0: Setting up the user interface:

        JFrame frame = new JFrame();
        JPanel panel = new movementPanel();
        //panel.setLayout(null);

        frame.add(panel);
        frame.setSize(400,400);
        frame.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
        frame.setVisible(true);

        // Here we are setting up a special listener also for what to do when closing the window
        // We want it to send to send to the server that we are leaving now, this is done when the window is closed down.

        frame.addWindowListener(new WindowAdapter() {
            @Override
            public void windowClosing(WindowEvent event) {
                leavingProcedure();

            }
        });

        // TESTAR KORT TODO: Ta bort när allt funkar.
        chanceCard card = new chanceCard();
        card.setCardNumber(15);
        drawing.drawCard(card);

        // Step 2 Play the game: (Server state = S2)
        out.println("GIVE PLAYER ID");
        while(!lose && !win){                                                   // Game is on.

            if(askStatus){
                out.println("STATUS");
                askStatus = false;
            }

            String responseString = readLine();

            // Modified From Stack Overflow: https://stackoverflow.com/questions/12908412/print-hello-world-every-x-seconds
            Timer timer = new Timer();
            timer.schedule(new Status(), 0, 2000);

            if(responseString != null) {
                String[] split = responseString.split(" ");
                if (responseString != null) {
                    if (split[0].equals("ID:")) {                              // Set player unique number as ID.
                        id = Integer.parseInt(split[1]);                       // The player receives the ID.
                        drawing.upPlayer(id, 1);
                        drawing.setPlayerName(id, "Spelarnamn " + id);
                    }
                    else if (split[0].equals("PLAYER-POSITIONS:")){

                    }
                    else if(split[0].equals("PLAYER-PROPERTIES:")){
                        // TODO: Långsam metod att calla draw 26 ggr men smidigast atm:
                        for (int i = 0; i < 26; i++){
                            int property = i+1;
                            int player = Integer.parseInt(split[property]);
                            if(player != 0){
                                drawing.updateProperty(property,player);
                            }
                        }
                    }
                    else if (split[0].equals("POSITION")) {
                        int id2 = Integer.parseInt(split[1]);
                        int pos = Integer.parseInt(split[2]);
                        drawing.upPlayer(id2, pos);
                        drawing.setPlayerName(id2, "Spelarnamn " + id2);
                    }
                    else if(split[0].equals("PURCHASE")){
                        int id2 = Integer.parseInt(split[1]);
                        int cost = Integer.parseInt(split[2]);
                        String property = split[3];
                        choice = true;
                        drawing.setPurchase(id2, cost, property);
                    }
                    else if(split[0].equals("PAYMENTOK")){
                        drawing.upPlayerMoney(id,Integer.parseInt(split[1]));
                        choice = false;
                        out.println("UPDATE");
                    }
                    else if(split[0].equals("DECLINED")){
                        choice = false;
                    }
                    else if(split[0].equals("PLAYER-UPDATES:")){
                        System.out.println(responseString);
                        int m1 = Integer.parseInt(split[1]);
                        int m2 = Integer.parseInt(split[2]);
                        int m3 = Integer.parseInt(split[3]);
                        int m4 = Integer.parseInt(split[4]);
                        drawing.updateMoneyList(m1,m2,m3,m4);

                    }
                    else if(split[0].equals("PROPERTY-UPDATES:")){
                        int property = Integer.parseInt(split[1]);
                        int player = Integer.parseInt(split[2]);
                        System.out.println(responseString);

                        if(property != 0)
                            drawing.updateProperty(property, player);
                    }
                    else if(split[0].equals("NON-CHOICE-CARD:")){
                        System.out.println("Row 253 Non choice card");
                        int cardNumber = Integer.parseInt(split[1]);
                        card = new chanceCard();
                        card.setCardNumber(cardNumber);

                        drawing.drawCard(card);
                    }
                    else if(split[0].equals("CHOICE-CARD:")){
                        choice = true;
                        int cardNumber = Integer.parseInt(split[1]);
                        card = new chanceCard();
                        card.setCardNumber(cardNumber);

                        drawing.drawCard(card);
                    }
                }
            }
        }

        // Step 4 - Leaving:
        leavingProcedure();
        in.close();
        out.close();
        Socket.close();

    }
}