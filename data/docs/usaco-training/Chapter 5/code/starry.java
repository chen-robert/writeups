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
TASK: starry
*/
public class starry{
	static{
		rename();
	}
    public static final String problem = "starry";
    public static final boolean testing = !new File(problem + ".in").exists();
	public static void main(String args[]) throws Exception{
		BufferedWriter out = new BufferedWriter(new PrintWriter(testing ?
                new OutputStreamWriter(System.out) : new FileWriter(problem + ".out")));
        BufferedScanner in = new BufferedScanner();
        
        int h = in.nextInt();
        int w = in.nextInt();
        
        boolean[][] map = new boolean[w][h];
        boolean[][] copy = new boolean[w][h];
        char[][] ret = new char[w][h];
        for(int i = 0; i < w; i++){
        	for(int z = 0; z < h; z++)ret[i][z] = '0';
        }
        for(int i = 0; i < w; i++){
        	String s = in.next();
        	if(s.length() != h)throw new IllegalArgumentException();
        	
        	for(int z = 0; z < h; z++){
        		map[i][z] = s.charAt(z) == '1';
        		copy[i][z] = map[i][z];
        	}
        }
        HashMap<Long, Character> lp = new HashMap<>(); 
        char curr = 'a';
        for(int i = 0; i < w; i++){
        	for(int z = 0; z < h; z++){
        		if(map[i][z]){
        			State s = new State(i, z, copy);
        			explore(i, z, s, map);
        			long[] hashes = s.hash();
        			if(!lp.containsKey(hashes[0])){
        				char newChar = curr++;
        				for(Long l: hashes){
        					lp.put(l, newChar);
        				}
        			}
        			
        			char fill = lp.get(hashes[0]);
        			s.fill(ret, fill);
        		}
        	}
        }
        
        for(char[] ch: ret){
        	for(char c: ch)out.write(c);
        	out.write('\n');
        }
        
        in.close();
        out.flush();
        out.close();
	}
	
	public static void explore(int x, int y, State s, boolean[][] grid){
		if(x < 0 || x >= grid.length)return;
		if(y < 0 || y >= grid[0].length)return;
		if(!grid[x][y])return;
		grid[x][y] = false;
		
		s.relax(x, y);
		
		for(int i = -1; i <= 1; i++){
			for(int z = -1; z <= 1; z++){
				explore(x + i, y + z, s, grid);
			}
		}
	}
	static class State{
		public long A = 1376223234457L;

		int u;
		int d;
		int l;
		int r;
		
		boolean[][] ori;
		public State(int x, int y, boolean[][] map){
			l = x;
			r = x;
			u = y;
			d = y;
			
			ori = new boolean[map.length][map[0].length];
		}
		public void relax(int x, int y){
			if(l > x)l = x;
			if(r < x)r = x;
			if(d > y)d = y;
			if(u < y)u = y;
			
			ori[x][y] = true;
		}
		static long sketch;
		public long[] hash(){
			sketch = (r - l + 107) * (u - d + 107);
			long[] a = hash(l, r, d, u);
			long[] b = hash(l, r, u, d);
			long[] c = hash(r, l, d, u);
			long[] d = hash(r, l, u, this.d);
			
			return new long[]{a[0], a[1], b[0], b[1], c[0], c[1], d[0], d[1]};			
		}
		private long[] hash(int sX, int eX, int sY, int eY){
			int incX = sX < eX? 1: -1;
			int incY = sY < eY? 1: -1;
			
			long[] ret = new long[2];
			ret[0] = sketch;
			ret[1] = sketch;
			for(int i = sX; i != eX + incX; i+= incX){
				for(int z = sY; z != eY + incY; z+= incY){
					ret[0] *= A;
					ret[0] += ori[i][z]? 13: 3;
				}
			}
			for(int z = sY; z != eY + incY; z+= incY){
				for(int i = sX; i != eX + incX; i+= incX){
					ret[1] *= A;
					ret[1] += ori[i][z]? 13: 3;
				}
			}
			return ret;
		}
		public void fill(char[][] ret, char fill){
			for(int i = l; i <= r; i++){
				for(int z = d; z <= u; z++){
					if(ret[i][z] != '0')continue;
					ret[i][z] = ori[i][z]? fill: '0';
				}
			}
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
