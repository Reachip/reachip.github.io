---
layout: post
title: Approche stratégique pour la gestion du code legacy
subtitle: Il dort dans le soleil, la main sur sa poitrine. Tranquille, il a deux trous rouges au côté droit.
cover-img: /assets/img/shaun-darwood-TC6u_HnDDqs-unsplash.jpg
thumbnail-img: /assets/img/shaun-darwood-TC6u_HnDDqs-unsplash.jpg
share-img: /assets/img/shaun-darwood-TC6u_HnDDqs-unsplash.jpg
tags: [refactoring, legacy]
---

La gestion du code legacy a toujours été une étape cruciale dans le cycle de vie d'un logiciel. Souvent négligée, elle peut être repoussée jusqu'à ce que la dette technique devienne si importante qu'il devient impératif pour les développeurs de prendre en charge cette problématique qui entrave toute amélioration du produit.

Comme le grand secret de notre maladie oscille entre la précipitation et la négligence (comme dirait l'autre), la précipitation liées à l'urgence induit trop souvent à la négligence lorsque que l'on s'attaque à la dette technique.Beaucoup de développeurs trouvent compliquer de trouver un équilibre entre une action réfléchie et une attention minutieuse pour surmonter ces défis.

Il nous faut alors un plan d'action global, conçu pour atteindre un objectif spécifique à long terme. Il faudra prendre des décisions clés et de mettre en œuvre des actions coordonnées pour maximiser les chances de succès dans la transformation de notre code legacy. En d'autres termes, mener à bien une stratégie.

# Stratégie "Strangler Fig"

Martin Fowler propose pour cela un design pattern apppelé Strangler Fig. Il décrit une stratégie de modernisation progressive d'un système existant, plutôt que de le remplacer d'un coup par un système entièrement nouveau.

Cette stratégie à plusieurs avantages :

- **Réduction des risques :** Plutôt que de remplacer un système entièrement fonctionnel par un nouveau système, on permet de réduire les risques associés à une refonte complète. En modernisant progressivement des parties spécifiques du système, les problèmes potentiels peuvent être identifiés et résolus plus facilement, minimisant ainsi les risques d'interruption des opérations commerciales.

- **Amélioration de la stabilité :** En modernisant progressivement le système, il est possible de s'assurer que chaque étape de la transition est stable et fonctionnelle. Cela permet de maintenir la continuité des opérations et d'éviter les problèmes majeurs pouvant survenir lors du passage à un nouveau système.

- **Notion de coexistence harmonieuse :** Le pattern Strangler Fig permet à l'ancien système et au nouveau système de coexister harmonieusement pendant la transition. Les fonctionnalités du système existant peuvent être progressivement migrées vers le nouveau système sans interruption majeure des services. Cela permet aux utilisateurs de bénéficier des améliorations apportées par le nouveau système sans perturber leur expérience utilisateur.

- **Modularité et scalabilité :** La modernisation progressive permet de décomposer le système en modules plus petits et plus gérables. Chaque module peut être modernisé indépendamment, ce qui facilite la maintenance, la mise à l'échelle et l'intégration de nouvelles fonctionnalités.

- **Utilisation des ressources existantes :** En utilisant le pattern Strangler Fig, les investissements déjà réalisés dans le système existant peuvent être réutilisés. Les ressources, telles que les bases de données, les infrastructures de déploiement, les intégrations, etc., peuvent être conservées et utilisées avec le nouveau système, réduisant ainsi les coûts associés à une refonte complète.

- **Approche itérative et adaptable :** Le design pattern Strangler Fig suit une approche itérative, permettant des ajustements continus en fonction des besoins et des retours d'expérience. Cela facilite l'adaptation aux changements et aux évolutions du système, tout en minimisant les perturbations pour les utilisateurs et les opérations.

On obtient alors approche progressive, souple et à moindre risque pour moderniser un système existant. Il permet de réduire les risques, d'améliorer la stabilité, de faciliter la coexistence harmonieuse des anciens et nouveaux systèmes, de favoriser la modularité et la scalabilité, de réutiliser les ressources existantes et de s'adapter de manière itérative aux changements.

# Etude de cas : l'entreprise Compta & Ci

Imaginez travailler dans l'entreprise Compta & Ci qui produit le meilleur logiciel de comptabilité pour toutes les petites PME françaises du territoire.

Dans ce logiciel, on trouve les fonctionnalités suivantes :

- **Saisie des transactions :** Saisis les transactions financières telles que les ventes, les achats, les paiements, les encaissements, les salaires, etc. Il offre des formulaires et des modèles préconfigurés pour faciliter la saisie des données.

- **Journalisation :** Enregistre automatiquement toutes les transactions dans un journal général, en attribuant des numéros de compte, des dates et des montants.

- **Comptes fournisseurs et clients :** Gérer les comptes fournisseurs et clients en enregistrant les factures, les paiements, les avoirs, les remboursements, les soldes et les historiques de transactions.

- **Gestion de la trésorerie :** Suivre les flux de trésorerie, de gérer les comptes bancaires, de concilier les relevés bancaires, d'enregistrer les dépôts, les retraits et les virements.

- **Facturation et devis :** Fonctionnalités de facturation et de création de devis, permettant de générer des factures professionnelles, d'envoyer des devis aux clients et de suivre les paiements.

- **Gestion des stocks :** Modules de gestion des stocks, permettant de suivre les mouvements d'inventaire, de gérer les commandes, les réceptions, les retours et les niveaux de stock.

- **Rapports financiers :** Générer des rapports financiers tels que le bilan, le compte de résultat, le grand livre, le livre de caisse, les rapports de TVA, les rapports de gestion, etc. Ces rapports aident à analyser la santé financière de l'entreprise.

L'entreprise maintient painiblement sont logiciel depuis plusieurs années. Plusieurs éléments de l’infrastructure sont en phase décommissionnement. Par exemple, le support à l'ensemble des Interface Homme Machine (IHM), qui a été gelé en 2022, sera totalement arrêté en 2025. De même pour le bus de communication entre les IHM et la partie serveur.

En somme, Compta & Ci veut revoir l'aspect saisie des transactions et rapports financiers de son logiciel tout en ameliorant la qualité de code de ces deux fonctionnalités majeurs de l'application.

# Identification des zones à moderniser

Sur la base de l'analyse effectuée, nous devons tout d'abord identifier les parties du code qui doivent être modernisées en raison de leur obsolescence, de leur mauvaise performance ou de leurs risques de sécurité. Ici, on souhaite repenser l'IHM qui était une application pour client lourd au profit d'une application web non-obselète et améliorant le confort des utlisateurs.

La saisie des transactions représente une très grosse partie du logiciel et est fréquemment modifié et lu par les développeurs. On suppose donc qu'un refactoring est nécessaire pour cette aspect. Il en va de même pour la partie "rapport financiers".

C'est l'occasion de faire une ouverture sur la méthodologie de refactoring proposé par Mariusz Sieraczkiewicz que vous pouvez retrouver ici : [https://www.infoq.com/fr/presentations/natural-course-refactoring](https://www.infoq.com/fr/presentations/natural-course-refactoring)

On aimerait ainsi effectuer l'action représenter ci-dessous. Le but étant de progresssivement faire passer le code dit "legacy" à un code "moderne" étape par étape, au fur et à mesure de l'avancer des sprint et du temps allouer à ce refactoring comme mentionné précédemment.

![Acte I de la startégie strangler fig](/assets/img/legacy-code-article/legacy-code-acte-1.png)

# Mise en place du pattern

Une approche naif consisterait à directement liées les systèmes sain à la fois au système "legacy" et au nouveau système dit "moderne".

Avec cette approche, on se rend bien compte que les couches appelantes du nouveau système correspondent absoluement à ce qu'attendent les systèmes sains.

![Acte II de la startégie strangler fig](/assets/img/legacy-code-article/legacy-code-acte-2.png)

C'est généralement cette problèmatique qui pousse à refactorer rapidement et "en gros" sans approche progressive.

Le patttern Strangler Fig préconise d'éliminer ce problème en passant par une façade. Cette dernière isole les composants du système existant des changements et des dépendances introduits par les nouveaux composants. Elle intègre les nouvelles fonctionnalités ou services dans le système existant en fournissant une interface unifiée et permet aux composants existants de communiquer avec les nouvelles fonctionnalités, sans avoir à connaître les détails internes de ces dernières. On peut alors aisément faire cohabiter nos deux systèmes en cours de mutation.

```java
interface ComptaFacade {
    void enregistrerTransaction(Transaction transaction);
    void genererRapports();
}

class ComptaFacadeImpl implements ComptaFacade {
    private ModuleEnregistrementTransaction moduleEnregistrementTransaction;
    private ModuleRapportsFinanciers moduleRapportsFinanciers;

    public ComptaFacadeImpl() {
        this.moduleEnregistrementTransaction = new ModuleEnregistrementTransaction();
        this.moduleRapportsFinanciers = new ModuleRapportsFinanciers();
    }

    public void enregistrerTransaction(Transaction transaction) {
        moduleEnregistrementTransaction.enregistrer(transaction);
    }

    public void genererRapports() {
        moduleRapportsFinanciers.genererRapports();
    }
}

class ModuleEnregistrementTransaction {
    public void enregistrer(Transaction transaction) {
        // ...
    }
}

class ModuleRapportsFinanciers {
    public void genererRapports() {
        // ...
    }
}

class Transaction {

}
```

On peut utiliser la façade comme suit :

```java
ComptaFacade facade = new ComptaFacadeImpl();
Transaction transaction = new Transaction();

facade.enregistrerTransaction(transaction);
facade.genererRapports();
```

On se retrouve pour l'instant avec l'architecture representé ci-dessous.

![Acte III de la startégie strangler fig](/assets/img/legacy-code-article/legacy-code-acte-3.png)

On peut alors commencer la transition sans pour autant configurer la facade pour rediriger les appels. Il peut s'agir ici simplement de commencer à refactorer en optant par exemple pour une approche basé sur le Test Driven Design (TDD). L'idée étant ici de s'assurer que tout fonctionne avant de remplacer le système. Strangler Fig est justement là pour prendre le temps et les moyens nécessaire pour effectuer un refactoring minutieux.

![Acte IV de la startégie strangler fig](/assets/img/legacy-code-article/legacy-code-acte-4.png)

Vient sûrement la partie la plus délicate du processus. Lors de la transition, certains nouveaux systèmes, bien que déplacés, auront toujours besoin de l'API des systèmes legacy pour pouvoir continuer à fonctionner. Une solution permettant la communication entre système "moderne" et "legacy" peut-être d'utiliser l'Anti-Corruption Layer Pattern (ACL).

L'ACL permet de maintenir une interface propre et adaptée au système moderne, tout en gérant les interactions avec le système legacy. Il consiste à créer une couche intermédiaire, appelée "couche anti-corruption", entre le système moderne et le système legacy. La couche agit comme un traducteur entre les deux systèmes, en transformant les requêtes et les réponses de l'API legacy vers un format compréhensible pour le système moderne, et vice versa. En utilisant l'ACL, on respect la philosophie Strangler Fig qui est de moderniser, oui, mais progressivement !

![Acte V de la startégie strangler fig](/assets/img/legacy-code-article/legacy-code-acte-5.png)

Les parties de codes sont alors progressivement mis à jours jusqu'à que tout le travail à fournir soit terminé. On peut à ce stade hôter le lien qui relie le système legacy à la facade et au système moderne.

![Acte VI de la startégie strangler fig](/assets/img/legacy-code-article/legacy-code-acte-6.png)

Une fois que tous les tests passent, on peut alors supprimer la facade et directement interfacé notre nouveau système à nos différents services.

![Acte VI de la startégie strangler fig](/assets/img/legacy-code-article/legacy-code-acte-7.png)

# Quand ne pas utiliser Strangler Fig ?

On identifie deux situations où l'utilisation du pattern peut ne pas être appropriée.

## Incapacité d'exposer le système

Comme nous l'avons vu, le pattern "strangler fig" repose sur la capacité à intercepter les requêtes provenant de l'ancien système et à les rediriger vers la nouvelle version. Cependant, dans certains cas, il peut être difficile ou même impossible d'intercepter ces requêtes selon le SI ou évolue une application.

## Keep It Simple

Strangler Fig permet de réduire les risques en remplaçant progressivement les fonctionnalités, en s'assurant que le nouveau système fonctionne correctement à chaque étape.

A contrario, pour les systèmes plus petits et moins complexes, le coût et la complexité du remplacement complet peuvent être relativement faibles.

Dans ces cas, il est peut être plus simple et plus efficace de procéder à un remplacement complet du système plutôt que de mettre en place une telle stratégie.
