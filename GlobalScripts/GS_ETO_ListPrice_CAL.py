def ETO_ListPrice_CAL(Quote,cartitem):
    pf_res = SqlHelper.GetFirst("select PartNumber,family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS where PartNumber = '{}'".format(cartitem.PartNumber))

    if pf_res is not None: # To Add ETO price for Gas and Marine(Instrumentation) Products
        if pf_res.family_code=='Gas Products':
            # Gas ETO Price cannot be discounted.
            fetch_qt = SqlHelper.GetList("SELECT ETO_Price,ETO_Cost FROM QT__PMC_ETO_Selection WHERE  PartNumber = '{}'  AND cartid = '{}' AND CartItemGUID = '{}'".format(str(cartitem.PartNumber),str(Quote.QuoteId),str(cartitem.QuoteItemGuid)))
            addonprice = 0.0
            cost = 0.0
            if fetch_qt.Count>0:
                for rw in fetch_qt:
                    if rw.ETO_Price!='':
                        chn = float(rw.ETO_Price)
                        addonprice += float(chn)
                    if rw.ETO_Cost!='':
                        cost += float(rw.ETO_Cost)
            elif fetch_qt.Count == 0  and cartitem.QI_ETO_COST.Value > 0:
                cost = cartitem.QI_ETO_COST.Value
            cartitem.QI_GAS_ETO_PRICE_ADD.Value=addonprice
            cartitem.QI_NetPrice_With_ETO.Value=cartitem.NetPrice + addonprice
            cartitem.QI_GAS_ETO_PRICE_ADD.Value=addonprice
            cartitem.QI_ETO_COST.Value=cost
            cartitem.QI_REGIONAL_ETO_COST.Value=cost * cartitem.Quantity
            cartitem.QI_TOTAL_COST.Value = cost + cartitem.Cost
            cartitem.QI_TOTAL_EXTENDED_COST.Value = cartitem.QI_TOTAL_COST.Value * cartitem.Quantity
        if pf_res.family_code in ('Instrumentation','Elster Product'):
            # Marine ETO or Elster ETO 
            #CXCPQ-52824:Added Elster Product in if condition
            fetch_qt = SqlHelper.GetList("SELECT ETO_Price,ETO_Cost FROM QT__PMC_ETO_Selection WHERE  PartNumber = '{}'  AND cartid = '{}' AND CartItemGUID = '{}'".format(str(cartitem.PartNumber),str(Quote.QuoteId),str(cartitem.QuoteItemGuid)))
            addonprice = 0.0
            cost = 0.0
            if fetch_qt.Count>0:
                for rw in fetch_qt:
                    if rw.ETO_Price!='':
                        chn = float(rw.ETO_Price)
                        addonprice += float(chn)
                    if rw.ETO_Cost!='':
                        cost = cost + float(rw.ETO_Cost)
            elif fetch_qt.Count == 0  and cartitem.QI_ETO_COST.Value > 0:
                cost = cartitem.QI_ETO_COST.Value
            cartitem.QI_ETO_PMC_Price_Add.Value=cartitem.ProductModelPrice+addonprice
            if pf_res.family_code == 'Elster Product':
                cartitem.QI_GAS_ETO_PRICE_ADD.Value=addonprice
                cartitem.QI_NetPrice_With_ETO.Value=cartitem.NetPrice + addonprice
                cartitem.QI_ETO_COST.Value=cost
                cartitem.QI_REGIONAL_ETO_COST.Value=cost * cartitem.Quantity
                cartitem.QI_TOTAL_COST.Value = cost + cartitem.Cost
                cartitem.QI_TOTAL_EXTENDED_COST.Value = cartitem.QI_TOTAL_COST.Value * cartitem.Quantity
        '''if pf_res.family_code=='Field Instruments' and cartitem.QI_FME.Value[0].upper() == "Y" and cartitem.QI_FME.Value is not None:
            # To Add Yspec price for FP Yearly Speical Products. Yspecial_Selection table has list price in USD. Below logic also converts Yspec price from USD to Quote Currency.
            # FP Yearly yspecial
            fetch_qt = SqlHelper.GetList("SELECT LP_Part,Cost FROM QT__Yspecial_Selection WHERE cartid = '{}' AND MainPart = '{}' AND CartItemGUID = '{}'".format(str(Quote.QuoteId),str(cartitem.PartNumber),str(cartitem.QuoteItemGuid)))
            addonprice = 0.0
            cost = 0.0
            if fetch_qt.Count>0:
                for rw in fetch_qt:
                    chn = float(rw.LP_Part)
                    addonprice += float(chn)
                    if rw.Cost!='':
                        cost += float(rw.Cost)
            cur_code = Quote.SelectedMarket.CurrencyCode
            rate = SqlHelper.GetFirst("SELECT Exchange_Rate FROM CURRENCY_EXCHANGERATE_MAPPING WHERE From_Currency = 'USD' AND To_Currency = '{}'".format(cur_code))
            rate_amt = rate.Exchange_Rate if rate else 1 #CXCPQ-90706, CXCPQ-90704
            cartitem.Yspec_Add.Value = cartitem.ProductModelPrice+(float(addonprice)*float(rate_amt))
            cartitem.QI_GAS_ETO_PRICE_ADD.Value=addonprice
            cartitem.QI_NetPrice_With_ETO.Value=cartitem.NetPrice + addonprice
            cartitem.QI_ETO_COST.Value=cost
            cartitem.QI_REGIONAL_ETO_COST.Value=cost * cartitem.Quantity
            cartitem.QI_TOTAL_COST.Value = cost + cartitem.Cost
            cartitem.QI_TOTAL_EXTENDED_COST.Value = cartitem.QI_TOTAL_COST.Value * cartitem.Quantity '''