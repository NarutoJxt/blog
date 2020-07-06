function add(value, counter) {
    var btn = document.getElementById(counter);
    btn.innerText = value + 1;
}

//收藏文章
function transImg() {
    var pics = document.getElementById("tranImg");
    var img = pics.getAttribute("src");
    var collections = document.getElementById("collections");
    var count = collections.innerText;
    if (!img.startsWith("http:")) {
        img = "http://127.0.0.1:8000" + img;
    }
    if (img === "http://127.0.0.1:8000/static/image/collected/1.png") {
        img = "http://127.0.0.1:8000/static/image/collected/2.png";
        count--;
    } else if (img === "http://127.0.0.1:8000/static/image/collected/2.png") {
        img = "http://127.0.0.1:8000/static/image/collected/1.png";
        count++;
    }
    collections.innerText = count.toString();
    pics.setAttribute("src", img);
};
//实现点赞功能
$(document).ready(function () {
    var is_thumb = false;
    $("a#thumb").click(function () {
        if(!is_thumb) {
            var title = $(".title").text();
            var thumb_up = $(this).children()[0];
            var author = $(".author-name").text();
            var thumb_up_count = parseInt($(this).children().children().text()) + 1;
            $(this).children().children().text(thumb_up_count);
            thumb_up = thumb_up.setAttribute("src", "../../../../static/image/design/praise(9).png");
            var opt = {"title": title, "author": author, "type": "thumb_up"};
            is_thumb = true;
            $.post(
                "http://127.0.0.1:8000/dealArticle/", opt,
                function (data, status) {

                }
            )
        }
    });

});
$(document).ready(function () {
    var is_thumb = false
    $("div#comment").mouseover(function () {
        var img = $(this).children()[0];
        img.setAttribute("src","../../../../static/image/design/comment(6).png")
    });
    $("div#comment").mouseout(function () {
        var img = $(this).children()[0];
        img.setAttribute("src","../../../../static/image/design/comment(5).png")
    });
    //评论点击按钮滑到底部
    $('div#comment').click(function () {
        $("#parent_comment_id").attr("value",null);
        $('html,body').animate({ scrollTop: document.getElementsByTagName('BODY')[0].scrollHeight}, 2000);
        return false;
    });
    $('button.replyComment').click(function () {
        c_id = $.trim($(this).parent().prev().children(":first").text());
        $('html,body').animate({ scrollTop: document.getElementsByTagName('BODY')[0].scrollHeight}, 2000);
        $("#parent_comment_id").attr("value",c_id);
        return false;
    });
        $('button.replyComment_tree').click(function () {

        c_id = $.trim($(this).parent().prev().prev().children("span").text());
        $('html,body').animate({ scrollTop: document.getElementsByTagName('BODY')[0].scrollHeight}, 2000);
        $("#parent_comment_id").attr("value",c_id);
        return false;
    });
});
$(document).ready(function () {
    $("a#collection").click(function () {
        var host =  window.location.host;
        var url = "http://"+host+"/dealArticle/";
        var title = $(".title").text();
        var author = $($(".author-name")[0]).text();
        var img = $(this).children()[0];
        img = img.getAttribute("src");
        console.log(author);
        var type = "collection";
        if(img === "/static/image/design/collection(11).png" || img === "../../../../static/image/design/collection(11).png"){
            type = "cancleCollection";
        }
        var opt = {"title": title, "author": author, "type": type};
        $.post(
            url, opt, function (data, status) {
                if (data["result"] === 3) {
                    var thumb_up = $("a#collection").children()[0];
                    var collection_count = $("a#collection").children().children().text();
                    collection_count = parseInt(collection_count) + 1;
                    thumb_up = thumb_up.setAttribute("src", "../../../../static/image/design/collection(11).png");
                    $("a#collection").children().children().text(collection_count);
                }
                else if(data["result"]===4){
                    var thumb_up = $("a#collection").children()[0];
                    var collection_count = $("a#collection").children().children().text();
                    collection_count = parseInt(collection_count) - 1;
                    thumb_up = thumb_up.setAttribute("src", "../../../../static/image/design/collection(10).png");
                    $("a#collection").children().children().text(collection_count);
                }
            }
        )

    });
});
function showAppeal() {
    $("div.appeal").removeClass("hide");
    $("div.appeal").addClass("show");
    $("div.container-main").css("opacity","0.5")

}
function cancleAppeal() {
    $("div.appeal").removeClass("show");
     $("div.appeal").addClass("hide");
    $("div.container-main").css("opacity","1")

}

