/* Set rates + misc */
var taxRate = 0.05;
var shippingRate = 15.00; 
var fadeTime = 300;


/* Assign actions */
$('.product-quantity input').change( function() {
  updateQuantity(this);
});

$(document).ready(function() {
updateQuantity($('.product-quantity input'));
});


$(".product-quantity input").change(function (){
$.ajax({
url : $(this).attr("data-url"),
type : "POST",
data : JSON.stringify({food_id : $(this).attr("food_id"), actual_freq:$(this).val(), cart_total:TOTAL}),
headers: {
                'X-CSRFToken': '{{csrf_token}}'
            }
});
});

/*$("#cart").click(function (){
$.ajax({
url : $(this).attr("data-url"),
type : "POST",
data : JSON.stringify({food_id : $(this).attr("food_id"), cart_total:TOTAL}),
headers: {
                'X-CSRFToken': '{{csrf_token}}'
            }
});
});*/


$('.product-removal button').click( function() {
  removeItem(this);
});


/* Recalculate cart */
function recalculateCart()
{
  var subtotal = 0;
  
  /* Sum up row totals */
  $('.product').each(function () {
    subtotal += parseFloat($(this).children('.product-line-price').text());
  });
  
  /* Calculate totals */
  var tax = subtotal * taxRate;
  var shipping = (subtotal > 0 ? shippingRate : 0);
  var total = subtotal + tax + shipping;
  
  /* Update totals display */
  $('.totals-value').fadeOut(fadeTime, function() {
    $('#cart-subtotal').html(subtotal.toFixed(2));
    $('#cart-tax').html(tax.toFixed(2));
    $('#cart-shipping').html(shipping.toFixed(2));
    $('#cart-total').html(total.toFixed(2));
    if(total == 0){
      $('.checkout').fadeOut(fadeTime);
    }else{
      $('.checkout').fadeIn(fadeTime);
    }
    $('.totals-value').fadeIn(fadeTime);
  });
return total;
}

var TOTAL = 0;
/* Update quantity */
function updateQuantity(quantityInput)
{
  /* Calculate line price */

  var productRow = $(quantityInput).parent().parent();
  var price = parseFloat(productRow.children('.product-price').text());
  var quantity = $(quantityInput).val();
  var linePrice = price * quantity;
  
  /* Update line price display and recalc cart totals */
  productRow.children('.product-line-price').each(function () {
    $(this).fadeOut(fadeTime, function() {
      $(this).text(linePrice.toFixed(2));
     TOTAL = recalculateCart();
      $(this).fadeIn(fadeTime);
    });
  });  
}


/* Remove item from cart */
function removeItem(removeButton)
{
  /* Remove row from DOM and recalc cart total */
  var productRow = $(removeButton).parent().parent();
  productRow.slideUp(fadeTime, function() {
    productRow.remove();
    recalculateCart();
});
}

var post_dict = {};
function update_rating_post(ele){
if(this.checked){
post_dict[this.name] = this.value;}
return;
};

function initialise_post_dict(ele){
post_dict[this.name] = "null";
return ;
}

function update_descriptive_post(ele){
post_dict[this.name] = this.value;
return;
};

$(".checkout").click(function(){
$.ajax({
url : $(this).attr('orders-url'),
type:"POST",
data :JSON.stringify({cart_total:TOTAL}),
headers: {
                'X-CSRFToken': '{{csrf_token}}'
            }
});
});


$(".checkout").click(function(){

      $all_ratings = $("input[type='radio']").map(function (){ return this; }).get();

$.each($all_ratings, initialise_post_dict);
console.log(post_dict);
$.each($all_ratings, update_rating_post);
$all_descrs = $("textarea");
$.each($all_descrs, update_descriptive_post);
let payload = $.param(post_dict);
let payloadjs = JSON.stringify(post_dict);
console.log(payloadjs);
      $.ajax({
	  url: "/orders/order_list/",
	type : "POST",
            data: payloadjs,
            headers: {
                'X-CSRFToken': '{{csrf_token}}'
            }
        });
window.location.href='../payment/';

          });