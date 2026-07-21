// Copyright (c) 2025, Azzir Group Limited and contributors
// For license information, please see license.txt
// elvisndegwa90@gmail.com

/**
 * Sets a query filter for selecting bank accounts in the 'details' child table.
 * Filters accounts based on account type ('Bank') and company.
 */
cur_frm.set_query("bank_account", "details", function(frm, cdt, cdn) {
    var d = locals[cdt][cdn];
    return {
        filters: [
            ["Account", "account_type", "=", "Bank"],
            ["Account", "company", "=", d.company],
        ]
    };
});

frappe.ui.form.on('Post Dated Cheque Tool', {
    /**
     * Triggered when the form is refreshed.
     * Sets a query filter for selecting the default bank account based on account type ('Bank').
     */
    refresh(frm) {
    	console.log("hae")
        frm.set_query("default_bank_account", function() {
            return {
                filters: [
                    ["Account", "account_type", "=", "Bank"],
                ]
            };
        });
    },

    /**
     * Applies the selected default bank account to all rows in the 'details' table.
     * Logs the selected rows for debugging.
     */
    apply_bank:function(frm) {
        // Log the entire details array for debugging purposes
        console.log("Selected rows:", frm.doc.details);

        // Loop through each row in the 'details' table and set the bank_account field
        frm.doc.details.forEach(function(d) {
            d.bank_account = frm.doc.default_bank_account;
        });

        // Refresh the 'details' field to reflect changes in the UI
        frm.refresh_field("details");
    },

    /**
     * Fetches post-dated cheques based on selected filters (company, cost center, department, date range).
     * Clears existing 'details' table and repopulates it with new records from the backend response.
     */
    get_posted_dated_cheques:function(frm) {
        // Clear the existing 'details' table
        console.log("hae")
        frm.doc.details = [];
        frm.refresh_field("details");

        // Call the backend method to fetch post-dated cheques
        frappe.call({
            method: "post_dated_cheque.post_dated_cheque.doctype.post_dated_cheque_tool.post_dated_cheque_tool.get_post_dated_cheques",
            args: {
                company: frm.doc.company,
                cost_center: frm.doc.cost_center,
                department: frm.doc.department,
                from_date: frm.doc.from_date,
                to_date: frm.doc.to_date,
            },
            callback: function(r) {
                var res = r.message;
                if (res) {
                    console.log(res);
                    
                    // Loop through the response data and add each cheque to the 'details' table
                    for (var d in res) {
                        frm.add_child("details", res[d]);
                    }

                    // Refresh the 'details' field to update the UI
                    frm.refresh_field("details");
                }
            }
        });
    },
});
