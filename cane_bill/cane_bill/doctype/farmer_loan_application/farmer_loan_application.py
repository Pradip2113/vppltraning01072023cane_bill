# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class FarmerLoanApplication(Document):
	@frappe.whitelist()
	def before_save(self):
		self.loan_validation()
	@frappe.whitelist()
	def loan_validation(self):
		if self.loan_amount and self.maximum_amount:
			if self.loan_amount > self.maximum_amount:
				self.loan_amount=0
				frappe.throw(f"Loan Amount should not be greater than {self.maximum_amount} for Lone Type '{self.loan_type}'")
		

	@frappe.whitelist()
	def loan_i_p(self):
		if self.loan_type and self.season:
			doc=frappe.get_doc("Farmer Loan Type",self.loan_type)
			self.rate_of_interest=doc.rate_of_interest
			self.repayment_period_in_years=doc.period_for_repayment
			self.append_on_installments_table()
		else:
			self.loan_type=""
			frappe.msgprint("Please select 'Posting Season'")
   
   
	@frappe.whitelist()
	def loan_amt_installment(self):
		if self.repayment_period_in_years and self.loan_amount:
			self.append_on_installments_table()

	@frappe.whitelist()
	def season_installment(self):
		if self.loan_amount and self.loan_type and  self.season:
			self.append_on_installments_table()
   
   
	@frappe.whitelist()
	def year_installment_installment(self):
		if self.loan_amount and self.loan_type and self.repayment_period_in_years:
			self.append_on_installments_table()
   
	@frappe.whitelist()
	def rate_of_interest_installment(self):
		if self.loan_amount and self.loan_type and self.repayment_period_in_years and self.rate_of_interest:
			self.append_on_installments_table()
		elif self.loan_amount and self.loan_type and self.repayment_period_in_years and self.rate_of_interest==0:
			self.append_on_installments_table()


	@frappe.whitelist()
	def append_on_installments_table (self):
		if self.loan_amount:
			loan_amt=self.loan_amount
			loan_installment_amt = int(loan_amt)/int(self.repayment_period_in_years)
		else:
			loan_installment_amt=0
   
		if self.rate_of_interest:
			loan_ir=self.rate_of_interest
			# loan_installment_amt = int(loan_amt)/int(self.repayment_period_in_years)
		else:
			loan_ir=0

		if self.season and self.repayment_period_in_years :
			current_year = int(self.season.split("-")[0])
			for i in range(int(self.repayment_period_in_years)):
				season_range = f"{current_year + i}-{current_year + i + 1}"
				self.append("installments_table", {
					"season": season_range,
					"installment": loan_installment_amt,
					"rate_of_interest":loan_ir,
					"interest":"Till The Billing Date",
     
				})
    


	

		
    
# ------------------------------------------------------------------------------------------------------------- 
		# if self.season:
		# 	for _ in range (int(self.repayment_period_in_years)):
		# 		self.append("installments_table",
		# 			{
		# 				"season": "pp",
		# 				"installment":0,
						
		# 			}
		# 		)



# if self.season:
		# 	current_year = int(self.season.split("-")[0])
		# 	installments = []
		# 	for i in range(int(self.repayment_period_in_years)):
		# 		season_range = f"{current_year + i}-{current_year + i + 1}"
		# 		installments.append({
		# 			"season": season_range,
		# 			"installment": 0,
		# 		})
		# 	self.installments_table = installments

