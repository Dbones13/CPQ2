from GS_ITEMCREATE_UPDATE_Functions import populateQuoteTableRow
def Add_ETO_QTable(Quote,item):
    Quote.SetGlobal('Eto_data_Lookedup', '')
    Quote.SetGlobal('Yspec_data_Lookedup', '')
    

    ETO_Row_CNT=''
    Trace.Write("G_ETO_json_Data---->"+str(Quote.GetGlobal('G_ETO_json_Data')))

    if str(Quote.GetGlobal('G_ETO_json_Data')) != "":#sets G_ETO_json_Data variable in GS_PMC_ETO_JsonData script
        ETO_json_Data = str(Quote.GetGlobal('G_ETO_json_Data'))
        Trace.Write('ETO_json_Data:' +ETO_json_Data)
        if str(Quote.GetGlobal('G_ETO_Row_CNT')) != "":
            ETO_Row_CNT = int(Quote.GetGlobal('G_ETO_Row_CNT'))
            Trace.Write('ETO_Row_CNT:' + str(ETO_Row_CNT))
        jsonObject = RestClient.DeserializeJson(ETO_json_Data)
        Trace.Write('json_Data length:' +str(len(jsonObject)))  
        #pf_res = SqlHelper.GetFirst("select PartNumber,ProductLineDesc,FamilyCode from HPS_PRODUCTS_MASTER where PartNumber = '{}'".format(str(item.PartNumber)))
        #CXCPQ-44061 Below function used to display ETO or Yspec table on product configurator. This script is called from header template. When a new Gas/Marine and Elster product is created, add the product to PMC_GASETO_YSPEC_MARINE_PRODUCTS table.
        pf_res = SqlHelper.GetFirst("select PartNumber,family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS where PartNumber = '{}'".format(item.PartNumber))
        if pf_res is not None:
            PMC_ETO_Selection = Quote.QuoteTables["PMC_ETO_Selection"]
            Qtble_data = SqlHelper.GetList("SELECT * FROM QT__PMC_ETO_Selection WHERE  PartNumber = '{}' AND cartid = '{}' AND CartItemGUID = '{}'".format(str(item.PartNumber),str(Quote.QuoteId),str(item.QuoteItemGuid)))
            for rw in Qtble_data:
                PMC_ETO_Selection.DeleteRow(rw.Id)
            PMC_ETO_Selection.Save()
            for i in range(ETO_Row_CNT):
                rowDict = {
                            'PartNumber' : item.PartNumber,
                            'ItemNumber' : item.RolledUpQuoteItem,
                            'ETO_Ref_No' : str(jsonObject.ETOSPEC[i].Customized_Special_Reference_Number),
                            'ETO_Proposal_Notes' : str(jsonObject.ETOSPEC[i].Customized_Special_Proposal_Notes),
                            'ETO_Production_Notes' : str(jsonObject.ETOSPEC[i].Customized_Special_Production_Notes),
                            'ETO_Manufacturing_Notes' : str(jsonObject.ETOSPEC[i].Customized_Special_Manufacturing_Notes),
                            'ETO_Price' : str(jsonObject.ETOSPEC[i].Customized_Special_Price),
                                'ETO_Cost' : str(jsonObject.ETOSPEC[i].Customized_ETO_Cost),
                            'CartItemGUID' : item.QuoteItemGuid,
                            'FME' : item.QI_FME.Value
                            }
                Trace.Write('ETO quote table GS_Add_ETO_QTable')
                populateQuoteTableRow(PMC_ETO_Selection , rowDict)
            PMC_ETO_Selection.Save()
            if pf_res.family_code=='Gas Products':
                # Gas ETO Price cannot be discounted.
                fetch_qt = SqlHelper.GetList("SELECT ETO_Price,ETO_Cost,ETO_Production_Notes,ETO_Proposal_Notes FROM QT__PMC_ETO_Selection(nolock) WHERE  PartNumber = '{}'  AND cartid = '{}' AND CartItemGUID = '{}'".format(str(item.PartNumber),str(Quote.QuoteId),str(item.QuoteItemGuid)))
                addonprice = 0.0
                cost = 0.0
                prop_notes = '' #added in CXCPQ-115107
                pr_notes = '' #added CXCPQ-115107
                if fetch_qt.Count>0:
                    for rw in fetch_qt:
                        if rw.ETO_Price!='':
                            chn = float(rw.ETO_Price)
                            addonprice += float(chn)
                        if rw.ETO_Cost!='':
                            cost += float(rw.ETO_Cost)
                        prop_notes += rw.ETO_Proposal_Notes+"
"
                        pr_notes += rw.ETO_Production_Notes+"
