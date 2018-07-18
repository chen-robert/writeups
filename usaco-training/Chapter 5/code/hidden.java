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
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.Scanner;
import java.util.StringTokenizer;


/*
ID: robertc5
LANG: JAVA
TASK: hidden
*/
public class hidden{
	static{
		rename();
	}
    public static final String problem = "hidden";
    public static final boolean testing = !new File(problem + ".in").exists();
	public static void main(String args[]) throws Exception{
		BufferedWriter out = new BufferedWriter(new PrintWriter(testing ?
                new OutputStreamWriter(System.out) : new FileWriter(problem + ".out")));
        BufferedScanner in = new BufferedScanner();
        
        int n = in.nextInt();
        StringBuilder sb = new StringBuilder();
        while(sb.length() != n){
        	sb.append(in.next());
        }
        
        sb.append(sb.toString());
        String fin = sb.toString();
        RollingHash lp = new RollingHash(fin);
        
        Comparator<Integer> comp =  new Comparator<Integer>(){
			@Override
			public int compare(Integer a, Integer b) {
				int l = 0;
				int r = n;
				while(r - l > 5){
					int mid = (l + r) / 2;
					if(lp.hashOf(a, a + mid) == lp.hashOf(b, b + mid)){
						l = mid - 1;
					}else{
						r = mid + 1;
					}
				}
				for(int i = l; i <= r; i++){
					if(fin.charAt(a + i) != fin.charAt(b + i)){
						return fin.charAt(a + i) - fin.charAt(b + i);
					}
				}
				return a - b;
			}
        	
        };
        int ret = 0;
        for(int i = 1; i < n; i++){
        	if(comp.compare(ret, i) > 0){
        		ret = i;
        	}
        }
        out.write(ret + "\n");
        
        in.close();
        out.flush();
        out.close();
	}
	public static int[][][] getLP(String[][] strs, String[] problem){
		int[][][] lp = new int[strs.length][strs[0].length][problem.length];
		
		for(int i = 0; i < strs.length; i++){
			for(int j = 0; j < strs[i].length; j++){
				for(int k = 0; k < problem.length; k++){
					int count = 0;
					for(int z = 0; z < 20; z++){
						if(strs[i][j].charAt(z) != problem[k].charAt(z))count++;
					}
					lp[i][j][k] = count;
				}
			}
		}
		
		return lp;
	}
	public static class RollingHash{
		public long[] p;
		public long[] h;
		
		public long A = 1500450271;
		public long B = 1000000007;
		
		public RollingHash(String s){
			p = new long[s.length()];
			h = new long[s.length()];
			
			p[0] = s.charAt(0);
			for(int i = 1; i < p.length; i++)p[i] = mod(A * p[i-1] + s.charAt(i), B);
			
			h[0] = 1;
			for(int i = 1; i < h.length; i++)h[i] = mod(A * h[i-1], B);
		}
		public long hashOf(int start, int end){
			if(start == 0)return p[end];
			
			return mod(p[end] - p[start-1] * h[end-start+1], B);
		}
		public long mod(long a, long b){
			return ((a % b) + b) % b;
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
