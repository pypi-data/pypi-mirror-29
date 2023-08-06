.. _install:

============
Installation
============


Installation sous Windows
==========================

L'installation pour un poste dev sous Windows consiste à installer une VM
roulant Linux sur laquelle le développeur va travailler.

Installation de VirtualBox
---------------------------

Télécharger VirtualBox pour windows.
        https://www.virtualbox.org/wiki/Downloads

Installer VirtualBox sur votre poste Windows.

Initialisation d'une machine virtuelle Linux
---------------------------------------------

Télécharger un ISO d'installation `LinuxMint`_ (ou une autre distribution de votre choix)

.. _LinuxMint: https://www.linuxmint.com/download.php

* Ouvrir VirtualBox et créer une nouvelle machine virtuelle de type Linux
  utilisant Other Linux. Donner lui 4GB de Ram et au moins 20gb d'espace disk.
  Gardez les paramètres par defaut autrement.
* Ouvrir le menu configuration de votre nouvelle machine virtuelle, aller dans
  l'onglet Système, sous-onglet Processeur et allouer 2 coeurs au minimum.
* Démarrer la VM, lorsqu'il est demandé de choisir de disque démarrage, trouver
  l'ISO de la distribution Linux.

Suivre les instructions d'installation de votre distribution.

Lorsque LinuxMint est installé sur le VM, il faut faire un peu de préparation
supplémentaire.

* Installer Git

  .. code-block:: console

    sudo apt-get install git

* Générer une clé ssh pour votre VM

  .. code-block:: console

    ssh-keygen -t rsa -C "your.email@exemple.com" -b 4096

Il faut ensuite ajouter cette clé dans votre gitlab. Connectez vous sur
`gitlab`_ , aller dans les ``settings`` de votre utilisateur, dans le  menu
``ssh keys``. Copier-coller la nouvelle clé dans le champ 'Key' puis ajouter la clé.

* Installer graphviz, pour faire de beaux graphiques.

  .. code-block:: console

    sudo apt-get install graphviz

Puis effectuer la section :ref:`install-linux`.


.. _gitlab: https://vcs.optelgroup.com/

.. _install-linux:

Installation sous Linux
========================

Initialisation d'un environnement virtuel
-----------------------------------------

Pour travailler sur ce projet, il vous faut premièrement
initialiser un environnement virtuel python avec la méthode
de votre choix. Un exemple:

* Installer virtualenv

  .. code-block:: console

   sudo apt-get install virtualenv

* Initialiser un environnement virtuel

  .. code-block:: console

   virtualenv -p python3.5 ~/.virtualenv/datalake
   source ~/.virtualenvs/datalake/bin/activate

  Pour désactiver l'environnement virtuel

  .. code-block:: console

   deactivate


Installation des dépendances
----------------------------

Pour rouler localement les tests, Spark [1]_ doit être installé. Sur Ubuntu,
l'installation peut se faire comme suit:

* S'assurer que Java est installé

  .. code-block:: console

    sudo apt-get install default-jdk


* Télécharger la dernière version de Spark
  http://spark.apache.org/downloads.html

* Désarchiver et déplacer Spark

  .. code-block:: console

    tar xzvf spark-2.0.1-bin-hadoop2.7.tgz
    mv spark-2.0.1-bin-hadoop2.7/ spark
    sudo mv spark/ /usr/lib/


* Configurer Spark

  Ajouter Spark_HOME à .bashrc

  .. code-block:: console

     export SPARK_HOME=/usr/lib/spark


* Installer les dépendances python

  .. code-block:: console

     pip install -r requirements_dev.txt

.. _installation:

Installation du package
-----------------------

Pour installer le package datalake:

.. code-block:: console

     git clone git@vcs.optelgroup.com:btech/bi/data-refinery/datalake.git
     cd datalake
     pip install --editable .

Bravo, vous-êtes maintenant prêts à développer dans la raffinerie de données
d'Optel !

Références
~~~~~~~~~~

.. [1] https://www.santoshsrinivas.com/installing-apache-spark-on-ubuntu-16-04/
