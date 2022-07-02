---
layout: post
title: C'est quoi le duck typing ?
subtitle: Si ça ressemble à un canard, si ça nage comme un canard et si ça cancane comme un canard, c'est un canard.
cover-img: /assets/img/big-duck.png
thumbnail-img: /assets/img/big-duck.png
share-img: /assets/img/big-duck.png
tags: [conception, programmation, poo]
---
Au risque de contrarier la communauté vegan, on va encore parler de canard dans cet article.
Si vous n'avez pas vu le précédent article sur les principes SOLID, ça se passe ici : <a href="https://reachip.github.io/articles/fr/concevoir-du-code-solid.html">https://reachip.github.io/articles/fr/concevoir-du-code-solid.html</a>

# Le duck typing ?

> En programmation informatique, le duck typing (traduction : typage canard) est un style de typage dynamique de certains langages de programmation orientés objet. En duck typing, la sémantique d'un objet, c'est-à-dire son type dans le contexte où il est utilisé, est déterminée par l'ensemble de ses méthodes et de ses attributs, et non, comme il l'est habituellement, par un type défini et nommé explicitement par le programmeur dans les systèmes à typage nominatif. C'est l'équivalent du typage structurel pour les langages à typage statique, comme OCaml

Merci Wikipédia. Pour faire simple, le ducktyping vous permet de coder en passant type qui possède les caractéristiques que vous voulez lui faire faire, sans se soucier de savoir si votre donnée est de A ou B.

Si je veux itérer, que se soit un un tuple, une list ou un générateur, je m'en fiche, c'est un itérable : *Si ça ressemble à un itérable, si ça nage comme un itérable et si ça cancane comme un itérable, c'est un itérable.*

Le concept est similaire à celui des interfaces (ou trait) dans des langages à typage statique comme Java, Rust ou C#. 

Dans des langages à typage dynamique comme Python, le comportement est déjà implémenté et géré par l'interpréteur.

# Exemple

```python
class MyIterable:
  def __iter__(self):
    self.counter = 10
    return self

  def __next__(self):
    if self.counter != 0:
      self.counter -= 1
      return self.counter * 2

    else:
      raise StopIteration

def sum_iterables(iterables):
  result = ""

  for iterable in iterables:
    for el in iterable:
      result += str(el)

  return result


iterables = (
  ("1", 2, 1.2), # Un tuple avec un mélange de types : str, int et float
  ("a", "b", "c"), # Un tuple avec des chaînes de caractères
  [12, 12.3, [10, 20]], # Une liste avec une liste à l'intérieur
  MyIterable(), # Un itérable custom
)

output = sum_iterables(iterables)
print(output)

# => 121.2abc1212.3[10, 20]16231068370
```    

On s'en fiche de ce qui se trouve dans le tuple iterables, du moment qu'on peut itérer dessus.

# Duck typing et prise de décision

On peut proposer à un langage qui implémente le duck typing une valeur par défaut si on ne précise rien dans les paramètres du fonction. Par exemple : 

```python
from random import randint

class MyIterable:
  def __iter__(self):
    self.max = 10
    return self

  def __next__(self):
    if self.max != 0:
      self.max -= 1
      return randint(0, 10)

    else:
      raise StopIteration

def sum_iterables(iterables, convertor=str):
  result = ""

  for iterable in iterables:
    for el in iterable:
        result += convertor(el)

  return result


iterables = (
  ("1", 2, 1.2), # Un tuple 
  ("a", "b", "c"), # Un tuple
  [12, 12.3, [10, 20]], # Une liste avec une liste à l'intérieur
  MyIterable(), # Un itérable custom
)

output = sum_iterables(iterables, int)
output = sum_iterables(iterables, str)
output = sum_iterables(iterables)

print(output)
```

# Conclusion

L'article suivant est principalement à destination des débutants. Il est aussi à titre indicatif pour les personnes confirmés : Acceptez d'utiliser le duck-typing dans les langages qui l'acceptent, vérifier strictement vos types ne sert à rien. Une bonne doc' fait le café !