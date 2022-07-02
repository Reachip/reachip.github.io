---
layout: post
title: Qu'est ce qu'une API (sur le web) ?
subtitle: Ou qu'est ce qu'une API REST pour rester dans la hype.
cover-img: /assets/img/servers.jpg
thumbnail-img: /assets/img/servers.jpg
share-img: /assets/img/servers.jpg
tags: [web, http, api]
---

En informatique tout est une question de données. Sans blague.

Parfois, voir souvent, il se peut que vous vouliez récupérer des données depuis un autre site internet : votre banque, Ruedesplaisirs.com, EDF, Facebook, Twitter etc.

Toutes ces données sont généralement récupérables depuis un serveur HTTP mais pas n'importe comment. En effet, on retourne **souvent (mais pas tout le temps)** du JSON en réponse à la requête HTTP pour une raison qu'on verra tout à l'heure.

# API de type "REST"

"REST" entre trop guillemets car c'est une façon de faire des API pour le web de manière très subjective.

D'après Wikipedia :

> REST (representational state transfer) est un style d'architecture logicielle définissant un ensemble de contraintes à utiliser
> pour créer des services web. Les services web conformes au style d'architecture REST, aussi appelés services web RESTful,
> établissent une interopérabilité entre les ordinateurs sur Internet. Les services web REST permettent aux systèmes effectuant des requêtes de manipuler des ressources web [...]

REST est donc un style d'architecture, une convention en d'autres termes. Il ne s'agit pas d'un protocole, d'un framework ou autre concept à appliquer à la lettre pour développer une API. On peut essayer de développer une API REST n'importe comment, d'ou l'importance d'écrire une documentation quand on veut en faire une.

## Un exemple

Disons que je veuille récupérer le nombre de cas infectés par le COVID-19 en France. Pour ça, je vais utiliser le service <a href="https://api.covid19api.com/">api.covid19api.com</a>.

En cherchant dans la doc, on m'indique que pour récupérer le nombre de cas en France dans plusieurs régions, il faut que je fasse une requête à l'adresse : <a href="https://api.covid19api.com/dayone/country/france/status/confirmed">https://api.covid19api.com/dayone/country/france/status/confirmed</a>

En faisant une requête avec curl, on obtient (en gros) :

```bash
curl -v https://api.covid19api.com/dayone/country/france/status/confirmed
```

```json
{
  "Country": "France",
  "CountryCode": "FR",
  "Province": "Martinique",
  "City": "",
  "CityCode": "",
  "Lat": "14.64",
  "Lon": "-61.02",
  "Cases": 202,
  "Status": "confirmed",
  "Date": "2020-06-07T00:00:00Z"
}
/*
 * etc ....
 */
```

Voilà un exemple de requête vers une API REST. On constate qu'une requête de type GET vers une URI spécifique nous retourne des données pour une ressource spécifique au format JSON.

## Pourquoi du JSON ?

### Simplicité et interportabilité

1. Quasiment tous les langages possèdent une librairie pour parser du JSON.
2. Du JSON peut facilement être convertis en liste, array, tableau (ou autre structure de données) pour pouvoir utiliser les données qu'il contient dans son programme.

```python
import json

DATA = '{"result":true, "count":42}';
json = json.loads(DATA)


print(json["count"])
// expected output: 42

print(json["result"])
// expected output: true
```

### Pour le front-end

Par soucis de framework JS en tout genre et de performance, il est courant pour le front-end de devoir communiquer avec le back-end pour récupérer toutes les données nécessaires à l'utilisateur. Pour ce faire, on implémente une API côté back-end.

Notre bien aimé JavaScript est en symbiose avec le JSON, si les données retournées par l'API sont en JSON, JS n'aura donc aucune difficulté à utiliser ces données, non non, vraiment aucune.

```js
const json = '{"result":true, "count":42}';
const obj = JSON.parse(json);

console.log(obj.count);
// expected output: 42

console.log(obj.result);
// expected output: true
```

<a href="https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Objets_globaux/JSON/parse">https://developer.mozilla.org/fr/docs/Web/JavaScript/Reference/Objets_globaux/JSON/parse</a>

### Parce que c'est cool le JSON, c'est issu du JS

Ça c'était pour troll.

## On peut récupérer des données, mais aussi en envoyer, en enlever et en modifier

Si on peut faire une requête de type GET, on peut aussi faire des requêtes POST, PUT, DELETE.

Pour cela, il vous faut une autorisation de la part de l'API, généralement légitimée par l'obtention d'un jeton (un peu comme un mot de passe) à fournir à l'API avant chaque requêtes pour prouver que c'est bien vous.

## Requête POST

Avec ce type de requête, on "poste" nos informations au serveur (et oui). La requête est généralement envoyée sous le format `application/x-www-form-urlencoded` :

```http
POST / HTTP/1.1
Host: https://reachip.github.io/e621/figurines/order/client?id=123
Content-Type: application/x-www-form-urlencoded

client=Loan&payement=espece
```

Rien n'empêche d'envoyer la donnée sous un autre format, par exemple en json en précisant au niveau du content-type `application/json`.

## Requête PUT

Même structure mais conceptuellement, au lieu de poster une nouvelle donnée, on modifie une donnée existante sur le serveur.

```http
PUT / HTTP/1.1
Host: https://reachip.github.io/e621/figurines/order/client?id=123
Content-Type: application/x-www-form-urlencoded

client=Loan&payement=nature
```

## Requête DELETE

Elle sert à demander la suppression d'une donnée.

```
DELETE /e621/figurines/order/client?id=123 HTTP/1.1
```
