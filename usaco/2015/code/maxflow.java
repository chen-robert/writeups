import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Scanner;

public class maxflow {
	public static void main(String args[]) throws Exception {
		boolean testing = false;// !new File("maxflow.in").exists();
		Scanner in = new Scanner(testing ? System.in : new FileInputStream("maxflow.in"));
		PrintStream out = new PrintStream(testing ? System.out : new FileOutputStream("maxflow.out"));

		int N = in.nextInt(), K = in.nextInt();
		ArrayList<HashSet<Integer>> adj = new ArrayList<>();

		for (int i = 0; i < N; i++) {
			adj.add(new HashSet<>());
		}

		for (int i = 0; i < N - 1; i++) {
			int a = in.nextInt() - 1;
			int b = in.nextInt() - 1;

			adj.get(a).add(b);
			adj.get(b).add(a);
		}

		ArrayList<HashSet<Point>> queries = new ArrayList<>();
		for (int i = 0; i < N; i++) {
			queries.add(new HashSet<>());
		}

		for (int i = 0; i < K; i++) {
			int a = in.nextInt() - 1;
			int b = in.nextInt() - 1;

			Point p = new Point(a, b);

			queries.get(a).add(p);
			queries.get(b).add(p);
		}

		int[] p = new int[adj.size()];

		makeDAG(0, adj, p);
		p[0] = adj.size();

		int[] deltas = new int[adj.size() + 1];
		TarjanLCA(adj, queries, deltas, p);

		ArrayList<Integer> revTopSort = new ArrayList<>();
		reverseTopsort(0, adj, revTopSort);

		int max = -1;
		int[] flows = new int[adj.size()];
		for (Integer u : revTopSort) {
			flows[u] += deltas[u];
			for (Integer v : adj.get(u)) {
				flows[u] += flows[v];
			}

			max = Math.max(flows[u], max);
		}
		out.println(max);

		in.close();
		out.close();
	}

	static class Point {
		int x;
		int y;

		Point(int x, int y) {
			this.x = x;
			this.y = y;
		}
	}

	public static void reverseTopsort(int u, ArrayList<HashSet<Integer>> adj, ArrayList<Integer> ret) {
		for (Integer v : adj.get(u)) {
			reverseTopsort(v, adj, ret);
		}
		ret.add(u);
	}

	public static void makeDAG(int u, ArrayList<HashSet<Integer>> adj, int[] p) {
		for (Integer v : adj.get(u)) {
			adj.get(v).remove(new Integer(u));
			p[v] = u;
		}

		for (Integer v : adj.get(u)) {
			makeDAG(v, adj, p);
		}
	}

	public static void TarjanLCA(ArrayList<HashSet<Integer>> adj, ArrayList<HashSet<Point>> qs, int[] deltas, int[] p) {
		LCAHelper(0, adj, qs, new DS(adj.size()), new int[adj.size()], new boolean[adj.size()], deltas, p);
	}

	public static void LCAHelper(int u, ArrayList<HashSet<Integer>> adj, ArrayList<HashSet<Point>> qs, DS ds,
			int[] ancestors, boolean[] vis, int[] deltas, int[] parents) {
		ancestors[ds.group(u)] = u;

		for (Integer v : adj.get(u)) {
			LCAHelper(v, adj, qs, ds, ancestors, vis, deltas, parents);

			ds.join(u, v);
			ancestors[ds.group(u)] = u;
		}
		vis[u] = true;

		HashSet<Point> done = new HashSet<>();
		for (Point p : qs.get(u)) {
			if (p.x == -1) {
				return;
			}
			int v = p.x == u ? p.y : p.x;

			if (vis[v]) {
				int lca = ancestors[ds.group(v)];

				deltas[u]++;
				deltas[v]++;
				deltas[lca]--;
				deltas[parents[lca]]--;

				done.add(p);
			}
		}
		for (Point p : done) {
			qs.get(p.x).remove(p);
			qs.get(p.y).remove(p);
		}

	}

	private static class DS {
		public int[] parents;

		public DS(int n) {
			parents = new int[n];
			for (int i = 0; i < parents.length; i++) {
				parents[i] = i;
			}
		}

		public boolean join(int a, int b) {
			a = group(a);
			b = group(b);

			parents[a] = b;

			return a == b;
		}

		public int group(int n) {
			int ori = n;
			while (parents[n] != n) {
				n = parents[n];
			}

			while (parents[ori] != ori) {
				int tmp = parents[ori];

				parents[ori] = n;
				ori = tmp;
			}
			return n;
		}

		public boolean same(int a, int b) {
			return group(a) == group(b);
		}
	}
}
