# Intro
The customer wants to perform umi deduplication using umi-tools. According to the documentation(https://umi-tools.readthedocs.io/en/latest/QUICK_START.html#paired-end-sequencing), *the UMI sequence should be on the 5' end of R1, however the UMI in the data is at the 3' end of R2*


This code will move some number of basepairs from some end of some fastq to some end of the same or another fastq.

# Requirements
python 3.xx

# Usage
## Quickstart
This code will, by default, move the last 6 bases (and quality scores) of R2 to the beginning of R1:

`python move_fastq_bases.py -i1 input-R1.fq -i2 input-R2.fq -o1 output-R1.fq -o2 output-R2.fq`

The assumptions made are as follows:
1. The data are unzipped
2. The data are paired end (no single end reads)
3. R1 and R2 have the same number of entries with the same order
4. Bases are moved, not copied. So R1_sequence + R2_sequence remains the same before and after running the code
5. Only performs operations on the ends of reads, not on the middle of reads (e.g. can't extract bases 10-12)

# Additional Options
When running with the -h option, a list of possible options are provided. Below are explanations of these options:
```
Required
-i1/-i2: These are the inputs for the R1 and R2 fastqs
-o1/-o2: These are the outputs for the R1 and R2 fastqs

Optional
-m: A two digit number telling us which fq to pull from (left digit) and which to add to (right digit). 
    E.g. to move sequences from R1 to R2, provide 12. 
    Defaults to 21
-s: An integer corresponding to the number of bases to move from the source sequence. 
    A positive number corresponds to moving the bases from the 5' end and a negative the 3' end.
    Defaults to -6
-d: Either 3 or 5. Corresponds to whether we want the sequence to be moved to the 3' or 5' end of
    the destination fastq file.
    Defaults to 5
```
