
	function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
        $(document).ready(function(){

        $('.increment-btn').click(function(e){
        alert("hai");
        e.preventDefault();

        var url  = "cart_prod_inr/"
        var csrftoken = getCookie('csrftoken')
        var id = $(this).data('value');
        console.log("id"+id);
        var inc_value = $(this).closest('.product_data').find('.qty-input').val();
        console.log("inc_value",inc_value);

        var price = $(this).closest('.product_data').find('.product_price').val();

        var delivery_charge = $('.delivery_charge').val();


        var value = parseInt(inc_value,5);
        value = isNaN(value) ? 0:value;
         if(value < 5)
         {
         value++;

            $(this).closest('.product_data').find('.qty-input').val(value);

            var total = price*value;
             $(this).closest('.product_data').find('.item_total').val(total);

//             inserting the value to  subtotal
                 $('.sub_total').val(total);

            var grand_total = parseInt(delivery_charge) + total;
            $('.grand_total').val(grand_total);

                sendData();
                function sendData(){
                 fetch(url, {
                                method : "POST",
                                headers: {
                                    "Content-type": "application/json",
                                    "X-CSRFToken": csrftoken,
                                },
                                body: JSON.stringify({
                                      quantity:value,
                                      id:id,
                                      total:total,

                                },null,2),
                            })
                            }
                       }
                });


$('.decrement-btn').click(function(e){
        e.preventDefault();
        var pid = $(this).data('pid');
        var cid = $(this).data('cid')
        var url  = "cart_prod_dec/"
        var csrftoken = getCookie('csrftoken')

         var dec_value = $(this).closest('.product_data').find('.qty-input').val();
         console.log("dec_value",dec_value);
        var price = $(this).closest('.product_data').find('.product_price').val();

        var total = $(this).closest('.product_data').find('.item_total').val();

        var delivery_charge = $('.delivery_charge').val();


            console.log("dec_value:",dec_value);
         if(dec_value > 1)
         {
         dec_value--;
          $(this).closest('.product_data').find('.qty-input').val(dec_value);

             total =price * dec_value;
            $(this).closest('.product_data').find('.item_total').val(total)


//             inserting the value to  subtotal
                 $('.sub_total').val(total);

                  var grand_total = parseInt(delivery_charge) + total;
                   $('.grand_total').val(grand_total);

                sendData();
                function sendData(){
                 fetch(url, {
                                method : "POST",
                                headers: {
                                    "Content-type": "application/json",
                                    "X-CSRFToken": csrftoken,
                                },
                                body: JSON.stringify({
                                      quantity:dec_value,
                                      product_id:pid,
                                      cartItem_id:cid,
                                      total:total,

                                },null,2),
                            })
                            }
                       }
                });



});