import frappe


def execute():
    """
    Rename the DocType "Post Dated Cheque" to "Post Dated Cheque Entry".

    The old name collided with the "Post Dated Cheque" Workspace (and module),
    causing desk routing conflicts. Renaming the DocType resolves the clash.

    frappe.rename_doc for a DocType also renames its table and updates every
    link/dynamic-link/custom-field option that referenced the old name, so no
    manual reference patching is required here.
    """
    old, new = "Post Dated Cheque", "Post Dated Cheque Entry"

    if frappe.db.exists("DocType", old) and not frappe.db.exists("DocType", new):
        frappe.rename_doc("DocType", old, new, force=True)
        frappe.clear_cache()
