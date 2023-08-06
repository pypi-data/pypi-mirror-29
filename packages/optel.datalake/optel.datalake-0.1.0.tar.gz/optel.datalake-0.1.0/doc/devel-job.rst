==========================
Développement d'un travail
==========================

Pour développer un nouveau travail, un définition claire et documenté
de ce que le client veut (e.g. KPI, dashboard, rapports ect...). Une fois
le besoin bien défini, un dépôt git doit être créé, dans le groupe
``BI/data-refinery``.

.. note::

   Ultimement, un `cookie-cutter`_ sera développé pour jeter les bases
   d'un nouveau projet.

Le nouveau travail développé (les fichiers python) doivent être déposés
dans le répertoire portant le nom du rapport.

.. _cookie-cutter: https://github.com/audreyr/cookiecutter


Étapes du développement
=======================

Ingestion
---------

L'ingestion est la première étape de l'exécution d'un travail.
Cette étape charge simplement les données requises et les transfère
dans le lac (bucket Google Cloud). Voir ``example/intake.py`` pour
un exemple de travail d'ingestion.

Intégration
-----------

L'intégration est le coeur du travail de la raffinerie de données, c'est
l'étape qui transforme les données et mène à un résultat qui pourra
être utilisé pour la présentation.


Atelier
=======

Pour cet atelier, nous utiliserons le projet example-job. Clôner ce dépôt:

.. code-block:: console

   git clone git@vcs.optelgroup.com:btech/bi/data-refinery/example-job.git

Utilisez le même environnement virtuel que vous avez mis en place pour lors
de l'instalation de ``datalake``.

Créer une nouvelle branche de travail:

.. code-block:: console

   git checkout -b your-branch


Installer le package (facilite l'implémentation des tests).

.. code-block:: console

   cd example-job
   pip install --editable .


But
---

* Convertir la colonne ``Amount``, que l'on sait être en US, en CAD. Le taux de conversion est 0.78.
* Présenter une table finale qui donnera la somme des montants en CAD, par années, départements et pays.


Méthode
-------

Utiliser du TDD pour coder les fonctions qui vous permettra de faire passer les tests.


* Tentez d'imaginer à quoi pourrait ressembler la table finale.
* Identifier les fonctions Spark que vous pensez avoir besoin.
   Vous pouvez consulter `la doc de pyspark`_
* Commencer par la fonction de conversion en CAD


.. _la doc de pyspark: http://spark.apache.org/docs/2.1.0/api/python/pyspark.sql.html#pyspark.sql.DataFrame.groupBy
