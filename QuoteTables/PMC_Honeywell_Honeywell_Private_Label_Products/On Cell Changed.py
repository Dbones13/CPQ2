HW = Quote.QuoteTables["PMC_Honeywell_Honeywell_Private_Label_Products"]
if HW.Rows.Count>0:
    for row in HW.Rows:
        row['Unit_Cost_Price'] = float(row['Cost_Price']) + float(row['Y_special_Cost_Price'])
        HW.Save()
        unit_cost = float(row['Unit_Cost_Price'])
        #Trace.Write('unitcost'+str(unit_cost))
        row['Extended_Cost_Price'] = float(row['Quantity']) * unit_cost
        HW.Save()
        #Trace.Write('extend'+str(float(row['Quantity']) * unit_cost))