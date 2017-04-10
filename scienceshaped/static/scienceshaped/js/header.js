$(function () {
    $('.ui.sidebar').sidebar('setting', 'transition', 'overlay');
    $('.sidetoggle').click(function () {
        $('.ui.sidebar').sidebar('toggle');
    });
    $('.ui.sidebar .item').click(function () {
        $('.ui.sidebar').sidebar('hide')
    });

    pos = "top";
});

$(window).scroll(function () {
    var scrollTop = $(window).scrollTop();
    if (pos == "top" && scrollTop > 50) {
        pos = "page";
        $(".desktop .headerbar").addClass("headerSmall");
        $(".desktop .headerbar").removeClass("headerLarge");
    } else if (pos == "page" && scrollTop <= 50) {
        pos = "top";
        $(".desktop .headerbar").addClass("headerLarge");
        $(".desktop .headerbar").removeClass("headerSmall");
    }
});

$("#logo").click(function () {
    $(".desktop .headerbar").addClass("headerLarge");
    $(".desktop .headerbar").removeClass("headerSmall");
});