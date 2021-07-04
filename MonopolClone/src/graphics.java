import javax.swing.*;
import java.awt.*;


public class graphics extends JComponent {
    private boolean readCard;
    private boolean drawPlayer;
    private chanceCard card;
    private Color[] colorArr = {Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW};
    private int[] moneyList = {30000, 30000, 30000, 30000};
    private String[] nameList = {"Ouppkopplad", "Ouppkopplad", "Ouppkopplad", "Ouppkopplad"};
    int[] playerList = {1,1,1,1};
    private int maxPlayers = 4;

    private int purchaseId = 0;
    private int purchaseCost = 0;
    private String purchaseName = "";
    private int[] propList;



    public graphics(){
        propList = new int[26];
        for(int i = 0; i < 26; i++){
            propList[i] = 0;
        }
        readCard = false;
    }

    // Default drawer
    public void paintComponent(Graphics g) {
        this.drawBoard(g); // Generically drawing the board
        this.drawPlayer(g,1);
        this.drawPlayer(g,2);
        this.drawPlayer(g,3);
        this.drawPlayer(g,4);

        this.drawInformation(g, 1, moneyList[0]);
        this.drawInformation(g, 2, moneyList[1]);
        this.drawInformation(g, 3, moneyList[2]);
        this.drawInformation(g, 4, moneyList[3]);

        if(readCard){
            g.setColor(Color.BLACK);
            //readCard = false;
            //g.fillRect(100,100,5000,5000);
            this.drawCardInt(g,card);
        }
        if(purchaseId != 0){
            this.drawPurchase(g);
        }

    }

    /* drawPurchase()
     * draws up a purchase for a user.
    */
    public void drawPurchase(Graphics g){
        this.drawTexts(g, 20, 200, "Vill du köpa tomt nr " + purchaseId +"'med namn: " + purchaseName + "'för " + purchaseCost + " kr?'Val(a) : Ja, Val(B) : Nej");
    }

    /* setPurchase()
     * Sets all the necessary variables so that when repaint() is called the drawPurchase can draw up everything.
     */
    public void setPurchase(int id2, int cost, String name){
        purchaseId = id2;
        purchaseCost = cost;
        purchaseName = name;
        repaint();
    }


    /* drawCard()
     * A method that signals that the player has drawn a card and sets all the prerequisites for drawing it on the board.
     */

    public void drawCard(chanceCard c){
        readCard = true;
        card = c;
        repaint();
    }

    /* drawCardInt()
    *  An internal drawing method that is used specifically to draw the text within the card.
    */
    public void drawCardInt(Graphics g, chanceCard c){
        System.out.println(c.readCard());
        this.drawTexts(g,1275,425, c.readCard());
    }

    /* upPlayer()
    *  Updates a player based on the id on the board. The id is both a determinant of colour and an offset, designed so that
    *  there are no collisions when drawing players.
    */
    public void upPlayer(int id, int position){
        playerList[id-1] = position;
        repaint();
    }

    /* upPlayerMoney()
     *
     */
    public void upPlayerMoney(int id, int money){
        moneyList[id-1] = money;
        repaint();
    }

    private void drawPlayer(Graphics g, int id){
        int idOffset = 22;
        g.setColor(colorArr[id-1]);
        int pos = playerList[id-1];

        if(pos < 5){
            g.fillOval(275, 675-100*pos-((id-1)*idOffset), 20,20);
        }
        else if(pos < 14){
            g.fillOval(275+100*(pos-5),175-((id-1)*idOffset), 20, 20);
        }
        else if(pos < 18){
            g.fillOval(1175, 175+100*(pos-14)-((id-1)*idOffset), 20, 20);
        }
        else if(pos < 26){
            g.fillOval(1175-100*(pos-18), 575-((id-1)*idOffset), 20, 20);
        }
    }

    public void setPlayerName(int id, String name){
        nameList[id-1] = name;
        repaint();
    }

    private void drawInformation(Graphics g, int id, int money){
        int idOffset = 25;
        g.setColor(colorArr[id-1]);
        g.fillRect(1250, 165+(id-1)*idOffset, 10,10);
        g.drawString(nameList[id-1] + " " + money, 1260, 175+(id-1)*idOffset);
    }

