import java.io.IOException;
import java.net.ServerSocket;
import java.util.ArrayList;
import java.util.Arrays;

/* Server
 * The purpose of this class is simplified in one sentence: STORE ALL PERSISTANT DATA.
 * To elaborate on that, what we are doing is to store information such as where are the players, what are their money, their
 * properties etc.
 */
public class Server {

    private static int connectionPort = 8989;
    private static int players = 0;
    private player[] playerList = {new player(0), new player(0), new player(0), new player(0)};
    private game game = new game();
    private int turn = 1;
    private game globalGame = new game();

    public int getTurn(){
        return turn;
    }


    public void endTurn(game g){
        turn += 1;
        globalGame = g;

        if(turn == 5){
            turn = 1;
        }
    }

    /* increasePlayers()
     * Increasing the amount of players and adding the player to the list.
    */

    public void increasePlayers(){
        players += 1;
        playerList[players - 1] = new player(players);
    }

    /* getGame()
     * returns the game object.
    */
    public game getGame(){
        return game;
    }

    /* setPlayer()
     * This method sets the player with the id n to be the player p.
     * Note: The indexing is zero-indexing as such we subtract one so that the id matches the index.
    */

    public void setPlayer(int n, player p){
        playerList[n-1] = p;
        //playerList.set(n-1, p);
    }

    /* getPlayer()
     * This getter method is likewise a zero-index method that uses a subtraction with one as an offset.
    */
    public player getPlayer(int n){
        return playerList[n-1];
        //return playerList.get(n-1);
    }

    // Getters for the playerlist and for the number of players.
    public int get_player_number(){
        return players;
    }

    public void go() throws IOException {
        ServerSocket serverSocket = null;
        boolean listening = true;

        // Checks if the connection port is already in use somewhere else:
        try {
            serverSocket = new ServerSocket(connectionPort);
        } catch (IOException e) {
            System.err.println("Could not listen on port: " + connectionPort);
            System.exit(1);
        }

        System.out.println("Game server started listening on port: " + connectionPort);

        while (listening)
            new serverThread(this, serverSocket.accept()).start();

        serverSocket.close();
    }
}