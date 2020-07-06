$(document).ready(function () {
    key = $.trim($("#get").text());
    lis = $(".change-back");
    key = parseInt(key);
    $(lis[key]).addClass("clicking");
})