    public void drawBoard(Graphics g){
        // The game borders:
        g.setColor(Color.BLACK);
        g.drawRect(200,100,1000,500);
        g.drawRect(300, 200, 800,300);

        // Game text:
        Font font = g.getFont().deriveFont( 45.0f );
        g.setFont(font);
        g.drawString("Norrtälje Monopol", 550, 275);

        font = g.getFont().deriveFont( 25.0f );
        g.setFont(font);
        g.drawString("Spelet där just du kan bli den nya Jan Emanuel!", 460, 325);

        // Game info to be broadcasted:
        g.drawString("Händelseförlopp:",0,150);
        g.drawRect(0, 160, 175,400);

        g.drawString("Deltagarlista:",1250, 150);
        g.drawString("Chanskort", 1250, 390);
        g.drawRect(1250, 400, 225, 275);

        // Spelrutorna:
        // Standard font
        font = g.getFont().deriveFont( 14.0f );
        g.setFont(font);

        this.playerSquare(g, 0,"START'inkassera'4000kr", Color.WHITE);
        this.playerSquare(g, 1,"Tiggare'Vid ICA'betala'2000kr", Color.WHITE);
        this.playerSquare(g, 2,"Roden'2000kr",Color.GREEN);
        this.playerSquare(g, 3, "Chans", Color.RED);
        this.playerSquare(g, 4, "Inlåst'på'Busstationen", Color.WHITE);

        this.playerSquare(g, 5, "Willys'2000kr", Color.BLUE);
        this.playerSquare(g, 6, "Chans", Color.RED);
        this.playerSquare(g, 7, "Coop'2000kr", Color.BLUE);
        this.playerSquare(g, 8, "ÖB'2500kr", Color.BLUE);
        this.playerSquare(g, 9, "Roslags'2000kr", Color.GREEN);
        this.playerSquare(g, 10, "Biltema'3500kr", Color.YELLOW);
        this.playerSquare(g, 11, "Jula'3500kr", Color.YELLOW);
        this.playerSquare(g, 12, "Rusta'4000kr", Color.YELLOW);
        this.playerSquare(g, 13, "Parkering'Friruta", Color.WHITE);

        this.playerSquare(g, 14, "Spel'Och'Sånt'4200kr", Color.BLACK);
        this.playerSquare(g, 15, "Nordic'Wellness'(City)'3000kr", Color.ORANGE);
        this.playerSquare(g, 16, "Norrtälje'Bibliotek'4500kr",Color.BLACK);
        this.playerSquare(g,17, "Fylleslagsmål:'Gå till'Busstation" ,Color.WHITE);

        this.playerSquare(g,18, "Elgiganten'5000kr",Color.BLACK);
        this.playerSquare(g, 19, "Nordic'Wellness'(Norrtelje-'porten)'3000kr",Color.ORANGE);
        this.playerSquare(g, 20, "Norrtälje'Park", Color.WHITE);
        this.playerSquare(g, 21, "Norrtälje'Teknik-'Gymnasium'2000kr", Color.GREEN);
        this.playerSquare(g, 22, "Chans", Color.RED);
        this.playerSquare(g, 23, "Norrtälje'Hamn'8000kr", Color.MAGENTA);
        this.playerSquare(g, 24, "Tiggare'Vid Willys'betala'1000kr", Color.WHITE);
        this.playerSquare(g, 25, "Jan Emanuels'Bostad'10000kr", Color.MAGENTA);
    }

    /* This function is a help function that makes it so that if we have one string we can use "'" as a delimiter for a now row.
    *  This is needed for longer texts on a game square.
    */
    public void drawTexts(Graphics g, int x, int y, String s){
        int offset = 20;
        String[] strings = s.split("'");
        for(int i = 0; i < strings.length; i++){
            g.drawString(strings[i], x-20, y+i*15);
        }

    }

    public void updateProperty(int property, int player){
        propList[property-1] = player;
        repaint();
    }

    public void updateMoneyList(int m1, int m2, int m3, int m4){
        moneyList[0] = m1;
        moneyList[1] = m2;
        moneyList[2] = m3;
        moneyList[3] = m4;
        repaint();
    }

    public void playerSquare(Graphics g, int square, String text, Color c){
        // Four steps: 1. fill a rectangle with a color, 2. write the game square, 3. write a text, 4. write a player marker.
        int yOffset = 15;

        if(square < 5){

            if(!(c.equals(Color.WHITE))) {                               // 1
                g.setColor(c);
                g.fillRect(200, 500 - square * 100, 100, 20);
                g.setColor(Color.BLACK);
                yOffset = 0;
            }

            g.drawRect(200, 500-square*100,100, 100);  // 2
            this.drawTexts(g, 225, 535-square*100-yOffset, text);  // 3

            if(propList[square] != 0) {
                System.out.println("216 lol");
                g.setColor(this.getColor(propList[square]));
                g.fillRect(200, 585-square*100,15,15);
                g.setColor(Color.BLACK);
            }
        }

        else if(square < 14){

            if(!(c.equals(Color.WHITE))) {                              // 1
                g.setColor(c);
                g.fillRect(200+100*(square-4), 100, 100, 20);
                g.setColor(Color.BLACK);
                yOffset = 0;
            }

            g.drawRect(200+100*(square-4), 100,100, 100); // 2

            this.drawTexts(g,225+100*(square-4),135-yOffset, text);           // 3

            if(propList[square] != 0) {
                System.out.println("237 graphics: Writing Marker");
                g.setColor(this.getColor(propList[square]));
                g.fillRect(200+100*(square-4), 185,15,15);
                g.setColor(Color.BLACK);
            }
        }

        else if(square < 18){
            if(!(c.equals(Color.WHITE))) {                                            // 1
                g.setColor(c);
                g.fillRect(1100, 200+100*(square-14), 100, 20);
                g.setColor(Color.BLACK);
                yOffset = 0;
            }

            g.drawRect(1100, 200+100*(square-14),100, 100);                     // 2
            this.drawTexts(g, 1125,  235+100*(square-14)-yOffset,text);                     // 3

            if(propList[square] != 0) {                                                           // 4
                System.out.println("257 graphics: Writing Marker");
                g.setColor(this.getColor(propList[square]));
                g.fillRect(1100, 285+100*(square-14),15,15);
                g.setColor(Color.BLACK);
            }
        }
        else {
            if(!(c.equals(Color.WHITE))) {                                                        // 1
                g.setColor(c);
                g.fillRect(1100-100*(square-17), 500, 100, 20);
                g.setColor(Color.BLACK);
                yOffset = 0;
            }

            g.drawRect(1100-100*(square-17),500, 100, 100);                     // 2
            this.drawTexts(g,1125-100*(square-17), 535-yOffset, text);                      // 3

            if(propList[square] != 0) {
                System.out.println("257 graphics: Writing Marker");
                g.setColor(this.getColor(propList[square]));
                g.fillRect(1100-100*(square-17), 585,15,15);
                g.setColor(Color.BLACK);
            }
        }
    }

    public Color getColor(int p){
        switch (p) {
            case 1: return Color.RED;
            case 2: return Color.BLUE;
            case 3: return Color.GREEN;
            case 4: return Color.YELLOW;
            default: return Color.black;
        }
    }
}
