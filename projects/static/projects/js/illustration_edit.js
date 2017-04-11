function addImage() {
    $('.images.add').append(
        `<div class="field image">
            <input class="imagepk" style="display: none;" name="image" type="number">
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
    $imageselect = $('.image.select');
    $closeicon = $('.card.image .close.icon');

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

    $imageselect.click(function () {
        imageCard = $(this).parent().parent();
        thumbWindow = window.open('/files/images');
    });

    $closeicon.click(function () {
        $(this).parent().parent().remove();
    });

    $('.submit.button').click(function () {
        $('#id_tags').val($('#id_tags_dummy').val().split(','));
        imagepk = [];
        $('.imagepk').each(function () {
            imagepk.push($(this).val());
        });
        $('#id_images').val(imagepk);
        $('.ui.calendar.date').calendar({
            type: 'date',
            firstDayOfWeek: 1,
            monthFirst: false,
            formatter: {
                date: function (date, settings) {
                    if (!date) return '';
                    var day = date.getDate();
                    var month = date.getMonth()+1;
                    var year = date.getFullYear();
                    return year + '-' + month + '-' + day;
                }
            },
        });
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
        monthFirst: false,
        formatter: {
            date: function (date, settings) {
                if (!date) return '';
                var day = date.getDate();
                var month = date.getMonth();
                var year = date.getFullYear();
                return day + ' ' + settings['text']['months'][month] + ' ' + year;
            }
        },
    });

    $('#pdfclear').click(function () {
        $('#id_pdf').val('');
        $('#pdf_dummy').val('');
    });

    $('.dropdown').dropdown();
});
