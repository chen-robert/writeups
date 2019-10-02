import java.awt.Point;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Scanner;
import java.util.TreeSet;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class disrupt {
	static ArrayList<ArrayList<Integer>> adj;
	static int[] p;
	static HashMap<Integer, ArrayList<Thing>> maps;

	static HashMap<Integer, Integer> ans = new HashMap<>();

	public static void main(String args[]) throws Exception {
		boolean testing = new File("disrupt.in").exists();
		Scanner in = new Scanner(testing ? new FileInputStream("disrupt.in") : System.in);
		PrintStream out = new PrintStream(testing ? new FileOutputStream("disrupt.out") : System.out);

		int N = in.nextInt(), M = in.nextInt();

		p = new int[N];
		adj = new ArrayList<>(Stream.generate(ArrayList<Integer>::new).limit(N).collect(Collectors.toList()));

		ArrayList<Point> edges = new ArrayList<>();
		for (int i = 0; i < N - 1; i++) {
			int f = in.nextInt() - 1;
			int t = in.nextInt() - 1;

			adj.get(f).add(t);
			adj.get(t).add(f);

			edges.add(new Point(f, t));
		}
		dfs(0, -1);

		maps = new HashMap<>();
		for (int i = 0; i < N; i++)
			maps.put(i, new ArrayList<>());

		for (int i = 0; i < M; i++) {
			int f = in.nextInt() - 1;
			int t = in.nextInt() - 1;
			int r = in.nextInt();

			Thing curr = new Thing(new Point(f, t), r);

			maps.get(f).add(curr);
			maps.get(t).add(curr);
		}

		explore(0, new TreeSet<Thing>((a, b) -> a.b - b.b));

		for (Point e : edges) {
			int val = e.y;
			if (p[e.x] == e.y) {
				val = e.x;
			}

			out.println(ans.get(val));
		}

		out.close();
		in.close();
	}

	static class Thing {
		Point a;
		int b;

		Thing(Point a, int b) {
			this.a = a;
			this.b = b;
		}

		@Override
		public boolean equals(Object o) {
			return ((Thing) o).a.equals(a);
		}
	}

	static TreeSet<Thing> explore(int curr, TreeSet<Thing> vals) {
		vals.addAll(maps.get(curr));

		for (Integer n : adj.get(curr)) {
			if (n != p[curr]) {
				TreeSet<Thing> sub = explore(n, new TreeSet<Thing>((a, b) -> a.b - b.b));

				if (sub.size() > vals.size()) {
					TreeSet<Thing> tmp = vals;
					vals = sub;
					sub = tmp;
				}

				for (Thing p : sub) {
					if (vals.contains(p)) vals.remove(p);
					else vals.add(p);
				}
			}
		}

		if (vals.isEmpty()) {
			ans.put(curr, -1);
		} else {
			ans.put(curr, vals.first().b);
		}

		return vals;
	}

	static void dfs(int curr, int pv) {
		p[curr] = pv;

		for (Integer n : adj.get(curr))
			if (n != pv) dfs(n, curr);
	}

}
