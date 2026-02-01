from GS_Validate_Product_Type import IsVCitem

def ExtendedETOCal(Quote, Item):
    Item.QI_REGIONAL_ETO_COST.Value = Item.QI_ETO_COST.Value * Item.Quantity
    Item.QI_TOTAL_COST.Value = Item.QI_ETO_COST.Value + Item.QI_SAP_UnitCost.Value
    Item.QI_TOTAL_EXTENDED_COST.Value = Item.QI_TOTAL_COST.Value * Item.Quantity
    if Item.QI_SAP_UnitCost.Value != 0:
        Item.Cost = Item.QI_SAP_UnitCost.Value
        Item.ExtendedCost = Item.QI_SAP_UnitCost.Value * Item.Quantity
    if Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true':
        #from GS_Validate_Product_Type import IsVCitem
        if IsVCitem( Item.PartNumber)==True:
            if float(Item.Yspec_Add.Value) > 0.0:
                Item.ListPrice = Item.Yspec_Add.Value
            if float(Item.QI_GAS_ETO_PRICE_ADD.Value) > 0.0 or float(Item.QI_ETO_PMC_Price_Add.Value) > 0.0:
                pf_res = SqlHelper.GetFirst("select PartNumber,family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS where PartNumber = '{}'".format(Item.PartNumber))
                if pf_res is not None:
                    if pf_res.family_code in ('Gas Products', 'Elster Product', 'Field Instruments'):#CXCPQ-42168: Gas ETO cannot be discounted. Business asked to update ETO price to the Net price
                        Item.QI_NetPrice_With_ETO.Value = Item.ExtendedAmount+(Item.QI_GAS_ETO_PRICE_ADD.Value*Item.Quantity)
                    else: #Other ETO products can be discounted.
                        Item.ListPrice = Item.QI_ETO_PMC_Price_Add.Value
                        Item.QI_NetPrice_With_ETO.Value= Item.NetPrice
            #if float(Item.QI_AceQuote_ListPrice.Value) > 0.0:
            #    Item.ListPrice = Item.QI_AceQuote_ListPrice.Value
            if Item.QI_Parent_Generic_system_GUID.Value!='':
                Item.ListPrice = 0
        if Quote.GetCustomField('CF_Plant_Prevent_Calc').Content == 'true':
            Quote.GetCustomField('CF_Plant_Prevent_Calc').Content = ''