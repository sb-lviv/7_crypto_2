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

    @staticmethod
    def save_to_file(filename, data):
        with open(filename, 'w') as f:
            f.write(data)

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

    def handle_input(self):
        if self.generate_key:
            n, e, d = RSA.generate_key_pair()

            output_file = self.output_file + '.pub'
            output_text = '{}\n{}'.format(n, e)
            RSA.save_to_file(output_file, output_text)

            output_file = self.output_file + '.prv'
            output_text = '{}\n{}'.format(n, d)
            RSA.save_to_file(output_file, output_text)

        elif self.file_to_encrypt is not None:
            key = RSA.read_from_file(self.key_file_name + '.pub')
            if not key:
                raise FileNotFoundError('key is empty')
            key = [int(x) for x in key.split('\n')]

            data = RSA.read_from_file(self.file_to_encrypt)
            data = RSA.encrypt(data, key)
            RSA.save_to_file(self.output_file, data)

        elif self.file_to_decrypt is not None:
            key = RSA.read_from_file(self.key_file_name + '.prv')
            if not key:
                raise FileNotFoundError('key is empty')
            key = [int(x) for x in key.split('\n')]

            data = RSA.read_from_file(self.file_to_decrypt)
            data = RSA.encrypt(data, key)
            RSA.save_to_file(self.output_file, data)

        else:
            raise RuntimeError('invalid input')

    @staticmethod
    def generate_key_pair():
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

    @staticmethod
    def encrypt(data, key):
        output = ((ord(x) ** key[1]) % key[0] for x in data)
        output = (chr(x) for x in output)
        return ''.join(output)


if __name__ == "__main__":
    RSA().handle_input()
