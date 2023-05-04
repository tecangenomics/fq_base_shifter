"""This code generates new fastq files

It allows user to move x bases from the 5' or 3' end of one fastq and
move it to another.

Limitations of code:
1. assumes that the data will be paired end
2. assumes that R1 and R2 files have the same number of entries and order
2. only moves bases, doesn't make a copy, so length_read_1 + length_read_2 always stays the same
3. only does operations on the ends of reads, not on the middle of reads

"""

import argparse


def get_arguments():
    """
    parses arguments from command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i1', '--fq1_in', help='the input R1 fastq file')
    parser.add_argument('-i2', '--fq2_in', help='the input R2 fastq file')
    parser.add_argument('-o1', '--fq1_out', help='the output R1 fastq file')
    parser.add_argument('-o2', '--fq2_out', help='the output R2 fastq file')
    parser.add_argument('-m', '--move', 
                        help='two digit number; left digit is which fq to pull from and right digit is which fq to push to', 
                        default='21', type=str, choices=['11','12','21','22'])
    parser.add_argument('-s', '--source_position', 
                        help='source sequence; integer means to pull the first n bases; positive is from 5-prime end and negative is from 3 prime', 
                        default=-8, type=int)
    parser.add_argument('-d', '--destination', help='where to put the source sequence; set to 5 for 5-prime and 3 for 3-prime', choices=[5,3], type=int, default=5)
    return parser.parse_args()


def pull_subseq(sequence: str, source_position: int) -> tuple[str, str]:
    """Pull Subsequence From Sequence
    Given a sequence, split it and return the two parts (one to keep and one to move)
    Input
        sequence: the sequence that we want to split
        source_position: how we want to split the sequence
            if positive n; move the first n bases and keep the rest
            if negative n; move the last n bases and keep the rest
    Return
        a tuple of (keep sequence, move sequence)
    """
    if source_position >= 0:
        return (sequence[source_position:], sequence[:source_position])
    else:
        return (sequence[:source_position], sequence[source_position:])
    

def update_sequence(sequence: str, subseq: str, destination: int) -> str:
    """Add Subsequence to Sequence
    Input
        sequence: the sequence to add subsequence to
        subseq: the subsequence to add to the sequence
        destination: tells us if subseq should go to 3' or 5' end
    Return
        string: a new sequence
    """
    if destination == 5:
        return subseq + sequence
    elif destination == 3:
        return sequence + subseq


def shift_bases(arguments) -> None:
    """Shift Bases and Create New FastQs
    Input
        arguments: this is the output from "get_arguments()" function
    Returns
        None
    Outputs
        new fastq1 and fastq2 files
    """
    with open(arguments.fq1_in, 'r') as i1, open(arguments.fq2_in, 'r') as i2, open(arguments.fq1_out, 'w') as o1, open(arguments.fq2_out, 'w') as o2:
        for line1, line2 in zip(i1, i2):
            # If sequence name (starts with "@" or "+"), just output line as no processing needed
            if (line1.startswith('@') and line2.startswith('@')) or \
                (line1.startswith('+') and line2.startswith('+')):
                o1.write(line1)
                o2.write(line2)
                continue
            # set default sequence (base or quality)
            seq1 = line1.strip() # read 1 bp seq or quality sequence
            seq2 = line2.strip() # read 2 bp seq or quality sequence
            subseq = '' # the sequence to pull
            # pull shifted sequence (base or quality) based on source
            if arguments.move[0] == '1':
                seq1, subseq = pull_subseq(seq1, arguments.source_position)
            elif arguments.move[0] == '2':
                seq2, subseq = pull_subseq(seq2, arguments.source_position)
            # update the destination sequence
            if arguments.move[1] == '1':
                seq1 = update_sequence(seq1, subseq, arguments.destination)
            elif arguments.move[1] == '2':
                seq2 = update_sequence(seq1, subseq, arguments.destination)
            # now write the sequences of interest
            o1.write(seq1 + '\n')
            o2.write(seq2 + '\n')
    return


def main():
    args = get_arguments()
    shift_bases(args)


if __name__ == '__main__':
    main()