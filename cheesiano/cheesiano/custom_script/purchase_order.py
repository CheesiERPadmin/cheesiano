import frappe

def save_item_price(doc,method):
    for item in doc.items:
        if item.rate != item.last_purchase_rate:
            item_price = frappe.get_doc(
			{
				"doctype": "Item Price",
				"item_code": item.item_code,
                "price_list": "Standard Buying",
		    }
		    )
            item_price.price_list_rate = item.rate
            item_price.insert()
            frappe.db.commit()