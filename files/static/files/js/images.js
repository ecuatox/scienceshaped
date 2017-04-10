function doneUploading() {
    uploadWindow.close();
    location.reload();
}

$(function () {

    $('.select.button').click(function () {
        var id = $(this).attr("imageID");
        window.opener.selectThumnail(id);
    });

    $('.button.upload').click(function () {
        uploadWindow = window.open('/files/image-upload/');
    });

    $('.card').click(function (e) {
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

    $(document).click(function () {
        $(".content.btns").css("display", "none");
        $(".content.txt").css("display", "block");
    });

    $(document).keyup(function (event) {
        if (event.which == 27) {
            event.preventDefault();
            $(".content.btns").css("display", "none");
            $(".content.txt").css("display", "block");
        }
    });

});
