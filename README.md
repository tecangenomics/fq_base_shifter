# Intro
The customer wants to perform umi deduplication using umi-tools. According to the documentation(https://umi-tools.readthedocs.io/en/latest/QUICK_START.html#paired-end-sequencing), *the UMI sequence should be on the 5' end of R1, however the UMI in the data is at the 3' end of R2*


This code will move some number of basepairs from some end of a source fastq to a destination fastq.

# Requirements
python 3.xx

# Usage
## Quickstart
This code will, by default, move the last 6 bases (and quality scores) of a source file to a new file.

The command to move last 6 bases of a source file (e.g. R2) to a new and separate file (e.g. one called umi.fq) is: \
`python move_fq_seq.py -si reads_R2.fq -do umi.fq`

The command to move the same 6 bases from umi.fq to the 5' end of an R1 file is: \
`python move_fq_seq.py -si umi.fq -di reads_R1.fq -do reads_R1_umi.fq -dm 1`

The assumptions made are as follows:
1. The data are unzipped
2. The source file is a superset of the destination file (all entries in destination file is in source, but the converse is not necessarily true)
3. Input file entries are in the same order (not taking into account missing entries)
4. Bases are moved, not copied. So R1_sequence + R2_sequence remains the same before and after running the code
5. Only performs operations on the ends of reads, not on the middle of reads (e.g. can't extract bases 10-12)

# Additional Options
When running with the -h option, a list of possible options are provided. Below are explanations of these options:
```
Required
-si/-di: These are the input source and destination files. di is not needed if -dm is set to 2

Optional
-so/-do: These are the outputs for the source and destination files. If they are not specified, a corresponding file is not created.
         E.g. if -so is included and -do is NOT included, only a file with bases removed from the source file is generated
-sp: An integer corresponding to the number of bases to move from the source sequence. 
     A positive number corresponds to moving the bases from the 5' end and a negative the 3' end.
     Defaults to -6
-dm: Where are we moving sequences to and from? Set to 1 to indicated that sequences are being moved between existing
     source and destination file. Set to 2 to move sequences from the source file to a new/nonexistent destination file (be careful, as
     existing filenames matching -do will be overwritten).
     Defaults to 2
-dl: Either 3 or 5. Corresponds to whether we want the sequence to be moved to the 3' or 5' end of
     the destination fastq file.
     Defaults to 5
```
