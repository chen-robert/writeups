import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.Scanner;

/*
ID: robertc5
LANG: JAVA
TASK: fence8
*/
public class fence8 {
	public static void main(String args[]) throws Exception {
		boolean testing = new File("fence8.in").exists();
		Scanner in = new Scanner(testing ? new FileInputStream("fence8.in") : System.in);
		PrintStream out = new PrintStream(testing ? new FileOutputStream("fence8.out") : System.out);

		int N = in.nextInt();
		int[] boards = new int[N];
		for (int i = 0; i < N; i++) {
			boards[i] = in.nextInt();
		}

		int R = in.nextInt();
		int[] rails = new int[R];
		for (int i = 0; i < R; i++) {
			rails[i] = in.nextInt();
		}

		Arrays.sort(boards);
		Arrays.sort(rails);

		int tot = Arrays.stream(boards).sum();
		int i = 0;
		while (i < rails.length && tot >= rails[i]) {
			tot -= rails[i];
			i++;
		}
		int[] relevantRails = new int[i];
		System.arraycopy(rails, 0, relevantRails, 0, i);
		rails = relevantRails;

		int l = 0, r = i;
		while (l < r) {
			int mid = (l + r) / 2;
			if (isPossib(boards, rails, mid)) {
				l = mid + 1;
			} else {
				r = mid;
			}
		}

		if (!isPossib(boards, rails, l)) {
			l--;
		}

		out.println(l);

		in.close();
		out.close();
	}

	public static boolean isPossib(int[] boards, int[] rails, int guess) {
		// We need to copy the array because it gets modified
		return isPossib(Arrays.copyOf(boards, boards.length), genRailsLp(rails, guess), 0, -1,
				genLeftover(boards, rails, guess));
	}

	public static int[] genRailsLp(int[] rails, int size) {
		int[] railsLp = new int[129];
		Arrays.stream(rails).limit(size).forEach(i -> railsLp[i]++);
		return railsLp;
	}

	public static int genLeftover(int[] boards, int[] rails, int size) {
		return Arrays.stream(boards).sum() - Arrays.stream(rails).limit(size).sum();
	}

	public static boolean isPossib(int[] state, int[] railsLp, int size, int continueIndex, int leftover) {
		if (Arrays.stream(railsLp).allMatch(i -> i == 0)) return true;
		if (size > state.length - 1) return false;

		for (int i = continueIndex == -1 ? railsLp.length - 1 : continueIndex; i > 0; i--) {
			if (railsLp[i] > 0) {
				if (state[size] >= i) {
					state[size] -= i;
					railsLp[i]--;

					if (isPossib(state, railsLp, size, i, leftover)) return true;

					railsLp[i]++;
					state[size] += i;
				}
			}
		}
		if (leftover >= state[size]) {
			if (isPossib(state, railsLp, size + 1, -1, leftover - state[size])) return true;
		}

		return false;
	}
}