m= []
validModelCont = Product.GetContainerByName("SC_BGP_Models_Scope_Cont")
invalidCont = Product.GetContainerByName("SC_BGP_Invalid_Cont")
Valid_Asset = ['M1747','M1747-01']
if validModelCont.Rows.Count:
    for row in validModelCont.Rows:
        bgpmodel = row['Asset No']
        if bgpmodel not in Valid_Asset:
                m.append(row.RowIndex)
                invalidrow = invalidCont.AddNewRow()
                invalidrow['Asset No'] = row['Asset No']
                invalidrow['Service_Product'] = row['Service_Product']
                invalidrow['Description'] = row['Description']
                invalidrow['Quantity'] = row['Quantity']
                invalidrow['Reason'] = "Asset is not Valid"
        elif row['Description'] == '':
            m.append(row.RowIndex)
            invalidrow = invalidCont.AddNewRow()
            invalidrow['Asset No'] = row['Asset No']
            invalidrow['Service_Product'] = row['Service_Product']
            invalidrow['Description'] = row['Description']
            invalidrow['Quantity'] = row['Quantity']
            invalidrow['Reason'] = "Desc is empty"
        elif  row['Quantity'] != str(1):
            m.append(row.RowIndex)
            invalidrow = invalidCont.AddNewRow()
            invalidrow['Asset No'] = row['Asset No']
            invalidrow['Service_Product'] = row['Service_Product']
            invalidrow['Description'] = row['Description']
            invalidrow['Quantity'] = row['Quantity']
            invalidrow['Reason'] = "Quantity is not Valid"
        elif  row["Unit_List_Price"] == str(0):
            m.append(row.RowIndex)
            invalidrow = invalidCont.AddNewRow()
            invalidrow['Asset No'] = row['Asset No']
            invalidrow['Service_Product'] = row['Service_Product']
            invalidrow['Description'] = row['Description']
            invalidrow['Quantity'] = row['Quantity']
            invalidrow['Reason'] = "LP is not valid"
        elif  row["Unit_Cost_Price"] == str(0):
            invalidrow = invalidCont.AddNewRow()
            invalidrow['Asset No'] = row['Asset No']
            invalidrow['Service_Product'] = row['Service_Product']
            invalidrow['Description'] = row['Description']
            invalidrow['Quantity'] = row['Quantity']
            invalidrow['Reason'] = "CP is not valid"
validModelCont.Calculate()            
m.reverse()
for i in m:
    validModelCont.DeleteRow(i)
    validModelCont.Calculate()