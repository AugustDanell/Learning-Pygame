import java.util.Random;

public class cardDealer {
    private int numberOfCards = 6;  // Ändra denna sen då.
    private chanceCard[] deck;

    public void setNumberOfCards(int n){
        numberOfCards = n;
    }

    public void shuffleCards(){
        deck = new chanceCard[numberOfCards];

        // Start with a deck with card numbers 1 to 6 resp.
        for(int i = 0; i < numberOfCards; i++){
            int j = i+1;
            deck[i] = new chanceCard();
            deck[i].setCardNumber(j);
        }

        // We are using Fisher-Yates shuffle algorithm to shuffle the cards around:
        // Algorithm can be read in detail here: https://www.geeksforgeeks.org/shuffle-a-given-array-using-fisher-yates-shuffle-algorithm/

        Random r = new Random();
        for(int i = numberOfCards-1; i>0; i--){
            int rand = r.nextInt(i+1);    // Default bound goes from [0,i+1) -> [0,i]

            chanceCard temp = deck[i];          // Temp is a placeholder, something we need for a swap.
            deck[i] = deck[rand];
            deck[rand] = temp;
        }
    }

    /* popCard()
    *  Since a low amount of cards are being used we are satisfied to use an array and not a dynamic datastructure.
    *  This segment simply puts every card one step back and puts the card that the player picks up back last into
    *  the fold, once he or she has read it:
    */

    public chanceCard popCard(){
        chanceCard c = deck[0];
        for(int i = 0; i < numberOfCards-1; i++){
            deck[i] = deck[i+1];
        }
        deck[numberOfCards-1] = c;

        return c;
    }
}
