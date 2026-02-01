if Product.Name != "Service Contract Products":
    ES_Asset_Summary_Cont = Product.GetContainerByName("ES_Asset_Summary")
    preYearQuote = Quote.GetCustomField('SC_CF_Parent_Quote_Number_Link').Content.strip()
    if Product.Attr('SC_Product_Type').GetValue() == "Renewal" and Product.Attr('SC_Renewal_check').GetValue() == "0":
        Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
        CY_AssetDetails_Cont = Product.GetContainerByName("Asset_details_ServiceProd")
        PY_AssetDetails_Cont = Product.GetContainerByName("ES_PY_Asset_Details")
        if CY_AssetDetails_Cont.Rows.Count:
            for cy_row in CY_AssetDetails_Cont.Rows:
                py_row = PY_AssetDetails_Cont.AddNewRow(False)
                for col in py_row.Columns:
                    if col.Name == "List Price":
                        py_row[col.Name] = str(float(cy_row[col.Name]) * Exchange_Rate)
                    else:
                        py_row[col.Name] = cy_row[col.Name]
                py_row.Calculate()
            PY_AssetDetails_Cont.Calculate()
            summary = ES_Asset_Summary_Cont.AddNewRow(False)
            summary.Calculate()
            if preYearQuote == '':
                summary['No_MSID_PY'] = '0'
            ES_Asset_Summary_Cont.Calculate()
            Product.Attr('SC_Renewal_check').AssignValue('1')
            CY_AssetDetails_Cont.Rows[0].Columns['List Price'].HeaderLabel = 'CY List Price'
        CY_AssetDetails_Cont.Rows.Clear()
        Product.Attr('SC_Renewal_check').AssignValue('1')
    elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":
        if ES_Asset_Summary_Cont.Rows.Count == 0:
            summary = ES_Asset_Summary_Cont.AddNewRow(False)
            summary.Calculate()
            if preYearQuote == '':
                summary['No_MSID_PY'] = '0'
            ES_Asset_Summary_Cont.Calculate()
