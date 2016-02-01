import java.io.*;
import java.util.*;

public class Convert {

    public DataInputStream dis;
    public PrintWriter out;

    public void run(String filename) {
        try {
            String[] name = filename.split("\\.");
            dis = new DataInputStream(new FileInputStream(filename));
            out = new PrintWriter(name[0] + ".txt");
            double x;
            while(dis.available() > 0) {
                x = dis.readDouble();
                out.println(x);
            }
            dis.close();
        } catch(Exception e) {
            e.printStackTrace();
        } finally {
            out.close();
        }

    }

    public static void main(String[] args) {
        String filename = args[0];
        new Convert().run(filename);
    }
}
