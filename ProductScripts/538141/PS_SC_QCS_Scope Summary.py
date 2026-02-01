SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
EXCHANGE_RATE = Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content if Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content else 1 #SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = 'USD' and To_Currency = '{}'".format(quoteCurrency))
def currency(c):
    return float(c)*float(EXCHANGE_RATE)
if SC_Product_Type == 'New':
    UI_Cont_Hidden = Product.GetContainerByName("SC_QCS_Pricing_Details_Cont_Hidden")
    UI_Cont_Hidden.Clear()
    UI_Cont_Add = Product.GetContainerByName("SC_QCS_Pricing_Details_Cont_Additional")
    UI_Cont_Add.Clear()
    quoteCurrency = Quote.SelectedMarket.CurrencyCode
    QCS_Cont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont')
    QCS_Cont.Clear()
    SC_QCS_Number_of_Machines = Product.Attr('SC_QCS_Number of Machines').GetValue()
    T = Product.Attr('SC_QCS_Subscription Tier').GetValue()
    M= Product.Attr('SC_QCS_Number of Machines').GetValue()
    MM= Product.Attr('SC_QCS_Number of Machines').GetValue()
    Y = Product.Attr('SC_QCS_Number of Years').GetValue()
    SC_QCS_Local_Onboarding_Support_Days = Product.Attr('SC_QCS_Local_Onboarding_Support_Days').GetValue()
    SC_QCS_No_Of_Machines = Product.Attr('SC_QCS_No_Of_Machines').GetValue()
    Year = int(float(Y)) if Y != '' else 0
    M = int(round(float(M)))
    if Year == 0:
        Year = 1
    Price = SqlHelper.GetFirst("select Per_year from CT_SC_QCS_MASTER_DATA where Machines = '{}'and Years = '{}' and Tier = '{}'".format(M,Year,T))
    Price1 = Price.Per_year
    if quoteCurrency != 'USD':
        M_Price = currency(Price1)
    else:
        M_Price = round(float(Price1),2)
    M_Price=M_Price*M
    i = QCS_Cont.AddNewRow(False)
    i['Service Product'] =  'QCS 4.0'
    i['Description'] = T
    i['List Price'] = str(M_Price)
    i['Select_Number_Machines'] = str(SC_QCS_Number_of_Machines)
    i['Select_Number_Years'] = str(Y)
    i['Subscription_Tier'] = str(T)
    a = UI_Cont_Hidden.AddNewRow(False)
    a['Service Product'] =  'QCS 4.0'
    a['Description'] = T
    a['List Price'] = str(M_Price)
    a['Renewal_Quantity'] = str(M)
    a['Section'] = 'Price Calculator'
    a['Service Product'] =  'QCS 4.0'
    a['Product_Name'] = T + ": " + a['Description']
    #Managed Services
    QCS_Cont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont')
    Edge_device = int(Product.ParseString("<*AttSel(SC_QCS_Edge_Device_Remote_Subscription) *>"))
    MPrice = SqlHelper.GetFirst("select Price from SC_Hardcode_Price where Name = 'Managed Services Price'")
    M = MPrice.Price
    M_Price1 = 0
    if Edge_device == 1:
        if quoteCurrency != 'USD':
            M_Price1 = currency(M)
        else:
            M_Price1 = round(float(M),2)
        j = QCS_Cont.AddNewRow(False)
        j['Description'] = 'Managed Services, Connection annual subscription price'
        j['List Price'] = str(M_Price1)
        b = UI_Cont_Hidden.AddNewRow(False)
        b['Description'] = 'Managed Services, Connection annual subscription price'
        b['List Price'] = str(M_Price1)
        b['Renewal_Quantity'] = str(MM)
        b['Section'] = "Price Calculator"
        b['Service Product'] =  'QCS 4.0'
        b['Product_Name'] = T + ": " + b['Description']
    p = UI_Cont_Add.AddNewRow(False)
    p['CY_ListPrice'] = str(M_Price + M_Price1)
    p['Service Product'] =  'QCS 4.0'
    #OneTimeService Charges
    Edge_Qty = float(0)
    QCS_Cont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont')
    quoteCurrency = Quote.SelectedMarket.CurrencyCode
    CM = Product.Attr('SC_QCS_Site_to_Cloud_Method').GetValue()
    Edge_Qty = Product.Attr('SC_QCS_Qty_Honeywell_Edge_Device').GetValue()
    if Edge_Qty == '':
        Edge_Qty = 0 
    if CM == 'Edge Device':
        X = 1
    elif CM == 'Edge Device Virtual Machine':
        X = 2
    elif CM == 'MSS-VSE/VPE (Service Node)':
        X = 3
    Price_new = SqlHelper.GetFirst("select Price from SC_Hardcode_Price where Comments = '{}' ".format(X))
    if X == 1:
        USD_Price = float(Price_new.Price)*float(Edge_Qty)
    elif X == 2:
        USD_Price = float(Price_new.Price)*float(Edge_Qty)
    elif X == 3:
        USD_Price = Price_new.Price
    if quoteCurrency != 'USD':
        test1=currency(USD_Price)
        M_Price = round(test1,2)
        Trace.Write(M_Price)    
    else:
         M_Price = round(float(USD_Price),2)
    One_Time = int(Product.ParseString("<*AttSel(SC_QCS_One Time Service Charges) *>"))
    ED_Price = OB__Price = Total_OTP = 0
    if One_Time == 1:
        k = QCS_Cont.AddNewRow(False)
        #k['Description'] = 'One-time Service Charge - Edge Device'
        k['Description'] = 'One-time Service Charge -'+CM
        k['List Price'] = str(M_Price)
        c = UI_Cont_Hidden.AddNewRow(False)
        #k['Description'] = 'One-time Service Charge - Edge Device'
        c['Description'] = 'One-time Service Charge -'+CM
        c['List Price'] = str(M_Price)
        ED_Price = str(M_Price)
        c['Renewal_Quantity'] = str(SC_QCS_Local_Onboarding_Support_Days)
        c['Section'] = 'One Time Service Charges'
        c['Service Product'] =  'QCS 4.0'
        c['Product_Name'] = T + ": " + c['Description']
    #On boarding
    OB = Product.Attr('SC_QCS_Local_Onboarding_Support_Days').GetValue()
    if OB == '':
        OB = 0
    LR = Product.Attr('SC_QCS_Local Day Rate').GetValue()
    if LR == '':
        LR = 0
    On_board = float(OB)*float(LR)
    OB_Price = round(float(On_board),2)
    if One_Time == 1 and OB > 0:
        l = QCS_Cont.AddNewRow()
        l['Description'] = 'One-time Service Charge - One-time Onboarding Services'
        l['List Price'] = str(OB_Price)
        d = UI_Cont_Hidden.AddNewRow()
        d['Description'] = 'One-time Service Charge - One-time Onboarding Services'
        d['List Price'] = str(OB_Price)
        OB__Price = str(OB_Price)
        d['Renewal_Quantity'] = str(SC_QCS_Local_Onboarding_Support_Days)
        d['Section'] = 'One Time Service Charges'
        d['Service Product'] =  'QCS 4.0'
        d['Product_Name'] = T + ": " + d['Description']
    Total_OTP = float(ED_Price) + float(OB__Price)
    Trace.Write("ED_Price   ----> "+str(ED_Price))
    Trace.Write("OB__Price   ----> "+str(OB__Price))
    Trace.Write("Total_OTP   ----> "+str(Total_OTP))
    Product.Attr('Hidden_QCS_One_Time_Price').AssignValue(str(Total_OTP))
    #Support Center
    SC = int(Product.ParseString("<* AttSel(SC_QCS_Support_Center_Select) *>"))
    SLP = Product.Attr('SC_QCS_Support_Center_List_Price').GetValue()
    if SC == 1:
        Q = QCS_Cont.AddNewRow()
        Q['Service Product'] =  'QCS Support Center'
        Q['Description'] = ''
        Q['List Price'] = str(SLP)
        e = UI_Cont_Hidden.AddNewRow()
        e['Service Product'] =  'QCS Support Center'
        e['Description'] = ''
        e['List Price'] = str(SLP)
        e['Renewal_Quantity'] = str(SC_QCS_No_Of_Machines)
        e['Section'] = "QCS Support Center"
        e['Service Product'] =  'QCS Support Center'
        e['Product_Name'] = "QCS Support Center Support:"
        l = UI_Cont_Add.AddNewRow(False)
        l['CY_ListPrice'] = str(SLP)
        l['Service Product'] =  'QCS Support Center'
    QCS_Cont.Calculate()
    UI_Cont_Hidden.Calculate()
    UI_Cont_Add.Calculate()
