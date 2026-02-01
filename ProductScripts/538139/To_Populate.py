if Product.Name != "Service Contract Products":
    QuoteType=Product.Attr('SC_Product_Type').GetValue()
    if QuoteType=="Renewal":
        Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
        validModelCont = Product.GetContainerByName("SC_BGP_Models_Scope_Cont")
        for i in validModelCont.Rows:
            i['Previous_Year_List_Price']= str(float(i['Unit_List_Price']) * Exchange_Rate) if i['Unit_List_Price'] else '0'
            i['Previous_Year_Cost_Price']= str(float(i['Unit_Cost_Price']) * Exchange_Rate) if i['Unit_Cost_Price'] else '0'
            i['Current_Year_List_Price']='0.00'
            i['PY_Quantity'] = i['Hidden_Quantity']
            i['Renewal_Quantity'] = '0'
            i['Hidden_Quantity'] = '0'
            i.Calculate()
        validModelCont.Calculate()
    Product.Attr('SC_Renewal_check').AssignValue('1')
