if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
    firstMesMargin = None
    for item in Quote.MainItems:
        itemValues = dict([(val.Name, val.Values[0].Display) for val in item.SelectedAttributes if val.Name in ('SC_ItemEditFlag','SC_Item_MarginPercent','SC_Item_BlockDiscount','SC_Item_Cost','SC_Item_CostStatus')])
        if item.PartNumber == 'MES Models':
            if firstMesMargin:
                item.QI_SC_Margin_Percent.Value = firstMesMargin
                item.QI_SC_Cost.Value = (1-item.QI_SC_Margin_Percent.Value/100) * item.ExtendedAmount
            else:
                firstMesMargin = item.QI_SC_Margin_Percent.Value
                item.QI_SC_Cost.Value = (1-item.QI_SC_Margin_Percent.Value/100) * item.ExtendedAmount
        if item.PartNumber == 'Platform' or item.PartNumber == 'Entitlement':
            for citem in item.Children:
                if citem.PartNumber != 'Total Expense' and citem.PartNumber != 'Resource Type':
                    citem.QI_SC_Margin_Percent.Value = item.QI_SC_Margin_Percent.Value
        if 'SC_Item_CostStatus' in itemValues and itemValues['SC_Item_CostStatus'] == '1':
            #item.QI_SC_Cost.Value = itemValues['SC_Item_Cost']
            item.QI_SC_Margin_Percent.Value = (1-item.QI_SC_Cost.Value/item.ExtendedAmount)*100 if item.ExtendedAmount>0 else 0
        else:
            item.QI_SC_Cost.Value = (1-item.QI_SC_Margin_Percent.Value/100) * item.ExtendedAmount
    Quote.CustomFields.AssignValue('SC_CF_RENEWAL_FLAG',"0")