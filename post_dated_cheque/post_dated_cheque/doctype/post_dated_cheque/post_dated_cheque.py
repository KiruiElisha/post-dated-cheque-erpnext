# Copyright (c) 2025, Aqiq Solutions Limited and contributors
# For license information, please see license.txt
#elvisndegwa90@gmail.com

import frappe
from frappe.model.document import Document


class PostDatedCheque(Document):
	
	def on_cancel(self):
		frappe.db.set_value(self.doctype, self.name, 'status', 'Cancelled')
		self.reload()
