Title: Créer un blog avec Pelican
Date: 2019-10-09
Author: Rached MEJRI
Tags: python, tuto
Slug: creer-blog-pelican
Summary: Python everywhere.

<div class="tenor-gif-embed" data-postid="11821610" data-share-method="host" data-width="100%" data-aspect-ratio="1.8721804511278197"><a href="https://tenor.com/view/the-wind-rises-writing-windy-gif-11821610">The Wind Rises Writing GIF</a> from <a href="https://tenor.com/search/thewindrises-gifs">Thewindrises GIFs</a></div><script type="text/javascript" async src="https://tenor.com/embed.js"></script>

# Pelican ?

Pelican est un générateur de site statique écrit en langage Python.
En bref, vous écrivez le contenu de votre blog en format Markdown ou RST article avec un petit de Python pour paramétrer le tout et le tour est joué.

Pas besoin de PHP (beurk), de base de données ou autre qui accompagne une logique serveur compliqué et difficile pour un blog qui sera sûrement lu que par votre oncle beauf aux blagues de mauvais goût.

# Installer Pelican

Me concernant, je suis sur Linux et plus précisement sur Fedora. Etant donné que j'ai une flemme intersidéral, je n'ai certainement pas envie de me pencher sur tous les cas de figures pour installer Pelican sur chaque OS mais sachez que la procédure est relativement la même à quelques exceptions près pour tout le monde.

On installe Python 3 via :

```sh
sudo dnf install python3
```

Sur Debian et ses dérivées remplacez dnf par apt.
Sur Mac et Windows, mh, débrouillez-vous :)

On installe Pelican et le support pour gérer le format Markdown via pip :

```sh
sudo pip3 install pelican markdown
```

C'est la même commande pour Windows et Mac, enfin je crois.<br/>
Et voilà, on est maintenant paré pour créer notre blog avec Pelican.

# Créer une instance de blog

J'espère que les web-designer vegan et les comptables aux gouts vestimentaires immondes n'auront pas trop galérés à installer Pelican. <br/><br/>

Après avoir installé le tout, on va pouvoir créer une instance de son blog via la commande :

```sh
pelican-quickstart
```

Cette commande va vous poser un tas de questions afin de configurer un minimum votre projet, dans la langue de Shakespeare, évidemment.

<img src="https://srv-file2.gofile.io/download/nT6GVb/Capture%20d%E2%80%99%C3%A9cran%20du%202019-10-09%2014-06-22.png" />

Après ça vous allez retrouver un dossier "output" et un dossier "content", c'est le dossier "content" qui va nous permettre d'éditer ces pages au format markdown. Le job de Pelican sera alors de compiler vos fichiers markdown au format HTML dans le dossier output. C'est aussi simple que ça.

Voici l'allure que devrait avoir le dossier ou se trouve votre projet :

```
.
├── content
├── Makefile
├── output
├── pelicanconf.py
├── publishconf.py
└── tasks.py

2 directories, 4 files
```

*A suivre*