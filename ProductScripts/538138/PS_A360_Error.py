err_msg =  ""
laborCont = Product.GetContainerByName("SC_Labor_Summary_Container")
if laborCont.Rows.Count:
	for row in laborCont.Rows:
		row.Product.Attr('SC_Labor_Block_Discount').AssignValue(Product.Attr('SC_OverAll_Labor_Block_Discount').GetValue())
		if row.Product.Attr('SC_Labor_Resource_Type').GetValue() == "A360 Contract Management":
			if row.Product.Attr('SC_Labor_Service_Product').GetValue() == "A360 Contract Management" and row.Product.Attr('SC_Labor_Entitlement').GetValue() == "A360 Contract Management" and row.Product.Attr('SC_AT_Related_Module_Autocomplete').GetValue() == "A360":
				pass
			else:
				err_msg = "When Resource Type is 'A360 Contract Management' then Service Product & Entitlement should be 'A360 Contract Management' and Related Module should be 'A360'"
		if row.Product.Attr('SC_Labor_Resource_Type').GetValue() == "Service Contract Management":
			if row.Product.Attr('SC_Labor_Service_Product').GetValue() == "Service Contract Management" and row.Product.Attr('SC_Labor_Entitlement').GetValue() == "Service Contract Management" and row.Product.Attr('SC_AT_Related_Module_Autocomplete').GetValue() == "A360":
				pass
			else:
				err_msg = "When Resource Type is 'Service Contract Management' then Service Product & Entitlement should be 'Service Contract Management' and Related Module should be 'A360'"
		if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
			if row["PY_Resource_Type"] == "A360 Contract Management":
				if row.Product.Attr('SC_PY_Labor_Service_Product').GetValue() == "A360 Contract Management" and row.Product.Attr('SC_PY_Labor_Entitlement').GetValue() == "A360 Contract Management" and row.Product.Attr('SC_AT_Related_Module_Autocomplete').GetValue() == "A360":
					pass
				else:
					err_msg = "When Resource Type is 'A360 Contract Management' then Service Product & Entitlement should be 'A360 Contract Management' and Related Module should be 'A360'"
			if row["PY_Resource_Type"] == "Service Contract Management":
				if row.Product.Attr('SC_PY_Labor_Service_Product').GetValue() == "Service Contract Management" and row.Product.Attr('SC_PY_Labor_Entitlement').GetValue() == "Service Contract Management" and row.Product.Attr('SC_AT_Related_Module_Autocomplete').GetValue() == "A360":
					pass
				else:
					err_msg = "When Resource Type is 'Service Contract Management' then Service Product & Entitlement should be 'Service Contract Management' and Related Module should be 'A360'"
Product.Attr("SC_Labor_ErrorMsg_2").AssignValue(err_msg)