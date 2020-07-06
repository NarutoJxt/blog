$(document).ready(function () {
        $("a.author-follow").click(function () {
            var username = $.trim($(this).prev().text());
            var i = $(this).children('i');
            var img = $(this).children("img");
            var  name =$.trim(i.text());
            let host = window.location.host;
            url = "http://" + host + "/account/attention/";
            if (name=="关注") {
                i.text("已关注");
                $(img).attr("src","/static/image/design/attented.png");
                var opt = {"username": username, "status": 1};
                $.get(
                    "http://127.0.0.1:8000/account/attention/",
                    opt,
                    function (data, status) {
                        alert(data["result"])
                    }
                )
            }
            else {
                i.text("关注");
                $(img).attr("src","/static/image/design/attention.png");
                var opt = {"username": username, "status": 3};
                $.get(
                    "http://127.0.0.1:8000/account/attention/",
                    opt,
                    function (data, status) {
                    }
                )
            }
        });

        //当type等于2时，显示取消关注，当鼠标移开时,变为type为1，显示已关注
        //当点击时，表示取消关注，type变为0，显示关注

});

