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
import dataclasses


def get_arguments():
    """
    parses arguments from command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-si', '--s_in', help='the file to extract sequences from')
    parser.add_argument('-di', '--d_in', help='the file to add sequences to')
    parser.add_argument('-so', '--s_out', help='the file after sequence removed; will not output if missing',
                        default=None)
    parser.add_argument('-do', '--d_out', help='the file after sequence added; will not output if missing',
                        default=None)
    parser.add_argument('-sp', '--s_pos', 
                        help='source sequence to extract; integer means to pull the first n bases; positive is from 5-prime end and negative is from 3 prime', 
                        default=-6, type=int)
    parser.add_argument('-dm', '--d_method', 
                        help='1: move sequences between existing files. \n 2: create new destination file with extracted sequences from source', 
                        default='2', type=int, choices=[1, 2])
    parser.add_argument('-dl', '--d_loc', 
                        help='where to put the source sequence; set to 5 for 5-prime and 3 for 3-prime', 
                        default=5, type=int, choices=[5,3])
    return parser.parse_args()


@dataclasses.dataclass
class FastqSequenceMover:
    """Class to use and run base shift command"""
    source_in: str # source file
    source_out: str # output source file
    dest_in: str # destination file
    dest_out: str # output destination file
    source_pos: int # what part of the source sequence to move
    dest_loc: int # where in the destination to put the sequence

    def __split_sequence(self, sequence: str, position: int) -> tuple[str, str]:
        """
        splits a source sequence into the sequence to keep and sequence to move
        Input:
            sequence: the sequence we want to split
            position: how we want to split the sequence
                if positive n; move the first n bases and keep the rest
                if negative n; move the last n bases and keep the rest
        Return
            Tuple of (sequence to keep, sequence to shift)
        """
        if position >= 0:
            return (sequence[position:], sequence[:position])
        else:
            return (sequence[:position], sequence[position:])
        
    def __update_sequence(self, sequence: str, subseq: str, destination: int) -> str:
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
        
    def __mod_identifier(self, id: str) -> str:
        """remove /1 or /2 at the end of reads
        Inputs
            id: the sequence identifier
        Returns
            string: an id without the /1 or /2 at the end of it if present
        """
        if id.endswith('/1') or id.endswith('/2'):
            return id[:-2]
        return id
        

    def __writer(self, io_wrapper, data_to_write: str) -> None:
        """Writes Data To IO
        Input
            io_wrapper: an object generated from open() function with write option OR None
            data_to_write: the data we want to write to the io_wrapper
        """
        if io_wrapper:
            io_wrapper.write(data_to_write)
        return


    def shift_seq_existing_destination(self) -> None:
        """Shift Bases between existing files
        Returns
            None
        Outputs
            new destination files and maybe source files
        """
        line_d_counter = 0 # only modify lines tnat are even (%2 == 0)
        #source_id = ''
        with open(self.source_in, 'r') as si, open(self.dest_in, 'r') as di:
            # open output files if they were specified
            so = open(self.source_out, 'w') if self.source_out else self.source_out
            do = open(self.dest_out, 'w') if self.dest_out else self.dest_out
            for line_s, line_d in zip(si, di): # loop through destination file, as it might not have all the reads as in the source file
                line_d_counter += 1
                # check if read identifiers are the same
                source_id = line_s.strip().split()[0]
                #print(self.__mod_identifier(line_d.strip().split()[0]), self.__mod_identifier(source_id))
                if line_d_counter % 4 == 1:
                    dest_id = self.__mod_identifier(line_d.strip().split()[0])
                    while self.__mod_identifier(source_id) != dest_id:
                        #print(self.__mod_identifier(source_id))
                        source_id = next(si).strip().split()[0]
                # no need to process non-sequence/quality lines, so output them as needed
                if line_d_counter % 2 == 1:
                    self.__writer(so, line_s)
                    self.__writer(do, line_d)
                    continue
                # pull shifted sequence (base or quality) based on source
                seq_new_source, subseq_shift = self.__split_sequence(line_s.strip(), self.source_pos)
                # update the destination sequence
                seq_new_dest = self.__update_sequence(line_d.strip(), subseq_shift, self.dest_loc)
                # now write the sequences of interest
                self.__writer(so, seq_new_source + '\n')
                self.__writer(do, seq_new_dest + '\n')
            if self.source_out:
                so.close()
            if self.dest_out:
                do.close()
        return
    
    def shift_seq_new_destination(self) -> None:
        """Shift Bases to empty file
        Returns
            None
        Outputs
            new destination files and maybe source files
        """
        line_counter = 0 # only modify lines tnat are even (%2 == 0)
        with open(self.source_in, 'r') as si:
            # open output files if they were specified
            so = open(self.source_out, 'w') if self.source_out else self.source_out
            do = open(self.dest_out, 'w') if self.dest_out else self.dest_out
            for line_s in si: # loop through destination file, as it might not have all the reads as in the source file
                line_counter += 1
                # no need to process non-sequence/quality lines, so output them as needed
                if line_counter % 2 == 1:
                    self.__writer(so, line_s)
                    self.__writer(do, line_s)
                    continue
                # pull shifted sequence (base or quality) based on source
                seq_new_source, subseq_shift = self.__split_sequence(line_s.strip(), self.source_pos)
                # now write the sequences of interest
                self.__writer(so, seq_new_source + '\n')
                self.__writer(do, subseq_shift + '\n')
            if self.source_out:
                so.close()
            if self.dest_out:
                do.close()
        return
        

def main():
    args = get_arguments()
    fastq = FastqSequenceMover(args.s_in, args.s_out, args.d_in, args.d_out, args.s_pos, args.d_loc)
    if args.d_method == 1:
        fastq.shift_seq_existing_destination()
    elif args.d_method == 2:
        fastq.shift_seq_new_destination()


if __name__ == '__main__':
    main()