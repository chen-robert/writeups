import java.awt.geom.Point2D;
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
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Scanner;
import java.util.StringTokenizer;


/*
ID: robertc5
LANG: JAVA
TASK: fc
*/
public class fc{
	static{
		rename();
	}
    public static final String problem = "fc";
    public static final boolean testing = !new File(problem + ".in").exists();
	public static void main(String args[]) throws Exception{
		BufferedWriter out = new BufferedWriter(new PrintWriter(testing ?
                new OutputStreamWriter(System.out) : new FileWriter(problem + ".out")));
        BufferedScanner in = new BufferedScanner();

        int n = in.nextInt();
        ArrayList<Point2D.Double> points = new ArrayList<>();
        for(int i = 0; i < n; i++)points.add(new Point2D.Double(Double.parseDouble(in.next()),
        		Double.parseDouble(in.next())));
        
        ArrayList<Point2D.Double> ret = ConvexHull(points);
        double fin = 0;
        for(int i = 0; i < ret.size() - 1; i++){
        	double vx = ret.get(i+1).x - ret.get(i).x;
        	double vy = ret.get(i+1).y - ret.get(i).y;
        	
        	fin += Math.sqrt(vx * vx + vy * vy);
        	System.out.println(ret.get(i));
        }
        System.out.println(ret.get(ret.size() - 1));
        double vx = ret.get(ret.size() - 1).x - ret.get(0).x;
        double vy = ret.get(ret.size() - 1).y - ret.get(0).y;
        fin += Math.sqrt(vx * vx + vy * vy);
        
        out.write(String.format("%.2f", fin) + "\n");
        
        in.close();
        out.flush();
        out.close();
	
	}
	public static ArrayList<Point2D.Double> ConvexHull(ArrayList<Point2D.Double> p){
		Point2D.Double base = p.remove(p.size() - 1);
		Collections.sort(p, new Comparator<Point2D.Double>() {
			@Override
			public int compare(Point2D.Double a, Point2D.Double b) {
				double val1 = Math.atan2(a.y - base.y, a.x - base.x);
				double val2 = Math.atan2(b.y - base.y, b.x - base.x);
				
				double val = val1 - val2;
				if(val < 0)return -1;
				else if(val > 0)return 1;
				return 0;
			}
		});
		p.add(base);
		for(Point2D n: p)System.out.println(n);
		System.out.println("___");
		ArrayList<Point2D.Double> ret = new ArrayList<>();
		ret.add(p.get(0));
		ret.add(p.get(1));
		
		for(int i = 2; i < p.size(); i++){
			ret.add(p.get(i));
			while(ret.size() > 2 && 
					angle(ret.get(ret.size()-3), ret.get(ret.size()-2), ret.get(ret.size()-1)) < 0){
				ret.remove(ret.size() - 2);
			}
		}
		
		boolean done = false;
		while(!done){
			done = true;
			for(int i = 0; i < ret.size(); i++){
				if(angle(ret.get((i)%ret.size()), ret.get((i+1)%ret.size()), ret.get((i+2)%ret.size()))<0){
					System.out.println(ret.get(i %ret.size()) + " " + ret.get((i+1)%ret.size()) 
					+ " " + ret.get((i+2) % ret.size()));
					ret.remove((i+1) % ret.size());
					i--;
					done = false;
				}
			}
		}
		return ret;
	}
	//Negative means bad
	public static double angle(Point2D.Double a, Point2D.Double b, Point2D.Double c){
		Point2D.Double v1 = new Point2D.Double(b.x - a.x, b.y - a.y);
		Point2D.Double v2 = new Point2D.Double(c.x - a.x, c.y - a.y);
		
		double val = v1.x * v2.y - v1.y * v2.x;
		return val;
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
