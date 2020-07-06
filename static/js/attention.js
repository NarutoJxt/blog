$(document).ready(function () {
    $("div.aside>ul>li").click(
        function () {
            var li = $(this);
            var liBase = $("div.aside>ul>li");
            var liLength = liBase.length;

            for (var i = 0; i < liLength; i++) {
                liBase[i].setAttribute("class","")
            }
            li.attr("class","li-focus");
        }
    );
});
$(document).ready(function () {
    //当type等于2时，显示取消关注，当鼠标移开时,变为type为1，显示已关注
    //当点击时，表示取消关注，type变为0，显示关注
    $("a.author-icon-2").click(function () {
        var parent = $(this).parent();
        var username = $(this).prev().text();
            var opt = {"username": username, "status": 3};
            parent.remove();
            $.get(
                "http://127.0.0.1:8000/account/attention/",
                opt,
                function (data, status) {
                    if(status == "success"){
                        alert(data["result"])
                    }

                }
            )

    });

});
$(document).ready(function () {
    $("a.author-foloow").hide();
    $("a.author-foloow").click(function () {
        var username = $(this).prev().text();
        var text_sign = $(this).text();
        text_sign = $.trim(text_sign);
        if (text_sign === "关注") {
            $(this).next().show();

            $(this).hide();
            var opt = {"username": username, "status": 1};
            $.get(
                "http://127.0.0.1:8000/account/attention/",
                opt,
                function (data, status) {
                    console.log(data["result"]);
                }
            )
        }
    });

    //当type等于2时，显示取消关注，当鼠标移开时,变为type为1，显示已关注
    //当点击时，表示取消关注，type变为0，显示关注
    $("a.author-foloowing").click(function () {
        var username = $(this).prev().prev().text();
        var text_sign = $(this).text();
        text_sign = $.trim(text_sign);
        if (text_sign === "已关注") {

            var opt = {"username": username, "status": 3};
            $(this).prev().show();
            $(this).hide();
            $.get(
                "http://127.0.0.1:8000/account/attention/",
                opt,
                function (data, status) {
                    console.log(data["result"]);

                }
            )
        }
    });

});