/*
Order static tree. 

Supports O(lg N):
- Insert
- Delete

Supports O(lg^2 N):
- Kth largest number
*/

class OrderStatisticTree {
  static class OSTree {
    int[] arr;
    int n;

    OSTree(int n) {
      arr = new int[n + 1];
      this.n = n;
    }

    void add(int n) {
      for (int i = n + 1; i < arr.length; i += -i & i) {
        arr[i]++;
      }
    }

    void remove(int n) {
      for (int i = n + 1; i < arr.length; i += -i & i) {
        arr[i]--;
      }
    }

    int sum(int n) {
      int ret = 0;
      for (int i = n + 1; i > 0; i -= -i & i) {
        ret += arr[i];
      }

      return ret;
    }

    int query(int k) {
      int l = 0;
      int r = n;
      while (l < r) {
        int mid = (l + r) / 2;

        if (k < sum(mid))
          r = mid;
        else
          l = mid + 1;
      }

      return l;
    }
  }
}