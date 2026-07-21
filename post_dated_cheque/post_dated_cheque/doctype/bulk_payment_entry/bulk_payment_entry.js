// Copyright (c) 2026, Azzir Group Limited and contributors
// For license information, please see license.txt

frappe.ui.form.on("Bulk Payment Entry", {
	refresh(frm) {
		frm.trigger("calculate_total");

		if (frm.doc.journal_entry) {
			frm.add_custom_button(__("Journal Entry"), () => {
				frappe.set_route("Form", "Journal Entry", frm.doc.journal_entry);
			}, __("View"));
		}
	},

	get_invoices(frm) {
		if (!frm.doc.company) {
			frappe.throw(__("Please select a Company first."));
			return;
		}

		const d = new frappe.ui.Dialog({
			title: __("Get Outstanding Invoices"),
			fields: [
				{
					fieldtype: "Link",
					fieldname: "customer",
					label: __("Customer (optional)"),
					options: "Customer",
					description: __("Leave blank to fetch invoices for all customers."),
				},
				{ fieldtype: "Column Break" },
				{ fieldtype: "Date", fieldname: "from_date", label: __("From Date") },
				{ fieldtype: "Date", fieldname: "to_date", label: __("To Date") },
			],
			primary_action_label: __("Get Invoices"),
			primary_action(values) {
				frappe.call({
					method: "post_dated_cheque.post_dated_cheque.doctype.bulk_payment_entry.bulk_payment_entry.get_outstanding_invoices",
					args: {
						company: frm.doc.company,
						customer: values.customer,
						from_date: values.from_date,
						to_date: values.to_date,
					},
					freeze: true,
					freeze_message: __("Fetching outstanding invoices..."),
					callback(r) {
						const rows = r.message || [];
						if (!rows.length) {
							frappe.msgprint(__("No outstanding Sales Invoices found."));
							return;
						}

						const existing = new Set(
							(frm.doc.invoices || []).map((row) => row.sales_invoice)
						);

						let added = 0;
						rows.forEach((inv) => {
							if (existing.has(inv.sales_invoice)) return;
							const child = frm.add_child("invoices");
							child.sales_invoice = inv.sales_invoice;
							child.customer = inv.customer;
							child.customer_name = inv.customer_name;
							child.posting_date = inv.posting_date;
							child.grand_total = inv.grand_total;
							child.outstanding_amount = inv.outstanding_amount;
							child.allocated_amount = inv.outstanding_amount;
							child.receivable_account = inv.receivable_account;
							added += 1;
						});

						frm.refresh_field("invoices");
						frm.trigger("calculate_total");
						d.hide();
						frappe.show_alert({
							message: __("{0} invoice(s) added.", [added]),
							indicator: "green",
						});
					},
				});
			},
		});
		d.show();
	},

	calculate_total(frm) {
		let total = 0;
		(frm.doc.invoices || []).forEach((row) => {
			total += flt(row.allocated_amount);
		});
		frm.set_value("total_allocated_amount", total);
	},
});

frappe.ui.form.on("Bulk Payment Entry Invoice", {
	allocated_amount(frm) {
		frm.trigger("calculate_total");
	},
	invoices_remove(frm) {
		frm.trigger("calculate_total");
	},
});
