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
import java.util.Scanner;
import java.util.StringTokenizer;


/*
ID: robertc5
LANG: JAVA
TASK: schlnet
*/
public class schlnet{
	static{
		rename();
	}
    public static final String problem = "schlnet";
    public static final boolean testing = !new File(problem + ".in").exists();
	public static void main(String args[]) throws Exception{
		BufferedWriter out = new BufferedWriter(new PrintWriter(testing ?
                new OutputStreamWriter(System.out) : new FileWriter(problem + ".out")));
        BufferedScanner in = new BufferedScanner();
        
        int n = in.nextInt();
        ArrayList<ArrayList<Integer>> adj = new ArrayList<>();
        ArrayList<ArrayList<Integer>> rev = new ArrayList<>();
        for(int i = 0; i < n; i++){
        	adj.add(new ArrayList<>());
        	rev.add(new ArrayList<>());
        }
        for(int i = 0; i < n; i++){
        	int curr;
        	while((curr = in.nextInt()) != 0){
        		adj.get(i).add(curr - 1);
        		rev.get(curr - 1).add(i);
        	}
        }
        
        ArrayList<Integer> list = new ArrayList<>();
        boolean[] v = new boolean[n];
        for(int i = 0; i < n; i++){
        	if(!v[i]){
        		v[i] = true;
        		topSort(list, rev, v, i);
        	}
        }
        
        int[] label = new int[n];
        Arrays.fill(label, -1);
        int count = 0;
        for(Integer curr: list){
        	if(label[curr] == -1)floodFill(label, adj, curr, count++);
        }
        
        ArrayList<ArrayList<Integer>> dag = new ArrayList<>();
        for(int i = 0; i < count; i++)dag.add(new ArrayList<>());

        int[] inCount = new int[count];
        int[] outCount = new int[count];
        
        for(int i = 0; i < adj.size(); i++){
        	for(Integer u: adj.get(i)){
        		if(label[i] == label[u])continue;
        		
        		if(!dag.get(label[i]).contains(label[u])){
        			dag.get(label[i]).add(label[u]);
        			inCount[label[u]]++;
        			outCount[label[i]]++;
        		}
        	}
        }
        
        
        int a = 0;
        int b = 0;
        for(int i = 0; i < count; i++){
        	if(inCount[i] == 0)a++;
        	if(outCount[i] == 0)b++;
        }
        
        //If only one vertex, we don't need to add any edges to make it strongly connected
        if(count == 1)
            out.write(a + "\n" + 0 + "\n");
        else
        	out.write(a + "\n" + Math.max(a, b) + "\n");
        	
        in.close();
        out.flush();
        out.close();
	}
	public static void floodFill(int[] label, ArrayList<ArrayList<Integer>> adj, int curr, int val){
		label[curr] = val;
		for(Integer n: adj.get(curr)){
			if(label[n] == -1){
				floodFill(label, adj, n, val);
			}
		}
	}
	public static void topSort(ArrayList<Integer> ret, ArrayList<ArrayList<Integer>> rev, boolean[] v, int curr){
		for(Integer n: rev.get(curr)){
			if(!v[n]){
				v[n] = true;
				topSort(ret, rev, v, n);
			}
		}
		ret.add(0, curr);
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
