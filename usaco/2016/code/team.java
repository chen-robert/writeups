import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.Scanner;

public class team {
	static final long MOD = 1000000009;

	public static void main(String args[]) throws Exception {
		boolean testing = !new File("team.in").exists();
		Scanner in = new Scanner(testing ? System.in : new FileInputStream("team.in"));
		PrintStream out = new PrintStream(testing ? System.out : new FileOutputStream("team.out"));

		int N = in.nextInt(), M = in.nextInt(), K = in.nextInt();
		int[] fj = new int[N];
		int[] fp = new int[M];

		for (int i = 0; i < N; i++) {
			fj[i] = in.nextInt();
		}
		for (int i = 0; i < M; i++) {
			fp[i] = in.nextInt();
		}
		Arrays.sort(fj);
		Arrays.sort(fp);

		long[][][] DP = new long[N + 1][M + 1][K + 1];
		long[][][] lp = new long[N + 1][M + 1][K + 1];

		for (int i = 0; i <= N; i++) {
			for (int z = 0; z <= M; z++) {
				lp[i][z][0] = 1;
			}
		}

		for (int i = 1; i <= N; i++) {
			for (int z = 1; z <= M; z++) {
				for (int k = 1; k <= K; k++) {

					if (fj[i - 1] > fp[z - 1]) {
						DP[i][z][k] = lp[i - 1][z - 1][k - 1];
					}
					lp[i][z][k] = lp[i - 1][z][k] + lp[i][z - 1][k] - lp[i - 1][z - 1][k] + DP[i][z][k];
					lp[i][z][k] %= MOD;
				}
			}
		}

		out.println((lp[N][M][K] + MOD) % MOD);

		in.close();
		out.close();
	}
}
