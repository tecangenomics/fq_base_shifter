'''
Will move bases from one fastq file to another. 
Assumptions:
- source and destination files are in the same order
- source is a superset of destination
'''
import argparse

def get_arguments():
    """
    parses arguments from command line
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--destination', help='the file to add sequences to')
    parser.add_argument('-s', '--source', help='the file to extract sequences from')
    parser.add_argument('-o', '--output', help='file with source sequences added to destination file')
    parser.add_argument('-s_len', '--sequence_length', 
                        help='DEFAULT=-8; length of the source sequence to extract; positive is from 5-prime end and negative is from 3 prime', 
                        default=-8, type=int)
    parser.add_argument('-d_loc', '--destination_location', 
                        help='DEFAULT=5; where to put the source sequence; set to 5 for 5-prime and 3 for 3-prime', 
                        default=5, type=int, choices=[5,3])
    return parser.parse_args()


class SequenceShifter:
    def __init__(self, destination:str, source:str, output:str, sequence_length:int, destination_location:int):
        self.destination = destination
        self.source = source
        self.output = output
        self.sequence_length = sequence_length
        self.destination_location = destination_location

    def __clean_read_name(self, read_id: str) -> str:
        """remove /1 or /2 at the end of reads
        Inputs
            id: the sequence identifier
        Returns
            string: an id without the /1 or /2 at the end of it if present
        """
        id = read_id.strip().split()[0]
        if id.endswith('/1') or id.endswith('/2'):
            return id[:-2]
        return id

    def __pull_source_sequence(self, sequence:str) -> str:
        '''
        Returns the part of the sequence we want to move from the source file
        as determined be self.sequence_length
        '''
        if self.sequence_length >= 0:
            return sequence[:self.sequence_length]
        else:
            return sequence[self.sequence_length:]

    def __create_output_sequence(self, destination_sequence:str, shifted_sequence:str) -> str:
        '''
        Given a destination sequence and the shifted sequence (to insert into destination),
        Return the output sequence based on self.destination_location
        '''
        if self.destination_location == 5: # add shifted sequence to 5' end
            return shifted_sequence + destination_sequence
        elif self.destination_location == 3: # add shifted sequence to 3' end
            return destination_sequence + shifted_sequence
        else: # an unallowed destination location is provided
            raise Exception('An invalid destination location is provided')

    def parse_fastqs(self) -> None:
        '''
        Loops through destination and then source file and outputs an updated fastq file
        '''
        # open all files
        destination_fs = open(self.destination, 'r')
        source_fs = open(self.source, 'r')
        output_fs = open(self.output, 'w')
        # loop through destination file
        destination_line_number = 0 # keep track of which line from destination file we're on
        source_name = '' # the current source read name/id we're one
        for destination_line in destination_fs:
            destination_line_number += 1
            if destination_line_number % 4 == 1: # handle line containing read information
                destination_name = self.__clean_read_name(destination_line)
                # keep looping through source file until the source read is the same as destination read
                while destination_name != source_name:
                    source_name = self.__clean_read_name(next(source_fs))
                # output the name
                output_fs.write(destination_line)
            elif destination_line_number % 2 == 0: # handle line containing sequence or quality, which are even number lines
                # the above should be the same as %4 == 0 AND %4 ==2 
                # note that the pointer in the source file is currently one line above the sequence of interest
                source_sequence = next(source_fs).strip()
                destination_sequence = destination_line.strip()
                # figure out what sequence to move
                shifted_sequence = self.__pull_source_sequence(source_sequence)
                # get the new sequence to output
                output_sequence = self.__create_output_sequence(destination_sequence, shifted_sequence)
                # write the line
                output_fs.write(f'{output_sequence}\n')
            elif destination_line_number % 4 == 3: # this line should only have the + sign
                # note that the pointer in the source file is currently one line above the sequence of interest
                source_plus = next(source_fs)
                output_fs.write(destination_line)
            else: # this should not be possible
                raise Exception('We have hit a line that does not mathc  %4==1, %4==3, and %2==0')
        return


def main():
    args = get_arguments()
    # initialize class and run necessary class functions
    sequence_shifter = SequenceShifter(args.destination, args.source, args.output, args.sequence_length, args.destination_location)
    sequence_shifter.parse_fastqs()
    return


if __name__ == '__main__':
    main()
