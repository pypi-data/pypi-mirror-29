===================================
Modèle de sécurité de l'application
===================================

Accès anonyme
-------------

Par défaut, l'application est installée en autorisant l'accès aux données sans avoir à
s'authentifier. Les utilisateurs anonymes peuvent voir toutes les données métiers mais ne peuvent
rien modifier.

Il est possible de supprimer l'accès anonyme en commentant les options ``anonymous-user`` et
``anonymous-password`` du fichier ``all-in-one.conf`` de l'instance. Attention, il faut synchroniser
l'utilisateur associé à ses options dans la base de données si vous souhaitez les modifier.


Utilisateurs "standards"
------------------------

.. warning::

  Hormis l'utilisateur dédié aux accès anonymes (en général "anon"), tous les utilisateurs doivent
  être dans le groupe "utilisateurs". De plus pour le bon fonctionnement de certain aspects métier,
  il faut les rattacher à une autorité administrative.

Un utilisateur standard (dans le groupe 'utilisateurs'), rattaché à une organisation, peut :

* ajouter et mettre à jour des notices d'autorité, des profils SEDA ;

* ajouter et mettre à jour des concepts dans des vocabulaires SKOS existants ;

* ajouter et mettre à jour des agents et unités d'organisation appartenant à la
  même autorité administrative que lui (ce qui inclut la sélection des profils
  et vocabulaires liés à une unité d'organisation).


Administrateurs
---------------

Les utilisateurs qui sont ajoutés dans le groupe "administrateurs" ont des droits supplémentaires
sur la plate-forme, notamment :

* ajouter et modifier des utilisateurs ;

* ajouter et modifier des autorités d'assignement de noms (**ARK NAA**), des
  autorités administratives et des vocabulaires.

Les actions spécifiques à l'administrateur sont accessibles dans l'interface web via la section
"Administration" de la page d'accueil une fois authentifié.
