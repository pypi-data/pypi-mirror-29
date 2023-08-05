Services Web spécifiques
========================

Authentification
----------------

L'authentification est effectuée en envoyant des requêtes signées à CubicWeb. Il faut commencer par
créer un jeton d'authentification pour l'utilisateur en question, et sauvegarder l'identifiant et le
secret du jeton quelque-part.

La création du jeton se fait via l'action "profil" du menu utilisateur, puis en cliquant sur
l'action "add token" du sous-menu "ajouter" de la boite d'actions.

Sur la base de cet identifiant et secret du jeton, on authentifie une requête HTTP en ajoutant
dans les en-têtes :

* ``Content-MD5``: le hash MD5 du corps de la requête

* ``Date``: la date d'émission de la requête au format '%a, %d %b %Y %H:%M:%S GMT' (heure GMT donc)

* ``Authorization``: 'Cubicweb <token-id>:<signature>' avec <token-id> l'identifiant du jeton et
  <signature> une signature HMAC (RFC 2104) de la concaténation :

  * du verbe HTTP ('GET', 'POST', etc),
  * de l'URL,
  * des en-têtes HTTP ``Content-MD5``, ``Content-Type`` et ``Date``,

  en utilisant le secret.

À noter qu'il est important que l'heure du client et serveur soient synchronisées. Il est donc
recommandé d'utiliser un serveur NTP_ sur chaque machine.

.. _NTP: https://fr.wikipedia.org/wiki/Network_Time_Protocol

Listes des services
-------------------

Pour obtenir les données au format RDF XML, il convient de positionner l'en-tête HTTP ``Accept``
pour la négociation de contenu.

Description des vocabulaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Liste des jeux de données au format RDF SKOS (XML) ::

    GET /conceptscheme
    Accept: application/rdf+xml

Description complète du jeu de données au format RDF SKOS (XML) ::

    GET /conceptscheme/<eid>
    Accept: application/rdf+xml


Description des services archives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Liste des services d'archives avec leur services versants ::

    GET /archival-units
    Accept: application/json

Exemple de réponse : ::

    [
        {
            "ark": "23578/ou000190053",
            "name": "Gironde. Archives départementales",
            "state": "published",
            "url": "http://orion.tls.logilab.fr:8080/ark:/0/ou000117240",
            "authority": {
                "ark": "XXX/o20",
                "name": "Test saem",
                "url": "http://orion.tls.logilab.fr:8080/ark:/XXX/o20"
            },
            "deposit-units": [
                {
                    "ark": "75548/ou000117317",
                    "name": "Cenon. service de la Commande publique",
                    "state": "published",
                    "url": "http://orion.tls.logilab.fr:8080/ark:/75548/ou000117317",
                    "authority": {
                        "ark": "XXX/o13",
                        "name": "Ville de Cenon",
                        "url": "http://orion.tls.logilab.fr:8080/ark:/XXX/o13"
                    }
                },
                {
                    "ark": "75548/ou000117342",
                    "name": "Direction du Patrimoine",
                    "state": "published",
                    "url": "http://orion.tls.logilab.fr:8080/ark:/75548/ou000117342",
                    "authority": {
                        "ark": "XXX/o19",
                        "name": "Conseil départemental",
                        "url": "http://orion.tls.logilab.fr:8080/ark:/XXX/o19"
                    }
                }
            ]
        }
    ]


Allocation d'identifiants ARK
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le point d'accès ``/ark`` permet d'obtenir un identifiant ARK à partir d'une
*autorité administrative* (collectivité) spécifié via le paramètre de requête
``organization=<identifiant ARK>``. L'identifiant d'une autorité administrative
peut être obtenu à partir des données RDF (elles-mêmes disponibles via une
requête OAI-PMH sur une unité administrative) en récupérant la valeur du champ
``dc:identifier`` (normalement une chaîne de caractères commençant par
'ark://').

Pour utiliser ce service il faut être authentifié.

Exemple de requête :

::

    POST /ark&organization=ark%3A%2F%2F12345%2Fo67
    Accept: application/json

Exemples de réponse (JSON) ::

    [{'ark': '12345/ext-000000001'}]

    [{'error': 'This service is only accessible using POST.'}]

    [{'error': 'This service requires authentication.'}]

    [{'error': 'Organization "12345/o67" cannot assign ARK identifiers.'}]

    [{'error': 'No organization matching identifier "12345/o67".'}]

    [{'error': 'Missing required "organization" query parameter.'}])


Import d'une notice d'autorité au format XML EAC
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Il est possible de poster un fichier XML EAC sur point d'accès ``/authorityrecord`` afin d'importer
la notice d'autorité qu'il décrit. Ce service renverra l'identifiant ARK de la notice importée ou
bien une erreur en cas de problème (voir les exemples ci-dessous).

