import java.io.IOException;

/* Server
 *  This is the object that is being called as an instance by the main programme, mainServer.java.
 *  This Server instance simply has two jobs
 *  1. Be on a infinite loop (seen in the go() function), listening to all clients that want to connect to the server.
 *  2. Store all the global data in this instance, so that we can have persistent data through all the serverThreads (and clients)
 *  When a connection is made, this object is passed down as a reference into the serverThread, which is where we have client - Server connection.
 *  If the client requests something valid from the serverThread, the serverThread will then pass this information up to this object.

 *  Example: Two clients connect, client 1 and client 2. The go() function will catch both of them and create two serverThreads for them we can call
 *  them serverThread1 and serverThread2.
 */


public class mainServer extends Thread{

    public static void main(String[]args) throws IOException {
        Server serv = new Server();
        serv.go();
    }

}