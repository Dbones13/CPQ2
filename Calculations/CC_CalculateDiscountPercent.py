import GS_ItemCalculations as icUtil


icUtil.calculateItemDiscountFromPercent(Quote , Item)
if Item.ProductName=="TPC_Product":
    Quote.GetCustomField("SC_CF_RENEWAL_FLAG").Content == "1"
if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
    ItemValues = dict([(val.Name, val.Values[0].Display) for val in Item.SelectedAttributes if val.Name in ('SC_ItemEditFlag','SC_Item_MarginPercent','SC_Item_BlockDiscount','SC_Item_Cost','SC_Item_CostStatus')])
    if 'SC_Item_CostStatus' in ItemValues and ItemValues['SC_Item_CostStatus'] == '1':
        Item.QI_SC_Cost.Value = ItemValues['SC_Item_Cost'] if Item.QI_SC_Product_ListPrice.Value == Item.ListPrice or Item.QI_SC_Product_ListPrice.Value == 0 else Item.ListPrice/Item.QI_SC_Product_ListPrice.Value * float(ItemValues['SC_Item_Cost'])
        if Item.ListPrice-Item.DiscountAmount > 0: 
            Item.QI_SC_Margin_Percent.Value = (1-Item.QI_SC_Cost.Value/(Item.ListPrice-Item.DiscountAmount))*100
        else:
            Item.QI_SC_Margin_Percent.Value = 0
    else:
        Item.QI_SC_Cost.Value = (1-Item.QI_SC_Margin_Percent.Value/100)*(Item.ListPrice-Item.DiscountAmount)