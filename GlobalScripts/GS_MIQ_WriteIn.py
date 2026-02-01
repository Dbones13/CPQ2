# CXCPQ-50830: GS_MIQ_WriteIn: Add "Write-In MIQ Optimize Annual Update Fee" when "Measurement IQ System" System is added in the new expansion project and attribute MIQ_Perpetual_Contract is Yes.
# write in Price = 18% of Total Price * Years of Annual Fee.  Cost = 45% of the write in Price
# If "Perpetual Contract" = Yes, Years of Annual Fee = "Contract Length" - 1

def AddMIQWriteIn():
    writeInProductQuery = SqlHelper.GetFirst("SELECT Product,Category,Description, ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure from WriteInProducts where Product = 'Write-In MIQ Optimize Annual Update Fee'")
    if writeInProductQuery is not None:
        WriteInItem = ProductHelper.CreateProduct('WriteIn_cpq')
        WriteInItem.Attr('Writein_Category').SelectValue(str(writeInProductQuery.Category))
        WriteInItem.Attr('WriteInProductsChoices').SelectValue(str(writeInProductQuery.Product))
        WriteInItem.Attr('Selected_WriteIn').AssignValue(str(writeInProductQuery.Product))
        WriteInItem.Attr('Description').AssignValue(str(writeInProductQuery.Description))
        WriteInItem.Attr('Product Line').AssignValue(str(writeInProductQuery.ProductLine))
        WriteInItem.Attr('Product Line Description').AssignValue(str(writeInProductQuery.ProductLineDescription))
        WriteInItem.Attr('Product line sub group').AssignValue(str(writeInProductQuery.ProductLineSubGroup))
        WriteInItem.Attr('PLSG description').AssignValue(str(writeInProductQuery.ProductLineSubGroupDescription))
        WriteInItem.Attr('Unit of Measure').AssignValue(str(writeInProductQuery.UnitofMeasure))
        WriteInItem.Attr('ItemQuantity').AssignValue('1')
        WriteInItem.Attr('Extended Description').AssignValue('MIQ Optimize Annual Update Fee')
        WriteInItem.ApplyRules()
        x = WriteInItem.AddToQuote()

def update_price(item, p_MIQListPrice, p_Contract_Len):
	lv_price = p_MIQListPrice*(p_Contract_Len-1)*float(0.18)
	item.ListPrice = lv_price
	lv_cost = lv_price*float(0.45)
	item.Cost = lv_cost

# CXCPQ-50830 Check quote line items has "Measurement IQ System".
lv_MIQ_Perp_contr_flag = 'No'
lv_Contract_Len = 0
lv_MIQListPrice = 0
write_in_item = None
miq_found = False
if Quote.GetCustomField("Quote Type").Content == "Projects" and Quote.Items.Count and Quote.ContainsAnyProductByName('Measurement IQ System'):
	if not Quote.ContainsAnyProductByPartNumber('Write-In MIQ Optimize Annual Update Fee'):
		AddMIQWriteIn()
	for i in Quote.Items:
		if i.PartNumber == 'Write-In MIQ Optimize Annual Update Fee':
			write_in_item = i
		elif i.ProductName == 'Measurement IQ System':
			miq_found = True
			Trace.Write('ListPrice:'+str(i.ListPrice))
			lv_MIQListPrice = i.ListPrice
			for attr in i.SelectedAttributes:
				if attr.Name in ('MIQ_Perpetual_Contract', 'MIQ_Contract_Length'):
					for value in attr.Values:
						if attr.Name == 'MIQ_Perpetual_Contract' and value.Display == 'Yes':
							lv_MIQ_Perp_contr_flag = 'Yes'
						elif attr.Name == 'MIQ_Contract_Length' and value.Display > 0:
							lv_Contract_Len = float(value.Display)
		if write_in_item is not None and miq_found:
			break
# Add WriteIn only when MIQ_Perpetual_Contract is Yes
	if lv_MIQ_Perp_contr_flag == 'Yes' and lv_Contract_Len > 0 and write_in_item is not None:
		update_price(write_in_item, float(lv_MIQListPrice), float(lv_Contract_Len))