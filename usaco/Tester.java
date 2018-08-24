import java.io.BufferedInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Enumeration;
import java.util.List;
import java.util.Scanner;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;

/**
 * Created by Robert on 8/5/2018.
 */
public class Tester {
	public static final String PROBLEM = "cardgame";

	public static final String TEMPLATE = "import java.io.File;\r\nimport java.io.FileInputStream;\r\nimport java.io.FileOutputStream;\r\nimport java.io.PrintStream;\r\nimport java.util.Scanner;\r\n\r\npublic class %1$s {\r\n\r\n\tpublic static void main(String args[]) throws Exception {\r\n\t\tboolean testing = new File(\"%1$s.in\").exists();\r\n\t\tScanner in = new Scanner(testing ? new FileInputStream(\"%1$s.in\") : System.in);\r\n\t\tPrintStream out = new PrintStream(testing ? new FileOutputStream(\"%1$s.out\") : System.out);\r\n\r\n\t\tin.close();\r\n\t\tout.close();\r\n\t}\r\n}\r\n";
	public static final String CURRENT_TEMPLATE = String.format(TEMPLATE, PROBLEM);
	public static final String DATA_PATH = "./data";
	public static final File DATA_DIR = new File(DATA_PATH);
	public static final File UNZIP_DIR = new File(DATA_PATH + "/tmp");
	public static final int MAX_RUNTIME = 3 * 1000;

	static final File INPUT_FILE = new File(PROBLEM + ".in");
	static final File OUTPUT_FILE = new File(PROBLEM + ".out");

	public static final Logger logger = Logger.getGlobal();

	public static void main(String[] args) {
		logger.setLevel(Level.INFO);

		if (generateProblemFile()) {
			extractFiles(UNZIP_DIR);

			TestResult[] results = runTests(UNZIP_DIR);
			printResults(results);

			cleanup(DATA_DIR);
		} else {
			logger.info(String.format("Generated problem file in src/%s.java", PROBLEM));
		}

	}

	public static boolean generateProblemFile() {
		File problemFile = new File(String.format("src/%s.java", PROBLEM));
		if (problemFile.exists()) {
			return true;
		}
		try {
			problemFile.createNewFile();

			try {
				PrintStream out = new PrintStream(problemFile);
				out.println(CURRENT_TEMPLATE);
				out.close();
			} catch (IOException e) {
				logger.severe("Failed to write template to file.");
				logger.severe(e.getMessage());
			}
		} catch (IOException e) {
			logger.severe("Failed to create new problem file.");
			logger.severe(e.getMessage());
		}
		return false;
	}

	public static void extractFiles(File unzipDir) {
		try {
			extractFilesHelper(unzipDir);
		} catch (IOException ie) {
			logger.severe("Failed to extract files");
			logger.severe(ie.getMessage());
		}
	}

	public static TestResult[] runTests(File unzipDir) {
		try {
			return runTestsHelper(unzipDir);
		} catch (IOException | ReflectiveOperationException e) {
			logger.severe("Failed to run tests");
			logger.severe(e.getMessage());
		}
		return null;
	}

	public static void printResults(TestResult[] results) {
		if (results == null) return;

		StringBuilder sb = new StringBuilder();
		sb.append("\n");
		for (TestResult result : results) {
			sb.append(result + "\n");
		}

		logger.info(sb.toString());
	}

	static class TestResult {
		boolean success;

		boolean match;
		boolean error;
		double runTime;

		int testCase;

		TestResult(int testCase, boolean match, boolean error, double runTime) {
			this.testCase = testCase;
			this.match = match;
			this.error = error;
			this.runTime = runTime / 1000;

			success = (match && !error && runTime < MAX_RUNTIME);
		}

		@Override
		public String toString() {
			StringBuilder sb = new StringBuilder();
			sb.append(String.format("#%2d | ", testCase));
			if (success) {
				sb.append(String.format("* %.2f", runTime));
			} else if (error) {
				sb.append("!");
			} else if (!match) {
				sb.append("WA");
			} else {
				sb.append(String.format("TLE %.2f", runTime));
			}
			return sb.toString();
		}
	}

