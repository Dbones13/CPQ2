cont = Product.GetContainerByName('SC_Labor_Summary_Container')
if cont.Rows.Count:
    for row in cont.Rows:
        row['Honeywell_List_Price_Hidden'] = row['Total_Honeywell_List_Price']
        row.Calculate()
cont.Calculate()