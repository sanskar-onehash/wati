import frappe
import json
from frappe.email.doctype.notification.notification import get_context
from wati.app_config import APP_TITLE
from wati.wati.doctype.wati_settings.wati_settings import send_template_message


def wati_validate(notification_doc):
    if (
        notification_doc.enabled
        and notification_doc.channel == "WhatsApp"
        and notification_doc.custom_whatsapp_app == APP_TITLE
    ):
        wati_validate_wati_settings()


def wati_validate_wati_settings():
    if not frappe.db.get_single_value("Wati Settings", "enabled"):
        frappe.throw(frappe._("Please enable Wati settings to send WhatsApp messages"))


def wati_send(notification_doc, doc):
    context = get_context(doc)
    context = {"doc": doc, "alert": notification_doc, "comments": None}
    if doc.get("_comments"):
        context["comments"] = json.loads(doc.get("_comments"))

    if notification_doc.is_standard:
        notification_doc.load_standard_properties(context)

    try:
        if (
            notification_doc.channel == "WhatsApp"
            and notification_doc.custom_whatsapp_app == APP_TITLE
        ):
            wati_send_whatsapp_msg(notification_doc, doc, context)
    except:
        frappe.log_error(
            title="Failed to send notification", message=frappe.get_traceback()
        )


def wati_send_whatsapp_msg(notification_doc, doc, context):
    whatsapp_template = notification_doc.wati_whatsapp_template

    if not whatsapp_template:
        return

    whatsapp_template = frappe.get_doc("WhatsApp Template", whatsapp_template)
    template_parameters = frappe.render_template(notification_doc.message, context)

    params = json.loads(template_parameters)
    for k, v in params.items():
        if (
            v
            and v.strip() in ["print_format", "Print Format"]
            and notification_doc.attach_print
            and notification_doc.print_format != ""
        ):
            url = (
                frappe.utils.get_url()
                + "/"
                + doc.doctype
                + "/"
                + doc.name
                + "?format="
                + notification_doc.print_format
                + "&key="
                + doc.get_signature()
            )
            params[k] = url

    send_template_message(
        doc=doc,
        whatsapp_numbers=notification_doc.get_receiver_list(doc, context),
        broadcast_name=whatsapp_template.broadcast_name,
        template_name=whatsapp_template.template_name,
        template_parameters=params,
    )
