import java.io.BufferedOutputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.io.Reader;
import java.util.HashMap;
import java.util.PriorityQueue;
import java.util.StringTokenizer;

public class redistricting {
	static final String problem = "redistricting";
	static final boolean testing = !new File(problem + ".in").exists();

	public static void main(String args[]) throws Exception {
		PrintStream out = new PrintStream(
				new BufferedOutputStream(testing ? System.out : new FileOutputStream(problem + ".out")));
		BufferedScanner in = new BufferedScanner(
				testing ? new InputStreamReader(System.in) : new FileReader(problem + ".in"));

		int N = in.nextInt(), K = in.nextInt();
		String cows = in.next();

		int[] hLp = new int[N + 1];
		int[] gLp = new int[N + 1];

		for (int i = 1; i <= cows.length(); i++) {
			if (cows.charAt(i - 1) == 'H') hLp[i]++;
			else gLp[i]++;

			if (i != 0) {
				hLp[i] += hLp[i - 1];
				gLp[i] += gLp[i - 1];
			}
		}

		int[] DP = new int[N + 1];
		ST norm = new ST(0, N + 1);
		ST aug = new ST(0, 2 * N);

		HashMap<Integer, PriorityQueue<PII>> augData = new HashMap<>();
		for (int i = 0; i <= 2 * N; i++) {
			PriorityQueue<PII> curr = new PriorityQueue<>((a, b) -> a.n - b.n);
			augData.put(i, curr);
			curr.add(PII.max);
		}

		aug.update(N, new PII(0));
		augData.get(N).add(new PII(0));
		norm.update(0, new PII(0));
		for (int i = 1; i < DP.length; i++) {
			int start = Math.max(i - K, 0);

			if (start - 1 >= 0) {
				int val = hLp[start - 1] - gLp[start - 1] + N;
				augData.get(val).remove(new PII(DP[start - 1]));
				aug.update(val, augData.get(val).peek());
			}

			int ans = norm.query(start, i).n + 1;
			ans = Math.min(ans, aug.query(0, hLp[i] - gLp[i] - 1 + N).n);

			int val = hLp[i] - gLp[i] + N;
			augData.get(val).add(new PII(ans));
			aug.update(val, augData.get(val).peek());

			norm.update(i, new PII(ans));
			DP[i] = ans;
		}
		out.println(DP[N]);

		in.close();
		out.close();
	}

	static class PII {
		final int n;

		PII(int n) {
			this.n = n;
		}

		public PII combine(PII o) {
			return this.n < o.n ? this : o;
		}

		@Override
		public boolean equals(Object o) {
			return ((PII) o).n == this.n;
		}

		static PII init = new PII(Integer.MAX_VALUE - 1);
		static PII max = new PII(Integer.MAX_VALUE - 1);

		@Override
		public String toString() {
			return "[" + this.n + "]";
		}
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

	static class BufferedScanner {
		private BufferedReader in;
		private StringTokenizer st;

		BufferedScanner(Reader in) throws IOException {
			this.in = new BufferedReader(in);
			st = new StringTokenizer(this.in.readLine());
		}

		int nextInt() throws IOException {
			return Integer.parseInt(next());
		}

		String next() throws IOException {
			if (!st.hasMoreElements()) st = new StringTokenizer(in.readLine());

			return st.nextToken();
		}

		void close() throws IOException {
			in.close();
		}

	}
}