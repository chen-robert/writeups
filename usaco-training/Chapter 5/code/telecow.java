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
import java.util.LinkedList;
import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Scanner;
import java.util.StringTokenizer;


/*
ID: robertc5
LANG: JAVA
TASK: telecow
*/
public class telecow{
	static{
		rename();
	}
    public static final String problem = "telecow";
    public static final boolean testing = !new File(problem + ".in").exists();
	public static void main(String args[]) throws Exception{
		BufferedWriter out = new BufferedWriter(new PrintWriter(testing ?
                new OutputStreamWriter(System.out) : new FileWriter(problem + ".out")));
        BufferedScanner in = new BufferedScanner();
        
        int n = in.nextInt();
        int m = in.nextInt();
        
        int s = in.nextInt() - 1 + n;
        int t = in.nextInt() - 1;
        
        ArrayList<ArrayList<Edge>> adj = new ArrayList<>();
        HashMap<Edge, Integer> lp = new HashMap<>();
        for(int i = 0; i < 2 * n; i++)adj.add(new ArrayList<>());
        for(int i = 0; i < n; i++){
        	Edge e = new Edge(i, i + n, 1);
        	adj.get(e.f).add(e);
        	adj.get(e.t).add(e);
        	
        	lp.put(e, i);
        }
        for(int i = 0; i < m; i++){
        	Edge e = new Edge(in.nextInt() - 1 + n, in.nextInt() - 1, 100);
        	adj.get(e.f).add(e);
        	adj.get(e.t).add(e);
        	
        	lp.put(e, 100000);

        	e = new Edge(e.t + n, e.f - n, 100);
        	adj.get(e.f).add(e);
        	adj.get(e.t).add(e);
        	
        	lp.put(e, 100000);
        	
        }
        ArrayList<Edge> ret = MinCut(adj, s, t, lp);
        out.write(ret.size() + "\n");
        for(int i = 0; i < ret.size(); i++){
        	out.write(lp.get(ret.get(i)) + 1 + (i == ret.size() - 1? "\n" : " "));
        }
        
        in.close();
        out.flush();
        out.close();
	}
	//I may have copied this from past problems...
	public static int NetworkFlow(ArrayList<ArrayList<Edge>> adj, int start, int end){
		Edge dummy = new Edge(0,0,0);
		while(true){
			Edge[] v = new Edge[adj.size()];
			for(int i = 0; i < v.length; i++)v[i] = null;
			
			Queue<Integer> q = new LinkedList<>();
			q.add(start);
			v[start] = dummy;
			while(!q.isEmpty()){
				int curr = q.poll();
				for(Edge e: adj.get(curr)){
					if(!e.active)continue;
					if(e.f == curr){
						if(v[e.t] != null)continue;
						if(e.w < e.max){
							v[e.t] = e;
							q.add(e.t);
						}
					}else{
						if(v[e.f] != null)continue;
						if(e.w > 0){
							v[e.f] = e;
							q.add(e.f);
						}
					}
				}
			}
			if(v[end] == null){
				int ret = 0;
				for(Edge e: adj.get(end)){
					if(!e.active)continue;
					
					if(e.t == end)ret += e.w;
				}
				return ret;
			}else{
				int curr = end;
				int maxPush = 1 << 30;
				while(curr != start){
					Edge e = v[curr];
					
					if(e.t == curr){
						maxPush = Math.min(e.max - e.w, maxPush);
						curr = e.f;
					}else if(e.f == curr){
						maxPush = Math.min(e.w, maxPush);
						curr = e.t;
					}
				}
				
				curr = end;
				while(curr != start){
					Edge e = v[curr];
					
					if(e.t == curr){
						e.w += maxPush;
						curr = e.f;
					}else if(e.f == curr){
						e.w -= maxPush;
						curr = e.t;
					}
				}
			}
			
		}
	}
	public static ArrayList<Edge> MinCut(ArrayList<ArrayList<Edge>> adj, int start, int end, 
			HashMap<Edge, Integer> lp){
		HashSet<Edge> set = new HashSet<>();
		for(ArrayList<Edge> n: adj){
			for(Edge k: n)set.add(k);
		}
		PriorityQueue<Edge> pq = new PriorityQueue<>(new Comparator<Edge>(){
			public int compare(Edge a, Edge b) {
				if(b.max != a.max)return b.max - a.max;
				return lp.get(a) - lp.get(b);
			}
		});
		pq.addAll(set);
		
		int currTot = NetworkFlow(adj, start, end);
		System.out.println("INIT: " + currTot);
		ArrayList<Edge> ret = new ArrayList<>();
		while(pq.size() > 0){
			ArrayList<ArrayList<Integer>> copy = new ArrayList<>();
			for(int i = 0; i < adj.size(); i++){
				copy.add(new ArrayList<>());
				for(Edge n: adj.get(i))copy.get(i).add(n.w);
			}
			Edge e = pq.poll();
			if(e.w != e.max)continue;
			
			int todo = e.w;
			//BFS to end
			while(todo > 0){
				Queue<Integer> reset = new LinkedList<>();
				Edge[] prev = new Edge[adj.size()];
				reset.add(e.t);
				while(!reset.isEmpty()){
					int curr = reset.poll();
					for(Edge n: adj.get(curr)){
						if(n.f == curr && n.w > 0){
							if(prev[n.t] == null){
								prev[n.t] = n;
								reset.add(n.t);
							}
						}
					}
				}
				int curr = end;
				int max = todo;
				while(curr != e.t){
					Edge tmp = prev[curr];
					if(tmp.w < max)max = tmp.w;
					curr = tmp.f;
				}
				curr = end;
				while(curr != e.t){
					Edge tmp = prev[curr];
					tmp.w-=max;
					if(tmp.t != curr)System.out.println("CRAP");
					
					curr = tmp.f;
				}
				todo-=max;
			}
			todo = e.w;
			//BFS to start
			while(todo > 0){
				Queue<Integer> reset = new LinkedList<>();
				Edge[] prev = new Edge[adj.size()];
				reset.add(e.f);
				while(!reset.isEmpty()){
					int curr = reset.poll();
					for(Edge n: adj.get(curr)){
						if(n.t == curr && n.w > 0){
							if(prev[n.f] == null){
								prev[n.f] = n;
								reset.add(n.f);
							}
						}
					}
				}
				int curr = start;
				int max = todo;
				while(curr != e.f){
					Edge tmp = prev[curr];
					if(tmp.w < max)max = tmp.w;
					curr = tmp.t;
				}
				curr = start;
				while(curr != e.f){
					Edge tmp = prev[curr];
					tmp.w-=max;
					if(tmp.f != curr)System.out.println("CRAP");
					
					curr = tmp.t;
				}
				todo-=max;
			}
			
			e.active = false;
			e.w = 0;
			int flow = NetworkFlow(adj, start, end);
			if(flow == currTot - e.max){
				ret.add(e);
				currTot = flow;
				System.out.println("NEW:" + currTot);
				
			}else{
				e.active = true;
				
				for(int i = 0; i < copy.size(); i++){
					for(int z = 0; z < copy.get(i).size(); z++){
						adj.get(i).get(z).w = copy.get(i).get(z);
					}
				}
				
				System.out.println(currTot + " " + flow + " " + e.max);
			}
		}
		return ret;
	}
	static class Edge{
		boolean active = true;
		int f;
		int t;
		int max;
		int w;
		Edge(int f, int t, int w){
			this.f = f;
			this.t = t;
			this.max = w;
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
