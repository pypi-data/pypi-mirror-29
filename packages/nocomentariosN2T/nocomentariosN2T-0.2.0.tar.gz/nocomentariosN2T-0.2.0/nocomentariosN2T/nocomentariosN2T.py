# -*- coding: utf-8 -*-
import os

"""Main module."""


def noComentariosN2T():
    textname = "./"
    try:
        ruta = os.listdir(textname)
        print("funciono")
        for i in ruta:
            if(i[-3:] == ".vm"):
                print(i)
                archive = open(textname + "/" + i, "r")
                asm = ""
                File = open(textname + "/" + i[:-3] + "1.vm", "w")
                for linea in archive.readlines():
                    a = ""
                    if linea[0] != "/" and linea[0] != "\n":
                        a = linea.split("/")
                        asm += a[0]
                File.write(asm)
                File.close()
                archive.close()
    except NameError as a:
        print(a)
