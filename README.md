>>Bofip-scraping

Description :
Ce projet GIT est un ensemble de scripts Python permettant de scraper des informations du site bofip.impots.gouv.fr (telles que les documents BOI et le contenu des articles).
        
Guide d'utilisation :
    -Avoir Python 3.0 ou plus installé et un IDE de préférence.
    -Télécharger/cloner le repo, l'emplacement n'a pas d'importance tant que le dossier '/data' existe.
    -Essayer de lire un peu le code pour le comprendre.
    -Lancer les scripts qui vous intéressent.

Si le dossier '/data' existe bien, lancer les scripts dans cet ordre :
scraping.py -> infoharvestV2.2.py
et optionnellement :
BOI_href_scrap.py -> BOI_scrapping.py

    
Gestion des erreurs /!\ :
S'il y a une/des erreurs, il est très probable qu'elles viennent des fonctions save_json / save_data ou autre itération de ce type. Pour une raison obscure,
il arrive que le code ne fonctionne que si l'on utilise les chemins absolus au lieu des chemins relatifs. 
Si rien ne fonctionne, prenez juste les informations déjà présente dans '/data'


Légalité :
https://github.com/etalab/licence-ouverte/blob/master/LO.md
D'après cette licence directement liée par le site :
N'importe qui est tout à fait en droit d'utiliser les informations à but commercial ou non, tant que je :
  - mentionne la source et la date de mise à jour de l’information (c'est fait dans le code).
  - respecte les lois en vigueur sur la protection des données personnelles si l'information contient de telles données (ça tombe bien, il n'y en a pas).
  - "n'induis pas en erreur quant au contenu, à la source et à la date de mise à jour de l’information" (altération de l'information à but malicieux).
