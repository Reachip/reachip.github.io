---
layout: post
title: "Passer des arguments sans les copier en langage Rust"
subtitle: "Sans copier-coller."
cover-img: /assets/img/passing.jpg
thumbnail-img: /assets/img/passing.jpg
share-img: /assets/img/passing.jpg
tags: [rust, programmation]
---

Rust répond à besoin, celui de vouloir développer des programmes performants (entre autre). Qui dit performance dit économie de mémoire vive et pour cela, Rust utilise deux concepts : Le passage par référence et la sémantique de mouvement. Respectivement, la deuxième méthode est utilisé implicitement quand l'objet passé en argument n'implémente pas le trait <a href="https://doc.rust-lang.org/std/marker/trait.Copy.html">Copy</a> qui comme son nom l'indique **permet de copier la valeur émise à la fonction cible**.

On peut en déduire que dans le cas contraire, vous devez **passer par référence la valeur que vous ne voudriez pas copier dans le but d'économiser de la mémoire.**

Voyons ça un peu plus en détail.

# Le trait Copy

Le trait Copy permet de copier une valeur émise, on le trouve <a href="https://doc.rust-lang.org/std/marker/trait.Copy.html#implementors">dans toutes les primitives du langage</a>.

Prenons un primitif : <a href="https://doc.rust-lang.org/std/primitive.usize.html">usize</a> et créeons une variable nommée *X* pour commencer.

```rust
fn main() {
    let mut x: usize = 20; // Une variable (mutable) nommée x de type usize.
}
```

J'aimerais créer une fonction ```add_one(x: usize)``` qui ajoute "1" à la variable passé en argument. J'ai bien dis la variable et non pas la valeur que contient la variable. C'est-à-dire que je veux modifier le nombre 20 qui se trouve dans X et non pas simplement faire une addition sur le nombre 20.

Pour ça, naïvement, je vais créer ma fonction sans faire un passage par référence.


```rust
fn add_one(mut y: usize) -> () {
    y += 1
}

fn main() {
    let mut x: usize = 20; // Une variable (mutable) nommée x de type usize.
    add_one(x); // Est-ce que add_one va modifier ma variable X ?
    println!("{}", x); // Non car X vaut toujours 20 lorsque qu'on debug.
}
```

Ici *x* vaut toujours 20, c'est parce que la variable *x* a été copié. Par conséquent la fonction ```add_one``` n'a pas modifié directement la variable *x* passé mais plûtot un type usize copié depuis le usize que contenait *x*.

Mais comment modifier la variable *x* via une fonction ? Je pense que vous vous en doutiez pour ceux qui auraient pratiqués les langages C/C++, il faut passer *x* "par référence".

# Le passage par référence

Le passage par référence évite la copie et permet de directement modifier un contenu mutable (une variable pour vulgariser) contenant un type.

Pour préciser qu'on va traiter une donnée par référence, on utilise ```&``` et ```*```. En pratique, ça donne ça :

```rust
fn add_one(y: &mut usize) -> () {
    *y += 1 // On "pointe" vers la valeur de Y via "*"
}

fn main() {
    let mut x: usize = 20; // Une variable (mutable) nommée x de type usize.
    add_one(&mut x); // Est-ce que add_one va modifier ma variable X ?
    println!("{}", x); // Oui car X vaut maintenant 21.
}
```

Le passage par référence (si le contexte est adapté pour ne pas copier) est donc le moyen explicite que le programmeur utilse pour ne pas copier un objet mutable ou immutable et de modifier directement la variable soumise à la fonction traitante.

Mais ce comportement, Rust permet de le faire seul si le trait Copy n'est pas implémenté chez un objet. C'est la sématique de mouvement.

# La sémantique de mouvement

Si un objet n'implémente pas le trait Copy, alors dans notre cas, Rust va automatiquement supprimé *x* pour "donner" sa valeur à la fonction qui dans laquelle on a passé *x* en argument.


<div class="tenor-gif-embed" data-postid="5306424" data-share-method="host" data-width="100%" data-aspect-ratio="1.9047619047619047"><a href="https://tenor.com/view/disparition-disparaitre-disappear-disappearance-gif-5306424">Disparition GIF</a> from <a href="https://tenor.com/search/harrypotter-gifs">Harrypotter GIFs</a></div><script type="text/javascript" async src="https://tenor.com/embed.js"></script>

Exemple :

```rust
fn add_one(mut v: y) -> () {
// Ajoute un au premier élément du vecteur.
v[0] += 1;
}

fn main() {
/* Le type Vec<usize> n'implémente pas le trait Copy donc Rust va utliser la sémantique de mouvement. */
let mut x: Vec<usize> = vec![10, 15];
add_one(x);
// Le compilateur renvoie une erreur an voulant afficher "x" car "x" a été supprimé grâce à la sémantique de mouvement, on évite de copier en déplacant.
println!("{}", x);
}
```

Parfait, Rust évite la copie automatiquement. Si vous voulez modifier directement "x" sans qu'il soit supprimé vous pouvez faire comme tout à l'heure en passant "x" à ```add_one``` par référence.

```rust
fn add_one(v: &mut Vec<usize>) -> () {
// Ajoute un au premier élément du vecteur.
v[0] += 1;
}

fn main() {
    /* Le type Vec<usize> n'implémente pas le trait Copy donc Rust va utliser la sémantique de mouvement. */
    let mut x: Vec<usize> = vec![10, 15];
    add_one(&mut x);
    println!("{}", x[0]);
    /* "x" n'a pas été supprimé et a donc été passé par référence. On peut donc constater que son premier élément ne vaut plus "10" mais "11". */
}
```
