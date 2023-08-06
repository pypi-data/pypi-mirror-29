Dataproc cluster
================

Aucun développeur n'a accès à l'amas Dataproc sur Google Cloud. Tous les travaux
qui sont exécutés et publiés, autant dans l'environnement de développement que
celui de production, le sont à partir d'un `gitlab-runnner`.


Création de l'amas
------------------

Pour créer un amas ``Dataproc`` sur Google Cloud, il suffit d'exécuter
le script ``dataproc.sh``:

.. code-block:: console

   sh ./deployment/dataproc.sh


Ce script crée l'amas et au final appelle ``provision-gc.sh`` pour provisionner
les machines. Les paramètres de création de l'amas (e.g. nombre de machines, cpu,
fichiers d'initialisation ect...) sont explicitement statués dans le fichier
``create-cluster.sh``.

.. note::

   L'amas Dataproc de google est installé par défault avec open-jdk. Pour des
   raisons encore inconnues, les machine de l'amas utilisant cette version de
   Java ne peuvent communiquer avec nos serveur SQL locaux. Lors de
   l'installation, nous installons la version d'Oracle de Java et configurons
   l'application Spark pour utiliser cette version.


Exécution automatique des travaux
---------------------------------

Une fois qu'un travail développé dans la raffinerie est publié
sur une branche `dev` ou `master`, un `gitlab runner` se charge de
lancer le travail sur l'amas (cluster) Dataproc sur Google Cloud.

La création d'un `gitlab runner` est effectuée avec la commande suivante:

.. code-block:: console

   sh ./deployment/gitlab-runner.sh

La configuration du `gitlab runner` nécessaire à l'exécution
des travaux se trouve dans le fichier `deployment/gitlab-runner.sh`.
Ce script crée le runner et le configure selon le contenu du fichier
`deployment/provision-gitlab-runner.sh`
