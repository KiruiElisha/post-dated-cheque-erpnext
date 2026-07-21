// Copyright (c) 2025, Azzir Group Limited and contributors
// For license information, please see license.txt
//elvisndegwa90@gmail.com

frappe.ui.form.on("Post Dated Cheque Entry", {
    /**
     * Triggered when the form is refreshed.
     * If the form is new, it sets the initial status to "Pending".
     */
    refresh(frm) {
        if (frm.is_new()) {
            frm.doc.status = 'Pending';
            frm.refresh_field('status');
        }
    },

    /**
     * Triggered when the currency field changes.
     * Calls the get_ex() function to update exchange rates.
     */
    currency(frm) {
        get_ex(frm);
    },

    /**
     * Triggered when the company_currency field changes.
     * Calls the get_ex() function to update exchange rates.
     */
    company_currency(frm) {
        get_ex(frm);
    },

    /**
     * Triggered when the posting_date field changes.
     * Calls the get_ex() function to update exchange rates.
     */
    posting_date(frm) {
        get_ex(frm);
    },
    before_save(frm){
    	get_ex(frm);
    },

    /**
     * Triggered when the amount field changes.
     * Updates the base_amount field based on the target exchange rate.
     */
    amount(frm) {
        frm.set_value("base_amount", frm.doc.amount * frm.doc.target_exchange_rate);
    },

    /**
     * Triggered when the target_exchange_rate field changes.
     * Updates the base_amount field accordingly.
     */
    target_exchange_rate(frm) {
        frm.set_value("base_amount", frm.doc.amount * frm.doc.target_exchange_rate);
    },

    /**
     * Triggered when the payment_type field changes.
     * Sets the party_type field based on payment type if no party is selected.
     */
    payment_type(frm) {
        if (!frm.doc.party) {
            if (frm.doc.payment_type === "Receive") {
                frm.set_value("party_type", "Customer");
            } else {
                frm.set_value("party_type", "Supplier");
            }
        }
    },

    /**
     * Setup function for form queries.
     * Uncomment the set_query calls if needed to filter party_type and party selection.
     */
    setup(frm) {
        // frm.set_query("party_type", function() {
        //     return {
        //         filters: [
        //             ["DocType", "name", "in", ["Customer", "Supplier"]],
        //         ]
        //     };
        // });

        // cur_frm.set_query("party", function() {
        //     return {
        //         filters: { "company": cur_frm.doc.company }
        //     };
        // });
    },

    /**
     * Triggered when the party field changes.
     * Fetches and sets the party name based on the selected party type (Customer or Supplier).
     */
    party(frm) {
        if (frm.doc.party_type === 'Customer' && frm.doc.party) {
            frappe.db.get_value('Customer', frm.doc.party, 'customer_name')
                .then(r => {
                    frm.doc.party_name = r.message.customer_name;
                    frm.refresh_field('party_name');
                });
        }
        if (frm.doc.party_type === 'Supplier' && frm.doc.party) {
            frappe.db.get_value('Supplier', frm.doc.party, 'supplier_name')
                .then(r => {
                    frm.doc.party_name = r.message.supplier_name;
                    frm.refresh_field('party_name');
                });
        }
    }
});

/**
 * Function to fetch exchange rates between selected currency and company currency.
 * Calls the erpnext.setup.utils.get_exchange_rate method via Frappe API.
 */
var get_ex = function(frm) {
    if (frm.doc.currency && frm.doc.company_currency) {
        frappe.call({
            method: "erpnext.setup.utils.get_exchange_rate",
            args: {
                'from_currency': frm.doc.currency,
                'to_currency': frm.doc.company_currency,
                'transaction_date': frm.doc.posting_date,
            },
            callback: function(r) {
                var res = r.message;
                console.log(res);
                if (res) {
                    frm.set_value("target_exchange_rate", res);
                }
            }
        });
    }
};
