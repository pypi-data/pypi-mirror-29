// copyright 2015-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
// contact http://www.logilab.fr -- mailto:contact@logilab.fr
//
// This program is free software: you can redistribute it and/or modify it under
// the terms of the GNU Lesser General Public License as published by the Free
// Software Foundation, either version 2.1 of the License, or (at your option)
// any later version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
// details.
//
// You should have received a copy of the GNU Lesser General Public License along
// with this program. If not, see <http://www.gnu.org/licenses/>.

// An autocompletion widget to select a concept from a vocabulary specified by another widget
concept_autocomplete = {
    initConceptAutoCompleteWidget: function(masterSelectId, slaveSelectId, ajaxFuncName) {
        var masterSelect = cw.jqNode(masterSelectId);
        // bind vocabulary select to update concept autocompletion input on value change
        masterSelect.change(function() {
            concept_autocomplete.updateCurrentSchemeEid(this, slaveSelectId);
            concept_autocomplete.resetConceptFormField(slaveSelectId);
        });
        // initialize currentSchemeEid by looking the value of the master field
        concept_autocomplete.updateCurrentSchemeEid(masterSelect, slaveSelectId);
        // also bind the autocompletion widget
        cw.jqNode(slaveSelectId+'Label')
            .autocomplete({
                source: function(request, response) {
                    if (concept_autocomplete.currentSchemeEid) {
                        var form = ajaxFuncArgs(ajaxFuncName,
                                                {'q': request.term,
                                                 'scheme': concept_autocomplete.currentSchemeEid});
                        var d = loadRemote(AJAX_BASE_URL, form, 'POST');
                        d.addCallback(function (suggestions) { response(suggestions); });
                    }
                },
                focus: function( event, ui ) {
                    cw.jqNode(slaveSelectId+'Label').val(ui.item.label);
                    return false;
                },
                select: function(event, ui) {
                    cw.jqNode(slaveSelectId+'Label').val(ui.item.label);
                    cw.jqNode(slaveSelectId).val(ui.item.value);
                    return false;
                },
                'mustMatch': true,
                'limit': 100,
                'delay': 300})
            .tooltip({
                tooltipClass: "ui-state-highlight"
            });

        // add key press and focusout event handlers so that value which isn't matching a vocabulary
        // value will be erased
        resetIfInvalidChoice = function() {
            if (concept_autocomplete.currentSchemeEid) {
                var validChoices = $.map($('ul.ui-autocomplete li'),
                                         function(li) {return $(li).text();});
                var value = cw.jqNode(slaveSelectId + 'Label').val();
                if ($.inArray(value, validChoices) == -1) {
                    concept_autocomplete.resetConceptFormField(slaveSelectId);
                }
            }
        };
        cw.jqNode(slaveSelectId+'Label').keypress(function(evt) {
            if (evt.keyCode == $.ui.keyCode.ENTER || evt.keyCode == $.ui.keyCode.TAB) {
                resetIfInvalidChoice();
            }
        });
        cw.jqNode(slaveSelectId+'Label').focusout(function(evt) {
            resetIfInvalidChoice();
        });
    },
    updateCurrentSchemeEid: function(masterSelect, slaveSelectId) {
        concept_autocomplete.currentSchemeEid = $(masterSelect).val();
        if (concept_autocomplete.currentSchemeEid == '__cubicweb_internal_field__') {
            concept_autocomplete.currentSchemeEid = null;
            cw.jqNode(slaveSelectId+'Label').prop('disabled', true);
        } else {
            cw.jqNode(slaveSelectId+'Label').prop('disabled', false);
        }
    },
    resetConceptFormField: function(slaveSelectId) {
        cw.jqNode(slaveSelectId+'Label').val('');
        cw.jqNode(slaveSelectId).val('');
    }
};

typed_vocabularies = {
    initKeywordTypeMasterWidget: function(masterSelectId, slaveSelectBaseName, allVocabularies) {
        typed_vocabularies.allVocabularies = allVocabularies;
        var $masterSelect = cw.jqNode(masterSelectId);
        var $slaveSelect = $('select[name*="' + slaveSelectBaseName + '"]');
        if ($slaveSelect.length === 0) {
            // simple keyword, don't do anything
            return
        }
        // bind keyword type select to update possible vocabularies on value change
        $masterSelect.change(function() {
            typed_vocabularies.updatePossibleVocabularies($masterSelect, $slaveSelect);
        });
        // initialize possible vocabularies by looking the value of the master field
        typed_vocabularies.updatePossibleVocabularies($masterSelect, $slaveSelect);
    },

    updatePossibleVocabularies: function($masterSelect, $slaveSelect) {
        if (typeof $masterSelect != 'undefined') {
            var selected_type = $masterSelect.val();
        } else {
            var selected_type = '__cubicweb_internal_field__';
        }
        var selected_vocab = $slaveSelect.val();
        // empty possible vocabularies, then refill it with vocabularies that match selected type
        // (or every vocabulary if there is no selected type)
        $slaveSelect.empty();
        $slaveSelect.append('<option value="__cubicweb_internal_field__"></option>');
        for (i=0; i < typed_vocabularies.allVocabularies.length; i++) {
            var vocabulary = typed_vocabularies.allVocabularies[i];
            if (selected_type == '__cubicweb_internal_field__'
                    || selected_type == vocabulary.keyword_type) {
                var selected = '';
                if (selected_vocab == vocabulary.eid) {
                    selected = ' selected="1"'
                }
                $slaveSelect.append(
                    '<option value="' + vocabulary.eid+ '"' + selected + '>'
                        + vocabulary.title + '</option>');
            }
        }
        // we've to trigger the change event by ourselves to kick in concept_autocomplete,
        // probably because we did not changed the value but rather rebuilt the select values
        $slaveSelect.trigger('change');
    },
};
