---
layout: post
title: Concevoir du code SOLID
subtitle: Concevoir du code SOLID, sans mauvais jeux de mots.
cover-img: /assets/img/wall.jpg
thumbnail-img: /assets/img/wall.jpg
share-img: /assets/img/wall.jpg
tags: [conception, programmation, poo]
---

Aujourd'hui, j'ai décidé d'écrire un article sur ce que sont les principes dit "SOLID", comment et quand les appliquer dans vos projets.

Tout d'abord, et toujours d'après ce chère Wikipédia :

>En programmation orientée objet, SOLID est un acronyme mnémonique qui regroupe cinq principes de conception destinés à produire des architectures logicielles plus compréhensibles, flexibles et maintenables. Les principes sont un sous-ensemble de nombreux principes promus par l'ingénieur logiciel et instructeur américain Robert C. Martin.

>Bien qu'ils s'appliquent à toute conception orientée objet, les principes SOLID peuvent également former une philosophie de base pour des méthodologies telles que le développement agile ou le développement de logiciels adaptatifs. 

Maintenant qu'on sait ça, place à la pratique. J'écris actuellement ces lignes avec tritesse, car je n'utiliserais pas le langage Python pour illustrer mes propos, mais le langage C# qui proposent une meilleure intégration des concepts d'interfaces, de classes abstraites et de polymorphisme. Nous aurions pu le faire en Python, mais cela aurait risqué d'être plus trivial à implémenter.

# S comme principe de responsabilité unique

Ce principe est surement l'un des plus simples à comprendre. **Arrêtez les classes foures-tout !**
Une classe doit avoir une seule et unique responsabilité, une seule et unique tâche.

Si vous avez une classe qui représente une forme géométrique, une fausse bonne idée serait de lui passer des méthodes qui réalisent les calculs d'air ou de périmètre liées à cette classe. On se retrouve donc avec une classe qui doit à la fois créer nos formes et réaliser les calculs par rapports aux propriétés. Cela n'est pas modulable et viole les prochains principes que nous allons voir.

```csharp
abstract class Rectangle
{
    public double Length { get; protected set; }
    public double Width { get; protected set; }

    public Rectangle(double length, double width)
    {
        Length = length;
        Width = width;
    }

    public double Air()
    {
        return Length * Width;
    }
}
```

Nous allons donc mettre toutes nos méthodes de calcul dans une classe dédié à cette tâche.

```csharp
abstract class Rectangle
{
    public double Length { get; protected set; }
    public double Width { get; protected set; }

    public Rectangle(double length, double width)
    {
        Length = length;
        Width = width;
    }

}

class ComputeRectangle
{
    public Rectangle Rectangle { get; private set; }

    public ComputeRectangle(Rectangle rectangle)
    {
        Rectangle = rectangle;
    }

    public double Air()
    {
        return Rectangle.Length * Rectangle.Width;
    }
}
```

C'est bien, mais on peut faire beaucoup mieux. Admettons que je veuille faire la même chose pour d'autres figures géométriques. Comment je ferais ?

# O comme principe Ouvert/fermé (Open/closed principle)

Toujours d'après Wikipédia : Une entité applicative (class, fonction, module ...) doit être fermée à la modification directe mais ouverte à l'extension.

Concrètement, même si je veux calculer l'air de mon triangle, je n'aurais pas le droit de modifier ma classe ComputeRectangle pour faire en sorte qu'elle puisse aussi calculer l'air de mon triangle. Souvenez-vous, cela violera le principe vu précédemment et modifier le code d'une classe amenerait à pas mal de régressions dans certains cas. Il faudrait avoir une entité distinct pour les calculs du rectangle et du triangle.

## Quelle solution ?

Une interface. Avec elle, on pourra avoir différentes classes qui font nos calcules géométriques qui auront à la fois une seule et même responsabilité dans lesquelles on va pouvoir seulement modifier le corps des méthodes, sans en rajouter à chaque nouvelles figures géométriques ajoutés au programme.

Ce qui nous donne :

```csharp
interface IComputeGeometricForm
{
    public double Area();
}


class Rectangle
{
    public double Length { get; protected set; }
    public double Width { get; protected set; }

    public Rectangle(double length, double width)
    {
        Length = length;
        Width = width;
    }

}

class Triangle
{
    public double Base { get; protected set; }
    public double Width { get; protected set; }

    public Triangle(double base_, double width)
    {
        Base = base_;
        Width = width;
    }
}


class ComputeRectangle : IComputeGeometricForm
{
    public Rectangle Rectangle { get; private set; }

    public ComputeRectangle(Rectangle rectangle)
    {
        Rectangle = rectangle;
    }

    public double Area()
    {
        return Rectangle.Length * Rectangle.Width;
    }
}

class ComputeTriangle : IComputeGeometricForm
{
    public Triangle Triangle { get; private set; }

    public ComputeTriangle(Triangle triangle)
    {
        Triangle = triangle;
    }

    public double Area()
    {
        return Triangle.Base * Triangle.Width / 2;
    }
}
```

