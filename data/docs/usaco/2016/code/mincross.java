import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Scanner;

public class mincross {
	public static void main(String args[]) throws Exception {
		boolean testing = new File("mincross.in").exists();
		Scanner in = new Scanner(testing ? new FileInputStream("mincross.in") : System.in);
		PrintStream out = new PrintStream(testing ? new FileOutputStream("mincross.out") : System.out);

		int N = in.nextInt();

		int[] a = new int[N];
		int[] aLp = new int[N];
		int[] b = new int[N];
		int[] bLp = new int[N];

		for (int i = 0; i < N; i++) {
			int curr = in.nextInt() - 1;
			a[i] = curr;
			aLp[curr] = i;
		}
		for (int i = 0; i < N; i++) {
			int curr = in.nextInt() - 1;
			b[i] = curr;
			bLp[curr] = i;
		}

		long curr = crossing(a, bLp);
		long ret = Long.MAX_VALUE;
		for (int i = N - 1; i >= 0; i--) {
			ret = Math.min(ret, curr);

			int oppPos = bLp[a[i]];
			curr += 2 * oppPos - N + 1;
		}
		for (int i = N - 1; i >= 0; i--) {
			ret = Math.min(ret, curr);

			int oppPos = aLp[b[i]];
			curr += 2 * oppPos - N + 1;
		}
		out.println(ret);

		in.close();
		out.close();
	}

	public static long crossing(int[] a, int[] bLp) {
		long ret = 0;
		BIT bit = new BIT();
		for (int i = a.length - 1; i >= 0; i--) {
			int oppPos = bLp[a[i]];

			ret += bit.query(oppPos);
			bit.update(oppPos, 1);
		}
		return ret;
	}

	static class BIT {
		public static int SIZE = 100000 + 1;
		public int[] mem = new int[SIZE];

		public void update(int n, int k) {
			for (int i = n + 1; i < mem.length; i += lsOne(i))
				mem[i] += k;
		}

		public int query(int n) {
			int ret = 0;
			for (int i = n + 1; i > 0; i -= lsOne(i))
				ret += mem[i];

			return ret;
		}

		public int query(int a, int b) {
			return query(b) - query(a - 1);
		}

		public int lsOne(int n) {
			return -n & n;
		}
	}

}
