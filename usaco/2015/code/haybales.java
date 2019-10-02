import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.Scanner;

public class haybales {
	public static void main(String args[]) throws Exception {
		boolean inContest = true;
		Scanner in = new Scanner(
				inContest ? new BufferedInputStream(new FileInputStream(new File("haybales.in"))) : System.in);
		PrintStream out = new PrintStream(
				inContest ? new BufferedOutputStream(new FileOutputStream(new File("haybales.out"))) : System.out);

		int N = in.nextInt();
		int Q = in.nextInt();
		LazySegTree tree = new LazySegTree(N);

		for (int i = 0; i < N; i++) {
			tree.update(i, in.nextInt());
		}
		for (int i = 0; i < Q; i++) {
			char c = in.next().charAt(0);

			switch (c) {
			case 'M':
				out.println(tree.query(in.nextInt() - 1, in.nextInt() - 1, true));
				break;
			case 'S':
				out.println(tree.query(in.nextInt() - 1, in.nextInt() - 1, false));
				break;
			case 'P':
				tree.update(in.nextInt() - 1, in.nextInt() - 1, in.nextInt());
				break;
			}
		}
		out.close();
		in.close();
	}

	public static class LazySegTree {
		long[] tree;
		long[] sums;
		long[] lazy;
		int n;

		public LazySegTree(int n) {
			n = (int) Math.pow(2, Math.ceil(Math.log(n) / Math.log(2)));

			tree = new long[2 * n - 1];
			sums = new long[tree.length];
			lazy = new long[tree.length];

			Arrays.fill(tree, Long.MAX_VALUE);

			this.n = n;
		}

		public void update(int idx, int k) {
			int curr = idx + n - 1;

			tree[curr] = k;
			sums[curr] = k;

			while (curr > 0) {
				curr = p(curr);

				recalc(curr);
			}
		}

		void processLazy(int idx, int intWidth) {
			if (lazy[idx] != 0) {
				tree[idx] += lazy[idx];
				sums[idx] += intWidth * lazy[idx];

				if (valid(l(idx))) {
					lazy[l(idx)] += lazy[idx];
				}
				if (valid(r(idx))) {
					lazy[r(idx)] += lazy[idx];
				}
				lazy[idx] = 0;
			}
		}

		public void update(int left, int right, int diff) {
			update(0, 0, n - 1, diff, left, right);
		}

		public void update(int idx, int il, int ir, int diff, int ql, int qr) {
			if (ql <= il && ir <= qr) {
				lazy[idx] += diff;
			}
			processLazy(idx, ir - il + 1);

			// Current interval is outside of query
			if (il > qr || ir < ql || (ql <= il && ir <= qr)) {
				return;
			}

			int mid = (il + ir) / 2;
			update(l(idx), il, mid, diff, ql, qr);
			update(r(idx), mid + 1, ir, diff, ql, qr);

			recalc(idx);
		}

		public long query(int left, int right, boolean rmq) {
			return query(0, left, right, 0, n - 1, rmq);
		}

		/**
		 *
		 * @param idx
		 * @param ql
		 *            Query left
		 * @param qr
		 *            Query right
		 * @param il
		 *            Interval left (of interval at idx)
		 * @param ir
		 *            Interval right
		 * @param rmq
		 *            Is this a range min query
		 * @return
		 */
		public long query(int idx, int ql, int qr, int il, int ir, boolean rmq) {
			processLazy(idx, ir - il + 1);

			if (ql <= il && ir <= qr) {
				return rmq ? tree[idx] : sums[idx];
			}
			long ret = rmq ? Long.MAX_VALUE : 0;
			int mid = (il + ir) / 2;

			if (ql <= mid) {
				ret = query(l(idx), ql, qr, il, mid, rmq);
			}
			if (qr >= mid + 1) {
				long val = query(r(idx), ql, qr, mid + 1, ir, rmq);

				ret = rmq ? Math.min(ret, val) : ret + val;
			}
			return ret;
		}

		public void recalc(int idx) {
			if (valid(l(idx))) {
				tree[idx] = tree[l(idx)];
				sums[idx] = sums[l(idx)];
				if (valid(r(idx))) {
					tree[idx] = Math.min(tree[idx], tree[r(idx)]);
					sums[idx] += sums[r(idx)];
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
