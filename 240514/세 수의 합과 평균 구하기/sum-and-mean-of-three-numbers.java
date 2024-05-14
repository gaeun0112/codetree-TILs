import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt(), b = sc.nextInt(), c = sc.nextInt();

        System.out.printf("%d \n%.0f",a+b+c, ((double) (a+b+c)/3));
    }
}