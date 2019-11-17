Title: Guide de survie à l'usage du projet final d'STI2D SIN
Date: 2019-04-07
Author: Rached MEJRI
Tags: tuto
Slug: guide-survie-projet-sti2d-sin
Summary: En toute modestie.

Parce que j'ai rencontré un élève de terminal STI2D complétement paumé à tout juste un mois et demi de sa soutenance oral de présentation de son projet final, j'ai décidé de faire une petite note concernant les éléments à connaître afin de ne pas périr tel un petit chiot asiatique jeté dans la marmite.

<div style="width:100%;height:0;padding-bottom:100%;position:relative;"><iframe src="https://giphy.com/embed/3o7ZeAgHVHDH0jCTN6" width="100%" height="100%" style="position:absolute" frameBorder="0" class="giphy-embed" allowFullScreen></iframe></div>
## Connaissances globales

- Arduino et/ou Raspberry PI et ses composants
- Notions de base en réseau et systèmes binaire puis héxadécimal
- Notions de base en éléctricité
- Diagrammes SysML
- Notions en SolidWorks
- Notions d'éco-conception et des concepts du développement durable
- Notions en signal

### Programmation
- Langage Python (pour le Raspberry PI)
- Langage C (pour l'Arduino)
- Système de gestion de bases de données pour MySQL et le langage SQL

#### Notions
- [Terminal](https://guide.boum.org/tomes/1_hors_connexions/3_outils/00_utiliser_un_terminal/)
- [Protocole Réseau](http://www.zeitoun.net/articles/les_protocoles_reseaux/start)
- [Threads](https://www.developpez.net/forums/d606570/c-cpp/cpp/c-quoi-thread/)
- [Programmation orientée objet](https://whatis.techtarget.com/fr/definition/Programmation-orientee-objet)
- [Base de données](https://www.commentcamarche.net/contents/104-bases-de-donnees-introduction)
- [Système UNIX (Linux)](http://sebsauvage.net/comprendre/linux/index.html)

#### Pour une application mobile

| Technologie | Documentation | Difficulté |
| --------    | --------      | --------   |
| React Native| https://facebook.github.io/react-native/docs/getting-started| Moyenne|
| Java et Kotlin pour Android | https://developer.android.com/docs | Difficile |
| Swift pour Iphone et Ipad | https://developer.apple.com/documentation/ | Moyenne |  

### Pour un site web

| Technologie | Documentation | Avantage | Inconvénient |
| -------- | -------- | -------- | -------- |
| PHP sans framework    | https://www.php.net/docs.php | Simple à mettre en place - | Désorganisé - lent - peu sécurisé |
| Flask (Python) | http://flask.pocoo.org/docs/1.0/ | Simple - organisé - léger | lent |
| Node JS (JavaScript) | https://nodejs.org/en/docs/ | Complexe | Très performant |


**PS:** La partie inconvénient et difficulté des deux tableaux sont évidemment non-objectif et prend donc seulement en compte mon avis et mes expériences personnelles.

### Pour communiquer

| Protocole/Technologie | Cas d'utilisation
| --------              | -------- |
| SFTP                   | Transfert de fichiers|
| SSH  | Contrôle à distance via un terminal
| HTTP | Serveur web - Récupération de données d'API REST/GRAPH SQL
| UART | Communication entre deux périphériques par câble (l'exemple le plus courant est celui d'un Arduino et ses composants)


## Logiciels

|Logiciel     |Alternatifs gratuites|Resource d'apprentissage|Utilité
|:------------|:-------------:|:-------------:|:-------------:|
|Solid Works  |Blender        |<a href="https://openclassrooms.com/fr/courses/1553986-apprenez-a-utiliser-solidworks">OpenClassroms</a>|  Construction de pièces     |
|Magic Draw  |Papyrus et son extension SysML|<a href="https://jmbruel.github.io/sysmlpapyrusbook/">Cours du professeur Jean-Michel Bruel (Université de Toulouse)</a>|Diagrammes SysML |
|Editeur de texte|VS Code, Notepad|<a href="https://www.supinfo.com/articles/single/6616-decouvrir-visual-studio-code-2017">Supinfo</a>|Coloration du code et/ou automatisation de tâches redondantes|

## Outils de coopérations
- Discord, une très très bonne alternatif à Skype.
- Trello, outil de gestion de projet en ligne facile à prendre en main.
- Wise mapping, l'un des seuls outils gratuits en ligne pour créer des cartes mentales.
- Digramme de Gantt afin de suivre la timeline du projet.

## Le mot de la fin

*Mise à jour du 06/05/2019*

Voilà tout pour ce billet. Il me semblait nécessaire de proposer des alternatifs gratuites aux logiciels proposés pour pouvoir pratiquer chez soi, sans devoir dépenser des centaines d'euros.

Finalement, j'avais le ressentis que ce que j'avais appris cette année de première n'était pas représentatif des notions à connaitre pour pouvoir consituer une application moderne, et je ne m'étais pas trompé. En espérant que ce billet pourra réparer les pots cassés.
