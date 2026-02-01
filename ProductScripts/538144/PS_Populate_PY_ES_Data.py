if Product.Name != "Service Contract Products":
    if Product.Attr('SC_Product_Type').GetValue() == "Renewal" and Product.Attr('SC_Renewal_check').GetValue() == "0":
        Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
        CY_AssetDetails_Cont = Product.GetContainerByName("Asset_details_ServiceProd")
        PY_AssetDetails_Cont = Product.GetContainerByName("ES_PY_Asset_Details")
        ES_Asset_Summary_Cont = Product.GetContainerByName("ES_Asset_Summary")
        if CY_AssetDetails_Cont.Rows.Count:
            for cy_row in CY_AssetDetails_Cont.Rows:
                Trace.Write("cy_row[List Price] Service contract enabled services ---> "+str(cy_row["List Price"]))
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
            ES_Asset_Summary_Cont.Calculate()
            Product.Attr('SC_Renewal_check').AssignValue('1')