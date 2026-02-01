if Product.Attr('SC_Product_Type').GetValue() is not None and Product.Attr('SC_Product_Type').GetValue() == 'Renewal':
	Product.Attr("SC_ServiceProduct_HR_RWL").Access = AttributeAccess.ReadOnly
	#Product incomplete on renewal quantity / Honeywell list price is zero
	isNone = False
	con = Product.GetContainerByName("SC_ValidModels_HR_RWL")
	if con.Rows.Count:
		for i in con.Rows:
			if i['SC_RenewalQuantity_HR_RWL'] == '' or float(i['SC_RenewalQuantity_HR_RWL']) == 0 or i['SC_HoneywellListPrice_HR_RWL'] == '' or float(i['SC_HoneywellListPrice_HR_RWL']) == 0 or i['SC_Asset_HR_RWL'] == '' or i['SC_Asset_HR_RWL'] is None or i['SC_Model_HR_RWL'] is None or i['SC_Description_HR_RWL'] is None or i['SC_Model_HR_RWL'] == '' or i['SC_Description_HR_RWL'] == '':
				isNone = True
				Product.Attr('IncompleteMessageFlag_HWR').AssignValue('False')
				Product.Attr('ModelAndDescription_CompleteCheck_HRW').AssignValue('False')
				Product.Attr('qtyAndUnitprice_CompleteCheck_HRW').AssignValue('False')
				if (i['SC_RenewalQuantity_HR_RWL'] == '' or float(i['SC_RenewalQuantity_HR_RWL']) == 0) and (i['SC_HoneywellListPrice_HR_RWL'] == '' or float(i['SC_HoneywellListPrice_HR_RWL']) == 0) and (i['SC_Asset_HR_RWL'] == '' or i['SC_Asset_HR_RWL'] is None) and (i['SC_Model_HR_RWL'] is None or i['SC_Model_HR_RWL'] == '') and (i['SC_Description_HR_RWL'] is None or i['SC_Description_HR_RWL'] == ''):
					Product.Attr('IncompleteMessageFlag_HWR').AssignValue('True')
				elif i['SC_Model_HR_RWL'] is None or i['SC_Description_HR_RWL'] is None or i['SC_Model_HR_RWL'] == '' or i['SC_Description_HR_RWL'] == '':
					Product.Attr('ModelAndDescription_CompleteCheck_HRW').AssignValue('True')
					Product.Attr('qtyAndUnitprice_CompleteCheck_HRW').AssignValue('False')
				elif i['SC_RenewalQuantity_HR_RWL'] == '' or float(i['SC_RenewalQuantity_HR_RWL']) == 0 or i['SC_HoneywellListPrice_HR_RWL'] == '' or float(i['SC_HoneywellListPrice_HR_RWL']) == 0:
					Product.Attr('qtyAndUnitprice_CompleteCheck_HRW').AssignValue('True')
		else :
			if isNone:
				Product.Attr('IsproductComplete_HRW').Required = True
				Product.Attr('IncompleteMessageFlag_HWR').AssignValue('True')
			else:
				Product.Attr('IsproductComplete_HRW').Required = False
				Product.Attr('IncompleteMessageFlag_HWR').AssignValue('False')
	else :
		Product.Attr('IsproductComplete_HRW').Required = True
		Product.Attr('IncompleteMessageFlag_HWR').AssignValue('True')
else:
	Product.Attr('IsproductComplete_HRW').Required = False
	Product.Attr('IncompleteMessageFlag_HWR').AssignValue('False')