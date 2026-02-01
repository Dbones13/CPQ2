list1=[]
list2=[]
discount = 0
comparision_cont = Product.GetContainerByName("ComparisonSummary")
if arg.NameOfCurrentTab == 'Scope Summary':
    entitlement_readonly_cont = Product.GetContainerByName('CBM_Service_Products&Entitlements_Cont')
    entitement_editable_cont = Product.GetContainerByName('CBM_Entitlements_Cont')
    entitlement_readonly_cont.Rows.Clear()
    for ent in entitement_editable_cont.Rows:
        readonly_cont_row = entitlement_readonly_cont.AddNewRow()
        readonly_cont_row['Service Product'] = 'Condition Based Maintenance'
        readonly_cont_row['Entitlement'] = ent['Entitlement']
        if ent.IsSelected == True:
            readonly_cont_row['Type'] = 'Mandatory'
        elif ent.IsSelected == True :
            readonly_cont_row['Type'] = 'Optional'
    #Update the model readonly container
    if Product.Attributes.GetByName("SC_Product_Type").GetValue() == "New":
        model_readonly_container = Product.GetContainerByName('CBM_Models_Cont')
        asset_editable_container = Product.GetContainerByName('CBM_Pricing_Container')
        model_readonly_container.Rows.Clear()
        for asset in asset_editable_container.Rows:
            if asset['Product Family'] not in list1:
                model_row = model_readonly_container.AddNewRow()
                model_row['Service Product'] = 'Condition Based Maintenance'
                model_row['Product Family'] = asset.Product.Attr('CBM_PRODUCT_FAMILY').GetValue()
                model_row['List Price'] = asset['Annual Price']
                model_row['SR_Price'] = "0"
                model_row['SA_Price'] = asset['Annual Price']
                model_row['Escalation_Price'] = asset['Annual Price']
                list1.append(asset['Product Family'])
            else:
                for i in model_readonly_container.Rows:
                    if i['Product Family'] == asset.Product.Attr('CBM_PRODUCT_FAMILY').GetValue():
                        i['List Price'] = str(float(i['List Price']) + float(asset['Annual Price']))
            model_readonly_container.Calculate()
    if Product.Attributes.GetByName("SC_Product_Type").GetValue() == "Renewal":
        cont = Product.GetContainerByName("CBM_Pricing_Container")
        cont1 = Product.GetContainerByName("CBM_Models_Cont")
        cont1.Rows.Clear()
        for row in cont.Rows:
            row['CY_Count_Backup'] = row['CY_Count']
            if row['CY_ProductFamily'] != "":
                if row['CY_ProductFamily'] not in list2:
                    row1 = cont1.AddNewRow()
                    row1['Service Product'] = 'Condition Based Maintenance'
                    row1['Product Family'] = row['CY_ProductFamily']
                    row1['PY_LevelOffering'] = row['PY_LevelOffering']
                    row1['PY_PMCBM'] = row['PY_PMCBM']
                    row1['PY_ListPrice'] = row['PY_ListPrice']
                    row1['CY_LevelOffering'] = row['CY_LevelOffering']
                    row1['CY_PMCBM'] = row['CY_PMCBM']
                    row1['CY_ListPrice'] = row['CY_ListPrice']
                    if row1['PY_ListPrice'] == "":
                        row1['PY_ListPrice'] = str(0)
                        Trace.Write(row1['PY_ListPrice'])
                        Trace.Write(row1['CY_ListPrice'])
                    if float(row1['PY_ListPrice']) > float(row1['CY_ListPrice']):
                        row1['Comments'] = "Scope Reduction"
                    elif float(row1['PY_ListPrice']) < float(row1['CY_ListPrice']):
                        row1['Comments'] = "Scope Addition"
                    elif float(row1['PY_ListPrice']) == float(row1['CY_ListPrice']):
                        row1['Comments'] = "No Scope Change"
                    if row['CY_ProductFamily'] != "":
                        list2.append(row['CY_ProductFamily'])
                else:
                    for i in cont1.Rows:
                        if i['Product Family'] == row.Product.Attr('CBM_PRODUCT_FAMILY').GetValue():
                            i['CY_ListPrice'] = str(float(i['CY_ListPrice']) + float(row['CY_ListPrice']))
            for row1 in cont1.Rows:
                if float(row1['PY_ListPrice']) > float(row1['CY_ListPrice']):
                    row1['Comments'] = "Scope Reduction"
                    row1['SR_Price'] = str(float(row1['CY_ListPrice']) - float(row1['PY_ListPrice']))
                    row1['SA_Price'] = '0'
                elif float(row1['PY_ListPrice']) < float(row1['CY_ListPrice']):
                    row1['Comments'] = "Scope Addition"
                    row1['SA_Price'] = str(float(row1['CY_ListPrice']) - float(row1['PY_ListPrice']))
                    row1['SR_Price'] = '0'
                elif float(row1['PY_ListPrice']) == float(row1['CY_ListPrice']):
                    row1['Comments'] = "No Scope Change"
                if row1['PY_ListPrice'] == "":
                    row1['PY_ListPrice'] = 0
                #row1['Escalation_Price'] = str(float(row1['PY_ListPrice']) - float(row1['SR_Price']))
                cont1.Calculate()

