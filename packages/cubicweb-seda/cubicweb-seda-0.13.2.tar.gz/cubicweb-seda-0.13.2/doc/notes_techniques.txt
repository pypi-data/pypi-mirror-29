Fonctionnement du formulaire simplifié des objet-données

* on affiche un formulaire pour un 'SEDABinaryDataObject' qui va aussi créer un
  'SEDADataObjectReference' non visible

* `view.simplified.DataObjectReferenceNoTitleEntityInlinedFormRenderer` permet
  de n'avoir pas de titre ni de lien pour supprimer le formulaire inlined

* `view.simplified.DataObjectSimplifiedAutomaticEntityForm` ajoute un champ caché pour créé la relation entre le DataObjectReference et le SEDASeqAltArchiveUnitArchiveUnitRefIdManagement

* `hooks.SimplifiedProfileSyncDORefCardOnCreateHook` garde la synchro entre la
  cardinality du bdo et de sa référence