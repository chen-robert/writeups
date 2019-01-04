
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashSet;
import java.util.Scanner;

public class itout {
	public static void main(String args[]) throws Exception {
		boolean testing = new File("itout.in").exists();
		Scanner in = new Scanner(testing ? new BufferedInputStream(new FileInputStream("itout.in")) : System.in);
		PrintStream out = new PrintStream(
				testing ? new BufferedOutputStream(new FileOutputStream("itout.out")) : System.out);

		int N = in.nextInt();
		long K = in.nextLong();
		int[] cows = new int[N];
		for (int i = 0; i < N; i++)
			cows[i] = in.nextInt();

		HashSet<Integer> compl = new HashSet<>();
		for (int i = 1; i <= N; i++)
			compl.add(i);

		for (int n : longestIncreasingSubsequence(cows, K))
			compl.remove(n);

		ArrayList<Integer> ret = new ArrayList<>(compl);
		Collections.sort(ret);

		out.println(ret.size());
		for (int a : ret)
			out.println(a);

		in.close();
		out.close();
	}

	public static int[] longestIncreasingSubsequence(int[] arr, long K) {
		ST dp = new ST(arr.length + 1);
		Arrays.fill(dp.tree, new PII(0, -1, -1, 0));
		dp.update(arr.length, new PII(0, -1, -1, 1));

		int[] lenDp = new int[arr.length];
		long[] kDp = new long[arr.length];

		for (int i = arr.length - 1; i >= 0; i--) {
			PII curr = dp.query(arr[i], arr.length);
			PII toAdd = new PII(curr.dpVal + 1, arr[i], i, curr.size);
			kDp[i] = curr.size;
			lenDp[i] = toAdd.dpVal;

			dp.update(arr[i], toAdd);
		}

		int max = Arrays.stream(lenDp).max().getAsInt();
		ArrayList<ArrayList<Integer>> lp = new ArrayList<>();
		for (int i = 0; i <= max; i++)
			lp.add(new ArrayList<>());

		for (int i = 0; i < arr.length; i++) {
			lp.get(lenDp[i]).add(arr[i]);
		}
		for (ArrayList<Integer> a : lp)
			Collections.sort(a, (b, c) -> c - b);
		int[] arrLp = new int[arr.length + 1];
		for (int i = 0; i < arr.length; i++)
			arrLp[arr[i]] = i;

		int[] ret = new int[max];
		int currI = -1;
		int currArr = -1;
		for (int i = lp.size() - 1; i >= 1; i--) {
			for (int j = 0; j < lp.get(i).size(); j++) {
				int elem = lp.get(i).get(j);
				if (elem < currArr || arrLp[elem] < currI) continue;

				if (kDp[arrLp[elem]] < K) {
					K -= kDp[arrLp[elem]];
				} else {
					ret[i - 1] = elem;
					currArr = elem;
					currI = arrLp[elem];
					break;
				}
			}
		}
		return ret;
	}

	static class PII {
		int dpVal;
		int arrVal;
		int idx;
		long size;

		PII(int a, int b, int idx, long size) {
			dpVal = a;
			arrVal = b;
			this.idx = idx;
			this.size = Math.min(size, (long) 1e18);
		}

		public boolean bigger(PII o) {
			if (o == null) return true;
			if (dpVal == o.dpVal) return arrVal > o.arrVal;
			return dpVal > o.dpVal;
		}
	}

	static class ST {

		PII[] tree;
		int n;

		public ST(int n) {
			n = (int) Math.pow(2, Math.ceil(Math.log(n) / Math.log(2)));
			tree = new PII[2 * n - 1];

			this.n = n;
		}

		public PII combine(PII a, PII b) {
			if (a == null) return b;
			if (b == null) return a;

			if (a.dpVal != b.dpVal) return a.bigger(b) ? a : b;
			long retSize = a.size + b.size;
			PII ret = a.bigger(b) ? new PII(a.dpVal, a.arrVal, a.idx, retSize)
					: new PII(b.dpVal, b.arrVal, b.idx, retSize);
			return ret;
		}

		public void update(int idx, PII k) {
			int curr = idx + n - 1;

			tree[curr] = k;

			while (curr > 0) {
				curr = p(curr);

				recalc(curr);
			}
		}

		public PII query(int left, int right) {
			return query(0, left, right, 0, n - 1);
		}

		public PII query(int idx, int ql, int qr, int il, int ir) {
			if (ql <= il && ir <= qr) return tree[idx];

			PII ret = null;
			int mid = (il + ir) / 2;

			if (ql <= mid) ret = query(l(idx), ql, qr, il, mid);
			if (qr >= mid + 1) ret = combine(query(r(idx), ql, qr, mid + 1, ir), ret);
			return ret;
		}

		public void recalc(int idx) {
			if (l(idx) < tree.length) {
				tree[idx] = tree[l(idx)];
				if (r(idx) < tree.length) {
					tree[idx] = combine(tree[idx], tree[r(idx)]);
				}
			}
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
