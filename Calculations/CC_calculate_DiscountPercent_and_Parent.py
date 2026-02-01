if Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true' and Quote.GetGlobal('PerformanceUpload') != 'Yes':
    # import GS_ItemCalculations as icUtil
    import GS_CalculateTotals as tcUtil
    from GS_HCI_WRITEIN_HW_SW import HCISoftwareWriteInCalc
    hcpcartDict = {}
    labitm_guid =Session['HCI_Labor_Guid'] or []
    from GS_CommonConfig import CL_CommonSettings as CS
    for Item in Quote.Items:
        #if Quote.GetCustomField("Booking LOB").Content == "HCP":
        if Item.ProductName == 'HCI Labor Upload':
            CS.setdefaultvalue["LaborParentGuid"]=Item.QuoteItemGuid
        if Item.ProductName == 'Honeywell Enterprise Data Management':
            hcpcartDict = HCISoftwareWriteInCalc(Quote, Item, hcpcartDict)
        if len(hcpcartDict)>0:
            cartValues = hcpcartDict.get(Item.PartNumber)
            if cartValues:
                Item.QI_Target_Sell_Price.Value = Item.ListPrice = float(cartValues['UnitListPrice'])
                Item.Cost = float(cartValues['UnitRegionalCost'])
                Item.QI_TOTAL_COST.Value = Item.QI_TOTAL_EXTENDED_COST.Value = float(cartValues['UnitRegionalCost'])
                Item.Quantity =  cartValues['QTY']
                Item.Description = cartValues.get('Description')
                Item['QI_FoWTWCost'].Value = (float(Item.Cost)/(1+float(cartValues['W2WCost'])))
                Item['QI_UnitWTWCost'].Value = (float(Item.Cost)/(1+float(cartValues['W2WCost'])))
                Item.QI_ExtendedWTWCost.Value = float(Item['QI_UnitWTWCost'].Value)*Item.Quantity
                Item.QI_ProductLine.Value = cartValues.get('ProductLine','')
                Item.QI_ProductLineDesc.Value = Item.QI_PLSGDesc.Value = cartValues.get('PLSGDesc','')
                Item.QI_ProductCostCategory.Value = cartValues.get('CostCategory','')
                Item.QI_PLSG.Value = cartValues.get('PLSG','')
        if Session['LaborPricesDict'] and Item.QuoteItemGuid in labitm_guid:
            pricesDictval = eval(Session['LaborPricesDict'])
            # Trace.Write('Updating HCI Labor prices '+str(pricesDictval))
            pricesDict = pricesDictval.get(Item.PartNumber)
            if pricesDict:
                Item.QI_GESRegionalCost.Value = Item.Cost = float(pricesDict.get("RegionalCost",0))
                # Trace.Write(str(pricesDict.get("RegionalCost"))+'--Item.Cost--'+str(Item.Cost))
                Item.QI_FoWTWCost.Value = Item['QI_UnitWTWCost'].Value = float(pricesDict.get("WTWCost",0))
                Item.QI_ExtendedWTWCost.Value = float(Item['QI_UnitWTWCost'].Value)*Item.Quantity
                Item.ListPrice = float(pricesDict.get("UnitListPrice",0))
        if Item.ProductSystemId != 'Write-In_Tariff_cpq':
            #Trace.Write("lisprice"+str(Item.ListPrice)+"quantity"+str(Item.Quantity))
            Item.ExtendedListPrice = Item.ListPrice * Item.Quantity
            Item.ExtendedCost = Item.Cost * Item.Quantity
            #CXCPQ-109001 - Start (This is added since performance changes are not moved related to reprice action)
            Item.QI_TOTAL_COST.Value = Item.QI_ETO_COST.Value + Item.Cost
            Item.QI_TOTAL_EXTENDED_COST.Value = Item.QI_TOTAL_COST.Value * Item.Quantity
            Item.NetPrice = Item.ListPrice * (1 - Item.DiscountPercent / 100)
            Item.ExtendedAmount = Item.NetPrice * Item.Quantity
            Item.QI_Target_Sell_Price.Value = Item.ExtendedListPrice - float(Item.QI_MPA_Discount_Amount.Value)
            if Item.QI_Tariff_PCT.Value:
                Item.QI_Tariff_Amount.Value = (Item.ExtendedAmount * Item.QI_Tariff_PCT.Value)/100
            else:
                Item.QI_Tariff_Amount.Value=0.00
            #Item.QI_Sell_Price_Inc_Tariff.Value = Item.ExtendedAmount + Item.QI_Tariff_Amount.Value
            Item["QI_RegionalMargin"].Value = Item.ExtendedAmount - Item.QI_TOTAL_EXTENDED_COST.Value
            Item["QI_WTWMargin"].Value = Item.ExtendedAmount - Item["QI_ExtendedWTWCost"].Value
            if Item.ExtendedAmount != 0:
                Item["QI_RegionalMarginPercent"].Value = (Item.QI_RegionalMargin.Value/Item.ExtendedAmount) * 100
                Item["QI_WTWMarginPercent"].Value = (Item["QI_WTWMargin"].Value / Item.ExtendedAmount) * 100
            #CXCPQ-109001 - End
        else:
            Trace.Write('Write-IN tariff encountered!!!!!!!!!!!!!!!!!!!!'+str(Item.ExtendedCost)+'    '+str(Item.ExtendedAmount))
        #This is used to appned the Write-In_Tariff_cpq to the going sell price value to match the toatl sell price
        Item.QI_Sell_Price_Inc_Tariff.Value = Item.ExtendedAmount + Item.QI_Tariff_Amount.Value
        #Moved it here from CC_QICF_Calc since Extended Amount is calculated here
        Item.QI_LineTotal.Value = float(Item.ExtendedAmount) + float(Item.QI_Expedite_Fees.Value)
    tcUtil.calculateParent(Quote)
    '''icUtil.calculateItemDiscountFromPercent(Quote , Item)
    if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
        ItemValues = dict([(val.Name, val.Values[0].Display) for val in Item.SelectedAttributes if val.Name in ('SC_ItemEditFlag','SC_Item_MarginPercent','SC_Item_BlockDiscount','SC_Item_Cost','SC_Item_CostStatus')])
        if 'SC_Item_CostStatus' in ItemValues and ItemValues['SC_Item_CostStatus'] == '1':
            Item.QI_SC_Cost.Value = ItemValues['SC_Item_Cost'] if Item.QI_SC_Product_ListPrice.Value == Item.ListPrice or Item.QI_SC_Product_ListPrice.Value == 0 else Item.ListPrice/Item.QI_SC_Product_ListPrice.Value * float(ItemValues['SC_Item_Cost'])
            if Item.ListPrice-Item.DiscountAmount > 0:
                Item.QI_SC_Margin_Percent.Value = (1-Item.QI_SC_Cost.Value/(Item.ListPrice-Item.DiscountAmount))*100
            else:
                Item.QI_SC_Margin_Percent.Value = 0
        else:
            Item.QI_SC_Cost.Value = (1-Item.QI_SC_Margin_Percent.Value/100)*(Item.ListPrice-Item.DiscountAmount)'''



    # tcUtil.calculateParent(Quote)
    # Quote.Save(False)
    #Quote.Calculate()