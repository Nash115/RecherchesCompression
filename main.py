# Génération de fichiers

from random import randint
import zipfile
import time
import os

def generateFiles():
    car = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.?!:*/-_=()[]{}çéèà'"
    """
    for nbFile in range(1,10):
        with open("files/file" + str(nbFile+1) + ".txt","w",encoding="utf8") as file:
            for i in range(100000):
                file.write(car[randint(0,len(car)-1)])
    """
    with open("files/file0.txt","w",encoding="utf8") as file:
        for i in range(100000):
            file.write("a")
    with open("files/file1.txt","w",encoding="utf8") as file:
            for i in range(100000):
                file.write(car[randint(0,len(car)-1)])
            

# Ecriture du temps

listePourCSV = []

# Type, Compression, TempsMoyen, TailleInitiale, TailleFinale
# [{""}]

def writeInCSV(list):
    with open("temps.csv", "w", encoding="utf8") as f:
        header = ""
        for i in list[0].keys():
            if header != "":
                header += ", " + i
            else:
                header += i
        f.write(header + "\n")
        for i in list:
            content = ""
            for element in i.values():
                if content != "":
                    content += ", " + str(element)
                else:
                    content += str(element)
            f.write(content + "\n")
    return True

def moyenne(tab):
    s = 0
    for i in tab:
        s += i
    return s/len(tab)

for nbFile in range(2):
    for levelCompression in range(10):
        times = []
        tailleInitiale = os.path.getsize("files/file" + str(nbFile) + ".txt")
        for i in range(50):
            start_time = time.perf_counter()
            with zipfile.ZipFile("files/compressed/file"+ str(nbFile) + ".zip", "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.write("files/file" + str(nbFile) + ".txt", compresslevel=levelCompression)
            end_time = time.perf_counter()
            tailleFinale = os.path.getsize("files/compressed/file" + str(nbFile) + ".zip")
            elapsed_time = end_time - start_time
            times.append(elapsed_time*1000)
        moyenneTemps = moyenne(times)
        listePourCSV.append({"Type":nbFile, "Compression(0-9)":levelCompression, "TempsMoyen(ms)":moyenneTemps, "TailleInitiale(ko)":tailleInitiale/1000, "TailleFinale(ko)":tailleFinale/1000})
        writeInCSV(listePourCSV)
