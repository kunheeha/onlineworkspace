

function runStripe(productID) {
	var stripe = Stripe("pk_test_51IcE41LxTuLFo4wY1xRnnXqX8XTq7UyUfHsVvzhe75P2Zh19COwbop1MSUDjcTLSsp5iRaWQRa8a5D7sYDwnYkFO003I1BPo64");

	fetch('/create-checkout-session/' + productID + '/', {
		method: 'POST',
	})
	.then(function(response) {
		return response.json();
	})
	.then(function(session) {
		return stripe.redirectToCheckout({ sessionId: session.id });
	})
	.then(function(result) {
		if (result.error) {
			alert(result.error.message);
		}
	})
	.catch(function(error) {
		console.error('Error: ', error);
	});
}

$(document).ready(function () {

	$('.checkout-button').on('click', function() {
		var productID = $(this).attr('data-productid');
		runStripe(productID);
	})

});