#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import sqlite3
import csv
import json
import argparse

try:
    import win32crypt
except ImportError:
    pass

def parse_arguments():
    parser = argparse.ArgumentParser(description="Récupérer les mots de passe Google Chrome et WiFi")
    parser.add_argument("-o", "--output", choices=['csv', 'json'],
                        help="Exporter les mots de passe au format [ CSV | JSON ].")
    parser.add_argument(
        "-d", "--dump", help="Afficher les mots de passe dans la console. ", action="store_true")
    parser.add_argument(
        "-w", "--wifi", help="Récupérer les mots de passe WiFi. ", action="store_true")

    args = parser.parse_args()
    
    if args.dump:
        for data in recuperer_mots_de_passe(args.wifi):
            print(data)
    
    if args.output == 'csv':
        enregistrer_en_csv(recuperer_mots_de_passe(args.wifi))
    
    if args.output == 'json':
        enregistrer_en_json(recuperer_mots_de_passe(args.wifi))
    
    else:
        parser.print_help()

def recuperer_mots_de_passe(recuperer_wifi=False):
    liste_infos_mdp = []
    chemin_chrome = obtenir_chemin_chrome()
    
    try:
        connection = sqlite3.connect(os.path.join(chemin_chrome, "Login Data"))
        
        with connection:
            cursor = connection.cursor()
            requete = 'SELECT action_url, username_value, password_value FROM logins'
            cursor.execute(requete)
            lignes = cursor.fetchall()

        if (os.name == "posix") and (sys.platform == "darwin"):
            print("Mac OSX n'est pas pris en charge.")
            sys.exit(0)

        for origin_url, username, password in lignes:
            if os.name == 'nt':
                password = win32crypt.CryptUnprotectData(
                    password, None, None, None, 0)[1]
            
            if password:
                liste_infos_mdp.append({
                    'url_origine': origin_url,
                    'nom_utilisateur': username,
                    'mot_de_passe': str(password)
                })

        if recuperer_wifi:
            wifi_passwords = recuperer_mots_de_passe_wifi()
            liste_infos_mdp.extend(wifi_passwords)

    except sqlite3.OperationalError as e:
        e = str(e)
        if (e == 'database is locked'):
            print('[!] Assurez-vous que Google Chrome ne fonctionne pas en arrière-plan')
        elif (e == 'no such table: logins'):
            print('[!] Problème avec le nom de la base de données')
        elif (e == 'unable to open database file'):
            print('[!] Problème avec le chemin de la base de données')
        else:
            print(e)
        sys.exit(0)

    return liste_infos_mdp

def recuperer_mots_de_passe_wifi():
    wifi_passwords = []
    if os.name == "nt":
        try:
            import subprocess
            result = subprocess.check_output(
                ['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
            profiles = [line.split(":")[1].strip() for line in result if "All User Profile" in line]
            
            for profile in profiles:
                wifi_info = {}
                try:
                    profile_info = subprocess.check_output(
                        ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear']).decode('utf-8').split('\n')
                    
                    for line in profile_info:
                        if "SSID name" in line:
                            wifi_info["SSID"] = line.split(":")[1].strip()
                        elif "Key Content" in line:
                            wifi_info["Mot de passe"] = line.split(":")[1].strip()
                    
                    wifi_passwords.append(wifi_info)
                
                except subprocess.CalledProcessError:
                    pass
        
        except ImportError:
            pass

    return wifi_passwords

def obtenir_chemin_chrome():
    if os.name == "nt":
        # Chemin sous Windows
        chemin_chrome = os.getenv('localappdata') + \
            '\\Google\\Chrome\\User Data\\Default\\'
    elif os.name == "posix":
        chemin_chrome = os.getenv('HOME')
        if sys.platform == "darwin":
            # Chemin sous macOS
            chemin_chrome += '/Library/Application Support/Google/Chrome/Default/'
        else:
            # Chemin sous Linux
            chemin_chrome += '/.config/google-chrome/Default/'
    
    if not os.path.isdir(chemin_chrome):
        print('[!] Chrome n\'existe pas')
        sys.exit(0)

    return chemin_chrome

def enregistrer_en_csv(infos):
    try:
        with open('chromepass-mots-de-passe.csv', 'w', newline='') as fichier_csv:
            csv_writer = csv.writer(fichier_csv)
            csv_writer.writerow(['url_origine', 'nom_utilisateur', 'mot_de_passe'])
            for data in infos:
                csv_writer.writerow([data['url_origine'], data['nom_utilisateur'], data['mot_de_passe']])
        print("Données enregistrées dans chromepass-mots-de-passe.csv")
    except EnvironmentError:
        print('EnvironmentError : impossible d\'écrire les données')

def enregistrer_en_json(infos):
    try:
        with open('chromepass-mots-de-passe.json', 'w') as fichier_json:
            json.dump({'elements_mdp': infos}, fichier_json)
            print("Données enregistrées dans chromepass-mots-de-passe.json")
    except EnvironmentError:
        print('EnvironmentError : impossible d\'écrire les données')

if __name__ == '__main__':
    parse_arguments()
