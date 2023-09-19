import frappe
# from erpnext.stock.doctype.material_request.material_request import make_purchase_order
from frappe.utils import add_days, cint, flt, nowdate, getdate

def create_purchase_order(doc,method):
    if doc.material_request_type == "Purchase":
        supplier_wise_items = {}
        for item in doc.items:
            po_supplier = frappe.db.get_value("Item Reorder",{"parent":item.item_code,"warehouse":item.warehouse},"supplier")
            if po_supplier:
                if po_supplier in supplier_wise_items:
                    item_details = {
                        "item_code":item.item_code,
                        "item_name":item.item_name,
                        "schedule_date":str(nowdate()),
                        "warehouse":item.warehouse,
                        "qty":item.qty,
                        "material_request":doc.name
                    }
                    item_list = supplier_wise_items.get(po_supplier).get("items")
                    item_list.append(item_details)
                else:
                    temp = {
                        "supplier":po_supplier,
                        "items":[{
                            "item_code":item.item_code,
                            "item_name":item.item_name,
                            "schedule_date":str(nowdate()),
                            "warehouse":item.warehouse,
                            "qty":item.qty,
                            "material_request":doc.name
                        }],
                        "date" : doc.transaction_date,
                        "schedule_date":nowdate()
                    }
                    supplier_wise_items.update({po_supplier:temp})
        # print(supplier_wise_items)
        for supplier in supplier_wise_items:
            res = new_purchase_order(supplier_wise_items[supplier],doc)

def new_purchase_order(supplier,doc):
    try:
        po_doc = frappe.new_doc("Purchase Order")
        po_doc.supplier = supplier.get("supplier")
        po_doc.date = doc.transaction_date
        po_doc.schedule_date = doc.schedule_date
        for item in supplier.get("items"):
            po_doc.append(
                "items",item
            )
        po_doc.run_method("calculate_taxes_and_totals")
        po_doc.save()
        frappe.db.commit()
        
        print(po_doc.name)
    except Exception as e:
        print(f'exception raised in create purchase order function for supplier {supplier.get("supplier")} ')
        frappe.log_error(title="Create Purchase order", message=e)
        frappe.db.commit()
        raise