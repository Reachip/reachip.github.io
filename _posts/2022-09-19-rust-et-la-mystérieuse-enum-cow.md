---
layout: post
title: Rust et la mystérieuse enum "Cow"
subtitle: All my life I was swinging for the fence, I was looking for the triple, Never playing good defense
cover-img: /assets/img/sebastian-knoll-vNQ57VEqceY-unsplash.jpeg
thumbnail-img: /assets/img/sebastian-knoll-vNQ57VEqceY-unsplash.jpeg
share-img: /assets/img/sebastian-knoll-vNQ57VEqceY-unsplash.jpeg
tags: [rust, programmation]
---

Il arrive parfois que l’on veuille faire une opération couteuse que si cela est nécessaire. Rien ne vaut que quelques conditions triviales pour arriver cela, mais lorsque que l’on touche à des opérations évaluées au runtime, nous devons nous armer d’outils efficaces.

On pense notamment aux pointeurs intelligents quand il s’agit de modifier le comportement au runtime des mécanismes de gestion de la mémoire.

Nous verrons un type de pointeur intelligent “clone-on-write” que propose Rust dans sa librairie standard appelé `Cow`. Un nom bien abstrait pour décrire un usage bien pratique des pointeurs intelligents dans la plupart des langages qui en possèdent.

Avant de voir cela, un petit rappel sur l’ownership s’impose.

# Petit rappel concernant l'ownership

Si Rust est aussi intéressant, c'est grâce à son abstraction sans cout. La plupart des langages haut-niveau utilisent le garbage collector afin de s'occuper de la gestion la mémoire au runtime à la place du programmeur. Sujet à des baisses de performances et de contraintes techniques, Rust quant à lui utilisent l'ownership dans le but de gérer ladite mémoire.

Concrètement, en Rust, une valeur doit avoir un seul et unique propriétaire. Elle peut être empruntée au cours de l'exécution, mais jamais possédé par plus d'une entité.

```rust
fn main() {
    let brown = String::from("- Où est Brown ? - Il est mort. - Le con !");
    let orange = brown; // orange devient propriétaire de brown

    println!("{:?}", brown);

    // brown est appellé, alors que c'est orange qui possède la valeur de brown.
    // Rust a déjà libèré brown et nous signale donc au compile-time
    // que le principe d'ownership n'est pas respecté ...
}
```

```rust
/* Traceback :
error[E0382]: borrow of moved value: `brown`
--> src/main.rs:18:22
|
15 | let brown = String::from("- Où est Brown ? - Il est mort. - Le con !");
| ----- move occurs because `brown` has type `String`, which does not implement the `Copy` trait
16 | let orange = brown;
| ----- value moved here
17 |
18 | println!("{:?}", brown);
| ^^^^^ value borrowed here after move
*/
```

Maintenant, on sait que c'est l'ownership qui a tué M.Brown dans Reservoir Dog.

Aussi, avec Rust, tout est une question de scope. Lorsque qu'un scope se termine, les valeurs à l'intérieur sont libérées.

```rust
fn main() {
    let a = String::from("zero");

    {
        let z = String::from("zero");

        if a == z {
            println!("It's true");
        } else {
            println!("It's false");
        }
    } // z est libéré

    println!("{:?}", z); // ne compile pas
}
```

# Le trait Copy à la rescousse

L'ownership n'est parfois ni pratique, ni facile à prendre en main lorsque que l'on est dans la phase de conception.

Il s'agit de passer des références aux fonctions et aux structures notamment afin d'assurer le respect du principe. Cela n'est pas sans complexité quand le code grossi, voir impossible quand on veut étendre la taille d'une variable, spécifiquement quand nous travaillons avec des tableaux.

Pour pallier cela, Rust propose le trait Copy qui permet la copie d'une valeur lorsque qu'au compile-time, on détecte une entité qui veut devenir nouveau propriétaire.

La plupart des types de base du langage comme `String`, `i32` ou `usize` implémentent le trait Copy, et temps mieux ! On peut aussi facilement l'implémenter sur nos propres structures.

# Copy ou pas Copy ?

Est-ce performant d'utiliser `Copy` implicitement à chaque fois que nous souhaitons passer une valeur à une fonction par exemple ?

Non seulement [l'explicite est préférable à l'implicite](https://peps.python.org/pep-0020/#the-zen-of-python), mais en plus, la copie peut être très couteux si notre valeur est relativement imposante.

La solution serait de copier seulement si cela est nécessaire.

# Cow à la rescousse

Il s'agit donc d'utiliser `Cow` afin de détecter au runtime qu'une copie est nécessaire.
Imaginons que nous avons une fonction qui modifie un tableau passé par référence, seulement le nombre `200` est détecté.

```rust
use std::borrow::Cow;

use rand::Rng;

fn big_vec_with_given_capacity(capacity: i64) -> Vec<i64> {
    let mut rng = rand::thread_rng();
    let mut big_vec: Vec<i64> = Vec::with_capacity(capacity as usize);

    for _ in 0..capacity {
        big_vec.push(rng.gen::<i64>());
    }

    big_vec
}

fn modify_vec_if_find(value: i64, vec: &mut Cow<[i64]>) {
    for iterator in 0..vec.len() {
        let input = vec[iterator];

        if input == value {
            // On modifie le vecteur, donc à ce moment là, on copie
            println!("Do a copy of {:?}", &vec as *const _);
            vec.to_mut()[iterator] = 0;
        }

        // Si à la fin de la fonction on ne rentre pas dans la condition, on ne copie pas.
    }
}

fn main() {
    {
        // On effectue pas de copie, 200 n'est pas présent dans le vecteur
        let mut big_vec_without_cow = big_vec_with_given_capacity(90000);
        big_vec_without_cow.retain(|&value| value != 200);

        let mut big_vec = Cow::from(big_vec_without_cow);
        modify_vec_if_find(200, &mut big_vec);
    }

    {
        // On effectue une copie, 200 est bien présent
        let mut big_vec_without_cow = big_vec_with_given_capacity(90000);
        big_vec_without_cow.push(200);

        let mut big_vec = Cow::from(big_vec_without_cow);
        modify_vec_if_find(200, &mut big_vec);
    }
}
```

Grâce au pointeur `Cow`, on permet au langage de réagir de manière perraine au cas par cas au lieu de reagir de manière disproportionné, peut importe les valeurs qu'on possède.