Et là, on vient de violer un autre principe : l'Inversion des dépendances.

# L comme principe de substitution de Liskov

Dans notre exemple, les classes qui implémentent ```IComputeGeometricForm``` requièrent dans leurs constructeurs une forme géométrique bien spécifique.

On peut constater qu'on limite le couplage en injectant les dépendances directement dans les classes chargées des calcul, mais cela ne suffit pas.

## Le test du canard

> "If it look like a duck, quaks like a duck, but needs batteries - You probably have the wrong abstraction"

Cette assertion est asser représentative du problème posé. Si vous demandez de faire des calculs sur un triangle, il s'agit d'une forme géométrique qui a des caractéristiques communes avec le rectangle, le carré, le cercle et j'en passe. Comme c'est une forme géometrique, elle doit posséder les mêmes caractéristiques que les autres et les mêmes propriétés n'est ce pas ?

## Quelle solution ?

Il s'agit donc dans notre code de dire : "Je vais te passer une forme géométrique que tu va pouvoir utiliser comme toutes les autres et tu n'auras aucune suprise, promis".

Petite ouverture concernant la programmation par contrat : <a href="https://fr.wikipedia.org/wiki/Programmation_par_contrat">https://fr.wikipedia.org/wiki/Programmation_par_contrat</a>

Pour cela, on pourrait créer une classe abstraite Form qui contient l'ensemble des propriétés du forme géometrique et d'explicitement demander dans les classes qui calculent un objet de type ```Form```.


```csharp
abstract class Form
{
    public double Length { get; protected set; }
    public double Width { get; protected set; }
    public double Base { get; protected set; }

    public Form(double lenght, double width, double base_)
    {
        Length = lenght;
        Width = width;
        Base = base_;
    }
}

class Rectangle : Form
{
    public Rectangle(double length, double width) : base(length, width, 0) {}
}

class Triangle : Form
{
    public Triangle(double base_, double width) : base(0, width, base_) {}
}

class ComputeRectangle : IComputeGeometricForm
{
    public Form Rectangle { get; private set; }

    public ComputeRectangle(Form rectangle)
    {
        Rectangle = rectangle;
    }

    public double Area()
    {
        return Rectangle.Length * Rectangle.Width;
    }
}

class ComputeTriangle : IComputeGeometricForm
{
    public Form Triangle { get; private set; }

    public ComputeTriangle(Form triangle)
    {
        Triangle = triangle;
    }

    public double Area()
    {
        return Triangle.Base * Triangle.Width / 2;
    }
}
```

# I comme principe de ségrégation des interfaces

C'est surement le principe le plus facile à comprendre.

> Il faut diviser les interfaces volumineuses en plus petites plus spécifiques, de sorte que les clients 
> n'ont accès qu'aux méthodes intéressantes pour eux.

Limiter vous à quelques méthodes tout en gardant en tête que les méthodes classe qui hérite d'une interface doivent toujours avec un but. Si elles doivent ne contenir aucun corps ou lancer une exception dès son appel, vous avez sûrement violé ce principe.

# D comme principe d'inversion des dépendances

> Les modules de haut-niveau ne doivent pas dépendre des modules de bas-niveau. Les deux doivent dépendre 
> d’abstraction.

Il s'agit de ce qu'on vient de voir tout à l'heure avec Liskov, mais sous un autre angle : Rien ne doit dépendre de qui que ce soit.

Nos propriétés de calculs doivent se faire injecter une dépendance si besoin, dans le constructeur, ou dans des méthodes et doivent réclamer une interface ou une abstraction. C'est un ensemble des trois principes vues précédemment afin d'avoir une couche d'abstraction supplémentaire et de limiter la casse quant aux violations de principe de responsabilité unique et du principe ouvert/fermé.

# Est-ce que je dois suivre tous ces principes à la lettre ?

<div class="tenor-gif-embed" data-postid="3440314" data-share-method="host" data-width="100%" data-aspect-ratio="1.358695652173913"><a href="https://tenor.com/view/care-bears-train-rainbow-gif-3440314">Calinours GIF</a> from <a href="https://tenor.com/search/carebears-gifs">Carebears GIFs</a></div><script type="text/javascript" async src="https://tenor.com/embed.js"></script>

Dans le monde des Bisounours, toute votre équipe connait ces principes et les appliquent scrupuleusement. Dans la vraie vie c'est différent : On fait, on défait et on injecte très souvent sans abstraction.

Echouer, c'est avoir la possibilité de recommencer de manière plus intelligente.