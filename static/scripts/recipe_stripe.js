(function($){
    $(document).ready(function() {

      // Code initially obtained from Stripe documentation at: https://stripe.com/docs/payments/accept-a-payment
      // The script from the Stripe site must be included before the execution of this code from
      // https://js.stripe.com/v3/"
      // Modified to use JQuery and integrate with the recipe site custom-built pages

      // Publicly accessible key provided by the Stripe dashboard. This has to be modified for each new stripe account
      let stripe = Stripe(
        'pk_test_51II4NQBC4shKo1aqBULTRTh7zFy6hfpNx7LpfpiPCb4TlbkiYehTn34C4iC3VW368NInGSC82NMHw88PeUz2Ge9j00w4wigfuq'
      );

      let checkoutButton = $('#checkout-button');

      checkoutButton.click(function(e) {
        e.preventDefault()

        fetch('/create-checkout-session', {
          method: 'POST',
          headers: {'X-CSRFToken': getCookie('csrftoken')}
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
          console.log('Error: ' + error);
        });
      })
  })
})(this.jQuery);
