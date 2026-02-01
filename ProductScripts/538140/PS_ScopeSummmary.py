SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
QuoteType = Quote.GetCustomField("Quote Type").Content
if SC_Product_Type == 'New':
    scopesummary_ent = Product.GetContainerByName('SC_ScopeSummary_entitlement_cont')
    scopesummary_ent.Rows.Clear()
    scopesummary_ent_type = Product.GetContainerByName('SC_TPS_Entitlements_Scope_summary')
    scopesummary_ent_type.Rows.Clear()
    ValidModelsCont = Product.GetContainerByName('SC_TPS_Models_Scope')

    tps_hw = 0
    tps_labor = 0
    tps_sw_sub = 0

    hw_listPrice = 0
    labor_listPrice = 0
    sw_sub_listPrice = 0
    hw_cost = 0
    labor_cost = 0
    sw_sub_cost = 0

    if ValidModelsCont.Rows.Count:
        for row in ValidModelsCont.Rows:
            if row['Entitlement'] == "Third Party Hardware" and tps_hw == 0:
                ScopeSummaryTypeRow = scopesummary_ent_type.AddNewRow(False)
                ScopeSummaryTypeRow["Entitlement"] = "Third Party Hardware"
                ScopeSummaryTypeRow["Type"] = "Optional"
                tps_hw += 1
            if row['Entitlement'] == "Third Party Labour" and tps_labor == 0:
                ScopeSummaryTypeRow = scopesummary_ent_type.AddNewRow(False)
                ScopeSummaryTypeRow["Entitlement"] = "Third Party Labour"
                ScopeSummaryTypeRow["Type"] = "Optional"
                tps_labor += 1
            if row['Entitlement'] == "Third Party Software/Subscription" and tps_sw_sub == 0:
                ScopeSummaryTypeRow = scopesummary_ent_type.AddNewRow(False)
                ScopeSummaryTypeRow["Entitlement"] = "Third Party Software/Subscription"
                ScopeSummaryTypeRow["Type"] = "Optional"
                tps_sw_sub += 1

            if row['Entitlement'] == 'Third Party Hardware' and row['List_Price'] != "":
                hw_listPrice += eval(row['List_Price'])
                hw_cost += eval(row['COST']) if row['COST'] != "" else 0
            elif row['Entitlement'] == 'Third Party Labour' and row['List_Price'] != "":
                labor_listPrice += eval(row['List_Price'])
                labor_cost += eval(row['COST']) if row['COST'] != "" else 0
            elif row['Entitlement'] == 'Third Party Software/Subscription' and row['List_Price'] != "":
                sw_sub_listPrice += eval(row['List_Price'])
                sw_sub_cost += eval(row['COST']) if row['COST'] != "" else 0


    if hw_listPrice != 0:
        row = scopesummary_ent.AddNewRow(False)
        row['Entitlement'] = 'Third Party Hardware'
        row['List Price'] = str(hw_listPrice)
        row['COST'] = str(hw_cost)

    if labor_listPrice != 0:
        row = scopesummary_ent.AddNewRow(False)
        row['Entitlement'] = 'Third Party Labour'
        row['List Price'] = str(labor_listPrice)
        row['COST'] = str(labor_cost)

    if sw_sub_listPrice != 0:
        row = scopesummary_ent.AddNewRow(False)
        row['Entitlement'] = 'Third Party Software/Subscription'
        row['List Price'] = str(sw_sub_listPrice)
        row['COST'] = str(sw_sub_cost)
