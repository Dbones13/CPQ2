def calculate_products_data(Quote,coo_map,markup_rates,tariff_details):
    # coo_list = SqlHelper.GetList("SELECT TP.COO, TP.PART_NUMBER FROM HPS_Tariff_Products_COO as TP join CART_ITEM as CI on TP.PART_NUMBER = CI.CATALOGCODE where CI.CART_ID = '"+str(Quote.QuoteId)+"'")
    # coo_map = {c.PART_NUMBER: c.COO for c in coo_list}

    #tariff_details = SqlHelper.GetList('select COO,TARIFF_COST_PER,TARIFF_LIST_PER from HPS_TARIFF_DETAILS where SHIP_TO = ''+booking_country+''')
    tariff_map = {t.COO: t for t in tariff_details}

    #markup_rates = SqlHelper.GetList('select MARKUP_RATE,PLSG from HPS_TARIFF_PLSG_MARKUP_RATE as TP join CARTITEMCUSTOMFIELDS as CIC on TP.PLSG=CIC.QI_PLSG where CIC.CART_ID = ''+str(Quote.QuoteId)+''')
    markup_rate_map = {v.PLSG: v.MARKUP_RATE for v in markup_rates}
    total_list_price = 0.00
    total_cost = 0.00
    
    for item in Quote.MainItems:
        part_number = item.PartNumber
        coo = coo_map.get(part_number)
        Trace.Write('COO: '+str(coo))
        Trace.Write('Cost tariff '+str(total_cost)+'  '+str(item.PartNumber))
        if coo and coo in tariff_map:
            tariff = tariff_map[coo]
            cost_per = tariff.TARIFF_COST_PER
            list_per = tariff.TARIFF_LIST_PER

            product_line = item['QI_PLSG'].Value
            markup_rate = markup_rate_map.get(product_line, 0)

            item.QI_Cost_Tariff_Amount.Value = item.QI_ExtendedWTWCost.Value * cost_per / 100
            Trace.Write('Cost Tariff: '+str(item.QI_Cost_Tariff_Amount.Value)+'   '+str(item.PartNumber)+'  '+str(cost_per))

            base_value = item.QI_ExtendedWTWCost.Value * (1 + markup_rate / 100)
            item.QI_Tariff_Amount.Value = base_value * list_per / 100
            Trace.Write('List Tariff: '+str(item.QI_Tariff_Amount.Value))
        
            total_list_price += float(item.QI_Tariff_Amount.Value or 0)
            total_cost += float(item.QI_Cost_Tariff_Amount.Value or 0)
        elif item.ProductName == 'TPC_Product':
            total_list_price += float(item.QI_Tariff_Amount.Value or 0)
            total_cost += float(item.QI_Cost_Tariff_Amount.Value or 0)
    return total_list_price, total_cost
        



def has_valid_tariff_product(Quote, booking_country):
    
    plsgs=SqlHelper.GetList('select MARKUP_RATE,PLSG from HPS_TARIFF_PLSG_MARKUP_RATE as TP join CARTITEMCUSTOMFIELDS as CIC on TP.PLSG=CIC.QI_PLSG where CIC.CART_ID = ''+str(Quote.QuoteId)+'' and CIC.userid=''+str(Quote.UserId)+''')
    valid_plsgs = {row.PLSG for row in plsgs}
    
    tariff_details = SqlHelper.GetList("SELECT COO,TARIFF_COST_PER,TARIFF_LIST_PER FROM HPS_TARIFF_DETAILS WHERE SHIP_TO = '"+booking_country+"'")
    valid_tariff_coos = {row.COO for row in tariff_details}

    coo_list = SqlHelper.GetList(
        "SELECT TP.COO, TP.PART_NUMBER FROM HPS_Tariff_Products_COO as TP join CART_ITEM as CI on TP.PART_NUMBER = CI.CATALOGCODE where CI.CART_ID = '"+str(Quote.QuoteId)+"' and CI.USERID='"+str(Quote.UserId)+"'"
    )
    coo_map = {c.PART_NUMBER: c.COO for c in coo_list}

    
    for item in Quote.MainItems:
        plsg = item.QI_PLSG.Value
        coo = coo_map.get(item.PartNumber)
        tpc_tariff = False
        if item.ProductName == 'TPC_Product' and item.QI_Tariff_Amount.Value > 0:
            tpc_tariff = True

        if (coo and valid_plsgs and plsg in valid_plsgs and coo in valid_tariff_coos) or tpc_tariff:
            Quote.Messages.Remove("Tariff is not applicable for any product in the cart")
            return True,coo_map,plsgs,tariff_details


    Quote.Messages.Add("Tariff is not applicable for any product in the cart")
    return False, [],[],[]


