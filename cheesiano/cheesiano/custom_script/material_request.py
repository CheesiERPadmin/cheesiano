import frappe
from erpnext.stock.doctype.material_request.material_request import make_purchase_order

def create_purchase_order(doc,method):
    # print(doc.item)
    if doc.material_request_type == "Purchase":
        po_doc = make_purchase_order(doc.name)
        for item in doc.items:
            print("====Item details\n")
            # print(item.name)
            print(item.item_code) 
            # item_info = frappe.get_doc("Item",item.item_code)
            # print(f"item doctype fetched {item_info}")        
            print("Create Purchase order function called after submission of materialrequest ")
            po_doc.supplier = frappe.db.get_value("Item Supplier",{"parent":item.item_code},'supplier') 
            po_doc.save()

def delete_purchase_order(doc,method):
    print("======= Material request is cancelled =======")
    frappe.msgprint(f"Purchase Order for this Material Request {doc.name} has been deleted")
    return True