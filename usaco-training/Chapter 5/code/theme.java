import java.awt.Point;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.Reader;
import java.util.HashMap;
import java.util.Scanner;
import java.util.StringTokenizer;


/*
ID: robertc5
LANG: JAVA
TASK: theme
*/
public class theme{
	static{
		rename();
	}
    public static final String problem = "theme";
    public static final boolean testing = !new File(problem + ".in").exists();
	public static void main(String args[]) throws Exception{
		BufferedWriter out = new BufferedWriter(new PrintWriter(testing ?
                new OutputStreamWriter(System.out) : new FileWriter(problem + ".out")));
        BufferedScanner in = new BufferedScanner();
        int n = in.nextInt();
        int[] change = new int[n-1];
        int curr = in.nextInt();
        for(int i = 0; i < n - 1; i++){
        	int tmp = in.nextInt();
        	change[i] = tmp - curr + 87;
        	curr = tmp;
        }
        
        RollingHash rh = new RollingHash(change);
        for(int a: change)System.out.println(a);
        int ans = 0;
        for(int i = 4; i < change.length; i++){
        	if(!isAns(i, rh)){
        		ans = i;
        		break;
        	}
        }
        if(ans == 4)ans = 0;
        out.write(ans + "\n");
        
        in.close();
        out.flush();
        out.close();
	
	}
	public static boolean isAns(int n, RollingHash rh){
        HashMap<Long, Integer> check = new HashMap<>();
        for(int i = 0; i < rh.p.length - n + 1; i++){
        	long l = rh.hashOf(i, i + n - 1);
        	if(!check.containsKey(l))check.put(l, i);
        	int k = check.get(l);
        	
        	if(i - k > n){
        		return true;
        	}
        }
        return false;
	}
	public static class RollingHash{
		public long[] p;
		public long[] h;
		
		public long A = 1376223234457L;
		public long B = 0;
		
		public RollingHash(int[] s){
			p = new long[s.length];
			h = new long[s.length];
			
			p[0] = s[0];
			for(int i = 1; i < p.length; i++)p[i] = mod(A * p[i-1] + s[i], B);
			
			h[0] = 1;
			for(int i = 1; i < h.length; i++)h[i] = mod(A * h[i-1], B);
		}
		public long hashOf(int start, int end){
			if(start == 0)return p[end];
			
			return mod(p[end] - p[start-1] * h[end-start+1], B);
		}
		public long hashOfAll(){
			return p[p.length - 1];
		}
		public long mod(long a, long b){
			return a;
		}
	}

	private static class BufferedScanner{
		private BufferedReader in;
		private StringTokenizer st;
		public BufferedScanner() throws IOException{
			this(testing ?
	                new InputStreamReader(System.in) : new FileReader(problem + ".in"));
		}
		public BufferedScanner(Reader r) throws IOException{
			in = new BufferedReader(r);
			st = new StringTokenizer(in.readLine());
		}
		public int nextInt() throws IOException{
			return Integer.parseInt(next());
		}
		public String nextLine() throws IOException{
			return in.readLine();
		}
		public String next() throws IOException{
			if(!st.hasMoreElements())st = new StringTokenizer(in.readLine());
			
			return st.nextToken();			
		}
		public void close() throws IOException{
			in.close();
		}
		
	}
	public static void rename(){
		try{
			if(!new File("src").exists())return;
			
			File f = new File("src/Generic.java");
			File dir = new File("src");
			for(File k: dir.listFiles()){
				if(!k.getName().equals("Generic.java") && !k.getName().equals("Util.java")){
					f = k;
				}
			}
			
			String name = f.getName();			
			name = name.substring(0,name.indexOf('.'));
			if(name.equals(problem))return;
			
			Scanner in = new Scanner(new FileInputStream(f));
			String s = "";
			String keyWord = "public static final String problem";
			String tmp;
			
			while(!(tmp = in.nextLine()).contains(keyWord))s += tmp + "\n";
			s += tmp + "\n";
			
			s = s.replace(name, problem);
			
			while(in.hasNextLine())s += in.nextLine() + "\n";
			

			FileOutputStream out = new FileOutputStream(f);
			out.write(s.getBytes());
			
			in.close();
			out.close();
			
			boolean success = f.renameTo(new File("src/" + problem + ".java"));
			System.out.println(success ? "Successful rename" : "Failed");
			System.out.println(s.getBytes().length + " bytes");
			System.exit(0);
		}catch(IOException e){
			e.printStackTrace();
		}
	}

}
