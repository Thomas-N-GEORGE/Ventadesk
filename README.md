# Ventadesk

Application de bureau de gestion des commandes.
Accompagne l'application Web Ventashop.
Destinée aux employés de Ventalis.


---

## Distribution :

 - Vous pouvez trouver l'exécutable correspondant à votre plateforme dans la release 1.0 de ce dépôt Github.

---
## Code source : 

### Comment installer Ventadesk en local : 

0. Pré-requis : 
 - Avoir installé Python v10. ou plus sur la machine locale. https://www.python.org/downloads/
 - Avoir installé Git sur la machine locale. https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

1. Cloner le projet : 
 - Copier le lien Github en haut à droite de la page "code" du dépôt.
 - Dans un terminal, se placer à l'emplacement local où l'on veut que le dossier source soit cloné.
 - Exécuter la commande git clone : 
````
 git clone https://github.com/Thomas-N-GEORGE/Ventadesk.git
````

 - En principe un dossier nommé Ventadesk s'est crée. S'y déplacer : 
````
 cd Ventadesk
````
2. Créer un environnement virtuel (ici nommé *env* ) à l'aide de la commande : 
````
 python3 -m venv env
````

3. Activer l'environnement virtuel à l'aide de la commande : 
 
* pour les plateformes Unix/Linux : 
````
 source env/bin/activate
````

* pour la plateforme Windows (cmd.exe):
````
 source env/scripts/activate
````
 * autre : consulter https://docs.python.org/3/library/venv.html

Votre invite de commande doit maintenant être précédée de `(env)`, vous indiquant que vous êtes bien dans l'environnement virtuel.

4. Installer les dépendances du projet : 
````
pip install -r requirements.txt
````

5. Lancer l'application : 
````
python3 cli.py
````
