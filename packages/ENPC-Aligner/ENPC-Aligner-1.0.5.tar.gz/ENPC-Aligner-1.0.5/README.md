# Bibliothèque d'alignement de textes dans des langues différentes

# Théorie

Le poster de présentation des méthodes implémentées dans cette bibliothèque est [ici](/doc/theory.pdf).

# Installer la bibliothèque

Lancez dans un terminal :
`sudo pip install ENPC-Aligner`

# Tester la bibliothèque

Lancez dans un terminal :
`align-example`

## Textes sources

* Bible
  * fr : http://godieu.com/doc/telechargement.html (Bible Jean Frédéric Ostervald 1996)
  * en : http://www.truth.info/download/bible.htm (King James Bible also known as the Authorised Version)
* Le petit prince
  * fr : http://lepetitprinceexupery.free.fr/telecharger/le-petit-prince--antoine-de-saint-exupery.txt
  * en : https://www.odaha.com/antoine-de-saint-exupery/maly-princ/the-little-prince

En 20 langues : http://www.malyksiaze.net/us/ksiazka

* Pinocchio :
  * fr : https://www.ebooksgratuits.com/pdf/collodi_pinocchio.pdf
  * en : http://www.gutenberg.org/files/500/500-0.txt

## Development

```
sudo pip install -e .
```
Cela créer un lien symbolique dans site-packages vers le répo pour que les modifications des sources prennent effet immédiatement.

## Publish to PyPi

Mettre dans ~/.pypirc
```
[distutils]
index-servers =
    pypi

[pypi]
repository: https://pypi.org/project/ENPC-Aligner/
username: <username>
password: <password>
```

Modifier le numéro de version dans *enpc_aligner/version.py* et lancer
```
python setup.py sdist upload -r pypi
```
