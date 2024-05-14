import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        sc.useDelimiter("\\.");
        int y = sc.nextInt(), m = sc.nextInt(), d = sc.nextInt();
        System.out.printf("%d-%d-%d",m,d,y);
    }
}