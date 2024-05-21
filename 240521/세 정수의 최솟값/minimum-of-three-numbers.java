import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        // 여기에 코드를 작성해주세요.
        Scanner sc = new Scanner(System.in);
        int a = sc.nextInt(), b = sc.nextInt(), c = sc.nextInt();
        int min_num = a;
        if (a>=b && c>=b){
            min_num = b;
        }
        if (a>=c && b>=c){
            min_num=c;
        }
        System.out.print(min_num);
    }
}