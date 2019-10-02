import java.awt.Point;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.Scanner;

public class balancing {
	public static void main(String args[]) throws Exception {
		boolean testing = !new File("balancing.in").exists();
		Scanner in = new Scanner(testing ? System.in : new FileInputStream("balancing.in"));
		PrintStream out = new PrintStream(testing ? System.out : new FileOutputStream("balancing.out"));

		int N = in.nextInt();

		ArrayList<Integer> ys = new ArrayList<>();
		ArrayList<Point> points = new ArrayList<>();
		for (int i = 0; i < N; i++) {
			points.add(new Point(in.nextInt(), in.nextInt()));

			ys.add(points.get(points.size() - 1).y);
		}

		Collections.sort(ys);

		int curr = 1;
		HashMap<Integer, Integer> yLp = new HashMap<>();
		for (int i = 0; i < ys.size(); i++, curr++) {
			yLp.put(ys.get(i), curr);
			while (i < ys.size() - 1 && ys.get(i) == ys.get(i + 1)) {
				i++;
			}
		}

		for (Point p : points) {
			p.y = yLp.get(p.y);
		}

		Collections.sort(points, (a, b) -> a.x - b.x);

		BIT left = new BIT();
		BIT right = new BIT();
		for (Point p : points) {
			right.update(p.y, 1);
		}

		int ret = Integer.MAX_VALUE;
		ret = Math.min(ret, bestSplit(left, right, curr));
		for (Point p : points) {
			right.update(p.y, -1);
			left.update(p.y, 1);

			ret = Math.min(ret, bestSplit(left, right, curr));
		}
		out.println(ret);

		in.close();
		out.close();
	}

	public static int bestSplit(BIT left, BIT right, int size) {
		int totLeft = left.sumTo(BIT.size - 1);
		int totRight = right.sumTo(BIT.size - 1);

		int l = 0;
		int r = size;

		while (r - l > 4) {
			int mid = (l + r) / 2;

			int lb = left.sumTo(mid);
			int lt = totLeft - lb;

			int rb = right.sumTo(mid);
			int rt = totRight - rb;

			boolean moveDown;
			if (Math.max(rb, rt) > Math.max(lb, lt)) {
				moveDown = rb > rt;
			} else {
				moveDown = lb > lt;
			}
			if (moveDown) {
				r = mid + 1;
			} else {
				l = mid - 1;
			}
		}

		int ret = Integer.MAX_VALUE;
		for (int i = l; i <= r; i++) {

			int lb = left.sumTo(i);
			int lt = totLeft - lb;

			int rb = right.sumTo(i);
			int rt = totRight - rb;
			ret = Math.min(ret, Math.max(Math.max(lb, lt), Math.max(rb, rt)));
		}
		return ret;
	}
}

class BIT {
	public static int size = 110011;
	public int[] mem = new int[size];

	// Change key n by k
	public void update(int n, int k) {
		for (int i = n; i < mem.length; i += lsOne(i)) {
			mem[i] += k;
		}
	}

	void update(int l, int r, int k) {
		update(l, k);
		update(r + 1, -k);
	}

	// Sum from 0 - n inclusive
	public int sumTo(int n) {
		int ret = 0;
		for (int i = n; i > 0; i -= lsOne(i)) {
			ret += mem[i];
		}

		return ret;
	}

	private int lsOne(int n) {
		return -n & n;
	}
}