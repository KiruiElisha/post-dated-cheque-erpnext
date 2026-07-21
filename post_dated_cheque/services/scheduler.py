# elvisndegwa90@gmail.com
import json

import frappe
from frappe import _
from frappe.utils import format_datetime

from post_dated_cheque.post_dated_cheque.report.statement_details_with_chq_no.statement_details_with_chq_no import (
    execute as get_statement_details,
)


@frappe.whitelist()
def send_email_statement_detail_on_specific_email(filters, customer_email):
    """
    Render the "Statement Details with Chq No" report for the given filters
    and email it to the supplied address.

    Triggered by the "Send via Email" button in the report view.
    """
    if not customer_email:
        frappe.throw(_("An email address is required to send the statement."))

    if isinstance(filters, str):
        filters = json.loads(filters)
    filters = frappe._dict(filters)

    columns, data = get_statement_details(filters)[:2]

    if not data:
        frappe.throw(_("There is no data to send for the selected filters."))

    message = build_statement_html(columns, data, filters)
    subject = _("Account Statement")
    if filters.get("party"):
        subject = f"{subject} - {filters.party}"

    frappe.sendmail(
        recipients=[customer_email],
        subject=subject,
        message=message,
        reference_doctype="Report",
        reference_name="Statement Details with Chq No",
    )

    return _("Email sent successfully to {0}").format(customer_email)


def build_statement_html(columns, data, filters):
    """Render report columns/rows into a simple HTML table for the email body."""
    columns = [frappe._dict(col) if isinstance(col, dict) else col for col in columns]

    header_cells = "".join(
        "<th style='text-align:left;padding:6px;border-bottom:2px solid #d1d8dd'>"
        f"{frappe.utils.escape_html(col.label or col.fieldname)}</th>"
        for col in columns
    )

    rows_html = []
    for row in data:
        cells = []
        for col in columns:
            value = row.get(col.fieldname) if isinstance(row, dict) else None
            try:
                formatted = frappe.format(value, col, row) if value is not None else ""
            except Exception:
                formatted = frappe.utils.escape_html(str(value)) if value is not None else ""
            cells.append(
                f"<td style='padding:6px;border-bottom:1px solid #ebeff2'>{formatted}</td>"
            )
        rows_html.append(f"<tr>{''.join(cells)}</tr>")

    generated_on = format_datetime(frappe.utils.now_datetime())

    return f"""
        <p>{_('Please find your account statement below.')}</p>
        <table style='border-collapse:collapse;width:100%;font-size:12px'>
            <thead><tr>{header_cells}</tr></thead>
            <tbody>{''.join(rows_html)}</tbody>
        </table>
        <p style='color:#8d99a6;font-size:11px;margin-top:12px'>{_('Generated on')} {generated_on}</p>
    """
