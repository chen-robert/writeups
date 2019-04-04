import java.awt.Rectangle;
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
import java.util.Arrays;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;
import java.util.StringTokenizer;


/*
ID: robertc5
LANG: JAVA
TASK: tour
*/
public class tour{
	static{
		rename();
	}
    public static final String problem = "tour";
    public static final boolean testing = !new File(problem + ".in").exists();
	public static void main(String crap/*I'm only temporarily renaming this*/[]) throws Exception{
		BufferedWriter out = new BufferedWriter(new PrintWriter(testing ?
                new OutputStreamWriter(System.out) : new FileWriter(problem + ".out")));
        BufferedScanner in = new BufferedScanner();
        
        int n = in.nextInt();
        int v = in.nextInt();
        
        HashMap<String, Integer> lp = new HashMap<>();
        for(int i = 0; i < n; i++){
        	lp.put(in.next(), i);
        }

        ArrayList<ArrayList<Integer>> adj = new ArrayList<>();
        for(int i = 0; i < n; i++)adj.add(new ArrayList<>());
        
        for(int i = 0; i < v; i++){
        	int u = lp.get(in.next());
        	int t = lp.get(in.next());
        	
        	adj.get(u).add(t);
        	adj.get(t).add(u);
        }
        
        int[][] DP = new int[n][n];
        DP[0][0] = 1;
        
        for(int i = 0; i < n; i++){
        	for(int z = 0; z < n; z++){
        		if(DP[i][z] == 0)continue;
        		
        		for(Integer to: adj.get(i)){
        			if(to > z){
        				if(DP[i][z] + 1 > DP[to][z])DP[to][z] = DP[i][z] + 1;
        			}
        		}
				for(Integer to: adj.get(z)){
        			if(to > i){
        				if(DP[i][z] + 1 > DP[i][to])DP[i][to] = DP[i][z] + 1;
        			}
        		}
        	}
        }
        System.out.println(Arrays.deepToString(DP));
        int ans = 1;
        for(int i = 0; i < n; i++){
        	if(adj.get(i).contains(n-1)){
        		ans = Math.max(ans, DP[n-1][i]);
            	ans = Math.max(ans, DP[i][n-1]);
        	}
        }
        out.write(ans + "\n");
        
        in.close();
        out.flush();
        out.close();
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
