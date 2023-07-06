import argparse
import RLBL
from matplotlib import pyplot as plt
import cv2 as cv

def generate_args():
    parser = argparse.ArgumentParser(
                prog='python3 main.py',
                description='Comprime uma imagem',
                epilog='Compressor de imagem Flyweight')
    parser.add_argument('-i', action='store', required = True, 
                        help='Arquivo de entrada', metavar='input')
    parser.add_argument('-o', action='store', 
                        help='arquivo de saida(sem extensao)', metavar='output')
    parser.add_argument('-d', action='store_true',
                        help='Descomprimir')
    parser.add_argument('-c', action='store_true',
                        help='Comprimir')
    parser.add_argument('-e', action='store_true',
                        help='Estimar compressao')

    return parser.parse_args()

if __name__ == '__main__':
    args = generate_args()

    if args.e or args.c:
        cpr = RLBL.compressor(args.i, args.o)

    if args.e:
        cpr.calculate_compression()
    
    if args.c:
        cpr.compress()
    elif args.d:
        dpr = RLBL.descompressor(args.i)
        img = dpr.decompress()
        cv.imwrite(args.o, img)
