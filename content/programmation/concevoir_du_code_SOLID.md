Title: Concevoir du code SOLID
Date: 2021-03-27
Author: Rached MEJRI
Tags: conception, programmation, poo
Slug: concevoir-du-code-solid
Summary: Concevoir du code SOLID, sans mauvais jeux de mots.

<div class="videoWrapper">
    <iframe width="1280" height="765" src="https://www.youtube.com/embed/ozkNEOGpIe8" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div>

Dis donc ça faisait longtemps que je n'avais pas écris sur ce blog.

Aujourd'hui j'ai décidé d'écrire un article sur ce que sont les principes dit "SOLID", comment et quand les appliquer dans vos projets.

Tout d'abord, et toujours d'après ce chère Wikipédia :

>En programmation orientée objet, SOLID est un acronyme mnémonique qui regroupe cinq principes de conception destinés à produire des architectures logicielles plus compréhensibles, flexibles et maintenables. Les principes sont un sous-ensemble de nombreux principes promus par l'ingénieur logiciel et instructeur américain Robert C. Martin.

>Bien qu'ils s'appliquent à toute conception orientée objet, les principes SOLID peuvent également former une philosophie de base pour des méthodologies telles que le développement agile ou le développement de logiciels adaptatifs. 

Maintenant qu'on sait ça, place à la pratique. J'écris actuellement ces lignes avec tritesse car je n'utiliserais pas le langage Python pour illustrer mes propos, mais un le langage C# qui proposent une meilleur intégration des concepts d'interfaces, de classes abstraites et de polymorphisme. Nous aurions pu le faire en Python, mais cela aurait risqué d'être plus trivial à implémenter.

# Le principe de responsabilité unique

Ce principe est surement l'un des plus simples à comprendre. **Arrêtez les classes foures-tout !**
Une classe doit avoir une seule et unique responsabilité, une seule et unique tâche.

Si vous avez une classe qui représente une forme géométrique, une fausse bonne idée serait de lui passer des méthodes qui réalisent les calculs d'air ou de perimètre liées à cette classe. On se retrouve donc avec une classe qui doit à la fois créer nos formes et réaliser les calculs par rapports aux propriétés. Cela n'est pas modulable et viole les prochains principes que nous allons voir.

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

C'est bien mais on peut faire beaucoup mieux. Admettons que 