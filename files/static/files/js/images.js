$("#upload").click(function() {
  uploadWindow = window.open('/files/image-upload/');
});

$(".selectButton").click(function() {
  var src = $(this).attr("selectImage");
  var id = $(this).attr("selectID");
  window.opener.selectThumnail(src, id);
});

function doneUploading(src) {
  uploadWindow.close();
  location.reload();
}

$(function() {

  $('.card').click(function(e) {
    e.stopPropagation();
    if ($(this).find(".content.btns").css("display") == "none") {
      $(".content.btns").css("display", "none");
      $(".content.txt").css("display", "block");
      $(this).find(".content.btns").css("display", "block");
      $(this).find(".content.txt").css("display", "none");
    } else {
      $(".content.btns").css("display", "none");
      $(".content.txt").css("display", "block");
    }
  });

  $(document).click(function() {
    $(".content.btns").css("display", "none");
    $(".content.txt").css("display", "block");
  });

  $(document).keyup(function(event) {
    if (event.which == 27) {
      event.preventDefault();
      $(".content.btns").css("display", "none");
      $(".content.txt").css("display", "block");
    }
  });

});
