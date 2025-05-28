// Copyright (c) 2023, Abhishek Chougule and contributors
// For license information, please see license.txt

frappe.ui.form.on('WhatsApp Web Message Template', {
	before_save: function(frm) {
		const formattedText = "%0a" + frm.doc.whatsapp_messages_template.split('\n').join('%0a') + "%0a";
		frm.doc.whatsapp_messages_template=formattedText;
	}
});
