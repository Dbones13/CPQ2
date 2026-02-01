if Product.Attr('SC_Product_Type').GetValue() == "Renewal":
    Exchange_Rate = float(Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content) if Quote.GetCustomField('SC_CF_PRVYR_EXCH_RATE').Content else 1
    import GS_GetPriceFromCPS
    import GS_CostAPI_Module

    def getFloat(Var):
        if Var:
            return float(Var)
        return 0

    #Get host name from environment
    def getHost():
        hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
        if hostquery is not None:
            return hostquery.HostName
        return ''

    #Call API to fetch cost and assign to Quote Item fields
    def fn_getCost(host,p_Material,p_fme,p_plant):
        #Trace.Write('In CC_GetCost_Plant_Change fn_getCost')
        req_payload=GS_CostAPI_Module.gen_Item_PayLoad(Quote,p_Material,p_fme,p_plant)
        accessTkn = GS_CostAPI_Module.getAccessToken(host)
        CostAPIResp_Json = GS_CostAPI_Module.getCost(host, accessTkn,req_payload)
        #Trace.Write('API response:'+str(CostAPIResp_Json))
        return CostAPIResp_Json

    def fetchCost(model,plantCode):
        responseCost = "0"
        try:
            _responseCost = fn_getCost(host,model,'',plantCode)
            if _responseCost is not None and _responseCost['vcMaterialCostResponse'] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse'] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0] is not None and _responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0]['totalCost'] is not None:
                responseCost = str(_responseCost['vcMaterialCostResponse']['vcCostResponse']["item"][0]['totalCost'])
        except:
            responseCost = '0'
        return responseCost

    def AssignPriceCost(partsList,cont,entitlementCont):
        flag_20 = False
        if cont.Name in ('SC_WEP_Models_Scope_IFS','SC_WEP_Models_Scope_Halo'):
            for entRow in entitlementCont.Rows:
                if entRow["Entitlement"] == "Software Updates" or entRow["Entitlement"] == "Software Upgrades":
                    if entRow.IsSelected == True:
                        flag_20 = True
                        break
        priceDict = GS_GetPriceFromCPS.getPrice(Quote,{},partsList,TagParserQuote,Session)
        for row in cont.Rows:
            if priceDict.get(row["Model"],"0") not in ("0.00","0",""):
                row["Unit_Price"] = priceDict[row["Model"]]
                cost = fetchCost(row["Model"],costQuery.Plant_Code) if costQuery is not None else "0"
                                                  
                                                              
                     
                row["Unit_Cost"] = cost if cost != "0" else str(float(row["Unit_Price"])/2)
            else:
                row["Unit_Price"] = '0'
                row["Unit_Cost"] = '0'
            if flag_20 == True:
                row["CY_UnitPrice"] = str(float(float(row["Unit_Price"])*20/100))
                row["Hidden_UnitPrice"] = str(float(float(row["Unit_Price"])*20/100))
                row["CY_UnitCost"] = str(float(float(row["Unit_Cost"])*20/100))
                row["Hidden_UnitCost"] = str(float(float(row["Unit_Cost"])*20/100))
            else:
                row["CY_UnitPrice"] = row["Hidden_UnitPrice"] = row["Unit_Price"]
                row["CY_UnitCost"] = row["Hidden_UnitCost"] = row["Unit_Cost"]
            row.Calculate()

    host=getHost()
    salesOrg = Quote.GetCustomField('Sales Area').Content
    costQuery = SqlHelper.GetFirst("select Plant_Code from SC_Plant_SalesOrg_Mapping where Sales_Org='{}'".format(salesOrg))

    ###### Code added for HIF Block #######
    Invalid_cont_HIF = Product.GetContainerByName("SC_WEP_Invalid_Models_HIF")
    Invalid_cont_HIF.Rows.Clear()
    Model_cont_HIF = Product.GetContainerByName("SC_WEP_Models_Scope_HIF")
    if Model_cont_HIF.Rows.Count:
        for row in Model_cont_HIF.Rows:
            row['PY_Quantity'] = row['Hidden_Quantity']
            row['PY_UnitPrice'] = str(float(row['Hidden_UnitPrice']) * Exchange_Rate) if row['Hidden_UnitPrice'] else '0'
            row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['PY_UnitCost'] = str(float(row['Hidden_UnitCost']) * Exchange_Rate) if row['Hidden_UnitCost'] else '0'
            row['PY_CostPrice'] = str(float(row['Hidden_CostPrice']) * Exchange_Rate) if row['Hidden_CostPrice'] else '0'
            row['CY_Quantity'] = row['Hidden_Quantity']
            row['BackupRenewalQuantity'] = row['Hidden_Quantity']
            row.Calculate()
        Model_cont_HIF.Calculate()

    ###### Code added for IFS Block #######
    Invalid_cont_IFS = Product.GetContainerByName("SC_WEP_Invalid_Models_IFS")
    Invalid_cont_IFS.Rows.Clear()
    Model_cont_IFS = Product.GetContainerByName("SC_WEP_Models_Scope_IFS")
    Entitlement_cont_IFS = Product.GetContainerByName('SC_WEP_Entitlement_IFS')
    ifsList = []
    if Model_cont_IFS.Rows.Count:
        for row in Model_cont_IFS.Rows:
            row['PY_Quantity'] = row['Hidden_Quantity']
            row['PY_UnitPrice'] = str(float(row['Hidden_UnitPrice']) * Exchange_Rate) if row['Hidden_UnitPrice'] else '0'
            row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['PY_UnitCost'] = str(float(row['Hidden_UnitCost']) * Exchange_Rate) if row['Hidden_UnitCost'] else '0'
            row['PY_CostPrice'] = str(float(row['Hidden_CostPrice']) * Exchange_Rate) if row['Hidden_CostPrice'] else '0'
            row['CY_Quantity'] = row['Hidden_Quantity']
            row['BackupRenewalQuantity'] = row['Hidden_Quantity']
            row['Product_Type'] = "Renewal"
            row.Calculate()
            ifsList.append(row['Model'])
        AssignPriceCost(ifsList,Model_cont_IFS,Entitlement_cont_IFS)
        Model_cont_IFS.Calculate()

    ###### Code added for HALO Block #######
    Invalid_cont_HALO = Product.GetContainerByName("SC_WEP_Invalid_Models_Halo")
    Invalid_cont_HALO.Rows.Clear()
    Model_cont_HALO = Product.GetContainerByName("SC_WEP_Models_Scope_Halo")
    Entitlement_cont_HALO = Product.GetContainerByName('SC_WEP_Entitlement_Halo')
    haloList = []
    if Model_cont_HALO.Rows.Count:
        for row in Model_cont_HALO.Rows:
            row['PY_Quantity'] = row['Hidden_Quantity']
            row['PY_UnitPrice'] = str(float(row['Hidden_UnitPrice']) * Exchange_Rate) if row['Hidden_UnitPrice'] else '0'
            row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['PY_UnitCost'] = str(float(row['Hidden_UnitCost']) * Exchange_Rate) if row['Hidden_UnitCost'] else '0'
            row['PY_CostPrice'] = str(float(row['Hidden_CostPrice']) * Exchange_Rate) if row['Hidden_CostPrice'] else '0'
            row['CY_Quantity'] = row['Hidden_Quantity']
            row['BackupRenewalQuantity'] = row['Hidden_Quantity']
            row['Product_Type'] = "Renewal"
            row.Calculate()
            haloList.append(row['Model'])
        AssignPriceCost(haloList,Model_cont_HALO,Entitlement_cont_HALO)
        Model_cont_HALO.Calculate()

    ###### Code added for TNA Block #######
    Invalid_cont_TNA = Product.GetContainerByName("SC_WEP_Invalid_Models_TNA")
    Invalid_cont_TNA.Rows.Clear()
    Model_cont_TNA = Product.GetContainerByName("SC_WEP_Models_Scope_TNA")
    Entitlement_cont_TNA = Product.GetContainerByName('SC_WEP_Entitlement_TNA')
    System_sel_cont_TNA = Product.GetContainerByName('SC_WEP_System_Selection_TNA')
    tnaList = []
    if Model_cont_TNA.Rows.Count:
        for row in Model_cont_TNA.Rows:
            row['PY_Quantity'] = row['Hidden_Quantity']
            row['PY_UnitPrice'] = str(float(row['Hidden_UnitPrice']) * Exchange_Rate) if row['Hidden_UnitPrice'] else '0'
            row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['PY_UnitCost'] = str(float(row['Hidden_UnitCost']) * Exchange_Rate) if row['Hidden_UnitCost'] else '0'
            row['PY_CostPrice'] = str(float(row['Hidden_CostPrice']) * Exchange_Rate) if row['Hidden_CostPrice'] else '0'
            row['CY_Quantity'] = row['Hidden_Quantity']
            row['BackupRenewalQuantity'] = row['Hidden_Quantity']
            row['Product_Type'] = "Renewal"
            row.Calculate()
            tnaList.append(row['Model'])
        AssignPriceCost(tnaList,Model_cont_TNA,Entitlement_cont_TNA)
        Model_cont_TNA.Calculate()

    if System_sel_cont_TNA.Rows.Count:
        for row in System_sel_cont_TNA.Rows:
            row["PY_UserCount"] = row["Hidden_UserCount"]
            row["PY_UserPrice"] = str(float(row['Hidden_UserPrice']) * Exchange_Rate) if row['Hidden_UserPrice'] else '0'
            row["PY_SystemPrice"] = str(float(row['Hidden_SystemPrice']) * Exchange_Rate) if row['Hidden_SystemPrice'] else '0'
            row["PY_UserCost"] = str(float(row['Hidden_UserCost']) * Exchange_Rate) if row['Hidden_UserCost'] else '0'
            row["PY_SystemCost"] = str(float(row['Hidden_SystemCost']) * Exchange_Rate) if row['Hidden_SystemCost'] else '0'
            if row["CY_UserCount"] == '':
                row["CY_UserCount"] = '0'
            if row["PY_UserCount"] == '':
                row["PY_UserCount"] = '0'
            if int(row["CY_UserCount"]) > int(row["PY_UserCount"]):
                row['SA_Price'] = str((eval(row["CY_UserCount"])-eval(row["PY_UserCount"]))*eval(row["CY_UserPrice"]))
                row["SR_Price"] = '0'
            elif int(row["CY_UserCount"]) < int(row["PY_UserCount"]):
                row['SR_Price'] = str((eval(row["CY_UserCount"])-eval(row["PY_UserCount"]))*eval(row["PY_UserPrice"]))
                row["SA_Price"] = '0'
            else:
                row["SA_Price"] = '0'
                row["SR_Price"] = '0'
            row.Calculate()
        System_sel_cont_TNA.Calculate()

    ###### Code added for Training Block #######
    Invalid_cont_Training = Product.GetContainerByName("SC_WEP_Invalid_Models_Training")
    Invalid_cont_Training.Rows.Clear()
    Model_cont_Training = Product.GetContainerByName("SC_WEP_Models_Scope_Training")
    Entitlement_cont_Training = Product.GetContainerByName('SC_WEP_Entitlement_Training')
    Model_cont_conf_train = Product.GetContainerByName("SC_WEP_Configurable_Models_Training")
    trainingList = []
    if Model_cont_Training.Rows.Count:
        for row in Model_cont_Training.Rows:
            row['PY_Quantity'] = row['Hidden_Quantity']
            row['PY_UnitPrice'] = str(float(row['Hidden_UnitPrice']) * Exchange_Rate) if row['Hidden_UnitPrice'] else '0'
            row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['PY_UnitCost'] = str(float(row['Hidden_UnitCost']) * Exchange_Rate) if row['Hidden_UnitCost'] else '0'
            row['PY_CostPrice'] = str(float(row['Hidden_CostPrice']) * Exchange_Rate) if row['Hidden_CostPrice'] else '0'
            row['CY_Quantity'] = row['Hidden_Quantity']
            row['BackupRenewalQuantity'] = row['Hidden_Quantity']
            row['Product_Type'] = "Renewal"
            row.Calculate()
            trainingList.append(row['Model'])
        AssignPriceCost(trainingList,Model_cont_Training,Entitlement_cont_Training)
        Model_cont_Training.Calculate()

    if Model_cont_conf_train.Rows.Count:
        for row in Model_cont_conf_train.Rows:
            row['PY_Quantity'] = row['Hidden_Quantity']
            row['PY_UnitPrice'] = str(float(row['Hidden_UnitPrice']) * Exchange_Rate) if row['Hidden_UnitPrice'] else '0'
            row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['PY_UnitCost'] = str(float(row['Hidden_UnitCost']) * Exchange_Rate) if row['Hidden_UnitCost'] else '0'
            row['PY_CostPrice'] = str(float(row['Hidden_CostPrice']) * Exchange_Rate) if row['Hidden_CostPrice'] else '0'
            row['CY_Quantity'] = '1'
            row.Calculate()
        Model_cont_conf_train.Calculate()

    ###### Code added for O&M Block #######
    Sub_Cont = Product.GetContainerByName("SC_WEP_Subscription_Price_OM")
    Add_Cont = Product.GetContainerByName("SC_WEP_Add_On_Fees_OM")

    if Sub_Cont.Rows.Count:
        for row in Sub_Cont.Rows:
            row['PY_UserCount'] = row['Hidden_UserCount']
            row['PY_SubscriptionPrice'] = str(float(row['Hidden_SubscriptionPrice']) * Exchange_Rate) if row['Hidden_SubscriptionPrice'] else '0'
            row.Calculate()
        Sub_Cont.Calculate()
    if Add_Cont.Rows.Count:
        for row in Add_Cont.Rows:
            row['PY_SubscriptionPrice_USD'] = row['Hidden_SubscriptionPrice_USD']
            row['PY_SubscriptionPrice'] = str(float(row['Hidden_Subscription_Price']) * Exchange_Rate) if row['Hidden_Subscription_Price'] else '0'
            row.Calculate()
        Add_Cont.Calculate()

    ###### Code added for OCP Block #######
    Product.Attr('SC_WEP_Current_Score_OCP_PY').SelectValue(Product.Attr('SC_WEP_Current_Score_OCP').GetValue())
    Product.Attr('SC_WEP_No_of_Users_OCP_PY').AssignValue(Product.Attr('SC_WEP_No_of_Users_OCP').GetValue())
    Product.Attr('SC_WEP_Effort_Loading_OCP_PY').AssignValue(Product.Attr('SC_WEP_Effort_Loading_OCP').GetValue())
    Product.Attr('SC_WEP_Skill_Assessment_Level_OCP_PY').AssignValue(Product.Attr('SC_WEP_Skill_Assessment_Level_OCP').GetValue())
    SC_WEP_Courses_OCP = Product.GetContainerByName("SC_WEP_Courses_OCP")
    if SC_WEP_Courses_OCP.Rows.Count:
        for row in SC_WEP_Courses_OCP.Rows:
            row['PY_UnitPrice'] = str(float(row['Hidden_UnitPrice']) * Exchange_Rate) if row['Hidden_UnitPrice'] else '0'
            row['PY_ListPrice'] = str(float(row['Hidden_ListPrice']) * Exchange_Rate) if row['Hidden_ListPrice'] else '0'
            row['PY_EffortLoading'] = str(float(row['Hidden_EffortLoading']) * Exchange_Rate) if row['Hidden_EffortLoading'] else '0'
            row.Calculate()
        SC_WEP_Courses_OCP.Calculate()
    SC_WEP_Conclusion_OCP = Product.GetContainerByName("SC_WEP_Conclusion_OCP")
    if SC_WEP_Conclusion_OCP.Rows.Count:
        for row in SC_WEP_Conclusion_OCP.Rows:
            row['PY_Value'] = str(float(row['Hidden_Value']) * Exchange_Rate) if row['Hidden_Value'] else '0'
            row.Calculate()
        SC_WEP_Conclusion_OCP.Calculate()
    Product.Attr('SC_WEP_Current_Score_OCP').SelectValue("1")

    Product.Attr('SC_ScopeRemoval').AssignValue('')
    Product.Attr('SC_ScopeRemoval_Training').AssignValue('')
    #######  Making Renewal Check as 1 #######
    Product.Attr('SC_Renewal_check').AssignValue('1')