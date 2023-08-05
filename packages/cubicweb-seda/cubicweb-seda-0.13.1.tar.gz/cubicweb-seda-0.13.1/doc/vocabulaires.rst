Administration des vocabulaires SEDA
====================================

Le cube SEDA vient avec un certain nombre de vocabulaires utilisés pour
contrôler les valeurs possibles pour différents champs des profils. Cette
section détaille quelques points à noter à ce sujet.

Paramétrage des vocabulaires
----------------------------

Tout d'abord, le vocabulaire associé par défaut à un champ du SEDA est configuré
via des enregistrements dans la base de données, mais cela n'est pas à ce jour
configurable via l'interface Web. Dans le cas des profils complet, on peut en
configurer certains via l'onglet "vocabulaires". Dans le cas des profils
simplifiés ou des composants unités d'archives, les vocabulaires par défaut sont
utilisés et il n'est pas encore possible de faire autrement.

Le champ "type de descripteur" d'un vocabulaire permet de contrôler l'interface
de saisie des mots-clés associés à une unité d'archive, en ne rendant disponible
que les vocabulaires d'un type données en fonction du type choisie dans
l'interface.

Contrôle des valeurs entre les différents versions de SEDA
----------------------------------------------------------

Lors de l'export SEDA, la valeur à utiliser dans le cas d'un champ non
"sémantisé" (i.e. pour lequel on cherche à exporter une valeur et non une URL)
est cherchée de la manière suivante. Étant donné un concept lié, on va chercher
le libellé préféré dans la langue :

#. spécifique à la version du SEDA exportée : 'seda-2', 'seda-1', 'seda-02',
#. générique au SEDA : 'seda'
#. anglais : 'en'
#. français : 'fr'

Gestion du vocabulaire "Catégories de fichier"
----------------------------------------------

Ce vocabulaire est un peu particulier car il ne sert que dans l'interface
utilisateur. En fonction de la valeur saisie, le profil sera lié à différents
concepts correpondants pour les champs "type MIME" et "identifiant de format" du
SEDA.

La structure de ce vocabulaire est la suivante : ::

  + catégorie
   \
    + extension
     \
      + type MIME
       \
        - identifiant de format (PRONOM)

Lorsqu'une ou plusieurs valeurs sont sélectionnées pour la catégorie de fichier
d'un objet-données d'un profil, une jointure est effectuée sur le nom des type
MIME et identifiants de format sous-jacent avec les vocabulaires "types MIME" et
"formats de fichier" sélectionnés pour ce profil. Par défaut, le vocabulaire
sélectionné pour ces deux champs et le vocabulaire "Catégories de fichier" (ce
qui autorise théoriquement des valeurs supplémentaires indésirées pour chacun
des champs mais reste un choix pragmatique) et celui-ci reflêtera donc seul les
valeurs exportables.

Dans le cas d'un profil complet avec des vocabulaires spécifiques pour les
listes "types MIME" et "formats de fichier" (par exemple en utilisant les
vocabulaires dédiés "Types MIME" et/ou "Formats de fichier (PRONOM)") il
conviendra de s'assurer de la cohérence du vocabulaire "Catégories de fichier"
avec les vocabulaires sélectionnés car les valeurs exportées seront
l'intersection entre les valeurs spécifiées via la catégorie / extension du
fichier et les valeurs disponibles dans l'un ou l'autre vocabulaire.

Vocabulaires de contrôle des langues
------------------------------------

En l'état 2 vocabulaires sont fournis pour les langues : l'un correspond à la
liste ISO-639-3 et contient plus de 7000 langues ; l'autre est une restriction
de ce vocabulaire ne contenant que des langues dont le code à deux lettres est
autorisé par la version 0.2 du SEDA. Celui-ci a été construit par extraction des
codes ISO-639-3 de SEDA 1 puis filtrage sur les libellés spécifiés dans le
schéma SEDA 0.2 et insertion du code à deux lettres correspondant.

À l'issue de ce traitement automatique, les langues suivantes présentes en SEDA
0.2 n'était pas représentées dans le vocabulaire ainsi créé :

* Bihari languages
* Bokmål, Norwegian; Norwegian Bokmål
* Catalan; Valencian
* Chichewa; Chewa; Nyanja
* Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic
* Divehi; Dhivehi; Maldivian
* Dutch; Flemish
* Gaelic; Scottish Gaelic
* Greek, Modern (1453-)
* Haitian; Haitian Creole
* Interlingue; Occidental
* Kalaallisut; Greenlandic
* Kikuyu; Gikuyu
* Kirghiz; Kyrgyz
* Kuanyama; Kwanyama
* Limburgan; Limburger; Limburgish
* Luxembourgish; Letzeburgesch
* Malay
* Navajo; Navaho
* Ndebele, North; North Ndebele
* Ndebele, South; South Ndebele
* Norwegian Nynorsk; Nynorsk, Norwegian
* Ossetian; Ossetic
* Panjabi; Punjabi
* Pushto; Pashto
* Romanian; Moldavian; Moldovan
* Sichuan Yi; Nuosu
* Sinhala; Sinhalese
* Sotho, Southern
* Spanish; Castilian
* Swahili
* Uighur; Uyghur
* Volapük
* Zhuang; Chuang

Les codes pour l'espagnol et le grec moderne ont été ajoutés manuellement, les
autres ont été ignorées pour le moment.

Si vous souhaitez utiliser le vocabulaire complet, c'est possible en tapant les
commandes suivantes dans un *shell cubicweb* : ::

  rql('DELETE CS scheme_relation_type RT WHERE '
      'RT name IN ("seda_language_to", "seda_description_language_to")')
  rql('SET CS scheme_relation_type RT WHERE '
      'CS name "Langues (ISO-639-3)", '
      'RT name IN ("seda_language_to", "seda_description_language_to")')
  commit()

sachant qu'en faisant ceci vous risquez de générer des profils SEDA 0.2
invalides car utilisant des codes à deux lettres inconnus de cette version du
SEDA. Il faudrait pour palier à ce problème retirer du vocabulaire la langue
'seda-02' fournissant un code non supporté et améliorer la gestion de ce genre
d'erreur dans l'application.

