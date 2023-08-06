Historique des révisions
========================

**0.17.2**

* Correction de l'import d'unités d'archive dans un profil (#43776568)

* Prise en compte des identifiants ARK pour l'import LCSV de concepts en ligne
  de commande (#44146518)

* Suppression des contraintes NOT NULL pour les champs "ville", "rue" et "code
  postal" du type d'entité "addresse postale" pour permettre l'import de
  données lorsque ces champs sont absents (ils sont non-requis par la norme
  EAC-CPF) (#44640239)

**0.17.1**

* Correction de la création d'une nouvelle version d'un profil (#42522316)

* Suppression des formats dupliqués dans l'export XSD/RNG (#42606987)

* Correction de l'erreur sur suppression d'un objet-donnée dans un profil (#42606987)

* Possibilité d'import LCSV en ligne commande (#37463080)

* Possibilité de tri sur les noeuds de l'arbre SEDA via drag & drop (financé par le SIAF)

**0.17.0**

SEDA :

* Ajout d'un identifiant sur les noeuds d'un profil (#39304385)

* Correction d'erreur sur les profils créés avant la version 0.16.0 (#39859256)

* Modification pour n'avoir que le vocabulaire "catégorie de fichiers" comme
  référence pour les types MIME et identifiants de format (#39322647)

* Ajout d'un attribut dans le XML indiquant si le profil est ambigüe ou non (#39305748)

* Transformation du mécanisme de détection des profils non validable en
  message de diagnostic du problème plutôt qu'une erreur (#39302963)

Vocabulaires :

* Correction évitant de modifier la date de modification du vocabulaire "type de
  mot clé" lorsque celui-ci est utilisé pour typer un autre vocabulare
  (#37975627)

* Restriction du vocabulaire des langues aux langues du SEDA 0.2 (#40281602)

Autres :

* Publication automatique des unités administratives et des contacts référents
  (#37370184)

* Ajout d'un service web retournant les sites d'archives et les versants
  associés (#37441757)


**0.16.1**

SEDA :

* Correction du type mime et identifiant de format des objet-données importés
  d'un composant unité d'archive (#38194980)

* Correction erreur sur création d'une unité d'archive ou d'une règle de gestion
  (#37884173)

**0.16.0**

SEDA :

* Ajout d'un contrôle de conformité pour les cardinalités ambigües en SEDA 0.2
  (#34307460)

* Filtrage du vocabulaire "langues" sur les codes disponibles en SEDA 0.2
  (#36332314)

* Gestion des type MIME et identifiants de format via un vocabulaire "catégorie
  de fichiers" (#36331831)

* Correction crash sur import d'UA dans un profil (#37372358)

Autres :

* Ajout de la possibilité d'importer des concepts dans un vocabulaire existant
  (#29482125)

* Correction crash sur création d'une notice d'autorité sur une base vide
  (#36759603)

* Correction crash sur ajout d'un email à un utilisateur (#36119710)

* Migration vers cubicweb 3.25 (#36861534)



**0.15.6**

SEDA :

* Correction de l'ordre des balises Document / ArchiveObject (#33070904)

* Correction de l'export des types MIME (e.g. `pdf` au lieu de
  `application/pdf`) (#32206261)

* Correction de l'export du langauge (e.g. `fra` au lieu de `fr`) (#32959185)

* Changement du libellé "Accord de service" devient "Accord de versement"
  (https://www.cubicweb.org/ticket/17098388)

* Changements pour s'assurer qu'on ne génère pas de profils invalidables
  (https://www.cubicweb.org/ticket/17098404)

  - dans le cas des éléments répétables (unité d'archive, objet données,
    mot-clé, historique) on ne peut plus avoir qu'un seul élément avec une
    cardinalité différente de un, sans quoi une erreur sera levé à l'édition

  - pour éviter les erreurs, la cardinalité par défaut est maintenant
    "obligatoire et unique" plutôt que "optionel et unique"

  - lors de l'export SEDA, on s'assure que l'élément de cardinalité différente
    de un est à la fin

Web services :

* Correction de l'identification de l'organisation sur le service d'attribution
  d'identifiant (#32206278)


**0.15.5**

OAI-PMH :

* Correction pour ne pas mettre à jour le concept/scheme lors du
  référencement par un profil ou une notice (#29296087)

SEDA :

* Correction des permissions rendant possible la modification d'un
  profil après sa publication (#25271719)

* Correction pour l'affichage de la cardinalité sur le champ date de
  début en création (#24660770)

* Correction de l'affichage du service producteur sur une unité
  d'archive (seda #17084054)

* Correction des valeurs exportées en SEDA 0.2 pour les langues (seda
  #17091259)

* Correction du manque de préfixe 'ark://' lors de l'export SEDA 2 des
  services (#26003592)

Web services :

* Le service d'assignement d'identifiant ark attend maintenant
  l'identifiant ARK complet de l'organisation (#29484932)


**0.15.4**

Sécurité :

* Correction des permissions d'ajout sur les unités d'organisation et
  les agents (#21913461)

* Correction des permissions d'ajout sur les types de notice (#21936714)

Interface utilisateur :

* Correction sur le rendu de la pagination après filtrage à l'aide des
  facettes (#21942222)

SEDA :

* Correction de l'ordre des élements `Description` et `Language` dans
  l'export SEDA 0.2 (#23707701)

* Correction crash sur export SEDA d'un profil avec un service
  producteur non fixé (#22071759)

* Ajout du  préfix 'ark:/' sur la valeur exportée pour `ArchivalProfil`
  (#23707073)

**0.15.3**

Interface utilisateur :

* Correction crash du formulaire de modification d'une notice sur la démo (#18336413, #19232725)
* Correction de la disparition du bouton "+" (ajouter un profil) lors de l'utilisation d'une facette (#18229045)
* Correction de l'incohérence des champs visibles dans le formulaire de création d'unité d'archive (#18337031)
* Correction du crash de l'onglet 'concepts' d'un vocabulaire "vide" (#15932289)
* Changement du libellé du bouton pour l'import d'unité d'archive (#18337720)
* Changement du libellé de l'onglet 'utilise' entre autorité nommante et notice d'autorité pour éviter une ambiguité (#19227068)
* Réinsertion du lien pour afficher la version du référentiel (#18554125)

Sécurité / permissions :

* Ajout de la possibilité à un utilisateur standard d'éditer les relations d'une notices (#18336405)
* Suppression de la possibilité à un administrateur de modifier un profil après sa publication (#19216837)
* Suppression de la possibilité d'ajouter des vocabulaires à un utilisateur standard (#18369309)


**0.15.1**

Interface utilisateur :

* cohérence entre le formulaire d'édition / création et l'onglet
  description d'une unité d'archive (seda #76bb0064f236)

* changement traduction des éléments du menu 'ajouter' de l'onglet
  "unité d'archives" (seda #7769b2787347),
  et de précurseur vs prédécesseur en eac (saem #fe766631d60a)

* amélioration du formulaire d'édition d'un vocabulaire (seda
  #c82265657b76, #78ea78713e34),
  d'un utilisateur (saem #810a47d39c9f, #80dc15aa47bc), de copie d'un
  profil (saem #5bacf7866df5)

* simplification générale de l'interface en enlevant les éléments
  indésirés (saem #55db28377169)

Schéma :

* ajout d'une contrainte sur l'état publié d'un profil pour la relation
  "utilisé par" (saem #95202d3dc968)

* ajout d'une contrainte d'unicité sur Agent(nom, autorité
  administrative) (saem #57c9841da900)

* suppression d'une contrainte d'unicité sur OrganizationUnit(nom) (saem
  #ca3741e6372d)

* correction / amélioration de la sécurité
  pour les relations "type d'agent" (saem #7e1a8f1c1102), "nouvelle
  version de" (saem #f3850e014596),
  "type de mot clé" (saem #36596ca5247c), les types d'entités ARK NAA
  (saem #85e085e85f4a),
  Activity (saem #b8599a52fa6d, #569dbecd0736, #a42d3be56b5f),
  Agent et OrganizationUnit (saem #569dbecd0736)

Autres :

* ne copie plus la relation "nouvelle version de" lors d'une copie (saem
  #dccf96319df2)

* cohérence des URL générés en fonction des versions du SEDA (saem
  #eacf1752ed3d)


**0.15.0**

Gestion fonctionnelle :

* Ajout d'un onglet pour les entité Autorités administratives (#12251003)

* Correctif pour l'ajout d'une relation 'utilise' entre autorité
  nommante et notice d'autorité (#14910419)

EAC :

* Affichage des relations entre agents dans une vue liste même pour les
  relations hiérarchiques et chronologique (#14591642)

* Export de l'identifiant ARK dans la fiche EAC (#12572781)

SEDA :

* Support des activités PROV sur les profils SEDA (#3101354)

* Affichage des règles de gestion héritées (#14593198)

* Correctif pour la création unité d'archives en tant qu'utilisateur non
  admin (#15224324)

* Correctif pour la création d'un objet données dans une unité
  d'archives (#14592486)

Interopérabilité :

* Exposition des données prov-o dans les vues RDF des notices
  d'autorité, vocabulaires et concepts (#12175187)

Interface utilisateur :

* Typage des vocabulaires, améliorant l'interface de saisie des
  mots-clés SEDA (#12351787)

* Correction d'un libellé sur la fenêtre modale de sélection de concept
  (#12346621)

* Amélioration de l'interface de saisie des mots clés (#14592456)

Autres :

* Possibilité de séparer une instance web d'une instance point d'accès
  OAI-PMH (#11855076)

* Correctif pour la création d'un email pour un utilisateur applicatif
  impossible (#15224342)


**0.14**

Gestion fonctionnelle :

* Ajout d'un ark sur les organisations (#12308170)
* Ajout d'une relation 'utilise' entre autorité nommante et notice d'autorité (#12572793)


EAC :

* Amélioration de la gestion des relations entre agents (#12136839)

* Implémentation du champ "statut juridique" (#12218902) et différentes formes du nom (#12249296)

* Plus de création d'agent lors de l'import EAC (#12573609)

* Outil d'import en ligne de commande d'un lot de fichiers EAC (#12294160)

* Ajout d'un service web pour l'ajout de fichier EAC (#12362590)


SEDA :

* Modification des messages par défaut de l'onglet contenu d'une unité d'archives, financé par le
  SIAF (#12346618)

* Séparation mot-clé libre / mot-clé contrôlé (#12349783)

* Suppression de l'identifiant pour les unités d'archives et objets-données (#12349490 et #12349471)

* Complétion des profils pour permettre la validation côté asalae (#12542834)


Interopérabilité :

* Rationalisation des urls et identifiants pour utiliser l'ARK quand disponible (#3606819)

* Développement d'un client en ligne de commande pour poster un fichier EAC (#12572067) et moissoner
  les notices EAC et les vocabulaires SKOS (#12571247), mis à disposition à Anaphore sous la forme
  d'un exécutable Windows

* Propagation des règles de gestion (#12369828)

* Ajout d'un set OAI pour les autorités administratives, aka organisations (#12369805)


Interface utilisateur :

* Suppression de l'affichage "Autorité d'archivage" sur les vue des autorités administratives
  (#12272253)

Autres :

* Modification de la formule Salt pour installer des paquets Python hébergé sur pypi.python.org
  plutôt que des RPM d'un entrepôt spécifique maintenu par Logilab

* Amélioration de la couverture de tests fonctionnels dans la formule Salt et
  ajout de test du client en ligne de commande vis-à-vis d'une application
  déployée.

* Montée de version de différents composants sous-jacents, et notamment passage à cubicweb 3.24

* Modification de la structure du cube `saem_ref` pour être transformée en paquet python standard
  (possible depuis cubicweb 3.24)


**0.13**

SEDA :

Changement majeur lié à l'utilisation du cube seda développé avec le SIAF sur la base du modèle SEDA
2, en lieu et place du modèle développé dans le référentiel. Pour le moment, uniquement les profils
"simplifiés" du cube seda sont visibles, et non les profils SEDA 2 complet. Ce changement entraîne :

* quelques éléments supplémentaires dans le modèle SEDA supporté (qu'il reste à exporter en XSD/RNG
  0.2/1.0),

* une interface utilisateur un peu différente,

* un support de l'export des profils au format RNG, ainsi qu'en version SEDA 2,

* uniquement des unités d'archives comme composant SEDA, plus de *data object* / document.

A noter que l'aide à la saisie "globale" (i.e. au niveau du profil) était avant transmise via le
champ *commentaire* du seda 0.2. C'est maintenant une annotation comme pour les autres, et on peut
décrire des commentaires comme les autres champs SEDA.

EAC :

Utilisation du cube eac extrait du référentiel pour utilisation dans le cadre du projet France
Archives. Ceci a permis d'avoir dans cette livraison l'implémentation du champ 'OtherRecordId' qui a
été financé par le SIAF.


OAI :

* Il faut maintenant obligatoirement indiquer le "metadata prefix" lors
  des échanges oai pmh ;

* Dans le cas des profils, il y a maintenant les formats `seda02xsd`, `seda02rng`, `seda1rng` et
  `seda2rng` ;

* Les notices d'autorités sont exposés en EAC via le format `eac`.


RDF :

* Utilisation d'URL pérenne dans les exports RDF, i.e. n'incluant pas d'élément possiblement
  changeant de l'entité, et si possible en se basant sur l'identifiant ark.


**0.12**

Interface utilisateur :

* Optimisation pour minimiser le nombre de requêtes des pages principales (#12136865)

* Déploiement WSGI - devrait améliorer le support des requêtes concurrentes  (#12136865)

EAC :

* Séparation d'agent en une partie fonctionnelle (`OrganizationUnit` et `Agent`) et une partie
  archivistique EAC (`AuthorityRecord`) (#12140367).

SEDA :

* Amélioration de l'arbre SEDA (#12059534) :

  - drag and drop désactivé pour les anonymes

  - suppression des requêtes synchrone, ce qui devrait améliorer l'utilisabilité globale

  - tentative d'amélioration de l'affichage des hiérarchie en supprimant la marge sur les feuilles de l'arbre

* Import multiples #12205200


Interopérabilité :

* Modification du XSD exporté :
  - plus d'attribut `type` sur les éléments définis "en-ligne",
  - utilisation d'`extension` pour les éléments avec un contenu textuel et des attributs.

* Les *setspecs* OAIPMH ``agent:kind:<KIND NAME>`` ont été supprimés du fait de
  la dichotomie ``Agent`` / ``OrganizationUnit``.

* Le setSpec OAI-PMH ``agent`` a été renommée en ``organizationunit`` (incluant tous les setSpecs
  sous-jacents tels que ``organizationunit:role:control`` par exemple).

* Un setSpecs OAI-PMH ``agent`` a été introduit pour permettre de moissonner les entités de type
  ``Agent``.


**0.11.0**

Interopérabilité :

* Ajout d'un préfix 'ark:/' devant la valeur du champ 'identifier' de l'en-tête OAI-PMH, qu'il
  convient de retirer pour construire les setSpec qui eux n'ont pas changé (#11831203).

* Ajout dans le RDF d'un agent des relations hiérarchiques et d'association avec l'ontologie
  Organization du W3C (#11668412).

* Correction de l'export XSD des profils SEDA pour produire du XSD valide et non le format
  spécifique à Agape (#3606843)


Interface utilisateur :

* Charte graphique (#11754074).

* Ajout des types d'entités Collectivité (Authority) et Autorité d'assignement de nom ARK
  (ARKNameAssigningAuthority) afin de contrôler la collectivité responsable d'un agent et l'autorité
  d'assignement de nom à utiliser pour la génération des identifiants ARK (#11855091).

* Correction de l'autocomplétion pour éviter des propositions incohérentes (#11884489).

* Affichage uniquement des agents de types personnes dans la liste déroulante contact référent
  (#11867467).

* Lancement automatique de la recherche après sélection d'une proposition de l'autocomplétion
  (#11884492).

* Optimisation de l'affichage des arbres de concept sur les vocabulaire : temps d'affichage divisé
  par deux (#11884230).

* Suppression de l'action "Copier" sur les agents (#11716529).

* Correction de l'import des objets-données ou des unités documentaires SEDA (#11785516).

* Correction de l'affichage de l'arbre "Elément du profil SEDA" pour les objets données ou des
  unités documentaires (#11785524).

* Navigation plus cohérente pour les objets-données et unités documentaires des unités d'archive
  SEDA (#11557857)

* Utilisation de l'annotation comme titre des objets-données SEDA (#3471036).

* Utilisation d'un vocabulaire pour les durées de conservation SEDA (#3466081).

* Affichage correct des données contenant des accents importées via EAC (#11664020).


EAC :

* Meilleure gestion de l'import/export des paragraphes (#11987275) et des liens (#11664008) EAC.

* Import des balises <generalContext> (#3511427) et <objectXMLWrap> (#3381087).

* Import des fichiers sans éléments <authorizedForm> (#11716516).

* Nommage des fichiers exportés sur la base de l'identifiant ARK (#11664003).

* Corrections pour la validation de l'EAC exporté (#11663901).


Déploiement :

* Mise à disposition d'une recette Salt pour l'installation sur CentOS 6 ou 7, incluant la mise à
  disposition d'un entrepôt de paquets CentOS 7 (#11884390).



**0.10.0**

* affichage des (sous)-concepts sous forme d'une liste paginée plutôt qu'un arbre s'il y a plus
  de 500 concepts à afficher (#2974227, #3350215)

* amélioration de synchronisation de source depuis l'interface : aide en ligne, warning plutôt
  qu'erreur en cas de définition multi-lingues non supportée, outil pour import de thésaurus de
  taille importante (#3392144, #3349339)

* problème d'interface empêchant la liaison de concept équivalent si le vocabulaire est publié
  (#5603390)

* possibilité de mise à jour des vocabulaires contrôlés publiés : possibilité d'ajout de nouveaux
  concepts et d'ajout / suppression de libellés (#11578206)

* import des balises EAC mandates et des sous-balises mandate (#3381084)

* import des balises EAC occupations et des sous-balises occupation (#3381034)

* export au format XML EAC des fiches agents (#3239716)

* état des lieux des balises non implémentés du schéma EAC (#11543984)

* changement de la gestion des vocabulaires sources : dans l'interface, soit on sélectionne un
  vocabulaire et un champ permet de sélectionner un concept de ce vocabulaire via auto-complétion,
  soit on peut saisir du texte libre (#3512232, #3511423)

* on n'affiche pas les agents liés à des utilisateurs dans les listes déroulantes (#3384078)

* on n'affiche pas les agents non publiés dans les listes déroulantes (#3507748)

* intégration basique de la charge graphique développé pour le blog saem, dont notamment le logo
  (#11520162)

*  plus d'incohérence dans l'interface des agents quand on édite les rôles archivistiques (#3510158)

* correction fautes d'orthographe (#11544090, #11557853)

* suppression de la relation `useProfile` dans 'export RDF, on peut utiliser les *sets* OAI pour
  obtenir cette information (#3507873)

* ajout des relations chronolique en utilisant `dcterms:isReplacedBy` (partie de #3477127)

* suppression de la gestion de connecteur vers alfresco et asalae (#3478851)

* amélioration de la gestion des démonstrateurs : sentry, supervision, docker reproductible
  (#11509296)


**0.9.1**

* l'export RDF d'un agent de type service versant n'inclut plus la description complète de son
  service archive, uniquement son URL

* L'attribut foaf:type d'un agent de type contact dans l'export RDF d'un agent est bien foaf:Person

* Plus d'agent dans l'état brouillon exporté sur certains set OAI

* On ne peut plus supprimer des éléments d'un profil publié

* Corrections de plantages sur agent avec lieu sans adresse ou sur certains set OAI avec resumption
  token

* Corrections / amélioration de label

**0.9.0**

* ajout des concepts en tant que set specifiers OAI-PMH de premier niveau

  la requête `oai?verb=ListSets` renvoie maintenant des set avec le préfixe
  `concept` du type :

    * `concept`
    * `concept:in_scheme:saemref-test/000002219`

  ce dernier résultat permet de filter les concepts d'un vocabulaire
  particulier via son identifiant

* correction du problème de dates pour l'OAI-PMH : toutes les dates sont maintenant en UTC
  tant au niveau des résultats retournés que des restrictions de requête via
  `from`/`until` ; on retourne les informations de fuseaux horaires (le
  suffixe `Z` dans le cas de l'UTC).

* ajout d'attribut à la balise OAI-PMH pour la définition des espaces des noms
  notamment et du schéma de validation

* utilisation d'identifiant ARK pour les profils dans OAI-PMH

* gestion des entités supprimées dans OAI-PMH par ajout d'une balise <header status="deleted">

* web service d'attribution d'ARK (il faut être authentifié) ::

    POST /ark/
    Accept: application/json

  Exemples de réponse (JSON) ::

    [{'ark': '12345/ext-000000001'}]

    [{'error': 'This service is only accessible using POST.'}]

    [{'error': 'This service requires authentication.'}]

* le service versant et service archive associé d'un profil ne sont plus inclus dans l'export SEDA XSD
