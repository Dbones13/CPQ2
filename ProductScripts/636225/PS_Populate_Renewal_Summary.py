SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
quoteCurrency = Quote.SelectedMarket.CurrencyCode

query = SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = '{}' and To_Currency = '{}'".format('USD', quoteCurrency))
if query is not None:
    ExchangeRate =  eval(query.Exchange_Rate)

if SC_Product_Type == 'New':
    TPSPlus_EXP = Product.Attr('HDP_Exprion_TPSPlus_EXP').GetValue()
    HW_Summary_Cont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
    HW_Summary_Cont.Clear()
    SC_HDP_Additional_Cont = Product.GetContainerByName('SC_HDP_Additional_Cont')
    SC_HDP_Additional_Cont.Clear()
    SC_RC_Honeywell_Scope_Summary_Pricing_Hidden = Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
    SC_RC_Honeywell_Scope_Summary_Pricing_Hidden.Clear()

    TotListPrice = 0
    priceData = SqlHelper.GetList("select Name,Price from SC_HARDCODE_PRICE where Comments = 'HDP_NEW'")
    summaryProducts = {
        'Base Package Experion': {'Status': 'Yes' if Product.Attr('HDPBase Package').GetValue() =='Experion' else 'No', 'Qty': 1},
        'Base Package TPS+EXP': {'Status': 'Yes' if Product.Attr('HDPBase Package').GetValue() =='TPS+Exp' and Product.Attr('HDP_System_Size').GetValue() not in ['Small (10 Appliance)','Medium (10-25 Appliance)','Large (25-35 Appliance)'] else 'No', 'Qty': 1},
        'Base Package TPS Small': {'Status': 'Yes' if Product.Attr('HDPBase Package').GetValue() in ['TPS','TPS+Exp'] and Product.Attr('HDP_System_Size').GetValue()=='Small (10 Appliance)' else 'No', 'Qty': 1},
        'Base Package TPS Medium': {'Status': 'Yes' if Product.Attr('HDPBase Package').GetValue() in ['TPS','TPS+Exp'] and Product.Attr('HDP_System_Size').GetValue()=='Medium (10-25 Appliance)' else 'No', 'Qty': 1},
        'Base Package TPS Large': {'Status': 'Yes' if Product.Attr('HDPBase Package').GetValue() in ['TPS','TPS+Exp'] and Product.Attr('HDP_System_Size').GetValue()=='Large (25-35 Appliance)' else 'No', 'Qty': 1},
        'TPS Only Small': {'Status': 'Yes' if Product.Attr('HDP TPS Only').GetValue() and int(Product.Attr('HDP TPS Only').GetValue()) > 0 and Product.Attr('HDP_System_additional_Size').GetValue()=='Small (10 Appliance)' else 'No', 'Qty': int(Product.Attr('HDP TPS Only').GetValue())},
        'TPS Only Medium': {'Status': 'Yes' if Product.Attr('HDP TPS Only').GetValue() and int(Product.Attr('HDP TPS Only').GetValue()) > 0 and Product.Attr('HDP_System_additional_Size').GetValue()=='Medium (10-25 Appliance)' else 'No', 'Qty': int(Product.Attr('HDP TPS Only').GetValue())},
        'TPS Only Large': {'Status': 'Yes' if Product.Attr('HDP TPS Only').GetValue() and int(Product.Attr('HDP TPS Only').GetValue()) > 0 and Product.Attr('HDP_System_additional_Size').GetValue()=='Large (25-35 Appliance)' else 'No', 'Qty': int(Product.Attr('HDP TPS Only').GetValue())},
        'Safety Manager': {'Status': 'Yes' if Product.Attr('HDP Safety Manager').GetValue() and int(Product.Attr('HDP Safety Manager').GetValue()) > 0 else 'No', 'Qty': int(Product.Attr('HDP Safety Manager').GetValue())},
        'Additional Concurrent Users': {'Status': 'Yes' if Product.Attr('HDP Additional Concurrent user').GetValue() and int(Product.Attr('HDP Additional Concurrent user').GetValue()) > 0 else 'No','Qty': int(Product.Attr('HDP Additional Concurrent user').GetValue())},
        "Swap MSID" :{'Status': 'Yes' if Product.Attr('HDP_Swap_MSID').GetValue() and int(Product.Attr('HDP_Swap_MSID').GetValue()) > 0 else 'No','Qty': int(Product.Attr('HDP_Swap_MSID').GetValue())},
        "Experion/ TPS+EXP" :{'Status': 'Yes' if Product.Attr('HDP_Exprion_TPSPlus_EXP').GetValue() and int(Product.Attr('HDP_Exprion_TPSPlus_EXP').GetValue()) > 0 else 'No','Qty': int(Product.Attr('HDP_Exprion_TPSPlus_EXP').GetValue())},
        "Additional Appliance" :{'Status': 'Yes' if Product.Attr('HDP_Additional_Appliance').GetValue() and int(Product.Attr('HDP_Additional_Appliance').GetValue()) > 0 else 'No','Qty': int(Product.Attr('HDP_Additional_Appliance').GetValue())}
    }

    desired_order = [
        'Base Package Experion',
        'Base Package TPS Small',
        'Base Package TPS Medium',
        'Base Package TPS Large',
        'Base Package TPS+EXP',
        'Safety Manager',
        'Experion/ TPS+EXP',
        'TPS Only Small',
        'TPS Only Medium',
        'TPS Only Large',
        'Additional Appliance',
        'Additional Concurrent Users',
        'Swap MSID'
    ]

    output_list = [(key, summaryProducts[key]) for key in desired_order]
    for key, value in output_list:
        #Trace.Write(str(output_list))
        if value['Status'] == "Yes":
            pData = next((x for x in priceData if x.Name == key), None)
            if pData:
                row = HW_Summary_Cont.AddNewRow(False)
                XPrice = (float(pData.Price) * ExchangeRate)
                #####for TPS Size Additional Logic
                if pData.Name in ['Base Package TPS Small','Base Package TPS Medium','Base Package TPS Large']:
                    row['Description'] = "Base Package TPS" if Product.Attr('HDPBase Package').GetValue() =='TPS' else 'Base Package TPS+EXP'
                    XPrice = (float(pData.Price) * ExchangeRate) if Product.Attr('HDPBase Package').GetValue() =='TPS' else ((float(pData.Price) + 30000) * ExchangeRate)
                elif pData.Name in ['TPS Only Small','TPS Only Medium','TPS Only Large']:
                    row['Description'] = "Additional MSID TPS/TPS+EXP"
                elif pData.Name in ['Experion/ TPS+EXP']:
                    row['Description'] = "Additional MSID Experion"
                else:
                     row['Description'] = pData.Name
                #XPrice = (float(pData.Price) * ExchangeRate)
                row['Quantity'] = str(value['Qty'])
                row['Unit Price'] = str(XPrice)
                row['List Price'] = str(round(float(XPrice) * value['Qty'], 2))
                #TotUnitPrice += round(float(XPrice), 2)
                TotListPrice += round(float(XPrice) * value['Qty'], 2)
                row1 = SC_HDP_Additional_Cont.AddNewRow(False)
                #####for TPS Size Additional Logic
                if pData.Name in ['Base Package TPS Small','Base Package TPS Medium','Base Package TPS Large']:
                    row1['Description'] = "Base Package TPS" if Product.Attr('HDPBase Package').GetValue() =='TPS' else 'Base Package TPS+EXP'
                elif pData.Name in ['TPS Only Small','TPS Only Medium','TPS Only Large']:
                    row1['Description'] = "Additional MSID TPS/TPS+EXP"
                elif pData.Name in ['Experion/ TPS+EXP']:
                    row1['Description'] = "Additional MSID Experion"
                else:
                     row1['Description'] = pData.Name
                row1['CY_Quantity'] = str(value['Qty'])
                row1['CY_UnitPrice'] = str(XPrice)
                row1['CY_ListPrice'] = str(round(float(XPrice) * value['Qty'], 2))
                TotListPrice += round(float(XPrice) * value['Qty'], 2)
                row1.Calculate()
                row2 = SC_RC_Honeywell_Scope_Summary_Pricing_Hidden.AddNewRow(False)
                #####for TPS Size Additional Logic
                if pData.Name in ['Base Package TPS Small','Base Package TPS Medium','Base Package TPS Large']:
                    row2['Description'] = "Base Package TPS" if Product.Attr('HDPBase Package').GetValue() =='TPS' else 'Base Package TPS+EXP'
                elif pData.Name in ['TPS Only Small','TPS Only Medium','TPS Only Large']:
                    row2['Description'] = "Additional MSID TPS/TPS+EXP"
                elif pData.Name in ['Experion/ TPS+EXP']:
                    row2['Description'] = "Additional MSID Experion"
                else:
                     row2['Description'] = pData.Name
                row2['Quantity'] = str(value['Qty'])
                row2['Unit Price'] = str(XPrice)
                row2['List Price'] = str(round(float(XPrice) * value['Qty'], 2))
                row2['HW_ListPrice'] = row2['Unit Price']
                row2['Hidden_Quantity'] = str(value['Qty'])
                row2['Hidden_UnitPrice'] = str(XPrice)
                row2['Hidden_ListPrice'] = str(round(float(XPrice) * value['Qty'], 2))
                row2.Calculate()
    HW_Summary_Cont.Calculate()
    SC_HDP_Additional_Cont.Calculate()
    SC_RC_Honeywell_Scope_Summary_Pricing_Hidden.Calculate()

    cu = Product.Attr('SC_Concurrent_Users').GetValue()
    md = Product.Attr('SC_Num_of_MSID').GetValue()

