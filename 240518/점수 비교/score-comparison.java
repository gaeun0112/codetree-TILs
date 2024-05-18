import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        // 여기에 코드를 작성해주세요.
        Scanner sc = new Scanner(System.in);
        int math_a = sc.nextInt(), eng_a = sc.nextInt();
        int math_b = sc.nextInt(), eng_b = sc.nextInt();
        if (math_a>math_b && eng_a>eng_b){
            System.out.print(1);
        }
        else{
            System.out.print(0);
        }
    }
}