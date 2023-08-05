Gestion de configuration
------------------------

Le référentiel SAEM est construit sur le cadre applicatif CubicWeb_. À ce titre, c'est un composant
CubicWeb, dont la structure générale est décrite ici_.

Il s'appuie sur les composants logiciels suivants :

* le cadre applicatif CubicWeb_ lui-même (>= 3.24) ;

* `cubicweb-saem_ref`_, l'application référentiel proprement dite, agrégeant les différents composants
  ci-dessous ;

* `cubicweb-seda`_, cube implémentant le modèle de données SEDA 2, complet et simplifié, ainsi que
  les fonctions d'export ;

* `cubicweb-eac`_, cube implémentant le modèle de données EAC, et permettant notamment d'importer
  puis de réexporter les notices d'autorités ;

* `cubicweb-skos`_, cube implémentant le modèle de données SKOS, et permettant notamment d'importer
  puis de réexporter des vocabulaires au format SKOS_ pour la gestion des thésaurus et autres
  vocabulaires contrôlés;

* `cubicweb-oaipmh`_ , cube implémentant un serveur OAI-PMH ;

* `cubicweb-signedrequest`_ , cube permettant d'authentifier les requêtes HTTP d'accès aux
  différents web service.


Pour faire fonctionner une instance, vous aurez également besoin de :

* psycopg2, bibliothèque pour l'accès aux bases de données Postgresql ;

* rdflib (>= 4.1), bibliothèque pour la manipulation de données RDF en Python, utilisée notamment
  pour l'import de fichier SKOS.


Enfin, une `formule Salt pour le déploiement`_ et un `client en ligne de commande d'accès aux
services web`_ sont disponibles.


.. _CubicWeb: https://cubicweb.org
.. _ici: http://cubicweb.readthedocs.io/en/3.24/book/devrepo/cubes/layout/

.. _`cubicweb-saem_ref`: https://www.cubicweb.org/project/cubicweb-saem_ref
.. _`cubicweb-seda`: https://www.cubicweb.org/project/cubicweb-seda
.. _`cubicweb-eac`: https://www.cubicweb.org/project/cubicweb-eac
.. _`cubicweb-skos`: https://www.cubicweb.org/project/cubicweb-skos
.. _`cubicweb-signedrequest`: https://www.cubicweb.org/project/cubicweb-signedrequest
.. _`cubicweb-oaipmh`: https://www.cubicweb.org/project/cubicweb-oaipmh

.. _SKOS: https://fr.m.wikipedia.org/wiki/Simple_Knowledge_Organization_System


.. _`formule Salt pour le déploiement`: https://framagit.org/saemproject/saemref-formula
.. _`client en ligne de commande d'accès aux services web`: https://framagit.org/saemproject/saem-client/