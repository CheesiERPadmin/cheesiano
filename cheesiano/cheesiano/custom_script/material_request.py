import frappe
from erpnext.stock.doctype.material_request.material_request import make_purchase_order

def create_purchase_order(doc,method):
    if doc.material_request_type == "Purchase":
        po_doc = make_purchase_order(doc.name)
        for item in doc.items:
            try:
                po_doc.supplier = frappe.db.get_value("Item Supplier",{"parent":item.item_code},'supplier')
                
                if not po_doc.supplier:
                    frappe.msgprint("Supplier is not assigned")
                    po_doc.save()
            except:
                raise
            

def delete_purchase_order(doc,method):
    frappe.msgprint(f"Purchase Order for this Material Request {doc.name} has been deleted")
    return True