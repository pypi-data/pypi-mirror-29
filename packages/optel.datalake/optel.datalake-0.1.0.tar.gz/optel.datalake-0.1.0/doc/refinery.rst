=====================
Raffinerie de données
=====================

La raffinerie de données est un concept qui permet de visualiser
facilement les flux de transformations de données. Voir la `publication de
Kiran Donepudi <https://www.linkedin.com/pulse/data-refinery-kiran-donepudi>`_ sur le sujet.

.. image:: figures/refinery.png


Raffinerie de données Optel
===========================

La raffinerie de données Optel utilise à la base le concept de Lac de données.
Ce lac est utilisé pour regrouper les données de l'entreprise à un endroit
peu dispendieux et extensible (bucket Google Cloud). Les différents travaux dans
la raffinerie se chargent d'entreposer les données dans le lac, de les indexer,
de les nettoyer et de les transformer.

Travail (job)
   Un travail est défini comme toute les opérations nécessaires à
   la création d'un rapport. Ce rapport doit au préalable être défini
   et documenté. Une consultation avec le client doit d'abord avoir lieu.
   La figure suivant illustre ce que nous considérons comme être un travail.

   .. graphviz:: jobs.dot

   Un travail a donc un cycle de vie propre à lui même, avec son propre
   dépôt git, son propre scheme de versionnement et sa propre documentation.

Exécution d'un travail
   Tous les travaux effectués dans la raffinerie se passent exclusivement dans
   une ferme de calcul, un amas Dataproc [1]_ sur Google Cloud.

   .. graphviz:: workflow.dot


Références
==========

.. [1] https://cloud.google.com/dataproc/?utm_source=google&utm_medium=cpc&utm_campaign=na-CA-all-en-dr-skws-all-all-trial-e-dr-1003905&utm_content=text-ad-none-any-DEV_c-CRE_248610853853-ADGP_Hybrid+%7C+AW+SEM+%7C+SKWS+%7C+EXA+~+Dataproc-KWID_43700029902768301-kwd-463390531167&utm_term=KW_dataproc-ST_Dataproc&gclid=EAIaIQobChMIjaObuY3G2QIV0rXACh2dYw-FEAAYASAAEgLSWvD_BwE&dclid=CMO4ibqNxtkCFQG4yAodsisBYg
