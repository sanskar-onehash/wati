import frappe
from wati.app_config import APP_TITLE


def after_install():
    try:
        add_app_to_whatsapp_apps()
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
