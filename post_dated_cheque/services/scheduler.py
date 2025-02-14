
import frappe

""" This api call is for sending Statement Detail Report on click of Send Specifically button in report page """
@frappe.whitelist(allow_guest  = True)
def send_email_statement_detail_on_specific_email(filters, customer_email):
    filters = frappe._dict(json.loads(filters))

    try:
        email_id = customer_email
        result = get_party_data(filters.company, filters.party_type, filters.party, filters.from_date, filters.to_date, email_id,  today())
        return 'Success in sending email ' + str(result)
    except Exception as e:
        error_message = frappe.get_traceback()+"Error\n"+str(e)
        frappe.log_error(error_message, "Main function named Check Scheduler Date failed.")
        return error_message