import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Scanner;

/*
ID: robertc5
LANG: JAVA
TASK: cryptcow
*/
public class cryptcow {
	static final String goal = "Begin the Escape execution at the Break of Dawn";
	static int cheeseNum = 50007;
	static boolean[] cheese = new boolean[cheeseNum];
	static HashSet<String> goalSubstrs = new HashSet<>();

	public static void main(String args[]) throws Exception {
		boolean testing = new File("cryptcow.in").exists();
		Scanner in = new Scanner(testing ? new FileInputStream("cryptcow.in") : System.in);
		PrintStream out = new PrintStream(testing ? new FileOutputStream("cryptcow.out") : System.out);

		for (int i = 0; i < goal.length(); i++) {
			for (int z = i + 1; z < goal.length(); z++) {
				goalSubstrs.add(goal.substring(i, z + 1));
			}
		}

		String cipher = in.nextLine();
		int[] counts = new int[128];
		cipher.chars().forEach(i -> counts[i]++);
		goal.chars().forEach(i -> counts[i]--);

		int[] COW = new int[3];
		COW[0] = counts['C'];
		COW[1] = counts['O'];
		COW[2] = counts['W'];

		int encryptRuns = COW[0];

		boolean valid = (Arrays.stream(counts).sum() == Arrays.stream(COW).sum())
				&& (COW[0] == COW[1] && COW[1] == COW[2]) && (decode(cipher, encryptRuns));

		if (valid) {
			out.printf("%d %d%n", 1, encryptRuns);
		} else {
			out.printf("0 0%n");
		}

		in.close();
		out.flush();
		out.close();
	}

	public static boolean decode(String cipher, int size) {
		if (size == 0) return true;

		int[][] positions = new int[3][size];
		int[] sizes = new int[3];

		for (int i = 0; i < cipher.length(); i++) {
			int index = "COW".indexOf(cipher.charAt(i));

			if (index != -1) {
				positions[index][sizes[index]] = i;
				sizes[index]++;
			}
		}

		if (positions[0][0] > positions[1][0] || positions[0][0] > positions[2][0]) return false;
		if (positions[2][size - 1] < positions[1][size - 1] || positions[2][size - 1] < positions[0][size - 1])
			return false;

		for (int i : positions[0]) {
			for (int j : positions[1]) {
				for (int k : positions[2]) {
					if (j < i || k < j) continue;

					StringBuilder next = new StringBuilder();
					next.append(cipher.substring(0, i));
					next.append(cipher.substring(j + 1, k));
					next.append(cipher.substring(i + 1, j));
					next.append(cipher.substring(k + 1));

					String nextStr = next.toString();
					int hash = ((nextStr.hashCode()) % cheeseNum + cheeseNum) % cheeseNum;
					if (checkParts(nextStr)) {
						if (!cheese[hash]) {
							cheese[hash] = true;
							if (decode(nextStr, size - 1)) return true;
						}
					}
				}
			}
		}
		return false;
	}

	public static boolean checkParts(String cipher) {
		for (int i = 0; i < cipher.length();) {
			int z = i;
			while (z < cipher.length() && "COW".indexOf(cipher.charAt(z)) == -1) {
				z++;
			}

			if (z - i > 1) {
				if (!goalSubstrs.contains(cipher.substring(i, z))) {
					return false;
				}
			}
			i = z + 1;
		}
		return true;
	}

}
