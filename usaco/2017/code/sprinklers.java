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
import java.util.Scanner;

public class sprinklers {
	static int MOD = (int) 1e9 + 7;

	public static void main(String args[]) throws Exception {
		boolean testing = new File("sprinklers.in").exists();
		Scanner in = new Scanner(testing ? new BufferedInputStream(new FileInputStream("sprinklers.in")) : System.in);
		PrintStream out = new PrintStream(
				testing ? new BufferedOutputStream(new FileOutputStream("sprinklers.out")) : System.out);

		int N = in.nextInt();

		ArrayList<Point> points = new ArrayList<>();
		for (int i = 0; i < N; i++)
			points.add(new Point(in.nextInt(), in.nextInt()));
		points.sort((a, b) -> a.x - b.x);

		ArrayList<Point> lower = new ArrayList<>();
		for (int i = 0, min = Integer.MAX_VALUE; i < points.size(); i++) {
			Point curr = points.get(i);
			if (curr.y < min) {
				min = curr.y;
				lower.add(curr);
			}
		}

		ArrayList<Point> upper = new ArrayList<>();
		for (int i = points.size() - 1, max = Integer.MIN_VALUE; i >= 0; i--) {
			Point curr = points.get(i);
			if (curr.y > max) {
				max = curr.y;
				upper.add(curr);
			}
		}

		Collections.sort(lower, (a, b) -> a.x - b.x);
		Collections.sort(upper, (a, b) -> a.x - b.x);

		upper.add(new Point(Integer.MAX_VALUE, Integer.MIN_VALUE));
		lower.add(new Point(Integer.MAX_VALUE, Integer.MAX_VALUE));

		int[] left = new int[N];
		Arrays.fill(left, -1);

		long ret = 0;
		int l = -1, u = 0;
		long cached = -1;
		for (int i = 0; i < N; i++) {
			if (i >= lower.get(l + 1).x) {
				l++;
				cached = -1;
			}
			if (i > upper.get(u).x) {
				u++;
				cached = -1;
			}

			if (l == -1) continue;

			if (cached == -1) {
				cached = 0;

				for (int j = lower.get(l).y; j < upper.get(u).y; j++) {
					if (left[j] == -1) {
						left[j] = lower.get(l).x;
					}
					cached += 1L * (i - left[j]) * (upper.get(u).y - j);
					cached %= MOD;
				}
			} else {
				long len = upper.get(u).y - lower.get(l).y;
				len = Math.max(len, 0);

				cached += len * (len + 1) / 2;
				cached %= MOD;
			}
			ret += cached;
			ret %= MOD;
		}
		out.println(ret);

		in.close();
		out.close();
	}
}
