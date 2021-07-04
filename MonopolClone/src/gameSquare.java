public class gameSquare {
    private boolean isProperty;
    private int squareNumber;
    private int cost;
    private String name;
    private int owned;
    private int rent;

    public gameSquare(String n, int sn, boolean isProp, int c, int r){
        name = n;
        isProperty = isProp;
        squareNumber = sn;
        cost = c;
        owned = 0;
        rent = r;
    }

    /* getRent()
     * Returns the rent of a square.
     */
    public int getRent(){
        return rent;
    }

    /* getName()
     * returns the name of a square.
    */
    public String getName(){
        return name;
    }

    /* getCost()
     * returns the cost of buying a square.
     */
    public int getCost(){
        return cost;
    }

    /* setOwnership()
     * Used to set the ownership of a square so that a player is listed to poccess an item
     * that he or she might have bought.
     */
    public void setOwnership(int o){
        owned = o;
    }

    /* getOwnership()
     * Used to get that ownership mentioned briefly above.
     */
    public int getOwnership(){
        return owned;
    }
}
