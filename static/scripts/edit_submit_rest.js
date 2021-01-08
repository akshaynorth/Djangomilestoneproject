(function($){
	$(document).ready(function() {

	    /**
	    * Submits a RESTFull API request to submit edited recipe information
	    */
	    function submit_edit_recipe() {
	        // Gather all the information on the generate cooking directions form

	        // Obtain recipe label
            let recipe_label = $('#recipe_label').val().trim();

            // Verify that the recipe label is not empty
            if (recipe_label.length == 0) {
                alert('Please provide a recipe label.');
                return;
            }

            // Obtain the recipe type and verify that a non-empty recipe type has been provided
            let recipe_type = $('#recipe_type').val().trim();
            if (recipe_type.length == 0) {
                alert('Please provide a selection for the recipe type.')
                return;
            }

            // Obtain recipe description and verify that a non-empty value has been provided
            let recipe_description = $.trim($('#recipe_desc').val());
            if (recipe_description.length == 0) {
                alert('Please provide a recipe description.');
                return;
            }

            // Obtain all the ingredients provided by the user. The ingredients are present in the form as input fields
            // that start with the name property value set to the ingredient_name prefix
            let ingredient_list = []
            $('input[name="ingredient_name"]').each(
                function() {
                    ingredient_list.push($(this).val())
                }
            );

            // Verify that all ingredients input fields have been provided
            for (i in ingredient_list) {
                if (ingredient_list[i].trim().length == 0) {
                    alert('Provide an ingredient description for each of added ingredients');
                    return;
                }
            }

            // Obtain all the instructions provided by the user. The instructions are present in the form as input fields
            // what start with the name property value set to the instructions_desc prefix
            let instruction_list = []
            $('input[name="instruction_desc"]').each(
                function() {
                    instruction_list.push($(this).val())
                }
            );

            // Verify that all instruction input fields were filled out
            for (i in instruction_list) {
                if (instruction_list[i].trim().length == 0) {
                    alert('Provide an instruction description for each of added instructions');
                    return;
                }
            }

            // Obtain the preparation time and verify that a non-empty value has been provided
            let prep_time = $('#prep_time').val().trim()
            if (prep_time.length == 0) {
                alert('Provide a preparation time');
                return;
            }

            // Obtain the recipe cook time and verify that a non-empty value has been provided
            let cook_time = $('#cook_time').val().trim();
            if (cook_time.length == 0) {
                alert('Provide the cooking time');
                return;
            }

            // Obtain the recipe calories and verify that a non-empty value has been provided. The calories provided is
            // assumed to be a string. e.g. (20 cal)
            let calories = $('#calories').val().trim();
            if (calories.length == 0) {
                alert('Provide the recipe calories');
                return;
            }

            // Obtain the recipe portions (aka. servings) and verify that a non-empty value was provided
            let portions = $('#portions').val().trim();
            if (portions.length == 0) {
                alert('Provide the number of portions/servings')
                return;
            }

	        // Send a request to the flask application to create the recipe
	        let form_data = new FormData()
	        if ($('input[type="file"]')[0].files.length > 0) {
	            let upload_file = $('input[type="file"]')[0].files[0]
	            // Add the file object to be sent to the server
	            form_data.append('file', upload_file)
	        }

            // Add the recipe data to be sent in the RESTFul request
	        form_data.append('name', recipe_label)
	        form_data.append('type', recipe_type)
	        form_data.append('recipe_desc', recipe_description)
	        form_data.append('prep_time', prep_time)
	        form_data.append('cook_time', cook_time)
	        form_data.append('calories', calories)
	        form_data.append('portions', portions)
	        form_data.append('ingredients', JSON.stringify(ingredient_list))
	        form_data.append('instructions', JSON.stringify(instruction_list))

            // Send an edit recipe POST request
            $.ajax(
            {
                type: 'POST',
                headers: {'X-CSRFToken': getCookie('csrftoken')},
                url: '/recipe/edit_submit/' + $('#obj_id').val(),
                data: form_data,
                processData: false,
                contentType: false,
                cache: false,
                success: function() {
                    console.log('Recipe update submitted');
                    alert('Recipe updated successfully')
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.log('Recipe creation failed: ' + errorThrown + ' textStatus = ' + textStatus)
                    alert('Could not updated recipe record. Try again later.')
                }
            }
            )

	    }

        // Attach the submit recipe function to the submit recipe button
        $('#submit_recipe_btn').click(function (e) {
            e.preventDefault()
            submit_edit_recipe()
        })

        // Attach a function to the upload recipe photo button to update the field to show the selected photo file name
        $(':file').change(function(e) {
	        e.preventDefault();
	        if (this.files.length > 0) {
	            $('#upload_picture_filename').text(this.files[0].name);
	        }
	    });
	})
})(this.jQuery);