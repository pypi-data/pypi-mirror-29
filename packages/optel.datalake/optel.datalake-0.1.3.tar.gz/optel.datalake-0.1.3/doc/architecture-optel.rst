Architecture du lac de données Optel et son infrastructure
==========================================================

Infrastructure
--------------

L'infrastructure du lac de données est entièrement basée sur des
technologies issues de l'infonuagique (Cloud Computing). L'idée de
base étant de fournir aux analystes des composantes qui pourront
croître facilement avec l'entreprise (Scalability).

.. graphviz:: optel-infra.dot



Entrepôt de données original (GC Bucket)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les données originales de l'entreprise sont déposées dans un endroit
sécurisé et peu dispendieux, qui peut croître à la demande (Bucket GC).
Cet entrepôt peut facilement être connecté aux ordinateurs de calcul et
est persistant.


Amas de calcul (Dataproc Calculation Cluster)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le lac de données utilise un amas (cluster) Dataproc de Google. Cet
amas est déployé de façon automatique à l'aide d'un simple script en shell.
Les calculs sont effectués en mémoire et en parallèle, à l'aide de la
technologie Apache Spark. Les connecteurs pour accéder au données
originale présentes dans l'entrepôt original (Bucket) sont incluses
par défaut avec le service Dataproc.

Il est donc très simple de charger des données de l'entrepôt original
et d'effectuer des calculs sur l'amas Dataproc.


Entrepôt de service (Data Hub)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

L'entrepôt de service est constitué d'un amas Elastic Stack et l'ajout
d'un amas sql PostgreSQL est planifié.

Composantes du lac
------------------

Le découpage du lac de données d'Optel suit le modèle suivant:

.. graphviz:: optel-structure.dot



Ingestion (Intake)
~~~~~~~~~~~~~~~~~~

La partie ingestion comprend toutes manipulation destinées à
obtenir des données. Différents connecteurs peuvent
être utilisé pour charger des données provenant de diverses
sources, comme par exemples, des base de données, des logs
ou des serveur de fichiers.

Zone d'origine (raw zone)
+++++++++++++++++++++++++

La zone d'orgine contient des donnée très peu transformées. Ces données
sont tirées d'une ou plusieurs sources et sont par la suite
grossièrement nettoyées et ingérées. Pour un exemple concret
d'ingestion de données dans cette zone, voir ...

Les principales fonctions de cette zone sont les suivantes:

* Recevoir les données nouvellement créées, de façon incrémentale ou non.
* S'assurer que les données sont bien reçues.
* S'assurer qu'un nettoyage minimal est fait, comme
  par exemple enlever les colonnes ou les lignes vides)

Cette zone est utilisée pour récolter les données et les découpler des systèmes
de production. Elle sert aussi à fournir une vue sur la source des données
qui entrent dans le lac. Les données stockées dans cette zone doivent être
nettoyées et enrichies avant d'être utilisées.

Intégration (Data Integration)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La partie intégration est un des endroits où des transformations importantes
on lieu. Les principales fonctions de cette partie sont:

* Profilage
* Nettoyage
* Transformations
* Validation de la qualité

Les données issues de la partie d'intégration sont des données qui ne
ressemblent pas aux données originales (zone d'origine). Elles ont subit
une multitude de transformations et sont passées par différents modèles
de validation.

Transformations
+++++++++++++++

Les transformations visent d'abord et avant à fournir des données
avec l'objectif de répondre à une question précise. La question doit
être bien définie avant d'entamer l'écriture du code qui transformera
les données.

Profilage
+++++++++

Le profilage est une étape qui décrit sommairement les données pour
y détecter, par exemple, des anomalies. Une simple passe de statistique
descriptive est un bon départ.

Nettoyage
+++++++++

Garder un jeu de données propre doit faire partie des préocupations
de l'analyse, à toute les étapes. Des colonnes vides, ou avec un grand
nombre de valeurs manquantes ne devrait jamais être accepté.

Validation de la qualité
++++++++++++++++++++++++

La validation de la qualité des données est une étape essentielle
visant à corroborer les résultats obtenus (après transformations/nettoyage)
avec des données connues. Idéalement, un jeu de données connues est
produit, avec l'aide du client, contenant des valeurs reconnues pour
être justes et qui ne varierons pas dans le temps.


Entrepôts de données (Processed Data Stores)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Une fois les transformations réalisées, le nettoyage et la validation faites,
les données résultantes sont transférées dans un ou des entrepôts de données
(Processed Data Stores).


Références
----------
