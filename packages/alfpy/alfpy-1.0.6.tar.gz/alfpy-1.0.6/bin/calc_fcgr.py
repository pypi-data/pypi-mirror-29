#! /usr/bin/env python

# Copyright (c) 2016 Zielezinski A, combio.pl

import argparse
import sys

from alfpy import fcgr
from alfpy.utils import distmatrix
from alfpy.utils import seqrecords
from alfpy.version import __version__


def get_parser():
    parser = argparse.ArgumentParser(
        description='''Calculate distances between DNA sequences based on
        Frequency Chaos Game Representation (FCGR) patterns of
        word occurrences.''',
        add_help=False, prog='calc_fcgr.py'
    )
    group = parser.add_argument_group('REQUIRED ARGUMENTS')
    group.add_argument('--fasta', '-f',
                       help='input FASTA sequence filename', required=True,
                       type=argparse.FileType('r'), metavar="FILE")
    group.add_argument('--word_size', '-w', required=True,
                       help='word size', type=int)

    group = parser.add_argument_group('OUTPUT ARGUMENTS')
    group.add_argument('--out', '-o', help="output filename",
                       metavar="FILE")
    group.add_argument('--outfmt', choices=['phylip', 'pairwise'],
                       default='phylip',
                       help='distances output format [DEFAULT: %(default)s]')

    group = parser.add_argument_group("OTHER OPTIONS")
    group.add_argument("-h", "--help", action="help",
                       help="show this help message and exit")
    group.add_argument('--version', action='version',
                       version='%(prog)s {}'.format(__version__))

    if len(sys.argv[1:]) == 0:
        # parser.print_help()
        parser.print_usage()
        parser.exit()
    return parser


def validate_args(parser):
    args = parser.parse_args()
    if args.word_size < 1:
        parser.error('--word_size must be >= 1')
    return args


def main():
    parser = get_parser()
    args = validate_args(parser)

    seq_records = seqrecords.read_fasta(args.fasta)

    vector = fcgr.create_vectors(seq_records, args.word_size)
    dist = fcgr.Distance(vector)
    matrix = distmatrix.create(seq_records.id_list, dist)

    if args.out:
        oh = open(args.out, 'w')
        matrix.write_to_file(oh, args.outfmt)
        oh.close()
    else:
        matrix.display(args.outfmt)


if __name__ == '__main__':
    main()
