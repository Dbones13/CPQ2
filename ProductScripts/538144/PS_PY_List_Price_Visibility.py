if Product.Name != "Service Contract Products":
    Product_type = Product.Attr('SC_Product_Type').GetValue()
    Quote_Number = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content.strip()
    #if Product_type == 'Renewal' and Quote_Number != '':
    if Product_type == 'Renewal':
        #make list price column as editable
        TagParserProduct.ParseString('<*CTX ( Container(ES_PY_Asset_Details ).Column(List Price).SetPermission(Editable) )*>')
        compCont = Product.GetContainerByName("ESComparisonSummary")
        cyServiceProduct = ''
        pyServiceProduct = ''
        descopeSelected = False
        if compCont.Rows.Count > 0:
            compContRow = compCont.Rows[0]
            cyServiceProduct = Product.Attr('EnabledServices_servprod').GetValue()
            pyServiceProduct = compContRow['Service_Product']
            descopeSelected = compContRow.IsSelected
        if descopeSelected  and cyServiceProduct != pyServiceProduct:
            #make list price column as editable
            TagParserProduct.ParseString('<*CTX ( Container(ES_PY_Asset_Details ).Column(List Price).SetPermission(ReadOnly) )*>')
        else:
            ES_Asset_Summary = Product.GetContainerByName("ES_Asset_Summary")
            for row1 in ES_Asset_Summary.Rows:
                if row1["PY_List_Price"] == "0":
                    row1["PY_List_Price"] = Product.GetContainerByName('ES_PY_Asset_Details').TotalRow.Columns['List Price'].Value
                    row1.Calculate()
            ES_Asset_Summary.Calculate()
        if compCont.Rows.Count > 0:
            compContRow = compCont.Rows[0]
            if not descopeSelected:
                Matrix_Lic = float(Product.Attr('SC_ES_Matrikon_License').GetValue()) if Product.Attr("SC_ES_Matrikon_License").GetValue() != '' else 0
                compContRow['Configured_PY_List_Price'] = str(float(Product.GetContainerByName('ES_PY_Asset_Details').TotalRow.Columns['List Price'].Value) + Matrix_Lic)
                discount_percent = ((float(compContRow['PY_List_Price_SFDC']) - float(compContRow['PY_Sell_Price_SFDC']))/float(compContRow['PY_List_Price_SFDC']) if float(compContRow['PY_List_Price_SFDC']) != '' else 0)
                compContRow['Configured_PY_Sell_Price'] = str(float(compContRow['Configured_PY_List_Price']) - (float(compContRow['Configured_PY_List_Price']) * discount_percent))
                compContRow['List_Price_Delta'] = str(float(compContRow['PY_List_Price_SFDC']) - float(compContRow['Configured_PY_List_Price']))
                compContRow['Sell_Price_Delta'] = str(float(compContRow['PY_Sell_Price_SFDC']) - float(compContRow['Configured_PY_Sell_Price']))
            ScriptExecutor.Execute('PS_ES_OPB_Popup_Message')