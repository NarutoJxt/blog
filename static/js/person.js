$(document).ready(function () {
    $("form.person-signature").hide();
        key = $.trim($("#get").text());
    console.log(key);
    lis = $(".person-body>ul>li");
    key = parseInt(key);
    switch (key){
        case 1:$(lis[2]).addClass("clicking");break;
        case 2:$(lis[3]).addClass("clicking");break;
        case 3:$(lis[1]).addClass("clicking");break;
        case 4:$(lis[4]).addClass("clicking");break;
        default:$(lis[0]).addClass("clicking");break

    }
    $("a.show-form").click(function () {
         $("form.person-signature").slideDown("slow");
    });
    $("button#cancel").click(function () {
           $("form.person-signature").slideUp("slow");
    });
	$("button#remove").click(function(){
		var title = $(this).prev().prev().text();
		title = $.trim(title);
        var opt = {"title":title,"type":"remove"};
		$.get("http://127.0.0.1:8000/editArticle/",
			opt,
			function(data,status){

			}
		);
	});
		$("button#removeCollection").click(function(){
		var title = $(this).prev().prev().text();
		title = $.trim(title);
        var opt = {"article":title,"is_collected":0,};
	    $.post("http://127.0.0.1:8000/collected/collected.html/",
			JSON.stringify(opt),
			function(data,status) {
                if (data["result"] != 0) {
                    alert(data["result"]);
                }
            })
	});

});

function deleteNode(node) {
    var par = node.parentNode;
    var parUl = par.parentNode;
    parUl.removeChild(par);
}