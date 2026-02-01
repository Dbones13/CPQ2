if Quote.GetCustomField("CF_Plant_Prevent_Calc").Content != 'true' and Quote.GetGlobal('PerformanceUpload') != 'Yes':
    #CC_LP_YSPEC_ADD
    BookingLob = Quote.GetCustomField("Booking LOB").Content
    if BookingLob == "PMC":
        product_query = "select 1 from Products where IsSyncedFromBackOffice = 'True' and IsSimple = 'False' and product_catalog_code = '{}'"
        if SqlHelper.GetFirst(product_query.format(Item.PartNumber)):
            yspec_add_value = float(Item.Yspec_Add.Value)
            if yspec_add_value > 0.0:
                Item.ListPrice = yspec_add_value
            eto_price_add_value = float(Item.QI_GAS_ETO_PRICE_ADD.Value)
            pmc_price_add_value = float(Item.QI_ETO_PMC_Price_Add.Value)
            if eto_price_add_value > 0.0 or pmc_price_add_value > 0.0:
                family_code_query = "select family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS(NOLOCK) where PartNumber = '{}'"
                pf_res = SqlHelper.GetFirst(family_code_query.format(Item.PartNumber))
                if pf_res.family_code in ('Gas Products', 'Elster Product','Field Instruments'):
                    Item.QI_NetPrice_With_ETO.Value = Item.ExtendedAmount + (eto_price_add_value * Item.Quantity)
                else:
                    Item.ListPrice = pmc_price_add_value
                    Item.QI_NetPrice_With_ETO.Value = Item.NetPrice
            ace_quote_list_price_value = float(Item.QI_AceQuote_ListPrice.Value)
            if ace_quote_list_price_value > 0.0:
                Item.ListPrice = ace_quote_list_price_value
            if Item.QI_Parent_Generic_system_GUID.Value:
                Item.ListPrice = 0

    # CC_UpdateListPrice
    import GS_ItemCalculations as icUtil
    from GS_CommonConfig import CL_CommonSettings as CS
    from GS_ITEMCREATE_UPDATE_Functions import loadwtwfactor
    wtwcostfactor_dict,nonpricecont = loadwtwfactor(Quote)
    Quotetype = Quote.GetCustomField("Quote Type").Content

    icUtil.CalculateListPrice(Quote , Item,nonpricecont, TagParserQuote,Session)
    # if not Item.IsLineItem and Item.PartNumber == "Write-in Site Support Labor":
        # opm_lp,sesp_lp,opm_dis,sesp_dis = 0,0,0,0
        # if Item.ProductName == "OPM":
            # opm_lp = (Item.ListPrice * 0.05)
            # opm_dis = Item.QI_MPA_Discount_Percent.Value
        # if Item.ProductName == "Non-SESP Exp Upgrade":
            # sesp_lp = (Item.ListPrice * 0.05)
            # sesp_dis = Item.QI_MPA_Discount_Percent.Value

        # opm_tot = opm_lp - (opm_lp * (opm_dis/100))
        # sesp_tot = sesp_lp - (sesp_lp * (sesp_dis/100))

        # writeIn_lp = opm_tot + sesp_tot
        # if Item.ProductName == "OPM":
            # for child in Item.Children:
                # if child.PartNumber == "Write-in Site Support Labor":
                    # child.ListPrice = writeIn_lp

    #CC_GetCost_Plant_Change
    #Get cost from SAP
    #import sys # Commented due to th error "Import of iron python built-in modules: "sys" on the line 2 is not allowed."
    import GS_Curr_ExchRate_Mod
    import re

    def removeQuoteMessages(Quote):
        pattern = r'^Cost for [\w\W]*? is either Zero or not defined in SAP[\w\W]*?Plant[^>]*?$|^Quote Currency [\w\W]*? and SAP Plant [\w\W]*? Cost Currency [\w\W]*? is different. Exchange Rate is missing in the Currency_ExchangeRate_Mapping table.$|^Error while Fetching the Cost from SAP for the material[\w\W]*?$'
        for i in list(Quote.Messages):
            if re.match(pattern, i):
                Quote.Messages.Remove(i)

    def getFloat(Var):
        if Var:
            return float(Var)
        return 0

    #Get host name from environment
    def getHost():
        hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME(NOLOCK) where Domain in (select tenant_name from tenant_environments(NOLOCK) where is_current_environment = 1)")
        if hostquery is not None:
            return hostquery.HostName
        return ''

    #Call API to fetch cost and assign to Quote Item fields
    def fn_getCost(host,p_Material,p_fme,p_plant):
        import GS_CostAPI_Module
        try:
            req_payload=GS_CostAPI_Module.gen_Item_PayLoad(Quote,p_Material,p_fme,p_plant)
            accessTkn = GS_CostAPI_Module.getAccessToken(host)
            CostAPIResp_Json = GS_CostAPI_Module.getCost(host, accessTkn,req_payload)
            lv_res=CostAPIResp_Json['vcMaterialCostResponse']['vcCostResponse']['item']
            for atnm in list(lv_res):
                if str(atnm["status"])!='E' and getFloat(atnm["totalCost"])>0:
                    #CXCPQ-59003 Added conversion logic when CPQ quote currency is different from the SAP Plant Currency code. 07/19/2023
                    if Quote.GetCustomField("Currency").Content==str(atnm["currency"]):
                        Item.Cost=getFloat(atnm["totalCost"])
                        Item.QI_SAP_UnitCost.Value=getFloat(atnm["totalCost"])
                        Item.QI_prev_plant_value.Value=Item.QI_Plant.Value
                    else:
                        lv_exrate=GS_Curr_ExchRate_Mod.fn_get_curr_exchrate(str(atnm["currency"]),Quote.GetCustomField("Currency").Content)
                        if lv_exrate!=0:
                            Item.Cost=getFloat(atnm["totalCost"]) * getFloat(lv_exrate)
                            Item.QI_SAP_UnitCost.Value=getFloat(atnm["totalCost"]) * getFloat(lv_exrate)
                            Item.QI_prev_plant_value.Value=Item.QI_Plant.Value
                        else:
                            Item.Cost=0
                            Item.QI_SAP_UnitCost.Value=0
                            # Quote.Messages.Clear()
                            removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
                            Quote.Messages.Add("Quote Currency " + Quote.GetCustomField("Currency").Content +" and SAP Plant "+str(Item.QI_Plant.Value)+ " Cost Currency "+ str(atnm["currency"]) + " is different. Exchange Rate is missing in the Currency_ExchangeRate_Mapping table.")
                else:
                    Item.Cost=0
                    Item.QI_SAP_UnitCost.Value=0
                    # Quote.Messages.Clear()
                    removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
                    Quote.Messages.Add("Cost for the "+ p_Material + ' is either Zero or not defined in SAP (Plant :'+str(Item.QI_Plant.Value)+')')
        except Exception as e:
            Item.Cost=0
            Item.QI_SAP_UnitCost.Value=0
            # Quote.Messages.Clear()
            removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
            Quote.Messages.Add("Error while Fetching the Cost from SAP for the material"+ p_Material)

            #Below logic runs only for PMC Parts & Spot Quote
    if Quote.GetCustomField("CF_Plant").Content!='' and Quote.GetCustomField("Quote Type").Content == 'Parts and Spot' and Quote.GetCustomField('Booking LOB').Content == "PMC":

        #Observed PMC writeIn products are created in SAP. Hence, adding extra condition to not to override writeIn cost via API
        writein_data = SqlHelper.GetFirst("SELECT Product FROM WRITEINPRODUCTS(NOLOCK) WHERE Product= '{}'".format(str(Item.PartNumber)))
        getprdid = SqlHelper.GetFirst("SELECT IsSyncedFromBackOffice from products(NOLOCK) where product_catalog_code= '{}' and IsSyncedFromBackOffice = 'True' and PRODUCT_ACTIVE = 1 ".format(str(Item.PartNumber)))
        if getprdid is not None and writein_data is None:
            if Item.QI_prev_plant_value.Value!=Item.QI_Plant.Value or Item.QI_SAP_UnitCost.Value==0:
                #call cost API only when there is plant change at Item level or when cost is zero.
                host=getHost()
                if Item.QI_Plant.Value=='':#Set only when Quote Item Plant is blank
                    Item.QI_Plant.Value=Quote.GetCustomField("CF_Plant").Content
                if host!='':
                    fn_getCost(host,Item.PartNumber,Item.QI_FME.Value,Item.QI_Plant.Value)
            else:
                if Item.QI_prev_plant_value.Value==Item.QI_Plant.Value and Item.QI_SAP_UnitCost.Value!=0:
                    #cost already fetched from SAP
                    Item.Cost=Item.QI_SAP_UnitCost.Value
                else:
                    Item.Cost=0
                    Item.QI_SAP_UnitCost.Value=0
                    # Quote.Messages.Clear()
                    removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
                    Quote.Messages.Add('Cost for material '+ p_Material + ' is either Zero or not defined in SAP (Plant :'+str(Item.QI_Plant.Value)+'). Please consider different Plant.')

    #Get VC cost from SAP for Project Type Quote CXCPQ-59003 & CXCPQ-66622
    if Quote.GetCustomField("Quote Type").Content == 'Projects' and SqlHelper.GetFirst("select 1 from Products where IsSyncedFromBackOffice = 'True' and IsSimple = 'False' and product_catalog_code = '{}'".format(Item.PartNumber)):
        qplant=None
        if Item.ProductName=='Generic System Child Product' and Item.QI_FME.Value!='': # For Generic system
            qplant = SqlHelper.GetFirst("select PLANT_CODE,PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING(NOLOCK)  where PRODUCT_NAME='{}'".format(Item.ProductName))
        else:
            qVFD = SqlHelper.GetFirst("select VFD_VC_Model from VFD_VC_MODELS(NOLOCK)  where VFD_VC_Model='{}'".format(Item.PartNumber))
            if qVFD is not None: #VFD Materials
                qplant = SqlHelper.GetFirst("select PLANT_CODE,PLANT_NAME from COUNTRY_SORG_PLANT_MAPPING(NOLOCK)  where PART_NUMBER='{}'".format(Item.PartNumber))
        if qplant is not None:
            if Item.QI_SAP_UnitCost.Value==0:
                host=getHost()
                if host!='' and qplant.PLANT_NAME!='':
                    fn_getCost(host,Item.PartNumber,Item.QI_FME.Value,qplant.PLANT_NAME)
            else:
                if Item.QI_SAP_UnitCost.Value!=0:
                    #cost already fetched from SAP
                    Item.Cost=Item.QI_SAP_UnitCost.Value
                else:
                    Item.Cost=0
                    Item.QI_SAP_UnitCost.Value=0
                    # Quote.Messages.Clear()
                    removeQuoteMessages(Quote) # CXCPQ-78401: Added on 28/02/2024
                    Quote.Messages.Add('Cost for material '+ p_Material + ' is either Zero or not defined in SAP (Plant :'+str(Item.QI_Plant.Value)+'). Please consider different Plant.')
        else:
            Trace.Write('Plant is not defined for the VC Material:'+str(Item.PartNumber))

    #CC_CalculateCostFields
    #CXCPQ-65110: Added condition to improve the performance. calculateCosts not required to run for PMC Parts and Spot Quote and for VC products defined in FME_PARTS table.
    if Item.ProductName in ['HCI Labor Upload', 'HCI Labor Config','PHD Labor','Uniformance Insight Labor','AFM Labor']:
        CS.setdefaultvalue["LaborParentGuid"]= Item.QuoteItemGuid
    if (BookingLob != "PMC" or Quotetype != "Parts and Spot") and Quotetype not in ('Contract New','Contract Renewal') and (CS.setdefaultvalue.get("LaborParentGuid",'0')!= Item.ParentItemGuid):
        if Item.ProductName!='Productized Skid Quote Item': #For productized skid Items cost is fetched from SAP
            qry = SqlHelper.GetFirst("SELECT 1 as flag from FME_PARTS WHERE PARTNUMBER = '{}'".format(str(Item.PartNumber)))
            if qry is None: #	CXCPQ-69436: Added Qry condition to avoid conflict with  K&E VC materials
                icUtil.calculateCosts(Quote , BookingLob, Quotetype, Item,wtwcostfactor_dict,nonpricecont, TagParserQuote)

    #CXCPQ-80164 : [PMC] Unit WTW cost should be equal to Unit Regional Cost at Quote Line items
    elif (BookingLob == "PMC" and Quotetype == "Parts and Spot"):
        icUtil.calculateCosts(Quote , BookingLob, Quotetype, Item,wtwcostfactor_dict,nonpricecont, TagParserQuote)

    Item.ExtendedCost = Item.Quantity * Item.Cost
    # CC_CalculateDiscountPercent
    # icUtil.calculateItemDiscountFromPercent(Quote , Item)

    # if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
        # ItemValues = dict([(val.Name, val.Values[0].Display) for val in Item.SelectedAttributes if val.Name in ('SC_ItemEditFlag','SC_Item_MarginPercent','SC_Item_BlockDiscount','SC_Item_Cost','SC_Item_CostStatus')])
        # if 'SC_Item_CostStatus' in ItemValues and ItemValues['SC_Item_CostStatus'] == '1':
            # Item.QI_SC_Cost.Value = ItemValues['SC_Item_Cost'] if Item.QI_SC_Product_ListPrice.Value == Item.ListPrice or Item.QI_SC_Product_ListPrice.Value == 0 else Item.ListPrice/Item.QI_SC_Product_ListPrice.Value * float(ItemValues['SC_Item_Cost'])
            # if Item.ListPrice-Item.DiscountAmount > 0:
               # Item.QI_SC_Margin_Percent.Value = (1-Item.QI_SC_Cost.Value/(Item.ListPrice-Item.DiscountAmount))*100
            # else:
                # Item.QI_SC_Margin_Percent.Value = 0
        # else:
            # Item.QI_SC_Cost.Value = (1-Item.QI_SC_Margin_Percent.Value/100)*(Item.ListPrice-Item.DiscountAmount)

    #CC_PMC_GAS_ETO
    if Quote.GetCustomField('Booking LOB').Content == "PMC":
        if SqlHelper.GetFirst("select 1 from Products where IsSyncedFromBackOffice = 'True' and IsSimple = 'False' and product_catalog_code = '{}'".format(Item.PartNumber)):
            if float(Item.QI_GAS_ETO_PRICE_ADD.Value) > 0.0:
                pf_res = SqlHelper.GetFirst("select PartNumber,family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS(NOLOCK) where PartNumber = '{}'".format(Item.PartNumber))
                if pf_res is not None:
                    if pf_res.family_code in ('Gas Products', 'Elster Product', 'Field Instruments'):#CXCPQ-42168: Gas ETO cannot be discounted. Business asked to update ETO price to the Net price
                        Item.QI_NetPrice_With_ETO.Value = Item.ExtendedAmount+(Item.QI_GAS_ETO_PRICE_ADD.Value*Item.Quantity)
            else:
                Item.QI_NetPrice_With_ETO.Value = Item.ExtendedAmount