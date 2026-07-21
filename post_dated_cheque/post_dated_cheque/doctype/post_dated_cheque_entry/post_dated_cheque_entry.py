# Copyright (c) 2025, Azzir Group Limited and contributors
# For license information, please see license.txt
#elvisndegwa90@gmail.com

import frappe
from frappe.model.document import Document


class PostDatedChequeEntry(Document):
	
	def on_cancel(self):
		# db_set updates both the database and the in-memory document,
		# avoiding a separate reload.
		self.db_set("status", "Cancelled")
