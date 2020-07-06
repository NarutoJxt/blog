$(document).ready(function(){
	$("input#showImg").blur(function(){
		var opt = {
			"showImg":$(this).val(),
			"csrfmiddlewaretoken": "{{ csrf_token }}"
		};
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