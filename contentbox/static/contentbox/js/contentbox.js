$('.submit').click(function () {
    $('form').submit();
});

function lighten() {
    $('.cke_wysiwyg_frame').contents().find('.cke_editable').css('background-color', '#fff');
    $('#id_light').prop('checked', true);
    light = true;
}
function darken() {
    $('.cke_wysiwyg_frame').contents().find('.cke_editable').css('background-color', '#444');
    $('#id_light').prop('checked', false);
    light = false;
}

$('.dark').click(function () {
    darken();
});
$('.light').click(function () {
    lighten();
});

$(function () {
    setTimeout(function () {
        $('.cke_button__source').click(function () {
            if (light) {
                setTimeout(function () {
                    lighten();
                }, 50);
            } else {
                setTimeout(function () {
                    darken();
                }, 50);
            }
        });
    }, 500);
});
