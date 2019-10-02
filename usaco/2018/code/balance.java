
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class balance {
	public static void main(String args[]) throws Exception {
		boolean testing = new File("balance.in").exists();
		Scanner in = new Scanner(testing ? new BufferedInputStream(new FileInputStream("balance.in")) : System.in);
		PrintStream out = new PrintStream(
				testing ? new BufferedOutputStream(new FileOutputStream("balance.out")) : System.out);

		int N = in.nextInt();

		ArrayList<Point> points = new ArrayList<>();
		points.add(new Point(-1, 0));
		points.add(new Point(N, 0));
		for (int i = 0; i < N; i++) {
			points.add(new Point(i, 1e5 * in.nextInt()));
		}

		ArrayList<Point> hull = new ArrayList<>(convexHull(points));
		Collections.sort(hull, (a, b) -> Double.compare(a.x, b.x));

		boolean first = true;
		for (int i = 0; i < hull.size() - 1; i++) {
			double diffX = hull.get(i + 1).x - hull.get(i).x;
			double diffY = hull.get(i + 1).y - hull.get(i).y;
			for (int j = 0; j < diffX; j++) {
				if (first) {
					first = false;
				} else {
					out.println((Math.round(hull.get(i).y * diffX) + j * Math.round(diffY)) / Math.round(diffX));
				}
			}
		}

		in.close();
		out.close();
	}

	public static ArrayList<Point> convexHull(ArrayList<Point> points) {
		if (points.size() < 2) points.clone();
		Collections.sort(points, (a, b) -> a.x == b.x ? Double.compare(a.x, b.x) : Double.compare(a.y, b.y));

		ArrayList<Point> lower = new ArrayList<>();
		for (Point p : points) {
			while (lower.size() >= 2 && cwturn(lower, p)) {
				lower.remove(lower.size() - 1);
			}
			lower.add(p);
		}
		lower.remove(lower.size() - 1);

		ArrayList<Point> upper = new ArrayList<>();
		for (int i = points.size() - 1; i >= 0; i--) {
			Point p = points.get(i);
			while (upper.size() >= 2 && cwturn(upper, p)) {
				upper.remove(upper.size() - 1);
			}
			upper.add(p);
		}
		upper.remove(upper.size() - 1);

		lower.addAll(upper);
		return lower;
	}

	static boolean cwturn(ArrayList<Point> arr, Point c) {
		Point a = arr.get(arr.size() - 1);
		Point b = arr.get(arr.size() - 2);
		return (a.x - b.x) * (c.y - b.y) >= (a.y - b.y) * (c.x - b.x);
	}

	static class Point {

		public final double x;
		public final double y;

		public Point(double x, double y) {
			this.x = x;
			this.y = y;
		}
	}

}
