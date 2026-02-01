SC_Product_Type = Product.Attr('SC_Product_Type').GetValue()
if SC_Product_Type == 'New':
    quoteCurrency = Quote.SelectedMarket.CurrencyCode
    EXCHANGE_RATE = Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content if Quote.GetCustomField(
        'SC_CF_EXCHANGE_RATE').Content else 1  # SqlHelper.GetFirst("select Exchange_Rate from Currency_ExchangeRate_Mapping where From_Currency = 'USD' and To_Currency = '{}'".format(quoteCurrency))


    def currency(c):
        return float(c) * float(EXCHANGE_RATE)


    Model_Scope = Product.GetContainerByName("SC_GN_AT_Models_Scope_Cont")
    CYB_Models_Hid_Cont = Product.GetContainerByName('SC_GN_AT_Models_Cont_Hidden')
    CYB_Models_Hid_Cont.Clear()
    SP = []
    summary = Product.GetContainerByName('SC_GN_AT_Models_Cont')
    summary.Clear()
    # Fetching all values
    for row in Model_Scope.Rows:
        sp_name = row['Service_Product']
        SP.append(sp_name)
    sp1 = set(SP)
    # calculation part
    for i in sp1:
        final_sum_lp = 0
        final_sum_cp = 0
        for row in Model_Scope.Rows:
            if i == row['Service_Product']:
                qty = int(row['Quantity'])
                if row['Unit_List_Price'] == "":
                    a = 0
                else:
                    a = float(row['Unit_List_Price'])
                if row['Unit_Cost_Price'] == "":
                    b = 0
                else:
                    b = float(row['Unit_Cost_Price'])
                lp = a
                cp = b
                s = qty * lp
                c = qty * cp
                final_sum_lp += s
                final_sum_cp += c

        row1 = summary.AddNewRow(True)
        row1['Service_Product'] = i
        L_Price = round(final_sum_lp, 2)
        row1['List_Price'] = str(L_Price)

        C_Price = round(final_sum_cp, 2)
        row1['Cost_Price'] = str(C_Price)
        Hidden_row = CYB_Models_Hid_Cont.AddNewRow(True)
        Hidden_row['Service_Product'] = row1['Service_Product']
        Hidden_row['Asset'] = row1['Asset']
        Hidden_row['Model'] = row1['Model']
        Hidden_row['Description'] = row1['Description']
        #Hidden_row['Quantity'] = str(qty)
        Hidden_row['List_Price'] = row1['List_Price']
        Hidden_row['Cost_Price'] = row1['Cost_Price']
    summary.Calculate()
    CYB_Models_Hid_Cont.Calculate()
