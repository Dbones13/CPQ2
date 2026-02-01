validModelCont = Product.GetContainerByName('HWOS_Model Scope_3party')
t = Product.GetContainerByName('HWOS_Entitlement')
for i in validModelCont.Rows:
    if i['Entitlement'] != '' and i['Unit List Price'] != '' and i['List Price'] != '' and i['Quantity'] != '' and i['3rd Party Model'] != '' and i['Description'] != '':
        ents = []
        for j in t.Rows:
            ents.append(j['Entitlement'])
        if i['Entitlement'] not in ents:
            row = t.AddNewRow(False)
            row['Entitlement'] = i['Entitlement']
ScriptExecutor.Execute('GS_delete_ThirdPartyModels')