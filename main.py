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

    @staticmethod
    def read_from_file(filename):
        with open(filename, 'r') as f:
            return f.read()

    def __init__(self):
        parser = argparse.ArgumentParser()
        input_group = parser.add_mutually_exclusive_group(required=True)
        input_group.add_argument('--encrypt', help='path to source file')
        input_group.add_argument('--decrypt', help='path to source file')
        input_group.add_argument('--gen-key', dest='generate',
                                 help='prompt to generate key pair',
                                 action='store_true')
        parser.add_argument('--key', default='key',
                            help='path to key (default key.pub, key.prv)')
        parser.add_argument('--output', default='out.txt', required=True,
                            help='path to resulting file')
        args = parser.parse_args()
        print(args)

        self.file_to_encrypt = args.encrypt
        self.file_to_decrypt = args.decrypt
        self.output_file = args.output
        self.key_file_name = args.key
        self.generate_key = args.generate
        self.__input = ''
        self.__output = ''
        self.__key = []

        self.handle_input()

    def handle_input(self):
        if self.generate_key:
            n, e, d = self.generate_key_pair()
            f = self.output_file
            self.output_file = f + '.pub'
            self.__output = '{}\n{}'.format(n, e)
            self.save_to_file()
            self.output_file = f + '.prv'
            self.__output = '{}\n{}'.format(n, d)
            self.save_to_file()
            self.output_file = f
            self.__output = ''
        elif self.file_to_encrypt is not None:
            key = RSA.read_from_file(self.key_file_name + '.pub')
            if not key:
                raise FileNotFoundError('key is empty')
            mod, exp = key.split('\n')
            self.__key = (int(mod), int(exp))
            self.__input = RSA.read_from_file(self.file_to_encrypt)
            self.encrypt()
            self.save_to_file()
        elif self.file_to_decrypt is not None:
            key = RSA.read_from_file(self.key_file_name + '.prv')
            if not key:
                raise FileNotFoundError('key is empty')
            mod, exp = key.split('\n')
            self.__key = (int(mod), int(exp))
            self.__input = RSA.read_from_file(self.file_to_decrypt)
            self.encrypt()
            self.save_to_file()
        else:
            raise RuntimeError('invalid input')

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

    def encrypt(self):
        self.__output = ((ord(x) ** self.__key[1]) % self.__key[0]
                         for x
                         in self.__input)
        self.__output = (chr(x) for x in self.__output)
        self.__output = ''.join(self.__output)

    def save_to_file(self):
        print('save_to_file(self)')
        with open(self.output_file, 'w') as f:
            f.write(self.__output)


if __name__ == "__main__":
    RSA()
