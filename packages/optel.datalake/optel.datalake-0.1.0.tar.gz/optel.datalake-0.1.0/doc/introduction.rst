.. lac-olap_

Lac versus OLAP
===============

Les modèles traditionnels de transformation, d'analyse et d'entreposage
de données sont basées sur les technologies OLAP (Online Analytical Processing)
, une technologie développée dans les années 70 [1]_ et utilisée en masse à
partir des années 90 [18]_, [25]_. Cependant, la rigidité de ces
systèmes [3]_, [19]_, [9]_, [20]_, [21]_, [15]_ , [4]_, [13]_, le fait qu'ils
soient difficilement extensibles [12]_, [13]_, [17]_ et leurs coûts élevé de
création et d'entretient [5]_, [9]_, [14]_, [16]_, [13]_, [17]_
les rendent de moins en moins attirants pour les entreprises modernes. Aussi,
ces solutions ne sont pas adaptés pour faire face aux enjeux modernes de
traitement de données (e.g. Big Data) [20]_, [22]_, [21]_, [17]_, [25]_.
Toutefois, les technologies OLAP  permettent de fournir rapidement les données
nécessaire à la fabrication de rapports de base. Au cours des trois dernières
décennies, ces technologies ont servit et continuent de servir bon nombre
d'entreprises [25]_.

Le phénomène des données de masse (Big Data) existe, entre autre, du fait qu'une
grande part des données générées aujourd'hui, soit plus de 90 %, sont non
structurées [25]_. Les entreprises modernes font donc face au défi de pourvoir
tirer de l'information à la fois de leurs données structurées et
de celles qui ne le sont pas [25]_. Les technologies existantes
permettant de relevé ce défi sont regroupées sous le terme Lac de données
(Data Lake) [6]_, [7]_, [25]_. Ces technologies donnent une plus grande
flexibilité aux entreprises en ce qui concernent les choix qui se présentent à
eux, à la fois pour analyser et entreposer leurs données [15]_, [4]_, [24]_.
Aussi, elles permettent de faire face à de grande quantité de donnée, sont
facilement extensibles [4]_, [23]_ et plus abordables [24]_, [25]_.

Cependant, puisque les entreprises disposent souvent d'entrepôts de données
basées sur des technologies OLAP, une solution hybride, qui récupère les données
existantes (cubes, entrepôts) et tire profit des avancées technologies
(e.g. Spark [10]_ ou Hadoop [11]_) s'impose d'elle même [2]_, [15]_.

Références
----------

En Ligne
~~~~~~~~

.. [1] http://olap.com/learn-bi-olap/olap-business-intelligence-history/
.. [2] https://www.softwareadvice.com/resources/olap-data-warehouse-alternatives/
.. [3] https://www.connexica.com/2016/04/are-olap-cubes-an-outdated-technology/
.. [4] https://www.sisense.com/blog/white-elephant-named-olap/
.. [5] https://www.connexica.com/2016/04/are-olap-cubes-an-outdated-technology/
.. [6] https://www.searchtechnologies.com/blog/search-data-lake-with-big-data
.. [7] http://www.martinsights.com/?p=1094
.. [9] https://www.yurbi.com/blog/considering-olap-vs-oltp-3-things-to-know/
.. [10] https://spark.apache.org/
.. [11] http://hadoop.apache.org/
.. [12] http://data-informed.com/htap-what-it-is-and-why-it-matters/
.. [13] https://blog.westmonroepartners.com/is-data-warehousing-really-dead/
.. [14] http://searchcio.techtarget.com/feature/Data-lake-governance-A-big-data-do-or-die
.. [15] https://knowledgent.com/whitepaper/design-successful-data-lake/
.. [16] https://www.solverglobal.com/blog/2014/04/data-warehouse-vs-olap-cube/
.. [17] http://www1.memsql.com/rs/461-ZPB-764/images/Building_Real-Time_Data_Platforms_MemSQL.pdf
.. [18] http://eng.localytics.com/spark-passing-data-platform-gravestones/
.. [19] http://www.itprotoday.com/microsoft-sql-server/4-darn-good-reasons-not-building-cubes-transactional-systems
.. [20] https://www.softwareadvice.com/resources/data-warehouse-problems/
.. [21] https://www.zoomdata.com/blog/your-organization-using-outdated-technology/
.. [22] http://labs.sogeti.com/data-warehouse-obsolete/
.. [23] https://insidebigdata.com/2017/03/06/realizing-a-scalable-data-lake/
.. [24] http://usblogs.pwc.com/emerging-technology/data-lakes-and-the-promise-of-unsiloed-data/

Livres
~~~~~~

.. [25] John, T. (2017). Data Lake for Enterprises. Packt Publishing. Retrieved from https://www.packtpub.com/mapt/book/big_data_and_business_intelligence/9781787281349