elif SC_Product_Type == 'Renewal':
    def getInt(n):
        try:
            return float(n)
        except:
            return 0
    scopesummary_ent = Product.GetContainerByName('SC_ScopeSummary_entitlement_cont')
    scopesummary_ent.Rows.Clear()
    scopesummary_ent_type = Product.GetContainerByName('SC_TPS_Entitlements_Scope_summary')
    scopesummary_ent_type.Rows.Clear()
    scopesummary_ent_hidden = Product.GetContainerByName('SC_TPS_RC_Entitlements_Scope_summary_hidden')
    scopesummary_ent_hidden.Rows.Clear()
    ValidModelsCont = Product.GetContainerByName('SC_TPS_Models_Scope')
    SC_Pricing_Escalation = Product.Attr('SC_Pricing_Escalation').GetValue()

    comparisonCont = Product.GetContainerByName('ComparisonSummary')
    compDict = {}
    if comparisonCont.Rows.Count:
        for compRow in comparisonCont.Rows:
            compDict[compRow["Service_Product"]] = compRow["PY_Discount_SFDC"] if compRow["PY_Discount_SFDC"] else '0'


    tps_hw = 0
    tps_labor = 0
    tps_sw_sub = 0

    if ValidModelsCont.Rows.Count:
        for row in ValidModelsCont.Rows:
            if row['Entitlement'] == "Third Party Hardware" and tps_hw == 0:
                ScopeSummaryTypeRow = scopesummary_ent_type.AddNewRow(False)
                ScopeSummaryTypeRow["Entitlement"] = "Third Party Hardware"
                ScopeSummaryTypeRow["Type"] = "Optional"
                tps_hw += 1
            if row['Entitlement'] == "Third Party Labour" and tps_labor == 0:
                ScopeSummaryTypeRow = scopesummary_ent_type.AddNewRow(False)
                ScopeSummaryTypeRow["Entitlement"] = "Third Party Labour"
                ScopeSummaryTypeRow["Type"] = "Optional"
                tps_labor += 1
            if row['Entitlement'] == "Third Party Software/Subscription" and tps_sw_sub == 0:
                ScopeSummaryTypeRow = scopesummary_ent_type.AddNewRow(False)
                ScopeSummaryTypeRow["Entitlement"] = "Third Party Software/Subscription"
                ScopeSummaryTypeRow["Type"] = "Optional"
                tps_sw_sub += 1

            scopesummary_ent_hiddenRow = scopesummary_ent_hidden.AddNewRow(False)
            scopesummary_ent_hiddenRow['Entitlement'] = row['Entitlement']
            scopesummary_ent_hiddenRow['3rd_Party_Models'] = row['3rd_Party_Models']
            scopesummary_ent_hiddenRow['Description'] = row['Description']
            scopesummary_ent_hiddenRow['PY_Quantity'] = row['PY_Quantity']
            scopesummary_ent_hiddenRow['Quantity'] = row['Renewal_Quantity']
            scopesummary_ent_hiddenRow['PY_ListPrice'] = row['PY_ListPrice']
            scopesummary_ent_hiddenRow['HW_ListPrice'] = row['HW_ListPrice']
            scopesummary_ent_hiddenRow['COST'] = row['CY_Cost_Price']
            scopesummary_ent_hiddenRow['PY_COST'] = row['PY_COST']
            #scopesummary_ent_hiddenRow['Scope_Change_Price'] = row['Scope_Change']
            scopesummary_ent_hiddenRow['SA_Price'] = row['SA_Price']
            scopesummary_ent_hiddenRow['SR_Price'] = row['SR_Price']
            SA = getInt(row['SA_Price'])
            SR = getInt(row['SR_Price'])
            if SA+SR == 0:
                scopesummary_ent_hiddenRow["Comments"] = 'No Scope Change'
            elif SA+SR < 0:
                scopesummary_ent_hiddenRow["Comments"] = 'Scope Reduction'
            else:
                scopesummary_ent_hiddenRow["Comments"] = 'Scope Addition'
            row['PY_Quantity'] = row['PY_Quantity'] if row['PY_Quantity'] != '' else '0'
            row['Renewal_Quantity'] = row['Renewal_Quantity'] if row['Renewal_Quantity'] != '' else '0'
            row['PY_UnitPrice'] = row['PY_UnitPrice'] if row['PY_UnitPrice'] != '' else '0'
            row['HW_UnitPrice'] = row['HW_UnitPrice'] if row['HW_UnitPrice'] != '' else '0'
            scopesummary_ent_hiddenRow['PY_ListPrice'] = scopesummary_ent_hiddenRow['PY_ListPrice'] if scopesummary_ent_hiddenRow['PY_ListPrice'] != '' else '0'
            if SC_Pricing_Escalation == "Yes":
                if int(row['Renewal_Quantity']) > int(row['PY_Quantity']):
                    scopesummary_ent_hiddenRow['Escalation_Price'] = str(float(row['PY_Quantity'])*float(row['PY_UnitPrice']))
                    scopesummary_ent_hiddenRow['List_Price'] = str((float(row['PY_Quantity'])*float(row['PY_UnitPrice'])) + ((int(row['Renewal_Quantity']) - int(row['PY_Quantity']))*float(row['HW_UnitPrice'])))
                else:
                    scopesummary_ent_hiddenRow['Escalation_Price'] = str(float(row['Renewal_Quantity'])*float(row['PY_UnitPrice']))
                    scopesummary_ent_hiddenRow['List_Price'] = str(float(row['Renewal_Quantity'])*float(row['PY_UnitPrice']))
            else:
                scopesummary_ent_hiddenRow['Escalation_Price'] = '0'
                scopesummary_ent_hiddenRow['List_Price'] = row['HW_ListPrice']
            py_discount = float(compDict.get('Third Party Services',0))
            scopesummary_ent_hiddenRow["PY_Discount"] = str(py_discount * 100)
            scopesummary_ent_hiddenRow["PY_SellPrice"] = str(float(scopesummary_ent_hiddenRow['PY_ListPrice']) - (float(scopesummary_ent_hiddenRow['PY_ListPrice']) * py_discount))
        scopesummary_ent_hidden.Calculate()

        attr_sel = Product.Attr("SC_TPS_RC_Selection").SelectedValues
        if scopesummary_ent_hidden.Rows.Count:
            for row in scopesummary_ent_hidden.Rows:
                for value in attr_sel:
                    if value.Display == row["Comments"]:
                        scopesummary_entRow = scopesummary_ent.AddNewRow(False)
                        scopesummary_entRow['Entitlement'] = row['Entitlement']
                        scopesummary_entRow['3rd_Party_Models'] = row['3rd_Party_Models']
                        scopesummary_entRow['Description'] = row['Description']
                        scopesummary_entRow['PY_Quantity'] = row['PY_Quantity']
                        scopesummary_entRow['Quantity'] = row['Quantity']
                        scopesummary_entRow['PY_ListPrice'] = row['PY_ListPrice']
                        scopesummary_entRow['HW_ListPrice'] = row['HW_ListPrice']
                        scopesummary_entRow['CY_CostPrice'] = row['COST']
                        scopesummary_entRow['PY_COST'] = row['PY_COST']
                        #scopesummary_entRow['Scope_Change_Price'] = row['Scope_Change_Price']
                        scopesummary_entRow['SA_Price'] = row['SA_Price']
                        scopesummary_entRow['SR_Price'] = row['SR_Price']
                        scopesummary_entRow['Comments'] = row['Comments']
            scopesummary_ent.Calculate()

if SC_Product_Type == 'New': # and QuoteType == 'Contract Renewal':
    Trace.Write('hey')
    ValidModelsCont = Product.GetContainerByName('SC_TPS_Models_Scope')
    scopesummary_new_hidden = Product.GetContainerByName('SC_TPS_RC_Entitlements_Scope_summary_hidden')
    scopesummary_new_hidden.Rows.Clear()


    if ValidModelsCont.Rows.Count:
        for row in ValidModelsCont.Rows:
            scopesummary_new_hiddenRow = scopesummary_new_hidden.AddNewRow(False)
            scopesummary_new_hiddenRow['Entitlement'] = row['Entitlement']
            scopesummary_new_hiddenRow['3rd_Party_Models'] = row['3rd_Party_Models']
            scopesummary_new_hiddenRow['Description'] = row['Description']
            scopesummary_new_hiddenRow['Quantity'] = row['Quantity']
            scopesummary_new_hiddenRow['HW_ListPrice'] = row['List_Price']
            scopesummary_new_hiddenRow['List_Price'] = row['List_Price']
            scopesummary_new_hiddenRow['COST'] = row['COST']
        scopesummary_new_hidden.Calculate()