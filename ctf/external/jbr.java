import java.io.InputStream;
import java.io.PrintStream;
import java.net.Socket;
import java.util.Scanner;

public class jbr {
	static volatile boolean done = false;

	public static void main(String args[]) throws Exception {
		// For every offset
		for (int offset = 0; offset < 32; offset++) {
			// Multi-threaded approach to speed up computation
			Thread[] threads = new Thread[1000];
			done = false;
			for (int i = 0; i < threads.length; i++) {
				if (done) break;
				// Make temporary variable to store offset.
				final int tmp = offset;
				threads[i] = new Thread(() -> {
					int c;
					try {
						c = tryFlip(tmp);
						if (c != -1) {
							System.out.print(c + " ");
							System.out.print((char) c + " ");
							done = true;
						} else {
						}
					} catch (Exception e) {
						e.printStackTrace();
					}
				});
				threads[i].start();
				Thread.sleep(50);
			}
			// Wait until all threads have finished executing
			for (int i = 0; i < threads.length; i++) {
				if (threads[i] != null) {
					threads[i].join();
				}
			}
			System.out.println();
		}
	}

	public static int tryFlip(int offset) throws Exception {
		Socket s = new Socket("2018shell1.picoctf.com", 22666);
		InputStream sin = s.getInputStream();
		PrintStream out = new PrintStream(s.getOutputStream());
		Scanner in = new Scanner(sin);

		// Manually remove the fluff text
		in.nextLine();
		in.nextLine();
		in.nextLine();
		in.nextLine();
		out.println("E");

		// Prefix padding. Aligned with lots of guess and check.
		String prefix = "";
		for (int i = 0; i < (11 + 32) - offset; i++) {
			prefix += "A";
		}
		out.println(prefix);

		// Suffix padding
		String suffix = "";
		int currLen = -offset - 1;
		while (currLen % 16 != 0) {
			suffix += "B";
			currLen++;
		}
		out.println(suffix);
		while (!in.next().equals("encrypted:")) {
		}
		String hexStr = in.next();

		// Remove padding
		hexStr = hexStr.substring(0, hexStr.length() - 32);

		// Get the respective blocks
		String hashBlock = hexStr.substring(hexStr.length() - 32);
		String currBlock = hexStr.substring(256, 288);
		String prevBlock = hexStr.substring(224, 256);

		// Construct a payload with the ciphertext minus padding and a
		// ciphertext
		// block
		String payload = hexStr + currBlock;

		out.println("S");
		out.print(payload + "\n");

		// Equivalent to python recieve until
		while (!in.next().equals("message:")) {
		}

		if (in.next().equals("Ooops!")) {
			s.close();
			return -1;
		}
		s.close();

		// We use 16 here because only when the block padding is 16 will the
		// entire padding block be removed
		return 16 ^ lsb(prevBlock) ^ lsb(hashBlock);
	}

	public static int lsb(String s) {
		return Integer.parseInt(s.substring(s.length() - 2), 16);
	}
}