import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        // 여기에 코드를 작성해주세요.
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt(), b = sc.nextInt(), c = sc.nextInt();
        int d = sc.nextInt(), e = sc.nextInt();
        if (a>b){
            System.out.println(1);
        }
        else {
            System.out.println(0);
        }
        if (a>c){
            System.out.println(1);
        }
        else {
            System.out.println(0);
        }
        if (a>d){
            System.out.println(1);
        }
        else {
            System.out.println(0);
        }
        if (a>e){
            System.out.println(1);
        }
        else {
            System.out.println(0);
        }
    }
}