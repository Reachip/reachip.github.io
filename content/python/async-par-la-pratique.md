Title: L'asynchronisme par la pratique avec E621
Date: 2019-10-30
Author: Rached MEJRI
Tags: python, asyncio, tuto  
Slug: python-asynchronisme-par-la-pratique
Summary: Ou la zoophilie au service de l'apprentissage ...

<div class="tenor-gif-embed" data-postid="4903957" data-share-method="host" data-width="100%" data-aspect-ratio="0.7550200803212851"><a href="https://tenor.com/view/furry-gif-4903957">Furry GIF</a> from <a href="https://tenor.com/search/furry-gifs">Furry GIFs</a></div><script type="text/javascript" async src="https://tenor.com/embed.js"></script>

Bon de base c'était un projet pour le fun mais je me suis dis que ça pourrait être pas mal de faire un mini-tutoriel dessus.

Bonsoir peuple de France et de Navarre. Ce soir on va pratiquer l'asynchronisme en langage Python. J'avais déjà écrit une page dessus que vous pouvez retrouver <a href="https://reachip.github.io/lasynchronisme-avec-python.html">en cliquant ici</a>.

C'était un pavé de théorie avec un petit exemple à la fin avec quelques sous-entendus grosophobe donc j'ai décidé d'écrire cette présente page pour expliquer le concept avec d'avantage de pratique pour le plus grand plaisir des gens avec un soupçon de déviance zoophile.


# Déjà qu'est ce que E621

E621 est un site de partage d'images, qualifiées parfois d'oeuvres basées le thème du furry. Pour faire simple c'est de la pornographie zoophile masqué par des images aux allures de dessins animés. Je remercie un certain **ǤŦҠ#2548** pour m'avoir fait découvert cette atrocité.

![](https://image.noelshack.com/fichiers/2019/44/3/1572460473-screenshot-2019-10-30-e621.png)

C'est bien ce que je disais.

# Objectif

Après vous avoir fait découvrir le dark net des oursons en peluches place au sujet central : On veut pouvoir télécharger toutes les images d'une des catgéories de E621 pour les stocker et je ne sais trop quoi en faire après. Après tout ça vous regarde.

On pourrait naïvement utiliser les threads mais avec la notion de <a href="http://www.xavierdupre.fr/app/teachpyx/helpsphinx/notebooks/gil_example.html">GIL</a> ça va s'avérer être de la bricole et en vu des opérations très orientées <a href="https://fr.wikipedia.org/wiki/Entr%C3%A9es-sorties">*I/O*</a>, se pencher vers un code asynchrone pourrait être une meilleure solution.

# Plan d'attaque

<div class="tenor-gif-embed" data-postid="5622846" data-share-method="host" data-width="100%" data-aspect-ratio="1.496"><a href="https://tenor.com/view/fail-gun-gif-5622846">Fail Gun GIF</a> from <a href="https://tenor.com/search/fail-gifs">Fail GIFs</a></div><script type="text/javascript" async src="https://tenor.com/embed.js"></script>

Pour se faire, on va implémenter les fonctions suivantes : ```get_html_source```, ```get_image```, ```make_image_path```, ```write_image```, ```get_image_from_categorie```, ```fetch_images_urls``` et ```main```.

Toutes les fonctions que nous allons implémenter seront des coroutines (donc de type asynchrone) exceptées ```fetch_images_urls``` et ```make_image_path```. Elles sont donc qualifiées comme fonctions bloquantes.

## Pourquoi executer du code bloquant alors qu'on veut du code qui ne bloque jamais quand on veut du code asynchrone ?

Les fonctions bloquantes sont des fonctions qui font appeles à des opérations non-asynchrone et qui donc font des opérations liées au CPU bound et non à *l'I/O*. Elles sont nécessaires, même dans un code ou on veut une logique asynchrone. Pour les utiliser de façon non-bloquante on va donc devoir passer obligatoirement par des threads.

Il ne faut donc pas voir les threads et l'asynchronisme comme deux paradigmes opposés mais comme deux façon de faire tout à fait complémentaires.

Python nous permet de lancer un thread sur une fonction en utilisant la méthode ```run_in_executor```.

## Let's code

**NB :** Pensez à importer toutes les dépendances nécessaires au début du script :
**NB2 :** Libre à vous de créer un fichier de logs pour visualiser  les actions effectuées au fil du temps lorsque que le code adopte une logique asynchrone.

```python
import asyncio
import os
import sys
import logging
from uuid import uuid4

# A installer via pip

# Pour travailler avec le protocole HTTP
import aiohttp

# Pour travailler avec les fichiers,
# il s'agit d'un wrapper de open() en version async
import aiofiles

# Pour parser de l'HTML
import bs4

logging.basicConfig(
    filename="log", format="%(threadName)s %(asctime)s %(message)s", level=logging.DEBUG
)
```

Dans un premier temps on va implémenter la fonction ```get_html_source``` qui comme son nom l'indique nous permet de récupérer le contenu html d'une des pages du site en fonction de l'index (numéro de page grosomodo) et de la catégorie choisi par notre utilisateur zoophile.

```python
async def get_html_source(categorie, index):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36"
    }

    url = f"https://e621.net/post/index/{index}/{categorie}"

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as response:
            return await response.text()
```

Puis on va se charger d'écrire la fonction ```fetch_images_urls``` chargé de parser l'HTML récupéré ```get_html_source``` et d'en retourner l'url menants aux images se trouvant sur la page cible.

```python
def fetch_images_urls(html):
    parser = bs4.BeautifulSoup(html, "lxml")
    img_pattern = {"class": "preview"}

    return [img_url["src"] for img_url in parser.find_all("img", img_pattern)]
```

Il s'agit d'une fonction qui ne fait aucun appelles d'entrée ou de sortie (*I/O*), c'est donc du calcul pur et dur et donc une fonction bloquante. On utilisera ```run_in_executor``` pour l'appeler.

Parfait. On a pour l'instant un programme qui recupère et traite l'HTML d'une page d'E621 pour en récupérer les url qui pointent vers différentes images d'une page du site.

*A suivre*
