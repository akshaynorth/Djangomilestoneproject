(function($){
	$(document).ready(function() {

	    /**
	    * Submits a RESTFull API request to add a recipe to the cart
	    */
	    function add_recipe_to_cart(add_to_cart_link_obj) {
	        // Obtain the recipe id URL from the recipe add to cart URL anchor element

            // Send an edit recipe POST request
            $.ajax(
            {
                type: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                url: $(add_to_cart_link_obj).attr('href'),
                data: {},
                processData: false,
                contentType: false,
                cache: false,
                success: function() {
                    console.log('Recipe added to cart successfully');
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Recipe creation failed: ' + errorThrown + ' textStatus = ' + textStatus)
                    alert('Could not add recipe to cart. Try again later.')
                }
            }
            )

	    }

        // Attach the submit recipe function to the submit recipe button
        $('#add_to_cart').click(function (e) {
            e.preventDefault()
            add_recipe_to_cart(this)
        })
	})
})(this.jQuery);