"
                item.QI_Special_Production_Notes.Value = pr_notes #added in CXCPQ-115107
                item.QI_Special_Proposal_Notes.Value = prop_notes #added CXCPQ-115107
                item.QI_GAS_ETO_PRICE_ADD.Value=addonprice
                item.QI_NetPrice_With_ETO.Value=item.NetPrice + addonprice
                item.QI_ETO_COST.Value=cost
                item.QI_REGIONAL_ETO_COST.Value=cost * item.Quantity
                item.QI_TOTAL_COST.Value = cost + item.Cost
                item.QI_TOTAL_EXTENDED_COST.Value = item.QI_TOTAL_COST.Value * item.Quantity
            if pf_res.family_code in ('Instrumentation','Elster Product'):
                # Marine ETO or Elster ETO 
                #CXCPQ-52824:Added Elster Product in if condition
                fetch_qt = SqlHelper.GetList("SELECT ETO_Price,ETO_Cost FROM QT__PMC_ETO_Selection(nolock) WHERE  PartNumber = '{}'  AND cartid = '{}' AND CartItemGUID = '{}'".format(str(item.PartNumber),str(Quote.QuoteId),str(item.QuoteItemGuid)))
                addonprice = 0.0
                cost = 0.0
                if fetch_qt.Count>0:
                    for rw in fetch_qt:
                        if rw.ETO_Price!='':
                            chn = float(rw.ETO_Price)
                            addonprice += float(chn)
                        if rw.ETO_Cost!='':
                            rowCost = float(rw.ETO_Cost)
                            cost += float(rowCost)
                item.QI_ETO_PMC_Price_Add.Value=item.ProductModelPrice+addonprice
                Trace.Write('--cost-->>'+str(cost))
                if pf_res.family_code == 'Elster Product':
                    item.QI_GAS_ETO_PRICE_ADD.Value=addonprice
                    item.QI_NetPrice_With_ETO.Value=item.NetPrice + addonprice
                    item.QI_ETO_COST.Value=cost
                    item.QI_REGIONAL_ETO_COST.Value=cost * item.Quantity
                    item.QI_TOTAL_COST.Value = cost + item.Cost
                    item.QI_TOTAL_EXTENDED_COST.Value = item.QI_TOTAL_COST.Value * item.Quantity
            '''if pf_res.family_code=='Field Instruments' and item.QI_FME.Value[0].upper() == "Y" and item.QI_FME.Value is not None:
                # To Add Yspec price for FP Yearly Speical Products. Yspecial_Selection table has list price in USD. Below logic also converts Yspec price from USD to Quote Currency.
                # FP Yearly yspecial
                fetch_qt = SqlHelper.GetList("SELECT LP_Part,Cost FROM QT__Yspecial_Selection(nolock) WHERE cartid = '{}' AND MainPart = '{}' AND CartItemGUID = '{}'".format(str(Quote.QuoteId),str(item.PartNumber),str(item.QuoteItemGuid)))
                addonprice = 0.0
                cost = 0.0
                if fetch_qt.Count>0:
                    for rw in fetch_qt:
                        chn = float(rw.LP_Part)
                        addonprice += float(chn)
                        if rw.Cost > 0:
                            cost = float(rw.Cost)
                cur_code = Quote.SelectedMarket.CurrencyCode
                rate = SqlHelper.GetFirst("SELECT Exchange_Rate FROM CURRENCY_EXCHANGERATE_MAPPING(nolock) WHERE From_Currency = 'USD' AND To_Currency = '{}'".format(cur_code))
                if rate:
                    rate_amt = rate.Exchange_Rate
                else:
                    rate_amt = 1
                item.Yspec_Add.Value = item.ProductModelPrice+(float(addonprice)*float(rate_amt))
                item.QI_GAS_ETO_PRICE_ADD.Value=addonprice
                item.QI_NetPrice_With_ETO.Value=item.NetPrice + addonprice
                item.QI_ETO_COST.Value=cost
                item.QI_REGIONAL_ETO_COST.Value=cost * item.Quantity
                item.QI_TOTAL_COST.Value = cost + item.Cost
                item.QI_TOTAL_EXTENDED_COST.Value = item.QI_TOTAL_COST.Value * item.Quantity

    if str(Quote.GetGlobal('G_yspec_json_data')) != "":#sets G_yspec_json_data variable in GS_Yspec_table script
        yspec_json_data = str(Quote.GetGlobal('G_yspec_json_data'))
        Trace.Write('yspec_json_data:' +yspec_json_data)
        if str(Quote.GetGlobal('G_yspec_row_cnt')) != "":
            yspec_row_cnt = int(Quote.GetGlobal('G_yspec_row_cnt'))
            Trace.Write('yspec_row_cnt:' + str(yspec_row_cnt))
        jsonObject = RestClient.DeserializeJson(yspec_json_data)
        Trace.Write('json_Data length:' +str(len(jsonObject)))
        PMC_Yspec_Selection = Quote.QuoteTables["Yspecial_Selection"]
        Qtble_data = SqlHelper.GetList("SELECT * FROM QT__Yspecial_Selection WHERE  MainPart = '{}' AND cartid = '{}' AND CartItemGUID = '{}'".format(str(item.PartNumber),str(Quote.QuoteId),str(item.QuoteItemGuid)))
        for rw in Qtble_data:
            PMC_Yspec_Selection.DeleteRow(rw.Id)
        PMC_Yspec_Selection.Save()
        for i in range(yspec_row_cnt):
            try:
                cost = int(jsonObject.YSPEC_info[i].Yspec_Cost_Price)
            except:
                cost = 0
            rowDict = {
                            'Yspecial_Quote' : str(jsonObject.YSPEC_info[i].Yearly_Yspec_Quote_Ref),
                            'LP_Part' : str(jsonObject.YSPEC_info[i].Yspec_Price),
                            'Sample_Model' : str(jsonObject.YSPEC_info[i].Yspec_SampleModel),
                            'Comments' : str(jsonObject.YSPEC_info[i].Yspec_Specifications),
                            'Y_Description' : str(jsonObject.YSPEC_info[i].Yspec_Short_Description),
                            'Cost':  cost,
                            'MainPart':str(item.PartNumber),
                            'ItemNumber':item.RolledUpQuoteItem,
                            'CartItemGUID':item.QuoteItemGuid
                            }
            Trace.Write('Yspec quote table GS_Add_ETO_QTable')  
            populateQuoteTableRow(PMC_Yspec_Selection , rowDict)
        PMC_Yspec_Selection.Save()
        Quote.SetGlobal('G_yspec_json_data', '')
        Quote.SetGlobal('G_yspec_row_cnt', '')

    if str(Quote.GetGlobal('BU_Yspecial')) != "":# sets BU_Yspecial attribute in "Product Bulk Upload" Configurable product.
        YSpecial_subopt = str(Quote.GetGlobal('BU_Yspecial'))
        Trace.Write("YSpecial_subopt----->" +YSpecial_subopt)  
        json_yspec = RestClient.DeserializeJson(YSpecial_subopt)
        Trace.Write(json_yspec)

        PMC_Yspec_Selection = Quote.QuoteTables["Yspecial_Selection"]
        for i in range(1,len(json_yspec)+1):
            Trace.Write("length---->"+str(len(json_yspec)))
            Trace.Write("yspecRef----->"+str(json_yspec[str(i)]["yspecRef"]))


            query = SqlHelper.GetFirst("select * from YSPECIAL  where Yspecial_Quote = '{}' and Sub_Option = '{}'".format(str(json_yspec[str(i)]["yspecRef"]),str(json_yspec[str(i)]["yspecSubopt"])))
            Trace.Write("Yspecial_Quote----->"+query.Yspecial_Quote)
            rowDict = {
                        'Yspecial_Quote' : str(query.Yspecial_Quote),
                        'Sub_Option' : str(query.Sub_Option),
                        'LP_Part' : str(query.LP_Part),
                        'Sample_Model' : str(query.Sample_Model),
                        'Comments' : str(query.Comments),
                        'Y_Description' : str(query.Y_Description),
                        'MainPart':str(item.PartNumber),
                        'ItemNumber':item.RolledUpQuoteItem,
                        'CartItemGUID':item.QuoteItemGuid
                        }
            populateQuoteTableRow(PMC_Yspec_Selection , rowDict)
        PMC_Yspec_Selection.Save()
        Quote.SetGlobal('BU_Yspecial','')
        '''
        
    if str(Quote.GetGlobal('BU_ETO')) != "": # sets BU_ETO attribute in "Product Bulk Upload" Configurable product.
        BU_ETO = str(Quote.GetGlobal('BU_ETO'))
        Trace.Write("BU_ETO----->" +BU_ETO)  
        json_eto = RestClient.DeserializeJson(BU_ETO)
        Trace.Write(json_eto)

        PMC_ETO_Selection = Quote.QuoteTables["PMC_ETO_Selection"]
        for i in range(1,len(json_eto)+1):
            Trace.Write("length---->"+str(len(json_eto)))
            Trace.Write("Eto_ref----->"+str(json_eto[str(i)]["Eto_ref"]))

            rowDict = {
                        'PartNumber' : item.PartNumber,
                        'ItemNumber' : item.RolledUpQuoteItem,
                        'ETO_Ref_No' : str(json_eto[str(i)]["Eto_ref"]),
                        'ETO_Proposal_Notes' : str(json_eto[str(i)]["proposal_notes"]),
                        'ETO_Production_Notes' : str(json_eto[str(i)]["production_notes"]),
                        'ETO_Manufacturing_Notes' : str(json_eto[str(i)]["manufacturing_notes"]),
                        'ETO_Price' : str(json_eto[str(i)]["net_price"]),
                        'CartItemGUID' : item.QuoteItemGuid,
                        'FME' : item.QI_FME.Value
                        }
            populateQuoteTableRow(PMC_ETO_Selection , rowDict)
        PMC_ETO_Selection.Save()
        Quote.SetGlobal('BU_ETO','')
