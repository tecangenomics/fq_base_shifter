# [fq_base_shifter](https://github.com/tecangenomics/fq_base_shifter/tree/main)
## Introduction
Select Tecan Genomics library preparation kits include UMI or Molecular Tag sequences positioned behind the I1 index read (i7 sequence; **see Table 1 below**). To capture these UMI sequences, a user must sequence additional bases during the I1 index read (see your kit User Guide for details). This will result in a longer I1 index read sequence that includes the index sequence itself as well as the desired UMI sequence. Some sequencers may need to be configured to store the index read fastq for use as input with code in this repository. It may also be necessary to demultiplex data off-instrument after separating the index 1 sequence from the UMI sequence.

This repository (fq_base_shifter) allows users who want to perform UMI-based fastq sequence deduplication using [UMI-tools](https://github.com/CGATOxford/UMI-tools) and have the index sequence(s) in separate fastq files. When executed, this code will allow a user to move some number of basepairs from either end of a source fastq to either end of a destination fastq or to a new fastq file. If deduplicating sequence data generated with Tecan Genomics library preparation kits, move the UMI sequence from the 3' end of index 1 fastq file (I1) to the 5' of read 1 fastq file (R1) followed by downstream deduplication as described by UMI-tools.

Link to UMI-tools documentation: https://umi-tools.readthedocs.io/en/latest/QUICK_START.html#paired-end-sequencing

## Requirements
python 3.xx

## Usage

The command to move 8 UMI bases from 3' of 16 base I1 file to the 5' end of an R1 file is: \
`python move_fq_seq.py -si I1.fq -di R1.fq -so I1_without_UMI.fq -do R1_with_UMI.fq`

[fq_base_shifter](https://github.com/tecangenomics/fq_base_shifter/tree/main) assumptions:
1. The data are unzipped
2. The source file is a superset of the destination file (all entries in destination file is in source, but the converse is not necessarily true)
3. Input file entries are in the same order (not taking into account missing entries)
4. Bases are moved, not copied. So R1_sequence + R2_sequence remains the same before and after running the code
5. Only performs operations on the ends of reads, not on the middle of reads (e.g. can't extract bases 10-12)

## Additional Options
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
---

## Table 1.
**Tecan Genomics library preparation kits and specific adaptor plates that include I1-based UMI sequences (N6 or N8 Molecular Tag).**
| Kit  | Adaptor plate PN | UMI/Molecular tag lenth |
| ------------- | ------------- | :-------------: |
| Universal Plus mRNA-Seq  | S02622 (24 rxn) | N8 |
| Universal Plus mRNA-Seq  | S02480 (96 rxn plate A) | N8 |
| Universal Plus mRNA-Seq  | S02690 (96 rxn plate B) | N8 |
| Universal Plus mRNA-Seq  | 30185200 (96 rxn plate C) | N8 |
| Universal Plus mRNA-Seq  | 30185201 (96 rxn plate D) | N8 |
| Universal Plus Total RNA-Seq  | S02622 (24 rxn) | N8 |
| Universal Plus Total RNA-Seq  | S02480 (96 rxn plate A) | N8 |
| Universal Plus Total RNA-Seq  | S02690 (96 rxn plate B) | N8 |
| Universal Plus Total RNA-Seq  | 30185200 (96 rxn plate C) | N8 |
| Universal Plus Total RNA-Seq  | 30185201 (96 rxn plate D) | N8 |
| Ovation SoLo RNA-Seq | S02221 (32 rxn) | N8 |
| Ovation SoLo RNA-Seq | S02238 (96 rxn) | N8 |
| Ovation SoLo RNA-Seq | S02574 (96 rxn) | N8 |
| Ovation Ultralow Systen V2 DNA-Seq | S02215 (96 rxn UDI) | N8 |
| Ovation RRBS Methyl-Seq | S02140 - S02155 (tubes, 6 nt index) | N6 |
| Ovation RRBS Methyl-Seq | S02223 (96 rxn, custom product) | N8 |
