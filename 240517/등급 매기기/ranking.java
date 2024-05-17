import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        // 여기에 코드를 작성해주세요.
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        if (n>=90){
            System.out.print("A");
        }
        else if (n>=80){
            System.out.print("B");
        }
        else if (n>=70){
            System.out.print("C");
        }
        else if (n>=60){
            System.out.print("D");
        }
        else {
            System.out.print("F");
        }
    }
}