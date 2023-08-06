===============================
Gestion d'identifiants pérennes
===============================

Introduction
============

* Pourquoi avoir des identifiants plutôt que simplement des URL (qui peuvent
  être tout aussi pérennes) ?

  Un identifiant (qui peut d'ailleurs être inclus dans une URL, comme dans le
  cas de ARK) offre une indication plus claire à l'utilisateur final que la
  référence de l'objet est persistante alors qu'il est difficile de dire à
  partir d'une URL si elle est persistante ou non.

  Un identifiant peut être diffusé par plusieurs canaux (via différentes URL
  incluant un même identifiant par exemple). L'utilisateur final peut savoir
  qu'il s'agit de la même ressource.

* ARK vs DOI

  ARK et DOI fournissent tous deux un mécanisme d'identification pérenne des
  objets. Historiquement DOI est associé au monde des éditeurs (notamment de
  publications techniques) et ARK plutôt au monde des associations culturelles
  (bibliothèques, archives, etc.). La création d'identifiant DOI est payante.

  ARK s'intéresse uniquement à l'aspect pérenne de l'identification des
  objets, pas à la persistance de l'accès à ces objets qui est vu comme une
  question de *service*. Ainsi un identifiant ARK est généralement inclus dans
  une URL de façon à être actionnable directement. DOI s'appuie sur un
  ensemble d'autorités intermédiaires garantes du registre des identifiants et
  chargées de la résolution des identifiants DOI (en URL). Ainsi le système DOI
  se substitue au mécanisme de résolution du DNS ce que ne fait pas ARK (à
  dessein).

  ARK laisse une grande liberté à l'autorité de nommage.


ARK
===

La forme générale d'un identifiant ARK_ est la suivante (les éléments entre
crochets sont optionnels) :

::

    [http://NMAH/]ark:/NAAN/Name[Qualifier]


- ``NMAH`` (`Name Mapping Authority Hostport`) est une adresse
  (potentiellement temporaire) qui fournira une réponse aux requêtes ARK, on
  parle d'autorité d'adressage. Cette autorité fournit le service de
  persistence des URL.

- ``NAAN`` (`Name Assigning Authority Number`) est l'identifiant de l'autorité
  de nommage. Il sert notamment à obtenir (auprès d'un registre) un ``NMAH``
  valide pour cette autorité.

- ``Name`` est le nom assigné par l'autorité de nommage.

- ``Qualifier`` permet de fournir d'autres ressources ou représentation à
  partir de l'identifiant ARK (par exemple, une page particulière d'un
  document, une vue particulière ; voir des exemples plus loin).

.. _ARK: https://tools.ietf.org/id/draft-kunze-ark-15.txt


Génération de la partie ``NAME`` des identifiants ARK
-----------------------------------------------------

La partie ``NAME`` de l'identifiant ARK est de la responsabilité de
l'autorité de nommage. Une grande liberté est laissée à cette autorité mais
en pratique on recommande de générer des identifiants opaques en respectant
quelques règles comme :

- ne pas rentrer en conflit avec la syntaxe HTML/XML
- éviter les caractères de ponctuation
- de façon générale, limiter les effets liés au contexte du langage de
  l'utilisateur

A priori, l'autorité de nommage est libre de générer des noms selon la méthode
qu'elle choisit. Il est par exemple assez courant de s'appuyer sur un
identifiant existant en interne de l'organisation pour construire un
identifiant ARK. Il existe des logiciels (tel que NOID_ ou arkpy_) ou des
services Web (comme EZID_) qui permettent de d'automatiser la génération (et
la validation) des identifiants ARK.

.. _NOID: https://wiki.ucop.edu/display/Curation/NOID
.. _arkpy: https://pypi.python.org/pypi/arkpy
.. _EZID: http://ezid.cdlib.org/


La partie ``Qualifier``
-----------------------

L'utilisation de cette partie optionnelle de l'identifiant ARK est laissé à la
discrétion de l'autorité de nommage. Elle permet souvent de fournir des
services ou ressources complémentaires associés à l'objet identifié par le
numéro ARK (par exemple la version d'un document, différents formats ou
langues). Par exemple, ::

  http://gallica.bnf.fr/ark:/12148/bpt6k103039f/f26.thumbnail

