import java.io.*;
import java.nio.Buffer;
import java.util.*;
import java.awt.Point;

public class ${NAME} {
    static final String name = "${NAME}";
    static final boolean test = new File(name + ".in").exists();


    static void solve(BufferedScanner in, BufferedPrinter out) throws Exception {



    }


    /**
     * My template below. FastIO and utility functions.
     * Minimized with https://codebeautify.org/javaviewer.
     */

    // @formatter:off
    public static void main(String args[])throws Exception{BufferedScanner in=new BufferedScanner(test?new FileInputStream(name+".in"):System.in);BufferedPrinter out=new BufferedPrinter(test?new FileOutputStream(name+".out"):System.out);solve(in,out);out.close();in.close();}
    static void readGraph(BufferedScanner in,ArrayList<ArrayList<Integer>>adj,int n){for(int i=0;i<n;i++){int u=in.nextInt()-1,v=in.nextInt()-1;adj.get(u).add(v);adj.get(v).add(u);}}
    static<T>ArrayList<ArrayList<T>>get2D(int n){ArrayList<ArrayList<T>>ret=new ArrayList<>();for(int i=0;i<n;i++)ret.add(new ArrayList<>());return ret;}
    static void force(boolean condition){if(!condition)throw new IllegalStateException();}
    static void debug(Object obj){if(obj instanceof long[][]){for(long[]a:(long[][])obj)System.out.println(Arrays.toString(a));}
    else if(obj instanceof int[][]){for(int[]a:(int[][])obj)System.out.println(Arrays.toString(a));}
    else if(obj instanceof char[][]){for(char[]a:(char[][])obj)System.out.println(Arrays.toString(a));}
    else if(obj instanceof boolean[][]){for(boolean[]a:(boolean[][])obj)System.out.println(Arrays.toString(a));}
    else if(obj instanceof long[]){System.out.println(Arrays.toString((long[])obj));}
    else if(obj instanceof int[]){System.out.println(Arrays.toString((int[])obj));}
    else if(obj instanceof char[]){System.out.println(Arrays.toString((char[])obj));}
    else if(obj instanceof boolean[]){System.out.println(Arrays.toString((boolean[])obj));}
    else{System.out.println(obj);}}
    static class BufferedPrinter{PrintWriter out;BufferedPrinter(OutputStream out){this(new OutputStreamWriter(out));}
    BufferedPrinter(Writer out){this.out=new PrintWriter(new BufferedWriter(out));}
    void print(Object...os){for(int i=0;i<os.length;i++){if(i!=0)out.print(' ');out.print(os[i]);}}
    void println(Object...os){print(os);out.println();}
    void close(){out.close();}
    void flush(){out.flush();}}
    static class BufferedScanner{private final InputStream in;private final byte[]buf=new byte[1<<13];int pos,count;BufferedScanner(InputStream in)throws IOException{this.in=in;}
    long nextLong()throws IOException{return Long.parseLong(next());}
    int[]nextN(int n)throws IOException{int[]ret=new int[n];for(int i=0;i<n;i++)ret[i]=this.nextInt();return ret;}
    long[]nextNL(int n)throws IOException{long[]ret=new long[n];for(int i=0;i<n;i++)ret[i]=this.nextLong();return ret;}
    private int read(){if(count==-1)err();try{if(pos>=count){pos=0;count=in.read(buf);if(count<=0)return-1;}}catch(IOException e){err();}
    return buf[pos++];}
    private static boolean isSpace(int c){return c==' '||c=='\n'||c=='\r'||c=='\t'||c==-1;}
    private int readSkipSpace(){int ret;do{ret=read();}while(isSpace(ret));return ret;}
    int nextInt(){int sign=1;int c=readSkipSpace();if(c=='-'){sign=-1;c=read();}
    int ret=0;do{if(c<'0'||c>'9')err();ret=ret*10+c-'0';c=read();}while(!isSpace(c));return sign*ret;}
    String next(){StringBuilder sb=new StringBuilder();int c=readSkipSpace();do{sb.append((char)c);c=read();}while(!isSpace(c));return sb.toString();}
    private void err(){throw new InputMismatchException();}
    void close()throws IOException{in.close();}}
    // @formatter:on
}
