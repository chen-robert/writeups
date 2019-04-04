import java.awt.*;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Scanner;

public class triangles {
    public static void main(String[] args) throws Exception {
        boolean testing = !new File("triangles.in").exists();
        Scanner in = new Scanner(testing ? System.in : new FileInputStream("triangles.in"));
        PrintStream out = new PrintStream(testing ? System.out : new FileOutputStream("triangles.out"));

        int N = in.nextInt();

        ArrayList<Point> ps = new ArrayList<>();
        for (int i = 0; i < N; i++) {
            ps.add(new Point(in.nextInt(), in.nextInt()));
        }

        int[][] lp = new int[N][N];
        for (int i = 0; i < lp.length; i++) {
            for (int j = i + 1; j < lp.length; j++) {
                for (int k = 0; k < lp.length; k++) {
                    if (k == i || k == j) continue;
                    if (under(ps.get(i), ps.get(j), ps.get(k), false)) {
                        lp[i][j]++;
                        lp[j][i]++;
                    }
                }
            }
        }

        int[] ret = new int[N-2];
        for (int i = 0; i < N; i++) {
            for (int j = i + 1; j < N; j++) {
                for (int k = j + 1; k < N; k++) {
                    int count = 0;
                    Point a = ps.get(i), b = ps.get(j), c = ps.get(k);

                    count += (under(a, b, c, true) ? 1: -1) * (lp[i][j] + (under(a, b, c, false) ? -1: 0));
                    count += (under(b, c, a, true) ? 1: -1) * (lp[j][k] + (under(b, c, a, false) ? -1: 0));
                    count += (under(c, a, b, true) ? 1: -1) * (lp[k][i] + (under(c, a, b, false) ? -1: 0));

                    ret[count]++;
                }
            }
        }

        for(int i = 0; i < ret.length; i++){
            out.println(ret[i]);
        }

        in.close();
        out.close();
    }

    public static boolean under(Point l, Point r, Point p, boolean extrapolate) {
        if(l.x > r.x){
            Point tmp = l;
            l = r;
            r = tmp;
        }
        if (l.x == r.x) {
            return p.x == l.x;
        }
        if (!extrapolate && (p.x < l.x || r.x <= p.x)) return false;
        double slope = 1.0 * (r.y - l.y) / (r.x - l.x);

        double expectedY = slope * (p.x - l.x) + l.y;
        return p.y < expectedY;
    }
}
