#!/usr/bin/env python3

import argparse
import random


class RSA(object):

    ACTIONS = [
        'generate key',
        'encrypt',
        'decrypt',
    ]

    @staticmethod
    def prime(val=3):
        while True:
            for n in range(2, val):
                if (val % n) == 0:
                    break
            else:
                yield val
            val += 1

    def __init__(self):
        parser = argparse.ArgumentParser()
        input_group = parser.add_mutually_exclusive_group()
        input_group.add_argument('--encrypt', help='path to source file')
        input_group.add_argument('--decrypt', help='path to source file')
        input_group.add_argument('--gen-key', default=False, dest='generate',
                                 help='prompt to generate key pair',
                                 action='store_true')
        parser.add_argument('--key', help='path to key')
        parser.add_argument('--seed', '-s', default=0, type=int,
                            help='used for random generators')
        parser.add_argument('--output', default='out.txt', required=True,
                            help='path to resulting file')
        args = parser.parse_args()

        self.file_to_encrypt = args.encrypt
        self.file_to_decrypt = args.decrypt
        self.output_file = args.output
        self.key_file_name = args.key
        self.__input = ''
        self.__output = ''
        self.__key = ''
        self.__seed = args.seed
        self.__action = ''


if __name__ == "__main__":
    RSA()
