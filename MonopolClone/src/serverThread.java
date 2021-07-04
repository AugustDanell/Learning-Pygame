import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

/* serverThread
 *  This object is tasked with holding a connection with a client and handling all the client requests that may come (Communication protocol in the report).
 *  The object will carry information back and forth, depending on what the client sends, and serverThread may also pass information up to the Server, via
 *  the server instance passed in its constructor.
*/

public class serverThread extends Thread {
    private Socket socket = null;                   // Our socket connection to client.
    private BufferedReader in;                      // Our object that enables us to take input from the client.
    private PrintWriter out;                        // Our object that enables us to send output to the client.
    private boolean victory;                        // Flag to keep track of victory condition.
    private boolean defeat;                         // Flag to keep track of defeat condition.
    private Server servData;                        // The instance of the server that holds global data that both players should see.
    private chanceCard pendingCard;
    private int pid;

    public serverThread(Server servData, Socket socket) {
        super("ServerThread");
        this.socket = socket;
        victory = false;
        defeat = false;
        this.servData = servData;
    }

    // Global update functions in response to a status ping:
    public String updateMoney(){
        return ("PLAYER-UPDATES: " + servData.getPlayer(1).getMoney() + " " + servData.getPlayer(2).getMoney() + " " + servData.getPlayer(3).getMoney() + " " + servData.getPlayer(4).getMoney());

    }

    public String updatePositions(){
        return ("PLAYER-POSITIONS: " + servData.getPlayer(1).getPosition() + " " + servData.getPlayer(2).getPosition() + " " + servData.getPlayer(3).getPosition() + " " + servData.getPlayer(4).getPosition());
    }

    public String updateProperties(){
        return ("PLAYER-PROPERTIES: " + ownershipStrings(servData.getGame()));
    }



    // TODO: Due to Javas string concatenation ---> Slow method
    public String ownershipStrings (game game){
        StringBuilder strB = new StringBuilder();
        for (int i = 0; i < 26; i++){
            strB.append(game.getOwnership(i + 1)).append(" ");
        }

        return strB.toString();
    }

    // This is the main function that is being called upon a client connection.
    // run() essentially carries a communication with the client that connects and if the client gives a valid request, for instance moving on the board
    // in a place in which there is no debris, no other player or no walls, the run function will then update the server instance that is being passed
    // as "servData". In other words, "servData" is global and can be seen by all the other serverThreads, and a specific serverThread, via this run()
    // function, simply relays information back and forth and if a valid request is being made, the global data is updated:

    public void run() {

        // We establish a connection with the client:
        try (
                PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                BufferedReader in = new BufferedReader(
                        new InputStreamReader(
                                socket.getInputStream(), "UTF-8"));
        ) {

            // We have an ongoing game, where we catch any request from our linked client and handle it:
            String input;
            while (!victory && !defeat) {
                input = in.readLine();
                if(input != null) {

                    if (input.equals("GIVE PLAYER ID")) {
                        System.out.println("YO");
                        servData.increasePlayers();
                        int players = servData.get_player_number();
                        pid = players;
                        out.println("ID: " + players);
                    }
                    else if(input.equals("STATUS")){
                        // The Broadcasting State:
                        out.println(updateMoney());        // Updating players' money
                        out.println(updatePositions());                 // -||-  positions
                        out.println(updateProperties());                // -||-  properties
                        out.println("TURN: " + servData.getTurn());     // -||-  turn
                    }
                    else {
                        String[] split = input.split(" ");
                        System.out.println(input);
                        game game = servData.getGame();
                        player p = servData.getPlayer(pid);

                        if (split[0].equals("DICE")) {
                            int id = Integer.parseInt(split[1]);
                            int moves = Integer.parseInt(split[2]);
                            p.movePlayer(moves);
                            out.println("POSITION " + id + " " + p.getPosition());

                            // If a player lands on a property:
                            int pos = p.getPosition();
                            if (game.propertySquare(pos)) {
                                // Check who owns it:
                                int ownId = p.getPlayerId();
                                int propId = game.getOwnership(pos);

                                if (ownId == propId) {
                                    // Do nothing because this property is our own.
                                }
                                else if (propId == 0) {
                                    if (game.getCost(pos) <= p.getMoney()) {
                                        // Case 2: Purchasing a property
                                        out.println("PURCHASE " + pos + " " + game.getCost(pos) + " " + game.getName(pos));
                                        game.setMode("PURCHASE");
                                        game.setPendingPurchase(pos + " " + game.getName(pos));
                                    } else {
                                        out.println("CANNOT-AFFORD " + ownId + " " + pos);
                                    }
                                } else {
                                    int rent = game.getRent(pos);
                                    player us = servData.getPlayer(ownId);
                                    player landlord = servData.getPlayer(propId);
                                    us.pay(rent);
                                    landlord.recieve(rent);
                                    servData.setPlayer(ownId,us);
                                    servData.setPlayer(propId,landlord);
                                    out.println(updateMoney());
                                    game.endTurn();
                                }
                            }

                            // Chanskort
                            else if(pos == 4 || pos == 7 || pos == 23){
                                chanceCard c = game.drawCard();
                                if(c.choiceCard()){
                                    // The chance card is a multi choice card:
                                    System.out.println("Row 99");
                                    out.println("CHOICE-CARD: " + c.getCardNumber());
                                    game.setMode("CARD");
                                }
                                else {
                                    System.out.println("Row 102");
                                    // The Chance Card is a regular card:
                                    c.effectOfCard(p);
                                    out.println("NON-CHOICE-CARD: " + c.getCardNumber());
                                    pendingCard = c;
                                    out.println(updateMoney());
                                }
                            }

                            else
                                if(pos == 2 || pos == 25){
                                    // Case 1: Tiggare // Beggars:
                                    p.pay(game.getRent(pos));
                                    out.println(updateMoney());
                                }

                        }
                        else if (split[0].equals("A")) {
                            if(game.getMode().equals("PURCHASE")){
                                int playerID = Integer.parseInt(split[1]);
                                String s = game.getPendingPurchase();
                                String[] split2 = s.split(" ");
                                int pos = Integer.parseInt(split2[0]);

                                // Making transactions:
                                p = servData.getPlayer(playerID);
                                int cost = game.buyProperty(pos, playerID);
                                p.pay(cost);
                                servData.setPlayer(playerID, p);

                                // Transmitting back:
                                out.println("PAYMENTOK " + p.getMoney());
                                game.setPropertyProceeding(pos);
                            }
                            else if(game.getMode().equals("CARD")){
                                pendingCard.firstEffect(p);
                            }

                            game.setMode("Normal");


                        }
                        else if (split[0].equals("B")) {
                            game.setMode("Normal"); // Declining offer.
                            out.println("DECLINED");
                        }
                        else if(split[0].equals("UPDATE")){
                            // Playerinfo:
                            out.println(updateMoney());                        // Recently Property bought this turn
                            out.println("PROPERTY-UPDATES: " + game.getPropertyProceeding() + " " + game.getTurn());
                            servData.endTurn(game);
                        }
                        else if(game.getMode().equals("CARD")){
                            pendingCard.secondEffect(p);
                        }
                    }
                }
            }

            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}