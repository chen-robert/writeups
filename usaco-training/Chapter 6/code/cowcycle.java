
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.Scanner;
import java.util.stream.Collectors;

/*
ID: robertc5
LANG: JAVA
TASK: cowcycle
*/
public class cowcycle {
	static int rearLow;
	static int rearUp;

	static int[] front;
	static int[] rear;

	static double best = Double.MAX_VALUE;
	static int[] bestF;
	static int[] bestR;

	static int NUM = 50007;
	static boolean[] hashArr = new boolean[NUM];

	public static void main(String args[]) throws Exception {
		boolean testing = new File("cowcycle.in").exists();
		Scanner in = new Scanner(testing ? new FileInputStream("cowcycle.in") : System.in);
		PrintStream out = new PrintStream(testing ? new FileOutputStream("cowcycle.out") : System.out);

		int F = in.nextInt(), R = in.nextInt();

		rear = new int[R];

		int frontLow = in.nextInt();
		int frontHigh = in.nextInt();
		rearLow = in.nextInt();
		rearUp = in.nextInt();

		for (int i = frontLow; i <= Math.min(frontHigh, frontLow + 1); i++) {
			front = new int[F];
			front[0] = i;
			bash(1, i + 1, frontHigh);
		}

		Arrays.sort(bestF);
		Arrays.sort(bestR);
		out.println(Arrays.stream(bestF).mapToObj(String::valueOf).collect(Collectors.joining(" ")));
		out.println(Arrays.stream(bestR).mapToObj(String::valueOf).collect(Collectors.joining(" ")));

		in.close();
		out.flush();
		out.close();
	}

	public static int hash(int[] arr) {
		int gcd = 1;
		int max = Arrays.stream(arr).max().orElse(-1);
		for (int i = 1; i <= max; i++) {
			int tmp = i;
			if (Arrays.stream(arr).allMatch(n -> n % tmp == 0)) {
				gcd = i;
			}
		}

		int finGcd = gcd;
		return ((Arrays.hashCode(Arrays.stream(arr).map(i -> i / finGcd).toArray()) % NUM) + NUM) % NUM;
	}

	public static void bash(int size, int lower, int upper) {
		if (size < front.length) {
			for (int i = lower; i <= upper; i++) {
				front[size] = i;
				bash(size + 1, i + 1, upper);
			}
		} else {
			int hash = hash(front);
			if (!hashArr[hash]) {
				hashArr[hash] = true;
				update(front);
			}
		}
	}

	public static void update(int[] front) {
		for (int i = rearLow; i < rearUp; i++) {
			update(i);
		}
	}

	public static void update(int rearLow) {
		int wantUp = upperBound(rearLow, front);
		if (wantUp > rearUp) return;

		rear[0] = rearLow;
		rear[rear.length - 1] = wantUp;
		bashRear(front, rear, 1, rearLow, wantUp);
	}

	public static void bashRear(int[] front, int[] rear, int size, int lower, int upper) {
		if (size < rear.length - 1) {
			for (int i = lower; i <= upper; i++) {
				rear[size] = i;
				bashRear(front, rear, size + 1, i + 1, upper);
			}
		} else {
			double curr = variance(front, rear);
			if (curr < best) {
				bestF = front.clone();
				bestR = rear.clone();

				best = curr;
			}
		}
	}

	// Assumes front and rear are sorted
	public static boolean isValid(int[] front, int[] rear) {
		return 1.0 * front[front.length - 1] / rear[0] >= 3.0 * front[0] / rear[rear.length - 1];
	}

	public static int upperBound(int lower, int[] front) {
		int ret = lower + 1;
		while (!isValid(front, new int[] { lower, ret })) {
			ret++;
		}
		return ret;
	}

	public static double variance(int[] front, int[] rear) {
		double[] ratios = new double[front.length * rear.length];

		int i = 0;
		for (int a : front) {
			for (int b : rear) {
				ratios[i++] = 1.0 * a / b;
			}
		}

		Arrays.sort(ratios);

		double[] diffs = new double[ratios.length - 1];
		for (i = 0; i < diffs.length; i++) {
			diffs[i] = ratios[i + 1] - ratios[i];
		}

		double mean = Arrays.stream(diffs).sum() / diffs.length;

		return Arrays.stream(diffs).map(d -> (d - mean) * (d - mean)).sum();
	}
}