def add_write_in_tariff(Quote, ProductHelper):
    if not Quote.ContainsAnyProductByName('Write-In Tariff'):
        tariff_product = ProductHelper.CreateProduct('Write-In_Tariff_cpq')
        tariff_product.AddToQuote()

def delete_write_in_tariff_product(Quote):
    if Quote.ContainsAnyProductByName('Write-In Tariff'):
        writein_item_id = Quote.GetCustomField('WriteIn_Tariff_Rolled_Up_Value').Content
        Quote.GetItemByQuoteItem(writein_item_id).Delete()

def update_write_in_tariff_items(Quote,coo_map,markup_rates,tariff_details):
    tariff_data = SqlHelper.GetFirst("SELECT ProductLine, ProductLineDescription, ProductLineSubGroup, ProductLineSubGroupDescription, UnitofMeasure FROM WriteInProducts WHERE Product = 'Write-in Tariff'")
    
    for item in Quote.GetItemsByProductTypeSystemId('Write-In_cpq'):
        if item.ProductSystemId == 'Write-In_Tariff_cpq':
            item["QI_ProductLine"].Value = tariff_data.ProductLine
            item["QI_ProductLineDesc"].Value = tariff_data.ProductLineDescription
            item["QI_PLSG"].Value = tariff_data.ProductLineSubGroup
            item["QI_PLSGDesc"].Value = tariff_data.ProductLineSubGroupDescription
            item["QI_UoM"].Value = tariff_data.UnitofMeasure
            item["QI_No_Discount_Allowed"].Value = '0'
            Quote.GetCustomField('WriteIn_Tariff_Rolled_Up_Value').Content = str(item.RolledUpQuoteItem)
            item.ListPrice, item.Cost = calculate_products_data(Quote,coo_map,markup_rates,tariff_details)
            #item.ListPrice, item.Cost = calculate_price_data(Quote)
            item.ExtendedListPrice, item.ExtendedCost = (item.Quantity*item.ListPrice), (item.Quantity*item.Cost)
            item.NetPrice = item.ListPrice * (1 - item.DiscountPercent / 100)
            item.ExtendedAmount = item.NetPrice*item.Quantity
            query = SqlHelper.GetFirst("SELECT WTW_FACTOR from HPS_PLSG_WTW_FACTOR wtw JOIN WriteInProducts wrt on wrt.ProductLineSubGroup = wtw.PL_PLSG where wrt.Product = 'Write-In Tariff'")
            wtwFac =  query.WTW_FACTOR if query else 0
            cost = item.Cost
            wtwCost = cost / (1 + float(wtwFac)) if cost else 0.0
            item['QI_UnitWTWCost'].Value = wtwCost
            item['QI_ExtendedWTWCost'].Value = wtwCost * item.Quantity
            item['QI_RegionalMargin'].Value = (item.ExtendedAmount - item.ExtendedCost)
            item['QI_WTWMargin'].Value = (item.ExtendedAmount - item['QI_ExtendedWTWCost'].Value)
            if item.ExtendedAmount != 0:
                item['QI_RegionalMarginPercent'].Value = (item.ExtendedAmount - item.ExtendedCost)/item.ExtendedAmount * 100
                item['QI_WTWMarginPercent'].Value = (item.ExtendedAmount - item['QI_ExtendedWTWCost'].Value)/item.ExtendedAmount * 100
    Quote.Save(False)