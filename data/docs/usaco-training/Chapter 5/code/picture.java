
/*
TASK: picture
LANG: JAVA
ID: robertc5
 */

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.Scanner;

/**
 * Created by Robert on 7/4/2018.
 */
public class picture {
	public static void main(String arg[]) throws Exception {
		boolean testing = !new File("picture.in").exists();

		Scanner in = new Scanner(testing ? System.in : new BufferedInputStream(new FileInputStream("picture.in")));
		PrintStream out = new PrintStream(
				testing ? System.out : new BufferedOutputStream(new FileOutputStream("picture.out")));

		int N = in.nextInt();
		Edge[] horiz = new Edge[2 * N];
		Edge[] vert = new Edge[2 * N];
		for (int i = 0; i < N; i++) {
			int lx = in.nextInt(), ly = in.nextInt();
			int rx = in.nextInt(), ry = in.nextInt();

			lx = 2 * lx - 1;
			ly = 2 * ly - 1;
			rx = 2 * rx - 1;
			ry = 2 * ry - 1;

			horiz[2 * i] = new Edge(lx, rx, ly, false);
			horiz[2 * i + 1] = new Edge(lx, rx, ry, true);

			vert[2 * i] = new Edge(ly, ry, lx, false);
			vert[2 * i + 1] = new Edge(ly, ry, rx, true);
		}

		int ret = solve(horiz) + solve(vert);

		out.println(ret / 2);

		in.close();
		out.close();
	}

	static int SIZE = 20000;
	static IntervalTree tree = new IntervalTree(2 * SIZE);

	public static int solve(Edge[] edges) {
		Arrays.sort(edges, (a, b) -> a.z - b.z);
		int ret = 0;
		int prev = 0;

		int count = 0;

		for (Edge e : edges) {
			int prevIntCount = tree.condense();

			ret += prevIntCount * (e.z - prev);
			prev = e.z;

			if (e.end) {
				// Is the end of an interval
				tree.update(e.a, e.b, -1);
				count--;
			} else {
				tree.update(e.a, e.b, 1);
				count++;
			}
		}
		return ret;
	}

	static class Interval {
		int s;
		int e;

		Interval(int s, int e) {
			this.s = s;
			this.e = e;
		}
	}

	static class Edge {
		int a, b, z;
		boolean end;

		Edge(int a, int b, int z, boolean end) {
			if (a > b) {
				int c = b;
				b = a;
				a = c;
			}
			this.a = a;
			this.b = b;
			this.z = z;
			this.end = end;
		}
	}

	static class IntervalTree {
		int[] cs, ip;
		boolean[] cl, cu;

		int n;

		public IntervalTree(int n) {
			n = (int) Math.pow(2, Math.ceil(Math.log(n) / Math.log(2)));

			cs = new int[2 * n - 1];
			ip = new int[2 * n - 1];
			cl = new boolean[2 * n - 1];
			cu = new boolean[2 * n - 1];

			this.n = n;
		}

		public void update(int left, int right, int diff) {
			left += SIZE;
			right += SIZE;

			update(0, 0, n - 1, diff, left, right);
		}

		/**
		 * @param idx
		 *            Index
		 * @param il
		 *            Left bound of interval at idx
		 * @param ir
		 *            Right bound of interval at idx
		 * @param delta
		 *            Amount to update each element in (ul, ur) by
		 * @param ul
		 *            Left bound of update interval
		 * @param ur
		 *            Right bound of update interval
		 */
		public void update(int idx, int il, int ir, int delta, int ul, int ur) {
			// If completely contained, change current update counter
			if (ul <= il && ir <= ur) {
				cs[idx] += delta;
				recalc(idx);
				return;
			}

			if (il > ur || ir < ul || (ul <= il && ir <= ur)) {
				return;
			}

			// Recursively called upon child nodes
			int mid = (il + ir) / 2;
			update(l(idx), il, mid, delta, ul, ur);
			update(r(idx), mid + 1, ir, delta, ul, ur);

			// Recalculate current node
			recalc(idx);
		}

		public void recalc(int idx) {
			if (cs[idx] == 0) {
				if (valid(r(idx))) {
					cl[idx] = cl[l(idx)];
					cu[idx] = cu[r(idx)];

					ip[idx] = ip[l(idx)] + ip[r(idx)] + (cu[l(idx)] == cl[r(idx)] ? 0 : 1);
				} else {
					cl[idx] = cu[idx] = false;

					ip[idx] = 0;
				}
			} else {
				cl[idx] = cu[idx] = true;

				ip[idx] = 0;
			}
		}

		public boolean valid(int n) {
			return n < cs.length;
		}

		int p(int n) {
			return (n - 1) / 2;
		}

		int l(int n) {
			return 2 * n + 1;
		}

		int r(int n) {
			return l(n) + 1;
		}

		public int condense() {
			return (cl[0] ? 1 : 0) + (cu[0] ? 1 : 0) + ip[0];
		}

	}
}
