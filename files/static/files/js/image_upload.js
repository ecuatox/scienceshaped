$(function () {

    $('.submit').click(function () {
        $('form').submit();
    });

    $("#id_title").keypress(function (event) {
        if (event.which == 13) {
            event.preventDefault();
            $("#id_description").focus();
        }
    });

    $("#id_description").keypress(function (event) {
        if (event.which == 13) {
            event.preventDefault();
            $("#id_tags").focus();
        }
    });

    $("#id_file").change(function (event) {
        var path = $("#id_file").val();
        if (path.includes("C:\\fakepath\\")) {
            path = path.replace("C:\\fakepath\\", "")
        }
        $("#file_dummy").val(path);
    });

    $('.dropdown').dropdown();
});
