if Product.Name != "Service Contract Products":
    if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
        Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
        Model_cont = Product.GetContainerByName("SC_Experion_Models_Scope")
        if Model_cont.Rows.Count:
            for row in Model_cont.Rows:
                row['PY_Quantity'] = row['Hidden_Quantity']
                row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
                row['PY_CostPrice'] = str(float(row['Hidden_CostPrice']) * Exchange_Rate) if row['Hidden_CostPrice'] else '0'
                row['Renewal_Quantity'] = '1'
                row['BackupRenewalQuantity'] = '1'
                row['HW_ListPrice'] = '0'
                row['Cost_Price'] = '0'
                row['Comment'] = 'No Scope Change'
                row['Hidden_ListPrice'] = '0' #row['CY_ListPrice']
                row['Hidden_CostPrice'] = '0' #
                row['Hidden_Quantity'] = '0' #row['Renewal_Quantity']
                row['Select'] = row['Select'] #if row['Select'] else False
                row.Calculate()
        Model_cont.Calculate()
    Product.Attr('SC_Renewal_check').AssignValue('1')