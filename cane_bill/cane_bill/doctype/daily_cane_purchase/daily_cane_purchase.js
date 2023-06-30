// Copyright (c) 2023, quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Cane Purchase', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on('Daily Cane Purchase', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});



frappe.ui.form.on('Daily Cane Purchase', {
	
	show_list: function(frm) {
		frm.call({
				method:'get_cane_weight_data',//function name defined in python
				doc: frm.doc, //current document
			});

	}
});