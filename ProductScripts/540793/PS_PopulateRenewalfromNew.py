if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
    Invalid_cont = Product.GetContainerByName("SC_Local_Support_invalidCont")
    Invalid_cont.Rows.Clear()
    Model_cont = Product.GetContainerByName("SC_Local_Support_Standby_validModel")
    if Model_cont.Rows.Count:
        for row in Model_cont.Rows:
            row['Previous Year Quantity'] = row['Hidden_Quantity']
            row['BackupRenewalQuantity'] = '0'
            row['BackupRenewalListPrice'] = '0'
            row['BackupRenewalCostPrice'] = '0'
            row['Renewal Quantity'] = '0' #user input
            row['Previous Year Unit List Price'] = str(float(row['Hidden_UnitListPrice']) * Exchange_Rate) if row['Hidden_UnitListPrice'] else '0'
            row['Previous Year List Price'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['Previous Year Unit Cost price'] = str(float(row['Hidden_UnitCostPrice']) * Exchange_Rate) if row['Hidden_UnitCostPrice'] else '0'
            row['Previous Year Cost price'] = str(float(row['Hidden_CostPrice']) * Exchange_Rate) if row['Hidden_CostPrice'] else '0'
            row['Hidden_UnitListPrice'] = '0'
            row['Hidden_ListPrice'] = '0'
            row['Hidden_Quantity'] = '0'
            row['Hidden_UnitCostPrice'] = '0'
            row['Hidden_CostPrice'] = '0'
            row['Honeywell List Price Per Unit'] = '0'
            row['Honeywell List Price'] = '0' 
            row['Current Year Unit Cost Price'] = '0'
            row['Current Year Cost Price'] = '0'
            row['Unit List Price'] = '0'
            row['List Price'] = '0'
            row['Unit Cost  Price'] = '0'
            row['Cost Price'] = '0'
            row['Comment']= "Scope Reduction"
            row['Backup_SC_Comment_HR_RWL']= "Scope Reduction"
            row.Calculate()
    Model_cont.Calculate()
Product.Attr('SC_Renewal_check').AssignValue('1')