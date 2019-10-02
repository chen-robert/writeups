/*
Standard binary indexed tree
*/

class BinaryIndexedTree {
  static class BIT {
    int[] mem;

    BIT(int n) {
      mem = new int[n + 1];
    }

    public void update(int n, int k) {
      for (int i = n + 1; i < mem.length; i += -i & i) {
        mem[i] += k;
      }
    }

    int query(int a, int b) {
      return query(b) - query(a - 1);
    }

    int query(int n) {
      int ret = 0;
      for (int i = n + 1; i > 0; i -= -i & i) {
        ret += mem[i];
      }

      return ret;
    }
  }
}