#!/usr/bin/env python

# -*- coding: utf-8 -*-

import names
import random
import os 
import binascii
import shutil

def random_gen():
    left = [
        "admiring",
        "adoring",
        "affectionate",
        "agitated",
        "amazing",
        "angry",
        "awesome",
        "beautiful",
        "blissful",
        "bold",
        "boring",
        "brave",
        "busy",
        "charming",
        "clever",
        "compassionate",
        "competent",
        "condescending",
        "confident",
        "cool",
        "cranky",
        "crazy",
        "dazzling",
        "determined",
        "distracted",
        "dreamy",
        "eager",
        "ecstatic",
        "elastic",
        "elated",
        "elegant",
        "eloquent",
        "epic",
        "exciting",
        "fervent",
        "festive",
        "flamboyant",
        "focused",
        "friendly",
        "frosty",
        "funny",
        "gallant",
        "gifted",
        "goofy",
        "gracious",
        "great",
        "happy",
        "hardcore",
        "heuristic",
        "hopeful",
        "hungry",
        "infallible",
        "inspiring",
        "intelligent",
        "interesting",
        "jolly",
        "jovial",
        "keen",
        "kind",
        "laughing",
        "loving",
        "lucid",
        "magical",
        "modest",
        "musing",
        "mystifying",
        "naughty",
        "nervous",
        "nice",
        "nifty",
        "nostalgic",
        "objective",
        "optimistic",
        "peaceful",
        "pedantic",
        "pensive",
        "practical",
        "priceless",
        "quirky",
        "quizzical",
        "recursing",
        "relaxed",
        "reverent",
        "romantic",
        "sad",
        "serene",
        "sharp",
        "silly",
        "sleepy",
        "stoic",
        "strange",
        "stupefied",
        "suspicious",
        "sweet",
        "tender",
        "thirsty",
        "trusting",
        "unruffled",
        "upbeat",
        "vibrant",
        "vigilant",
        "vigorous",
        "wizardly",
        "wonderful",
        "xenodochial",
        "youthful",
        "zealous",
        "zen"
    ]

    adj = random.choice(left)
    prenom = names.get_first_name()

    res = adj + "_" + prenom
    return res


def has_duplicates(list_a, list_b, list_c):
    all_elements = set()
    all_elements.update(list_a)
    all_elements.update(list_b)
    all_elements.update(list_c)
    return len(all_elements) != len(list_a) + len(list_b) + len(list_c)

def read_file(filename):
    with open(filename, 'r', encoding="utf-8") as file:
        content = file.read()
    return content

def write_to_file(file_name, line):
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(line + "\n")

def write_to_file_bytes(file_name, line):
    with open(file_name, 'wb') as file:
        file.write(line)

def print_random_line(file_quotes_content, output_destination):
    lines = file_quotes_content.splitlines()
    random_line = random.choice(lines)
    index = lines.index(random_line)
    output_destination = output_destination + ("/" + random_gen() + "_" + str(index) )
    write_to_file(output_destination, random_line)

def mdkir_quotes(name, listbc, file_quotes_content):
    path = name + listbc
    os.mkdir (path)
    sub_path = path + ("/" + random_gen())
    os.mkdir (sub_path)
    print_random_line(file_quotes_content, sub_path)
    sub_path = path + ("/" + random_gen())
    os.mkdir (sub_path)
    print_random_line(file_quotes_content, sub_path)
    sub_path = path + ("/" + random_gen())
    os.mkdir (sub_path)
    print_random_line(file_quotes_content, sub_path)


def recurse_delete_dir(path):
    if not os.path.exists(path):
        return
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            shutil.rmtree(item_path)

def convert_flag():#14
    filename = '/root/flag'
    with open(filename, 'rb') as f:
        content = f.read()
    return(binascii.hexlify(content))

def split_flag(hex):
    part_size = len(hex) // 14
    flag_parts = []

    for i in range(14):
        start = i * part_size
        end = start + part_size
        if i == 13:
            end = None
        flag_parts.append(hex[start:end])
    return flag_parts



def main():
    #recurse_delete_dir("/var/www/html")
    max_attempts = 3
    attempt = 0
    split_idx = 0
    while attempt < max_attempts:
        try:
            file_quotes_content = read_file("/root/Knuth_quotes")
            liste_a = []
            liste_b = []
            liste_c = []
            for i in range(150):
                a = random_gen()
                b = random_gen()
                c = random_gen()

                if has_duplicates(liste_a + [a], liste_b + [b] , liste_c + [c] ):
                    while True: 
                        a = random_gen()
                        b = random_gen()
                        c = random_gen()
                        if not has_duplicates(liste_a + [a], liste_b + [b] , liste_c + [c] ):
                            break

                liste_a.append(a)
                liste_b.append(b)
                liste_c.append(c)

            str_mkdir = "/var/www/html/"
            for i in range(150):
                if i == 7 or i == 43 or i == 77:
                    str_mkdir_tmp = str_mkdir
                    os.mkdir (str_mkdir + liste_a[i])
                    mdkir_quotes(str_mkdir, liste_b[i], file_quotes_content)
                    mdkir_quotes(str_mkdir, liste_c[i], file_quotes_content)
                elif i == 37 or i == 73 or i == 123:
                    os.mkdir (str_mkdir + liste_a[i])
                    mdkir_quotes(str_mkdir, liste_c[i], file_quotes_content)
                    src = str_mkdir + liste_b[i]
                    write_to_file ("/root/symlink" + str(i), "Creation de symlink de : \n" + str_mkdir + "\nvers str_mkdir_tmp : \n" + str_mkdir_tmp + "\n" )
                    os.symlink(str_mkdir_tmp, src )             
                else:
                    os.mkdir(str_mkdir + liste_a[i])
                    mdkir_quotes(str_mkdir, liste_b[i], file_quotes_content)
                    mdkir_quotes(str_mkdir, liste_c[i], file_quotes_content)
                if i == 149:
                    write_to_file_bytes(str_mkdir + liste_a[i] + "/" + "flag.txt", split_flag(convert_flag())[split_idx])
                    write_to_file("/root/soluce.txt", "Fin du labyrinthe : " + str_mkdir + liste_a[i])
                else:
                    if (i % 11) == 1 and i != 1 :
                        write_to_file_bytes(str_mkdir + liste_b[i] + "/" + "flag.txt", split_flag(convert_flag())[split_idx])
                        split_idx = split_idx + 1
                    str_mkdir = str_mkdir + liste_a[i] + "/"
            
        except OSError as e:
            if e.errno == 17:
                attempt += 1
                print("Le dossier existe déjà. Voici la valeur de i : %i", i)
                if attempt == max_attempts:
                    print("Nombre maximal de tentatives atteint. Arrêt du script.")
                    recurse_delete_dir("/var/www/html")
                    break
                else:
                    print("Recommencer depuis le début")
                    recurse_delete_dir("/var/www/html")
                    continue
            elif e.errno == 13:
                print("Permission refusée pour créer le dossier. ")
                break
            else:
                print("Erreur lors de la création du dossier :", e)
                raise
                break            
        break       


if __name__ == '__main__':
    main()








