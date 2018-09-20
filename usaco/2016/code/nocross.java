import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.Scanner;

public class nocross {
	public static void main(String args[]) throws Exception {
		boolean testing = new File("nocross.in").exists();
		Scanner in = new Scanner(testing ? new FileInputStream("nocross.in") : System.in);
		PrintStream out = new PrintStream(testing ? new FileOutputStream("nocross.out") : System.out);

		int N = in.nextInt();

		int[] a = new int[N];
		int[] bLp = new int[N];
		for (int i = 0; i < N; i++) {
			a[i] = in.nextInt() - 1;
		}
		for (int i = 0; i < N; i++) {
			bLp[in.nextInt() - 1] = i;
		}

		RMQ rmq = new RMQ(N);
		for (int i = 0; i < N; i++) {
			int l = Math.max(0, a[i] - 4);
			int r = Math.min(N - 1, a[i] + 4);

			int[] todo = new int[r - l + 1];
			Arrays.fill(todo, -1);
			for (int j = l; j <= r; j++) {
				int curr = 1;
				if (bLp[j] != 0) {
					curr = 1 + rmq.query(0, bLp[j] - 1);
				}
				if (rmq.query(bLp[j], bLp[j]) < curr) {
					todo[j - l] = curr;
				}
			}

			for (int j = 0; j < todo.length; j++) {
				if (todo[j] != -1) {
					rmq.update(bLp[l + j], todo[j]);
				}
			}
		}

		out.println(rmq.query(0, N - 1));

		in.close();
		out.close();
	}

	static class RMQ {
		int[] tree;
		int n;

		public RMQ(int n) {
			n = (int) Math.pow(2, Math.ceil(Math.log(n) / Math.log(2)));
			tree = new int[2 * n - 1];
			Arrays.fill(tree, 0);

			this.n = n;
		}

		public void update(int idx, int k) {
			int curr = idx + n - 1;

			tree[curr] = k;

			while (curr > 0) {
				curr = p(curr);

				recalc(curr);
			}
		}

		public int query(int left, int right) {
			return query(0, left, right, 0, n - 1);
		}

		public int query(int idx, int ql, int qr, int il, int ir) {
			if (ql <= il && ir <= qr) {
				return tree[idx];
			}
			int ret = Integer.MIN_VALUE;
			int mid = (il + ir) / 2;

			if (ql <= mid) {
				ret = query(l(idx), ql, qr, il, mid);
			}
			if (qr >= mid + 1) {
				ret = Math.max(ret, query(r(idx), ql, qr, mid + 1, ir));
			}
			return ret;
		}

		public void recalc(int idx) {
			if (valid(l(idx))) {
				tree[idx] = tree[l(idx)];
				if (valid(r(idx))) {
					tree[idx] = Math.max(tree[idx], tree[r(idx)]);
				}
			}
		}

		public boolean valid(int n) {
			return n < tree.length;
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
	}
}
