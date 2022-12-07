import sys
from markov import identify_speaker
import pathlib

if __name__ == "__main__":

    if len(sys.argv) != 6:
        print(
            f"Usage: python3 {sys.argv[0]} <filenameA> <filenameB> <filenameC> <k> <hashtable-or-dict>"
        )
        sys.exit(1)

    # extract parameters from command line & convert types
    filenameA, filenameB, filenameC, k, hashtable_or_dict = sys.argv[1:]
    k = int(k)
    if hashtable_or_dict not in ("hashtable", "dict"):
        print("Final parameter must either be 'hashtable' or 'dict'")
        sys.exit(1)
    elif hashtable_or_dict in ("hashtable"):
        hashtable_or_dict = True
    else:
        hashtable_or_dict = False

    # TODO: add code here to open files & read text
    fileA = pathlib.Path(__file__).parent / filenameA
    fileB = pathlib.Path(__file__).parent/ filenameB
    fileC = pathlib.Path(__file__).parent / filenameC
    readA = fileA.read_text()
    readB = fileB.read_text()
    readC = fileC.read_text()

    # TODO: add code to call identify_speaker & print results


    (speaker_a, speaker_b, most_likely) = identify_speaker(
        readA, readB, readC, k, hashtable_or_dict)

    # Output should resemble (values will differ based on inputs):

    # Speaker A: -2.1670591295191572
    # Speaker B: -2.2363636778055525

    print(f"Speaker A: {speaker_a}")
    print(f"Speaker B: {speaker_b}")

    # Conclusion: Speaker A is most likely

    print(f"Conclusion: Speaker {most_likely} is most likely")