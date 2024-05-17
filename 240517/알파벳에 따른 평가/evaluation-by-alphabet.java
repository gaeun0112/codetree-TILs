import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        // 여기에 코드를 작성해주세요.
        Scanner sc = new Scanner(System.in);
        char a = sc.next().charAt(0);
        if (a=='S'){
            System.out.print("Superior");
        }
        else if (a=='A'){
            System.out.print("Exellent");
        }
        else if (a=='B'){
            System.out.print("Good");
        }
        else if (a=='C'){
            System.out.print("Usually");
        }
        else if (a=='D'){
            System.out.print("Effort");
        }
        else {
            System.out.print("Failure");
        }
    }
}