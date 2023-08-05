// overwrite CW's addInlineCreationForm function to propagate container eid information
function addInlineCreationForm(peid, petype, ttype, rtype, role, i18nctx, insertBefore) {
    insertBefore = insertBefore || cw.getNode('add' + rtype + ':' + peid + 'link').parentNode;
    var ceid = $('#sedaContainerEID');
    if (ceid.length == 1) {
        form = {'sedaContainerEID': ceid.attr('value')};
    } else {
        form = null;
    }
    var args = ajaxFuncArgs('inline_creation_form', form, peid, petype, ttype, rtype, role, i18nctx);
    var d = loadRemote(AJAX_BASE_URL, args);
    d.addCallback(function(response) {
        var dom = getDomFromResponse(response);
        loadAjaxHtmlHead(dom);
        var form = jQuery(dom);
        form.css('display', 'none');
        form.insertBefore(insertBefore).slideDown('fast');
        updateInlinedEntitiesCounters(rtype, role);
        reorderTabindex(null, $(insertBefore).closest('form')[0]);
        jQuery(cw).trigger('inlinedform-added', form);
        // if the inlined form contains a file input, we must force
        // the form enctype to multipart/form-data
        if (form.find('input:file').length) {
            // NOTE: IE doesn't support dynamic enctype modification, we have
            //       to set encoding too.
            form.closest('form').attr('enctype', 'multipart/form-data').attr('encoding', 'multipart/form-data');
        }
        _postAjaxLoad(dom);
    });
    d.addErrback(function(xxx) {
        cw.log('xxx =', xxx);
    });
}
