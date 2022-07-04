---
layout: post
title: N'utilisez l'héritage que si cela est nécessaire !
subtitle: “Rien de plus pur que les rivières de diamants, rien de plus trouble que leur source.” - Hervé Bazin
cover-img: /assets/img/annie-spratt-lU4TuhmIKs4-unsplash.jpeg
thumbnail-img: /assets/img/annie-spratt-lU4TuhmIKs4-unsplash.jpeg
share-img: /assets/img/annie-spratt-lU4TuhmIKs4-unsplash.jpeg
tags: [conception, programmation, poo]
---

On retient souvent l'héritage comme l'un des principaux concepts piliers de la programmation orientée objet. En partant du polymorphisme, à l'addition de couches d'abstraction jusqu'à l'ensapsulation, par étonnant que des langages comme Python fondent leurs architectures sur la base d'un seul objet, qui fait dérivé l'ensemble des types de bases d'un langage.

Comme il est d'usage à notre époque de déconstruire tout et n'importe quoi, nous allons tenter aujourd'hui de déconstruire le mythe de l'héritage qui résout ou presque n'importe quel problème. Et puisque tout ce qui est extrême est dangereux, nous verrons à la fois les bons usages de l'héritage, mais surtout les mauvais, parce que j'estime que vous êtes là pour ça non ?

# L'héritage, _de base_, c'est une bonne idée si

Bah oui, bien sûr que l'héritage c'est bien :

- On réduit, voir on fait disparaitre les redondances dans le code.
- On pourrait simplifier la compréhension du code en représentant un type d'objet pouvant appartenir à d'autre type de sous-objets.
- Le code est réutilisable. Si les besoins changent, on est capable d'implémenter un nouveaux sous-type sans devoir retoucher l'existant (principe de l'ouverture-fermeture issus des principes SOLID).

<img 
    style="width: 200px;display: block;margin-left: auto;margin-right: auto;" 
    src="/assets/img/polygones-heritage.png"
/>

L'exemple typique pour expliquer l'héritage est celui des polygones. Parce que tout le monde sait ce qu'est un polygone. Sauf les Kevin.

On pourrait tout simplement représenter un polygone, permettant de représenter les données et le comportements de base d'un carré, d'un triangle ou encore d'un cercle.

Un carré peut-être en quelque sorte un cube, une sphère ou un rectangle.


```python
class Coordinates:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z


class Polygon:
    def __init__(self, coordinates):
      self.x = coordinates.x
      self.y = coordinates.y
      self.z = coordinates.z

    def move(self, dot, distance):
      setattr(self, dot, getattr(self, dot) + distance)
      
    def move_x(self, distance):
      self.move("x", distance)

    def move_y(self, distance):
      self.move("y", distance)

    def move_z(self, distance):
      self.move("z", distance)

    def __str__(self):
      return f"x => {self.x} y => {self.y} z => {self.z}"


class Square(Polygon):
  def __init__(self, coordinates, width):
    super().__init__(coordinates)
    self.width = width


class Rectangle(Square):
    def __init__(self, coordinates, width, lenght):
      super().__init__(coordinates, width)
      self.lenght = lenght


square = Square(Coordinates(27, 39, 40), 10)
rectangle = Rectangle(Coordinates(27, 39, 40), 10, 20)
print(rectangle) # x => 27 y => 39 z => 40

rectangle.move_x(10)
print(rectangle) # x => 37 y => 39 z => 40

print(isinstance(rectangle, Polygon)) # True
print(isinstance(rectangle, Square)) # True
```

On a ici une représentation simpliste de ce qu'on peut faire avec de l'héritage.
Quelques points sont à noter : 

- L'héritage permet le concept de polymorphisme, un rectangle peut alors être traité comme un rectangle ou comme un polygone.
- On peut réutiliser les comportements (méthodes) des classes mères afin de les réutiliser dans les classes enfants.
- Dans les langages permettant la surcharge de méthodes, on pourrait réutiliser le constrcuteur de la classe sans avoir besoin de le re-écrire.

# L'héritage, c'est une très (très) mauvaise idée si

Dans un cadre non-abusif, l'héritage est une solution louable et maintenable dans le temps, mais comme le monde n'est jamais parfait, on constate très souvent un usage abusif de l'héritage. 

On pourrait utiliser d'autres solutions comme les interfaces, afin de s'assurer de l'implementation d'un comportement ou des classes abstraites dans le but de n'utiliser que le nécessaire et d'éviter de tomber dans le piège de la classe "fourre-tout". J'appelle fourre-tout des classes des classes contienent des données inutilisées pour la plupart des classes enfants ou qui a trop de résponsabilitées.

## Utiliser l'héritage afin de partager du code


### Non respect du principe de substitution de Liskov

Faire de l'héritage, c'est s'assurer qu'on puisse réspecter le principe de substitution de Liskov, autrement, il n'est pas pertinent de faire de l'héritage. Dans l'exemple précédent, on doit pouvoir s'assurer que notre carré est bien un polygone et qu'aucune des méthodes dérivées de la classe mère sont bien "implémentable". On se doute bien que partager du code via l'héritage peut vite devenir une façon trivial de ne pas respecter ce principe.

### Non respect du principe de responsabilitée unique

Ça aussi. Facile de tomber dans le piège ! Il se peut quand dans notre exemple précédent on veuille rajouter une méthode dans notre carré qui fait en sorte de le déplacer en utilisant 

### Exemple


```python
class Coordinates:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z


class Polygon:
    def __init__(self, coordinates):
      self.x = coordinates.x
      self.y = coordinates.y
      self.z = coordinates.z

    def move(self, dot, distance):
      setattr(self, dot, getattr(self, dot) + distance)
      
    def move_x(self, distance):
      self.move("x", distance)

    def move_y(self, distance):
      self.move("y", distance)

    def move_z(self, distance):
      self.move("z", distance)

    def __str__(self):
      return f"x => {self.x} y => {self.y} z => {self.z}"


class Square(Polygon):
    def __init__(self, coordinates, width):
        super().__init__(coordinates)
        self.width = width

    def move_square(self, distance):
        self.move_x(distance)
        self.move_y(distance)
  

square = Square(Coordinates(27, 39, 40), 10)
print(square) # x => 27 y => 39 z => 40

square.move_square(34)
print(square) # x => 61 y => 73 z => 40
```

## Utiliser l'héritage au lieu des interfaces


## Utiliser partiellement l'héritage


# Conclusion