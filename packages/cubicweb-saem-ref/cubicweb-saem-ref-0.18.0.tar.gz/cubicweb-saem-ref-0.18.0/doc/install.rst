============
Installation
============

Pour installer le référentiel, plusieurs moyens sont à votre disposition :

* en utilisant pip_ ;

* en utilisant la formule Salt_.

Ces différentes options sont décrites dans les sections suivantes. La formule Salt effectue une
installation destinée à la production : elle automatise la création de l'application avec une
instance dédiée au point d'accès OAI-PMH.


Installation avec pip
=====================


Configuration du serveur PostgreSQL
-----------------------------------

Si vous n'en n'avez pas encore un disponible, il faut commencer par installer un serveur PostgreSQL
(pas nécessairement sur la même machine que le réferentiel). Sur une distribution Red-Hat / CentOS,
il faut commencer par installer les paquets suivants :

::

    yum install postgresql94-contrib
    yum install postgresql94-plpython
    yum install postgresql94-server
    yum install mailcap # pour /etc/mime.types

Créer et démarrer un *cluster* PostgreSQL

::

    service postgresql-9.4 initdb
    service postgresql-9.4 start

En tant qu'utilisateur ``postgres`` (par exemple ``su - postgres``),
créer un nouveau compte d'accès à Postgres :

::

    createuser --superuser --login --pwprompt cubicweb

De retour en ``root``, éditer le fichier ``/var/lib/pgsql/9.4/data/pg_hba.conf``
pour donner les droits d'accès à l'utilisateurs ``cubicweb`` fraichement créé :

::

    local   all   cubicweb    md5


.. warning::

    L'ordre des directives de ce fichier est important. La directive concernant
    l'utilisateur ``cubicweb`` doit précéder celles déjà présentes dans le
    fichier. Dans le cas contraire, elle sera ignorée.

Enfin, on relance PostgreSQL pour qu'il prenne en compte les modifications :

::

    service postgresql-9.4 reload

Pour s'assurer du bon fonctionnement de PostgreSQL et du rôle ``cubicweb``, la
commande suivante doit afficher le contenu du *cluster* sans erreur :

::

    psql -U cubicweb -l


Installation du référentiel
---------------------------

Nous recommandons d'installer le code du référentiel avec un utilisateur
standard (pas *root*) :

::

    adduser saemref
    su - saemref

et dans un virtualenv_, qu'il convient donc de créer puis d'activer :

::

    virtualenv saemref-venv
    . saemref-venv/bin/activate

Par la suite, nous supposerons que vous tapez les commandes indiquées en tant qu'utilisateur
`saemref` et avec le *virtualenv* activé.

Installer le référentiel :

::

    pip install cubicweb-saem-ref


Création de l'instance
----------------------

Une fois le cube saem_ref et ses dépendances installées, il reste à créer une
instance de celui-ci :

::

  CW_MODE=user cubicweb-ctl create saem_ref saemref

.. note ::

    La phase finale de création prend quelques minutes, afin de remplir la base
    avec quelques données nécessaires au bon fonctionnement de l'application.

* Laisser le choix par défaut à toutes les questions ;

* Choisir un login / mot de passe administrateur sécurisé (admin/admin est une
  mauvaise idée, nous recommandons d'installer le paquet ``pwgen`` et de
  générer un mot de passe aléatoire avec la commande ``pwgen 20``).

Selon votre configuration postgres, vous pouvez avoir à modifier le fichier sources pour y spécifier
les informations de connexion au serveur (hôte, port, utilisateur et mot de passe). Le plus simple
est de répondre non à la question "Run db-create to create the system database ?", d'éditer le
fichier `~/etc/cubicweb.d/saemref/sources` puis de reprendre le processus d'initialisation en
tapant :

::

  CW_MODE=user cubicweb-ctl db-create saemref

Vous pouvez maintenant lancer l'instance :

::

  CW_MODE=user cubicweb-ctl pyramid saemref

L'instance est désormais lancée et disponible sur le port 8080.

Pour une instance de production, il est recommandé d'utilisé un serveur d'application WSGI tel que
`gunicorn`_ et un superviseur tel que `supervisor`_.


Installation avec Salt
======================

Une `formule Salt`_ est à votre disposition pour installer le référentiel.

L'usage recommandé est le suivant, en supposant que l'identifiant du minion est 'srv' :


