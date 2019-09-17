#!/usr/bin/env python3

import argparse
import random
from math import gcd


class RSA(object):

    @staticmethod
    def prime(low=None, high=None):
        if low is not None:
            val = low
            while True:
                for n in range(2, val):
                    if (val % n) == 0:
                        break
                else:
                    yield val
                val += 1
        elif high is not None:
            val = high
            while True:
                for n in range(2, val):
                    if (val % n) == 0:
                        break
                else:
                    yield val
                val -= 1
                print(val)
                if val <= 0:
                    raise GeneratorExit()
        else:
            raise ValueError('You must specify a high or low number')

    def __init__(self):
        parser = argparse.ArgumentParser()
        input_group = parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument('--encrypt', help='path to source file')
        input_group.add_argument('--decrypt', help='path to source file')
        input_group.add_argument('--gen-key', dest='generate',
                                 help='prompt to generate key pair',
                                 action='store_true')
        parser.add_argument('--key', help='path to key')
        parser.add_argument('--output', default='out.txt', required=True,
                            help='path to resulting file')
        args = parser.parse_args()
        print(args)

        self.file_to_encrypt = args.encrypt
        self.file_to_decrypt = args.decrypt
        self.output_file = args.output
        self.key_file_name = args.key
        self.__input = ''
        self.__output = ''
        self.__key = ''

    def generate_key_pair(self):
        prime = RSA.prime(random.randint(10, 20))  # Magic number
        p = next(prime)
        q = next(prime)
        n = p * q
        euler = (p - 1) * (q - 1)
        print('p {}\tq {}\tn {}\teuler {}'.format(p, q, n, euler))

        e = next(prime)  # Magic number
        while gcd(e, euler) != 1:
            print(e, euler)
            e += 1

        d = 2
        while ((d * e) % euler) != 1:
            d += 1
            if d >= n:
                raise ValueError('secret key could not be found')

        return n, e, d


if __name__ == "__main__":
    print(RSA().generate_key_pair())
