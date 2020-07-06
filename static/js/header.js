$(document).ready(function(){
	$("input#showImg").load(function(){
		var opt = {"showImg":$(this).val()};
		$.post("http://127.0.0.1:8000/account/showImg/",
			JSON.stringify(opt),
			function(data,status){
				if(data["a"]) {
					document.getElementById("chanImg")
						.setAttribute("src",data['a']);
				}
			}
		);
	});
});