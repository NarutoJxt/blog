var countdown = 60;

function send_email_code() {
    let host = window.location.host;
    url = "http://" + host + "/account/get_code/";
    csrf = $(".identy-email").children("form").children("input")[0];
    csrf = $(csrf).val();
    data = {
        "csrfmiddlewaretoken": csrf
    };
    $.post(url, data, function (data, status) {
        $("#confirm-code").click(
            function () {
                var1 = String($(".form").val());
                var2 = String(data["code"]);
                if (var1 == var2) {
                    $(".email-block").css("display", "none")
                    $(".pwd-block").css("display", "block")

                } else {
                    $("#code-email-error").css("visibility", "visible");
                    $("#code-email-error").text("验证码错误，请诚信输入")
                }
            }
        )
    })
}

function confirm_email(obj) {
    obj = $(obj);
    send_email_code();
    settime(obj);
}

function settime(obj) { //发送验证码倒计时
    if (countdown == 0) {
        obj.attr('disabled', false);
        //obj.removeattr("disabled");
        obj.text("发送验证码");
        countdown = 60;
        return;
    } else {
        obj.attr('disabled', true);
        obj.text("重新发送(" + countdown + ")");
        countdown--;
    }
    setTimeout(function () {
            settime(obj)
        }
        , 1000)
};
$(document).ready(function () {
    $("#modify-pwd").click(function () {
        var pwd1 = $("#pwd1").val();
        var pwd2 = $("#pwd1").val();
      if (pwd1 == "" || pwd2 == "") {
            $("#pwd-error").text("输入密码不能为空")
      }
      else if (pwd1 == pwd2) {
          regx= "[A-Za-z0-9@]+";
          regx = new RegExp(regx);
             if(!regx.test(pwd1)){
                   $("#pwd-error").text("输入密码要求由字母数字@组成")
             }
             else if(pwd1.length<8){
                 $("#pwd-error").text("输入密码要求超过8位")
             }
             else {
                  let host = window.location.host;
                   url = "http://" + host + "/account/modify_pwd/?type=modify";
                           csrf = $(".pwd-body").children("form").children("input")[0];
                    csrf = $(csrf).val();
                   data = {
                       "password":pwd1,
                        "csrfmiddlewaretoken": csrf
                   }
                 $.post(url,data,function (data,status) {
                         alert("取消修改");
                         $(location).attr('href', data["url"]);
                     }

                 )
             }
        }
      else{
            $("#pwd-error").text("两次驶入密码不一致")
        }

    })
    $("#cancel-pwd").click(function () {
                      let host = window.location.host;
                   url = "http://" + host + "/account/modify_pwd/?type=cancel";
                           csrf = $(".pwd-body").children("form").children("input")[0];
                    csrf = $(csrf).val();
                   data = {
                        "csrfmiddlewaretoken": csrf
                   };
                 $.post(url,data,function (data,status) {
                         alert("修改成功");
                         $(location).attr('href', data["url"]);
                     }
                 )
    })
});