$('.submit').click(function() {
  $('form').submit();
});

light = true;

function lighten() {
  $('.cke_wysiwyg_frame').contents().find('.cke_editable').css('background-color', '#fff');
}
function darken() {
  $('.cke_wysiwyg_frame').contents().find('.cke_editable').css('background-color', '#444');
}

$('.dark').click(function() {
  light = false;
  darken();
});
$('.light').click(function() {
  light = true;
  lighten();
});
$(function() {
  setTimeout(function() {
    $('.cke_button__source').click(function() {
      if (light) {
        setTimeout(function() {lighten();}, 50);
      } else {
        setTimeout(function() {darken();}, 50);
      }
    });
  }, 500);
});
