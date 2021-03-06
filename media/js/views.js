$(document).ready(function() {
    var metadata = $('#view-metadata');
    var form = $('#obj-form form')[0];
    var objType = metadata.attr('data-objType');
    var prettyObjType = metadata.attr('data-prettyObjType');
    var searchUrl = metadata.attr('data-searchUrl');
    var getUrl = metadata.attr('data-getUrl');
    var domainsUrl = metadata.attr('data-domainsUrl');
    var objPk = metadata.attr('data-objPk');
    // For inputs with id = 'id_fqdn' | 'id_target' | server, make smart names.
    if (domainsUrl) {
        make_smart_name_get_domains($('#id_fqdn, #id_target, #id_server'), true, domainsUrl);
    }

    function prettify(obj) {
        var obj_name = obj.split('_');
        for(i=0; i < obj_name.length; i++){
            obj_name[i] = obj_name[i].charAt(0).toUpperCase() + obj_name[i].slice(1);
        }
        return obj_name.join(' ');
    }

    $('.create-obj').click(function(e) {
        // Show create form on clicking create button.
        e.preventDefault();
        if(this.hasAttribute('data-objType')) {
            var $createBtn = $(this);
            var formPrettyObjType = $createBtn.attr('data-prettyobjtype');
            var formObjType = $createBtn.attr('data-objType');
            var formGetUrl = $createBtn.attr('data-getUrl');
            var formObjName = $createBtn.attr('data-objName');
            var data_to_post = $createBtn.attr('data-kwargs');
            slideUp($('#obj-form'));
            $.get(formGetUrl,
                {
                    'object_type': formObjType,
                    'related_type': objType,
                    'related_pk': objPk,
                    'data': data_to_post
                },
                function(data) {
                    setTimeout(function() {
                        if(formObjName) {
                            $('#form-title').html('Creating ' + formPrettyObjType + ' for ' + formObjName);
                        } else {
                            $('#form-title').html('Creating ' + formPrettyObjType);
                        }
                        data.form.action = $createBtn.attr('href');
                        $('.inner-form').empty().append(data.form);
                        initForms();
                    }, 150);
                    $('#obj-form form')[0].action = $createBtn.attr('href');
                    $('.form-btns a.submit').text('Create ' + formPrettyObjType);
                    $('#obj-form').slideToggle();
                }, 'json');
        } else {
            setTimeout(function() {
                $('#form-title').html('Creating ' + prettyObjType);
                clear_form_all(form);
            }, 150);
            $('.form-btns a.submit').text('Create ' + prettyObjType);
            $('#obj-form').slideToggle();
        }
    });

    $('.update').click(function(e) {
        // Show update form on clicking update icon.
        slideUp($('#obj-form'));

        e.preventDefault();
        form.action = this.href;
        var object_type = $(this).attr('data-object_type') || objType;
        $.get($(this).attr('data-getUrl') || getUrl, {'object_type': object_type,
                       'pk': $(this).attr('data-pk')}, function(data) {
            setTimeout(function() {
                $('#form-title').html('Updating ' + prettify(object_type));
                $('.inner-form').empty().append(data.form);
                initForms();
            }, 150);
            $('.form-btns a.submit').text('Update ' + prettify(object_type));
            $('#obj-form').slideDown();
        }, 'json');
    });
});
