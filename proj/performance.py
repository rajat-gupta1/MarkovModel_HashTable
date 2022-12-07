import sys
from markov import identify_speaker
import pathlib
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <max-k> <runs>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, max_k, runs = sys.argv[1:]
    max_k = int(max_k)
    runs = int(runs)

    # TODO: add code here to open files & read text

    fileA = pathlib.Path(__file__).parent / filenameA
    fileB = pathlib.Path(__file__).parent/ filenameB
    fileC = pathlib.Path(__file__).parent / filenameC
    readA = fileA.read_text()
    readB = fileB.read_text()
    readC = fileC.read_text()

    # TODO: run performance tests as outlined in README.md

    df = pd.DataFrame(columns = ['Implementation', 'K', 'Time'])

    use_hashtable = True
    for k in range(2):
        if k == 1:
            use_hashtable = False
        for i in range(max_k):
            total_time = 0
            for j in range(runs):
                start = time.perf_counter()
                tup = identify_speaker(readA, readB, readC, i + 1, use_hashtable)
                elapsed = time.perf_counter() - start
                total_time += elapsed
            total_time /= (runs)
            if k == 0:
                df.loc[len(df.index)] = ['hashtable', i + 1, total_time]
            else:
                df.loc[len(df.index)] = ['dict', i + 1, total_time]

    # TODO: write execution_graph.png

    sns.pointplot(x = df['K'], y = df['Time'], hue= df['Implementation'], linestyle='-', marker='o')
    plt.ylabel(f"Average Time (Runs={runs})")
    plt.title("HashTable vs Python dict")
    plt.savefig('execution_graph.png')