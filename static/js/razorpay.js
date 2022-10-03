$(document).ready(function(){

            $('#rzp-button1').click(function(e){

            e.preventDefault();
               alert("hello");


            $.ajax({

            method:"GET",
            success:function (response){


            };


            });
            var options = {
    "key": "rzp_test_GTE5lPRQI44nk6", // Enter the Key ID generated from the Dashboard
    "amount": "50000", // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
    "currency": "INR",
    "name": "Beeshopee",
    "description": "Test Transaction",
    "image": "https://example.com/your_logo",
    "order_id": "{{order.order_number}}", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
    "callback_url": "{% url 'success' %}",
    "prefill": {
        "name": "{{order.user.name}}",
        "email": "{{request.user}}",
        "contact": "{{order.user.phone}}"
    },
    "notes": {
        "address": "Razorpay Corporate Office"
    },
    "theme": {
        "color": "#3399cc"
    }
};

var rzp1 = new Razorpay(options);
document.getElementById('rzp-button1').onclick = function(e){
    rzp1.open();
    e.preventDefault();
}
})

})