import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        // 여기에 코드를 작성해주세요.
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt();
        if ((a%2!=0 && a%3==0)||(a%2==0 && a%5==0)){
            System.out.print("true");
        }
        else{
            System.out.print("false");
        }
    }
}