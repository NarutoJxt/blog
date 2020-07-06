$(document).ready(function(){
	$("button#post_thumb_up").click(function(){
		var opt = {"thumb_up":$(this).children().text(),"comment_id":$(this).next().text()};
		$.post("http://127.0.0.1:8000/comment/comment/postthumb_up.html/",
			JSON.stringify(opt),
			function(data,status){
			alert("点赞成功，谢谢您的支持")
		}
		);
	});
});
$(document).ready(function(){
	$("button#collected").click(function(){
		    var pics = $("img#tranImg");
    		var img = pics.attr("src");
			var cancle = 0;
    		if(!img.startsWith("http:")){
    			img = "http://127.0.0.1:8000"+img;
			}
    		var result = img.search("attention.png");
    		if (result === -1){
        		cancle = 0;
    		}
    		else{
    			cancle = 1;
    		}
    		var opt = {
    			"is_collected":cancle,
				"article":$("h3#get_title").text(),
			};
			$.post("http://127.0.0.1:8000/collected/collected.html/",
			JSON.stringify(opt),
			function(data,status){
				if(data["result"] != 0) {
					alert(data["result"]);
				}
		}
		);
	});
});