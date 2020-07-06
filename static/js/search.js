
function addAttention(obj) {
    let img = $(obj).children("img");
    let i = $(obj).children("i");
    let text  = $.trim($(i).text());
    let username = $.trim($(obj).prev().text());
    let status = 1
    if(text=="关注"){
        $(i).text("已关注");
        $(img).attr("src","/static/image/search/search-success.png");
        status = 1;
    }
    else{
         $(i).text("关注");
        $(img).attr("src","/static/image/search/search-attention.png")
        status = 3
    }
    host = window.location.host;
    url = "http://" + host + "/account/attention/";
    data = {
        "status":status,
        "username":username
    };
    $.get(url,data,function (data,status) {
        alert(data["result"])
    })
}