référence la page 26 en miniature du document identifié par `ark:/12148/bpt6k103039f`.

Historiquement,  le standard ARK propose également un protocole de requête
permettant d'obtenir des informations supplémentaires (notamment liées à la
persistence) à partir d'un identifiant. Ce protocole nommé `THUMP` (pour `The
HTTP URL Mapping Protocol`) est basé sur l'utilisation du caractère ``?`` à
ajouter à l'identifiant va enrichir la réponse HTTP d'un enregistrement
de métadonnées spécifiques à ARK. En pratique, les implémentations de ce
protocole semble assez rares, probablement du fait que la plupart des
fournisseurs de services ARK ont choisi de s'appuyer sur les `qualifiers`.

Résoudre les identifiants ARK
-----------------------------

La résolution des identifiants ARK repose en général sur le mécanisme de DNS et d'URL. Le standard
ne spécifie pas à notre connaissance de moyen d'obtenir l'"adresse" d'un objet à partir de son
identifiant ARK uniquement.


Utilisation d'ARK à la BNF
==========================

ARK est utilisé pour identifier les ressources du type *documents numériques* et *notices*
(bibliographiques, d'autorité, etc). Dans chaque cas, la BNF utilise un identifiant interne
(existant) pour générer l'identifiant ARK avec en plus :

* un préfixe correspondant au type de ressource,
* un caractère de contrôle

La politique d'utilisation des identifiants ARK à la BNF est disponible à
l'adresse suivante : http://ark.bnf.fr/ark:/12148/bpt6k107371t.policy.

Selon les portails de la BNF, l'identifiant ARK peut servir directement d'URL
principale ou uniquement d'URL *pérenne* (permalien). En particulier, le
portail `data.bnf.fr`_ transforme une URL incluant un identifiant ARK en URL
sans identifiant, mais incluant une partie intelligible permettant
de reconnaitre l'objet désigné. Par exemple,
l'URL `http://data.bnf.fr/ark:/12148/cb11907966z` devient
`http://data.bnf.fr/11907966/victor_hugo/` et est référencée en tant que
permalien de la ressource. On notera la présence de l'identifiant de la notice
`11907966` dans les deux URL et le préfixe `c` indiquant qu'il s'agit d'une
notice (*a contrario* http://gallica.bnf.fr/ark:/12148/bpt6k107371t référence
un document numérique).

Les identifiants ARK sont par ailleurs utilisés en tant qu'URL dans la version
RDF des documents (voir par exemple :
http://data.bnf.fr/11907966/victor_hugo/rdf.xml) et sont aussi présents dans
la version JSON (sous forme courte).

.. _`data.bnf.fr`: http://data.bnf.fr


Utilisation d'ARK dans le cadre du Référentiel SAEM
===================================================

Le référentiel permet de paramétrer des autorités nommante ARK. Chaque autorité administrative est
associée à une autorité nommante et enfin chaque utilisateur est lui-même associé à une autorité
administrative.

Pour créer une notice d'autorité, un vocabulaire ou un profil SEDA, il faut spécifier l'autorité
nommante qui sera utilisée pour générer on identifiant ARK - par défaut celle de l'autorité
administrative de l'utilisateur connecté.

Une fois le ``NAAN`` désigné, le ``Name`` est généré de la forme "<prefix><random number>" avec préfix qui vaut :

* 'r' pour les notices d'autorités (`AuthorityRecord`),

* 'p' pour les profiles SEDA (`SEDAArchiveTransfer`),

* 'v' pour les vocabulaires (`ConceptScheme`),

* 'c' pour les termes de vocabulaire (`Concept`),

* 'o' pour les autorités administratives (`Organization`),

* 'ou' pour les unités administratives (`OrganizationUnit`),

* 'oa' pour les agents (`Agent`),

* 'a' pour les identifiants attribués par le web-service d'assignement d'identifiant ARK, en général
  pour les archives proprement dites.