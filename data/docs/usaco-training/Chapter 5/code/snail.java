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
import java.util.HashMap;
import java.util.Scanner;
import java.util.StringTokenizer;


/*
ID: robertc5
LANG: JAVA
TASK: snail
*/
public class snail{
	static{
		rename();
	}
    public static final String problem = "snail";
    public static final boolean testing = !new File(problem + ".in").exists();
	public static void main(String args[]) throws Exception{
		BufferedWriter out = new BufferedWriter(new PrintWriter(testing ?
                new OutputStreamWriter(System.out) : new FileWriter(problem + ".out")));
        BufferedScanner in = new BufferedScanner();
        
        int n = in.nextInt();
        int b = in.nextInt();
        
        int[][] map =  new int[n+2][n+2];
        for(int i = 0; i < n+2; i++){
        	map[0][i] = 1;
        	map[n+1][i] = 1;
        	map[i][0] = 1;
        	map[i][n+1] = 1;
        }
        for(int i = 0; i < b; i++){
        	String s = in.next();
        	int x = s.charAt(0) - 'A' + 1;
        	int y = Integer.parseInt(s.substring(1));
        	
        	map[x][y] = 1;
        }
        for(int[] a: map){
        	System.out.println(Arrays.toString(a));
        }
        explore(1, 0, 1, 1, 1, map);
        explore(0, 1, 1, 1, 1, map);
        
        out.write(ans + "\n");
        
        in.close();
        out.flush();
        out.close();
	}
	static int ans = 0;
	public static void explore(int vx, int vy, int x, int y, int path, int[][] map){
		if(ans < path)ans = path;
		
		int next = map[x+vx][y+vy];
		map[x][y] = 2;
		if(next == 1){
			if(vx == 0){
				if(map[x-1][y] == 0)explore(-1, 0, x, y, path, map);
				if(map[x+1][y] == 0)explore(1, 0, x, y, path, map);
			}else{
				if(map[x][y-1] == 0)explore(0, -1, x, y, path, map);
				if(map[x][y+1] == 0)explore(0, 1, x, y, path, map);
			}
		}else if(next == 0){
			explore(vx, vy, x + vx, y + vy, path + 1, map);
		}
		map[x][y] = 0;
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
