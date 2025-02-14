# elvisndegwa90@gmail.com
import frappe


def payment_entry_validate(self, method):
    """
    Triggered when a Payment Entry is being validated.
    Updates the status of the linked Post Dated Cheques.
    """
    update_pt_cheque_status(self)


def payment_entry_on_submit(self, method):
    """
    Triggered when a Payment Entry is submitted.
    Ensures the Post Dated Cheques status is updated accordingly.
    """
    update_pt_cheque_status(self)


def payment_entry_on_cancel(self, method):
    """
    Triggered when a Payment Entry is canceled.
    Resets the status of the linked Post Dated Cheques.
    """
    update_pt_cheque_status(self)


def update_pt_cheque_status(self):
    """
    Updates the status of the Post Dated Cheques based on the Payment Entry's docstatus.
    
    Status Mapping:
    - docstatus 0 -> "Payment Entry Created"
    - docstatus 1 -> "Payment Entry Submitted"
    - docstatus 2 -> "Pending" (Canceled or Unsubmitted)
    
    This function modifies the "status" field in the Post Dated Cheques DocType.
    """
    if self.custom_post_dated_cheques:
        status = "Pending"

        if self.docstatus == 0:
            status = "Payment Entry Created"
        elif self.docstatus == 1:
            status = "Payment Entry Submitted"
        elif self.docstatus == 2:
            status = "Pending"

        # Update the status in the Post Dated Cheques DocType
        frappe.db.set_value(
            "Post Dated Cheque", self.custom_post_dated_cheques, "status", status
        )
