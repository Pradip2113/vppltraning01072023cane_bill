# Copyright (c) 2023, quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class DailyCanePurchase(Document):
	@frappe.whitelist()
	def get_cane_weight_data(self):
		# doc = frappe.get_all('Cane Weight', filters={'docstatus': 1,'date': self.date}, fields={"actual_weight","farmer_code" }   , limit=100  )
  
  
		doc= [

 {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'},
 {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'},
 {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'},
 {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'},
 {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1.762, 'farmer_code': 'FA-148025'},
 {'actual_weight': 1.762, 'farmer_code': 'FA-148025'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'},
 {'actual_weight': 2, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'},
 {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'},
 {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'},
 {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'},
 {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 1, 'farmer_code': 'FA-144490'}, {'actual_weight': 2.297, 'farmer_code': 'FA-139708'},
 {'actual_weight': 2.297, 'farmer_code': 'FA-139708'}, {'actual_weight': 2.297, 'farmer_code': 'FA-139708'}, {'actual_weight': 2.297, 'farmer_code': 'FA-139708'}, {'actual_weight': 2.297, 'farmer_code': 'FA-139708'},
 {'actual_weight': 2.297, 'farmer_code': 'FA-139708'}, {'actual_weight': 2.297, 'farmer_code': 'FA-139708'}, {'actual_weight': 2.297, 'farmer_code': 'FA-139708'}, {'actual_weight': 2.297, 'farmer_code': 'FA-139708'},
 {'actual_weight': 2.297, 'farmer_code': 'FA-139708'}, {'actual_weight': 15.84, 'farmer_code': 'FA-136810'}, {'actual_weight': 15.84, 'farmer_code': 'FA-136810'}, {'actual_weight': 15.84, 'farmer_code': 'FA-136810'},
 {'actual_weight': 15.84, 'farmer_code': 'FA-136810'}, {'actual_weight': 15.84, 'farmer_code': 'FA-136810'}, {'actual_weight': 15.84, 'farmer_code': 'FA-136810'}, {'actual_weight': 15.84, 'farmer_code': 'FA-136810'},
 {'actual_weight': 15.84, 'farmer_code': 'FA-136810'}, {'actual_weight': 2.653, 'farmer_code': 'FA-136118'}, {'actual_weight': 2.653, 'farmer_code': 'FA-136118'}, {'actual_weight': 2.653, 'farmer_code': 'FA-136118'},
 {'actual_weight': 2.653, 'farmer_code': 'FA-136118'}, {'actual_weight': 2.653, 'farmer_code': 'FA-136118'}, {'actual_weight': 2.653, 'farmer_code': 'FA-136118'}, {'actual_weight': 2.653, 'farmer_code': 'FA-136118'},
 {'actual_weight': 2.653, 'farmer_code': 'FA-136118'}, {'actual_weight': 11.573, 'farmer_code': 'FA-126503'}, {'actual_weight': 11.573, 'farmer_code': 'FA-126503'}, {'actual_weight': 11.573, 'farmer_code': 'FA-126503'},
 {'actual_weight': 11.573, 'farmer_code': 'FA-126503'}, {'actual_weight': 8.653, 'farmer_code': 'FA-116862'}, {'actual_weight': 8.653, 'farmer_code': 'FA-116862'}, {'actual_weight': 9.464, 'farmer_code': 'FA-116706'},
 {'actual_weight': 9.464, 'farmer_code': 'FA-116706'}, {'actual_weight': 9.464, 'farmer_code': 'FA-116706'}, {'actual_weight': 9.464, 'farmer_code': 'FA-116706'}, {'actual_weight': 9.464, 'farmer_code': 'FA-116706'},
 {'actual_weight': 9.464, 'farmer_code': 'FA-116706'}, {'actual_weight': 9.464, 'farmer_code': 'FA-116706'}, {'actual_weight': 9.464, 'farmer_code': 'FA-116706'}, {'actual_weight': 9.464, 'farmer_code': 'FA-116706'},
 {'actual_weight': 9.464, 'farmer_code': 'FA-116706'}, {'actual_weight': 10.098, 'farmer_code': 'FA-110099'}, {'actual_weight': 2.138, 'farmer_code': 'FA-99133'}, {'actual_weight': 2.138, 'farmer_code': 'FA-99133'}, 
 {'actual_weight': 2.138, 'farmer_code': 'FA-99133'}, {'actual_weight': 2.138, 'farmer_code': 'FA-99133'}, {'actual_weight': 2.138, 'farmer_code': 'FA-99133'}, {'actual_weight': 2.138, 'farmer_code': 'FA-99133'},
 {'actual_weight': 2.138, 'farmer_code': 'FA-99133'}, {'actual_weight': 2.138, 'farmer_code': 'FA-99133'}, {'actual_weight': 2.138, 'farmer_code': 'FA-99133'}, {'actual_weight': 2.138, 'farmer_code': 'FA-99133'},
 {'actual_weight': 2.138, 'farmer_code': 'FA-99133'}, {'actual_weight': 2.901, 'farmer_code': 'FA-95265'}, {'actual_weight': 2.901, 'farmer_code': 'FA-95265'}, {'actual_weight': 2.901, 'farmer_code': 'FA-95265'}]
  
  
  
  
  
		frappe.msgprint(str(doc))
		moc = [{'farmer_code': code, 'actual_weight': sum(record['actual_weight'] for record in doc if record['farmer_code'] == code)} for code in set(record['farmer_code'] for record in doc)]
		frappe.msgprint(str(moc))




 