	public static TestResult[] runTestsHelper(File unzipDir) throws IOException, ReflectiveOperationException {
		List<TestResult> results = new ArrayList<>();

		int fileCount = unzipDir.listFiles().length;
		String unzipPath = unzipDir.getCanonicalPath();

		logger.finer("Running tests...");
		for (int testCase = 1; testCase <= fileCount / 2; testCase++) {
			try {
				setupTestData(testCase, unzipPath);
			} catch (IllegalArgumentException iae) {
				logger.severe(iae.getMessage());
				continue;
			}

			logger.info(String.format("Running test case %d.", testCase));
			File output = new File(String.format("%s/%d.out", unzipPath, testCase));
			TestResult result = runTest(testCase, output);
			results.add(result);

			System.gc();

			logger.info(result.toString());

			if (testCase == 1 && !result.success) {
				break;
			}
		}

		INPUT_FILE.delete();
		OUTPUT_FILE.delete();

		Collections.sort(results, (a, b) -> a.testCase - b.testCase);
		return results.toArray(new TestResult[results.size()]);
	}

	public static void setupTestData(int testCase, String unzipPath) throws IOException {
		File input = new File(String.format("%s/%d.in", unzipPath, testCase));
		File output = new File(String.format("%s/%d.out", unzipPath, testCase));

		if (!input.exists() || !output.exists()) {
			throw new IllegalArgumentException(String.format("Invalid test data for #%d", testCase));
		}

		INPUT_FILE.delete();
		Files.copy(input.toPath(), INPUT_FILE.toPath());
		OUTPUT_FILE.delete();
		OUTPUT_FILE.createNewFile();
	}

	public static TestResult runTest(int testCase, File output) throws ReflectiveOperationException, IOException {
		Class solution = Class.forName(PROBLEM);
		Method solutionMain = solution.getMethod("main", String[].class);

		boolean error = false, match = false;
		String[] args = new String[1];

		long startTime = System.currentTimeMillis(), runTime = MAX_RUNTIME;

		// If not the first test, silence stdout.
		if (testCase != 1) {
			System.setOut(new PrintStream(new ByteArrayOutputStream()));
		}
		try {
			solutionMain.invoke(null, args);

		} catch (InvocationTargetException ite) {
			if (testCase == 1) {
				ite.getCause().printStackTrace();
			}
			error = true;
		}
		if (!error) {
			runTime = System.currentTimeMillis() - startTime;

			match = filesEqual(OUTPUT_FILE, output);
		}
		return new TestResult(testCase, match, error, runTime);
	}

	public static boolean filesEqual(File solutionOutputFile, File testOutputFile) throws IOException {
		try (Scanner solutionOutput = new Scanner(new BufferedInputStream(new FileInputStream(solutionOutputFile)));
				Scanner testOutput = new Scanner(new BufferedInputStream(new FileInputStream(testOutputFile)));) {
			while (solutionOutput.hasNextLine() && testOutput.hasNextLine()) {
				if (!solutionOutput.nextLine().equals(testOutput.nextLine())) {
					return false;
				}
			}
			return solutionOutput.hasNextLine() == testOutput.hasNextLine();
		}
	}

	public static void extractFilesHelper(File unzipDir) throws IOException {
		// If the directory already existed, we may have to clean up old files
		if (!unzipDir.mkdir()) {
			cleanup(unzipDir);
		}

		logger.log(Level.FINER, "Extracting files...");

		ZipFile zip = new ZipFile(getZipFile());
		Enumeration<? extends ZipEntry> zEntries = zip.entries();

		while (zEntries.hasMoreElements()) {
			ZipEntry curr = zEntries.nextElement();
			Files.copy(zip.getInputStream(curr), new File(unzipDir.getCanonicalPath() + "/" + curr.getName()).toPath());
		}
		logger.log(Level.FINEST, String.format("Finished extracting %d files", unzipDir.listFiles().length));
	}

	public static void cleanup(File dir) {
		Arrays.stream(dir.listFiles()).filter(f -> !f.getName().endsWith(".zip")).forEach(f -> {
			if (f.isDirectory()) cleanup(f);
			f.delete();
		});
	}

	public static File getZipFile() {
		return Arrays.stream(DATA_DIR.listFiles()).filter(f -> f.getName().endsWith(".zip"))
				.filter(f -> f.getName().contains(PROBLEM)).findAny()
				.orElseThrow(() -> new IllegalArgumentException(String.format("Missing data for %s.", PROBLEM)));
	}
}
