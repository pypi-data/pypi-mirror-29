Export des profils SEDA
=======================

Selon leurs caractéristiques, les profils créés dans l'application sont exportable dans une ou
plusieurs versions du SEDA_ (2, 1 ou 0.2) au format RelaxNG_, celui-ci étant plus adapté à la
génération de profil que les `schémas XML`_.

Les versions supportées sont indiquées dans l'onglet 'diagnostic' du transfert.

Il est important de noter que quelque soit la version utilisée, le profil seul n'est pas suffisant
pour valider un bordereau. Il faut également valider ce dernier contre le schéma XSD de la version
correspondante, car elle permet de valider certains aspects qui ne seront pas validés par le profil.

.. _SEDA: https://redirect.francearchives.fr/seda/
.. _RelaxNG: http://relaxng.org/
.. _`schémas XML`: https://www.w3.org/XML/Schema

Limitation des schémas RelaxNG
------------------------------

Les profils autorisants plusieurs éléments de même nom à un même niveau avec
plus d'un d'entre eux ayant une cardinalité différente de 1 vont générer des
schémas RelaxNG valides mais invérifiables par les validateurs existants
(`Jing`_ par exemple). Une solution technique reste à trouver pour ce
problème. Les profils dans ce cas peuvent être identifiés à l'export à l'aide de
l'attribut `seda:warnings` ([1]_) sur la balise racine (`rng:grammar` ou
`xsd:schema` selon le format choisi) qui contiendra la chaîne 'rng-ambiguous'
dans ce cas.

.. _Jing: http://www.thaiopensource.com/relaxng/jing.html
.. [1] le préfix `seda` étant associé à l'espace de nom
   "fr:gouv:culture:archivesdefrance:seda:v2.0"


Identification des éléments
---------------------------

Afin de faciliter l'éventuel travail d'une application cliente, des identifiants
sont exportés pour les différents éléments répétables du profil (e.g. unité
d'archive, objet-données, mot-clé, etc.) via l'attribut standard `xml:id`.


Export SEDA 2
-------------

Gestion des identifiants et références
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Les identifiants spécifiés dans l'interface utilisateur sur les objets-données et les unités
d'archives sont reportés via un attribut `xml:id` sur l'élément correspond dans le profil
RelaxNG_ généré. La valeur de cette attribut est ensuite utilisée comme valeur par défaut des
éléments référençant cet élément.

Ce mécanisme permet de gérer des identifiants pour des éléments XSD qui ne sont
pas encore créés (puisqu'ils le seront à la création du bordereau), ce qui est
nécessaire pour pouvoir ensuite les référencer, la norme SEDA 2 faisant
largement usage de telles références. Il est à noter qu'il est donc à la
responsabilité de l'outil qui génère le bordereau de gérer les définitions de
références ainsi créées en substituant dans les éléments référencés la valeur de
l'identifiant qu'il a attribué à l'élément portant le `xml:id`
correspondant.

Ceci n'étant pas un mécanisme standard de RelaxNG_, la cohérence des références entre
le bordereau et le profil ne sera pas vérifiée par les outils de validation XSD
classiques.


Autres limitations
~~~~~~~~~~~~~~~~~~

Il est à noter que les références sont exportées en utilisant le type `NCName` et non `IDREF` comme
dans le schéma XSD : c'est lié au fait qu'il n'est pas autorisé en RelaxNG_ d'utiliser le type
`IDREF` pour le contenu texte d'une balise, mais uniquement pour le contenu d'un attribut : ::

  <reference>id référencé</reference>

versus : ::

  <reference idref="id référencé"/>


Export SEDA 0.2 et 1
--------------------

Les schémas des versions 0.2 et 1 de la norme SEDA utilisent des types personnalisés venant de
différents espaces de nom (par exemple
`fr:gouv:culture:archivesdefrance:seda:v1.0:QualifiedDataType:1`,
`urn:un:unece:uncefact:data:standard:UnqualifiedDataType:10`, etc.). Ces types ne sont
malheureusement pas utilisables dans un schéma RelaxNG, uniquement XSD. Pour palier à ce problème,
les éléments utilisant ces types sont exportés en tant que simple chaîne de caractères "xsd:string",
en supposant que les transferts seront validés contre le profil *et* contre le schéma XSD de la
norme. La même stratégie était utilisée par Agape V1.

Le SEDA 2 n'utilise plus ces types et n'est donc pas exposé à ce problème.
