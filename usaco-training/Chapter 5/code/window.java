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
TASK: window
*/
public class window{
	static{
		rename();
	}
    public static final String problem = "window";
    public static final boolean testing = !new File(problem + ".in").exists();
	public static void main(String crap/*I'm only temporarily renaming this*/[]) throws Exception{
		BufferedWriter out = new BufferedWriter(new PrintWriter(testing ?
                new OutputStreamWriter(System.out) : new FileWriter(problem + ".out")));
        BufferedScanner in = new BufferedScanner();
        
        HashMap<Integer, Rectangle> win = new HashMap<>();
        ArrayList<Rectangle> rects = new ArrayList<Rectangle>();
        try{
	        while(true){
	        	String s = in.next();
	        	char type = s.charAt(0);
	        	s = s.substring(2, s.length() - 1);
	        	
	        	String[] args = s.split(",");
	        	int id = args[0].charAt(0);
	        	
	        	Rectangle curr = null;
        		if(win.containsKey(id))curr = win.get(id);
	        	switch(type){
	        	case 'w':
	        		int[] vals = new int[4];
	        		for(int i = 1; i < 5; i++){
	        			vals[i-1] = Integer.parseInt(args[i]);
	        		}
	        		//Note the non-standard usage of java.awt.Rectangle's fields
	        		win.put(id, new Rectangle(Math.min(vals[0],  vals[2]), Math.min(vals[1],  vals[3]), 
	        				Math.max(vals[0],  vals[2]), Math.max(vals[1],  vals[3])));
	        		rects.add(win.get(id));
	        		break;
	        	case 't':
	        		rects.remove(curr);
	        		rects.add(curr);
	        		break;
	        	case 'b':
	        		rects.remove(curr);
	        		rects.add(0, curr);
	        		break;
	        	case 'd':
	        		rects.remove(curr);
	        		win.remove(id);	        		
	        		break;
	        	case 's':
	        		ArrayList<Data> arr = new ArrayList<>();
	        		for(int i = rects.indexOf(curr) + 1; i < rects.size(); i++){
	        			Rectangle rect = rects.get(i);
	        			
	        			Package pack = new Package(rect.y, rect.height);
	        			arr.add(new Data(pack, rect.x));
	        			arr.add(new Data(pack, rect.width));
	        		}
	        		arr.sort(new Comparator<Data>(){
	        			public int compare(Data a, Data b){
	        				return a.x - b.x;
	        			}
	        		});
	        		
	        		HashSet<Package> all = new HashSet<>();
	        		int size = curr.height - curr.y;
	        		int prevX = 0;
	        		int ret = 0;
	        		for(int i = 0; i < arr.size();){
	        			int currX = arr.get(i).x;
	        			if(currX > curr.width)break;
	        			prevX = Math.max(curr.x, prevX);
	        			ret += size * Math.max(0, currX - prevX);
	        			
	        			while(i < arr.size() && arr.get(i).x == currX){
		        			Package p = arr.get(i).p;
		        			if(all.contains(p)){
		        				all.remove(p);
		        			}else{
		        				all.add(p);
		        			}
		        			i++;
	        			}
	        			
	        			boolean[] bash = new boolean[curr.height - curr.y];
	        			
	        			for(Package p: all){
		        			Arrays.fill(bash, Math.max(0, Math.min(bash.length, p.s - curr.y)), 
		        					Math.max(0, Math.min(bash.length, p.e - curr.y)), true);
	        			}
	        			size = 0;
	        			for(int z = 0; z < bash.length; z++){
	        				if(!bash[z])size++;
	        			}
	        			prevX = currX;
	        		}
        			prevX = Math.max(curr.x, prevX);
        			
	        		ret += size * (curr.width - prevX);
	        		out.write(String.format("%.3f\n", 100.0 * ret / ((curr.width - curr.x) * (curr.height - curr.y))));
	        		break;
        		default:
        			System.err.println("Crap");
        			break;
	        	}
	        	
	        }
        }catch(Exception noMoreTokensHopefully){}
        
        in.close();
        out.flush();
        out.close();
	}
	static class Package{
		int s;
		int e;
		
		Package(int s, int e){
			this.s = s;
			this.e = e;
		}
	}
	static class Data{
		Package p;
		
		int x;
		Data(Package p, int x){
			this.p = p;
			this.x = x;
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
