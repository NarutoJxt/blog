$(document).ready(function () {
    key = $.trim($("#notice-type").text());
    lis = $(".aside>ul>li");
    typeList = ["comment","attention","collection","appeal","other"]
    for(i=0;i<typeList.length;i++){
        if(typeList[i] == key) {
            $(lis[i]).css("background-color", "lightgrey");
            break;
        }
    }

});