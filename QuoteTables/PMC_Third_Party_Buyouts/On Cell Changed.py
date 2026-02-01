TP = Quote.QuoteTables["PMC_Third_Party_Buyouts"]
if TP.Rows.Count>0:
    for row in TP.Rows:
        row['Unit_Sell_Price'] = float(row['Purchase_Price_Unit']) / (1- float(row['Margin'])/100)
        TP.Save()
        row['Extended_3_rd_party_Cost_Price'] = float(row['Quantity']) * float(row['Third_party_Cost_Price'])
        TP.Save()
        row['Extended_Purchase_Price'] = float(row['Quantity']) * float(row['Purchase_Price_Unit'])
        TP.Save()
        row['Extended_Sell_Price'] = float(row['Quantity']) * float(row['Unit_Sell_Price'])
        TP.Save()
#ScriptExecutor.ExecuteGlobal('GS_Populate_HoneywellProducts')