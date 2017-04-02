$('.dropdown').dropdown();

$('.removeloader').on('load', function() {
  $(this).siblings('.dimmer').remove();
}).each(function() {
  if ($(this).prop('complete')) {
    $(this).siblings('.dimmer').remove();
  }
});

$('.readmore').click(function () {
    $('.modal.' + $(this).attr('illustration')).modal('show');
});
