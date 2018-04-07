#Written by Nathan Estrada (psychic2ombie,CyberNight)

import numpy as np
import re
import string
import sys


class Enigma:

    def __init__(self):

        if sys.version_info[0] < 3:
            print("YOU MUST BE USING PYTHON 3.x.x")
            exit()

        self.matrix = self.set_matrix_key()
        choice = input("1:Encode 2:Decode ")

        if choice == "1":
            self.phrase = input("Enter phrase to encode ")

            if self.phrase.__len__()%self.matrix.__len__() != 0:
                while self.phrase.__len__()%self.matrix.__len__() != 0:
                    self.phrase += " "

            self.encoded = [0 for x in range(self.phrase.__len__())]
            self.encode_string()
        if choice == "2":
            self.decode_string()

    def set_matrix_key(self):
        matrix_string = input("Input Key In Format:[[x,x,x],[x,x,x],[x,x,x]] ")
        mat = np.matrix([])
        if matrix_string.__len__() < 9:
            print("Enter Valid Matrix!")
            self.set_matrix_key()
        else:
            try:
                mat = np.matrix(eval(matrix_string))
            except Exception as e:
                print("Enter Valid Matrix")
                self.set_matrix_key()
            if mat.shape[0] != mat.shape[1]:
                print("Non-square Matrix! Check Matrix and Try Again")
                self.set_matrix_key()
        return mat

    def decode_string(self):
        matrices_string = input("Input list of matrices in format: [[x,x,x]]:[[x,x,x]]:[[x,x,x]]" +
                                "or [x,x,x]:[x,x,x]:[x,x,x] ")
        matrices = matrices_string.split(":")
        number_string = ""
        for matrix in matrices:
            mx = np.matrix(matrix)
            number_string += np.array2string(np.round(np.abs(mx * self.matrix.I))).replace(".", "")
        number_string = re.findall(r'\b\d+\b', number_string)
        text_string = ""
        for number in number_string:
            if number == "0":
                text_string += " "
            else:
                text_string += string.ascii_lowercase[int(number)-1]
        print(text_string)

    def encode_string(self):
        i = 0
        for l in self.phrase:
            self.encoded[i] = self.convert_char(l)
            i += 1
        arrays = self.split_list(self.encoded,int(self.encoded.__len__()/self.matrix.__len__()))
        print("Numbers:"+str(arrays))
        encoded = ""
        for a in arrays:
            mx = np.matrix(a)
            my = np.array(mx*self.matrix)
            encoded += np.array2string(my,separator=",")+":"
        print("Encoded Numbers:"+str(encoded[:-1]))

        out = ""
        for i in range(self.matrix.__len__()):
            temp = np.array2string(self.matrix[i], separator=",")
            temp = temp[:-1]
            temp = temp[1:]
            out += temp + ","
        key = "[" + out[:-1] + "]"

        print("Key:" + key)
        filename = input("Enter Name of output file ")
        f = open(filename+".txt",'w')
        f.truncate()
        f.write("Numbers:"+str(arrays)+"\n")
        f.write("Encoded Numbers:"+str(encoded[:-1])+"\n")
        f.write("Key:"+key)
        print("Result saved to "+filename+".txt")
        f.close()

    @staticmethod
    def split_list(alist, wanted_parts=1):
        length = len(alist)
        return [alist[i * length // wanted_parts: (i + 1) * length // wanted_parts]
            for i in range(wanted_parts)]

    @staticmethod
    def convert_char(old):
        if len(old) != 1:
            return 0
        new = ord(old)
        if 65 <= new <= 90:
            # Upper case letter
            return new - 64
        elif 97 <= new <= 122:
            # Lower case letter
            return new - 96
        # Unrecognized character
        return 0


main = Enigma()
