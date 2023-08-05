Implémentation de la norme SEDA 2
=================================

Éléments non supportés
----------------------

Le modèle de données implémenté ne supporte pas l'intégralité du SEDA 2. Certains éléments sont
simplifiés, d'autres non supportés.

Les éléments non supportés sont les suivants :

* groupes d'objets (`DataObjectGroupId`, `DataObjectGroupReferenceId`),

* métadonnées étendues des objets-données (`Metadata`, `OtherMetadata`),

* référence à des profils ou unités d'archives (`ArchivalProfile`,  `ArchiveUnitProfile`),

* `Signature` sous la balise `Content`,

Enfin, il n'y a pas pour le moment de pas de possibilité d'étendre le modèle comme le prévoit le
SEDA 2 (c.f. les éléments `ArchiveUnitReferenceAbstract`, `ObjectGroupExtenstionAbstract`,
`OtherManagementAbstract`, `OtherCoreTechnicalMetadataAbstract`, `OtherDimensionsAbstract`,
`OtherCodeListAbstract` du `schéma XSD`_)

.. _`schéma XSD`: https://redirect.francearchives.fr/seda/seda_v2-0.zip


Référence vers des notices d'autorités et vers des vocabulaires
---------------------------------------------------------------

Dans une approche "référentiel" inspirée du `référentiel SAEM`_, un certain nombre d'éléments sont
implémentés via des références vers des notices d'autorité EAC ou des concepts de vocabulaires SKOS
(pour certains extrait du schéma du SEDA 2). De ce fait, tous les éléments de type `CodeListVersion`
pointent vers des vocabulaires et permettent de contrôler les concepts disponibles pour les éléments
associés.

Les balises référençant une notice d'autorité sont les suivantes : `Validator`, `Signer`, `Writer`,
`AuthorizedAgent`, `Addressee`, `Recipient`, `OriginatingAgency`, `SubmissionAgency`,
`ArchivalAgency`, `TransferringAgency`.

Les balises référençant un ou plusieurs concepts d'un vocabulaires sont les suivants :
`AcquisitionInformation`, `DescriptionLevel`, `ClassificationLevel`, `FinalAction`, `Encoding`,
`MimeType`, `EventType`, `LegalStatus`, `KeywordType`, `KeywordReference`, `CompressionAlgorithm`,
`MeasurementUnits`, `MeasurementWeightUnits`, `unit`, `FinalActionStorageCode`,
`FinalActionAppraisalCode`, `Level`, `FileFormat`, `VersionId`, `DataObjectVersion`, `FormatId`,
`Rule`, `RefNonRuleId`, `Type`. Les attributs suivants sont également gérés via référence vers un
concept : `type` (balise `Relationship`), `algorithm` et `language`.


.. _`référentiel SAEM`: http://www.saem.e-bordeaux.org/