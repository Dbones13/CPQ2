from GS_GetPriceFromCPS import getPrice,getTariffPrice
from GS_PrdUpldCommon import fnEscpUniode

class bulk_product_upload():
    def __init__(self, quote, pproduct, tag_parser, wrkbook):
        self.tagParserQuote = tag_parser
        self.quote = quote
        self.prduct = pproduct
        self.cells = wrkbook.GetSheet("Upload list VC models").Cells
        self.data = wrkbook.GetSheet("Upload list VC models").Cells.GetRange("A1","K999")
        self.TotalRows = self.cells.GetRowCount

        self.cells1 = wrkbook.GetSheet("Y-Special Suboption").Cells
        self.data1 = wrkbook.GetSheet("Y-Special Suboption").Cells.GetRange("A1","G999")
        self.TotalRows1 = self.cells1.GetRowCount

        self.validPartsCon = self.prduct.GetContainerByName("PU_Valid_Parts")
        self.validPartsConfme = self.prduct.GetContainerByName("FME_Valid_Parts")
        self.invalidPartsCon = self.prduct.GetContainerByName("PU_InValid_Parts")
        self.yspecialCon = self.prduct.GetContainerByName("YSpecial_Suboption")

        self.validPartsCon.Rows.Clear()
        self.invalidPartsCon.Rows.Clear()
        self.validPartsConfme.Rows.Clear()
        self.yspecialCon.Rows.Clear()
        self.product_upload()

    def GetPrice(self, catlogProducts):
        PriceData = dict()
        # Invalidparts = []
        tariffData = []
        if self.quote.GetCustomField('Booking LOB').Content == 'PMC' and self.quote.GetCustomField('Quote Type').Content in ('Parts and Spot','Projects'):
            PriceData,tariffData = getTariffPrice(self.quote, PriceData, catlogProducts, self.tagParserQuote)
        else:
            PriceData = getPrice(self.quote, PriceData, catlogProducts, self.tagParserQuote)
        Trace.Write("PriceData----->"+str(PriceData))
        Trace.Write("tariffData----->"+str(tariffData))
        # for part in catlogProducts:
        #     if part not in PriceData.keys():
        #         Invalidparts.append(part)
        Invalidparts = [ part for part in catlogProducts if part not in PriceData.keys() ]
        return PriceData,tariffData,Invalidparts


    def PopulateValidPartsCon(self, partNumber,quantity,Price,TariffPCT,salesText,extended_desc, cost_price):
        row = self.validPartsCon.AddNewRow(False)
        row["Part Number"]     = partNumber
        row["Quantity"]        = str(quantity)
        row["Unit List Price"] = str(Price)
        row["ERP Text"]        = salesText if salesText else ''
        row["ExtendedDescription"] = str(extended_desc)
        row["Unit Cost Price"] = str(cost_price)
        row['Tariff PCT'] = str(TariffPCT) if TariffPCT else ''

    def PopulateInValidCon(self,ID,partNumber,quantity,message,salesText):
        row = self.invalidPartsCon.AddNewRow(False)
        row["ID"]              = str(ID)
        row["Part Number"]     = partNumber
        row["Quantity"]        = str(quantity)
        row["ERP Text"]        = salesText if salesText else ''
        row["Message"]         = message

    def PopulateValidPartsConfme(self,id1,partNumber,quantity,Price,salesText,fme,extended_desc,acerefno,acedesc,cost_price,labor_hours,adder_total_ETO):
        row = self.validPartsConfme.AddNewRow(False)
        row["ID"] = str(id1)
        row["Part Number"]     = partNumber
        row["Quantity"]        = str(quantity)
        row["Unit List Price"] = str(Price)
        row["FME"] = str(fme)
        row["ExtendedDescription"] = str(extended_desc)
        row["ERP Text"]        = salesText if salesText else ''
        row["Ace Quote Reference Number"] = str(acerefno) if acerefno else ''
        row["Ace Quote Description"] = str(acedesc)
        row["Unit Cost Price"] = str(cost_price)
        row["Labor Hours"] = str(labor_hours)
        row['AdderTotalETO'] = str(adder_total_ETO)

    def PopulateYspecialCon(self,id2,yspec_quote_ref,yspec_subopt,proposal_notes,production_notes,manufacturing_notes,net_price,eto_yspec_marine):
        row = self.yspecialCon.AddNewRow(False)
        row["ID"] = str(id2)
        row["YSpecial_Quote_Ref"] = str(yspec_quote_ref)
        row["YSpecial_Suboption"] = str(yspec_subopt)
        row["ETO proposal notes"] = str(proposal_notes)
        row["ETO production notes"] = str(production_notes)
        row["ETO manufacturing notes"] = str(manufacturing_notes)
        row["ETO Nett Price"] = str(net_price)
        row["ETO_Marine_Yspec"] = str(eto_yspec_marine)

    def product_upload(self):
        partsQty = dict()
        partList = []
        catlogProducts = []
        configurableProducts = []
        allIds = dict()
        validID = []
        invalidID = []
        validParts = []
        lineItem2 = []
        validET0 = []
        #validMarine = [] #CXCPQ-53124: Commented
        CanAddProduct = True

        if self.quote.GetCustomField('Sales Area').Content == "1109":
            yspectable = "YSpecial_US"
        else:
            yspectable = "YSpecial"

        if CanAddProduct:
            sheet_data = fnEscpUniode(self.data,self.TotalRows,9)
            for i in range(1, self.TotalRows):
                id1= sheet_data[i,0].strip()
                part_Number = sheet_data[i,1].strip()
                if part_Number == "": continue
                fme = sheet_data[i,2].strip() if sheet_data[i,2].strip()!= "" else ""
                Qty = int(sheet_data[i,4]) if str(sheet_data[i,4]) != "" else 0
                extended_desc = sheet_data[i,3].strip()
                acerefno = sheet_data[i,5].strip()
                ace_listprice =self. data[i,7].strip()
                cost_price = sheet_data[i,8].strip()

                partList.append(part_Number)
                allIds[str(id1)] = {"part_Number" : part_Number, "fme" : fme, "Qty": Qty, "desc" : extended_desc, "acerefno" : acerefno, "ace_listprice" : ace_listprice, "cost_price" : cost_price}
                partsQty[part_Number] = {"Qty" : Qty,"desc" : extended_desc}
                
            query = ("SELECT distinct TOP 1000 PRODUCT_CATALOG_CODE,IsSimple, SalesText FROM PRODUCTS(nolock) A JOIN product_versions(nolock) B ON A.PRODUCT_ID = B.PRODUCT_ID left join HPS_PRODUCTS_MASTER hps on hps.PartNumber = A.PRODUCT_CATALOG_CODE WHERE A.PRODUCT_ACTIVE = 'True' AND A.PRODUCT_CATALOG_CODE In ('{}') AND (B.version_end_date IS NULL  or B.version_end_date <= getdate()) ").format("','".join(partList))
            productCatalog = SqlHelper.GetList(query)

            if productCatalog:
                for product in productCatalog:
                    if partsQty.get(product.PRODUCT_CATALOG_CODE):
                        partsQty[product.PRODUCT_CATALOG_CODE]["SalesText"] = product.SalesText
                        if product.IsSimple == True:
                            catlogProducts.append(product.PRODUCT_CATALOG_CODE)
                        else:
                            configurableProducts.append(product.PRODUCT_CATALOG_CODE)
            sheet_data1 = fnEscpUniode(self.data1,self.TotalRows,7)
            for i in range(1,self.TotalRows1):
                id2 = sheet_data1[i,0].strip()
                yspec_quote_ref = sheet_data1[i,1].strip()
                yspec_subopt = sheet_data1[i,2].strip()
                net_price = sheet_data1[i,6].strip()
                if allIds.get(id2):
                    if yspec_quote_ref != "" and yspec_subopt != "":
                        query2 = SqlHelper.GetList("Select Yspecial_Quote, Sub_Option from {}(nolock) where Part_Number = '{}'".format(str(yspectable),str(allIds[id2]["part_Number"])))
                        if len(query2) != 0:
                            for item in query2:
                                if item.Yspecial_Quote == yspec_quote_ref and item.Sub_Option == yspec_subopt:
                                    validID.append(id2)
                                    lineItem2.append(i)
                                else:
                                    invalidID.append(id2)
                        else:
                            invalidID.append(id2)
                            
                    elif (yspec_quote_ref != "" and net_price != "") and (str(allIds[id2]["part_Number"]) in configurableProducts) and (str(allIds[id2]["acerefno"]) == "" and str(allIds[id2]["ace_listprice"]) == ""):
                        eto_query = SqlHelper.GetFirst("Select FAMILY_CODE from PMC_GASETO_YSPEC_MARINE_PRODUCTS where PartNumber = '{}'".format(str(allIds[id2]["part_Number"])))
                        if eto_query is not None:
                            if eto_query.FAMILY_CODE == "Gas Products" or eto_query.FAMILY_CODE == "Instrumentation":
                                validET0.append(id2)
                                lineItem2.append(i)
                            #CXCPQ-53124:Start: Earlier there are two seperate quote tables for Gas and Marine ETO and now with this story it merged into one.    
                            ''''elif eto_query.FAMILY_CODE == "Instrumentation":
                                validMarine.append(id2)
                                lineItem2.append(i)'''
                            #CXCPQ-53124:End.
                        else:
                            invalidID.append(id2)

            '''query = ("SELECT distinct TOP 1000 PRODUCT_CATALOG_CODE,IsSimple, SalesText FROM PRODUCTS A JOIN product_versions B ON A.PRODUCT_ID = B.PRODUCT_ID left join HPS_PRODUCTS_MASTER hps on hps.PartNumber = A.PRODUCT_CATALOG_CODE WHERE A.PRODUCT_ACTIVE = 'True' AND A.PRODUCT_CATALOG_CODE In ('{}') AND (B.version_end_date IS NULL  or B.version_end_date <= getdate()) ").format("','".join(partList))
            productCatalog = SqlHelper.GetList(query)

                for product in productCatalog:
                    partsQty[product.PRODUCT_CATALOG_CODE]["SalesText"] = product.SalesText
                    if product.IsSimple == True:
                        ##Log.Info("Simple product----->")
                        catlogProducts.append(product.PRODUCT_CATALOG_CODE)
                    else:
                        ##Log.Info("configurable product----->")
                        configurableProducts.append(product.PRODUCT_CATALOG_CODE)'''
            if productCatalog:
                if catlogProducts:
                    message = Translation.Get('message.uploadExcel.simple') #BS Modified -Start
                    lv_cps_price_dict,tariff_cps_price_dict,Invalidparts = self.GetPrice(catlogProducts)
                    Trace.Write("lv_cps_price_dict----->"+str(lv_cps_price_dict))
                    #Trace.Write("allId's-->"+str(allIds))
                    #Trace.Write("InvalidId's-->"+str(invalidID))
                    if lv_cps_price_dict:
                        for key in allIds:
                            if allIds[key]["part_Number"] in lv_cps_price_dict:
                                if  allIds[key]["fme"]== "" and key not in invalidID:
                                    #Trace.Write("PartNumber--->"+str(allIds[key]["part_Number"]))
                                    self.PopulateValidPartsCon(allIds[key]["part_Number"],allIds[key]["Qty"],lv_cps_price_dict[allIds[key]["part_Number"]],tariff_cps_price_dict.get(allIds[key]["part_Number"]),partsQty[allIds[key]["part_Number"]]["SalesText"],allIds[key]["desc"],allIds[key]["cost_price"])
                                else:
                                    self.PopulateInValidCon(key, allIds[key]["part_Number"],allIds[key]["Qty"],"Simple Products cannot have Yspecial or FME code",partsQty[allIds[key]["part_Number"]]["SalesText"])
                    if Invalidparts:
                        message = Translation.Get('message.uploadExcel.pricebook')
                        for partNumber in Invalidparts:
                            if partNumber != "":
                                self.PopulateInValidCon("",partNumber,partsQty[partNumber]["Qty"],message,partsQty[partNumber]["SalesText"])

                # if configurableProducts:
                #     ##Log.Info("in configurable product----->"+str(configurableProducts))
                #     message = Translation.Get('message.uploadExcel.configurable')
                #     for partNumber in configurableProducts:
                #        #Log.Info("partnumber111--->"+str(partNumber))

            for i in range(1,self.TotalRows):
                id1 = sheet_data[i,0].strip()
                part_Number = sheet_data[i,1].strip()
                if str(sheet_data[i,4]) != '':
                    Qty = int(sheet_data[i,4])
                else:
                    Qty = 0
                message = ""
                SalesText = ""
                extended_desc = sheet_data[i,3].strip()

                if id1 not in invalidID or id1 in validID:
                    if sheet_data[i,1].strip() != "" and sheet_data[i,2].strip() != "" and sheet_data[i,4].strip() != "": #BS Modified condition
                        fme = sheet_data[i,2].strip()
                        #if (id1 in validID) or (id1 in validET0) or (id1 in validMarine):#CXCPQ-53124:Modified If condition 
                        if (id1 in validID) or (id1 in validET0):
                            if fme[0] != "Y":
                                fme = "Y"+fme
                        acerefno = sheet_data[i,5].strip()
                        acedesc = sheet_data[i,6].strip()
                        adder_total_ETO = sheet_data[i,7].strip()
                        ace_listprice = sheet_data[i,8].strip()
                        cost_price = sheet_data[i,9].strip()
                        labor_hours = sheet_data[i,10].strip()
                        self.PopulateValidPartsConfme(id1,part_Number,Qty,ace_listprice,SalesText,fme,extended_desc,acerefno,acedesc,cost_price,labor_hours,adder_total_ETO)
                elif allIds[id1]["part_Number"] not in catlogProducts and part_Number != "":
                    self.PopulateInValidCon(id1,part_Number,Qty,"Invalid Y-special,ETO or Yspecial-Marine assigned to PartNumber",SalesText)
                    '''if allIds[id1]["fme"][0:1] != "Y":
                        self.PopulateInValidCon(id1,part_Number,Qty,"Y-Prefix is needed to be a valid Yspecial,ETO or Yspecial-Marine",SalesText)
                    else:
                        self.PopulateInValidCon(id1,part_Number,Qty,"Invalid Y-special,ETO or Yspecial-Marine assigned to PartNumber",SalesText)'''

            #validPartsCon = pProduct.GetContainerByName("PU_Valid_Parts")
            for row in self.validPartsCon.Rows:
                row.IsSelected = True
            #validPartsCon.Calculate()

            message = Translation.Get('message.uploadExcel.catalog')
            for partNumber in partList:
                if partNumber not in catlogProducts and partNumber not in configurableProducts:
                    self.PopulateInValidCon("",partNumber,partsQty[partNumber]["Qty"],message,'')
        #ScriptExecutor.ExecuteGlobal('GS_FME_BULKUPLOAD_VALIDATE')
        for row in self.validPartsConfme.Rows:
            if row["Message"] == '<label style="color:green">Valid</label>':
                validParts.append(row["ID"])
        sheet_data1 = fnEscpUniode(self.data1,self.TotalRows,7)
        for i in range(1,self.TotalRows1):
            if i in lineItem2:
                id2_f = sheet_data1[i,0].strip()
                yspec_quote_ref_f = sheet_data1[i,1].strip()
                yspec_subopt_f = sheet_data1[i,2].strip()
                proposal_notes = sheet_data1[i,3].strip()
                production_notes = sheet_data1[i,4].strip()
                manufacturing_notes = sheet_data1[i,5].strip()
                net_price = sheet_data1[i,6].strip()
                if id2_f in validParts:
                    if id2_f in validID:
                        self.PopulateYspecialCon(id2_f,yspec_quote_ref_f,yspec_subopt_f,proposal_notes,production_notes,manufacturing_notes,net_price,"Yspecial")
                    elif id2_f in validET0:
                        self.PopulateYspecialCon(id2_f,yspec_quote_ref_f,yspec_subopt_f,proposal_notes,production_notes,manufacturing_notes,net_price,"ETO")
                    #CXCPQ-53124:Start
                    ''''elif id2_f in validMarine:
                        self.PopulateYspecialCon(id2_f,yspec_quote_ref_f,yspec_subopt_f,proposal_notes,production_notes,manufacturing_notes,net_price,"YspecMarine")'''
                    #CXCPQ-53124:End