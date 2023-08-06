==============
Optel Datalake
==============


|build_badge| |cov_badge| |lic_badge| |py_badge|


Quelques liens utiles


    * `Fichiers sources sur Gitlab`_
    * `Récente documentation`_
    * `À faire sur Jira`_
    * `Couverture de tests`_


.. _Couverture de tests: _static/coverage_html/index.html

.. |build_badge| image:: https://vcs.optelgroup.com/btech/bi/data-refninery/datalake/badges/master/pipeline.svg
    :target: https://vcs.optelgroup.com/btech/bi/data-refinery/datalake/pipelines
    :alt: Build Status

.. |cov_badge| image:: https://vcs.optelgroup.com/btech/bi/data-refinery/datalake/badges/master/coverage.svg
    :target: https://vcs.optelgroup.com/btech/bi/data-refinery/datalake/pipelines
    :alt: Coverage Report

.. |lic_badge| image:: https://img.shields.io/badge/license-proprietary-orange.svg
    :target: https://www.optelgroup.com/
    :alt: GNU Lesser General Public License v3

.. |py_badge| image:: https://img.shields.io/badge/python-3.6-blue.svg
    :target: https://www.python.org/downloads/release/python-36
    :alt: Python version


.. _Fichiers sources sur Gitlab: https://vcs.optelgroup.com/btech/bi/data-refinery/datalake
.. _Récente documentation: http://btechdoc.optelgroup.com/static/docfiles/datalake/master/index.html
.. _À faire sur Jira: https://jira.optelgroup.com/projects/BTECH/issues

Ce projet héberge l'information globale sur la raffinerie de donnés Optel, ainsi
que le code réutilisable (boîtes à outils) qui peut servir à plusieurs
travaux dans la raffinerie.



Introduction au concept de lac de données
=========================================

.. toctree::
    :maxdepth: 2

    Lac versus OLAP <introduction.rst>
    Architecture du lac Optel <architecture-optel.rst>
    Dévelopment TDD basé sur les données <tdd.rst>
    Raffinerie de données <refinery.rst>



Utilisation
===========

.. toctree::
   :maxdepth: 2

   Installation <install.rst>
   Utilisation <usage.rst>
   Documentation des modules <modules.rst>

Développement
=============

.. toctree::
   :maxdepth: 2

    Développement dans ce package <devel.rst>
    Développement d'un travail <devel-job.rst>


Administration systèmes
=======================

.. toctree::
   :maxdepth: 2

       Dataproc cluster <cluster.rst>
