import java.util.Scanner;
public class Main {
    public static void main(String[] args) {
        // 여기에 코드를 작성해주세요.
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();
        if (t<0){
            System.out.print("ice");
        }
        else if (t>=100){
            System.out.print("vapor");
        }
        else{
            System.out.print("water");
        }
    }
}