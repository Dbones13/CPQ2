from GS_Curr_ExchRate_Mod import fn_get_curr_exchrate
saveAction = Quote.GetCustomField("R2Q_Save").Content
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
Quote_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content
exchange_rate = fn_get_curr_exchrate("USD", Quote_Currency)
if isR2Qquote and saveAction != 'Save':
	New_ProdCont = Product.GetContainerByName('WriteInProduct')
	if New_ProdCont.Rows.Count:
		getWriteinPrd = SqlHelper.GetFirst("SELECT PA.PRODUCT_ID, PA.PRODUCT_NAME FROM products PA INNER JOIN product_versions PV ON PV.product_id = PA.PRODUCT_ID WHERE PA.PRODUCT_NAME = 'Write-in Products' AND PV.is_active = 'True'")
		WriteinPrd_Id = int(getWriteinPrd.PRODUCT_ID)
		WriteinProduct = ProductHelper.CreateProduct(WriteinPrd_Id)
		WriteinProdCont = WriteinProduct.GetContainerByName('WriteInProduct')
		for itemdet in New_ProdCont.Rows:
			containerRow = WriteinProdCont.AddNewRow('WriteIn_cpq', False)
			containerRow.GetColumnByName('Category').SetAttributeValue('Common')
			containerRow["Selected_WriteIn"] = str(itemdet['Selected_WriteIn'])
			containerRow["WriteInProducts"] = str(itemdet['WriteInProducts'])
			# containerRow["Price"] = str(itemdet['Price'])
			# containerRow["Cost"] = str(itemdet['Cost'])
			containerRow["Price"] = str(float(itemdet['Price']) * exchange_rate)
			containerRow["Cost"] = str(float(itemdet['Cost']) * exchange_rate)
			containerRow["ItemQuantity"] = str(itemdet['ItemQuantity'])
			containerRow['Area'] = str(itemdet['Area'])
			containerRow["ExtendedDescription"]	= itemdet['ExtendedDescription']
			containerRow.Product.Attributes.GetByName("Writein_Category").SelectValue('Common')
			containerRow.Product.Attributes.GetByName("Selected_WriteIn").AssignValue(str(containerRow["Selected_WriteIn"]))
			containerRow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(containerRow["ItemQuantity"]))
			containerRow.Product.Attributes.GetByName("Extended Description").AssignValue(containerRow["ExtendedDescription"])
			containerRow.Product.Attributes.GetByName("Price").AssignValue(str(containerRow["Price"]))
			containerRow.Product.Attributes.GetByName("cost").AssignValue(str(containerRow["Cost"]))
			containerRow.Product.Attributes.GetByName('LCM_WriteIn_Area').AssignValue(str(containerRow["Area"]))
			containerRow.Product.ApplyRules()
			containerRow.ApplyProductChanges()
		WriteinProdCont.MakeAllRowsSelected()
		WriteinProdCont.Calculate()
		WriteinProduct.AddToQuote()
		Quote.Save(False)
SellPricesStrategy = Product.Attr('Sell Price Strategy').SelectedValue.Display
Quote.GetCustomField("SellPricestrategy").Content = SellPricesStrategy