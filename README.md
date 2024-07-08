# Bofip-scraping

## Description
Ce projet GIT est un ensemble de scripts Python permettant de scraper des informations du site [bofip.impots.gouv.fr](https://bofip.impots.gouv.fr) (telles que les documents BOI et le contenu des articles).

## Guide d'utilisation
1. Avoir Python 3.0 ou plus installé et un IDE de préférence.
2. Télécharger/cloner le repo. L'emplacement n'a pas d'importance tant que le dossier `/data` existe.
3. Essayer de lire un peu le code pour le comprendre.
4. Lancer les scripts qui vous intéressent.

### Si le dossier `/data` existe bien, lancer les scripts dans cet ordre :
1. `scraping.py`
2. `infoharvestV2.2.py`

### Optionnellement :
1. `BOI_href_scrap.py`
2. `BOI_scrapping.py`

## Gestion des erreurs /!\ 
S'il y a une/des erreurs, il est très probable qu'elles viennent des fonctions `save_json`, `save_data` ou autre itération de ce type. Pour une raison obscure, il arrive que le code ne fonctionne que si l'on utilise les chemins absolus au lieu des chemins relatifs. Si rien ne fonctionne, prenez juste les informations déjà présentes dans `/data`.

## Légalité
[D'après cette licence](https://github.com/etalab/licence-ouverte/blob/master/LO.md) directement liée par le site :
- N'importe qui est tout à fait en droit d'utiliser les informations à but commercial ou non, tant que :
  - La source et la date de mise à jour de l’information sont mentionnées (c'est fait dans le code).
  - Les lois en vigueur sur la protection des données personnelles sont respectées si l'information contient de telles données (ça tombe bien, il n'y en a pas).
  - L'information n'induit pas en erreur quant à son contenu, sa source et sa date de mise à jour (altération de l'information à but malicieux).

---

Ce projet est mis à disposition selon les termes de la Licence Ouverte 2.0 d'Etalab.
