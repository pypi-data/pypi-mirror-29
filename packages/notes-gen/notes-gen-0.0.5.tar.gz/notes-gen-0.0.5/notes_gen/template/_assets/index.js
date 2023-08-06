$( document ).ready( function(){

	var app = (function(){

		var selectedCategory = new Set();
		var searchText = '';

		//Setup all event handler
		var init = function(){

			//Event handler
			$('.category').click(handleCategoryClick);
			$('#searchInput').keyup(handleSearchInputKeyUp);
		};


		//Event handler for category
		var handleCategoryClick = function(){

			var isActive = $( this ).hasClass('active');

			//Toggle active class and update filter
			if(isActive===true){
				
				$( this ).removeClass('active');
				selectedCategory.delete($( this ).text());

			}else{

				$( this ).addClass('active');
				selectedCategory.add($( this ).text());
			}

			//Filter Notes
			filterNotes();
		}

		//Filter using isotope
		var handleSearchInputKeyUp = function() {

			searchText = $( this ).val();

			//Filter Notes
			filterNotes();
		}

		//Filter Notes based on catergory and search text
		var filterNotes = function() {

			$('.notes-item').each(function(){
				var title = $( this ).find('.notes-title').text().toLowerCase();
				
				//Get notes category
				var notesCategory = [];
				$( this ).find('.category').each(function(){
					notesCategory.push($( this ).val());
				})

				//Check if match
				var isTitleMatch = (title.indexOf(searchText.toLowerCase()) !== -1);
				var isCategoryPresent = Array.from(selectedCategory).every(function(val){
					return notesCategory.indexOf(val) !== -1;
				});

				//Hide or show notes
				if(isTitleMatch===true && isCategoryPresent===true){
					$( this ).show();
				}else{
					$( this ).hide();
				}

			})

		}

		//Return public methods
		return {
			init: init,
		}

	})();

	app.init();

});