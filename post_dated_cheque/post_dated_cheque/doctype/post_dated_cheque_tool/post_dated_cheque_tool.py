# Copyright (c) 2025, Aqiq Solutions Limited and contributors
# For license information, please see license.txt
# elvisndegwa90@gmail.com

import frappe
from frappe.model.document import Document


class PostDatedChequeTool(Document):
    """
    This class handles the submission of Post Dated Cheques (PDCs) and 
    ensures that payment entries are created for each cheque.
    """

    def on_submit(self):
        """
        This method runs upon submission of the document.
        It validates the bank account field, checks for existing payment entries, 
        and creates a new Payment Entry for each PDC if it does not already exist.
        """
        payment_entries = ""

        for d in self.details:
            # Ensure that a bank account is specified for each row
            if not d.bank_account:
                frappe.throw(f"Bank Account required on row {d.idx}")

            # Check if a payment entry already exists for the given PDC (excluding cancelled ones)
            existing_payment = frappe.db.get_value(
                "Payment Entry",
                {"custom_post_dated_cheques": d.post_dated_cheques, "docstatus": ("!=", 2)},
                "name"
            )

            if not existing_payment:
                print(d.name)
                
                # Fetch the corresponding Post Dated Cheques document
                pdc = frappe.get_doc("Post Dated Cheque", d.post_dated_cheques)

                # Create a new Payment Entry document
                doc = frappe.new_doc("Payment Entry")
                doc.company = d.company
                doc.cost_center = d.cost_center
                doc.department = d.department
                doc.project = d.project
                doc.mode_of_payment = d.mode_of_payment
                doc.payment_type = d.payment_type
                doc.reference_no = d.reference_no
                doc.reference_date = d.reference_date
                doc.party_type = d.party_type
                doc.party = d.party
                doc.custom_post_dated_cheque_reference = self.name
                doc.paid_amount = d.amount
                doc.received_amount = pdc.base_amount
                doc.source_exchange_rate = 1
                doc.target_exchange_rate = pdc.target_exchange_rate
                doc.custom_post_dated_cheques = d.post_dated_cheques

                # Set currency details
                doc.paid_from_account_currency = pdc.company_currency
                doc.paid_to_account_currency = pdc.currency

                # Set remarks and additional notes
                doc.remarks = pdc.additional_notes
                doc.additional_notes = pdc.additional_notes

                # Fetch the party account
                account = frappe.db.get_value(
                    "Party Account",
                    {"company": d.company, "parent": d.party},
                    "account"
                )

                # Determine payment accounts based on party type
                if d.party_type == "Customer":
                    account = account or frappe.db.get_value("Company", d.company, "default_receivable_account")
                    doc.paid_to = d.bank_account
                    doc.paid_from = account
                else:
                    account = account or frappe.db.get_value("Company", d.company, "default_payable_account")
                    doc.paid_from = d.bank_account
                    doc.paid_to = account

                # Save the payment entry document
                doc.save(ignore_permissions=True)
                payment_entries += f"{doc.name}, "

        # Display a message listing the created payment entries
        if payment_entries:
            frappe.msgprint(f"Payment Entries created: {payment_entries}")


@frappe.whitelist()
def get_post_dated_cheques(company=None, cost_center=None, department=None, from_date=None, to_date=None):
    """
    Fetches post-dated cheques that meet the specified filters.

    Args:
        company (str, optional): Company filter.
        cost_center (str, optional): Cost center filter.
        department (str, optional): Department filter.
        from_date (str, optional): Start date filter.
        to_date (str, optional): End date filter.

    Returns:
        list: A list of dictionaries containing PDC details.
    """
    conditions = []

    # Append conditions based on provided filters
    if company:
        conditions.append(f"company = '{company}'")
    if cost_center:
        conditions.append(f"cost_center = '{cost_center}'")
    if department:
        conditions.append(f"department = '{department}'")
    if from_date:
        conditions.append(f"posting_date >= '{from_date}'")
    if to_date:
        conditions.append(f"posting_date <= '{to_date}'")

    # Construct the SQL condition string
    condition_string = f" AND {' AND '.join(conditions)}" if conditions else ""

    # Execute the SQL query to fetch post-dated cheques
    data = frappe.db.sql(f"""
        SELECT company, cost_center, department, project, mode_of_payment, posting_date,
               payment_type, reference_no, reference_date, party_type, party, amount, 
               name AS post_dated_cheques, company_currency, currency
        FROM `tabPost Dated Cheque`
        WHERE docstatus = 1 AND status = 'Pending' {condition_string}
    """, as_dict=True)

    return data
