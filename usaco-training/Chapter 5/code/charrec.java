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
import java.util.Arrays;
import java.util.Scanner;
import java.util.StringTokenizer;


/*
ID: robertc5
LANG: JAVA
TASK: charrec
*/
public class charrec{
	static String decode = " abcdefghijklmnopqrstuvwxyz";
	static{
		rename();
	}
    public static final String problem = "charrec";
    public static final boolean testing = !new File(problem + ".in").exists();
	public static void main(String args[]) throws Exception{
		BufferedWriter out = new BufferedWriter(new PrintWriter(testing ?
                new OutputStreamWriter(System.out) : new FileWriter(problem + ".out")));
        BufferedScanner in = new BufferedScanner();
        BufferedScanner font = new BufferedScanner(new FileReader("font.in"));
        
        if(font.nextInt() != 540)throw new AssertionError();
        String[][] strs = new String[decode.length()][20];
        
        for(int i = 0; i < strs.length; i++){
        	for(int z = 0; z < 20; z++)strs[i][z] = font.next();
        }
        
        int n = in.nextInt();
        String[] problem = new String[n];
        for(int i = 0; i < n; i++)problem[i] = in.next();
        
        int[] DP = new int[n + 1];
        int[] vals = new int[DP.length];
        int[] back = new int[DP.length];
        Arrays.fill(DP, 1 << 30);
        Arrays.fill(vals, -1);
        Arrays.fill(back, -1);
        DP[0] = 0;
        
        memo(n, DP, strs, getLP(strs, problem), vals, back);
        
        StringBuilder sb = new StringBuilder();
        int curr = n;
        while(curr != 0){
        	sb.append(decode.charAt(vals[curr]));
        	
        	curr = back[curr];
        }
        String ret = sb.toString();
        for(int i = ret.length() - 1; i >= 0; i--){
        	out.write(ret.charAt(i));
        }
        out.write("\n");
        
        font.close();
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
	public static int memo(int pos, int[] DP, String[][] strs, int[][][] lp, int[] DPVals, int[] DPBack){
		if(pos < 0)return 1 << 30;
		if(DP[pos] != 1 << 30)return DP[pos];
		DP[pos]++;
		
		//No line change
		if(pos > 19){
			int nextLp = pos - 20;
			int best = 1 << 30;
			int bestChar = -1;
			for(int j = 0; j < strs.length; j++){
				String[] curr = strs[j];
				
				int count = 0;
				for(int i = 0; i < curr.length; i++){
					count += lp[j][i][nextLp + i];
				}
				if(best > count){
					best = count;
					bestChar = j;
				}
			}
			int val = best + memo(nextLp, DP, strs, lp, DPVals, DPBack);
			if(DP[pos] > val){
				DP[pos] = val;
				DPBack[pos] = nextLp;
				DPVals[pos] = bestChar;
				
				if(best == 0){
					return DP[pos];
				}
			}
		}
		//Deleted a line
		if(pos > 18){
			int nextLp = pos - 19;
			for(int k = 0; k < 20; k++){
				int best = 1 << 30;
				int bestChar = -1;
				for(int j = 0; j < strs.length; j++){
					String[] curr = strs[j];
					
					int count = 0;
					for(int i = 0; i < curr.length - 1; i++){
						count += lp[j][i + (i >= k? 1: 0)][nextLp + i];
					}
					if(best > count){
						best = count;
						bestChar = j;
					}
				}
				int val = best + memo(nextLp, DP, strs, lp, DPVals, DPBack);
				if(DP[pos] > val){
					DP[pos] = val;
					DPBack[pos] = nextLp;
					DPVals[pos] = bestChar;
				}
			}
		}
		//Duped a line
		if(pos > 20){
			int nextLp = pos - 21;
			for(int k = 0; k < 20; k++){
				int best = 1 << 30;
				int bestChar = -1;
				for(int j = 0; j < strs.length; j++){
					String[] curr = strs[j];
					
					int count = 0;
					for(int i = 0; i < curr.length + 1; i++){
						if(i == k){
							int count1 = lp[j][i][nextLp + i];
							int count2 = lp[j][i][nextLp + i + 1];
							count += Math.min(count1, count2);
							i++;
						}else{
							count += lp[j][i + (i >= k? -1: 0)][nextLp + i];
						}
					}
					if(best > count){
						best = count;
						bestChar = j;
					}
				}
				int val = best + memo(nextLp, DP, strs, lp, DPVals, DPBack);
				if(DP[pos] > val){
					DP[pos] = val;
					DPBack[pos] = nextLp;
					DPVals[pos] = bestChar;
				}
			}
		}
		
		return DP[pos];
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
