# Génération de fichiers

from random import randint
import zipfile
import time
import os

def generateFiles():
    print("Génération des fichiers...")
    car = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.?!:*/-_=()[]{}çéèà'"
    """
    for nbFile in range(1,10):
        with open("files/file" + str(nbFile+1) + ".txt","w",encoding="utf8") as file:
            for i in range(100000):
                file.write(car[randint(0,len(car)-1)])
    """
    print("Génération du fichier 0")
    with open("files/file0.txt","w",encoding="utf8") as file:
        for i in range(10000000):
            file.write("a")
    print("Génération du fichier 1")
    with open("files/file1.txt","w",encoding="utf8") as file:
            for i in range(10000000):
                file.write(car[randint(0,len(car)-1)])

#generateFiles()

# Ecriture du temps

listePourCSV = []

# Type, Compression, TempsMoyen, TailleInitiale, TailleFinale
# [{""}]

def writeInCSV(list):
    print("Ecriture des données dans le fichier csv...")
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
        for i in range(50): #Effectue 50 fois la compression et donne une moyenne du temps 
            start_time = time.perf_counter()
            with zipfile.ZipFile("files/compressed/file"+ str(nbFile) + ".zip", "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
                zip_file.write("files/file" + str(nbFile) + ".txt", compresslevel=levelCompression)
            end_time = time.perf_counter()
            tailleFinale = os.path.getsize("files/compressed/file" + str(nbFile) + ".zip")
            elapsed_time = end_time - start_time
            times.append(elapsed_time*1000)
        moyenneTemps = round(moyenne(times),3)
        print("Temps de compression pour 'file" + str(nbFile) + ".txt' : " + str(moyenneTemps) + "ms. Avec une compression de " + str(levelCompression))

        for i in range(50):
            start_time = time.perf_counter()
            with zipfile.ZipFile("files/compressed/file"+ str(nbFile) + ".zip", "r") as zip_file:
                zip_file.extractall("files/compressed/extract")
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            times.append(elapsed_time*1000)
        moyenneTempsDecomp = round(moyenne(times),3)
        print("Temps de décompression pour 'file" + str(nbFile) + ".txt' : " + str(moyenneTempsDecomp) + "ms")

        listePourCSV.append({"Type":nbFile, "Compression(0-9)":levelCompression, "TempsMoyenCompression(ms)":moyenneTemps, "TempsMoyenDecompression(ms)":moyenneTempsDecomp, "TailleInitiale(ko)":tailleInitiale/1000, "TailleCompressee(ko)":tailleFinale/1000})
        writeInCSV(listePourCSV)
