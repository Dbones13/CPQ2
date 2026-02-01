if Product.Name != "Service Contract Products":
    if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
        Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
        Model_cont = Product.GetContainerByName("SC_GN_AT_Models_Scope_Cont")
        Invalid_cont = Product.GetContainerByName("SC_GN_AT_Invalid_Cont")
        Invalid_cont.Rows.Clear()
        if Model_cont.Rows.Count:
            for row in Model_cont.Rows:
                row['PY_Quantity'] = row['Hidden_Quantity']
                row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
                row['PY_CostPrice'] = str(float(row['Hidden_CostPrice']) * Exchange_Rate) if row['Hidden_CostPrice'] else '0'
                row["Model_Number"] = row["Hidden_Model"]
                row['Renewal_Quantity'] = '0'
                row['CY_ListPrice'] = '0'
                row['CY_CostPrice'] = '0'
                row['Hidden_ListPrice'] = '0' #row['CY_ListPrice']
                row['Hidden_CostPrice'] = '0' #
                row['Hidden_Quantity'] = '0' #row['Renewal_Quantity']
                row['Select'] = row['Select'] #if row['Select'] else False
                row['Comments'] = 'Scope Reduction'
                row.Calculate()
        Model_cont.Calculate()
    Product.Attr('SC_Renewal_check').AssignValue('1')