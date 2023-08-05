====
SKOS
====

Le référentiel fournit une implémentation de SKOS_. Les thésaurus ou vocabulaires contrôlés peuvent
être créés ou importés directement dans l'interface web ou bien importés en ligne de commande.

.. _SKOS: https://fr.wikipedia.org/wiki/Simple_Knowledge_Organization_System

Notez qu'un vocabulaire importé peut être rattaché à une **source** ou non. L'intérêt de passer par
une source est que cette dernière permet de conserver l'URL d'origine du vocabulaire et ainsi de le
(re)synchroniser plus tard. De plus le vocabulaire et ses concepts sont identifiés comme provenant
de cette source.

Dans l'interface web, il y a deux moyens pour importer un vocabulaire en fonction de son
format. Pour importer un vocabulaire au format SKOS (XML ou n3 par exemple) il faut ajouter une
source via l'action "importer un vocabulaire contrôlé" disponible sur la page d'accueil. Si vous
souhaitez importer un fichier SKOS directement, il faut utiliser l'import en ligne de commande
expliqué ci-dessous.

Vous pouvez également depuis un vocabulaire existant importer des concepts issus d'un fichier CSV
"simple" ou Linked-CSV.


Import de vocabulaire en ligne de commande
==========================================

Lorsqu'il est lancé par l'interface web, l'import de thésaurus SKOS ne peut
utiliser les optimisations qui deviennent nécessaires dès que le thésaurus est
de taille conséquente (plus d'une centaine de concepts). En effet ces
optimisations nécessitent que l'import soit effectué sans que d'autres
connexions à la base de données soient actives (ce qui implique donc de stopper
le serveur web pendant ce temps).

Pour importer un fichier SKOS RDF sans que celui-ci soit rattaché à une source de données, vous
pouvez utiliser la commande 'skos-import' de `cubicweb-ctl` :

::

    CW_MODE=user cubicweb-ctl skos-import saemref fichier.rdf

Pour déclencher l'import initial ou la synchronisation de données SKOS RDF dont l'URL a été
spécifiée par l'ajout d'une source dans l'interface web, vous pouvez utiliser la commande
'source-sync' :

::

    CW_MODE=user cubicweb-ctl source-sync saemref <nom de la source>

Ces deux exemples supposent que votre instance se nomme "saem" et que vous avez coupé l'interface
web au préalable (``cubicweb-ctl stop saemref`` ou ``supervisorctl stop saemref`` si votre instance est
supervisée).


Import de fichier Linked CSV
============================

Vous pouvez importer un fichier au format `Linked CSV`_ depuis l'action "importer des concepts"
 disponible via l'onglet "concepts" d'un vocabulaire. Hormis le format, vous pourrez spécifier :

* le séparateur de colonnes (au choix parmi : tab, ',', ';' et espace),
* la langue par défaut des textes contenus dans le fichier,
* l'encodage du fichier.


.. _`Linked CSV`: http://jenit.github.io/linked-csv/)

Un fichier LCSV contient sur ces premières lignes des méta-données permettant d'associer les
différentes colonnes à une ontologie (SKOS/RDF en ce qui nous concerne).

Structure d'un fichier Linked CSV
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le fichier doit commencer par une ligne d'en-tête spécifiant le contenu des colonnes.
Cette ligne d'entête permettra d'identifier la colonne `#` qui signalera les lignes d'informations
*prolog* et la colonne `$id` qui contiendra un identifiant local pour les concepts décrits par chaque ligne.
Les autres valeurs présentes dans cette ligne ne seront pas utilisées lors du traitement du fichier
mais peuvent être renseignées pour améliorer la lisibilité du document.

Cette première ligne sera suivie d'une ou plusieurs lignes dites lignes *prolog*. Ces lignes
contiennent les informations qui nous permettent d'associer la valeur de chaque colonne au concept
décrit par la ligne.
La nature des informations de chaque ligne sera donnée par la valeur de la colonne `#`.
Les différentes valeurs possibles pour la colonne `#` sont:

* `url`, cette ligne indique la relation a établir entre le concept décrit et la
  valeur de chaque colonne dans le cas de la colonne `$id`, cette ligne spécifie
  le type des données représentées par chaque ligne (ex : `skos:Concept`)

* `type`, cette ligne indique le type de données contenu dans chaque colonne
  (`url`, `string`, `integer`)

* `lang`, cette ligne indique, uniquement pour les données de type `string`, la
  langue du texte. Si aucune langue n'est spécifiée, celle fournie par le
  formulaire sera utilisée par défaut.

Les colonnes pour lesquelles aucune information *prolog* n'aura été spécifiée seront ignorées lors du
traitement.

Les lignes *prolog* sont suivies par les lignes de données, identifiables par le fait que la
colonne `#` est vide. Toute ligne *prolog* survenant après une ligne de données sera ignorée.

Une erreur sera levée et le fichier non importé en cas de :

* fichier vide,

* absence de la colonne `#` ou `$id`,

* absence de valeur pour une colonne dans la ligne *url* (ou absence d'une ligne *url*)


Exemple
~~~~~~~

+------+------------+---------------+-----------------------+-------------------------------------+
|#     |$id         |Concept parent |Libellé                |Définition                           |
+======+============+===============+=======================+=====================================+
|lang  |            |               |fr                     |fr                                   |
+------+------------+---------------+-----------------------+-------------------------------------+
|url   |skos:Concept|skos:broader   |skos:prefLabel         |skos:definition                      |
+------+------------+---------------+-----------------------+-------------------------------------+
|type  |            |url            |string                 |string                               |
+------+------------+---------------+-----------------------+-------------------------------------+
|      |#1          |               |Vie politique          |organisation politique de l'organisme|
+------+------------+---------------+-----------------------+-------------------------------------+
|      |#2          |#1             |Assemblée délibérante  |règles de fonctionnement             |
+------+------------+---------------+-----------------------+-------------------------------------+
|      |#3          |#1             |Instances consultatives|création en application de la loi    |
+------+------------+---------------+-----------------------+-------------------------------------+
|      |#4          |               |Pilotage               |objectifs à long terme               |
+------+------------+---------------+-----------------------+-------------------------------------+
|      |#5          |#4             |Pilotage de Bordeaux   |projet d'administration              |
+------+------------+---------------+-----------------------+-------------------------------------+


Import de fichier CSV simple
============================

Vous pouvez également fournir un fichier décrivant simplement une hiérarchie de concepts :

* un concept par ligne,

* le délimiteur permet d'indiquer le niveau hiérarchique (aucun si le concept n'a pas de parent).

Par exemple, avec ';' comme délimiteur : ::


        espèce
        ;serpent
        ;;python

va ajouter au vocabulaire un concept 'espèce' qui aura un sous-concept 'serpent', qui aura lui-même
un sous-concept 'python'.

Enfin un simple fichier avec un mot par ligne fera l'affaire : ::

   bleu
   jaune
   rouge
