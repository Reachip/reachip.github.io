Title: Comment résoudre l'erreur ENOSPC watch limit sur expo ?
Date: 2019-11-11
Author: Rached MEJRI
Tags: js, tuto, expo, react native  
Slug: resoudre-erreur-ENOSPC-expo-react-native
Summary: Parce que j'adore bricoler

# Intro

Pour un projet top secret, je dois me servir de React Native afin de d'essayer de développer une application mobile multi-plateforme.

Sauf que coder tranquillement sans avoir une erreur qui n'arrive de nul part du jour au lendemain, avec le langage de programmation le plus incompris du monde (interpretez ça comme vous voulez), ça serait comme manger une biscotte sans Nutella.

# Le problème

Imaginez vous utiliser votre robinet, comme d'habitude, puis que du jour au lendemain ce même robinet s'arrête de fonctionner sans que vous ayez fait quoi que ce soit pour que l'eau arrête de couler.

Imaginez ce même problème sur Expo, un des outils pour générer, tester et déployer une application React Native avec ce code d'erreur : 

```
ENOSPC: System limit for number of file watchers reached...
```

Biensûr cette erreur n'apparaît pas dès votre premier lancement d'Expo mais après quelques semaines d'utilisation. Je ne sais pas pour vous, mais moi j'adore ce genre d'effet de suprise.

# La solution

Il va falloir chercher un fichier qui se trouve ici : 

```/proc/sys/fs/inotify/max_user_watches```

On le retrouve sur Mac et sur toutes les distributions Linux.
Sur Windows ? J'en sais rien.

Si on fait un ```cat``` sur ce fichier, vous pourrez constater qu'on trouve une valeur inférieur à 524288.

Si c'est le cas, il faut modifier le fichier qui se trouve ici : ```/etc/sysctl.conf``` et remplacer la valeur de ```fs.inotify.max_user_watches``` par 524288.

```bash
# sysctl settings are defined through files in
# /usr/lib/sysctl.d/, /run/sysctl.d/, and /etc/sysctl.d/.
#
# Vendors settings live in /usr/lib/sysctl.d/.
# To override a whole file, create a new file with the same in
# /etc/sysctl.d/ and put new settings there. To override
# only specific settings, add a file with a lexically later
# name in /etc/sysctl.d/ and put new settings there.
#
# For more information, see sysctl.conf(5) and sysctl.d(5).
fs.inotify.max_user_watches=524288
```

Il suffit ensuite d'appliquer les changements avec cette commande : 

```bash
sudo sysctl -p
```
# Conclusion 

Vive l'ecosystème JS !