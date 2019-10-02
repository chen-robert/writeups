import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.*;

/**
 * Created by Robert on 8/6/2018.
 */
public class promote {
    static ArrayList<HashSet<Integer>> adj;
    static int[] ret;
    static int[] ratings;

    public static void main(String[] args) throws Exception {
        boolean testing = !new File("promote.in").exists();
        Scanner in = new Scanner(testing ? System.in : new FileInputStream("promote.in"));
        PrintStream out = new PrintStream(testing ? System.out : new FileOutputStream("promote.out"));

        int N = in.nextInt();
        ratings = new int[N];
        for (int i = 0; i < N; i++) {
            ratings[i] = in.nextInt();
        }

        int[] ratingsCopy = ratings.clone();
        Arrays.sort(ratingsCopy);

        HashMap<Integer, Integer> lp = new HashMap<>();
        for (int i = 0; i < N; i++) {
            lp.put(ratingsCopy[i], i);
        }
        for (int i = 0; i < N; i++) {
            ratings[i] = lp.get(ratings[i]);
        }

        adj = new ArrayList<>();
        for (int i = 0; i < N; i++) {
            adj.add(new HashSet<>());
        }
        for (int i = 1; i < N; i++) {
            adj.get(in.nextInt() - 1).add(i);
        }

        ret = new int[N];

        visit(new BIT(), 0);

        for (int i = 0; i < N; i++) {
            out.println(ret[i]);
        }

        in.close();
        out.close();
    }

    public static void visit(BIT base, int curr) {
        int prev = base.count - base.query(ratings[curr]);
        for (Integer v : adj.get(curr)) {
            visit(base, v);
        }

        ret[curr] = base.count - base.query(ratings[curr]) - prev;
        base.update(ratings[curr]);
    }

    static class BIT {
        public static int size = 100000 + 1;

        public int[] mem = new int[size];

        int count = 0;

        public void update(int n) {
            count++;
            for (int i = n + 1; i < mem.length; i += lsOne(i)) mem[i] += 1;
        }

        //Sum from 0 - n inclusive
        public int query(int n) {
            int ret = 0;
            for (int i = n + 1; i > 0; i -= lsOne(i)) ret += mem[i];

            return ret;
        }

        public int query(int l, int r) {
            return query(r) - query(l - 1);
        }

        public int lsOne(int n) {
            return -n & n;
        }
    }

}
