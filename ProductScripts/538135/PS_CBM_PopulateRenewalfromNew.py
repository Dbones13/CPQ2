if Product.Name != "Service Contract Products":
	if Product.Attributes.GetByName("SC_Product_Type").GetValue() == "Renewal":
		cont = Product.GetContainerByName('CBM_Pricing_Container')
		Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
		if cont.Rows.Count:
			for row in cont.Rows:
				row['PY_ProductFamily'] = row['HDPY_ProductFamily']
				row['PY_AssetType']  = row['HDPY_AssetType']
				row['PY_Count'] = row['HDPY_Count']
				row['PY_LevelOffering'] = row['HDPY_LevelOffering']
				row['PY_PMCBM'] = row['HDPY_PMCBM']
				row['PY_ListPrice'] = str(float(row['HDPY_ListPrice']) * Exchange_Rate) if row['HDPY_ListPrice'] else '0' #updated for exchange rate consideration
				row['PY_Task'] = row['HDPY_Task']
				row['PY_Preventive'] = row['HDPY_Preventive']
				row['HDPY_ProductFamily'] = ""
				row['HDPY_AssetType']  = ""
				row['HDPY_Count'] = ""
				row['HDPY_LevelOffering'] = ""
				row['HDPY_PMCBM'] = ""
				row['HDPY_ListPrice'] = ""
				row['HDPY_Task'] = ""
				row['HDPY_Preventive'] = ""
				row['CY_ProductFamily'] = ""
				row.Product.ResetAttr('CBM_PRODUCT_FAMILY')
				row['CY_AssetType'] = ""
				row['Product_Type'] = "0"
				row.Product.ResetAttr('CBM_ASSET_TYPE')
	Product.Attr('SC_Renewal_check').AssignValue('1')    