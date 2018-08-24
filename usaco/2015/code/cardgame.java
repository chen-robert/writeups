import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.PrintStream;
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;
import java.util.TreeSet;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class cardgame {

	public static void main(String args[]) throws Exception {
		boolean testing = new File("cardgame.in").exists();
		Scanner in = new Scanner(testing ? new FileInputStream("cardgame.in") : System.in);
		PrintStream out = new PrintStream(testing ? new FileOutputStream("cardgame.out") : System.out);

		int N = in.nextInt();
		HashSet<Integer> all = new HashSet<>();
		all.addAll(IntStream.range(0, 2 * N).boxed().collect(Collectors.toSet()));

		int[] farmers = new int[N];
		for (int i = 0; i < N; i++) {
			farmers[i] = in.nextInt() - 1;
			all.remove(farmers[i]);
		}

		Set<Integer> cows = all;

		int[] pre = new int[N + 1];
		TreeSet<Integer> pq = new TreeSet<>();
		pq.addAll(cows);

		for (int j = 1; j <= N; j++) {
			Integer curr = pq.higher(farmers[j - 1]);

			pre[j] = pre[j - 1];
			if (curr != null) {
				pq.remove(curr);
				pre[j]++;
			}
		}
		int[] suf = new int[N + 1];
		pq = new TreeSet<>();
		pq.addAll(cows);

		for (int j = N - 1; j >= 0; j--) {
			Integer curr = pq.lower(farmers[j]);
			suf[j] = suf[j + 1];
			if (curr != null) {
				pq.remove(curr);
				suf[j]++;
			}
		}

		int ret = 0;
		for (int i = 0; i <= N; i++) {
			ret = Math.max(ret, pre[i] + suf[i]);
		}
		out.println(ret);

		in.close();
		out.close();
	}
}
