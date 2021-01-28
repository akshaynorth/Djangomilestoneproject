(function($){
	$(document).ready(function() {
	    /**
	    * Issues a RESFul API request to create the recipe
	    */
	    function create_recipe() {
	        // Gather all the information on the generate cooking directions form
	        // Validate that all fields were provided with a non-empty string input

	        // Obtain the recipe label input
            let recipe_label = $('#recipe_label').val().trim();

            // Verify that the recipe label is no empty
            if (recipe_label.length == 0) {
                alert('Please provide a recipe label.');
                return;
            }

            // Obtain the recipe type input
            let recipe_type = $('#recipe_type').val().trim();

            // Verify that the recipe type is not empty. The recipe type is a drop down that users select from a list of
            // pre-defined options. This is a safeguard in case someone tampers with the request to attempt passing an
            // empty recipe type value
            if (recipe_type.length == 0) {
                alert('Please provide a selection for the recipe type.')
                return;
            }

            // Obtain the recipe description value
            let recipe_description = $.trim($('#recipe_desc').val());

            // Verify that the description is not empty
            if (recipe_description.length == 0) {
                alert('Please provide a recipe description.');
                return;
            }

            // Obtain a list of ingredients provided by the user. The list of ingredients are present in the form
            // as added input fields with the name property set to ingredient_name
            let ingredient_list = []
            $('input[name="ingredient_name"]').each(
                function() {
                    ingredient_list.push($(this).val())
                }
            );

            // Verify that that all ingredient fields have been provided
            for (i in ingredient_list) {
                if (ingredient_list[i].trim().length == 0) {
                    alert('Provide an ingredient description for each of added ingredients');
                    return;
                }
            }

            // Obtain all the instructions provided by the user. Instructions are present the form as
            // input fields with the name property set to instruction_desc
            let instruction_list = []
            $('input[name="instruction_desc"]').each(
                function() {
                    instruction_list.push($(this).val())
                }
            );

            // Verify that all the instructions were filled out
            for (i in instruction_list) {
                if (instruction_list[i].trim().length == 0) {
                    alert('Provide an instruction description for each of added instructions');
                    return;
                }
            }

            // Obtain the recipe preparation time and verify that a non-empty value was provided
            let prep_time = $('#prep_time').val().trim()
            if (prep_time.length == 0) {
                alert('Provide a preparation time');
                return;
            }

            // Obtain the recipe cook time and verify that a value has been provided
            let cook_time = $('#cook_time').val().trim();
            if (cook_time.length == 0) {
                alert('Provide the cooking time');
                return;
            }

            // Obtain the recipe calories and verify that a value has been provided. All the content is assumged to be
            // a string
            let calories = $('#calories').val().trim();
            if (calories.length == 0) {
                alert('Provide the recipe calories');
                return;
            }

            // Obtain the recipe portions and verify that a value has been provided.
            let portions = $('#portions').val().trim();
            if (portions.length == 0) {
                alert('Provide the number of portions/servings')
                return;
            }

            let price = $('#recipe_price').val().trim()
            if (price.length == 0) {
                alert('Provide a price for the recipe')
                return
            }

            // Obtain the filename that was provided by the user for the recipe photo.
	        let form_data = new FormData()
	        if ($('input[type="file"]')[0].files.length > 0) {
	            let upload_file = $('input[type="file"]')[0].files[0]
	            // Append the file object to the file field of the form data to send to the server
	            form_data.append('file', upload_file)
	        }

	        // Add the form data to the RESTFul request
	        form_data.append('name', recipe_label)
	        form_data.append('type', recipe_type)
	        form_data.append('recipe_desc', recipe_description)
	        form_data.append('prep_time', prep_time)
	        form_data.append('cook_time', cook_time)
	        form_data.append('calories', calories)
	        form_data.append('portions', portions)
	        form_data.append('price', price)
	        form_data.append('ingredients', JSON.stringify(ingredient_list))
	        form_data.append('instructions', JSON.stringify(instruction_list))

            // Send a request to the flask application to create the recipe
            $.ajax(
            {
                type: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                url: '/recipe/create',
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                success: function() {
                    console.log('Recipe submitted');
                    alert('Recipe created successfully')
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Recipe creation failed: ' + errorThrown + ' textStatus = ' + textStatus)
                    alert('Could not create recipe record. Try again later.')
                }
            }
            )
	    }

        // Attach the create recipe function to the create recipe button
	    $('#create_recipe_btn').click(function(e) {
	        e.preventDefault();
            create_recipe();
	    });

        // Attach a function to the Upload photo button to display the selected photo filename
	    $(':file').change(function(e) {
	        e.preventDefault();
	        if (this.files.length > 0) {
	            $('#upload_picture_filename').text(this.files[0].name);
	        }
	    });

	})

})(this.jQuery);