tinyMCE.init({

    // see https://REMOVED
    selector:'textarea.TinyEditor, #flatpage_form textarea',
    height: 300,
    plugins: [
        "hr link lists image charmap paste print preview anchor pagebreak",
        "searchreplace visualblocks visualchars code fullscreen",
        "insertdatetime media nonbreaking save table emoticons template",
    ],
    toolbar1: "undo removeformat blockquote redo subscript superscript | cut copy paste | bold italic underline strikethrough | alignleft aligncenter alignright alignjustify",
    toolbar2: "bullist numlist outdent indent | link image media | print preview | forecolor backcolor emoticons",
    image_advtab: true,
    setup : function(ed) {
      ed.on('init', function(evt) {
          ed.getBody().setAttribute('spellcheck', true);
      });
    },
    relative_urls: false,
    document_base_url: "https://REMOVED
    style_formats_merge: true,
    style_formats: [
        {title: "Alerts", items: [
            {title: 'Information tip', block: 'p', classes: 'alert alert-info'},
            {title: 'Warning tip', block: 'p', classes: 'alert alert-warning'},
            {title: 'Success tip', block: 'p', classes: 'alert alert-success'},
            {title: 'Danger tip', block: 'p', classes: 'alert alert-danger'},
            {title: 'Alert link', inline: 'a', classes: 'alert-link'},
        ]},
        {title: 'Download', block: 'p', classes: 'download'},
        {title: 'Float left', block: 'div', classes: 'float-left'},
        {title: 'Float right', block: 'div', classes: 'float-right'},
    ],
    contextmenu: false,
    valid_elements : "@[id|class|style|title|dir<ltr?rtl|lang|xml::lang|onclick|ondblclick|"
    + "itemscope|itemprop|content|"
    + "onmousedown|onmouseup|onmouseover|onmousemove|onmouseout|onkeypress|"
    + "onkeydown|onkeyup],a[rel|rev|charset|hreflang|tabindex|accesskey|type|"
    + "name|href|target|title|class|onfocus|onblur],strong/b,em/i,strike,u,"
    + "#p,-ol[type|compact],-ul[type|compact],-li,br,img[longdesc|usemap|"
    + "src|border|alt=|title|hspace|vspace|width|height|align],-sub,-sup,"
    + "-blockquote,-table[border=0|cellspacing|cellpadding|width|frame|rules|"
    + "height|align|summary|bgcolor|background|bordercolor],-tr[rowspan|width|"
    + "height|align|valign|bgcolor|background|bordercolor],tbody,thead,tfoot,"
    + "#td[colspan|rowspan|width|height|align|valign|bgcolor|background|bordercolor"
    + "|scope],#th[colspan|rowspan|width|height|align|valign|scope],caption,-div,"
    + "-span,-code,-pre,address,-h1,-h2,-h3,-h4,-h5,-h6,hr[size|noshade],-font[face"
    + "|size|color],dd,dl,dt,cite,abbr,acronym,del[datetime|cite],ins[datetime|cite],"
    + "object[classid|width|height|codebase|*],param[name|value|_value],embed[type|width"
    + "|height|src|*],script[src|type],map[name],area[shape|coords|href|alt|target],bdo,"
    + "button,col[align|char|charoff|span|valign|width],colgroup[align|char|charoff|span|"
    + "valign|width],dfn,fieldset,form[action|accept|accept-charset|enctype|method],"
    + "input[accept|alt|checked|disabled|maxlength|name|readonly|size|src|type|value],"
    + "kbd,label[for],legend,noscript,optgroup[label|disabled],option[disabled|label|selected|value],"
    + "q[cite],samp,select[disabled|multiple|name|size],small,"
    + "textarea[cols|rows|disabled|name|readonly],tt,var,big,"
    + "iframe[allow|allowfullscreen|height|loading|name|referrerpolicy|src|width]",
    custom_elements: "style",

    file_picker_callback: FileBrowserPopup,
});

tinymce.init({
    selector: '#content_id',
    inline: true
});

function FileBrowserPopup(callback, value, type) {
    var fbURL = '/admin/filebrowser/browse/?pop=5';
    fbURL = fbURL + "&type=" + type.filetype;
    if(value)
        fbURL += '&input=';
    const instanceApi = tinyMCE.activeEditor.windowManager.openUrl({
        title: 'Filebrowser image/media/file picker',
        url: fbURL,
        width: 850, 
        height: 500,
        onMessage: function(dialogApi, details) {
            callback(details.content);
            instanceApi.close();
        }
    });
    return false;
}
