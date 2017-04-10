$(function () {
    $newtag = $('.newtag');
    $delete = $('.delete.ajax');

    $('.submit').click(function () {
        newTag($newtag.val());
    });

    $newtag.keypress(function (event) {
        if (event.which == 13) {
            event.preventDefault();
            newTag($newtag.val());
        }
    });

    $delete.click(function () {
        deleteTag($(this).attr('pk'));
    });
});

function newTag(tag) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    });

    $.ajax({
        type: "POST",
        url: 'new/',
        data: {
            'tag': tag,
        },
        success: function (data) {

            var success = data['success'];
            var pk = data['pk'];

            if (success) {
                $('.tags').append('<a class="ui label blue">' + tag + '<i class="delete icon delete ajax" pk="' + pk + '"></i></a>');
                $delete = $('.delete.ajax');
                $delete.unbind();
                $delete.click(function () {
                    deleteTag($(this).attr('pk'));
                });
                $newtag.val('');
            } else {
                var error = data['error'];
                alertify.message(error);
            }
        }
    });
}

function deleteTag(pk) {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    });

    $.ajax({
        type: "POST",
        url: '/tags/delete/' + pk + '/',
        success: function (data) {

            var success = data['success'];

            if (success) {
                $('.delete.ajax[pk=' + pk + ']').parent().remove();
            } else {
                var error = data['error'];
                alertify.message(error);
            }
        }
    });
}