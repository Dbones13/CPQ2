# GS_SC_UpdateProducts script has reached maximum character limit. 
#Created this script and added WEP, 

def GenProdDictFromConRow(row,spRemovalList,spRemovalDist,scDict=None, productlist=None):
    if row['Module'] == 'Workforce Excellence Program':
        Trace.Write('Workforce Excellence Program >>>>>> check')
        WEPDict = {}
        WEPEntDict = {}
        WEPEntitleContainer = row.Product.GetContainerByName('SC_WEP_Offering_Entitlement')
        for erow in WEPEntitleContainer.Rows:
            WEPEntDict.setdefault(erow['Offering_Name'], []).append(erow['Entitlements'])
        WEPContainer = row.Product.GetContainerByName('SC_WEP_Offering_ServiceProduct_Hidden')
        for wrow in WEPContainer.Rows:
            if wrow['Service_Product'] in WEPDict:
                notAvailable = True
                for offeringdict in WEPDict[wrow['Service_Product']]:
                    if offeringdict['OfferingName'] == wrow['Offering_Name']:
                        offeringdict['ListPrice'] = float(offeringdict['ListPrice']) + float(wrow['List_Price'] if wrow['List_Price'] else 0)
                        offeringdict['CostPrice'] = float(offeringdict['CostPrice']) + float(wrow['CY_CostPrice'] if wrow['CY_CostPrice'] else 0)
                        offeringdict['Escalation_Price'] = float(offeringdict['Escalation_Price']) + float(wrow['Escalation_Price'] if wrow['Escalation_Price'] else 0)
                        offeringdict['PY_ListPrice'] = float(offeringdict['PY_ListPrice']) + float(wrow['PY_ListPrice'] if wrow['PY_ListPrice'] else 0)
                        offeringdict['PY_SellPrice'] = float(offeringdict['PY_SellPrice']) + float(wrow['PY_SellPrice'] if wrow['PY_SellPrice'] else 0)
                        offeringdict['SR_Price'] = float(offeringdict['SR_Price']) + float(wrow['SR_Price'] if wrow['SR_Price'] else 0)
                        offeringdict['SA_Price'] = float(offeringdict['SA_Price']) + float(wrow['SA_Price'] if wrow['SA_Price'] else 0)
                        notAvailable = False
                if notAvailable:
                    WEPDict[wrow['Service_Product']].append({'OfferingName' : wrow['Offering_Name'], 'ListPrice' : float(wrow['List_Price']) if wrow['List_Price'] else 0, 'CostPrice' : float(wrow['CY_CostPrice']) if wrow['CY_CostPrice'] else 0,'ExtDescription': WEPEntDict[wrow['Offering_Name']] if wrow['Offering_Name'] in WEPEntDict else '','Escalation_Price': float(wrow['Escalation_Price']) if wrow['Escalation_Price'] else 0,'PY_ListPrice': float(wrow['PY_ListPrice']) if wrow['PY_ListPrice'] else 0,'PY_SellPrice': float(wrow['PY_SellPrice']) if wrow['PY_SellPrice'] else 0,'SR_Price': float(wrow['SR_Price']) if wrow['SR_Price'] else 0,'SA_Price': float(wrow['SA_Price']) if wrow['SA_Price'] else 0,'Quantity': 1})
            else:
                if wrow['Service_Product'] not in spRemovalList: #CXCPQ-82646: Modified for Scope Removal changes: 06/03/2024
                    WEPDict[wrow['Service_Product']] = [{'OfferingName' : wrow['Offering_Name'], 'ListPrice' : float(wrow['List_Price']) if wrow['List_Price'] else 0, 'CostPrice' : float(wrow['CY_CostPrice']) if wrow['CY_CostPrice'] else 0,'ExtDescription': WEPEntDict[wrow['Offering_Name']] if wrow['Offering_Name'] in WEPEntDict else '','Escalation_Price': float(wrow['Escalation_Price']) if wrow['Escalation_Price'] else 0,'PY_ListPrice': float(wrow['PY_ListPrice']) if wrow['PY_ListPrice'] else 0,'PY_SellPrice': float(wrow['PY_SellPrice']) if wrow['PY_SellPrice'] else 0,'SR_Price': float(wrow['SR_Price']) if wrow['SR_Price'] else 0,'SA_Price': float(wrow['SA_Price']) if wrow['SA_Price'] else 0,'Quantity': 1}]
        for wepproductName in spRemovalDist:#CXCPQ-82646: Added on 06/03/2024
            WEPDict[wepproductName] =  [{'Quantity': 0, 'OfferingName' : 'Scope Removed','ExtDescription':'','ListPrice':0,'CostPrice':0,'Escalation_Price':0,'PY_ListPrice': spRemovalDist[wepproductName]['PY_ListPrice'],'PY_SellPrice':spRemovalDist[wepproductName]['PY_SellPrice'],'SA_Price': 0, 'SR_Price': 0}]
        return WEPDict
    elif row['Module'] == 'Labor':
        laborDict = {}
        laborDictCombo = {}
        laborContainer = row.Product.GetContainerByName('SC_Labor_Summary_Container')
        for lRow in laborContainer.Rows:
            lPart = {'ResourceType':lRow['Resource_Type'] if lRow['Lumpsum'] == 'N' else 'Lumpsum', 'Price': float(lRow['Total_Customer_List_Price']) if lRow['Total_Customer_List_Price'] else 0, 'BlockDiscount': float(lRow['BlockDiscount']) if lRow['BlockDiscount'] else 0, 'Cost':((float(lRow['Deliverable_Hours'] if lRow['Deliverable_Hours'] else 0 )*float(lRow['BurdenRate'] if lRow['BurdenRate'] else 0 )))+(float(lRow['Contigency_Cost']) if lRow['Contigency_Cost'] else 0), 'Margin': (1-((float(lRow['Deliverable_Hours'] if lRow['Deliverable_Hours'] else 0 )*float(lRow['BurdenRate'] if lRow['BurdenRate'] else 0 ))+ float(lRow['Contigency_Cost'] if lRow['Contigency_Cost'] else 0))/float(lRow['Total_Customer_List_Price']))*100 if lRow['Total_Customer_List_Price'] and float(lRow['Total_Customer_List_Price'])>0 else 0, 'Expense':float(lRow['Other_Expenses']) if lRow['Other_Expenses'] and float(lRow['Other_Expenses']) > 0 else 0, 'Escalation_Price': float(lRow['Escalation_Price']) if lRow['Escalation_Price'] else 0, 'SA_Price': float(lRow['SA_Price']) if lRow['SA_Price'] else 0, 'SR_Price': float(lRow['SR_Price']) if lRow['SR_Price'] else 0, 'PY_ListPrice': float(lRow['PY_ListPrice']) if lRow['PY_ListPrice'] else 0, 'PY_SellPrice': float(lRow['PY_SellPrice']) if lRow['PY_SellPrice'] else 0, 'PY_Total_Expenses': float(lRow['PY_Total_Expenses']) if lRow['PY_Total_Expenses'] else 0, 'Escalation_Price_TotalExpense': float(lRow['Escalation_Price_TotalExpense']) if lRow['Escalation_Price_TotalExpense'] else 0, 'ExtDescription': '<b>Service Product:</b> ' + lRow['Related Module'] if lRow['Service_Product'] else '', 'Quantity': 1, 'Related Module': lRow['Related Module'] }
            if lRow['Service_Product']+'<*>'+lRow['Entitlement'] not in laborDictCombo: laborDictCombo[lRow['Service_Product']+'<*>'+lRow['Entitlement']] = [lPart]
            else:
                for exlPart in laborDictCombo[lRow['Service_Product']+'<*>'+lRow['Entitlement']]:
                    if exlPart['ResourceType'] == lPart['ResourceType']: #and exlPart['Related Module'] == lPart['Related Module']
                        for k in ['Price', 'Cost', 'Expense', 'Escalation_Price', 'SA_Price', 'SR_Price', 'PY_ListPrice', 'PY_SellPrice', 'PY_Total_Expenses', 'Escalation_Price_TotalExpense']: exlPart[k] += lPart[k]
                        exlPart['Margin'] = (1 - (exlPart['Cost'] / exlPart['Price'])) * 100 if exlPart['Price'] > 0 else 0; break
                else: laborDictCombo[lRow['Service_Product']+'<*>'+lRow['Entitlement']].append(lPart)
            #laborDictCombo.setdefault(lRow['Service_Product']+'<*>'+lRow['Entitlement'], []).append({'ResourceType':lRow['Resource_Type'] if lRow['Lumpsum'] == 'N' else 'Lumpsum', 'Price': lRow['Total_Customer_List_Price'], 'BlockDiscount': float(lRow['BlockDiscount']) if lRow['BlockDiscount'] else 0, 'Cost':((float(lRow['Deliverable_Hours'] if lRow['Deliverable_Hours'] else 0 )*float(lRow['BurdenRate'] if lRow['BurdenRate'] else 0 )))+(float(lRow['Contigency_Cost']) if lRow['Contigency_Cost'] else 0), 'Margin': (1-((float(lRow['Deliverable_Hours'] if lRow['Deliverable_Hours'] else 0 )*float(lRow['BurdenRate'] if lRow['BurdenRate'] else 0 ))+ float(lRow['Contigency_Cost']) if lRow['Contigency_Cost'] else 0)/float(lRow['Total_Customer_List_Price']))*100 if lRow['Total_Customer_List_Price'] and float(lRow['Total_Customer_List_Price'])>0 else 0, 'Expense':float(lRow['Other_Expenses']) if lRow['Other_Expenses'] and float(lRow['Other_Expenses']) > 0 else 0, 'Escalation_Price': float(lRow['Escalation_Price']) if lRow['Escalation_Price'] else 0, 'SA_Price': float(lRow['SA_Price']) if lRow['SA_Price'] else 0, 'SR_Price': float(lRow['SR_Price']) if lRow['SR_Price'] else 0, 'PY_ListPrice': float(lRow['PY_ListPrice']) if lRow['PY_ListPrice'] else 0, 'PY_SellPrice': float(lRow['PY_SellPrice']) if lRow['PY_SellPrice'] else 0, 'PY_Total_Expenses': float(lRow['PY_Total_Expenses']) if lRow['PY_Total_Expenses'] else 0, 'Escalation_Price_TotalExpense': float(lRow['Escalation_Price_TotalExpense']) if lRow['Escalation_Price_TotalExpense'] else 0, 'ExtDescription': '<b>Service Product:</b> ' + lRow['Related Module'] if lRow['Service_Product'] else '', 'Quantity': 1 })
        for vkey in laborDictCombo:
            vkeys = vkey.split('<*>')
            if vkeys[0] not in spRemovalList: #CXCPQ-82629: Modified for Scope Removal changes: 06/03/2024
                if vkeys[0] not in laborDict: laborDict[vkeys[0]] = {}
                laborDict[vkeys[0]][vkeys[1]] = laborDictCombo[vkey]
        for lproductName in spRemovalDist:#CXCPQ-82629: Added on 06/03/2024
            laborDict[lproductName] =  {'Scope Removed': [{'Quantity': 0, 'ResourceType' : 'Scope Removed','ExtDescription':'','Price':0,'BlockDiscount':0,'Cost':0,'Margin':0,'Expense':0,'Escalation_Price':0,'PY_ListPrice': spRemovalDist[lproductName]['PY_ListPrice'],'PY_SellPrice':spRemovalDist[lproductName]['PY_SellPrice'],'SA_Price': 0, 'PY_Total_Expenses':0,'Escalation_Price_TotalExpense': 0,'SR_Price': 0}]}
        return laborDict
    elif row['Module'] == 'Condition Based Maintenance':
        price_cum = PY_ListPrice= Escalation_Price= PY_SellPrice= SR_Price=SA_Price=0
        resDict = dict()
        if 'Condition Based Maintenance' not in spRemovalList:
            if row.Product.Attributes.GetByName("SC_Pricing_Escalation").GetValue() == "Yes":
                for type in row.Product.GetContainerByName('CBM_Pricing_Container').Rows:
                    price_cum += float(type['PY_ListPrice'])
            else:
                for type in row.Product.GetContainerByName('CBM_Pricing_Container').Rows:
                    price_cum += float(type['Annual Price'])
            for type1 in row.Product.GetContainerByName('CBM_Models_Cont').Rows:
                Escalation_Price += float(type1['Escalation_Price'] if type1['Escalation_Price'] else 0)
                PY_ListPrice += float(type1['PY_ListPrice'] if type1['PY_ListPrice'] else 0)
                PY_SellPrice += float(type1['PY_SellPrice'] if type1['PY_SellPrice'] else 0)
                SR_Price += float(type1['SR_Price'] if type1['SR_Price'] else 0)
                SA_Price += float(type1['SA_Price'] if type1['SA_Price'] else 0)
            resDict ={'CBM':'ServiceProd','Quantity': 1,"Price":price_cum,"Escalation_Price":Escalation_Price,"PY_ListPrice":PY_ListPrice,"PY_SellPrice":PY_SellPrice,"SR_Price":SR_Price,"SA_Price":SA_Price}
        else:
            resDict =	 {'CBM':'ServiceProd','Quantity': 0, 'Price' : 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist['Condition Based Maintenance']['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist['Condition Based Maintenance']['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0}
        return resDict
    elif row['Module'] == 'Local Support Standby': #added LSS Logic 10/15/2024
        price_cum = Escalation_Price = PY_SellPrice = SR_Price = SA_Price = Cost = PY_ListPrice =0
        lssDict = dict()
        if 'Local Support Standby' not in spRemovalList:
            for type1 in row.Product.GetContainerByName('SC_LSS_Models_Summary_Cont_Hidden').Rows:
                price_cum += float(type1['Hidden_List_Price'] if type1['Hidden_List_Price'] else 0)
                Escalation_Price += float(type1['Escalation_Price'] if type1['Escalation_Price'] else 0)
                PY_ListPrice += float(type1['PY_ListPrice'] if type1['PY_ListPrice'] else 0)
                PY_SellPrice += float(type1['PY_SellPrice'] if type1['PY_SellPrice'] else 0)
                SR_Price += float(type1['SR_Price'] if type1['SR_Price'] else 0)
                SA_Price += float(type1['SA_Price'] if type1['SA_Price'] else 0)
                Cost += float(type1['Hidden_Cost_Price'] if type1['Hidden_Cost_Price'] else 0)
            lssDict ={'Local Support Standby':'ServiceProd','Quantity': 1,"Price":price_cum,"Escalation_Price":Escalation_Price,"PY_ListPrice":PY_ListPrice,"PY_SellPrice":PY_SellPrice,"SR_Price":SR_Price,"SA_Price":SA_Price,"Cost":Cost}
        else:
            lssDict =	 {'Local Support Standby':'ServiceProd','Quantity': 0, 'Price' : 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist['Local Support Standby']['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist['Local Support Standby']['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0,'Cost': 0}
        return lssDict
    elif row['Module'] in ['Solution Enhancement Support Program', 'Enabled Services']:
        service = {}
        Product1 = row.Product
        prod = Product1.Attr('EnabledService_Entitlement').GetValue()
        a_flag = False
        issesp = False
        if row['Module'] == 'Solution Enhancement Support Program':
            issesp = True
            a_contract= Product1.Attr('A360Contract_SESPEnable').Values
            for i in a_contract:
                if i.IsSelected == True:
                    a_flag = True
                    break
        if Product1.Attr('OrderType_EnabledService').GetValue() == 'Renewal':
            EContainer = row.Product.GetContainerByName('ES_Asset_Summary')
            if prod not in spRemovalList:
                for erow in EContainer.Rows:
                    PY_SellPrice = float(erow['PY_SellPrice']) if erow['PY_SellPrice'].strip() != '' else 0
                    if a_flag == True: #Reset list price to o if any existing A360 Contract is selected
                        CY_List_Price = 0
                    else:
                        CY_List_Price = float(erow['Hidden_List_Price']) if erow['Hidden_List_Price'].strip() != '' else 0
                        if issesp == False:
                            CY_List_Price = CY_List_Price + ((CY_List_Price/100) * 10)
                    service[prod] = [{'ServiceProduct': prod, 'Quantity': 1, 'Price' : CY_List_Price, 'Escalation_Price' : float(erow['Escalation_Price']), 'PY_ListPrice' : float(erow['PY_ListPrice']), 'PY_SellPrice' : float(PY_SellPrice), 'SR_Price' : float(erow['SR_Price']), 'SA_Price' : float(erow['SA_Price'])}]
            for esproductName in spRemovalDist:
                if service:
                    service[prod].append({'ServiceProduct': esproductName, 'Quantity': 0, 'Price' : 0, 'Escalation_Price' : 0, 'PY_ListPrice' : float(spRemovalDist[esproductName]['PY_ListPrice']), 'PY_SellPrice' : float(spRemovalDist[esproductName]['PY_SellPrice']), 'SR_Price' : 0, 'SA_Price' : 0})
                else:
                    service[esproductName] = [{'ServiceProduct': esproductName, 'Quantity': 0, 'Price' : 0, 'Escalation_Price' : 0, 'PY_ListPrice' : float(spRemovalDist[esproductName]['PY_ListPrice']), 'PY_SellPrice' : float(spRemovalDist[esproductName]['PY_SellPrice']), 'SR_Price' : 0, 'SA_Price' : 0}]
        else:
            if row['Type'] == 'Renewal':
                service[prod] = []
                EContainer = row.Product.GetContainerByName('ES_Asset_Summary').Rows[0]
                totalcont = Product1.GetContainerByName('Asset_details_ServiceProd').TotalRow.Columns['List Price'].Value
                if a_flag == True: #Reset list price to o if any existing A360 Contract is selected
                    totalcont = 0
                totalcont = float(totalcont)
                if issesp == False:
                    totalcont = totalcont + ((totalcont/100) * 10)
                matrikon = Product1.Attr('Matrix License').GetValue()
                service[prod].append({'ServiceProduct': prod, 'Quantity': 1, 'Price' : float(totalcont), 'Escalation_Price': 0, 'PY_ListPrice': 0, 'PY_SellPrice': 0, 'SA_Price': float(EContainer['SA_Price']), 'SR_Price': float(EContainer['SR_Price'])})
                service[prod].append({'ServiceProduct': 'Matrikon License', 'Quantity': 1, 'Price' : matrikon, 'Escalation_Price': 0, 'PY_ListPrice': 0, 'PY_SellPrice': 0, 'SA_Price': matrikon, 'SR_Price': 0})
            else:
                service[prod] = []
                totalcont = Product1.GetContainerByName('Asset_details_ServiceProd').TotalRow.Columns['List Price'].Value
                if a_flag == True: #Reset list price to o if any existing A360 Contract is selected
                    totalcont = 0
                totalcont = float(totalcont)
                if issesp == False:
                    totalcont = totalcont + ((totalcont/100) * 10)
                matrikon = Product1.Attr('Matrix License').GetValue()
                service[prod].append({'ServiceProduct': prod, 'Quantity': 1, 'Price' : float(totalcont), 'Escalation_Price': 0, 'PY_ListPrice': 0, 'PY_SellPrice': 0, 'SA_Price': 0, 'SR_Price': 0})
                service[prod].append({'ServiceProduct': 'Matrikon License', 'Quantity': 1, 'Price' : matrikon, 'Escalation_Price': 0, 'PY_ListPrice': 0, 'PY_SellPrice': 0, 'SA_Price': 0, 'SR_Price': 0})                
        return service
    elif row['Module'] == 'Generic Module':
        ContainerName = 'SC_GN_AT_Models_Cont_Hidden'
        LP_ColumnName = 'List_Price'
        CP_ColumnName = 'CY_CostPrice' if row['Type'] == 'Renewal' else 'Cost_Price'
        CyDict = {}
        CyContainer = row.Product.GetContainerByName(ContainerName)
        for crow in CyContainer.Rows:
            if crow['Service_Product'] in CyDict:
                CyDict[crow['Service_Product']]['Price'] = float(CyDict[crow['Service_Product']]['Price']) + float(crow[LP_ColumnName] if crow[LP_ColumnName] else 0)
                CyDict[crow['Service_Product']]['Cost'] = float(CyDict[crow['Service_Product']]['Cost']) + float(crow[CP_ColumnName] if crow[CP_ColumnName] else 0)
                CyDict[crow['Service_Product']]['Escalation_Price'] = float(CyDict[crow['Service_Product']]['Escalation_Price']) + float(crow['Escalation_Price'] if crow['Escalation_Price'] else 0)
                CyDict[crow['Service_Product']]['SR_Price'] = float(CyDict[crow['Service_Product']]['SR_Price']) + float(crow['SR_Price'] if crow['SR_Price'] else 0)
                CyDict[crow['Service_Product']]['SA_Price'] = float(CyDict[crow['Service_Product']]['SA_Price']) + float(crow['SA_Price'] if crow['SA_Price'] else 0)
                CyDict[crow['Service_Product']]['PY_ListPrice'] = float(CyDict[crow['Service_Product']]['PY_ListPrice']) + float(crow['PY_ListPrice'] if crow['PY_ListPrice'] else 0)
                CyDict[crow['Service_Product']]['PY_SellPrice'] = float(CyDict[crow['Service_Product']]['PY_SellPrice']) + float(crow['PY_SellPrice'] if crow['PY_SellPrice'] else 0)
            else:
                if crow['Service_Product'] not in spRemovalList:
                    CyDict[crow['Service_Product']] = {'Price': float(crow[LP_ColumnName]) if crow[LP_ColumnName] else 0, 'Cost': float(crow[CP_ColumnName]) if crow[CP_ColumnName] else 0, 'Escalation_Price': float(crow['Escalation_Price']) if crow['Escalation_Price'] else 0, 'SR_Price': float(crow['SR_Price']) if crow['SR_Price'] else 0, 'SA_Price': float(crow['SA_Price']) if crow['SA_Price'] else 0, 'PY_ListPrice': float(crow['PY_ListPrice']) if crow['PY_ListPrice'] else 0, 'PY_SellPrice': float(crow['PY_SellPrice']) if crow['PY_SellPrice'] else 0, 'Quantity': 1}
        for cyproductName in spRemovalDist:
            CyDict[cyproductName] =  {'Quantity': 0, 'Price' : 0, 'Cost': 0, 'Escalation_Price': 0, 'PY_ListPrice': float(spRemovalDist[cyproductName]['PY_ListPrice']), 'PY_SellPrice': float(spRemovalDist[cyproductName]['PY_SellPrice']), 'SA_Price': 0, 'SR_Price': 0}
        if CyDict:
            scDict[row['Product_Name']] = CyDict
            productlist.append({'ProductName' : row['Product_Name'], 'UniqueID': row.UniqueIdentifier, 'PartNumber' : row.Product.PartNumber})
    return None

#CXCPQ-82924: Added CheckServiceProductInContainer
def CheckServiceProductInContainer(Quote, Product, p_container_name,p_cont_col_name, p_service_product):
    pCont = Product.GetContainerByName(p_container_name)
    if pCont is not None and pCont.Rows.Count>0:
        for prow in pCont.Rows:
            if (prow[p_cont_col_name]==p_service_product) or (prow[p_cont_col_name]=="Service Contract Management" and p_service_product =="A360 Contract Management"): #Need to check column name based on module. 
                return True
    return False