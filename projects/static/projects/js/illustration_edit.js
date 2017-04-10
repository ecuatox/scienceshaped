function addImage() {
    $('.images.add').append(
        `<div class="field image">
            <input style="display: none;" name="image" type="number">
            <div class="ui card image">
            <i class="close icon"></i>
            <div class="image select">
                <img src="` + defaultThumbnail + `">
            </div>
          </div>
        </div>`
    );
}

function selectThumnail(id) {
    thumbWindow.close();
    imageCard.find('input').val(id);
    imageCard.find('img').attr('src', '/files/image/' + id + '/view');
}

$(function () {

    $('.ui.checkbox.toggle').checkbox();

    $('.add.image').click(function () {
        addImage();
        $imageselect = $('.image.select');
        $imageselect.unbind();
        $imageselect.click(function () {
            imageCard = $(this).parent().parent();
            thumbWindow = window.open('/files/images');
        });
        $closeicon = $('.card.image .close.icon');
        $closeicon.unbind();
        $closeicon.click(function () {
            $(this).parent().parent().remove();
        });
    });

    $('.image.select').click(function () {
        imageCard = $(this).parent().parent();
        thumbWindow = window.open('/files/images');
    });

    $('.card.image .close.icon').click(function () {
        $(this).parent().parent().remove();
    });

    $('.submit.button').click(function () {
        $('form').submit();
    });

    $('#id_pdf').change(function () {
        var path = $('#id_pdf').val();
        if (path.includes('C:\\fakepath\\')) {
            path = path.replace('C:\\fakepath\\', '')
        }
        $('#pdf_dummy').val(path);
    });

    $('.ui.calendar.date').calendar({
        type: 'date',
        firstDayOfWeek: 1,
    });

    $('#pdfclear').click(function () {
        $('#id_pdf').val('');
        $('#pdf_dummy').val('');
    });

    $('.dropdown').dropdown();
});
