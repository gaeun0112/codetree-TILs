import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt(), b = sc.nextInt();
        a += 8;
        b *=3;
        System.out.printf("%d\n%d\n%d",a,b,a*b);
    }
}