Pour utiliser ce service, il faut être identifié avec le compte d'un utilisateur qui est lié à une
autorité administrative, elle-même liée à une autorité nommante.

Exemple de requête :

::

    POST /authorityrecord
    Content-Type: application/xml
    Accept: application/json

    <?xml version="1.0" encoding="UTF-8"?>
    <eac-cpf>
      <control>
      ...
    </eac-cpf>


Exemples de réponse (JSON) ::

    [{'ark': '12345/r000000042'}]

    [{'error': 'This service requires authentication.'}]

    [{'error': 'Authenticated user is not linked to an organisation,
                or his organisation has no ARK naming authority..'}]

    [{'error': u'Invalid XML file',
      'details': "Start tag expected, '<' not found, line 1, column 1"}]

    [{'error': 'Unexpected EAC data',
      'details': 'Missing tag control in XML file'}])


OAI-PMH
-------

On implémente les 6 types de requêtes (verbes) du protocole :

* GetRecord
* Identify
* ListIdentifiers
* ListMetadataFormats
* ListRecords
* ListSets

Moissonnage sélectif
~~~~~~~~~~~~~~~~~~~~

On supporte le moissonnage sélectif à l'aide des Sets_ hiérarchiques avec *a
priori* un hiérarchie à deux niveaux (pour l'instant, seul le cas des agents
est vraiment concret pour l'aspect hiérarchique).

Le premier niveau hiérarchique correspond au type d'entité sur lequel il faut
filtrer la réponse, on a 3 types de filtrage possible :

* `agent` : agents
* `organizationunit` : unités administratives
* `profile` : profils SEDA
* `conceptscheme` : vocabulaires contrôlés
* `concept` : concepts issus d'un vocabulaire contrôlé

Ainsi une requête pour obtenir la liste des identifiants des agents du
référentiel prend la forme : ``<baseurl>oai?ListIdentifiers&set=agent``

Pour le cas des unités administratives, on supporte un axe de hiérarchie :

* ``role``: les rôles archivistiques (service versant, service de contrôle, etc.)

Le prototype d'une requête avec un spécification de set hiérarchique est :

    <baseurl>oai?verb=<VERB>&set=<entity type>:<axis name>:<axis value>

Exemple de requêtes
~~~~~~~~~~~~~~~~~~~

* `ListSets`

    <baseurl>/oai?verb=ListSets

* `ListIdentifiers` avec un filtrage `set` (obligatoire dans notre cas) :

    <baseurl>oai?verb=ListIdentifiers&set=organizationunit

* `ListIdentifiers` avec filtrage hiérarchique :

    <baseurl>oai?verb=ListIdentifiers&set=organizationunit:role:deposit

* `ListRecords` avec ou sans filtrage hiérarchique :

    <baseurl>oai?verb=ListRecords&set=conceptscheme
    <baseurl>oai?verb=ListRecords&set=organizationunit:role:deposit

* `GetRecord` avec spécification de l'`identifier` (obligatoire dans notre
  cas) :

    <baseurl>oai?verb=GetRecord&identifier=ark:/01234/000004145


Moissonnage sélectif d'objets reliés à d'autres objets
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Certains Sets_ définis dans le référentiel permettent de moissonner des objets
en fonction de leur relation avec d'autres objets. C'est le cas par exemple
des concepts en fonction de leur appartenance à un vocabulaire à l'aide du set
``concept:in_scheme:<scheme identifier>`` ou encore des profils
sélectionnables par service versant à l'aide du set
``profile:transferring_agent:<agent identifier>``.

Dans ces cas, le set prend la forme :

::

    <type d'objet>:<relation>:<identifiant>

Il n'est pas possible selon la norme OAI d'utiliser des identifiants ARK pour les sets du
moissonnage sélectif car ces derniers contiennent des caractères interdits (``:`` et ``/``
notamment). Ce problème reste à résoudre à ce jour. Pour le moment, l'identifiant ARK peut-être
directement utilisé simplement en retirant le préfix "ark:/".


Format des enregistrements `record` des réponses OAI-PMH
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour les requêtes `GetRecord` et `ListRecords`, la réponse OAI-PMH contient
deux balises à l'intérieur de la (ou des) balise(s) ``<record>`` :

* la balise ``<header>``, qui contient l'`identifier` de l'enregistrement
  ainsi que sa date de modification ;
* la balise ``<metadata>`` qui contient les données de l'enregistrement dont
  le format dépend du type d'objet de la requête.

Pour les objets de type *agent* et *vocabulaire contrôlé*, la balise
``<metadata>`` contient une représentation RDF des entités. Pour les profils
SEDA, on renvoie le XSD SEDA en version 0.2.


.. _Set:
.. _Sets: http://www.openarchives.org/OAI/openarchivesprotocol.html#Set
