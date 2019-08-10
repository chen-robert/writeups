import java.util.Arrays;
import java.util.Random;

public class ArrayUtils {
  static Random rand = new Random(System.nanoTime());

  static void shuffle(int[] a) {
    for (int i = 0; i < a.length; i++) {
      int j = rand.nextInt(i + 1);

      int t = a[i];
      a[i] = a[j];
      a[j] = t;
    }
  }
}