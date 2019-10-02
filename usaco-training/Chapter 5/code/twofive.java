
/*
TASK: twofive
LANG: JAVA
ID: robertc5
 */

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.HashMap;
import java.util.Scanner;

public class twofive {
	static int SIZE = 5;

	public static void main(String args[]) throws Exception {
		boolean testing = !new File("twofive.in").exists();
		Scanner in = new Scanner(testing ? System.in : new BufferedInputStream(new FileInputStream("twofive.in")));
		PrintStream out = new PrintStream(
				testing ? System.out : new BufferedOutputStream(new FileOutputStream("twofive.out")));

		String type = in.next();

		HashMap<Integer, Integer> dp = new HashMap<>();
		int max = memo(dp) + 1;

		if (type.equals("N")) {

			int left = in.nextInt();

			out.println(solve(left, dp));
		} else {
			String word = in.next();

			int l = 0;
			int r = max;
			while (r - l > 4) {
				int mid = (l + r) / 2;
				if (solve(mid, dp).compareTo(word) < 0) {
					l = mid - 1;
				} else {
					r = mid + 1;
				}
			}
			int ret = -1;
			for (int i = l; i <= r; i++) {
				if (solve(i, dp).equals(word)) {
					ret = i;
				}
			}
			out.println(ret);
		}

		in.close();
		out.close();
	}

	public static String solve(int left, HashMap<Integer, Integer> dp) {
		int[][] board = new int[5][5];

		for (int i = 0; i < 5; i++) {
			for (int z = 0; z < 5; z++) {
				board[i][z] = -1;
			}
		}

		int currState = 0;

		boolean[] v = new boolean[25];
		for (int i = 0; i < SIZE; i++) {
			for (int z = 0; z < SIZE; z++) {
				currState |= (1 << t(i, z));
				for (int currLetter = 0; currLetter < 25; currLetter++) {
					boolean valid = !v[currLetter];
					if (i != 0 && currLetter < board[i - 1][z]) {
						valid = false;
					}

					if (z != 0 && currLetter < board[i][z - 1]) {
						valid = false;
					}
					if (valid) {
						board[i][z] = currLetter;
						v[currLetter] = true;

						int currCount = tot(board, v, currState, dp);
						if (left > currCount) {
							left -= currCount;
							v[currLetter] = false;
							board[i][z] = -1;
						} else {
							break;
						}

					}
				}
			}
		}
		String ret = "";
		for (int[] a : board) {
			for (int b : a)
				ret += (char) ('A' + b);
		}
		return ret;
	}

	static int tot(int[][] state, boolean[] v, int bitmask, HashMap<Integer, Integer> dp) {
		int currLetter = 100;
		int lim = -1;
		for (int i = v.length - 1; i >= 0; i--) {
			if (!v[i]) {
				currLetter = i;
			}
		}
		for (int i = 0; i < v.length; i++) {
			if (v[i]) {
				lim = i;
			}
		}
		if (currLetter >= lim) {
			return dp.get(bitmask);
		}
		int ret = 0;
		for (int i = 0; i < SIZE; i++) {
			for (int z = 0; z < SIZE; z++) {
				if (state[i][z] == -1) {
					boolean valid = true;
					if (i != 0 && (state[i - 1][z] == -1 || currLetter < state[i - 1][z])) {
						valid = false;
					}
					if (z != 0 && (state[i][z - 1] == -1 || currLetter < state[i][z - 1])) {
						valid = false;
					}
					if (valid) {
						int next = bitmask | (1 << t(i, z));
						state[i][z] = currLetter;
						v[currLetter] = true;
						ret += tot(state, v, next, dp);
						state[i][z] = -1;
						v[currLetter] = false;
					}
				}
			}
		}
		return ret;
	}

	static int memo(HashMap<Integer, Integer> memo) {

		int k = 0;
		for (int i = 0; i < SIZE * SIZE; i++) {
			k |= 1 << i;
		}
		memo.put(k, 1);

		return memo(0, -1, memo);
	}

	public static int memo(int currState, int currLen, HashMap<Integer, Integer> memo) {
		if (memo.containsKey(currState)) return memo.get(currState);

		int ret = 0;
		for (int i = 0; i < SIZE; i++) {
			for (int z = 0; z < SIZE; z++) {
				if (miss(currState, t(i, z))) {
					boolean valid = true;
					if (i != 0 && miss(currState, t(i - 1, z))) {
						valid = false;
					}
					if (z != 0 && miss(currState, t(i, z - 1))) {
						valid = false;
					}
					if (valid) {
						int next = currState | (1 << t(i, z));
						ret += memo(next, currLen + 1, memo);
					}
				}
			}
		}

		memo.put(currState, ret);
		return ret;
	}

	static int t(int a, int b) {
		return 5 * a + b;
	}

	static boolean miss(int a, int b) {
		return (a & (1 << b)) == 0;
	}
}
