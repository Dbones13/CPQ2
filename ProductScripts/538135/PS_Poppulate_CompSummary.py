SC_Product_Type = Product.Attr("SC_Product_Type").GetValue()
cont = Product.GetContainerByName('CBM_Pricing_Container')
cont1 = Product.GetContainerByName('CBM_Models_Cont')
discount = 0
if SC_Product_Type == 'Renewal' and Quote.GetCustomField('SC_CF_Parent_Quote_Number_Link').Content == "":
    for row in cont.Rows:
        row['PY_ProductFamily'] = row['CBM_Product_Family_OPB']
        row['PY_AssetType'] = row['CBM_Asset_Type_OPB']
        row['PY_Count'] = row['PY_Count_OPB']
        row['PY_LevelOffering'] = row['PY_Level_Count_OPB']
        row['PY_PMCBM'] = row['PY_PMCBM_OPB']
        row['PY_ListPrice'] = row['PY_Annual_Price_OPB']
        row['PY_Task'] = row['PY_Per_Task_OPB']
        row['PY_Preventive'] = row['Preventive_Main_OPB']

tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
ComparisonSummary = Product.GetContainerByName("ComparisonSummary")
if 'Scope Summary' in tabs:
    SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
    Py_List_Price = Product.Attr('CBM_Py_List_Price').GetValue()
    Py_Sell_Price = Product.Attr('CBM_Py_Sell_Price').GetValue()
    if SC_Product_Type == 'Renewal':
        for row in ComparisonSummary.Rows:
            row['Service_Product'] = 'Condition Based Maintenance'
            row['Configured_PY_List_Price'] = Py_List_Price
            row['Configured_PY_Sell_Price'] = str(float(row['Configured_PY_List_Price']) - (float(row['Configured_PY_List_Price']) * float(row['PY_Discount_SFDC']))) if row['PY_Discount_SFDC'] else str(float(row['Configured_PY_List_Price']))
            if row['Configured_PY_List_Price'] == "0":
                row['Configured_PY_List_Price'] = row['PY_List_Price_SFDC']
            row.Calculate()
        ComparisonSummary.Calculate()
for row in ComparisonSummary.Rows:
    if (row['PY_Sell_Price_SFDC']) == '':
        row['PY_Sell_Price_SFDC'] = '0'
    if (row['PY_List_Price_SFDC']) == '':
        row['PY_List_Price_SFDC'] = '0'
	if float(row['PY_List_Price_SFDC']) != '':
		discount = (float(row['PY_List_Price_SFDC']) - float(row['PY_Sell_Price_SFDC']))/float(row['PY_List_Price_SFDC'])

for row in cont1.Rows:
    if row['PY_ListPrice'] == "":
        row['PY_ListPrice'] = '0'
    row['LY_Discount'] = str(discount)
    row['PY_SellPrice'] = str(float(row['PY_ListPrice']) - (float(row['PY_ListPrice']) * discount))
cont1.Calculate()