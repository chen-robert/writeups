import java.awt.Point;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;

public class exercise {
	static int[] depth;
	static int[] p;
	static ArrayList<ArrayList<Integer>> adj = new ArrayList<>();

	static int[][] parents;

	static long vals[];

	static long runningVals[];

	public static void main(String args[]) throws Exception {
		boolean testing = !new File(".classpath").exists();
		Scanner in = new Scanner(new FileInputStream("exercise.in"));
		PrintStream out = new PrintStream(testing ? new FileOutputStream("exercise.out") : System.out);

		int N = in.nextInt(), M = in.nextInt();
		depth = new int[N];
		p = new int[N];
		vals = new long[N];
		runningVals = new long[N];

		parents = new int[N][20];

		for (int i = 0; i < N; i++)
			adj.add(new ArrayList<>());

		for (int i = 0; i < N - 1; i++) {
			int f = in.nextInt() - 1;
			int t = in.nextInt() - 1;

			adj.get(f).add(t);
			adj.get(t).add(f);
		}

		dfs(0, -1, 0);
		precompute();

		ArrayList<int[]> queries = new ArrayList<>();

		long ans = 0;
		HashMap<Point, Integer> lp = new HashMap<>();
		for (int i = 0; i < M - (N - 1); i++) {
			int f = in.nextInt() - 1;
			int t = in.nextInt() - 1;

			int lca = lca(f, t);

			queries.add(new int[] { f, t, lca });

			int topF = topEdge(lca, f);
			int topT = topEdge(lca, t);
			if (f != lca) {
				vals[topF]++;
				ans -= vals[topF];
			}
			if (t != lca) {
				vals[topT]++;
				ans -= vals[topT];
			}
			if (f != lca && t != lca) {
				if (topF > topT) {
					int tmp = topF;
					topF = topT;
					topT = tmp;
				}
				Point curr = new Point(topF, topT);
				if (!lp.containsKey(curr)) lp.put(curr, 0);
				ans -= lp.get(curr);
				lp.put(curr, lp.get(curr) + 1);
			}
		}
		dfsCount(0, 0);

		for (int[] q : queries) {
			int f = q[0], t = q[1], lca = q[2];
			ans += runningVals[f] + runningVals[t] - 2 * runningVals[lca];
		}

		out.println(ans);

		out.close();
		in.close();
	}

	static void dfsCount(int curr, long count) {
		count += vals[curr];
		runningVals[curr] = count;

		for (Integer n : adj.get(curr)) {
			if (n != p[curr]) dfsCount(n, count);
		}
	}

	static int topEdge(int top, int bot) {
		if (top == bot) return -1;

		for (int i = 19; i >= 0; i--)
			if (parents[bot][i] != -1 && depth[parents[bot][i]] > depth[top]) bot = parents[bot][i];
		return bot;
	}

	static void precompute() {
		for (int i = 0; i < p.length; i++)
			parents[i][0] = p[i];

		for (int j = 1; j < 20; j++) {
			for (int i = 0; i < p.length; i++) {
				if (parents[i][j - 1] == -1) {
					parents[i][j] = -1;
				} else {
					parents[i][j] = parents[parents[i][j - 1]][j - 1];
				}
			}
		}
	}

	static int lca(int a, int b) {
		for (int i = 19; i >= 0; i--) {
			if (parents[a][i] != -1 && depth[parents[a][i]] >= depth[b]) a = parents[a][i];
		}
		for (int i = 19; i >= 0; i--) {
			if (parents[b][i] != -1 && depth[parents[b][i]] >= depth[a]) b = parents[b][i];
		}
		if (a == b) return a;

		for (int i = 19; i >= 0; i--) {
			if (parents[a][i] != parents[b][i]) {
				a = parents[a][i];
				b = parents[b][i];
			}
		}
		return parents[a][0];
	}

	static void dfs(int curr, int par, int d) {
		p[curr] = par;
		depth[curr] = d;

		for (Integer n : adj.get(curr))
			if (n != par) dfs(n, curr, d + 1);
	}
}
