# Copyright (c) 2023, Quantbit and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate
from frappe.model.document import Document

from datetime import datetime


class CaneBilling(Document):
    # ------------------------------------------------------------------------------------------------------------

    @frappe.whitelist()
    def vivek(self):
        # **********if you want to change or any kind of update in this method the make sure check other method because data is filter from this metod used to change billing_status from Cane Weight
        farmer_list_in_date = []
        doc = frappe.db.get_list(
            "Cane Weight",
            filters={
                "docstatus": 1,
                "date": ["between", [self.from_date, self.to_date]],
                "billing_status": 0,
            },
            fields=[
                "farmer_name",
                "farmer_village",
                "date",
                "farmer_code",
                "docstatus",
                "billing_status",
            ],
        )
        # frappe.msgprint(str(doc))
        for d in doc:
            # if str(self.from_date) <= str(d.date) <= str(self.to_date) and d.docstatus == 1 and d.billing_status == 0:  #*****please do not remove this commented line contact vivek.kumbhar@erpdata.in
            farmer_list_in_date.append(
                {
                    "farmer_name": d.farmer_name,
                    "farmer_code": d.farmer_code,
                    "farmer_village": d.farmer_village,
                    "date": d.date,
                }
            )
        # frappe.msgprint(str(farmer_list_in_date))

        existing_farmer_codes = [
            ft.farmer_code for ft in self.farmer_table
        ]  # Get existing farmer codes in the child table

        for farmer in farmer_list_in_date:
            if farmer["farmer_code"] not in existing_farmer_codes:
                farmer_table = self.append("farmer_table", {})
                farmer_table.farmer_name = farmer["farmer_name"]
                farmer_table.farmer_id = farmer["farmer_code"]
                farmer_table.village = farmer["farmer_village"]
                farmer_table.date = farmer["date"]
                existing_farmer_codes.append(
                    farmer["farmer_code"]
                )  # Add the farmer code to the existing farmer codes list

        # frappe.msgprint(str(farmer_list_in_date))

    @frappe.whitelist()
    def selectall(self):
        # pass
        children = self.get("farmer_table")
        if not children:
            return
        all_selected = all([child.check for child in children])
        value = 0 if all_selected else 1
        for child in children:
            child.check = value

    @frappe.whitelist()
    def billing(self):
        for FAR in self.get("farmer_table"):
            total_weight = 0
            cane_rate = 0
            Total_collection_amount = 0
            total_deduction = 0
            sales_invoice_deduction = 0
            sales_invoices = []
            loan_installment_amount = 0
            loan_interest_amount = 0
            loan_installment = []
            loan_installment_intrest = []
            all_deduction = []
            total_payable = 0

            cane_price = frappe.get_all(
                "Item Price",
                filters={"item_code": "Sugar Cane"},
                fields={"valid_from", "valid_upto", "price_list_rate"},
            )
            for c_p in cane_price:
                if str(self.from_date) >= str(c_p.valid_from) and str(
                    self.to_date
                ) <= str(c_p.valid_upto):
                    cane_rate = c_p.price_list_rate  # /1000
                    break
            if cane_rate == 0:
                frappe.throw(
                    f" Please set Proper Item Price for Item 'Sugar Cane' which is in range of  {str(self.from_date)}  and {self.to_date}"
                )

            if FAR.check:
                # in doc all document are collcted from 'Cane Weight' where farmer is FAR.farmer_id
                doc = frappe.get_all("Cane Weight",
                                                    filters={
                                                        "docstatus": 1,
                                                        "date": ["between", [self.from_date, self.to_date]],
                                                        "billing_status": 0,
                                                        "farmer_code": FAR.farmer_id,
                                                    },
                                                    fields={"actual_weight", "farmer_code"},)
                for d in doc:
                    if d.actual_weight:
                        total_weight += round((float(d.actual_weight) / 1000), 2)  # here all cane weight,s  will calculate

                Total_collection_amount = total_weight * cane_rate

                # in deduction_doc all document are collcted  from 'Sales Invoice' where farmer is FAR.farmer_id and status are ['Unpaid', 'Overdue', 'Partly Paid']
                if self.includes_sales_invoice_deduction:
                    deduction_doc = frappe.get_all("Sales Invoice",
                                                                    filters={"customer": FAR.farmer_id,"status": ["in", ["Unpaid", "Overdue", "Partly Paid"]],},
                                                                    fields=["outstanding_amount", "customer", "name", "debit_to"],)
                    
                    sales_invoices = [{"Sales invoice ID": d_d.name,"Outstanding Amount": d_d.outstanding_amount,"Account": d_d.debit_to,}for d_d in deduction_doc]  # in this list all sales invoice will recored with there accound and outstanding_amount info
                    sales_invoice_deduction = sum(int(d["Outstanding Amount"]) for d in sales_invoices)  # calculating sum of all sales invoice

                if self.includes_loan_installment:
                    loan_doc = frappe.get_all("Farmer Loan",
                                                filters={"applicant_id": FAR.farmer_id,"docstatus": 1,},
                                                fields=["name","applicant_id","account_paid_to","account_interest_paid_to",],)
                    for l_d in loan_doc:
                        loan_doc_child = frappe.get_all("Child Farmer Loan",
                                                                            filters={"parent": l_d.name,"docstatus": 1,},
                                                                            fields=["name","season","installment","rate_of_interest","interest","from_date_interest_calculation",
                                                                                    "interest_calculate_on_amount","installment_status","interest_status","paid_installment"],)
                        for l_d_c in loan_doc_child:
                            if str(self.season) == str(l_d_c.season):
                                if str(l_d_c.installment_status) == "1":
                                    (l_d_c.installment) = 0
                                    (l_d_c.paid_installment) =0
                                loan_installment_amount=loan_installment_amount+round((float(l_d_c.installment)-float(l_d_c.paid_installment)),2)   # loan_installment_amount = loan_installment_amount + int(l_d_c.installment)
                                if round((float(l_d_c.installment)-float(l_d_c.paid_installment)),2) > 0:
                                    loan_installment.append({
                                                                "Farmer Loan ID": l_d.name,
                                                                "Farmer ID": l_d.applicant_id,
                                                                "season": l_d_c.season,
                                                                "Account": l_d.account_paid_to,
                                                                "Installment Amount":round((float(l_d_c.installment)-float(l_d_c.paid_installment)),2),
                                                            })

                if self.includes_loan_interest:
                    loan_doc_int = frappe.get_all("Farmer Loan",
                                                                filters={"applicant_id": FAR.farmer_id,"docstatus": 1,},
                                                                fields=["name","applicant_id","account_paid_to","account_interest_paid_to",],)
                    for l_d in loan_doc_int:
                        loan_doc_child_int = frappe.get_all("Child Farmer Loan",
                                                                            filters={"parent": l_d.name,"docstatus": 1,},
                                                                            fields=["name","season","installment","rate_of_interest","interest","from_date_interest_calculation",
                                                                                    "interest_calculate_on_amount","installment_status","interest_status",],)
                        for l_d_c in loan_doc_child_int:
                            p = 0
                            if str(self.season) == str(l_d_c.season):
                                p = round(
                                    float(l_d_c.interest_calculate_on_amount)
                                    * (float(l_d_c.rate_of_interest) / 100)
                                    * (
                                        (
                                            datetime.strptime(self.to_date, "%Y-%m-%d")
                                            - datetime.strptime(
                                                (
                                                    str(
                                                        l_d_c.from_date_interest_calculation
                                                    )
                                                ),
                                                "%Y-%m-%d",
                                            )
                                        ).days
                                        / 365
                                    ),
                                    2,
                                )
                                if str(l_d_c.interest_status) == "1":
                                    p = 0
                                loan_interest_amount = loan_interest_amount + p
                                loan_installment_intrest.append(
                                    {
                                        "Farmer Loan ID": l_d.name,
                                        "Farmer ID": l_d.applicant_id,
                                        "season": l_d_c.season,
                                        "Account": l_d.account_interest_paid_to,
                                        "Installment Interest Amount": p,
                                    }
                                )

                total_deduction = (
                    sales_invoice_deduction
                    + loan_installment_amount
                    + loan_interest_amount
                )
                total_payable = float(Total_collection_amount) - float(total_deduction)

                if total_payable < 0:
                    doc_acc = frappe.get_all(
                        "Account Priority Child",
                        fields={"priority_account", "idx"},
                        order_by="idx ASC",
                    )  # frappe.msgprint(str(doc_acc))
                    all_deduction = (
                        sales_invoices + loan_installment + loan_installment_intrest
                    )  # frappe.msgprint(str(all_deduction))
                    all_deduction = sorted(
                        all_deduction,
                        key=lambda x: next(
                            (
                                item["idx"]
                                for item in doc_acc
                                if item["priority_account"] == x["Account"]
                            ),
                            len(doc_acc) + 1,
                        ),
                    )
                    while float(Total_collection_amount) < float(total_deduction):
                        last_poped_entry = all_deduction.pop(-1)
                        total_sum = float(
                            sum(
                                [
                                    entry.get("Outstanding Amount", 0)
                                    + float(entry.get("Installment Amount", 0))
                                    + float(entry.get("Installment Interest Amount", 0))
                                    for entry in all_deduction
                                ]
                            )
                        )

                        total_deduction = float(total_sum)
                        total_payable = float(Total_collection_amount) - float(
                            total_deduction
                        )

                    contains_key = next(
                        (
                            key
                            for key in [
                                "Outstanding Amount",
                                "Installment Amount",
                                "Installment Interest Amount",
                            ]
                            if key in last_poped_entry
                        ),
                        None,
                    )
                    if (str(contains_key)) == "Outstanding Amount":
                        new_outstanding_amount = round(float(total_payable), 2)
                        total_deduction = round(
                            (float(total_deduction) + float(total_payable)), 2
                        )
                        total_payable = 0
                        last_poped_entry["Outstanding Amount"] = new_outstanding_amount
                        all_deduction.append(last_poped_entry)

                    loan_installment_amount = sum(
                        float(record["Installment Amount"])
                        for record in all_deduction
                        if "Installment Amount" in record
                    )
                    loan_interest_amount = sum(
                        float(record["Installment Interest Amount"])
                        for record in all_deduction
                        if "Installment Interest Amount" in record
                    )
                    sales_invoice_deduction = sum(
                        float(record["Outstanding Amount"])
                        for record in all_deduction
                        if "Outstanding Amount" in record
                    )

                    loan_installment = [
                        record
                        for record in all_deduction
                        if "Installment Amount" in record
                    ]
                    loan_installment_intrest = [
                        record
                        for record in all_deduction
                        if "Installment Interest Amount" in record
                    ]
                    sales_invoices = [
                        record
                        for record in all_deduction
                        if "Outstanding Amount" in record
                    ]

                self.append(
                    "calculation_table",
                    {
                        "farmer_name": FAR.farmer_name,
                        "farmer_id": FAR.farmer_id,
                        "village": FAR.village,
                        "total_weight": total_weight,
                        "rate_kg": cane_rate,
                        "total_collection_amount": Total_collection_amount,
                        "sales_invoice_deduction": sales_invoice_deduction,
                        "lone_deduction": loan_installment_amount,
                        "loan_interest_deduction": loan_interest_amount,
                        "total_deduction": total_deduction,
                        "total_payable_amount": total_payable,
                        "sales_invoice_information": str(sales_invoices),
                        "farmer_loan_information": str(loan_installment),
                        "farmer_loan_interest_information": str(
                            loan_installment_intrest
                        ),
                    },
                )

    @frappe.whitelist()
    def before_save(self):
        self.bill_status_change_of_cane_weight()

    @frappe.whitelist()
    def on_trash(self):
        self.bill_status_change_of_cane_weight_on_cancel()

    @frappe.whitelist()
    def before_submit(self):
        self.bill_status_change_of_cane_weight()
        self.je_of_sales_invoice_and_farmer_loan()
        self.change_status_of_farmer_loan()
        self.set_date_in_farmer_loan_child_for_next_installment()

    @frappe.whitelist()
    def before_cancel(self):
        self.bill_status_change_of_cane_weight_on_cancel()
        self.cancel_journal_entry()
        self.change_status_of_farmer_loan_on_cancel()
        self.set_date_in_farmer_loan_child_for_next_installment_on_cancel()

    @frappe.whitelist()
    def bill_status_change_of_cane_weight(self):
        pop = self.get("calculation_table")
        for p in pop:
            cane_weight_docs = frappe.get_all(
                "Cane Weight",
                filters={
                    "farmer_code": p.farmer_id,
                    "date": ["between", [self.from_date, self.to_date]],
                    "docstatus": 1,
                    "billing_status": 0,
                },
                fields=["farmer_code", "date", "name"],
            )
            # frappe.msgprint(str(cane_weight_docs))
            for k in cane_weight_docs:
                frappe.db.set_value("Cane Weight", k.name, "billing_status", 1)

    @frappe.whitelist()
    def bill_status_change_of_cane_weight_on_cancel(self):
        # frappe.msgprint("fgehwfqshjefhjf")
        non = self.get("calculation_table")
        for q in non:
            cane_weight_docs_c = frappe.get_all(
                "Cane Weight",
                filters={
                    "farmer_code": q.farmer_id,
                    "date": ["between", [self.from_date, self.to_date]],
                    "docstatus": 1,
                    "billing_status": 1,
                },
                fields=["farmer_code", "date", "name"],
            )
            # frappe.msgprint(str(cane_weight_docs))
            for t in cane_weight_docs_c:
                frappe.db.set_value("Cane Weight", t.name, "billing_status", 0)

    @frappe.whitelist()
    def je_of_sales_invoice_and_farmer_loan(self):
        # frappe.msgprint("str(s.sales_invoice_deduction)")
        doc_acc = frappe.get_doc("Account Priority", "Account Priority")
        company = str(doc_acc.company)
        acc_to_set_debit_side = str(doc_acc.debit_in_account_currency)

        for s in self.get("calculation_table"):
            list_data_se = []
            list_data_lo = []
            list_data_li = []
            if s.total_deduction:
                list_data_se = eval(s.sales_invoice_information)
                list_data_lo = eval(s.farmer_loan_information)
                list_data_li = eval(s.farmer_loan_interest_information)
                # frappe.msgprint(str(list_data_se))
                # ------------------------------------------------------------
                je = frappe.new_doc("Journal Entry")
                je.voucher_type = "Journal Entry"
                je.company = company
                je.posting_date = self.today
                je.append(
                    "accounts",
                    {
                        "account": acc_to_set_debit_side,
                        "party_type": "Supplier",
                        "party": s.farmer_id,
                        "debit_in_account_currency": s.total_deduction,
                    },
                )
                if list_data_se:
                    for data_se in list_data_se:
                        je.append(
                            "accounts",
                            {
                                "account": data_se["Account"],
                                "party_type": "Customer",
                                "party": s.farmer_id,
                                "credit_in_account_currency": data_se[
                                    "Outstanding Amount"
                                ],
                                "reference_type": "Sales Invoice",
                                "reference_name": data_se["Sales invoice ID"],
                            },
                        )
                if list_data_lo:
                    for data_lo in list_data_lo:
                        je.append(
                            "accounts",
                            {
                                "account": data_lo["Account"],
                                "party_type": "Supplier",
                                "party": s.farmer_id,
                                "credit_in_account_currency": data_lo[
                                    "Installment Amount"
                                ],
                            },
                        )
                if list_data_li:
                    for data_li in list_data_li:
                        if int(data_li["Installment Interest Amount"]) != 0:
                            je.append(
                                "accounts",
                                {
                                    "account": data_li["Account"],
                                    "party_type": "Supplier",
                                    "party": s.farmer_id,
                                    "credit_in_account_currency": data_li[
                                        "Installment Interest Amount"
                                    ],
                                    # "cost_center":"Main - VPPL",
                                },
                            )
                je.insert()
                je.save()
                je.submit()
                journal_entry = frappe.db.get_all(
                    "Journal Entry", fields=["name"], order_by="creation DESC", limit=1
                )
                s.journal_entry_id = str(journal_entry[0].name)
                # frappe.msgprint(str(journal_entry[0].name))
                # --------------------------------------------------------------------

    @frappe.whitelist()
    def cancel_journal_entry(self):
        for s in self.get("calculation_table"):
            if s.journal_entry_id:
                doc = frappe.get_doc("Journal Entry", (str(s.journal_entry_id)))
                doc.cancel()

                # ------------------------------------------------------------------------

    @frappe.whitelist()
    def change_status_of_farmer_loan(self):
        # ************Please set condition here to set filter here*********************
        if self.includes_loan_installment:
            for s in self.get("calculation_table"):
                list_data_lo = []
                list_data_lo = eval(s.farmer_loan_information)
                for data_lo in list_data_lo:
                    child_doc_farmer_loan = frappe.get_all(
                        "Child Farmer Loan",
                        filters={
                            "parent": data_lo["Farmer Loan ID"],
                            "season": data_lo["season"],
                        },
                        fields=["name", "installment"],
                    )
                    for d in child_doc_farmer_loan:
                        frappe.db.set_value(
                            "Child Farmer Loan", d.name, "installment_status", 1
                        )

        if self.includes_loan_interest:
            for s in self.get("calculation_table"):
                list_data_lo = []
                list_data_lo = eval(s.farmer_loan_information)
                for data_lo in list_data_lo:
                    child_doc_farmer_loan = frappe.get_all(
                        "Child Farmer Loan",
                        filters={
                            "parent": data_lo["Farmer Loan ID"],
                            "season": data_lo["season"],
                        },
                        fields=["name", "installment"],
                    )
                    for d in child_doc_farmer_loan:
                        frappe.db.set_value(
                            "Child Farmer Loan", d.name, "interest_status", 1
                        )

    @frappe.whitelist()
    def change_status_of_farmer_loan_on_cancel(self):
        # ************Please set condition here to set filter here*********************
        if self.includes_loan_installment:
            for s in self.get("calculation_table"):
                list_data_lo = []
                list_data_lo = eval(s.farmer_loan_information)
                for data_lo in list_data_lo:
                    child_doc_farmer_loan = frappe.get_all(
                        "Child Farmer Loan",
                        filters={
                            "parent": data_lo["Farmer Loan ID"],
                            "season": data_lo["season"],
                        },
                        fields=["name", "installment"],
                    )
                    for d in child_doc_farmer_loan:
                        frappe.db.set_value(
                            "Child Farmer Loan", d.name, "installment_status", 0
                        )

        if self.includes_loan_interest:
            for s in self.get("calculation_table"):
                list_data_lo = []
                list_data_lo = eval(s.farmer_loan_information)
                for data_lo in list_data_lo:
                    child_doc_farmer_loan = frappe.get_all(
                        "Child Farmer Loan",
                        filters={
                            "parent": data_lo["Farmer Loan ID"],
                            "season": data_lo["season"],
                        },
                        fields=["name", "installment"],
                    )
                    for d in child_doc_farmer_loan:
                        frappe.db.set_value(
                            "Child Farmer Loan", d.name, "interest_status", 0
                        )

                # -------------------------------------------------------------------------

    @frappe.whitelist()
    def set_date_in_farmer_loan_child_for_next_installment(self):
        for s in self.get("calculation_table"):
            list_data_lo = []
            list_data_lo = eval(s.farmer_loan_information)
            next_seasons = "\n".join(
                [
                    str(int(season["season"].split("-")[1]) + 0)
                    + "-"
                    + str(int(season["season"].split("-")[1]) + 1)
                    for season in list_data_lo
                ]
            )
            for data_lo in list_data_lo:
                child_doc_farmer_loan = frappe.get_all(
                    "Child Farmer Loan",
                    filters={
                        "parent": data_lo["Farmer Loan ID"],
                        "season": next_seasons,
                    },
                    fields=["name", "installment"],
                )
                for d in child_doc_farmer_loan:
                    frappe.db.set_value(
                        "Child Farmer Loan",
                        d.name,
                        "from_date_interest_calculation",
                        self.to_date,
                    )
                # --------------------------------------------------------------------------------

    @frappe.whitelist()
    def set_date_in_farmer_loan_child_for_next_installment_on_cancel(self):
        for s in self.get("calculation_table"):
            list_data_lo = []
            list_data_lo = eval(s.farmer_loan_information)
            next_seasons = "\n".join(
                [
                    str(int(season["season"].split("-")[1]) + 0)
                    + "-"
                    + str(int(season["season"].split("-")[1]) + 1)
                    for season in list_data_lo
                ]
            )
            for data_lo in list_data_lo:
                child_doc_farmer_loan = frappe.get_all(
                    "Child Farmer Loan",
                    filters={
                        "parent": data_lo["Farmer Loan ID"],
                        "season": next_seasons,
                    },
                    fields=["name", "installment"],
                )
                for d in child_doc_farmer_loan:
                    frappe.db.set_value(
                        "Child Farmer Loan",
                        d.name,
                        "from_date_interest_calculation",
                        None,
                    )

    @frappe.whitelist()
    def test_method_trigger_on_button_on_submit_event_call(self):
        frappe.msgprint("hgjg")
        doc_acc = frappe.get_doc("Account Priority", "Account Priority")
        frappe.msgprint(str(doc_acc.company))
        # for d in doc_acc:
        #     frappe.msgprint(d.name)
        # sales_invoices = []
        # loan_installment = []
        # loan_installment_intrest=[]
        # all_deduction=[{'idx': 1, 'priority_account': '12300000 - Trade Receivables - VPPL'}, {'idx': 2, 'priority_account': '52100009 - Interest Received (Bank) - VPPL'}, {'idx': 3, 'priority_account': '12520012 - Advance For Seeds - VPPL'}, {'idx': 4, 'priority_account': '10000000 - Application Of Funds(Assets) - VPPL'}, {'idx': 5, 'priority_account': '11111102 - Land At Narande - VPPL'}, {'idx': 6, 'priority_account': '11000000 - Non-Current Assets - VPPL'}, {'idx': 7, 'priority_account': '11000000 - Non-Current Assets - VPPL'}]

        # sales_invoices = [{'Sales invoice ID': 'SI/B/23-24/00022', 'Outstanding Amount': 38224.0, 'Account Debit To': '12300000 - Trade Receivables - VPPL'}]
        # loan_installment = [{'Farmer Loan ID': 'LOAN-FA-1002-2023-57655', 'Farmer ID': 'FA-1002', 'season': '2022-2023', 'Account': '11430001 - Advance For Irrigation Loan - VPPL', 'Installment Amount': '5400'}, {'Farmer Loan ID': 'LOAN-FA-1002-2023-57654', 'Farmer ID': 'FA-1002', 'season': '2022-2023', 'Account': '11430001 - Advance For Irrigation Loan - VPPL', 'Installment Amount': '10000'}]
        # loan_installment_intrest=  [{'Farmer Loan ID': 'LOAN-FA-1002-2023-57655', 'Farmer ID': 'FA-1002', 'season': '2022-2023', 'Account of intrest': '52100009 - Interest Received (Bank) - VPPL', 'Installment Interest Amount': 1560.82}, {'Farmer Loan ID': 'LOAN-FA-1002-2023-57654', 'Farmer ID': 'FA-1002', 'season': '2022-2023', 'Account of intrest': '52100009 - Interest Received (Bank) - VPPL', 'Installment Interest Amount': 1445.21}]

        # if sales_invoices :
        #         for d in all_deduction:
        #             frappe.msgprint(str(d['idx']))

        # for s in self.get("calculation_table"):
        #     list_data_lo =[]
        #     list_data_lo = eval(s.farmer_loan_information)
        #     next_seasons = ('\n'.join([str(int(season['season'].split('-')[1]) + 0) + '-' + str(int(season['season'].split('-')[1]) + 1) for season in list_data_lo]))
        #     for data_lo in list_data_lo:
        #         child_doc_farmer_loan=frappe.get_all('Child Farmer Loan', filters={'parent': data_lo['Farmer Loan ID'],'season':"2025-2026"}, fields=['name','installment'])
        #         for d in child_doc_farmer_loan:
        #             frappe.db.set_value("Child Farmer Loan",d.name,"from_date_interest_calculation",None)

        # for s in self.get("calculation_table"):
        #     list_data_lo =[]
        #     list_data_lo = eval(s.farmer_loan_information)
        #     for data_lo in list_data_lo:
        #         child_doc_farmer_loan=frappe.get_all('Child Farmer Loan', filters={'parent': data_lo['Farmer Loan ID'],'season':data_lo['season']}, fields=['name','installment'])
        #         for d in child_doc_farmer_loan:
        #             frappe.db.set_value("Child Farmer Loan",d.name,"installment_status",0)
        #             frappe.db.set_value("Child Farmer Loan",d.name,"interest_status",0)

        # frappe.msgprint('days_between')
        # days_between = (datetime.strptime(self.to_date, "%Y-%m-%d") - datetime.strptime(self.from_date, "%Y-%m-%d")).days
        # frappe.msgprint(str(days_between))
        # pass
        # for s in self.get("calculation_table"):
        #     list_data_se =[]
        #     list_data_lo =[]
        #     if s.sales_invoice_deduction:
        #         list_data_se = eval(s.sales_invoice_information)
        #         list_data_lo = eval(s.farmer_loan_information)
        #         # frappe.msgprint(str(list_data_se))
        #         # ------------------------------------------------------------
        #         je = frappe.new_doc("Journal Entry")
        #         je.voucher_type = "Journal Entry"
        #         je.company = "Venkateshwara Power Projects LTD."
        #         je.posting_date = self.today
        #         je.append(
        #             "accounts",
        #             {
        #                 "account": "22200001 - Cane Bill Payable - VPPL",
        #                 "party_type": "Supplier",
        #                 "party": s.farmer_id,
        #                 "debit_in_account_currency": s.total_deduction
        #             },
        #         )
        #         for data_se in list_data_se:
        #             je.append(
        #                 "accounts",
        #                 {
        #                     "account": data_se['Account Debit To'],
        #                     "party_type": "Customer",
        #                     "party": s.farmer_id,
        #                     "credit_in_account_currency": data_se['Outstanding Amount'],
        #                     "reference_type": "Sales Invoice",
        #                     "reference_name": data_se['Sales invoice ID'],
        #                 },
        #             )

        #         for data_lo in list_data_lo:
        #             je.append(
        #                 "accounts",
        #                 {
        #                     "account": data_lo['Account'],
        #                     "party_type": "Customer",
        #                     "party": s.farmer_id,
        #                     "credit_in_account_currency": data_lo['Installment Amount'],
        #                 },
        #             )
        #         je.insert()
        #         je.save()
        #         je.submit()

        # self.je_of_sales_invoice()
        # loan_doc = frappe.get_all('Farmer Loan', filters={'applicant_id': "FA-58", 'docstatus':1 ,}, fields=['name',])
        # for l_d in loan_doc:
        #     loan_doc_child = frappe.get_all('Child Farmer Loan', filters={'parent': l_d.name, 'docstatus':1 ,}, fields=['name','season', 'installment', 'rate_of_interest', 'interest'])
        #     for l_d_c in loan_doc_child:
        #         if str(self.season)==str(l_d_c.season):
        #             frappe.msgprint(str(l_d_c.installment))

        # Alldoc_BMC = frappe.get_all("Batch Milk Collection", filters=None, fields=["name","first_date","last_date","branch_id"])
        # for BMC in Alldoc_BMC:
        #         BMC_CHILD = frappe.get_all("Child Batch Milk Collection", filters={"parent": BMC.name}, fields=["supplier_id", "supplier_name","milk_type","fat","snf","litre","amount","bill_status"])

        # ------------------------------------------------------------------------
        # # frappe.msgprint(str(s.sales_invoice_deduction))
        # je = frappe.new_doc("Journal Entry")
        # je.voucher_type = "Journal Entry"
        # je.company = "Venkateshwara Power Projects LTD."
        # je.posting_date = self.today
        # je.append(
        #     "accounts",
        #     {
        #         "account": "22200001 - Cane Bill Payable - VPPL",
        #         "party_type": "Supplier",
        #         "party": s.farmer_id,
        #         "debit_in_account_currency": self.supplier_id,
        #         "milk_type": self.milk_type,
        #         "rate_group": self.rate_group,
        #         "supplier_name": self.supplier_name,
        #         "contact_number": self.contact_number,
        #         "fat": self.fat,
        #         "snf": self.snf,
        #         "litre": self.litre,
        #         "rate": self.rate,
        #         "amount": self.amount,
        #         "bill_status": self.bill_status,
        #     },
        # )
        # je.insert()
        # je.save()


