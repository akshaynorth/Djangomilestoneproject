(function($){
	$(document).ready(function() {

	    /**
	    * Submits a RESTFull API request to add a recipe to the cart
	    */
	    function add_recipe_to_cart(add_to_cart_link_obj) {
	        // Obtain the recipe id URL from the recipe add to cart URL anchor element

            // Send an add to cart recipe POST request
            $.ajax(
            {
                type: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                url: $(add_to_cart_link_obj).attr('href'),
                data: {},
                processData: false,
                contentType: false,
                cache: false,
                success: function(response) {
                    // Redraw the return HTML to update user view
                    let newDoc = document.open("text/html", "replace")
                    newDoc.write(response)
                    newDoc.close()
                    console.log('Recipe added to cart successfully');
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Recipe creation failed: ' + errorThrown + ' textStatus = ' + textStatus)
                    alert('Could not add recipe to cart. Try again later.')
                }
            }
            )

	    }

        /**
        * Submits a RESTFull API request to delete a recipe from the cart
        */
	    function delete_recipe_from_cart(delete_from_cart_link_obj) {
	        // Obtain the recipe id URL from the recipe add to cart URL anchor element

            // Send an delete from cart recipe POST request
            $.ajax(
            {
                type: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                url: $(delete_from_cart_link_obj).attr('href'),
                data: {},
                processData: false,
                contentType: false,
                cache: false,
                success: function(response) {
                    // Redraw the return HTML to update user view
                    let newDoc = document.open("text/html", "replace")
                    newDoc.write(response)
                    newDoc.close()
                    console.log('Recipe deleted from cart successfully');
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Recipe creation failed: ' + errorThrown + ' textStatus = ' + textStatus)
                    alert('Could not add recipe to cart. Try again later.')
                }
            }
            )

	    }

        // Attach the submit recipe function to the submit recipe button
        $('[id^=add_to_cart]').click(function (e) {
            e.preventDefault()
            add_recipe_to_cart(this)
        })

        $('[id^=delete_from_cart]').click(function (e) {
            e.preventDefault()
            delete_recipe_from_cart(this)
        })

	})
})(this.jQuery);