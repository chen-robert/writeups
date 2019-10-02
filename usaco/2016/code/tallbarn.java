import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.PriorityQueue;
import java.util.Scanner;

public class tallbarn {
	static int N;
	static long K;
	static long[] costs;
	static long[] vals;

	public static void main(String args[]) throws Exception {
		boolean testing = new File("tallbarn.in").exists();
		Scanner in = new Scanner(testing ? new FileInputStream("tallbarn.in") : System.in);
		PrintStream out = new PrintStream(testing ? new FileOutputStream("tallbarn.out") : System.out);

		N = in.nextInt();
		K = in.nextLong();
		costs = new long[N];
		vals = new long[N];
		Arrays.fill(vals, 1);
		for (int i = 0; i < N; i++)
			costs[i] = in.nextLong();

		double l = 0, r = K * (K + 1);
		while (l < r - 0.001) {
			double mid = (l + r) / 2;
			if (cost(mid) > K) r = mid;
			else l = mid;
		}

		cost(l);

		PriorityQueue<Integer> leftovers = new PriorityQueue<Integer>((a, b) -> better(a, b) ? -1 : 1);
		for (int i = 0; i < N; i++)
			leftovers.add(i);

		long size = K - Arrays.stream(vals).sum();
		for (int i = 0; i < size; i++) {
			int curr = leftovers.poll();
			vals[curr]++;
			leftovers.add(curr);
		}

		double ans = 0;
		for (int i = 0; i < N; i++) {
			ans += 1.0 * costs[i] / vals[i];
		}
		out.println(Math.round(ans));

		in.close();
		out.close();
	}

	static boolean better(int a, int b) {
		return costs[a] / vals[a] * (vals[a] + 1) > costs[b] / vals[b] * (vals[b] + 1);
	}

	static long cost(double lim) {
		long ret = 0;
		for (int i = 0; i < N; i++) {
			long curr = (long) ((-1 + Math.sqrt(1 + 4 * costs[i] * lim)) / 2 + 1);
			ret += curr;
			vals[i] = curr;
		}
		return ret;
	}

}
