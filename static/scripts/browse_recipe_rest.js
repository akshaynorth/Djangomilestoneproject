(function($){
	$(document).ready(function() {
	    /**
	    * Submit a recipe search RESTFul request
	    */
	    function submit_recipe_search() {
	        // Obtain the recipe category and verify that a non-empty value was provided. On the application form
	        // users are provided with a pre-defined set of recipe categories. This section is a safeguard in case
	        // someone attempts to tamper with the request by sending an empty value
	        let recipe_category = $('#recipe_category').val().trim()
	        if (recipe_category.length == 0) {
	            alert('Please provide a selection for the recipe category')
	            return
	        }

            // Ingredients search is optional
	        let ingredient_list = $('#ingredient_list').val()

	        // Ingredient search type is optional
            let ingredient_search_type = $('#ingredient_search_type').val()

            let form_data = new FormData()

            // Add the recipe category to the data to be sent to the server
            form_data.append('type', recipe_category)

            // The ingredients to be searched for is an optional field. If a user decides to provide a value then
            // send this information to the server
            if (ingredient_list != null && ingredient_list.length > 0) {
                // Add both the ingredient search type, (all or any of the ingredients provided)
                form_data.append('ingredient_search_type', ingredient_search_type)
                // Add the ingredient to be searched for as a list object to the request
                form_data.append('ingredient_list', JSON.stringify(ingredient_list.split(',')))
            }

            // Send a POST request to the server to the search endpoint
            $.ajax(
            {
                type: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                url: '/recipe/search',
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                success: function(response) {
                    // The server request succeeded, redisplay the page with the found recipes
                    let newDoc = document.open("text/html", "replace")
                    newDoc.write(response)
                    newDoc.close()

                    console.log('Recipe search succeeded')
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Recipe creation failed: ' + errorThrown + ' textStatus = ' + textStatus)
                    alert('Could not search for recipes. Try again later.')
                }
            }
            )

	    }

        /**
        * Issues an edit recipe RESTFul request
        *
        * @param {Object} edit_link_obj: the DOM object that refers to the edit link on the recipe page
        */
        function edit_recipe(edit_link_obj) {
            // Send the delete POST request to the serer
            $.ajax(
            {
                type: 'GET',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                // Obtain the href value that contains the endpoint to the recipe object to be edited
                // (e.g. /recipe/edit/<obj_id>)
                url: $(edit_link_obj).attr('href'),
                data: {},
                processData: false,
                contentType: false,
                cache: false,
                success: function(response) {
                    let newDoc = document.open("text/html", "replace")
                    newDoc.write(response)
                    newDoc.close()
                    console.log('Recipe edit succeeded')
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Recipe edit failed: ' + errorThrown + ' textStatus = ' + textStatus)
                    alert('Could not edit recipe. Try again later.')
                }
            }
            )
        }

        /**
        * Issues a delete recipe RESTFul request
        * @param {Object} delete_link_obj: the DOM object that refers to the delete link on the recipe page
        */
        function delete_recipe(delete_link_obj) {

            // Send the delete POST request to the serer
            $.ajax(
            {
                type: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                // Obtain the href value that contains the endpoint to the recipe object to be deleted
                // (e.g. /recipe/delete/<obj_id>
                url: $(delete_link_obj).attr('href'),
                data: {},
                processData: false,
                contentType: false,
                cache: false,
                success: function(response) {
                    console.log('Recipe delete succeeded')
                    alert('Recipe has been deleted.')
                    // The recipe delete succeeded, reload the page to update the fact the recipe no longer exists
                    location.reload()
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Recipe deletion failed: ' + errorThrown + ' textStatus = ' + textStatus)
                    alert('Could not delete recipe. Try again later.')
                }
            }
            )
        }

        // Attach the search function to the search recipe button
        $('#search_recipe_btn').click(function (e) {
            e.preventDefault()
            submit_recipe_search()
        })

        // Attach the edit recipe function to the edit link of each recipe
        $('[id^=edit_recipe]').click(function(e) {
            e.preventDefault()
            edit_recipe(this)
        })

        // Attach the delete recipe function to the delete link of each recipe
        $('[id^=delete_recipe]').click(function (e) {
            e.preventDefault()
            delete_recipe(this)
        })

	})
})(this.jQuery);