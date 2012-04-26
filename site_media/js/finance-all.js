$(document).ready(function() {
	
	// set mouseover functions for items in finance list
	$(".finance-row").mouseenter(function() {
		if(!$(this).closest("tr").next("tr").hasClass("finance-row-expanded")) {
			if($(this).hasClass("odd-row")) {
				$(this).css("background", "url(/site_media/img/arrows.png) no-repeat bottom left #eee");
			} else {
				$(this).css("background", "url(/site_media/img/arrows.png) no-repeat bottom left");
			}
		} else {
			// if it's expanded
			if($(this).hasClass("odd-row")) {
				$(this).css("background", "url(/site_media/img/arrows_up.png) no-repeat bottom left #eee");
			} else {
				$(this).css("background", "url(/site_media/img/arrows_up.png) no-repeat bottom left");
			}
		}
	});
	$(".finance-row").mouseleave(function() {
		if($(this).hasClass("odd-row")) {
			$(this).css("background", "#eee");
		} else {
			$(this).css("background", "#fff");
		}
	});
	
	//expand rows when clicked
	$(".finance-row").click(function() {
		// clear arrows from row
		if($(this).hasClass("odd-row")) {
			$(this).css("background", "#eee");
		} else {
			$(this).css("background", "#fff");
		}
		
		//add in a new row
		if($(this).closest("tr").next("tr").hasClass("finance-row-expanded")) {
			var expanded_row = $(this).closest("tr").next(".finance-row-expanded");
			expanded_row.fadeOut('fast', function() {
			expanded_row.remove();
			});
		} else {
			// create the row
			$(this).closest("tr").after('<tr class="finance-row-expanded"><td class="finance-is-mine-icon"></td><td colspan="4" class="finance-detail-cell"><div class="finances-loading">Loading...</div></td></tr>');
			var theNewRow = $(this).closest("tr").next(".finance-row-expanded");
			
			// set attribute of new row, and add up arrows to just expanded row
			if($(this).hasClass("odd-row")) {
				theNewRow.addClass("odd-row");
				$(this).css("background", "url(/site_media/img/arrows_up.png) no-repeat bottom right #eee");
			} else {
				$(this).css("background", "url(/site_media/img/arrows_up.png) no-repeat bottom right");
			}
			theNewRow.fadeIn(); // now fade it in
			
			// now load new contents all AJAX-like
			var theNewCell = theNewRow.children(".finance-detail-cell");
			var load_url = $(this).closest("tr").children(".finance-description").children(".finance-details-link").attr("href");
			theNewCell.load(load_url, {}, function() {
				theNewCell.children(".finances-loading").remove();
			});
			
			// now attach mouseover actions to the new row
			theNewRow.mouseover(function() {
				var old_row = $(this).closest("tr").prev(".finance-row");
				if($(this).hasClass("odd-row")) {
					old_row.css("background", "url(/site_media/img/arrows_up.png) no-repeat bottom right #eee");
				} else {
					old_row.css("background", "url(/site_media/img/arrows_up.png) no-repeat bottom right");
				}
			});
			theNewRow.mouseleave(function() {
				var old_row = $(this).closest("tr").prev(".finance-row");
				if($(this).hasClass("odd-row")) {
					old_row.css("background", "#eee");
				} else {
					old_row.css("background", "#fff");
				}
			});
			
			// attach click events to the new row
			theNewRow.click(function() {
				var old_row = $(this).closest("tr").prev(".finance-row");
				
				// clear arrows
				if($(this).hasClass("odd-row")) {
					old_row.css("background", "#eee");
				} else {
					old_row.css("background", "#fff");
				}
				
				$(this).fadeOut('fast', function() {
					$(this).remove();
				});
			});
		}
	});
});