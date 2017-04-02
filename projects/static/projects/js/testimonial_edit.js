$(function () {
  $('.ui.checkbox.toggle').checkbox();

  $('.submit.button').click(function () {
    $('form').submit();
  });

  $('.image.select').click(function () {
    imageCard = $(this).parent().parent();
    thumbWindow = window.open('/files/images');
  });

  $('.ui.calendar.date').calendar({
    type: 'date',
    firstDayOfWeek: 1,
  });
});

function selectThumnail(id) {
  thumbWindow.close();
  imageCard.find('input').val(id);
  imageCard.find('img').attr('src', '/files/image/' + id + '/view');
}