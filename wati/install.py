import frappe
from wati.app_config import APP_TITLE


def after_install():
    try:
        add_app_to_whatsapp_apps()
        add_custom_fields_to_notification()
    except Exception as e:
        frappe.log_error(f"Error occured after installing {APP_TITLE} app:", e)


def add_app_to_whatsapp_apps():
    try:
        field = frappe.db.get_list(
            "Custom Field",
            ["*"],
            {"dt": "Notification", "fieldname": "custom_whatsapp_app"},
        )[0]

        if not field.options:
            field.options = ""
        options = field.options.split("\n")

        if APP_TITLE not in options:
            options.append(APP_TITLE)
            frappe.db.set_value(
                "Custom Field", field.name, "options", "\n".join(options)
            )
            frappe.db.commit()
    except IndexError:
        raise Exception("Clientside is not installed.")


def add_custom_fields_to_notification():
    custom_fields = [
        {
            "depends_on": 'eval: (doc.channel == "WhatsApp") && (doc.custom_whatsapp_app == "Wati")',
            "dt": "Notification",
            "fieldname": "wati_map_fields",
            "fieldtype": "Button",
            "insert_after": "message_sb",
            "label": "Map Fields",
            "module": "Wati",
            "name": "Notification-map_fields",
        },
        {
            "depends_on": 'eval: (doc.channel == "WhatsApp") && (doc.custom_whatsapp_app == "Wati")',
            "description": "To use WhatsApp Wati.io service, select a pre-approved template.",
            "dt": "Notification",
            "fieldname": "wati_whatsapp_template",
            "fieldtype": "Link",
            "insert_after": "slack_webhook_url",
            "label": "WhatsApp Template",
            "mandatory_depends_on": 'eval: (doc.channel == "WhatsApp") && (doc.custom_whatsapp_app == "Wati")',
            "module": "Wati",
            "name": "Notification-whatsapp_template",
            "options": "WhatsApp Template",
        },
        {
            "depends_on": 'eval: (doc.channel == "WhatsApp") && (doc.custom_whatsapp_app == "Wati")',
            "dt": "Notification",
            "fieldname": "wati_whatsapp_parameter",
            "fieldtype": "Table",
            "insert_after": "wati_map_fields",
            "label": "WhatsApp Parameter",
            "module": "Wati",
            "name": "Notification-whatsapp_parameter",
            "options": "WhatsApp Parameter Map",
        },
    ]

    for field in custom_fields:
        if not frappe.db.exists(
            "Custom Field", {"dt": "Notification", "fieldname": field["fieldname"]}
        ):
            new_field = frappe.get_doc({"doctype": "Custom Field", **field})
            new_field.insert()
            frappe.db.commit()
