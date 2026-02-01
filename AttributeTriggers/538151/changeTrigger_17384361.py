a=Product.Attr('SC_Scope Addition').GetValue().split(', ')
#a=['Scope Addition', 'Scope Reduction', ' No Scope Change']
Trace.Write("test"+str(a))
SESP_Models_Cont_Renewal = Product.GetContainerByName('SC_SESP Models_Renewal')
SESP_Models_Hid_Cont_Renewal = Product.GetContainerByName('SC_SESP Models Hidden')
SESP_Models_Cont_Renewal.Clear()
for row in SESP_Models_Hid_Cont_Renewal.Rows:
    Trace.Write( row['Comments'] )
    
    if row['Comments'] in a :
        #Trace.Write("chk1:"+str(l))
        i = SESP_Models_Cont_Renewal.AddNewRow()
        i['MSID'] = row['MSID']
        i['System_Name'] = row['System_Name']
        i['System_Number'] = row['System_Number']
        i['Platform'] = row['Platform']
        
        i['SESP Model'] = row['Model#']
        i['Description'] = row['Description']
        i['Previous Year Quantity'] = row['Qty']
        i['Previous Year Unit Price'] = row['Previous Year Unit Price']
        i['Previous Year List Price'] = row['Previous Year List Price']
        i['Renewal Quantity']=row['Renewal Quantity']
        i['Scope Reduction Quantity']=row['Scope Reduction Quantity']
       
        i['Comments']=row['Comments']
        i['Scope Addition Quantity']=row['Scope Addition Quantity']
        i['Honeywell List Price Per Unit']=row['Honeywell List Price Per Unit']