if SC_Product_Type == 'Renewal':
    QCS_No = (Product.Attr('SC_QCS_Number of Machines_Py').GetValue()) if (Product.Attr('SC_QCS_Number of Machines_Py').GetValue()) != "" else 0
    QCS_No_Renewal = Product.Attr('SC_QCS_Number of Machines').GetValue() if (Product.Attr('SC_QCS_Number of Machines').GetValue()) != "" else 0
    Suport_No = (Product.Attr('SC_QCS_No_Of_Machines_Py').GetValue()) if (Product.Attr('SC_QCS_No_Of_Machines_Py').GetValue()) != "" else 0
    Suport_No_Renewal = Product.Attr('SC_QCS_No_Of_Machines').GetValue() if (Product.Attr('SC_QCS_No_Of_Machines').GetValue()) != "" else 0
    prev_quote = Quote.GetCustomField("SC_CF_Parent_Quote_Number_Link").Content
    active_contract = Quote.GetCustomField("SC_CF_Parent_Contract_Number_Link").Content
    UI_Cont_Add = Product.GetContainerByName("SC_QCS_Pricing_Details_Cont_Additional")
    cont = Product.GetContainerByName('QCS_OPB_Editable_Storage_Cont')
    PY_ListPrice = 0
    SPY_ListPrice = 0
    if UI_Cont_Add.Rows.Count:
        for row in UI_Cont_Add.Rows:
            Trace.Write("row['Service Product']"+str(row['Service Product']))
            if row['Service Product'] == 'QCS 4.0':
                PY_ListPrice = row['PY_ListPrice']
            if row['Service Product'] == 'QCS Support Center':
                SPY_ListPrice = row['PY_ListPrice']
    T = Product.Attr('SC_QCS_Subscription Tier').GetValue()
    M= Product.Attr('SC_QCS_Number of Machines').GetValue()
    Y = Product.Attr('SC_QCS_Number of Years').GetValue()
    Year = int(float(Y))
    M = int(round(float(M)))
    QCS_HW_LIST_PRICE = SqlHelper.GetFirst("select New_value from CT_QCS_HW_LIST_PRICE where Tier ='{}' and Machines ='{}' and Years ='{}'".format(T,M,Y))
    if QCS_HW_LIST_PRICE is not None:
        HW_LIST_PRICE = str(QCS_HW_LIST_PRICE.New_value)
    else:
        HW_LIST_PRICE = 0
    #Trace.Write("HW_LIST_PRICE " +str(HW_LIST_PRICE))
    UI_Cont = Product.GetContainerByName("SC_QCS_Pricing_Details_Cont")
    UI_Cont_Hidden = Product.GetContainerByName("SC_QCS_Pricing_Details_Cont_Hidden")
    UI_Cont_Hidden.Clear()
    quoteCurrency = Quote.SelectedMarket.CurrencyCode
    QCS_Cont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont')
    QCS_Cont.Clear()
    if Year == 0:
        Year = 1
    if int(M):
        Price = SqlHelper.GetFirst("select Per_year from CT_SC_QCS_MASTER_DATA where Machines = '{}'and Years = '{}' and Tier = '{}'".format(M,Year,T))
        Price1 = Price.Per_year
    else:
        Price1 = 0
    if quoteCurrency != 'USD':
        M_Price = currency(Price1)
    else:
        M_Price = round(float(Price1),2)
    M_Price=M_Price*M
    PY_QCS_4 = (Product.Attr('PY_QCS_4').GetValue()) if (Product.Attr('PY_QCS_4').GetValue()) != "" else 0
    PY_QCS_Support_Center = (Product.Attr('PY_QCS_Support_Center').GetValue()) if (Product.Attr('PY_QCS_Support_Center').GetValue()) != "" else 0
    #Hidden Container
    j = UI_Cont_Hidden.AddNewRow(False)
    j['Service Product'] =  'QCS 4.0'
    j['Description'] = T
    #j['List Price'] = str(M_Price)
    if active_contract and prev_quote in ("None",""):
        for ro in cont.Rows:
            if ro['Service_Product'] == 'QCS 4.0':
                if ro['PY_Quantity'] != 0:
                    j['PY_Quantity'] = str(ro['PY_Quantity'])
                else:
                    j['PY_Quantity'] ="0"
                if ro['PY_UnitPrice'] != 0:
                    j['PY_UnitPrice'] = str(ro['PY_UnitPrice'])
                    j['Hidden_PY_ListPrice'] = str(ro['PY_UnitPrice'])
                else:
                    j['PY_UnitPrice'] = "0"
                    j['Hidden_PY_ListPrice'] = "0"
                j['PY_ListPrice'] = str(float(j['PY_UnitPrice']) * float(j['PY_Quantity']))
        if j['PY_Quantity'] == '':
            j['PY_Quantity'] = '0'
        if j['PY_UnitPrice'] == '':
            j['PY_UnitPrice'] = '0'
            j['Hidden_PY_ListPrice'] = '0'
    else:
        j['PY_Quantity'] = str(QCS_No)
        j['PY_ListPrice'] = str(PY_ListPrice)
        if float(PY_QCS_4):
            j['PY_ListPrice'] = str(float(PY_QCS_4) * float(QCS_No))
        j['Hidden_PY_ListPrice'] = str(PY_ListPrice)
    j['Renewal_Quantity'] = str(QCS_No_Renewal)
    j['PY_ListPrice'] = j['PY_ListPrice'] if j['PY_ListPrice'] != "" else "0"
    if float(j['PY_Quantity']) not in ('',0):
        j['PY_UnitPrice'] = str(float(j['PY_ListPrice'])/float(j['PY_Quantity']))
    Trace.Write("LP--->"+str(j['PY_ListPrice']))
    Trace.Write("Qty--->"+str(j['PY_Quantity']))
    Trace.Write("UP--->"+str(j['PY_UnitPrice']))
    if QCS_No_Renewal not in ("","0","0.0"):
        j['HW_UnitPrice'] = str(float(float(M_Price) / float(QCS_No_Renewal)))
    else:
        j['HW_UnitPrice'] = "0"
    j['HW_ListPrice'] = str(M_Price)
    j['Section'] = "Price Calculator"
    j['Product_Name'] = T + ": " + j['Description']
    if int(j['PY_Quantity']) > int(j['Renewal_Quantity']):
        j['SR_Quantity'] = str(int(j['Renewal_Quantity'])-int(j['PY_Quantity']))
    else:
        j['SR_Quantity']= str(0)
    if int(j['PY_Quantity']) < int(j['Renewal_Quantity']):
        j['SA_Quantity'] = str(int(j['Renewal_Quantity'])-int(j['PY_Quantity']))
    else:
        j['SA_Quantity']= str(0)
    if int(j['PY_Quantity']) < int(j['Renewal_Quantity']):
        j['Comments'] = "Scope Addition"
    elif int(j['PY_Quantity']) > int(j['Renewal_Quantity']):
        j['Comments'] = "Scope Reduction"
    else:
        j['Comments'] = "No Scope Change"
    j['PY_UnitPrice'] = j['PY_UnitPrice'] if j['PY_UnitPrice'] != "" else "0"
    j['SR_Price'] = str(float(j['PY_UnitPrice'])*float(j['SR_Quantity']))
    j['SA_Price'] = str(float(j['HW_UnitPrice'])*float(j['SA_Quantity']))
    #SC_Pricing_Escalation Changes
    if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
        if int(j['Renewal_Quantity']) > int(j['PY_Quantity']):
            j['List Price'] = str(float(j['PY_ListPrice']) + ((float(j['Renewal_Quantity']) - float(j['PY_Quantity']))*float(j['HW_UnitPrice'])))
            j['Escalation_Price'] = str(float(j['PY_Quantity'])*float(j['PY_ListPrice']))
        else:
            #j['List Price'] = str(float(j['Renewal_Quantity'])*(float(j['PY_ListPrice'])/float(j['PY_Quantity']) if j['PY_Quantity'] != '' else '0'))
            #j['Escalation_Price'] = str(float(j['Renewal_Quantity'])*(float(j['PY_ListPrice'])/float(j['PY_Quantity']) if j['PY_Quantity'] != '' else '0'))
            if j['PY_Quantity'] not in ("0",'',"0.0"):
                j['List Price'] = str(float(j['Renewal_Quantity'])*(float(j['PY_ListPrice'])/float(j['PY_Quantity'])))
                j['Escalation_Price'] = str(float(j['Renewal_Quantity'])*(float(j['PY_ListPrice'])/float(j['PY_Quantity'])))
    else:
        j['List Price'] = str(j['HW_ListPrice'])
        j['Escalation_Price'] = '0'
    j.Calculate()
    UI_Cont_Hidden.Calculate()

    #Support Center
    SC = int(Product.ParseString("<* AttSel(SC_QCS_Support_Center_Select) *>"))
    SLP = Product.Attr('SC_QCS_Support_Center_List_Price').GetValue()
    SC_ScopeRemoval = Product.Attr('SC_ScopeRemoval').GetValue()
    H = UI_Cont_Hidden.AddNewRow(False)
    H['Service Product'] =  'QCS Support Center'
    if SC == 1 and "QCS Support Center" not in SC_ScopeRemoval:
        #Hidden Container
        H['Renewal_Quantity'] = str(Suport_No_Renewal)
        if Suport_No_Renewal not in ("","0","0.00"):
            H['HW_UnitPrice'] = str(float(float(SLP) / float(Suport_No_Renewal)))
        else:
            H['HW_UnitPrice'] = "0"
        H['HW_ListPrice'] = str(SLP)
    else:
        H['Renewal_Quantity'] = "0"
        H['HW_UnitPrice'] = "0"
        H['HW_ListPrice'] = "0"
    H['Description'] = ''
    H['List Price'] = str(SLP)
    if active_contract and prev_quote in ("None",""):
        for ro in cont.Rows:
            if ro['Service_Product'] == 'QCS Support Center':
                if ro['PY_Quantity'] != 0:
                    H['PY_Quantity'] = str(ro['PY_Quantity'])
                else:
                    H['PY_Quantity'] ="0"
                if ro['PY_UnitPrice'] != 0:
                    H['PY_UnitPrice'] = str(ro['PY_UnitPrice'])
                    H['Hidden_PY_ListPrice'] = str(ro['PY_UnitPrice'])
                else:
                    H['PY_UnitPrice'] = "0"
                    H['Hidden_PY_ListPrice'] = '0'
                H['PY_ListPrice'] = str(float(H['PY_UnitPrice']) * float(H['PY_Quantity']))
        if H['PY_Quantity'] == '':
            H['PY_Quantity'] = '0'
        if H['PY_UnitPrice'] == '':
            H['PY_UnitPrice'] = '0'
            H['Hidden_PY_ListPrice'] = '0'
    else:
        H['PY_Quantity'] = str(Suport_No)
        H['PY_ListPrice'] = str(SPY_ListPrice)
        if float(PY_QCS_Support_Center):
            H['PY_ListPrice'] = str(float(PY_QCS_Support_Center)*float(Suport_No))
        H['Hidden_PY_ListPrice'] = str(SPY_ListPrice)
    #H['PY_Quantity'] = str(Suport_No)
    #H['PY_UnitPrice'] = str(SPY_ListPrice)
    H['PY_ListPrice'] = H['PY_ListPrice'] if H['PY_ListPrice'] != "" else "0"
    if float(H['PY_Quantity']) not in ('',0):
        H['PY_UnitPrice'] = str(float(H['PY_ListPrice'])/float(H['PY_Quantity']))
    H['Section'] = "QCS Support Center"
    H['Product_Name'] = "QCS Support Center Support:"
    if int(H['PY_Quantity']) > int(H['Renewal_Quantity']):
        H['SR_Quantity'] = str(int(H['Renewal_Quantity'])-int(H['PY_Quantity']))
    else:
        H['SR_Quantity']= str(0)
    if int(H['PY_Quantity']) < int(H['Renewal_Quantity']):
        H['SA_Quantity'] = str(int(H['Renewal_Quantity'])-int(H['PY_Quantity']))
    else:
        H['SA_Quantity']= str(0)
    if int(H['PY_Quantity']) < int(H['Renewal_Quantity']):
        H['Comments'] = "Scope Addition"
    elif int(H['PY_Quantity']) > int(H['Renewal_Quantity']):
        H['Comments'] = "Scope Reduction"
    else:
        H['Comments'] = "No Scope Change"
    H['PY_UnitPrice'] = H['PY_UnitPrice'] if H['PY_UnitPrice'] != "" else "0"
    H['SR_Price'] = str(float(H['PY_UnitPrice'])*float(H['SR_Quantity']))
    H['SA_Price'] = str(float(H['HW_UnitPrice'])*float(H['SA_Quantity']))
   #SC_Pricing_Escalation Changes
    if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
        if int(H['Renewal_Quantity']) > int(H['PY_Quantity']):
            H['List Price'] = str(float(H['PY_ListPrice']) + ((float(H['Renewal_Quantity']) - float(H['PY_Quantity']))*float(H['HW_UnitPrice'])))
            H['Escalation_Price'] = str(float(H['PY_Quantity'])*float(H['PY_ListPrice']))
        else:
            #H['List Price'] = str(float(H['Renewal_Quantity'])*(float(H['PY_Quantity'])*(float(H['PY_ListPrice'])/float(H['PY_Quantity']) if H['PY_Quantity'] != '' else '0')))
            #H['Escalation_Price'] = str(float(H['Renewal_Quantity'])*(float(H['PY_Quantity'])*(float(H['PY_ListPrice'])/float(H['PY_Quantity']) if H['PY_Quantity'] != '' else '0')))
            if H['PY_Quantity'] not in ("0",'',"0.0"):
                H['List Price'] = str(float(H['Renewal_Quantity'])*(float(H['PY_ListPrice'])/float(H['PY_Quantity'])))
                H['Escalation_Price'] = str(float(H['Renewal_Quantity'])*(float(H['PY_ListPrice'])/float(H['PY_Quantity'])))
    else:
        H['List Price'] = str(H['HW_ListPrice'])
        H['Escalation_Price'] = '0'
    H.Calculate()
    UI_Cont_Hidden.Calculate()
    #PY sell price code
    SP_Discount = {}
    SP_Discount_Cy = {}
    QCS_Cont = Product.GetContainerByName('SC_QCS_Pricing_Details_Cont_Hidden')
    ComparisonSummary = Product.GetContainerByName("ComparisonSummary")
    if ComparisonSummary.Rows.Count:
        for row in ComparisonSummary.Rows:
            if row['PY_Sell_Price_SFDC'] == "" :
                row['PY_Sell_Price_SFDC'] = "0"
            if row['PY_List_Price_SFDC'] == "":
                row['PY_List_Price_SFDC'] = "0"
            #discount_percent = ((float(row['PY_List_Price_SFDC']) - float(row['PY_Sell_Price_SFDC']))/float(row['PY_List_Price_SFDC']) if float(row['PY_List_Price_SFDC']) != '' else 0)
            discount_percent = float(row['PY_Discount_SFDC']) if row['PY_Discount_SFDC'] else 0
            SP_Discount[row['Service_Product']] = discount_percent
            SP_Discount_Cy[row['CY_Service_Product']] = discount_percent
    if QCS_Cont.Rows.Count:
        for hrow in QCS_Cont.Rows:
            if hrow['Service Product'] in SP_Discount.Keys:
                if hrow['PY_ListPrice'] == "" :
                    hrow['PY_ListPrice'] = "0"
                discount = SP_Discount[hrow['Service Product']]
                hrow['PY_SellPrice'] = str(float(hrow['PY_ListPrice']) - (float(hrow['PY_ListPrice']) * discount))
                hrow['LY_Discount'] = str(discount)
            elif hrow['Service Product'] in SP_Discount_Cy.Keys:
                if hrow['PY_ListPrice'] == "" :
                    hrow['PY_ListPrice'] = "0"
                discount = SP_Discount_Cy[hrow['Service Product']]
                hrow['PY_SellPrice'] = str(float(hrow['PY_ListPrice']) - (float(hrow['PY_ListPrice']) * discount))
                hrow['LY_Discount'] = str(discount)
    x = Product.Attr("SC_QCS_Scope_Button").SelectedValues
    #Trace.Write("Hey1")
    if UI_Cont_Hidden.Rows.Count:
        #Trace.Write("Hey2")
        for row in UI_Cont_Hidden.Rows:
            #Trace.Write("Hey3")
            for i in x:
                #Trace.Write("i.Display " +str(i.Display))
                #Trace.Write("row[Comments]" +str(row["Comments"]))
                if i.Display == row["Comments"]:
                    Trace.Write("Hey4")
                    Trace.Write("Qty---->"+str(row['PY_Quantity']))
                    Trace.Write("LP---->"+str(row['PY_ListPrice']))
                    Trace.Write("UP---->"+str(row['PY_UnitPrice']))
                    scopeContRow = UI_Cont.AddNewRow(False)
                    scopeContRow['Service Product'] = row['Service Product']
                    scopeContRow['Description'] = row['Description']
                    scopeContRow['Section'] = row['Section']
                    scopeContRow['PY_Quantity'] = row['PY_Quantity']
                    scopeContRow['Renewal_Quantity'] = row['Renewal_Quantity']
                    scopeContRow['PY_UnitPrice'] = row['PY_UnitPrice']
                    scopeContRow['PY_ListPrice'] = row['PY_ListPrice']
                    scopeContRow['HW_UnitPrice'] = row['HW_UnitPrice']
                    scopeContRow['HW_ListPrice'] = row['HW_ListPrice']
                    scopeContRow['SR_Quantity'] = row['SR_Quantity']
                    scopeContRow['SA_Quantity'] = row['SA_Quantity']
                    scopeContRow['Comments'] = row['Comments']
                    scopeContRow['PY_SellPrice'] = row['PY_SellPrice']
                    scopeContRow.Calculate()
    if UI_Cont_Add.Rows.Count:
        for row in UI_Cont_Add.Rows:
            Trace.Write("row['Service Product']"+str(row['Service Product']))
            if row['Service Product'] == 'QCS 4.0':
                row['CY_ListPrice'] = str(HW_LIST_PRICE)
            if row['Service Product'] == 'QCS Support Center':
                row['CY_ListPrice'] = str(HW_LIST_PRICE)
    QCS_Cont.Calculate()
    UI_Cont_Hidden.Calculate()