$(document).ready(function () {
    $.ajaxSetup({cache: false});
    //绑定邮箱时进行弹出邮箱验证码框
    $("button.email-btn").click(function () {
        $("#email").removeClass("hidden");
        $("#email").addClass("show");
        $(".base-info").css("opacity", 0.5);
        $(".left-sidebar").css("opacity", 0.5);
    });
    //取消邮箱验证框
    $("button.bind-cancel").click(function () {
        $("#bind_email").removeClass(
            "show"
        );
        $("#bind_email").addClass("hidden");
        $(".base-info").css("opacity", 1);
        $(".left-sidebar").css("opacity", 1);
    });
    //取消邮箱验证码框
    $("button.cancel").click(function () {
        $("#email").removeClass(
            "show"
        );
        $("#email").addClass("hidden");
        $(".base-info").css("opacity", 1);
        $(".left-sidebar").css("opacity", 1);
    });
    //绑定邮箱时发送验证码
    $("button#send-code").click(function () {
        let host = window.location.host;
        url = "http://" + host + "/account/get_code/";
        csrf = $("#form-body").children("form").children("input")[0];
        csrf = $(csrf).val();
        data ={
            "csrfmiddlewaretoken": csrf
        }
        $.post(
            url, data, function (data, status) {
                $("#confirm-code").click(
                    function () {
                        var1 = String($(".form").val());
                        var2 = String(data["code"]);
                        if (var1 == var2) {
                            $("#code-error").css("visibility", "visible");
                            $("#email").removeClass(
                                "show"
                            );
                            $("#email").addClass("hidden");
                            $("#bind_email").removeClass("hidden");
                            $("#bind_email").addClass("show");
                            window.countdown = 60;
                        } else {
                            $("#code-error").css("visibility", "visible");
                            $("#code-error").text("验证码错误，请诚信输入")
                        }
                    }
                );


            }
        )
    });

});
