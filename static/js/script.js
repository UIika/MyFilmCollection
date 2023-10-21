// document.addEventListener('DOMContentLoaded', function () {
// 	var showFormButton = document.getElementById('showFormButton')
// 	var myForm = document.getElementById('importForm')

// 	showFormButton.style.width = '200px'
// 	myForm.style.margin = '10px'

// 	showFormButton.addEventListener('click', function () {
// 		if (myForm.style.display === 'none') {
// 			myForm.style.display = 'block'
// 			showFormButton.textContent = '       Cancel        '
// 		} else {

// 			myForm.style.display = 'none'
// 			showFormButton.textContent = 'Import your watchlist'
// 		}
// 	})
// })

function myFunction(myValue) {
	document.getElementById('currentValue').innerHTML = myValue
}

const outputElement = document.getElementById('liveSearchResults')

jQuery(document).ready(function ($) {
	$('.live-search-list li').each(function () {
		$(this).attr('data-search-term', $(this).text().toLowerCase())
	})

	$('.live-search-box').on('keyup', function () {
		var searchTerm = $(this).val().toLowerCase()
		var visibleItems = 0;

		$('.live-search-list li').each(function () {
			var text = $(this).attr('data-search-term')
			if (text.indexOf(searchTerm) !== -1 || searchTerm.length < 1) {
				outputElement.hidden = false
				if (visibleItems < 5) {
					$(this).show()
					visibleItems++;
				} else {
					$(this).hide()
				}
			} else {
				$(this).hide()
			}
		})
		if (visibleItems === 0 || searchTerm.length < 1) {
			outputElement.hidden = true
		}
	})
})