#Product Familly Matching
dicta = {}
cont = Product.GetContainerByName("CBM_Pricing_Container")
for row in cont.Rows:
    if row['PY_ProductFamily'] != "":
        PMCBM = row['PY_PMCBM']
        plevel = row['PY_LevelOffering']
    if row['PY_ProductFamily'] not in dicta.keys():
        if row['PY_ProductFamily'] != "":
            pf = row['PY_ProductFamily']
            val = row['PY_ListPrice']
            dicta[pf] = val
    else:
        dicta[row['PY_ProductFamily']] = float(dicta.get(row['PY_ProductFamily'])) + float(row['PY_ListPrice'])
        #Trace.Write()

Trace.Write(str(dicta))

lista = []
cont1 = Product.GetContainerByName("CBM_Models_Cont")
for row in cont1.Rows:
    if row['Product Family'] in dicta.keys():
        row['PY_ListPrice'] = str(float(dicta.get(row['Product Family'])))
        row['PY_LevelOffering'] = plevel
        row['PY_PMCBM'] = PMCBM
    else:
        row['PY_ListPrice'] = str(0)
        row['PY_LevelOffering'] = str(0)
        row['PY_PMCBM'] = str(0)
    if row['Product Family'] != "":
        lista.append(row['Product Family'])

Trace.Write(str(lista))
cont1.Calculate
for i in dicta.keys():
    if i not in lista:
        rown = cont1.AddNewRow()
        rown['Service Product'] = 'Condition Based Maintenance'
        rown['Product Family'] = i
        rown['PY_LevelOffering'] = plevel
        rown['PY_PMCBM'] = PMCBM
        rown['PY_ListPrice'] = str((dicta.get(i)))
cont1.Calculate

for row1 in cont1.Rows:
    PYLP = row1['PY_ListPrice']
    CYLP = row1['CY_ListPrice']
    if row1['PY_ListPrice'] == "":
        PYLP = 0
    if row1['CY_ListPrice'] == "":
        CYLP = 0
    PYLP = float(PYLP)
    CYLP = float(PYLP) if Product.Attributes.GetByName("SC_Pricing_Escalation").GetValue() == "Yes" else float(CYLP)
    if PYLP > CYLP:
        row1['SR_Price'] = str(CYLP - PYLP)
        row1['SA_Price'] = '0'
        row1['Comments'] = "Scope Reduction"
    elif PYLP < CYLP:
        row1['SA_Price'] = str(CYLP - PYLP)
        row1['SR_Price'] = '0'
        row1['Comments'] = "Scope Addition"
    elif PYLP == CYLP:
        row1['Comments'] = "No Scope Change"
        row1['SA_Price'] = '0'
        row1['SR_Price'] = '0'
    if Product.Attributes.GetByName("SC_Pricing_Escalation").GetValue() == "Yes":
        row1['Escalation_Price'] = str(PYLP + float(row1['SR_Price']))#changed to correct the scope reduction sum 16/08/2024
    elif Product.Attributes.GetByName("SC_Pricing_Escalation").GetValue() == "No":
        row1['Escalation_Price'] = "0"
    cont1.Calculate()

for row in comparision_cont.Rows:
    if (row['PY_Sell_Price_SFDC']) == '':
        row['PY_Sell_Price_SFDC'] = '0'
    if (row['PY_List_Price_SFDC']) == '':
        row['PY_List_Price_SFDC'] = '0'
    if (row['PY_List_Price_SFDC']):
        discount = (float(row['PY_List_Price_SFDC']) - float(row['PY_Sell_Price_SFDC']))/float(row['PY_List_Price_SFDC'])

for row in cont1.Rows:
    row['LY_Discount'] = str(discount)
    if row['PY_ListPrice'] ==  "":
        row['PY_ListPrice'] = "0"
    row['PY_SellPrice'] = str(float(row['PY_ListPrice']) - (float(row['PY_ListPrice']) * discount))
cont1.Calculate()