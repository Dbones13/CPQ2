if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
    Invalid_cont = Product.GetContainerByName("SC_TPS_Invalid_Models")
    Invalid_cont.Rows.Clear()
    Model_cont = Product.GetContainerByName("SC_TPS_Models_Scope")
    if Model_cont.Rows.Count:
        for row in Model_cont.Rows:
            row['PY_Quantity'] = row['Hidden_Quantity']
            row['BackupRenewalQuantity'] = '0'
            row['BackupRenewalListPrice'] = '0'
            row['BackupRenewalCostPrice'] = '0'
            row['Renewal_Quantity'] = '0' #user input
            row['PY_UnitPrice'] = str(float(row['Hidden_UnitPrice']) * Exchange_Rate) if row['Hidden_UnitPrice'] else '0'
            row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['PY_UNIT_COST'] = str(float(row['Hidden_UnitCost']) * Exchange_Rate) if row['Hidden_UnitCost'] else '0'
            row['PY_COST'] = str(float(row['Hidden_Cost']) * Exchange_Rate) if row['Hidden_Cost'] else '0'
            row['Hidden_UnitPrice'] = '0'
            row['Hidden_ListPrice'] = '0'
            row['Hidden_Quantity'] = '0'
            row['Hidden_UnitCost'] = '0'
            row['Hidden_Cost'] = '0'
            row['HW_UnitPrice'] = '0' #user input
            row['HW_ListPrice'] = '0' #calculated
            row['UNIT_COST'] = '0'
            row['COST'] = '0'
            row['CY_Unit_Cost_Price'] = '0'
            row['CY_Cost_Price'] = '0'
            row.Calculate()
    Model_cont.Calculate()
Product.Attr('SC_Renewal_check').AssignValue('1')