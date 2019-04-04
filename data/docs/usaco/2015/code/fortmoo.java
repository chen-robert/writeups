import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Scanner;

public class fortmoo {
	static int id = 13;

	public static void main(String args[]) throws Exception {
		boolean testing = !new File("fortmoo.in").exists();
		Scanner in = new Scanner(testing ? System.in : new FileInputStream("fortmoo.in"));
		PrintStream out = new PrintStream(testing ? System.out : new FileOutputStream("fortmoo.out"));

		int N = in.nextInt(), M = in.nextInt();
		boolean[][] map = new boolean[N][M];
		for (int i = 0; i < N; i++) {
			String s = in.next();
			for (int z = 0; z < M; z++) {
				map[i][z] = s.charAt(z) == 'X';
			}
		}

		int[][] lp = new int[N + 1][M];
		for (int i = 0; i < N; i++) {
			for (int z = 0; z < M; z++) {
				lp[i + 1][z] = (map[i][z] ? 1 : 0) + lp[i][z];
			}
		}

		int ret = 0;
		for (int i = 0; i < N; i++) {
			for (int z = i + 1; z < N; z++) {
				int l = 0;
				int r = 1;

				while (r < M) {
					if (lp[i][l] != lp[z + 1][l]) {
						l++;
						r = Math.max(r, l + 1);
					} else if (lp[i][r] != lp[z + 1][r]) {
						if (map[i][r] || map[z][r]) {
							l = r + 1;
							r = l + 1;
						} else {
							r++;
						}
					} else {
						ret = Math.max(ret, (z - i + 1) * (r - l + 1));
						r++;
					}
				}
			}
		}

		out.println(ret);

		in.close();
		out.close();
	}
}
