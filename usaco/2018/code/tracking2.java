import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Scanner;

public class tracking2 {
	static long MOD = (long) 1e9 + 7;

	public static void main(String args[]) throws Exception {
		boolean testing = new File("tracking2.in").exists();
		Scanner in = new Scanner(testing ? new FileInputStream("tracking2.in") : System.in);
		PrintStream out = new PrintStream(testing ? new FileOutputStream("tracking2.out") : System.out);

		int N = in.nextInt(), K = in.nextInt();

		int max = (int) 1e9;

		long ret = 1;

		if (K != 1) {
			int prev = in.nextInt();
			int prevIndex = -1;
			for (int i = 1; i < N - K + 1; i++) {
				int curr = in.nextInt();
				if (curr != prev) {
					int index;

					if (prev < curr) {
						index = i - 1;
					} else {
						index = i + K - 1;
					}

					ret *= ans(index - 1 - prevIndex, max - prev + 1, K);
					ret %= MOD;

					prevIndex = index;
					prev = curr;
				}
			}
			ret *= ans((N) - 1 - prevIndex, max - prev + 1, K);
		}
		ret %= MOD;

		out.println(ret);

		out.close();
		in.close();
	}

	public static long ans(int len, long choices, int K) {
		if (len == 0) return 1;

		long[] DP = new long[len + 2];
		DP[0] = DP[1] = 1;

		long[] modPow = new long[DP.length];
		modPow[0] = 1;
		for (int i = 1; i < modPow.length; i++) {
			modPow[i] = modPow[i - 1] * (choices - 1);
			modPow[i] %= MOD;
		}

		for (int i = 2; i < DP.length; i++) {
			DP[i] = DP[i - 1] * (choices - 1) + DP[i - 1];
			if (i > K) {
				DP[i] -= DP[i - K - 1] * modPow[K];
			}
			DP[i] = ((DP[i] % MOD) + MOD) % MOD;
		}

		return DP[len + 1];
	}

}
