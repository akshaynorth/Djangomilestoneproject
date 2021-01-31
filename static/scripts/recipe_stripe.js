(function($){
    $(document).ready(

      // Code initially obtained from Stripe documentation at: https://stripe.com/docs/payments/accept-a-payment
      // The script from the Stripe site must be included before the execution of this code from
      // https://js.stripe.com/v3/"
      // Modified to use JQuery and integrate with the recipe site custom-built pages
      var stripe = Stripe(
        'pk_test_51IFbK8IN8KUsEgP5iLWoeK93WTkY3xtWhZ4QHp6GG1Tj7bjmQBMh07q348VBCFxjNP8irfdrJ96554p1QzGsdEVw00lMdHdIq0'
      );

      var checkoutButton = $('#checkout-button');

      checkoutButton.click(function() {
        // Create a new Checkout Session using the server-side endpoint you
        // created in step 3.
        fetch('/create-checkout-session', {
          method: 'POST',
        })
        .then(function(response) {
          return response.json();
        })
        .then(function(session) {
          return stripe.redirectToCheckout({ sessionId: session.id });
        })
        .then(function(result) {
          // If `redirectToCheckout` fails due to a browser or network
          // error, you should display the localized error message to your
          // customer using `error.message`.
          if (result.error) {
            alert(result.error.message);
          }
        })
        .catch(function(error) {
          console.error('Error:', error);
        });
      })
})(this.jQuery);