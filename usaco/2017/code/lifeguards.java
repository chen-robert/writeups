import java.awt.Point;
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
import java.util.stream.Collectors;

public class lifeguards {
	public static void main(String args[]) throws Exception {
		boolean testing = new File("lifeguards.in").exists();
		Scanner in = new Scanner(testing ? new BufferedInputStream(new FileInputStream("lifeguards.in")) : System.in);
		PrintStream out = new PrintStream(
				testing ? new BufferedOutputStream(new FileOutputStream("lifeguards.out")) : System.out);

		int N = in.nextInt(), K = in.nextInt();

		ArrayList<Point> intervals = new ArrayList<>();
		for (int i = 0; i < N; i++) {
			intervals.add(new Point(in.nextInt(), in.nextInt()));
		}
		Collections.sort(intervals, (a, b) -> a.x - b.x);
		HashSet<Point> filtered = new HashSet<>();
		for (int i = 0; i < N;) {
			int j = i + 1;
			while (j < N && intervals.get(j).y < intervals.get(i).y) {
				filtered.add(intervals.get(j));
				j++;
			}
			i = j;
		}

		intervals = new ArrayList<>(intervals.stream().filter(p -> !filtered.contains(p)).collect(Collectors.toSet()));
		Collections.sort(intervals, (a, b) -> a.x - b.x);

		K -= N - intervals.size();
		int[] sizes = new int[intervals.size()];
		for (int i = 0; i < sizes.length; i++)
			sizes[i] = intervals.get(i).y - intervals.get(i).x;

		int ans = 0;
		int[][] DP = new int[intervals.size()][K + 1];
		int[][] lp = new int[DP.length][DP[0].length];
		for (int i = 0; i < DP.length; i++) {
			Arrays.fill(DP[i], Integer.MIN_VALUE);
			for (int j = 0; j < K + 1; j++) {
				if (j <= i) {
					DP[i][j] = sizes[i];
				}
				int k = 1;
				while (i - k >= 0 && j - k + 1 >= 0) {
					int next = i - k;
					if (intervals.get(next).y > intervals.get(i).x) {
						DP[i][j] = Math.max(DP[i][j], DP[next][j - k + 1] + intervals.get(i).y - intervals.get(next).y);
					} else {
						DP[i][j] = Math.max(DP[i][j], lp[next][j - k + 1] + sizes[i]);
						break;
					}
					k++;
				}
				if (j + intervals.size() - 1 - i >= K) {
					ans = Math.max(ans, DP[i][j]);
				}
				lp[i][j] = DP[i][j];
				if (i != 0 && j != 0) {
					lp[i][j] = Math.max(lp[i][j], lp[i - 1][j - 1]);
				}
			}
		}

		out.println(ans);

		in.close();
		out.close();
	}
}
