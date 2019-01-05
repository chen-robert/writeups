
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
		ST dp = new ST(0, arr.length);
		dp.update(arr.length, new PII(0, 1));

		int[] lenDp = new int[arr.length];
		long[] kDp = new long[arr.length];

		for (int i = arr.length - 1; i >= 0; i--) {
			PII curr = dp.query(arr[i], arr.length);
			PII toAdd = new PII(curr.dpVal + 1, curr.size);
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
		final int dpVal;
		final long size;

		PII(int a, long size) {
			dpVal = a;
			this.size = Math.min(size, (long) 1e18);
		}

		public PII combine(PII o) {
			if (this.dpVal == o.dpVal) {
				return new PII(this.dpVal, this.size + o.size);
			}
			return this.dpVal > o.dpVal ? this : o;
		}

		static PII init = new PII(0, 0);
		static PII max = init;
	}

	static class ST {
		PII val = PII.init;
		int il, ir;

		ST pl, pr;

		public ST(int il, int ir) {
			this.il = il;
			this.ir = ir;
		}

		void expand() {
			if (pl != null) return;

			int mid = (il + ir) / 2;
			pl = new ST(il, mid);
			pr = new ST(mid + 1, ir);
		}

		public void update(int idx, PII k) {
			if (idx == il && ir == idx) {
				val = k;
				return;
			}
			if (idx > ir || il > idx) return;

			expand();
			pl.update(idx, k);
			pr.update(idx, k);

			val = pl.val.combine(pr.val);
		}

		public PII query(int ql, int qr) {
			if (ql <= il && ir <= qr) return val;
			if (ql > ir || il > qr) return PII.max;

			expand();
			return pl.query(ql, qr).combine(pr.query(ql, qr));
		}
	}
}
