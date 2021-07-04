public class player {
    private int money;
    private int playerId;
    private int position;
    private int passTurns;
    private int shield;
    private int ownedProperties;

    player(int id){
        money = 30000;
        position = 25;
        position = 1;
        playerId = id;
        passTurns = 0;
        shield = 0;
        ownedProperties = 0;
    }

    public void increaseProperties(){
        ownedProperties ++;
    }

    public int getOwnedProperties(){
        return ownedProperties;
    }

    public void setShield(int shield) {
        this.shield = shield;
    }

    public int getShield(){
        return shield;
    }

    public boolean isShielded(){
        return shield > 0;
    }

    public void passTurn(int t){
        passTurns = t;
    }

    public int getPassTurns(){
        return passTurns;
    }

    public int getPlayerId(){
        return playerId;
    }

    public int getPosition(){
        return position;
    }

    public void setPosition(int p){
        position = p;
    }

    public void movePlayer(int m){
        System.out.println("Move: " + m + " Position: " + position);
        position += m;


        // Because of the indexing doesn't work straight of to use modulo:
        if(position > 25){
            position -= 25;
        }
    }

    public int getMoney(){
        return money;
    }

    public void pay(int n){
        money -= n;
    }

    public void recieve(int n){
        money += n;
    }
}
