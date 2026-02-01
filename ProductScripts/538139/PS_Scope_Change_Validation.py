#CXCPQ-89062       
BGP_ModelsScope_Container = Product.GetContainerByName("SC_BGP_Models_Scope_Cont")
row_list=[]
if BGP_ModelsScope_Container.Rows.Count>0:
    for crow in BGP_ModelsScope_Container.Rows:
        PY_Quantity = crow['PY_Quantity'] if crow['PY_Quantity'] != '' else '0'
        Renewal_Quantity=crow['Renewal_Quantity'] if crow['Renewal_Quantity'] != '' else '0'
        Previous_Year_List_Price=crow['Previous_Year_List_Price'] if crow['Previous_Year_List_Price'] != '' else '0'
        Current_Year_List_Price=crow['Current_Year_List_Price'] if crow['Current_Year_List_Price'] != '' else '0'
        SR_Price=crow['Scope Reduction Price'] if crow['Scope Reduction Price'] != '' else '0'
        SA_Price=crow['Scope Addition Price'] if crow['Scope Addition Price'] != '' else '0'
        if float(PY_Quantity)!=float(Renewal_Quantity) or float(Previous_Year_List_Price)!=float(Current_Year_List_Price):
            if float(SR_Price)==0 and float(SA_Price)==0:
                row_list.append(str(crow.RowIndex+1))
if len(row_list)>0:
    Product.Attr('SC_Scopechange_Cont_RowID').AssignValue(str(row_list))
else:
    Product.Attr('SC_Scopechange_Cont_RowID').AssignValue(str("0")) #empty list

Trace.Write('row_list:'+str(row_list))