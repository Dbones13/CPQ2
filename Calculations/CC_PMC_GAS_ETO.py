if Session["prevent_execution"] != "true" and Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true' and Quote.GetCustomField('Booking LOB').Content == "PMC":
    for item in Quote.Items:
        is_synced = SqlHelper.GetFirst("select 1 from Products where IsSyncedFromBackOffice = 'True' and IsSimple = 'False' and product_catalog_code = '{}'".format(item.PartNumber))
        gas_eto_price = float(item.QI_GAS_ETO_PRICE_ADD.Value)
        if is_synced and gas_eto_price >0.0:
            pf_res = SqlHelper.GetFirst("select family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS(NOLOCK) where PartNumber = '{}'".format(item.PartNumber))
            if pf_res:
                item.QI_NetPrice_With_ETO.Value = item.ExtendedAmount+(item.QI_GAS_ETO_PRICE_ADD.Value*item.Quantity) if pf_res.family_code in ('Gas Products', 'Elster Product', 'Field Instruments') else item.ExtendedAmount
