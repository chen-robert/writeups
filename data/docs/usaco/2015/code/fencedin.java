import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.Scanner;

public class fencedin {

	public static void main(String args[]) throws Exception {
		boolean testing = !new File("fencedin.in").exists();
		Scanner in = new Scanner(testing ? System.in : new FileInputStream("fencedin.in"));
		PrintStream out = new PrintStream(testing ? System.out : new FileOutputStream("fencedin.out"));

		int A = in.nextInt(), B = in.nextInt();
		long n = in.nextInt(), m = in.nextInt();

		ArrayList<Integer> horizVals = new ArrayList<Integer>();
		for (int i = 0; i < n; i++)
			horizVals.add(in.nextInt());

		ArrayList<Integer> vertVals = new ArrayList<Integer>();
		for (int i = 0; i < m; i++)
			vertVals.add(in.nextInt());

		Collections.sort(horizVals);
		Collections.sort(vertVals);

		ArrayList<Integer> horiz = new ArrayList<Integer>();
		ArrayList<Integer> vert = new ArrayList<Integer>();
		int prev = 0;
		for (int next : horizVals) {
			horiz.add(next - prev);
			prev = next;
		}
		horiz.add(A - prev);

		prev = 0;
		for (int next : vertVals) {
			vert.add(next - prev);
			prev = next;
		}
		vert.add(B - prev);

		long ret = 0;
		Collections.sort(horiz);
		Collections.sort(vert);

		System.out.println(horiz);
		System.out.println(vert);

		ret += horiz.remove(0) * m;
		ret += vert.remove(0) * n;

		PriorityQueue<Thing> all = new PriorityQueue<>((a, b) -> a.length - b.length);
		horiz.forEach((i) -> all.add(new Thing(i, true)));
		vert.forEach((i) -> all.add(new Thing(i, false)));

		int horizLines = 0;
		int vertLines = 0;
		long finished = n + m;
		while (finished < (n + 1) * (m + 1) - 1) {
			Thing curr = all.poll();

			long cuts = (curr.horiz ? (m - vertLines) : (n - horizLines));
			finished += cuts;

			ret += cuts * curr.length;

			if (curr.horiz) {
				horizLines++;
			} else {
				vertLines++;
			}
		}
		out.println(ret);
	}

	static class Thing {
		int length;
		boolean horiz;

		Thing(int n, boolean h) {
			length = n;
			horiz = h;
		}
	}
}
