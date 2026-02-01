tabs = [tab.Name for tab in Product.Tabs if tab.IsSelected]
if 'Scope Summary' in tabs:
    scope_summary = Product.GetContainerByName("SC_WEP_Offering_ServiceProduct")
    scope_summary.Rows.Clear()
    scope_summary_hidden = Product.GetContainerByName("SC_WEP_Offering_ServiceProduct_Hidden")
    scope_summary_hidden.Rows.Clear()

    HIF_valid = Product.GetContainerByName('SC_WEP_Models_Scope_HIF')
    IFS_valid = Product.GetContainerByName('SC_WEP_Models_Scope_IFS')
    Halo_valid = Product.GetContainerByName('SC_WEP_Models_Scope_Halo')
    Training_valid = Product.GetContainerByName('SC_WEP_Models_Scope_Training')
    TNA_valid = Product.GetContainerByName('SC_WEP_Models_Scope_TNA')
    OM_valid = Product.GetContainerByName('SC_WEP_Models_Scope_OM')
    OCP_valid = Product.GetContainerByName('SC_WEP_Models_Scope_OCP')
    Configurable_valid = Product.GetContainerByName('SC_WEP_Configurable_Models_Training')
    Sys_Sel = Product.GetContainerByName('SC_WEP_System_Selection_TNA')
    Subscription_OM = Product.GetContainerByName('SC_WEP_Subscription_Price_OM')
    Add_on_Fees_OM = Product.GetContainerByName('SC_WEP_Add_On_Fees_OM')
    Conclusion_OCP = Product.GetContainerByName('SC_WEP_Conclusion_OCP')

    if Product.Attr('SC_Product_Type').GetValue() == "New":

        hif_p = 0
        ifs_p = 0
        halo_p = 0
        training_p = 0
        tna_p = 0
        om_p = 0
        ocp_p = 0
        hif_c = 0
        ifs_c = 0
        halo_c = 0
        training_c = 0
        tna_c = 0

        if HIF_valid.Rows.Count:
            for row in HIF_valid.Rows:
                if row["Quantity"] != "" and row["Quantity"] != '0':
                    if row["List_Price"] != "":
                        hif_p += float(str(row['List_Price']))
                    if row["Cost_Price"] != "":
                        hif_c += float(str(row['Cost_Price']))
        if IFS_valid.Rows.Count:
            for row in IFS_valid.Rows:
                if row["Quantity"] != "" and row["Quantity"] != '0':
                    if row["List_Price"] != "":
                        ifs_p += float(str(row['List_Price']))
                    if row["Cost_Price"] != "":
                        ifs_c += float(str(row['Cost_Price']))
        if Halo_valid.Rows.Count:
            for row in Halo_valid.Rows:
                if row["Quantity"] != "" and row["Quantity"] != '0':
                    if row["List_Price"] != "":
                        halo_p += float(str(row['List_Price']))
                    if row["Cost_Price"] != "":
                        halo_c += float(str(row['Cost_Price']))
        if Training_valid.Rows.Count:
            for row in Training_valid.Rows:
                if row["Quantity"] != "" and row["Quantity"] != '0':
                    if row["List_Price"] != "":
                        training_p += float(str(row['List_Price']))
                    if row["Cost_Price"] != "":
                        training_c += float(str(row['Cost_Price']))
        if Configurable_valid.Rows.Count:
            for row in Configurable_valid.Rows:
                if row["Quantity"] != "" and row["Quantity"] != '0':
                    if row["List_Price"] != "":
                        training_p += float(str(row['List_Price']))
                    if row["Cost_Price"] != "":
                        training_c += float(str(row['Cost_Price']))
        if TNA_valid.Rows.Count:
            for row in TNA_valid.Rows:
                if row["Quantity"] != "" and row["Quantity"] != '0':
                    if row["List_Price"] != "":
                        tna_p += float(str(row['List_Price']))
                    if row["Cost_Price"] != "":
                        tna_c += float(str(row['Cost_Price']))
        if Sys_Sel.Rows.Count:
            for row in Sys_Sel.Rows:
                if row["User_Count"] != "" and row["User_Count"] != '0':
                    if row["Per_system_Price"] != "":
                        tna_p += float(str(row['Per_system_Price']))
                    if row["Per_system_Cost"] != "":
                        tna_c += float(str(row['Per_system_Cost']))
        if Subscription_OM.Rows.Count:
            for row in Subscription_OM.Rows:
                if row["User_Count"] != "" and row["User_Count"] != '0':
                    if row["Subscription_Price"] != "":
                        om_p += float(str(row['Subscription_Price']))
        if Add_on_Fees_OM.Rows.Count:
            for row in Add_on_Fees_OM.Rows:
                if row["Subscription_Price_USD"] != "" and row["Subscription_Price_USD"] != '0':
                    if row["Subscription_Price"] != "":
                        om_p += float(str(row['Subscription_Price']))
        if Conclusion_OCP.Rows.Count:
            for row in Conclusion_OCP.Rows:
                if row["Value"] != "" and row["Value"] != '0':
                    ocp_p += float(str(row['Value']))


        if hif_p != 0 or hif_c != 0:
            hif_row = scope_summary.AddNewRow(False)
            hif_row["Offering_Name"] = "Honeywell Integrated Field App"
            hif_row["Service_Product"] = "Workforce Excellence Program"
            hif_row["List_Price"] = str(hif_p)
            hif_row["Cost_Price"] = str(hif_c)
        if ifs_p != 0 or ifs_c != 0:
            ifs_row = scope_summary.AddNewRow(False)
            ifs_row["Offering_Name"] = "Immersive Field Simulator"
            ifs_row["Service_Product"] = "Workforce Excellence Program"
            ifs_row["List_Price"] = str(ifs_p)
            ifs_row["Cost_Price"] = str(ifs_c)
        if halo_p != 0 or halo_c != 0:
            halo_row = scope_summary.AddNewRow(False)
            halo_row["Offering_Name"] = "HALO OA"
            halo_row["Service_Product"] = "Workforce Excellence Program"
            halo_row["List_Price"] = str(halo_p)
            halo_row["Cost_Price"] = str(halo_c)
        if training_p != 0 or training_c != 0:
            training_row = scope_summary.AddNewRow(False)
            training_row["Offering_Name"] = "Training"
            training_row["Service_Product"] = "Training"
            training_row["List_Price"] = str(training_p)
            training_row["Cost_Price"] = str(training_c)
        if tna_p != 0 or tna_c != 0:
            tna_row = scope_summary.AddNewRow(False)
            tna_row["Offering_Name"] = "Training Needs Assessment"
            tna_row["Service_Product"] = "Workforce Excellence Program"
            tna_row["List_Price"] = str(tna_p)
            tna_row["Cost_Price"] = str(tna_c)
        if om_p != 0:
            om_row = scope_summary.AddNewRow(False)
            om_row["Offering_Name"] = "Operations and Maintenance"
            om_row["Service_Product"] = "Training"
            om_row["List_Price"] = str(om_p)
            om_row["Cost_Price"] = str(float((75*om_p)/100))

        years = 1
        if Quote:
            contractDuration = Quote.GetCustomField("SC_CF_CONTRACTDURYR").Content
            contractYears = contractDuration.Split(" ")
            years = contractYears[0]

        if years != "":
            if int(float(years)) == float(years):
                years = int(float(years))
            else:
                years = int(float(years)) + 1
        else:
            years = 1

        if ocp_p != 0:
            ocp_row = scope_summary.AddNewRow(False)
            ocp_row["Offering_Name"] = "Outcome Competency Program"
            ocp_row["Service_Product"] = "Workforce Excellence Program"
            ocp_row["List_Price"] = str(float(ocp_p/years))
            ocp_row["Cost_Price"] = str(float((55*float(ocp_row["List_Price"]))/100))
        scope_summary.Calculate()

        def populateScopeSummary(cont,model,desc,py_qty,cy_qty,py_lp,py_cp,cy_lp,cy_cp,py_ulp,cy_ulp,sr_price,sa_price):
            scopeRowHidden = scope_summary_hidden.AddNewRow(False)
            if cont.Name == "SC_WEP_Models_Scope_HIF":
                scopeRowHidden['Offering_Name'] = "Honeywell Integrated Field App"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
            elif cont.Name == "SC_WEP_Models_Scope_IFS":
                scopeRowHidden['Offering_Name'] = "Immersive Field Simulator"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
            elif cont.Name == "SC_WEP_Models_Scope_Halo":
                scopeRowHidden['Offering_Name'] = "HALO OA"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
            elif cont.Name == "SC_WEP_Models_Scope_Training":
                scopeRowHidden['Offering_Name'] = "Training"
                scopeRowHidden["Service_Product"] = "Training"
            elif cont.Name == "SC_WEP_Configurable_Models_Training":
                scopeRowHidden['Offering_Name'] = "Training"
                scopeRowHidden["Service_Product"] = "Training"
            elif cont.Name == "SC_WEP_Models_Scope_TNA":
                scopeRowHidden['Offering_Name'] = "Training Needs Assessment"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
            elif cont.Name == "SC_WEP_System_Selection_TNA":
                scopeRowHidden['Offering_Name'] = "Training Needs Assessment"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
            elif cont.Name == "SC_WEP_Subscription_Price_OM":
                scopeRowHidden['Offering_Name'] = "Operations and Maintenance"
                scopeRowHidden["Service_Product"] = "Training"
            elif cont.Name == "SC_WEP_Conclusion_OCP":
                scopeRowHidden['Offering_Name'] = "Outcome Competency Program"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
            scopeRowHidden["Model"] = model
            scopeRowHidden["Description"] = desc
            scopeRowHidden["PY_Quantity"] = py_qty if py_qty else "0"
            scopeRowHidden["CY_Quantity"] = cy_qty if cy_qty else "0"
            scopeRowHidden["PY_ListPrice"] = py_lp if py_lp else "0"
            scopeRowHidden["PY_CostPrice"] = py_cp if py_cp else "0"
            scopeRowHidden["CY_ListPrice"] = cy_lp if cy_lp else "0"
            scopeRowHidden["List_Price"] = cy_lp if cy_lp else "0"
            scopeRowHidden["CY_CostPrice"] = cy_cp if cy_cp else "0"
            scopeRowHidden["PY_UnitPrice"] = py_ulp if py_ulp else "0"
            scopeRowHidden["CY_UnitPrice"] = cy_ulp if cy_ulp else "0"
            if int(scopeRowHidden["PY_Quantity"]) > int(scopeRowHidden["CY_Quantity"]):
                scopeRowHidden["SR_Quantity"] = str(int(scopeRowHidden["CY_Quantity"]) - int(scopeRowHidden["PY_Quantity"]))
                scopeRowHidden["SA_Quantity"] = "0"
                scopeRowHidden['Comments'] = "Scope Reduction"
            elif int(scopeRowHidden["CY_Quantity"]) > int(scopeRowHidden["PY_Quantity"]):
                scopeRowHidden["SR_Quantity"] = "0"
                scopeRowHidden["SA_Quantity"] = str(int(scopeRowHidden["CY_Quantity"]) - int(scopeRowHidden["PY_Quantity"]))
                scopeRowHidden['Comments'] = "Scope Addition"
            else:
                scopeRowHidden["SR_Quantity"] = "0"
                scopeRowHidden["SA_Quantity"] = "0"
                scopeRowHidden['Comments'] = "No Scope Change"
            if cont.Name in ("SC_WEP_Configurable_Models_Training","SC_WEP_System_Selection_TNA"):
                scopeRowHidden["SR_Price"] = sr_price
                scopeRowHidden["SA_Price"] = sa_price
                scopeRowHidden['Escalation_Price'] = py_ulp if py_ulp else "0"
            else:
                scopeRowHidden["SR_Price"] = str(float(py_ulp)*float(scopeRowHidden['SR_Quantity'])) if py_ulp else "0"
                scopeRowHidden["SA_Price"] = str(float(cy_ulp)*float(scopeRowHidden['SA_Quantity'])) if cy_ulp else "0"
                if int(scopeRowHidden['CY_Quantity']) < int(scopeRowHidden['PY_Quantity']):
                    scopeRowHidden['Escalation_Price'] = str(float(scopeRowHidden["CY_Quantity"])*float(py_ulp)) if py_ulp else "0"
                else:
                    scopeRowHidden['Escalation_Price'] = str(float(scopeRowHidden["PY_Quantity"])*float(py_ulp)) if py_ulp else "0"
            scopeRowHidden.Calculate()

        def readWEPcont(cont):
            if cont.Name == "SC_WEP_Configurable_Models_Training":
                if cont.Rows.Count:
                    for row in cont.Rows:
                        populateScopeSummary(cont,row["Model"],row["Description"],"0","1","0","0",row["List_Price"],row["Cost_Price"],"0",row["Unit_Price"],"0","0")
            elif cont.Name in ("SC_WEP_Models_Scope_IFS","SC_WEP_Models_Scope_Halo"):
                if cont.Rows.Count:
                    for row in cont.Rows:
                        populateScopeSummary(cont,row["Model"],row["Description"],"0",row["Quantity"],"0","0",row["List_Price"],row["Cost_Price"],"0",row["UI_Price"],"0","0")
            else:
                if cont.Rows.Count:
                    for row in cont.Rows:
                        populateScopeSummary(cont,row["Model"],row["Description"],"0",row["Quantity"],"0","0",row["List_Price"],row["Cost_Price"],"0",row["Unit_Price"],"0","0")

        om_py = 0
        om_cy = 0
        ocp_py = 0
        ocp_cy = 0
        ss_py = 0
        ss_cy = 0
        ss_py_c = 0
        ss_cy_c = 0
        ss_sr_price = 0
        ss_sa_price = 0

        wepList = [HIF_valid,IFS_valid,Halo_valid,Training_valid,Configurable_valid,TNA_valid]
        for cont in wepList:
            readWEPcont(cont)

        #System Selection
        if Sys_Sel.Rows.Count:
            ss_desc = ""
            for row in Sys_Sel.Rows:
                if row["User_Count"] not in ("0",""):
                    ss_desc += row["Selected_System"] + ","
                ss_cy += float(str(row['Per_system_Price'])) if row["Per_system_Price"] else 0
                ss_cy_c += float(str(row['Per_system_Cost'])) if row["Per_system_Cost"] else 0
        if ss_cy != 0 or ss_cy_c != 0:
            if ss_desc != "":
                ss_desc = ss_desc[:-1]
            populateScopeSummary(Sys_Sel,"TNA-Systems",ss_desc,"0","1","0","0",str(ss_cy),str(ss_cy_c),"0",str(ss_cy),"0","0")

        #Operations and Maintenance
        if Subscription_OM.Rows.Count:
            for row in Subscription_OM.Rows:
                om_cy += float(str(row['Subscription_Price'])) if row["Subscription_Price"] else 0
        if Add_on_Fees_OM.Rows.Count:
            for row in Add_on_Fees_OM.Rows:
                om_cy += float(str(row['Subscription_Price'])) if row["Subscription_Price"] else 0
        if om_cy != 0:
            populateScopeSummary(Subscription_OM,"","","0","1","0","0",str(om_cy),str(float((75*om_cy)/100)),"0",str(om_cy),"0","0")

        #Outcome Comptency Program
        years = 1
        if Quote:
            contractDuration = Quote.GetCustomField("SC_CF_CONTRACTDURYR").Content
            contractYears = contractDuration.Split(" ")
            years = contractYears[0]

        if years != "":
            if int(float(years)) == float(years):
                years = int(float(years))
            else:
                years = int(float(years)) + 1
        else:
            years = 1

        if Conclusion_OCP.Rows.Count:
            for row in Conclusion_OCP.Rows:
                ocp_cy += float(str(row['Value'])) if row["Value"] else 0
        if ocp_cy != 0:
            ocp_desc = "Current Year Score : " + str(Product.Attr('SC_WEP_Current_Score_OCP').GetValue())
            ocp_cy_quantity = str(Product.Attr('SC_WEP_No_of_Users_OCP').GetValue())
            ocp_cyup = str(ocp_cy/float(ocp_cy_quantity)) if ocp_cy_quantity not in ("","0") else "0"
            populateScopeSummary(Conclusion_OCP,"",ocp_desc,"0",ocp_cy_quantity,"0","0",str(ocp_cy/years),str(float((55*float(ocp_cy/years))/100)),"0",ocp_cyup,"0","0")

        scope_summary_hidden.Calculate()


    elif Product.Attr('SC_Product_Type').GetValue() == "Renewal":

        def populateScopeSummary(cont,model,desc,py_qty,cy_qty,py_lp,py_cp,cy_lp,cy_cp,py_ulp,cy_ulp,sr_price,sa_price):
            scopeRowHidden = scope_summary_hidden.AddNewRow(False)
            if cont.Name == "SC_WEP_Models_Scope_HIF":
                scopeRowHidden['Offering_Name'] = "Honeywell Integrated Field App"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
                SC_Pricing_Escalation = Product.Attr('SC_WEP_HIF_Pricing_Escalation').GetValue()
            elif cont.Name == "SC_WEP_Models_Scope_IFS":
                scopeRowHidden['Offering_Name'] = "Immersive Field Simulator"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
                SC_Pricing_Escalation = Product.Attr('SC_WEP_IFS_Pricing_Escalation').GetValue()
            elif cont.Name == "SC_WEP_Models_Scope_Halo":
                scopeRowHidden['Offering_Name'] = "HALO OA"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
                SC_Pricing_Escalation = Product.Attr('SC_WEP_Halo_Pricing_Escalation').GetValue()
            elif cont.Name == "SC_WEP_Models_Scope_Training":
                scopeRowHidden['Offering_Name'] = "Training"
                scopeRowHidden["Service_Product"] = "Training"
                SC_Pricing_Escalation = Product.Attr('SC_WEP_Training_Pricing_Escalation').GetValue()
            elif cont.Name == "SC_WEP_Configurable_Models_Training":
                scopeRowHidden['Offering_Name'] = "Training"
                scopeRowHidden["Service_Product"] = "Training"
                SC_Pricing_Escalation = Product.Attr('SC_WEP_Training_Pricing_Escalation').GetValue()
            elif cont.Name == "SC_WEP_Models_Scope_TNA":
                scopeRowHidden['Offering_Name'] = "Training Needs Assessment"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
                SC_Pricing_Escalation = Product.Attr('SC_WEP_TNA_Pricing_Escalation').GetValue()
            elif cont.Name == "SC_WEP_System_Selection_TNA":
                scopeRowHidden['Offering_Name'] = "Training Needs Assessment"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
                SC_Pricing_Escalation = Product.Attr('SC_WEP_TNA_Pricing_Escalation').GetValue()
            elif cont.Name == "SC_WEP_Subscription_Price_OM":
                scopeRowHidden['Offering_Name'] = "Operations and Maintenance"
                scopeRowHidden["Service_Product"] = "Training"
                SC_Pricing_Escalation = Product.Attr('SC_WEP_OM_Pricing_Escalation').GetValue()
            elif cont.Name == "SC_WEP_Conclusion_OCP":
                scopeRowHidden['Offering_Name'] = "Outcome Competency Program"
                scopeRowHidden["Service_Product"] = "Workforce Excellence Program"
                SC_Pricing_Escalation = Product.Attr('SC_WEP_OCP_Pricing_Escalation').GetValue()
            scopeRowHidden["Model"] = model
            scopeRowHidden["Description"] = desc
            scopeRowHidden["PY_Quantity"] = py_qty if py_qty else "0"
            scopeRowHidden["CY_Quantity"] = cy_qty if cy_qty else "0"
            scopeRowHidden["PY_ListPrice"] = py_lp if py_lp else "0"
            scopeRowHidden["PY_CostPrice"] = py_cp if py_cp else "0"
            scopeRowHidden["CY_ListPrice"] = cy_lp if cy_lp else "0"
            scopeRowHidden["CY_CostPrice"] = cy_cp if cy_cp else "0"
            scopeRowHidden["PY_UnitPrice"] = py_ulp if py_ulp else "0"
            scopeRowHidden["CY_UnitPrice"] = cy_ulp if cy_ulp else "0"
            if int(scopeRowHidden["PY_Quantity"]) > int(scopeRowHidden["CY_Quantity"]):
                scopeRowHidden["SR_Quantity"] = str(int(scopeRowHidden["CY_Quantity"]) - int(scopeRowHidden["PY_Quantity"]))
                scopeRowHidden["SA_Quantity"] = "0"
                scopeRowHidden['Comments'] = "Scope Reduction"
            elif int(scopeRowHidden["CY_Quantity"]) > int(scopeRowHidden["PY_Quantity"]):
                scopeRowHidden["SR_Quantity"] = "0"
                scopeRowHidden["SA_Quantity"] = str(int(scopeRowHidden["CY_Quantity"]) - int(scopeRowHidden["PY_Quantity"]))
                scopeRowHidden['Comments'] = "Scope Addition"
            else:
                scopeRowHidden["SR_Quantity"] = "0"
                scopeRowHidden["SA_Quantity"] = "0"
                scopeRowHidden['Comments'] = "No Scope Change"
            if cont.Name in ("SC_WEP_Configurable_Models_Training","SC_WEP_System_Selection_TNA"):
                scopeRowHidden["SR_Price"] = sr_price
                scopeRowHidden["SA_Price"] = sa_price
            else:
                scopeRowHidden["SR_Price"] = str(float(py_ulp)*float(scopeRowHidden['SR_Quantity'])) if py_ulp else "0"
                scopeRowHidden["SA_Price"] = str(float(cy_ulp)*float(scopeRowHidden['SA_Quantity'])) if cy_ulp else "0"
            if SC_Pricing_Escalation == "Yes":
                if int(scopeRowHidden['CY_Quantity']) > int(scopeRowHidden['PY_Quantity']):
                    scopeRowHidden['Escalation_Price'] =  str(float(scopeRowHidden["PY_Quantity"])*float(py_ulp))
                    scopeRowHidden['List_Price'] = str((float(scopeRowHidden['PY_Quantity'])*float(py_ulp)) + ((int(scopeRowHidden['CY_Quantity']) - int(scopeRowHidden['PY_Quantity']))*float(cy_ulp)))
                else:
                    scopeRowHidden['Escalation_Price'] = str(float(scopeRowHidden['CY_Quantity'])*float(py_ulp))
                    scopeRowHidden['List_Price'] = str(float(scopeRowHidden['CY_Quantity'])*float(py_ulp))
            else:
                scopeRowHidden['Escalation_Price'] = '0'
                scopeRowHidden['List_Price'] = str(cy_lp)
            py_discount = float(compDict.get(scopeRowHidden["Service_Product"],0))
            scopeRowHidden["PY_Discount"] = str(py_discount * 100)
            scopeRowHidden["PY_SellPrice"] = str(float(scopeRowHidden['PY_ListPrice']) - (float(scopeRowHidden['PY_ListPrice']) * py_discount))
            scopeRowHidden.Calculate()

        def readWEPcont(cont):
            if cont.Name == "SC_WEP_Configurable_Models_Training":
                if cont.Rows.Count:
                    for row in cont.Rows:
                        populateScopeSummary(cont,row["Model"],row["Description"],"1",row["CY_Quantity"],row["PY_ListPrice"],row["PY_CostPrice"],row["CY_ListPrice"],row["CY_CostPrice"],row["PY_UnitPrice"],row["CY_UnitPrice"],row["SR_Price"],row["SA_Price"])
            else:
                if cont.Rows.Count:
                    for row in cont.Rows:
                        populateScopeSummary(cont,row["Model"],row["Description"],row["PY_Quantity"],row["CY_Quantity"],row["PY_ListPrice"],row["PY_CostPrice"],row["CY_ListPrice"],row["CY_CostPrice"],row["PY_UnitPrice"],row["CY_UnitPrice"],"","")

        om_py = 0
        om_cy = 0
        ocp_py = 0
        ocp_cy = 0
        ss_py = 0
        ss_cy = 0
        ss_py_c = 0
        ss_cy_c = 0
        ss_sr_price = 0
        ss_sa_price = 0

        comparisonCont = Product.GetContainerByName('ComparisonSummary')
        compDict = {}
        if comparisonCont.Rows.Count:
            for compRow in comparisonCont.Rows:
                compDict[compRow["Service_Product"]] = compRow["PY_Discount_SFDC"] if compRow["PY_Discount_SFDC"] else '0'

        wepList = [HIF_valid,IFS_valid,Halo_valid,Training_valid,Configurable_valid,TNA_valid]
        for cont in wepList:
            readWEPcont(cont)

        #System Selection
        if Sys_Sel.Rows.Count:
            ss_desc = ""
            for row in Sys_Sel.Rows:
                if row["CY_UserCount"] not in ("0",""):
                    ss_desc += row["Selected_System"] + ","
                ss_py += float(str(row['PY_SystemPrice'])) if row["PY_SystemPrice"] else 0
                ss_cy += float(str(row['CY_SystemPrice'])) if row["CY_SystemPrice"] else 0
                ss_py_c += float(str(row['PY_SystemCost'])) if row["PY_SystemCost"] else 0
                ss_cy_c += float(str(row['CY_SystemCost'])) if row["CY_SystemCost"] else 0
                ss_sr_price += float(str(row['SR_Price'])) if row["SR_Price"] else 0
                ss_sa_price += float(str(row['SA_Price'])) if row["SA_Price"] else 0
            if ss_desc != "":
                ss_desc = ss_desc[:-1]
        if (ss_py > 0 or ss_py_c > 0) and (ss_cy > 0 or ss_cy_c > 0):
            populateScopeSummary(Sys_Sel,"TNA-Systems",ss_desc,"1","1",str(ss_py),str(ss_py_c),str(ss_cy),str(ss_cy_c),str(ss_py),str(ss_cy),str(ss_sr_price),str(ss_sa_price))
        elif (ss_py > 0 or ss_py_c > 0) and (ss_cy <= 0 and ss_cy_c <= 0):
            populateScopeSummary(Sys_Sel,"TNA-Systems",ss_desc,"1","0",str(ss_py),str(ss_py_c),str(ss_cy),str(ss_cy_c),str(ss_py),str(ss_cy),str(ss_sr_price),str(ss_sa_price))
        elif (ss_py <= 0 and ss_py_c <= 0) and (ss_cy > 0 or ss_cy_c > 0):
            populateScopeSummary(Sys_Sel,"TNA-Systems",ss_desc,"0","1",str(ss_py),str(ss_py_c),str(ss_cy),str(ss_cy_c),str(ss_py),str(ss_cy),str(ss_sr_price),str(ss_sa_price))


        #Operations and Maintenance
        if Subscription_OM.Rows.Count:
            for row in Subscription_OM.Rows:
                om_py += float(str(row['PY_SubscriptionPrice'])) if row["PY_SubscriptionPrice"] else 0
                om_cy += float(str(row['CY_SubscriptionPrice'])) if row["CY_SubscriptionPrice"] else 0
        if Add_on_Fees_OM.Rows.Count:
            for row in Add_on_Fees_OM.Rows:
                om_py += float(str(row['PY_SubscriptionPrice'])) if row["PY_SubscriptionPrice"] else 0
                om_cy += float(str(row['CY_SubscriptionPrice'])) if row["CY_SubscriptionPrice"] else 0
        if om_py > 0 and om_cy > 0:
            populateScopeSummary(Subscription_OM,"","","1","1",str(om_py),str(float((75*om_py)/100)),str(om_cy),str(float((75*om_cy)/100)),str(om_py),str(om_cy),"","")
        elif om_py > 0 and om_cy <= 0:
            populateScopeSummary(Subscription_OM,"","","1","0",str(om_py),str(float((75*om_py)/100)),str(om_cy),str(float((75*om_cy)/100)),str(om_py),str(om_cy),"","")
        elif om_py <= 0 and om_cy > 0:
            populateScopeSummary(Subscription_OM,"","","0","1",str(om_py),str(float((75*om_py)/100)),str(om_cy),str(float((75*om_cy)/100)),str(om_py),str(om_cy),"","")


        #Outcome Comptency Program
        years = 1
        if Quote:
            contractDuration = Quote.GetCustomField("SC_CF_CONTRACTDURYR").Content
            contractYears = contractDuration.Split(" ")
            years = contractYears[0]

        if years != "":
            if int(float(years)) == float(years):
                years = int(float(years))
            else:
                years = int(float(years)) + 1
        else:
            years = 1

        if Conclusion_OCP.Rows.Count:
            for row in Conclusion_OCP.Rows:
                ocp_py += float(str(row['PY_Value'])) if row["PY_Value"] else 0
                ocp_cy += float(str(row['CY_Value'])) if row["CY_Value"] else 0
        if ocp_py != 0 or ocp_cy != 0:
            ocp_desc = "Previous Year Score : " + str(Product.Attr('SC_WEP_Current_Score_OCP_PY').GetValue()) + ", " + "Current Year Score : " + str(Product.Attr('SC_WEP_Current_Score_OCP').GetValue())
            ocp_py_quantity = str(Product.Attr('SC_WEP_No_of_Users_OCP_PY').GetValue())
            ocp_cy_quantity = str(Product.Attr('SC_WEP_No_of_Users_OCP').GetValue())
            ocp_pyup = str(ocp_py/float(ocp_py_quantity)) if ocp_py_quantity not in ("","0") else "0"
            ocp_cyup = str(ocp_cy/float(ocp_cy_quantity)) if ocp_cy_quantity not in ("","0") else "0"
            populateScopeSummary(Conclusion_OCP,"",ocp_desc,ocp_py_quantity,ocp_cy_quantity,str(float(ocp_py/years)),str(float((55*float(ocp_py/years))/100)),str(ocp_cy/years),str(float((55*float(ocp_cy/years))/100)),ocp_pyup,ocp_cyup,"","")

        scope_summary_hidden.Calculate()

        x = Product.Attr("SC_WEP_RC_Selection").SelectedValues
        if scope_summary_hidden.Rows.Count:
            for row in scope_summary_hidden.Rows:
                for i in x:
                    if i.Display == row["Comments"]:
                        scopeRow = scope_summary.AddNewRow(False)
                        scopeRow['Offering_Name'] = row['Offering_Name']
                        scopeRow['Model'] = row['Model']
                        scopeRow['Description'] = row['Description']
                        scopeRow['PY_Quantity'] = row['PY_Quantity']
                        scopeRow['CY_Quantity'] = row['CY_Quantity']
                        scopeRow['PY_ListPrice'] = row['PY_ListPrice']
                        scopeRow['PY_CostPrice'] = row['PY_CostPrice']
                        scopeRow['CY_ListPrice'] = row['CY_ListPrice']
                        scopeRow['CY_CostPrice'] = row['CY_CostPrice']
                        scopeRow['SR_Quantity'] = row['SR_Quantity']
                        scopeRow['SA_Quantity'] = row['SA_Quantity']
                        scopeRow['Comments'] = row['Comments']
                        scopeRow.Calculate()
            scope_summary.Calculate()