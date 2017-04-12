$(function () {
    testimonialpara();
});

$(window).resize(function () {
    testimonialpara();
});

$(document).scroll(function () {
    testimonialpara();
});

function testimonialpara() {
    var scroll = $(window).scrollTop() - 1000;
    $("#testimonial-para-container .para2").css("transform", "rotate(-20deg) translate(" + scroll * 0.05 + "px, " + scroll * 0.5 + "px)");
    $("#testimonial-para-container .para3").css("transform", "rotate(-50deg) translate(" + scroll * 0.1 + "px, " + scroll * 0.1 + "px)");
    $("#testimonial-para-container .para4").css("transform", "rotate(25deg) translate(-" + scroll * 0.1 + "px, " + scroll * 0.1 + "px)");
}