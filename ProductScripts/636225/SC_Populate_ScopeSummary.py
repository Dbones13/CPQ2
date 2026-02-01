HW_Summary_Cont = Product.GetContainerByName('SC_Honeywell_Scope_Summary_Pricing')
HW_Summary_Cont.Clear()
Product_Type=Product.Attr('SC_Product_Type').GetValue()
TotListPrice = 0

if Product_Type !="New":
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
        #Trace.Write(str(output_list))
        if value['Status'] == "Yes":
            pData = next((x for x in priceData if x.Name == key), None)
            if pData:
                row = HW_Summary_Cont.AddNewRow(False)
                row['Description'] = pData.Name
                row['Quantity'] = str(value['Qty'])
                row['Unit Price'] = str(pData.Price)
                row['List Price'] = str(round(float(pData.Price) * value['Qty'], 2))
                #TotUnitPrice += round(float(pData.Price), 2)
                TotListPrice += round(float(pData.Price) * value['Qty'], 2)

    #row = HW_Summary_Cont.AddNewRow(False)
    #row['Description'] = "Total List Price Per Year"
    #row['List Price'] = str(round(TotListPrice, 2))
    #row['Unit Price'] = str(round(TotUnitPrice, 2))
    HW_Summary_Cont.Calculate()

    cu = Product.Attr('SC_Concurrent_Users').GetValue()
    md = Product.Attr('SC_Num_of_MSID').GetValue()

    
    
###Added Logic for new UI Contract New
else:
    priceData = SqlHelper.GetList("select Name,Price from SC_HARDCODE_PRICE where Comments = 'HDP_NEW'")
    summaryProducts = {
        'Base Package Experion': {'Status': 'Yes' if Product.Attr('HDPBase Package').GetValue() =='Experion' else 'No', 'Qty': 1},
        'Base Package TPS+EXP': {'Status': 'Yes' if Product.Attr('HDPBase Package').GetValue() =='TPS+EXP' else 'No', 'Qty': 1},
        #'Base Package TPS': {'Status': 'Yes' if Product.Attr('HDPBase Package').GetValue() =='TPS' and Product.Attr('HDP_System_Size').GetValue() not in ['None',''] else 'No', 'Qty': 1},
        'Base Package Safety Manager': {'Status': 'Yes' if Product.Attr('HDP Safety Manager').GetValue() and int(Product.Attr('HDP Safety Manager').GetValue()) > 0 else 'No', 'Qty': int(Product.Attr('HDP Safety Manager').GetValue())},
        'No of Concurrent Users or Stations': {'Status': 'Yes' if Product.Attr('HDP Additional Concurrent user').GetValue() and int(Product.Attr('HDP Additional Concurrent user').GetValue()) > 0 else 'No','Qty': int(Product.Attr('HDP Additional Concurrent user').GetValue())},
        "No of MSID's": {'Status': 'Yes' if Product.Attr('SC_Num_of_MSID').GetValue() and int(Product.Attr('SC_Num_of_MSID').GetValue()) > 0 else 'No','Qty': int(Product.Attr('SC_Num_of_MSID').GetValue())},
        "Swap MSID" :{'Status': 'Yes' if Product.Attr('HDP_Swap_MSID').GetValue() and int(Product.Attr('HDP_Swap_MSID').GetValue()) > 0 else 'No','Qty': int(Product.Attr('HDP_Swap_MSID').GetValue())},
        "Additional Appliance" :{'Status': 'Yes' if Product.Attr('HDP_Additional_Appliance').GetValue() and int(Product.Attr('HDP_Additional_Appliance').GetValue()) > 0 else 'No','Qty': int(Product.Attr('HDP_Additional_Appliance').GetValue())}
    }

    desired_order = [
        'Base Package Experion',
        #'Base Package TPS',
        'Base Package TPS+EXP',
        'Base Package Safety Manager',
        "No of MSID's",
        'Additional Appliance',
        'No of Concurrent Users or Stations',
        'Swap MSID'
    ]
    output_list = [(key, summaryProducts[key]) for key in desired_order]
    for key, value in output_list:
        #Trace.Write(str(output_list))
        if value['Status'] == "Yes":
            pData = next((x for x in priceData if x.Name == key), None)
            if pData:
                row = HW_Summary_Cont.AddNewRow(False)
                row['Description'] = pData.Name
                row['Quantity'] = str(value['Qty'])
                row['Unit Price'] = str(pData.Price)
                row['List Price'] = str(round(float(pData.Price) * value['Qty'], 2))
                #TotUnitPrice += round(float(pData.Price), 2)
                TotListPrice += round(float(pData.Price) * value['Qty'], 2)

    #row = HW_Summary_Cont.AddNewRow(False)
    #row['Description'] = "Total List Price Per Year"
    #row['List Price'] = str(round(TotListPrice, 2))
    #row['Unit Price'] = str(round(TotUnitPrice, 2))
    HW_Summary_Cont.Calculate()