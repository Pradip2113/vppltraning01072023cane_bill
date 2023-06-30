// Copyright (c) 2023, Quantbit and contributors
// For license information, please see license.txt

frappe.ui.form.on('Farmer Loan Application', {
	// refresh: function(frm) {

	// }
});

frappe.ui.form.on('Farmer Loan Application', {
    refresh: function(frm) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper').css('margin-left', '0');
    }
});

frappe.ui.form.on('Farmer Loan Application', {
	loan_amount: function(frm) {
		frm.call({
			method: 'loan_validation',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Farmer Loan Application', {
	loan_type: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
		frm.call({
			method: 'loan_i_p',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Farmer Loan Application', {
	loan_amount: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
		frm.call({
			method: 'loan_amt_installment',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Farmer Loan Application', {
	season: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
		frm.call({
			method: 'season_installment',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Farmer Loan Application', {
	repayment_period_in_years: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
		frm.call({
			method: 'year_installment_installment',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});

frappe.ui.form.on('Farmer Loan Application', {
	rate_of_interest: function(frm) {
		frm.clear_table("installments_table")
		frm.refresh_field('installments_table')
		frm.call({
			method: 'rate_of_interest_installment',//function name defined in python
			doc: frm.doc, //current document
		});

	}
});