# -------------------------------------------------------------------------------------------------------------------------------------
# @frappe.whitelist()
# def find_farmer(self):
#     cane_weight_docs = frappe.get_all('Cane Weight', filters={'farmer_code': p.farmer_id}, fields=["farmer_code", "date","name"])


# frappe.msgprint(str(cane_weight_docs))


# @frappe.whitelist()
# def vivek(self):
#     farmer_list_in_date =[]
#     doc = frappe.db.get_list("Cane Weight",fields=["farmer_name","farmer_village","date","farmer_code"],)
#     for d in doc:
#         if ((str(self.from_date)<= str(d.date)<= str(self.to_date))):
#             farmer_list_in_date.append(
#                         {
#                             "farmer_name": d.farmer_name,
#                             "farmer_code": d.farmer_code,
#                             "farmer_village": d.farmer_village,
#                             "date": d.date,
#                         },
#                     )
#     frappe.msgprint(str(farmer_list_in_date))
#     existing_farmer_codes = [ft.farmer_code for ft in self.farmer_table]  # Get existing farmer codes in the child table

#     for farmer in farmer_list_in_date:
#         if farmer["farmer_code"] not in existing_farmer_codes:
#             farmer_table = self.append("farmer_table", {})
#             farmer_table.farmer_name = farmer["farmer_name"]
#             farmer_table.farmer_id = farmer["farmer_code"]
#             farmer_table.village = farmer["farmer_village"]


# frappe.msgprint(str(farmer_list_in_date))

# for l in farmer_list_in_date:
#     self.append("farmer_table",{
#                         "farmer_name":l['farmer_name'],
#                         "farmer_code":l['farmer_code'],
#                         "farmer_village":l['farmer_village'],
#                         "date": l['date'],

#                         }
#                     )

# child_table = frappe.get_doc("Cane Billing", self.name).farmer_table
# for data in farmer_list_in_date:
#     child_table.append(data)
# self.save()


#     parent_doc = Document({
#         'doctype': 'Cane Billing'  # Replace 'Parent Doctype' with the actual doctype
#     })
#     parent_doc.child_table_fieldname = []

#     # Append child table entries
#     for data in farmer_list_in_date:
#         child_row = parent_doc.append('farmer_table', data)  # Replace 'child_table_fieldname' with the actual fieldname
#         child_row.flags.ignore_mandatory = True

# # Save the parent document to persist the changes
#         parent_doc.insert()
# --------------------------------------------------------------------------------------------------------------
