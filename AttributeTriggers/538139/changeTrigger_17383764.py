a=Product.Attr('SC_Scope Addition').GetValue().split(', ')
#a=['Scope Addition', 'Scope Reduction', ' No Scope Change']
Trace.Write("test"+str(a))
SC_BGP_Models_Renewal=Product.GetContainerByName('SC_BGP_Models_Cont')
BGP_Models_Hid_Cont_Renewal=Product.GetContainerByName('SC_BGP_Models_Cont_Hidden')
SC_BGP_Models_Renewal.Clear()
for row in BGP_Models_Hid_Cont_Renewal.Rows:
    Trace.Write( row['Comments'] )
    
    if row['Comments'] in a :
        #Trace.Write("chk1:"+str(l))
        i = SC_BGP_Models_Renewal.AddNewRow()
        i['Service_Product'] = row['Service_Product']
        i['Quantity'] = row['Quantity']
        i['Renewal_Quantity'] = row['Renewal_Quantity']
        i['PY_Quantity'] = row['PY_Quantity']
        i['Honeywell_List_Price'] = row['Honeywell_List_Price']
        i['Previous_Year_List_Price'] = row['Previous_Year_List_Price']
        i['Scope Reduction Price']=row['Scope Reduction Price']
        i['Scope Addition Price']=row['Scope Addition Price']
        i['Model_Number'] = row['Model_Number']
        i['Description'] = row['Description']
        i['Asset_No'] = row['Asset_No']
        i['Comments']=row['Comments']
        i['Previous_Year_Cost_Price']=row['Previous_Year_Cost_Price']
                       
        i['Current_Year_Cost_Price']=row['Current_Year_Cost_Price']