import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Scanner;

public class art {
	static class A {
		int d = Integer.MIN_VALUE;
		int l = Integer.MAX_VALUE;
		int r = Integer.MIN_VALUE;
		int u = Integer.MAX_VALUE;
	}

	public static void main(String args[]) throws Exception {
		boolean testing = new File("art.in").exists();
		Scanner in = new Scanner(testing ? new FileInputStream("art.in") : System.in);
		PrintStream out = new PrintStream(testing ? new FileOutputStream("art.out") : System.out);

		int N = in.nextInt();
		int[][] map = new int[N][N];
		HashSet<Integer> colors = new HashSet<>();
		ArrayList<A> items = new ArrayList<>();
		for (int i = 0; i < N * N; i++) {
			items.add(new A());
		}
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				int c = in.nextInt();
				if (c != 0) {
					colors.add(c);
					A curr = items.get(c - 1);

					curr.u = Math.min(curr.u, i);
					curr.d = Math.max(curr.d, i);
					curr.l = Math.min(curr.l, j);
					curr.r = Math.max(curr.r, j);
				}
				map[i][j] = c;
			}
		}

		int[][] lp = new int[N + 1][N + 1];
		for (A curr : items) {
			if (curr.u == Integer.MAX_VALUE) continue;

			lp[curr.d + 1][curr.r + 1]++;
			lp[curr.u][curr.r + 1]--;
			lp[curr.d + 1][curr.l]--;
			lp[curr.u][curr.l]++;
		}

		int[][] ps = new int[N + 1][N + 1];
		for (int i = 0; i < N + 1; i++) {
			for (int j = 0; j < N + 1; j++) {
				ps[i][j] = lp[i][j];
				if (i > 0) {
					ps[i][j] += ps[i - 1][j];
				}

				if (j > 0) {
					ps[i][j] += ps[i][j - 1];
				}
				if (i > 0 && j > 0) {
					ps[i][j] -= ps[i - 1][j - 1];
				}
			}
		}

		HashSet<Integer> all = new HashSet<>();
		for (int i = 0; i < N; i++) {
			for (int j = 0; j < N; j++) {
				if (ps[i][j] > 1) {
					all.add(map[i][j]);
				}
			}
		}

		// If one color, can't be painted first
		if (colors.size() == 1) {
			out.println(N * N - 1);
		} else {
			out.println(N * N - all.size());
		}
		in.close();
		out.close();
	}
}