if SC_Product_Type == 'Renewal':
    modelScopeCont = Product.GetContainerByName('SC_GN_AT_Models_Scope_Cont')
    scopeCont = Product.GetContainerByName('SC_GN_AT_Models_Cont')
    scopeContHidden = Product.GetContainerByName('SC_GN_AT_Models_Cont_Hidden')
    scopeContHidden.Rows.Clear()
    scopeCont.Rows.Clear()

    if modelScopeCont.Rows.Count:
        for row in modelScopeCont.Rows:
            scopeContRowHidden = scopeContHidden.AddNewRow(False)
            scopeContRowHidden['Service_Product'] = row['Service_Product']
            scopeContRowHidden['Asset'] = row['Asset No']
            scopeContRowHidden['Model'] = row['Model_Number']
            scopeContRowHidden['Description'] = row['Description']
            scopeContRowHidden['PY_Quantity'] = row['PY_Quantity']
            scopeContRowHidden['Renewal_Quantity'] = row['Renewal_Quantity']
            scopeContRowHidden['PY_ListPrice'] = row['PY_ListPrice']
            scopeContRowHidden['CY_ListPrice'] = row['CY_ListPrice']
            scopeContRowHidden['PY_CostPrice'] = row['PY_CostPrice']
            scopeContRowHidden['CY_CostPrice'] = row['CY_CostPrice']
            scopeContRowHidden['Cost_Price'] = row['CY_CostPrice']
            scopeContRowHidden['HW_UnitPrice'] = row['HW_UnitPrice']
            scopeContRowHidden['PY_Discount'] = row['PY_Discount']
            scopeContRowHidden['PY_SellPrice'] = row['PY_SellPrice']
            # Trace.Write("row['Renewal_Quantity']:---"+str(row['HW_UnitPrice']))
            # Trace.Write("row['PY_Quantity']:---"+str(row['PY_Quantity']))
            if row['Renewal_Quantity'] == "":
                row['Renewal_Quantity'] = '0'
            if int(row['Renewal_Quantity']) > int(row['PY_Quantity']) if row['PY_Quantity'] else 0:
                scopeContRowHidden['SR_Quantity'] = '0'
                scopeContRowHidden['SA_Quantity'] = str(
                    int(row['Renewal_Quantity']) - int(row['PY_Quantity']) if row['PY_Quantity'] else 0)
                scopeContRowHidden['Comments'] = "Scope Addition"
            elif int(row['Renewal_Quantity']) < int(row['PY_Quantity']):
                scopeContRowHidden['SR_Quantity'] = str(
                    int(row['Renewal_Quantity']) - int(row['PY_Quantity']) if row['PY_Quantity'] else 0)
                scopeContRowHidden['SA_Quantity'] = '0'
                scopeContRowHidden['Comments'] = "Scope Reduction"
            else:
                scopeContRowHidden['SR_Quantity'] = '0'
                scopeContRowHidden['SA_Quantity'] = '0'
                scopeContRowHidden['Comments'] = "No Scope Change"
            if row['PY_Quantity'] not in ['', '0']:
                scopeContRowHidden['SR_Price'] = str(
                    (float(row['PY_ListPrice']) / int(row['PY_Quantity'])) * float(scopeContRowHidden['SR_Quantity']))
            scopeContRowHidden['SA_Price'] = str(
                (float(row['HW_UnitPrice']) if row['HW_UnitPrice'] != '' else 0) * float(
                    scopeContRowHidden['SA_Quantity']))
            if Product.Attr('SC_Pricing_Escalation').GetValue() == "Yes":
                if int(row['Renewal_Quantity']) > int(row['PY_Quantity']):
                    scopeContRowHidden['List_Price'] = str(float(row['PY_ListPrice']) + (
                                (float(row['Renewal_Quantity']) - float(row['PY_Quantity'])) * float(
                            row['HW_UnitPrice'])))
                    scopeContRowHidden['Escalation_Price'] = row['PY_ListPrice']
                else:
                    scopeContRowHidden['List_Price'] = str(float(row['Renewal_Quantity']) * (
                        float(row['PY_ListPrice']) / float(row['PY_Quantity']) if row['PY_Quantity'] != '' else '0'))
                    scopeContRowHidden['Escalation_Price'] = str(float(row['Renewal_Quantity']) * (
                        float(row['PY_ListPrice']) / float(row['PY_Quantity']) if row['PY_Quantity'] != '' else '0'))

            else:
                scopeContRowHidden['List_Price'] = str(row['CY_ListPrice'])
                scopeContRowHidden['Escalation_Price'] = '0'
            scopeContRowHidden.Calculate()
        scopeContHidden.Calculate()

    x = Product.Attr("SC_GN_AT_RC_Selection").SelectedValues
    if scopeContHidden.Rows.Count:
        for row in scopeContHidden.Rows:
            for i in x:
                if i.Display == row["Comments"]:
                    scopeContRow = scopeCont.AddNewRow(False)
                    scopeContRow['Service_Product'] = row['Service_Product']
                    scopeContRow['Asset'] = row['Asset']
                    scopeContRow['Model'] = row['Model']
                    scopeContRow['Description'] = row['Description']
                    scopeContRow['PY_Quantity'] = row['PY_Quantity']
                    scopeContRow['Renewal_Quantity'] = row['Renewal_Quantity']
                    scopeContRow['PY_ListPrice'] = row['PY_ListPrice']
                    scopeContRow['CY_ListPrice'] = row['CY_ListPrice']
                    scopeContRow['HW_UnitPrice'] = row['HW_UnitPrice']
                    scopeContRow['PY_CostPrice'] = row['PY_CostPrice']
                    scopeContRow['CY_CostPrice'] = row['CY_CostPrice']
                    scopeContRow['SR_Quantity'] = row['SR_Quantity']
                    scopeContRow['SA_Quantity'] = row['SA_Quantity']
                    scopeContRow['Comments'] = row['Comments']
                    scopeContRow.Calculate()
        scopeCont.Calculate()