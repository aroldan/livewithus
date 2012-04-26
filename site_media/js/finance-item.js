$(document).ready(function(event) {

jQuery.jQueryRandom = 0;
jQuery.extend(jQuery.expr[":"],
{
    random: function(a, i, m, r) {
        if (i == 0) {
            jQuery.jQueryRandom = Math.floor(Math.random() * r.length);
        };
        return i == jQuery.jQueryRandom;
    }
});

/*
 * Returns true if the currrent finance item is being split evenly.
 * Otherwise, returns false.
*/
function is_even_split () {
	return $("#finance-even-split input:first-child").attr("checked");
}

/*
* Determines if this text field has been touched by the user
* returns true if so
*/
function is_touched() {
	return $(this).data("touched") == "true";
}
function is_untouched() {
	return $(this).data("touched") == "false";
}

function do_uneven_split(event) {
	var amount = $("#create-purchase-form [name=amount]").asNumber();

	var all_targets = $(".finance-person-checkbox input[type=text]");
	var amount_targets = $(".finance-person-checkbox input:checked+[type=text]");
	var clear_targets = $(".finance-person-checkbox input:checkbox").not(":checked");
	var touched_targets = amount_targets.filter(is_touched);
	var untouched_targets = amount_targets.filter(is_untouched);
	
	var computed_total = 0;
	var unused_amount = amount;
	
	all_targets.css("border-top", "1px solid #888");
	all_targets.css("border-left", "1px solid #ccc");
	all_targets.css("border-right", "1px solid #ccc");
	all_targets.css("border-bottom", "1px solid #ccc");
	amount_targets.removeAttr("disabled");
	
	touched_targets.each(function() {
		computed_total += $(this).asNumber();
		$(this).css("background-color", "#fcc");
	});
	
	unused_amount = amount - computed_total;
	
	if((untouched_targets.length == 0 && unused_amount > 0) || unused_amount < 0) {
		// check for error conditions
		untouched_targets.val("$0.00")
		$("#create-purchase-form-error").show();
		
		$("#create-purchase-form-error .current-total").text(computed_total);
		$("#create-purchase-form-error .current-total").formatCurrency();
	} else {
		untouched_targets.val(unused_amount/untouched_targets.length);
		$("#create-purchase-form-error").hide();
	}
	
	untouched_targets.css("background-color", "#ccf");
	untouched_targets.formatCurrency(); // update untouched target amounts
	clear_targets.next("[type=text]").attr("disabled", "disabled");
	clear_targets.next("[type=text]").val(""); // clear unused targets
}


/*
* Set the item total to the computed item total
*/
function revise_total (event) {
	event.preventDefault();
	var amount_target = $("#create-purchase-form [name=amount]");

	var all_targets = $(".finance-person-checkbox input[type=text]");
	
	var computed_total = 0;
	
	all_targets.each(function() {
		computed_total += $(this).asNumber();
	});
	
	amount_target.val(computed_total);
	amount_target.formatCurrency();
	
	do_uneven_split(event);
}

function do_even_split (event) {
	var amount = $("#create-purchase-form [name=amount]").asNumber();
	
	var split_num = $(".finance-person-checkbox input:checked").length;
	
	var all_targets = $(".finance-person-checkbox input[type=text]");
	var amount_targets = $(".finance-person-checkbox input:checked+[type=text]");
	var clear_targets = $(".finance-person-checkbox input:checkbox").not(":checked");
	
	// remove error form and white out fields, just in case
	$("#create-purchase-form-error").hide();
	all_targets.css('background-color', '#fff');
	all_targets.css('border','none');
	
	if(split_num != 0) {
		//divide and format
		amount_targets.val(amount/split_num);
		amount_targets.formatCurrency();
		
		// now make sure we're not off by a cent
		var computed_total = 0;
		amount_targets.each(function() {computed_total += $(this).asNumber()});
		var random_target = amount_targets.filter(":random"); //TODO: actually make this random
		if(computed_total > amount) {
			random_target.val(random_target.asNumber()-0.01);
			random_target.formatCurrency();
		} else if(computed_total < amount) {
			random_target.val(random_target.asNumber()+0.01);
			random_target.formatCurrency();
		}
	}
	clear_targets.next("[type=text]").val(""); // clear unused targets
	all_targets.attr("disabled", "disabled");
}

function blur_text_input(event) {
	if(!is_even_split()) {
		var all_targets = $(".finance-person-checkbox input[type=text]");
		all_targets.formatCurrency();
	}
}

function show_values (event) {
	if($(event.target).is("[name=even_split]") && !is_even_split()) {
		$(".finance-person-checkbox input[type=text]").data("touched", "false"); // set all touched to false
	}

	if(is_even_split()) {
		do_even_split(event);
	} else {
		do_uneven_split(event);
	}
}

$("#create-purchase-form [name=amount]").blur(function() { $(this).formatCurrency() });

//update form values when anything changes
$("#create-purchase-form [name=amount]").keyup(show_values);

if($(document).data("editing") == "true") {
	$(".finance-person-checkbox input[type=text]").data("touched", "true"); // set all touched to true on load if editing a transaction
	$(".finance-person-checkbox input[type=text]").formatCurrency();
} else {
	$(".finance-person-checkbox input[type=text]").data("touched", "false"); // set all touched to false on load
}
$(".finance-person-checkbox input[type=text]").keyup(function(event) { $(this).data("touched", "true"); show_values(event); } ); // set touched values when touched
$(".finance-person-checkbox input[type=text]").blur(blur_text_input);
$("#create-purchase-form input").change(show_values);
show_values(event); // run initial show values

// attach events for errors
$('#link-revise-total').click(revise_total);
$('#link-reset-amounts').click(function(event) {
	event.preventDefault();
	$("#finance-even-split input:first-child").attr("checked", "checked");
	do_even_split(event);
});
	
// attach include everyone event
$('#link-include-everyone').click(function(event) {
	event.preventDefault();
	$('.finance-person-checkbox input:checkbox').attr('checked', 'checked');
	show_values(event);
});
	
// on submit, re-enable all fields
$("#create-purchase-form").submit(function(event) {
	$(this).find("input[type=text]").removeAttr("disabled");
});
	
});