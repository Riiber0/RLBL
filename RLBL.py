import cv2 as cv
import numpy as np
import io
from collections import deque

"""
 0             1               2               3               4
 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7 0 1 2 3 4 5 6 7
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|        altura da imagem       |       largura da imagem       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|               Tamanho do vetor de valores                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
"""


class compressor(object):

    """Classe compressor de imagem"""

    def __init__(self, input_file, output_file):
        """

        :input_file: arquivo de entrada
        :output_file: arquico de saida

        """
        self.input_file = input_file
        self.output_file = output_file

    def open_image(self):
        image = cv.imread(self.input_file)
        assert image is not None, 'imagem nao pode ser aberta'
        print('imagem aberta')
        dimention = [image.shape[0], image.shape[1]]
        print('dimessao da imagem: ', dimention)
        ret_img = image.reshape(image.shape[0]*image.shape[1], 3)
        return ret_img, dimention 

    def calculate_compression(self):
        img, dimention = self.open_image()
        cont = 0
        for p in range(0, 3):
            last = img[0][p]
            for pixel in img:
                if pixel[p] != last:
                    last = pixel[p]
                    cont += 1


        print('Compressor localizacao em bit e reparticao de cores', 
              '%0.2f' % (100 * (1 - ((cont + 3*len(img)//8)/(len(img)*3)))))
        print('Compressor sem localizacao em bit e reparticao de cores', 
              '%0.2f' % (100 * (1 - ((cont*2)/(len(img)*3)))))

        cont = 0
        last = img[0]
        for pixel in img:
            if (pixel != last).any():
                last = pixel
                cont += 1

        print('Compressor localizacao em bit sem reparticao de cores',
              '%0.2f' % (100 * (1 - ((cont*3 + len(img)//8))/(len(img)*3))))
        print('Compressor sem localizacao em bit sem reparticao de cores',
              '%0.2f' % (100 * (1 - ((cont*3 + cont))/(len(img)*3))))

    def write_file(self, values, b_matriz, dimention):
        out = open(self.output_file, 'wb')
        
        out.write(dimention[0].to_bytes(2))
        out.write(dimention[1].to_bytes(2))
        out.write(len(values).to_bytes(4))

        for value in values:
            out.write(value)

        rest = (dimention[0]*dimention[1])%8
        print('resto', rest)

        out.write(rest.to_bytes(1))

        for data in b_matriz:
            for i in range(0, 8 - rest):
                data.append(0)

            data = [data[8*i:8*(i+1)] for i in range(len(data)//8)]
            print(len(data))

            compress_vector = list()
            for byte in data:
                aux = 0
                for bit in byte:
                    aux = aux << 1
                    aux += bit
                compress_vector.append(aux)

            for byte in compress_vector:
                out.write(byte.to_bytes(1))

    def map_color(self, img, p, values):
        values.append(img[0][p])
        last = values[0]
        map_p = list()

        for pixel in img:
            if pixel[p] != last:
                map_p.append(1)   
                values.append(pixel[p])
                last = pixel[p]
            else:
                map_p.append(0)

        return map_p


    def compress(self):
        img, dimention = self.open_image()
        #img = img[0:20]
        b_matriz = list()
        values = list()

        for i in range(0, 3):
            aux = self.map_color(img, i, values)
            b_matriz.append(aux)

        self.write_file(values, b_matriz, dimention)

class descompressor(object):

    def __init__(self, input_file):
        """

        :input_file: arquivo

        """
        self.input_file = input_file

    def decompress(self):
        file = open(self.input_file, 'rb')

        altura = int.from_bytes(file.read(2))
        largura = int.from_bytes(file.read(2))
        print('dimensao da imagem:', altura, largura)
        pixel_amount = altura*largura
        print('quantidade de pixel', pixel_amount)

        values_len = int.from_bytes(file.read(4))
        values = deque(list(file.read(values_len)))

        rest = int.from_bytes(file.read(1))
        print('redto', rest)

        ret_img = np.zeros((pixel_amount, 3))
        for i in range(0, 3):
            img_index = 0
            value = values.popleft()

            buff = list(file.read(pixel_amount//8 ))
            print('tamanho do buffer lido',len(buff))
            for byte in buff:
                for bit in range(0, 8):
                    if byte & 128 == 128:
                        value = values.popleft()

                    byte = byte << 1
                    ret_img[img_index][i] = value
                    img_index += 1
                #print(img_index)

            
            if rest == 0:
                rest = 8

            byte = int.from_bytes(file.read(1))
            for bit in range(0 , rest):
                if byte & 128 == 128:
                    value = values.popleft()

                byte << 1
                ret_img[img_index][i] = value
                img_index += 1

        ret_img = ret_img.reshape(altura, largura, 3)
        ret_img = ret_img.astype(int)
        return ret_img
        
