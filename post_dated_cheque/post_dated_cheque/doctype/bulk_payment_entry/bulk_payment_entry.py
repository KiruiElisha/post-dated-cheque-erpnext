# Copyright (c) 2026, Azzir Group Limited and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt


class BulkPaymentEntry(Document):
	def validate(self):
		self.set_missing_values()
		self.validate_invoices()
		self.calculate_total()

	def set_missing_values(self):
		for row in self.invoices:
			if row.sales_invoice and not row.receivable_account:
				row.receivable_account = frappe.db.get_value(
					"Sales Invoice", row.sales_invoice, "debit_to"
				)
			if row.sales_invoice and not row.customer:
				row.customer = frappe.db.get_value(
					"Sales Invoice", row.sales_invoice, "customer"
				)

	def validate_invoices(self):
		if not self.invoices:
			frappe.throw(_("Please add at least one Sales Invoice."))

		seen = set()
		for row in self.invoices:
			if row.sales_invoice in seen:
				frappe.throw(
					_("Sales Invoice {0} is added more than once.").format(
						frappe.bold(row.sales_invoice)
					)
				)
			seen.add(row.sales_invoice)

			si = frappe.db.get_value(
				"Sales Invoice",
				row.sales_invoice,
				["docstatus", "company", "outstanding_amount", "debit_to", "customer"],
				as_dict=True,
			)
			if not si or si.docstatus != 1:
				frappe.throw(
					_("Sales Invoice {0} must be submitted.").format(
						frappe.bold(row.sales_invoice)
					)
				)

			if si.company != self.company:
				frappe.throw(
					_("Sales Invoice {0} belongs to company {1}, not {2}.").format(
						frappe.bold(row.sales_invoice), si.company, self.company
					)
				)

			if flt(row.allocated_amount) <= 0:
				frappe.throw(
					_("Allocated Amount for Sales Invoice {0} must be greater than zero.").format(
						frappe.bold(row.sales_invoice)
					)
				)

			if flt(row.allocated_amount) > flt(si.outstanding_amount):
				frappe.throw(
					_(
						"Allocated Amount {0} for Sales Invoice {1} cannot exceed its outstanding amount {2}."
					).format(
						flt(row.allocated_amount),
						frappe.bold(row.sales_invoice),
						flt(si.outstanding_amount),
					)
				)

			if not row.receivable_account:
				row.receivable_account = si.debit_to
			if not row.customer:
				row.customer = si.customer

	def calculate_total(self):
		self.total_allocated_amount = sum(flt(row.allocated_amount) for row in self.invoices)

	def on_submit(self):
		self.make_journal_entry()

	def on_cancel(self):
		self.cancel_journal_entry()

	def make_journal_entry(self):
		if self.journal_entry:
			return

		je = frappe.new_doc("Journal Entry")
		je.voucher_type = "Bank Entry"
		je.company = self.company
		je.posting_date = self.posting_date
		je.cheque_no = self.reference_no
		je.cheque_date = self.reference_date
		je.mode_of_payment = self.mode_of_payment
		je.user_remark = self.user_remark or _("Bulk Payment Entry {0}").format(self.name)
		je.custom_bulk_payment_entry = self.name

		# One credit line per selected Sales Invoice, keeping each customer + invoice reference
		for row in self.invoices:
			je.append(
				"accounts",
				{
					"account": row.receivable_account,
					"party_type": "Customer",
					"party": row.customer,
					"credit_in_account_currency": flt(row.allocated_amount),
					"reference_type": "Sales Invoice",
					"reference_name": row.sales_invoice,
				},
			)

		# Single debit line to the bank/cash account for the full amount
		je.append(
			"accounts",
			{
				"account": self.paid_to_account,
				"debit_in_account_currency": flt(self.total_allocated_amount),
			},
		)

		je.flags.ignore_permissions = True
		je.insert()

		# Journal Entry defaults its title to the customer name; override it to
		# describe the bulk payment and the invoice(s) it settles.
		je.db_set("title", self.get_journal_entry_title(), update_modified=False)

		je.submit()

		self.db_set("journal_entry", je.name)
		frappe.msgprint(
			_("Journal Entry {0} created.").format(
				frappe.utils.get_link_to_form("Journal Entry", je.name)
			),
			alert=True,
		)

	def get_journal_entry_title(self):
		invoices = [row.sales_invoice for row in self.invoices if row.sales_invoice]
		if len(invoices) == 1:
			title = _("Bulk Payment of {0}").format(invoices[0])
		elif len(invoices) <= 3:
			title = _("Bulk Payment of {0}").format(", ".join(invoices))
		else:
			title = _("Bulk Payment of {0} Invoices").format(len(invoices))
		return title[:140]

	def cancel_journal_entry(self):
		if not self.journal_entry:
			return

		if frappe.db.exists("Journal Entry", self.journal_entry):
			je = frappe.get_doc("Journal Entry", self.journal_entry)
			if je.docstatus == 1:
				je.flags.ignore_permissions = True
				je.cancel()

		self.db_set("journal_entry", None)


@frappe.whitelist()
def get_outstanding_invoices(company, customer=None, from_date=None, to_date=None):
	"""Return submitted Sales Invoices with a positive outstanding amount."""
	filters = {
		"docstatus": 1,
		"company": company,
		"outstanding_amount": [">", 0],
	}
	if customer:
		filters["customer"] = customer
	if from_date and to_date:
		filters["posting_date"] = ["between", [from_date, to_date]]
	elif from_date:
		filters["posting_date"] = [">=", from_date]
	elif to_date:
		filters["posting_date"] = ["<=", to_date]

	return frappe.get_all(
		"Sales Invoice",
		filters=filters,
		fields=[
			"name as sales_invoice",
			"customer",
			"customer_name",
			"posting_date",
			"grand_total",
			"outstanding_amount",
			"debit_to as receivable_account",
		],
		order_by="customer asc, posting_date asc",
	)
