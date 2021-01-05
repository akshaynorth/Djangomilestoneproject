(function($){
	$(document).ready(function() {
	    function create_recipe() {
	        // Gather all the information on the generate cooking directions form
            let recipe_label = $('#recipe_label').val().trim();

            if (recipe_label.length == 0) {
                alert('Please provide a recipe label.');
                return;
            }

            let recipe_type = $('#recipe_type').val().trim();
            if (recipe_type.length == 0) {
                alert('Please provide a selection for the recipe type.')
                return;
            }

            let recipe_description = $.trim($('#recipe_desc').val());

            if (recipe_description.length == 0) {
                alert('Please provide a recipe description.');
                return;
            }

            let ingredient_list = []
            $('input[name="ingredient_name"]').each(
                function() {
                    ingredient_list.push($(this).val())
                }
            );

            for (i in ingredient_list) {
                if (ingredient_list[i].trim().length == 0) {
                    alert('Provide an ingredient description for each of added ingredients');
                    return;
                }
            }

            let instruction_list = []
            $('input[name="instruction_desc"]').each(
                function() {
                    instruction_list.push($(this).val())
                }
            );

            for (i in instruction_list) {
                if (instruction_list[i].trim().length == 0) {
                    alert('Provide an instruction description for each of added instructions');
                    return;
                }
            }

            let prep_time = $('#prep_time').val().trim()
            if (prep_time.length == 0) {
                alert('Provide a preparation time');
                return;
            }

            let cook_time = $('#cook_time').val().trim();
            if (cook_time.length == 0) {
                alert('Provide the cooking time');
                return;
            }

            let calories = $('#calories').val().trim();
            if (calories.length == 0) {
                alert('Provide the recipe calories');
                return;
            }

            let portions = $('#portions').val().trim();
            if (portions.length == 0) {
                alert('Provide the number of portions/servings')
                return;
            }

	        // Send a request to the flask application to create the recipe
	        let form_data = new FormData()
	        if ($('input[type="file"]')[0].files.length > 0) {
	            let upload_file = $('input[type="file"]')[0].files[0]
	            form_data.append('file', upload_file)
	        }

	        form_data.append('name', recipe_label)
	        form_data.append('type', recipe_type)
	        form_data.append('recipe_desc', recipe_description)
	        form_data.append('prep_time', prep_time)
	        form_data.append('cook_time', cook_time)
	        form_data.append('calories', calories)
	        form_data.append('portions', portions)
	        form_data.append('ingredients', JSON.stringify(ingredient_list))
	        form_data.append('instructions', JSON.stringify(instruction_list))

            $.ajax(
            {
                type: 'POST',
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

	    $('#create_recipe_btn').click(function(e) {
	        e.preventDefault();
            create_recipe();
	    });

	    $(':file').change(function(e) {
	        e.preventDefault();
	        if (this.files.length > 0) {
	            $('#upload_picture_filename').text(this.files[0].name);
	        }
	    });

	})

})(this.jQuery);