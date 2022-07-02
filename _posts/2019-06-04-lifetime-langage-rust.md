---
layout: post
title: "Le concept de lifetimes du langage Rust"
subtitle: "Et tout ça sans laisser de miettes."
cover-img: /assets/img/time.jpg
thumbnail-img: /assets/img/time.jpg
share-img: /assets/img/time.jpg
tags: [rust, programmation]
---

D'après <a href="https://fr.wikipedia.org/wiki/Rust_(langage)">Wikipédia</a> pour ceux qui ne connaissent pas le langage : "Rust est un langage de programmation compilé multi-paradigme conçu et développé par Mozilla Research. Il a été conçu pour être « un langage sécurisé, concurrent, pratique » supportant les styles de programmation purement fonctionnel, modèle d'acteur, procédural, ainsi qu'orienté objet sous certains aspects.

# Les engagements de Rust

Comme vu précédemment, Rust se veux sécurisé, concurrent et pratique. Sécurisé en insistant sur des mécanismes que le programmeur doit impérativement appliquer, concurrent car il pousse à limiter les erreurs courantes de conceptions lors de l'écriture de programme concurrents et pratique de part son abstraction avec le moindre impact sur les performances, et ça, c'est plutôt cool.

# Prérequis

Dans ce billet je vais tenter de vulgariser le concept de lifetime, qui découle d'autres concepts tel que l'ownership de prime à bord, suivi de près par le borrowing. Le livre (book) de Rust explique avec précisions ses deux notions. Je vous laisse donc le soin d'aller vous documenter seul parce que je suis un flemmard hors-pair.

# Les lifetimes (les durées de vies en tant que bon français nationaliste)

Nous voilà au cœur du sujet. Qu'est-ce qu'une durée de vie en Rust ? Afin de répondre à cette question on va faire des conneries avec notre clavier afin de définir le concept plus facilement.

Imaginons que je souhaite créer une fonction qui pourra prendre en paramètre une référence de "vecteur" ('''std::vec::Vec''') et retourner une référence de son premier élément.

On ferait comme ça :

```rust
/*
* NB: Ce code ne compilera pas !
*/

fn main() {
  let elements: Vec<&str> = vec!["pierre", "paul", "jack"];
  let first_element = get_first_element(&elements);
}

fn get_first_element(x: &Vec<&str>) -> &str {
  &x[0]
}
```

Après une tentative de compilation qui a échouée et en gage de reconnaissance, notre bien aimé compilateur renvoie ceci :

```
error[E0106]: missing lifetime specifier
 --> main.rs:1:40
  |
1 | fn get_first_element(x: &Vec<&str>) -> &str {
  |                                        ^ expected lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does not say which one of `x`'s 2 lifetimes it is borrowed from

error: aborting due to previous error

For more information about this error, try `rustc --explain E0106`.
```

Lorsque cette erreur est mentionnée, vous allez devoir mettre explicitement des lifetime dans votre code.

En Rust vous devez penser scope car il n'y à pas de système de ramasse miettes comme en Python pour dé-allouer (vider la mémoire qu'occupe un objet quelconque dans votre programme). Plutôt qu'utiliser un système de ramasse miettes, Rust va désallouer les objets assignés à chaque fin de scopes. Il s'agit du concept d'ownership. Rapidement,la notion ressemble à ça :

```rust
fn main() {
    { // Scope A
        // Nous sommes entre duex accolades,
        // il s'agit donc d'un scope
        let a = 3;
        let b = 4;
    } // a et b ont été détruites car ici se situe la fin du scope A

    // Le Scope B, il s'agit du scope principal de la fonction main

    // Ici, le compilateur lévera une erreur dû au fait que a et b n'existent plus //// et sont donc indisponibles dans le scope B.
    let somme = a + b;
}
```

Comprenez qu'avec l'exemple de tout à l'heure qui utilisait la fonction `get_first_element` avait la même problématique que le code ci-contre.

La fonction `get_first_element` représentait un scope qui pouvait renvoyer une référence.

La problématique de tout à l'heure avec notre fonction `get_first_element` est donc la suivante : La réference retournée par la fonction `get_first_element` ne vit pas assez longtemps, elle a été "tué" lors de la fin du scope de la fonction `get_first_element`.

Parfois le compilateur n'est pas assez intelligent pour déduire le fait qu'on souhaite utiliser la référence de retour d'une fonction dans un autre scope, il va donc falloir préciser qu'on souhaite faire vivre plus longtemps la référence de retour via des tags qui représentent la durée de vie d'une référence.

Les lifetimes ou les durées de vies sont donc grosomodo des lettres (tags) que vous allez devoir ajouter à votre code afin d'exprimer ceci : "Je vais te passer une valeur, mais je veux que la référence de cette valeur à la fin du scope survive et que je puisse l'éxploiter sur un autre scope".

Si nous reprenons l'exemple de tout à l'heure mais cette fois en utilisant les tags de lifetimes :

```rust
fn main() {
  let elements: Vec<&str> = vec!["pierre", "paul", "jack"];
  let _first_element = get_first_element(&elements);
  // OK, &x[0] survivera jusqu'à la fin de ce scope
}

fn get_first_element<'a>(x: &'a Vec<&str>) -> &'a str {
  &x[0]
}
```
