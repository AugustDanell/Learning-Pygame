import java.util.ArrayList;

public class game {
    private gameSquare[] gameSquares;
    private String mode;
    private String pendingPurchase;
    private int turn;
    private int propertyProceeding;
    private cardDealer cd;

    game(){
        gameSquares = new gameSquare[26];
        mode = "Normal";
        this.init();
        turn = 1;
        propertyProceeding = 0;
        pendingPurchase = "none";

        // The man (or woman) who deals the cardw.
        cd = new cardDealer();
        cd.shuffleCards();
    }

    public chanceCard drawCard(){
        return cd.popCard();
    }

    /* Init()
    *  Initiates the board with objects that pertain to the board, initiating every square
    *
    */
    private void init(){
        // Init for the first row.
        gameSquares[0] = new gameSquare("Start", 1, false, 0,0);
        gameSquares[1] = new gameSquare("Tiggare vid ICA", 2, false, 0,2000);
        gameSquares[2] = new gameSquare("Roden", 3, true, 2000,500);
        gameSquares[3] = new gameSquare("Chans", 4, false, 0,0);
        gameSquares[4] = new gameSquare("Inlåst på Busstation", 5, false, 0,0);

        // Init for the second row.
        gameSquares[5] = new gameSquare("Willys", 6, true, 2000,400);
        gameSquares[6] = new gameSquare("Chans", 7, false, 0,0);
        gameSquares[7] = new gameSquare("Coop", 8, true, 2000,400);
        gameSquares[8] = new gameSquare("ÖB", 9, true, 2500,500);
        gameSquares[9] = new gameSquare("Roslags", 10, true, 2000,500);
        gameSquares[10] = new gameSquare("Biltema", 11, true, 3500,650);
        gameSquares[11] = new gameSquare("Jula", 12, true, 3500,650);
        gameSquares[12] = new gameSquare("Rusta", 13, true, 4000,700);
        gameSquares[13] = new gameSquare("Parkering", 14, false, 0,0);

        // Init for the third row.
        gameSquares[14] = new gameSquare("Spel och Sånt", 15, true, 4200, 800);
        gameSquares[15] = new gameSquare("Nordic Wellness (City)", 16, true, 3000,500);
        gameSquares[16] = new gameSquare("Norrtälje Bibliotek", 17, true, 4500,850);
        gameSquares[17] = new gameSquare("Fyllebråk", 18, false, 0,0);

        // Init for the fourth row.
        gameSquares[18] = new gameSquare("Elgiganten", 0, true, 5000,900);
        gameSquares[19] = new gameSquare("Nordic Wellness (Norrteljeporten)", 0, true, 3000,500);
        gameSquares[20] = new gameSquare("Norrtälje Park", 0, false, 0,0);
        gameSquares[21] = new gameSquare("Norrtälje Teknikgymnasium", 0, true, 2000,500);
        gameSquares[22] = new gameSquare("Chans", 0, false, 0,0);
        gameSquares[23] = new gameSquare("Norrtälje Hamn", 0, true, 8000,1250);
        gameSquares[24] = new gameSquare("Tiggare vid Willys", 0, false, 0,1000);
        gameSquares[25] = new gameSquare("Jan Emanuels Bostad", 0, true, 10000,1500);
    }

    /* setPropertyProceeding()
    *  This method puts a property into a proceeding, meaning that it is used to store a property that is being offered.
    *  If accepted this property number will then be transfered to the player so that the player can mark it.
    */
    public void setPropertyProceeding(int p){
        System.out.println("Method 'Set Property Proceeding' Entered");
        propertyProceeding = p;
    }

    /* getPropertyProceeding()
     * A getter method that is used to extract the proceeding mentioned above.
     */
    public int getPropertyProceeding(){
        return propertyProceeding;
    }

    /* getRent()
     * Extracts the rent from a square, given a position.
    */
    public int getRent(int pos){
        return gameSquares[pos-1].getRent();
    }

    /* setPendingPurchase()
     * Sets a string into what is known as a "pending purchase". This is
     */

    public void setPendingPurchase(String s){
        pendingPurchase = s;
    }

    public String getPendingPurchase(){
        return pendingPurchase;
    }


    public int getCost(int pos){
        return gameSquares[pos-1].getCost();
    }

    public String getMode(){
        return mode;
    }

    public void setMode(String s){
        mode = s;
    }

    public String getName(int pos){
        return gameSquares[pos-1].getName();
    }

    public void setOwnership(int p, int id){
        gameSquares[p-1].setOwnership(id);
    }

    public int getOwnership(int p){
        return gameSquares[p-1].getOwnership();
    }

    /* buyProperty()
     * A public method that returns the cost of a property to the player so that the program can withdraw that
     * number. Moreover the method also sets the player id as the property owner.
    */

    public int buyProperty(int p, int id){
        setOwnership(p, id);
        return gameSquares[p-1].getCost();
    }

    /* propertySquare()
     * A simple method that looks to see if a given square is a property or not, so that the game will know how
     * to handle it.
    */
    public boolean propertySquare(int pos){
        int[] propertyList = {3,6,8,9,10,11,12,13,15,16,17,19,20,22,24,26};
        if(contains(propertyList,pos)){
            return true;
        }

        return false;
    }



    private boolean contains(int[] arr, int pos){
        for (int i = 0; i < arr.length; i++){
            if(pos == arr[i]){
                return true;
            }
        }

        return false;
    }

    public int getTurn(){
        return turn;
    }

    public int endTurn(){
        turn %= 4;
        propertyProceeding = 0;
        return turn+1;
    }
}
