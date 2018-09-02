import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Scanner;

public class _262144 {
	static ArrayList<Integer> arr;

	public static void main(String args[]) throws Exception {
		boolean testing = !new File("262144.in").exists();
		Scanner in = new Scanner(testing ? System.in : new FileInputStream("262144.in"));
		PrintStream out = new PrintStream(testing ? System.out : new FileOutputStream("262144.out"));

		int N = in.nextInt();
		arr = new ArrayList<>();
		for (int i = 0; i < N; i++) {
			arr.add(in.nextInt());
		}

		solve(arr, 1);
		out.println(max);

		in.close();
		out.close();
	}

	static int max = -1;

	static void solve(ArrayList<Integer> arr, int curr) {
		max = Math.max(max, curr);

		ArrayList<Integer> blockCounts = new ArrayList<>();
		blockCounts.add(0);
		boolean inCurr = true;
		ArrayList<ArrayList<Integer>> blocks = new ArrayList<>();
		for (int i = 0; i < arr.size(); i++) {
			if (arr.get(i) == curr) {
				if (!inCurr) {
					blockCounts.add(0);
				}
				inCurr = true;
				blockCounts.set(blockCounts.size() - 1, blockCounts.get(blockCounts.size() - 1) + 1);
			} else {
				if (inCurr) {
					blocks.add(new ArrayList<>());
				}
				blocks.get(blocks.size() - 1).add(arr.get(i));
				inCurr = false;
			}
		}

		if (arr.get(arr.size() - 1) != curr) {
			blockCounts.add(0);
		}

		for (int i = 0; i < blocks.size(); i++) {
			ArrayList<Integer> ret = new ArrayList<>();
			addCount(ret, blockCounts.get(i), curr + 1);

			ret.addAll(blocks.get(i));
			while (i < blocks.size() - 1 && blockCounts.get(i + 1) % 2 == 0) {
				i++;
				addCount(ret, blockCounts.get(i), curr + 1);
				ret.addAll(blocks.get(i));
			}

			addCount(ret, blockCounts.get(i + 1), curr + 1);

			solve(ret, curr + 1);
		}

		int maxBlockSize = blockCounts.stream().mapToInt(i -> i).max().getAsInt();
		max = Math.max(max, curr + (int) (Math.log(maxBlockSize) / Math.log(2)));
	}

	static void addCount(ArrayList<Integer> ret, int times, int num) {
		for (int j = 0; j < times; j += 2)
			ret.add(num);

	}
}
