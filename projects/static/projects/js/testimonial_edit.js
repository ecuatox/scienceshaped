$(function () {
    $('.ui.checkbox.toggle').checkbox();

    $('.submit.button').click(function () {
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

    $('.image.select').click(function () {
        imageCard = $(this).parent().parent();
        thumbWindow = window.open('/files/images');
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
});

function selectThumnail(id) {
    thumbWindow.close();
    imageCard.find('input').val(id);
    imageCard.find('img').attr('src', '/files/image/' + id + '/view');
}