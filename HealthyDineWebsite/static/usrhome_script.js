$(".cart").click(function (){

$.ajax({
url : $(this).attr("data-url"),
type : "POST",
data : JSON.stringify({food_id : $(this).attr("food_id"), actual_freq:-1}),
headers: {
                'X-CSRFToken': '{{csrf_token}}'
            }
});
});

/*$("#cart").click(function (){
$.ajax({
url : $(this).attr("data-url"),
type : "POST",
data : JSON.stringify({food_id : $(this).attr("food_id")}),
headers: {
                'X-CSRFToken': '{{csrf_token}}'
            }
});
});*/

$(".orders_page").click(function (){
window.location.href = $(this).attr("directing-url");
});
