=======
EAC-CPF
=======

Le référentiel fournit une implémentation de EAC-CPF_ relativement complète. Les notices d'autorités
peuvent être créés ou importés directement dans l'interface web ou bien importés en ligne de
commande.

.. section sur les balises supportées ou non
.. include-url:: https://hg.logilab.org/review/cubes/eac/raw-file/tip/doc/supported.rst


Import de notices d'autorités en ligne de commande
==================================================

Pour importer un fichier EAC-CPF, vous pouvez utiliser la commande 'eac-import' de `cubicweb-ctl` :

::

    CW_MODE=user cubicweb-ctl eac-import saemref --authority <NAA name> fichier.rdf


À moins qu'il n'y ait qu'une seul autorité de nommage définie dans votre référentiel, il vous faudra
spécifier le nom de l'autorité à utiliser avec l'option `--authority`. Si vous ne connaissez pas le
nom de votre autorité de nommage, lancer la commande sans l'option elle vous indiquera les valeurs
possibles.


Export des notices en EAC
=========================

Le modèle des notices implémentées diffèrent nécessairement du module sous-jacent au EAC XML. Voici
quelques explications concernant l'export d'une notice en EAC XML.

La balise ``maintenanceStatus`` vaudra "new" si la notice a été créée mais pas encore été modifiée,
"revised" sinon.

La balise ``publicationStatus`` vaudra "inProcess" pour les notices dans l'état brouillon, "published"
pour les notices dans l'état publiée.

Pour chaque forme du nom, l'attribute 'parties' est découpée selon le caractère ", " puis chaque
élément est inséré dans une balise ``part``. C'est le traitement symétrique à ce qui est fait durant
l'import (concaténation des différentes balises ``part`` avec le séparateur ", ")