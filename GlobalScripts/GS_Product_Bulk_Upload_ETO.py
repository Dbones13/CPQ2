from GS_GetPriceFromCPS import getPrice,getTariffPrice

class BulkProductUpload():
    def __init__(self, quote, pproduct, tag_parser, wrkbook):
        self.tagParserQuote = tag_parser
        self.quote = quote
        self.prduct = pproduct
        self.cells = wrkbook.GetSheet("Upload list VC models").Cells
        self.data = wrkbook.GetSheet("Upload list VC models").Cells.GetRange("A1","K999")
        self.TotalRows = self.cells.GetRowCount

        self.validPartsCon = self.prduct.GetContainerByName("PU_Valid_Parts")
        self.validPartsConfme = self.prduct.GetContainerByName("FME_Valid_Parts")
        self.invalidPartsCon = self.prduct.GetContainerByName("PU_InValid_Parts")
        self.yspecialCon = self.prduct.GetContainerByName("YSpecial_Suboption")

        for container in [self.validPartsCon, self.invalidPartsCon, self.validPartsConfme, self.yspecialCon]:
            container.Rows.Clear()
        self.product_upload()

    def GetPrice(self, catlogProducts):
        PriceData = dict()
        tariffData = []
        if self.quote.GetCustomField('Booking LOB').Content == 'PMC' and self.quote.GetCustomField('Quote Type').Content in ('Parts and Spot','Projects'):
            PriceData, tariffData = getTariffPrice(self.quote, PriceData, catlogProducts, self.tagParserQuote)
        else:
            PriceData = getPrice(self.quote, PriceData, catlogProducts, self.tagParserQuote)
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

    def cleanUnicode(value):
        return value.encode('unicode_escape').strip() if value else ""

    def product_upload(self):
        partsQty = dict()
        partList = []
        catlogProducts = []
        configurableProducts = []
        partsList = dict()

        '''partsList["1"] = {
                "part_Number": "HON213",
                "fme": "YHON213-A0-A-J-A-AAMAP-DB-EA0EB0-A-F-AKAKF-AAB0BB0-A0000A0-A,B",
                "Qty": 1,
                "desc": "",
                "acerefno": "ETO3",
                "acedesc": "SEA test",
                "adder": "ETO",
                "ace_listprice": "5560.8",
                "cost_price": "900",
                "labor_hours": "1"
            }
        partsList["2"] = {
                "part_Number": "STD820",
                "fme": "STD820-E1AS4AS-1-C-BHC-13C-B-30A7-FX,F1,FE,TP,PM-0000",
                "Qty": 1,
                "desc": "Tag-1",
                "acerefno": "YHON226P-ETO",
                "acedesc": "YHON226P Special paint",
                "adder": "Adder",
                "ace_listprice": "500",
                "cost_price": "200",
                "labor_hours": ""
            }

        partsQty["HON213"] = {
            "Qty": 1,
            "desc": ""
        }

        partsQty["STD820"] = {
            "Qty": 1,
            "desc": "Tag-1"
        }

        # Append part number to partList
        partList=["HON213", "STD820"]'''
        for i in range(1, self.TotalRows):
            part_Number = self.data[i, 1]
            Trace.Write("---script---part_Number----"+str(part_Number))
            if not part_Number or not self.data[i, 0]: continue
            desc = self.data[i, 3] if self.data[i, 3] else ""
            qty = int(self.data[i, 4]) if self.data[i, 4] else 0
            fme = self.data[i, 2] if self.data[i, 2] else ""
            aceno = self.data[i, 5] if self.data[i, 5] else ""
            acedes = self.data[i, 6] if self.data[i, 6] else ""
            adder = self.data[i, 7] if self.data[i, 7] else ""
            ace_listprice = self.data[i, 8] if self.data[i, 8] else ""
            cost = self.data[i, 9] if self.data[i, 9] else ""
            labor = self.data[i, 10] if self.data[i, 10] else ""
            Trace.Write(str(self.cells)+"---script--ree-->"+str(self.data))
            Trace.Write(str(desc)+"-->"+str(qty)+"---script---desc----"+str(aceno)+"-->"+str(acedes)+"-->"+str(ace_listprice)+"-->"+str(cost)+"-->"+str(self.data[i, 10])+"-->"+str(labor))
            partsList[self.data[i, 0]] = {
				"part_Number": part_Number,
                "fme": fme,
                "Qty": qty,
                "desc": desc,
                "acerefno": aceno,
                "acedesc": acedes,
                "adder": adder,
                "ace_listprice": ace_listprice,
                "cost_price": cost,
                "labor_hours": labor
            }
            partsQty[part_Number] = {
                "Qty": qty,
                "desc": desc
            }
            partList.append(part_Number)



        '''for i in range(1, self.TotalRows):
            part_Number = self.data[i, 1] #self.cleanUnicode(self.data[i, 1])
            if not part_Number or not self.data[i, 0]: continue  # Skip empty part numbers or quantity
            desc = self.data[i, 3] #self.cleanUnicode(self.data[i, 3])
            qty = int(self.data[i, 4]) if self.data[i, 4] else 0
            partsList[self.data[i, 0]] = {
                "part_Number": part_Number,
                "fme": self.data[i, 2],
                "Qty": qty,
                "desc": desc,
                "acerefno": self.data[i, 5],
                "acedesc": self.data[i, 6],
                "adder": self.data[i, 7],
                "ace_listprice": self.data[i, 8],
                "cost_price": self.data[i, 9],
                "labor_hours": self.data[i, 10]
            }

            partsQty[part_Number] = {
                "Qty": qty,
                "desc": desc
            }

            # Append part number to partList
            partList.append(part_Number)'''
        Trace.Write("--script---partList--->"+str(partList))
        query = ("SELECT distinct TOP 1000 PRODUCT_CATALOG_CODE,IsSimple, SalesText, COALESCE(vp.FAMILY_CODE, '') as FAMILY_CODE FROM PRODUCTS(nolock) A JOIN product_versions(nolock) B ON A.PRODUCT_ID = B.PRODUCT_ID left join HPS_PRODUCTS_MASTER hps on hps.PartNumber = A.PRODUCT_CATALOG_CODE left join PMC_GASETO_YSPEC_MARINE_PRODUCTS vp on vp.PartNumber = A.PRODUCT_CATALOG_CODE WHERE A.PRODUCT_ACTIVE = 'True' AND A.PRODUCT_CATALOG_CODE In ('{}') AND (B.version_end_date IS NULL  or B.version_end_date <= getdate())").format("','".join(partList))
        productCatalog = SqlHelper.GetList(query)

        if productCatalog:
            for product in productCatalog:
                if partsQty.get(product.PRODUCT_CATALOG_CODE):
                    partsQty[product.PRODUCT_CATALOG_CODE]["SalesText"] = product.SalesText or ''
                    if product.IsSimple == True:
                        catlogProducts.append(product.PRODUCT_CATALOG_CODE)
                    else:
                        configurableProducts.append(product.PRODUCT_CATALOG_CODE)

        lv_cps_price_dict,tariff_cps_price_dict,Invalidparts = self.GetPrice(catlogProducts) if catlogProducts else {}, {}, []
        if catlogProducts or configurableProducts:
            message = Translation.Get('message.uploadExcel.simple') #BS Modified -Start
            priceBookMessage = Translation.Get('message.uploadExcel.pricebook')
            for key in partsList:
                if partsList[key]["part_Number"] in lv_cps_price_dict:
                    if  partsList[key]["fme"]== "":
                        self.PopulateValidPartsCon(partsList[key]["part_Number"],partsList[key]["Qty"],lv_cps_price_dict[partsList[key]["part_Number"]],tariff_cps_price_dict.get(partsList[key]["part_Number"]),partsQty[partsList[key]["part_Number"]]["SalesText"],partsList[key]["desc"],partsList[key]["cost_price"])
                    else:
                        self.PopulateInValidCon(key, partsList[key]["part_Number"],partsList[key]["Qty"],"Simple Products cannot have Yspecial or FME code",partsQty[partsList[key]["part_Number"]]["SalesText"])
                elif partsList[key]["part_Number"] in configurableProducts:
                    if partsList[key]["fme"]:
                        self.PopulateValidPartsConfme(key,partsList[key]["part_Number"],partsList[key]["Qty"],partsList[key]["ace_listprice"],"",partsList[key]["fme"],partsList[key]["desc"],partsList[key]["acerefno"],partsList[key]["acedesc"],partsList[key]["cost_price"],partsList[key]["labor_hours"],partsList[key]["adder"])
                    else:
                        self.PopulateInValidCon(key,partsList[key]["part_Number"],partsList[key]["Qty"],"Invalid FME assigned to PartNumber","")
                elif partsList[key]["part_Number"] in Invalidparts:
                    self.PopulateInValidCon("",partsList[key]["part_Number"],partsQty[partsList[key]["part_Number"]]["Qty"],priceBookMessage,partsQty[partsList[key]["part_Number"]]["SalesText"])
                else:
                    self.PopulateInValidCon("",partsList[key]["part_Number"],partsQty[partsList[key]["part_Number"]]["Qty"],message,partsQty[partsList[key]["part_Number"]]["SalesText"])

        self.validPartsCon.MakeAllRowsSelected()




#Session["prevent_execution"] = ""
#obj = BulkProductUpload(Quote, Product, TagParserQuote, "")
