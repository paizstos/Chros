# Chros

Chros est un programme Python qui permet de récupérer les mots de passe enregistrés dans le navigateur Google Chrome. Il offre la possibilité d'exporter ces mots de passe au format CSV ou JSON, ainsi que de les afficher dans la console. Je déclare que je n'ai aucune responsabilité sur les conséquences de votre utilisation de Chros. Ne soyez pas malveillants!

## Fonctionnalités

- Récupération des mots de passe enregistrés dans Google Chrome.
- Récupération des mots de passe WiFi (sous Windows).
- Exportation des mots de passe au format CSV ou JSON.
- Affichage des mots de passe dans la console.

## Prérequis

- Python 3.x
- Système d'exploitation Windows, macOS ou Linux

## Installation

1. Clonez ce dépôt :

   ```sh
   $ git clone https://github.com/paizstos/Chros.git
   ```
2. Accédez au répertoire du projet :

   ```sh
   $ cd Chros
   ```
3. Exécutez le script en utilisant Python :

   ```sh
   $ python chros.py [options]
   ```

## Utilisation
   ```bash
   $ python chros.py -o [csv|json]       # Exporte les mots de passe Chrome au format CSV ou JSON
   $ python chros.py -d                  # Affiche les mots de passe Chrome dans la console
   $ python chros.py -w                  # Récupère les mots de passe WiFi (sous Windows)
   ```
## Options
-o, --output: Spécifie le format de sortie des mots de passe (CSV ou JSON).
-d, --dump: Affiche les mots de passe dans la console.
-w, --wifi: Récupère les mots de passe WiFi (sous Windows).

## Contributions
Les contributions sont les bienvenues ! Si vous souhaitez améliorer ou ajouter des fonctionnalités à Chros, veuillez soumettre une demande d'extraction (pull request).

## Licence
Ce projet est sous licence GNU. Veuillez consulter le fichier LICENSE pour plus de détails.

Auteur : Christos DIONG AKETI PAIZANOS
Email : paizstos11012001@gmail.com
