# Introduction

Librairie Python permettant la communication avec le i-Parapheur en version 4.2+, au travers de l'API REST ou via webservice SOAP.

# Installation

Sur une distribution Ubuntu 14.04 LTS :

* une instance i-Parapheur accessible en v4.2.07 ou plus
* un environnement Python fonctionnel!
* ajout de 'easy_install', puis 'pip' :

```bash
sudo apt-get install python-setuptools
sudo easy_install pip
```

* installation du paquet python `iparapheur-utils` :

```bash
sudo easy_install iparapheur-utils
```

Support CentOS / RHEL :

* Version 6 : Cette version n'est plus supportée, en cause une version de python trop ancienne (2.6)
* Version 7 : Cette version requiert l'installation de paquets supplémentaires : `yum install libffi-devel gcc openssl-devel`

# Usage

Ces commandes sont actuellement disponibles :

- [`ph-init`](#ph-init)
- [`ph-check`](#ph-check)
- [`ph-echo`](#ph-echo)
- [`ph-recupArchives`](#ph-recuparchives)
- [`ph-export`](#ph-export)
- [`ph-import`](#ph-import)

## `ph-init`

Cette commande permet la génération d'un fichier de configuration "par défaut", qu'il faut bien sûr adapter au serveur.

Exemple d'utilisation :
```bash
usage: ph-init [-h] [-p P] [-c {recuparchives,export,import}]

Génère un fichier de configuration par défaut dans le répertoire courant

Arguments:
  -h, --help            Affiche ce message et quitte
  -p P                  Chemin du fichier de configuration
  -c {recuparchives,export,import}
                        Commande pour laquelle générer le fichier de
                        configuration
```

Le lancement de la commande génère un fichier `iparapheur-utils.cfg`, lu par défaut lors de l'appel des autres fonctions

## `ph-check`

Lance le script de check d'installation. Pas de pré-requis particulier.

## `ph-echo`

Lance la fonction `echo` vers le i-Parapheur désigné dans le fichier de configuration.

Exemple d'utilisation :
```bash
ph-echo -h
---
usage: ph-echo [-h] [-s S] [-c C] [-u U] [-p P]

Lance un echo via webservice sur un iParapheur

Arguments:
  -h, --help  Affiche ce message et quitte
  -s S        URL du serveur iParapheur
  -c C        Fichier de configuration
  -u U        Utilisateur
  -p P        Mot de passe
```

## `ph-recupArchives`

Lance la fonction de récupération ou/et de purge des archives.
Il est vivement conseillé d'utiliser la commande `ph-init -c recuparchives` afin de générer un squelette de fichier de configuration complet.

Exemple d'utilisation :
```bash
ph-recupArchives -h
---
usage: ph-recupArchives [-h] [-s S] [-c C] [-u U] [-p P] [-f F] [-ps PS]
                        [-r {true,false}] [-pu {true,false}] [-d {true,false}]
                        [-t T] [-st ST] [-w W]

Lance une récupération / purge des archives

Arguments:
  -h, --help        Affiche ce message et quitte
  -s S              URL du serveur iParapheur
  -c C              Fichier de configuration
  -u U              Utilisateur
  -p P              Mot de passe
  -f F              Répertoire de destination
  -ps PS            Taille des pages à récupérer
  -r {true,false}   Chemins réduis des téléchargements
  -pu {true,false}  Active la purge les données
  -d {true,false}   Télécharge les données
  -t T              Filtre sur type
  -st ST            Filtre sur sous-type
  -w W              Délai de conservation des données
```

## `ph-export`

Lance la fonction d'exporation de la configuration du parapheur vers un dossier.
Il est vivement conseillé d'utiliser la commande `ph-init -c export` afin de générer un squelette de fichier de configuration complet.

**ATTENTION** : Seule la **configuration** du parapheur est exportée. Comprendre qu'aucun dossier, archive, statistique ou historique n'est conservé.

Exemple d'utilisation :
```bash
usage: ph-export [-h] [-s S] [-c C] [-u U] [-p P] [-i I] [-dh DH] [-dp DP]
                 [-du DU] [-dpw DPW] [-dd DD]

Exporte la configuration du parapheur ciblé vers un dossier

Arguments:
  -h, --help  Affiche ce message et quitte
  -s S        URL du serveur iParapheur
  -c C        Fichier de configuration
  -u U        Utilisateur administrateur
  -p P        Mot de passe
  -i I        Répertoire de destination
  -dh DH      IP du serveur mysql
  -dp DP      Port du serveur mysql
  -du DU      Utilisateur alfresco de mysql
  -dpw DPW    Mot de passe utilisateur alfresco de mysql
  -dd DD      Nom de la base mysql
```

## `ph-import`

Lance la fonction d'importation de la configuration du parapheur à partir d'un dossier.
Il est vivement conseillé d'utiliser la commande `ph-init -c import` afin de générer un squelette de fichier de configuration complet.

**ATTENTION** : Seule la **configuration** du parapheur est importée. Comprendre qu'aucun dossier, archive, statistique ou historique n'est conservé.

Exemple d'utilisation :
```bash
usage: ph-import [-h] [-s S] [-c C] [-u U] [-p P] [-i I] [-dh DH] [-dp DP]
                 [-du DU] [-dpw DPW] [-dd DD]

Importe la configuration ciblée dans un parapheur vierge

Arguments:
  -h, --help  Affiche ce message et quitte
  -s S        URL du serveur iParapheur
  -c C        Fichier de configuration
  -u U        Utilisateur administrateur
  -p P        Mot de passe
  -i I        Répertoire à importer
  -dh DH      IP du serveur mysql
  -dp DP      Port du serveur mysql
  -du DU      Utilisateur alfresco de mysql
  -dpw DPW    Mot de passe utilisateur alfresco de mysql
  -dd DD      Nom de la base mysql
```

# Utilisation en librairie

Définir un fichier de configuration `script.cfg` dans le répertoire racine via la commande `ph-init`, qui aura la forme suivante :

```ini
[Parapheur]
username = admin
password = admin
server = secure-iparapheur.dom.local
```

Puis, créer un script python avec utilisation de l'API REST :

```python
#!/usr/bin/env python
# coding=utf-8

import parapheur

# Init REST API client
client = parapheur.getrestclient()

if client.islogged:
    # Do a lot of things...
```

Ou, pour une utilisation avec l'API SOAP :

```python
#!/usr/bin/env python
# coding=utf-8

import parapheur

# Init SOAP API client
webservice = parapheur.getsoapclient()

webservice.call().echo('Coucou, ici python !')
```

Le rendre éxecutable, puis le lancer depuis une console bash :

```bash
chmod +x ./script.py
./script.py
```

# Cas spécifiques

## Proxy

Il est possible de contourner l'usage d'un proxy pour les appels Webservices ou API REST, 
si le script à lancer doit communiquer directement avec le serveur i-Parapheur 
sans passer par un éventuel proxy défini sur le système.

Pour cela, il suffit d'ajouter la variable **NO_PROXY** avant l'appel d'une fonction ou d'un script.
Par exemple, pour un appel de `ph-echo` vers `secure-iparapheur.dom.local`, la commande sera :

```bash
NO_PROXY="secure-iparapheur.dom.local" ph-echo
```
