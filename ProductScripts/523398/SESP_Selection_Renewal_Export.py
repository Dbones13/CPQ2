sc_cont = Product.GetContainerByName("SC_SESP Models_Renewal_Export__Selection")
sc_cont.Rows.Clear()
sc_module1 = Product.GetContainerByName("Service Contract Modules")
if sc_module1.Rows.Count:
    for row in sc_module1.Rows:
        if row["Module"] == "Solution Enhancement Support Program":
            sc_module = row.Product.GetContainerByName("SC_Models_Scope_Renewal")
            if sc_module.Rows.Count > 0:
                for row in sc_module.Rows:
                    summ_hide = sc_cont.AddNewRow(False)
                    summ_hide['MSIDs']=row['MSIDs']
                    summ_hide['System_Name']=row['System_Name']
                    summ_hide['System_Number']=row['System_Number']
                    summ_hide['Platform']=row['Platform']
                    summ_hide['SESP_Models']=row['SESP_Models']
                    summ_hide['Quantity']=row['Quantity']
                    summ_hide['Renewal Quantity']=row['Renewal Quantity']
                    summ_hide['Asset Validation Line Item Number']=row['Asset Validation Line Item Number']
                    summ_hide['Description']=row['Description']
                    summ_hide['Difference']=row['Difference']
                    summ_hide['Comments']=row['Comments']
                    sc_cont.Calculate()
