/*
Order static tree. 

Supports O(lg N):
- Insert
- Delete
- Index of element

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

    int query(int k) {
      int ret = 0;
      int curr = 0;

      for (int i = 20; i >= 0; i--) {
        if (ret + (1 << i) < arr.length && curr + arr[ret + (1 << i)] <= k) {
          ret += 1 << i;
          curr += arr[ret];
        }
      }

      return ret;
    }
  }
}