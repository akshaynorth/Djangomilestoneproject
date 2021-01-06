/*----------------------------------------------------*/
/*  SCEditor
/*----------------------------------------------------*/

(function($){
	$(document).ready(function(){

	    /**
	    * Adds an ingredient to the interactive recipe form
	    *
	    * Note:
	    *    This function was altered from the initial template to fix a defect that occurred when all ingredients are
	    *    deleted. When all the ingredients are deleted, there are no rows to clone, therefore the code was not
	    *    able to create a new row. The code below was altered to create a new row when a pre-existing row can not
	    *    be cloned.
	    */
		function addIng() {
		    let newElem = null;

            // If there are any pre-existing ingredients, clone one to build a new ingredient text field
		    if ($("table#ingredients-sort tr").is('*')) {
		        newElem = $('table#ingredients-sort tr.ingredients-cont.ing:first').clone();
		    }
		    else {
		        // There were no pre-existing rows to clone, create a new one
		        newElem = $('<tr class="ingredients-cont ing"><td class="icon"><i class="fa fa-arrows"></i></td><td><input name="ingredient_name" type="text" class="ingredient" placeholder="" /></td><td class="action"><a title="Delete" class="delete" href="#"><i class="fa fa-remove"></i></a></td></tr>');
		    }

            // Clear the value of the ingredient just created getting it ready for user input
            newElem.find('input').val('');

            // Append the new ingredient to the ingredient table rows
			newElem.appendTo('table#ingredients-sort');
		}

        /**
        * Adds a recipe instruction to the interactive recipe form
        *
        * Note:
        *    This function was added from the initial site template to allow the instructions to be added
        *    interactively on a row-per-row basis as the ingredients were. The initial template did not have
        *    this capability and provided a WYSIWYG text area that did not fulfilled the requirements for this project
        */
		function addInstruction() {
		    let newElem = null;

		     // If there are any pre-existing instructions, clone one to build a new ingredient text field
		    if ($("table#instructions-sort tr").is('*')) {
		        newElem = $('table#instructions-sort tr.ingredients-cont.ing:first').clone();
		    }
		    else {
		        // There were no pre-existing rows to clone, create a new one
                newElem = $('<tr class="ingredients-cont ing"><td class="icon"><i class="fa fa-arrows"></i></td><td><input name="instruction_desc" type="text" class="ingredient" placeholder="" /></td><td class="action"><a title="Delete" class="delete" href="#"><i class="fa fa-remove"></i></a></td></tr>');
		    }

             // Clear the value of the ingredient just created getting it ready for user input
            newElem.find('input').val('');

            // Append the new ingredient to the ingredient table rows
			newElem.appendTo('table#instructions-sort');
		}

		//sortable table
		var fixHelper =  function(e, tr) {
		    let $originals = tr.children();
		    let $helper = tr.clone();
		    $helper.children().each(function(index)
		    {
		      // Set helper cell sizes to match the original sizes
		      $(this).width($originals.eq(index).width());
		    });
		    return $helper;
		  };

		// Add functions to add and delete ingredients to the add ingredient and the X buttons, respectively
		if ($("table#ingredients-sort").is('*')) {

		    // Add click action to the add ingredient button
			$('table#ingredients-sort + .add_ingredient').click(function(e){
				e.preventDefault();
				addIng();
			});

			// remove ingredient
			$('#ingredients-sort .delete').live('click',function(e){
				e.preventDefault();
				// Remove the row that was clicked on that is two levels above the button in the DOM
				$(this).parent().parent().remove();
			});

			$('table#ingredients-sort tbody').sortable({
				forcePlaceholderSize: true,
				forceHelperSize: true,
				placeholder : 'sortableHelper',
				helper: fixHelper,
				zIndex: 999990,
				opacity: 0.6,
				tolerance: "pointer"
			});

        }

		// Add functions to add and delete instructions to the add ingredient and the X buttons, respectively
        if ($("table#instructions-sort").is('*')) {

             // Add click action to the add instructions button
			$('table#instructions-sort + .add_ingredient').click(function(e){
				e.preventDefault();
				addInstruction();
			});

			// remove instruction
			$('#instructions-sort .delete').live('click',function(e){
				e.preventDefault();
				$(this).parent().parent().remove();
			});

			$('table#instructions-sort tbody').sortable({
				forcePlaceholderSize: true,
				forceHelperSize: true,
				placeholder : 'sortableHelper',
				helper: fixHelper,
				zIndex: 999990,
				opacity: 0.6,
				tolerance: "pointer"
			});
	 	}
	 	})
})(this.jQuery);