`/srv/salt/top.sls`::

    base:
        'srv':
            - saemref
            - saemref.supervisor


`/srv/pillar/top.sls`::

    base:
        'srv':
            - saemref


`/srv/pillar/saemref.sls`: voir le fichier `pillar.example`_


Pour la première installation, il faut d'abord créer la base de données (**cela détruira la base de
données déjà existante le cas échéant**) en exécutant :

::

   salt srv state.sls db-create

Pour finir l'installation puis lancer l'application, exécuter :

::

    salt srv state.highstate
    ssh saemref@srv supervisorctl start saemref saemref-oai

La formule installe deux instances : une qui servira le point d'accès OAI-PMH, et l'autre toutes les
autres requêtes. On veut en général un frontal qui routera les différentes requêtes sur l'instance
qui va bien. Ci-dessous un exemple de configuration pour nginx :

::

    server {
        listen 80;
        server_name saemref.example.com;
        location / {
            proxy_pass http://srv:8080;
        }
        location /oai {
            proxy_pass http://srv:8081;
        }
    }


Installation du frontal web
===========================

L'installation d'un frontal web (en général Apache ou Nginx) n'est pas géré par
la recette, car cela dépend fortement de l'environnement cible. Il est cependant
important de noter que si vous souhaitez que le référentiel soit installé
derrière un 'préfixe' (e.g. "http://demo.net/referentiel" plutôt que
"http://referentiel.demo.net/"), il est important de transmettre cette
information au référentiel via la variable "SCRIPT_NAME". Ci-dessous un exemple
pour le cas d'Apache : ::

    <Location /saem-demo/>
        RequestHeader set Host "demo.logilab.fr/saem-demo"
        SetEnv SCRIPT_NAME /saem-demo
        ProxyPassReverse "http://172.1.1.1:8084/"
        ProxyPass "http://172.1.1.1:8084/"
    </Location>


Mise à jour de l'instance
=========================

.. warning::

  Il y aura donc une interruption de service pendant cette opération

Lors qu'une nouvelle version est livrée, il faut commencer par mettre à jour le code de
l'application. Le plus simple pour cela est de supprimer le *virtualenv* et de le recréer. Si vous
avez installé le référentiel avec pip :

::

    # Ctrl-C pour couper l'instance qui tourne
    rm -rf saemref-venv
    virtualenv saemref-venv
    . saemref-venv/bin/activate
    pip install cubicweb_saem-ref

Puis il reste à mettre à jour l'instance CubicWeb. Pour une installation avec pip :

::

    CW_MODE=USER cubicweb-ctl upgrade saemref
    CW_MODE=USER cubicweb-ctl pyramid saemref


Si vous avez installé le référentiel avec la formule Salt, connectez vous sur le minion en tant que *root* puis :

::

    [root@minion] % supervisorctl stop all
    [root@minion] % salt-call state.sls saemref.install pillar='{"upgrade": true}'
    # soyez patient...
    [root@minion] % su - saemref
    [saemref@minion] % . venv/bin/activate
    (venv) [saemref@minion] % cubicweb-ctl upgrade saemref
    # répondre 'yes' aux questions
    (venv) [saemref@minion] % exit
    [root@minion] % supervisorctl start all

Dans les deux cas, la commande `cubicweb-ctl upgrade` pose un certain nombre de questions,
auxquelles il faut toujours répondre par oui (en tapant 'y' ou Entrée directement). Un backup de la
base de données est effectué avant la migration afin de pouvoir rejouer une migration en cas de
problème.

.. _pip: https://pip.pypa.io/
.. _virtualenv: https://virtualenv.pypa.io/
.. _gunicorn: http://gunicorn.org/
.. _supervisor: http://supervisord.org/
.. _Salt: https://saltstack.com/
.. _`formule Salt`: https://github.com/logilab/saemref-formula
.. _`pillar.example`: https://github.com/logilab/saemref-formula/blob/master/test/pillar/example.sls


Lancement de l'instance en mode debug
=====================================

Pour comprendre certains problèmes, il peut-être utile de lancer l'instance en mode "debug" afin d'augmenter le niveau de détails des *logs*. Pour cela, il faut mettre : ::

    log-threshold=DEBUG

dans le fichier ``~saemref/etc/cubicweb.d/saemref/all-in-one.conf`` puis relancer l'instance : ::

    [root@minion] % supervisorctl restart all