elif SC_Product_Type == 'Renewal':
    AdditionalCont = Product.GetContainerByName('SC_HDP_Additional_Cont')
    HW_Summary_Cont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
    SummaryContHidden = Product.GetContainerByName('SC_RC_Honeywell_Scope_Summary_Pricing_Hidden')
    HW_Summary_Cont.Clear()
    SummaryContHidden.Rows.Clear()

    TotListPrice = 0
    priceData = SqlHelper.GetList("select Name,Price from SC_HARDCODE_PRICE where Comments = 'HDP'")
    summaryProducts = {
        'Base Package Experion': {'Status': Product.Attr('SC_Experion_System').GetValue(), 'Qty': 1},
        'Base Package TPS': {'Status': Product.Attr('SC_TPS_LCN_Connected_System').GetValue(), 'Qty': 1},
        'Base Package Safety Manager': {'Status': Product.Attr('SC_Safety_Manager_System').GetValue(), 'Qty': 1},
        'No of Concurrent Users or Stations': {'Status': 'Yes' if Product.Attr('SC_Concurrent_Users').GetValue() and int(Product.Attr('SC_Concurrent_Users').GetValue()) >= 0 else 'No','Qty': int(Product.Attr('SC_Concurrent_Users').GetValue())},
        "No of MSID's": {'Status': 'Yes' if Product.Attr('SC_Num_of_MSID').GetValue() and int(Product.Attr('SC_Num_of_MSID').GetValue()) > 0 else 'No','Qty': int(Product.Attr('SC_Num_of_MSID').GetValue())}
    }

    desired_order = [
        'Base Package Experion',
        'Base Package TPS',
        'Base Package Safety Manager',
        "No of MSID's",
        'No of Concurrent Users or Stations'
    ]

    output_list = [(key, summaryProducts[key]) for key in desired_order]
    for key, value in output_list:
        St = 'Yes' #value['Status']
        if Quote.GetCustomField('SC_CF_Parent_Quote_Number_Link').Content == "":
            St = "Yes"
        if St == "Yes":
            pData = next((x for x in priceData if x.Name == key), None)
            if pData:
                XPrice = (float(pData.Price) * ExchangeRate)
                row = SummaryContHidden.AddNewRow(False)
                row['Description'] = pData.Name
                row['Quantity'] = str(value['Qty'])
                if row['Description'] == "Base Package TPS" and Product.Attr('SC_TPS_LCN_Connected_System').GetValue() == "No":
                    row['Quantity'] = '0'
                if row['Description'] == "Base Package Safety Manager" and Product.Attr('SC_Safety_Manager_System').GetValue() == "No":
                    row['Quantity'] = '0'
                row['HW_Unit_Price'] = str(XPrice)
                row['HW_ListPrice'] = row['HW_Unit_Price']
                row['List Price'] = str(round(float(XPrice) * value['Qty'], 2))
                row['Hidden_Quantity'] = str(value['Qty'])
                row['Hidden_UnitPrice'] = str(XPrice)
                row['Hidden_ListPrice'] = str(round(float(row['HW_ListPrice']) * float(row['Quantity'])))
                if row['Quantity'] == "":
                    row['Quantity'] = "0"
                if row['PY_Quantity'] == "":
                    row['PY_Quantity'] = "0"
                if int(row['Quantity']) > int(row['PY_Quantity']):
                    row['SR_Quantity'] = '0'
                    row['SA_Quantity'] = str(int(row['Quantity'])-int(row['PY_Quantity']))
                    row['Comments'] = "Scope Addition"
                elif int(row['Quantity']) < int(row['PY_Quantity']):
                    row['SR_Quantity'] = str(int(row['Quantity'])-int(row['PY_Quantity']))
                    row['SA_Quantity'] = '0'
                    row['Comments'] = "Scope Reduction"
                else:
                    row['SR_Quantity'] = '0'
                    row['SA_Quantity'] = '0'
                    row['Comments'] = "No Scope Change"
                TotListPrice += round(float(XPrice) * value['Qty'], 2)
                if AdditionalCont.Rows.Count:
                    for row1 in AdditionalCont.Rows:
                        if row['Description'] == row1['Description']:
                            row['PY_Quantity'] = row1['PY_Quantity']
                            row['PY_UnitPrice'] = row1['PY_UnitPrice']
                            row['PY_ListPrice'] = row1['PY_ListPrice']
                            if int(row['Quantity']) > int(row['PY_Quantity']):
                                row['SR_Quantity'] = '0'
                                row['SA_Quantity'] = str(int(row['Quantity'])-int(row['PY_Quantity']))
                                row['Comments'] = "Scope Addition"
                            elif int(row['Quantity']) < int(row['PY_Quantity']):
                                row['SR_Quantity'] = str(int(row['Quantity'])-int(row['PY_Quantity']))
                                row['SA_Quantity'] = '0'
                                row['Comments'] = "Scope Reduction"
                            else:
                                row['SR_Quantity'] = '0'
                                row['SA_Quantity'] = '0'
                                row['Comments'] = "No Scope Change"
                            break
                        else:
                            row['PY_Quantity'] = '0'
                            row['PY_UnitPrice'] = '0'
                            row['PY_ListPrice'] = '0'
                            row['SR_Quantity'] = '0'
                            row['SA_Quantity'] = row['Quantity']
                            row['Comments'] = "Scope Addition"
                SummaryContHidden.Calculate()
    addContList = []
    addinthelist = []
    if SummaryContHidden.Rows.Count:
        for row in SummaryContHidden.Rows:
            for addrow in AdditionalCont.Rows:
                addContList.append(addrow["Description"])
                if row["Description"] == addrow["Description"]:
                    addrow["CY_Quantity"] = row["Quantity"]
                    addrow["CY_UnitPrice"] = row["HW_Unit_Price"]
                    addrow["CY_ListPrice"] = str(float(row["HW_Unit_Price"]) * float(row["Quantity"]))
                elif row["Description"] not in addContList:
                    addinthelist.append(row["Description"])
            if row['Description'] in addinthelist:
                add_row_new = AdditionalCont.AddNewRow(False)
                add_row_new["Description"] = row["Description"]
                add_row_new["PY_Quantity"] = row["PY_Quantity"]
                add_row_new["PY_UnitPrice"] = row["PY_UnitPrice"]
                add_row_new["PY_ListPrice"] = row["PY_ListPrice"]
                add_row_new["CY_Quantity"] = row["Quantity"]
                add_row_new["CY_UnitPrice"] = row["HW_Unit_Price"]
                add_row_new["CY_ListPrice"] = str(float(row["HW_Unit_Price"]) * float(row["Quantity"]))
                add_row_new.Calculate()
            AdditionalCont.Calculate()


    x = Product.Attr("SC_HDP_RC_Selection").SelectedValues
    if SummaryContHidden.Rows.Count:
        for row in SummaryContHidden.Rows:
            for i in x:
                if i.Display == row["Comments"]:
                    HW_summary_row = HW_Summary_Cont.AddNewRow(False)
                    HW_summary_row['Description'] = row['Description']
                    HW_summary_row['Quantity'] = row['Quantity']
                    HW_summary_row['R_Quantity'] = row['Quantity']
                    HW_summary_row['PY_Quantity'] = row['PY_Quantity']
                    HW_summary_row['PY_UnitPrice'] = row['PY_UnitPrice']
                    HW_summary_row['PY_ListPrice'] = row['PY_ListPrice']
                    HW_summary_row['HW_ListPrice'] = row['HW_ListPrice']
                    HW_summary_row['Honeywell_List_Price'] = str (float(row['HW_ListPrice']) * float(HW_summary_row['R_Quantity']))
                    HW_summary_row['SR_Quantity'] = row['SR_Quantity']
                    if row['PY_UnitPrice'] == "":
                        row['PY_UnitPrice'] = "0"
                    HW_summary_row['SR_Price'] = str (float(row['SR_Quantity']) * float(row['PY_UnitPrice']))
                    HW_summary_row['SA_Quantity'] = row['SA_Quantity']
                    HW_summary_row['SA_Price'] = str(float(row['SA_Quantity']) * float(row['HW_ListPrice']))
                    HW_summary_row['Comments'] = row['Comments']
                    HW_summary_row.Calculate()
        HW_Summary_Cont.Calculate()
