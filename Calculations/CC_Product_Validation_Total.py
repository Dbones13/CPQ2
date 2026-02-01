if Quote.GetGlobal('PerformanceUpload') != 'Yes':
    from GS_CommonConfig import CL_CommonSettings as CS

    def productValid():
        cyberparts = 0 #cyber
        PreRealseParts = []
        CS.setdefaultvalue["EGAP_Contigency_Costs_USD"]=0
        Quote.GetCustomField('WriteIn_Tariff_Rolled_Up_Value').Content = '0'
        for item in Quote.MainItems:
            if item["QI_CrossDistributionStatus"].Value == '05 PreRelease' and item.ProductName not in PreRealseParts:
                PreRealseParts.append(item.PartNumber)
            elif item.ProductName == "Cyber" and item.ProductTypeName != "Service Contract" and '.' not in item.RolledUpQuoteItem: #cyber
                Quote.GetCustomField('cyberProductPresent').Content = 'Yes'
            elif cyberparts == 0 and item.PartNumber in CS.cyberProductfromtable: #cyber
                cyberparts = 1
                Quote.GetCustomField('cyberparts').Content = 'Yes'
            elif item.PartNumber=="Write-In Contingency":
                CS.setdefaultvalue["EGAP_Contigency_Costs_USD"] +=item.ExtendedCost
            elif item.ProductSystemId == 'Write-In_Tariff_cpq' and Quote.GetCustomField('Booking Lob').Content in ["CCC", "LSS", "HCP", "PAS"] and Quote.OrderStatus.Id == 32:
                Quote.GetCustomField('WriteIn_Tariff_Rolled_Up_Value').Content = str(item.RolledUpQuoteItem)
            if Quote.GetCustomField('Booking LOB').Content == 'CCC':
                if str(item.QI_ProductCostCategory.Value) in ('Honeywell Material','Honeywell Software'):
                    if Quote.GetCustomField('Booking Country').Content.lower() == 'united states':
                        item.MrcEndUserExtendedAmount = float(item.QI_ExtendedWTWCost.Value) 
                    elif Quote.GetCustomField('Booking Country').Content.lower() == 'brazil':
                        item.MrcEndUserExtendedAmount = float(item.ExtendedAmount)*float(0.80)
                    else:
                        item.MrcEndUserExtendedAmount = float(item.ExtendedAmount)*float(0.85)
                else:
                    item.MrcEndUserExtendedAmount = item.ExtendedCost
                item.MrcChannelMarginAmount = item.MrcEndUserExtendedAmount/item.Quantity
                item.MrcExtendedAmount = (float(item.ExtendedAmount)-float(item.MrcEndUserExtendedAmount))
                if str(round(item.ExtendedAmount,2)) not in ('0','0.00','0.0'):
                    item.MrcDiscountPercent = ((float(item.ExtendedAmount)-float(item.MrcEndUserExtendedAmount))/float(item.ExtendedAmount))*100
        
        Quote.GetCustomField('EGAP_Contigency_Costs_USD').Content=str(CS.setdefaultvalue.get("EGAP_Contigency_Costs_USD")) if CS.setdefaultvalue["EGAP_Contigency_Costs_USD"] else ''
        if Quote.ContainsAnyProductByPartNumber('C200_Migration'):
            PreRealseParts.append('C200_Migration') 
        Quote.GetCustomField('Unreleased_partList').Content=str(list(set(PreRealseParts))) if len(PreRealseParts)>0 else ''

    # simple & cyber bundle products document - cyber
    Quote.GetCustomField('cyberparts').Content = ''
    Quote.GetCustomField('cyberProductPresent').Content = ''
    # simple & cyber bundle products document - cyber
    productValid()

    #Script to populate CF_MigrationYes
    if Quote.ContainsAnyProductByPartNumber('PRJT'):
        Quote.GetCustomField('CF_MigrationYes').Content = 'New / Expansion Project'
    if Quote.ContainsAnyProductByPartNumber('Migration') and Quote.ContainsAnyProductByPartNumber('PRJT'):
        Quote.GetCustomField('CF_MigrationYes').Content = 'Both'