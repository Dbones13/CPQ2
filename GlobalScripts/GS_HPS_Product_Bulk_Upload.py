from GS_GetPriceFromCPS import getPrice
from GS_PrdUpldCommon import fnEscpUniode
#import GS_FME_CONFIG_MOD

class bulk_product_upload():
    
    #Initialization
    def __init__(self, quote, pproduct, tag_parser, wrkbook):
        self.tagParserQuote = tag_parser
        self.quote = quote
        self.prduct = pproduct
        self.cells = wrkbook.GetSheet("Upload list VC models").Cells
        self.data = wrkbook.GetSheet("Upload list VC models").Cells.GetRange("A1","I999")
        self.TotalRows = self.cells.GetRowCount

        self.validPartsCon = self.prduct.GetContainerByName("HPS_PU_Valid_Parts")
        self.validPartsConfme = self.prduct.GetContainerByName("HPS_Valid_Parts")
        self.invalidPartsCon = self.prduct.GetContainerByName("HPS_PU_Invalid_Parts")
        
        self.validPartsCon.Rows.Clear()
        self.invalidPartsCon.Rows.Clear()
        self.validPartsConfme.Rows.Clear()
        self.product_upload()

    #Get Price of products through CPS
    def GetPrice(self, catlogProducts):
        PriceData = dict()
        PriceData = getPrice(self.quote, PriceData, catlogProducts, self.tagParserQuote)
        Invalidparts = [ part for part in catlogProducts if part not in PriceData.keys() ]
        return PriceData,Invalidparts

    #Populates Non-FME Valid parts 
    def PopulateValidPartsCon(self, partNumber,quantity,Price,salesText):
        row = self.validPartsCon.AddNewRow(False)
        row["Part Number"]     = partNumber
        row["Quantity"]        = str(quantity)
        row["Unit List Price"] = str(Price)
        row["ERP Text"]        = salesText if salesText else ''
        
    #Populates Invalid parts
    def PopulateInValidCon(self,ID,partNumber,quantity,message,salesText):
        row = self.invalidPartsCon.AddNewRow(False)
        row["ID"]              = str(ID)
        row["Part Number"]     = partNumber
        row["Quantity"]        = str(quantity)
        row["ERP Text"]        = salesText if salesText else ''
        row["Message"]         = message

    #Populates FME Valid parts 
    def PopulateValidPartsConfme(self,id1,partNumber,quantity,Price,salesText,fme,extended_desc,cost_price):
        row = self.validPartsConfme.AddNewRow(False)
        row["ID"] = str(id1)
        row["Part Number"]     = partNumber
        row["Quantity"]        = str(quantity)
        row["Unit List Price"] = str(Price)
        row["FME"] = str(fme)
        row["ExtendedDescription"] = str(extended_desc)
        row["ERP Text"]        = salesText if salesText else ''
        #row["Unit Cost Price"] = str(cost_price)

    #Unpacks product data from excel file to respective containers
    def product_upload(self):
        partsQty = dict()
        partList = []
        catlogProducts = []
        configurableProducts = []
        allIds = dict()
        validParts = []
        CanAddProduct = True

        if CanAddProduct:
            #populate internal structure from excel records
            sheet_data = fnEscpUniode(self.data,self.TotalRows,4)
            for i in range(1, self.TotalRows):
                id1= sheet_data[i,0].strip()
                part_Number = sheet_data[i,1].strip()
                fme = sheet_data[i,2].strip() if sheet_data[i,2].strip()!= "" else ""
                Qty = int(sheet_data[i,3]) if str(sheet_data[i,3]) != "" else 0
                
                partList.append(part_Number)
                
                allIds[str(id1)] = {"part_Number" : part_Number, "fme" : fme, "Qty": Qty}
                partsQty[part_Number] = {"Qty" : Qty}

            #Get Product details from master database table    
            query = ("SELECT distinct TOP 1000 PRODUCT_CATALOG_CODE,IsSimple, SalesText FROM PRODUCTS(nolock) A JOIN product_versions(nolock) B ON A.PRODUCT_ID = B.PRODUCT_ID left join HPS_PRODUCTS_MASTER hps on hps.PartNumber = A.PRODUCT_CATALOG_CODE WHERE A.PRODUCT_ACTIVE = 'True' AND A.PRODUCT_CATALOG_CODE In ('{}') AND (B.version_end_date IS NULL  or B.version_end_date <= getdate()) ").format("','".join(partList))
            productCatalog = SqlHelper.GetList(query)
                        
            #segeregate products based on simple or configurable type 
            if productCatalog:
                for product in productCatalog:
                    partsQty[product.PRODUCT_CATALOG_CODE]["SalesText"] = product.SalesText
                    if product.IsSimple == True:
                        catlogProducts.append(product.PRODUCT_CATALOG_CODE)
                    else:
                        configurableProducts.append(product.PRODUCT_CATALOG_CODE)

            #populates valid parts/invalidparts container for simple products
            if catlogProducts:
                message = Translation.Get('message.uploadExcel.simple') 
                lv_cps_price_dict,Invalidparts = self.GetPrice(catlogProducts)
                if 1==1:#lv_cps_price_dict:
                    for key in allIds:
                        if allIds[key]["part_Number"] and (allIds[key]["part_Number"] in catlogProducts or allIds[key]["part_Number"] in configurableProducts):# in lv_cps_price_dict:
                            if  allIds[key]["fme"]== "":
                                self.PopulateValidPartsCon(allIds[key]["part_Number"],allIds[key]["Qty"],0,"")
								#self.PopulateValidPartsCon(allIds[key]["part_Number"],allIds[key]["Qty"],lv_cps_price_dict[allIds[key]["part_Number"]],partsQty[allIds[key]["part_Number"]]["SalesText"])
                            else:
								#self.PopulateInValidCon(key, allIds[key]["part_Number"],allIds[key]["Qty"],"Simple Products cannot have Yspecial or FME code",partsQty[allIds[key]["part_Number"]]["SalesText"])
                                prod =SqlHelper.GetFirst("select 1 from Products where IsSyncedFromBackOffice = 'True' and IsSimple = 'False' and product_catalog_code = '{}'".format(allIds[key]["part_Number"]))
                                if not prod:
									#Trace.Write("recheck--final-->"+str(allIds[key]["part_Number"]))
									self.PopulateInValidCon(key, allIds[key]["part_Number"],allIds[key]["Qty"],"Simple Products cannot have Yspecial or FME code","")
                """if Invalidparts:
                    message = Translation.Get('message.uploadExcel.pricebook')
                    for partNumber in Invalidparts:
                        InvpartID = [key for key, value in allIds.iteritems() if value["part_Number"] == partNumber]
                        if partNumber != "":
                            Trace.Write(str(partNumber)+"-------rechecking---1111--------->"+str(Invalidparts))
                            self.PopulateInValidCon(InvpartID[0],partNumber,partsQty[partNumber]["Qty"],message,partsQty[partNumber]["SalesText"]) """
            
            #Populates Valid parts/Invalid parts container for FME Products
            if configurableProducts:
                lv_cps_config_price_dict,Invalidconfigparts = self.GetPrice(configurableProducts)
                if 1==1:#lv_cps_config_price_dict:
                    extended_desc =''
                    cost_price = 0
                    for key in allIds:
                        if allIds[key]["part_Number"]:# in lv_cps_config_price_dict:
                            if  allIds[key]["fme"]!= "":
								#Trace.Write("--rechecking---333---"+str(partsQty[allIds[key]["part_Number"]]["SalesText"]))
								self.PopulateValidPartsConfme(key,allIds[key]["part_Number"],allIds[key]["Qty"],0,"",allIds[key]["fme"],extended_desc,cost_price)
								#self.PopulateValidPartsConfme(key,allIds[key]["part_Number"],allIds[key]["Qty"],lv_cps_config_price_dict[allIds[key]["part_Number"]],partsQty[allIds[key]["part_Number"]]["SalesText"],allIds[key]["fme"],extended_desc,cost_price)
                            #else:
                                #Trace.Write("--rechecking---444---"+str(partsQty[allIds[key]["part_Number"]]["SalesText"]))
                                #self.PopulateInValidCon(key, allIds[key]["part_Number"],allIds[key]["Qty"],"FME code missing for VC Product",partsQty[allIds[key]["part_Number"]]["SalesText"])
                """if Invalidconfigparts:
                    message = Translation.Get('message.uploadExcel.pricebook')
                    for partNumber in Invalidconfigparts:
                        InvpartID = [key for key, value in allIds.iteritems() if value["part_Number"] == partNumber]
                        if partNumber != "":
                            Trace.Write(str(partNumber)+"-------rechecking---2222--------->"+str(Invalidconfigparts))
                            self.PopulateInValidCon(InvpartID[0],partNumber,partsQty[partNumber]["Qty"],message,partsQty[partNumber]["SalesText"]) """
            
            #Set all products selected in Valid parts container to consider for add to quote action
            for row in self.validPartsCon.Rows:
                row.IsSelected = True
            
            #products not found in simple or configurable product list to be populated as invalid 
            message = Translation.Get('message.uploadExcel.catalog')
            for partNumber in partList:
                if partNumber not in catlogProducts and partNumber not in configurableProducts:
                    InvpartID = [key for key, value in allIds.iteritems() if value["part_Number"] == partNumber]
                    self.PopulateInValidCon(InvpartID[0],partNumber,partsQty[partNumber]["Qty"],message,'')
        # set color green for validfme parts
        #for row in self.validPartsConfme.Rows:
            #if row["Message"] == '<label style="color:green">Valid</label>':
            #    validParts.append(row["ID"])

'''hostquery = SqlHelper.GetFirst("Select HostName from CT_HOSTNAME where Domain in (select tenant_name from tenant_environments where is_current_environment = 1)")
host = hostquery.HostName
Trace.Write('Host Name:'+hostquery.HostName)
accessTkn = GS_FME_CONFIG_MOD.getAccessToken(host)

def assignval(resp,prod):
    for atnm in list(resp):
        Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
        a = prod.Attributes.GetBySystemId(str(atnm["atnam"])).DisplayType
        if a == "DropDown":
            prod.Attributes.GetBySystemId(str(atnm["atnam"])).SelectValue(str(atnm["atwtb"]))
        elif a == "Free Input, no Matching":
            prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
        else:
            prod.Attributes.GetBySystemId(str(atnm["atnam"])).AssignValue(str(atnm["atwtb"]))
            Trace.Write("name--->{}val--->{}".format(str(atnm["atnam"]),str(atnm["atwtb"])))
    prod.ApplyRules()
    return prod.IsComplete,prod.TotalPrice

FME_Valid_Parts = Product.GetContainerByName("HPS_Valid_Parts")
if FME_Valid_Parts.Rows.Count>0:
    for prow in FME_Valid_Parts.Rows:
        Trace.Write("FME---->"+str(prow["FME"]))
        getprdid = SqlHelper.GetFirst("SELECT top 1 p.product_ID from products p LEFT OUTER JOIN product_versions pv on p.product_id=pv.product_id where p.product_catalog_code= '{}' and p.PRODUCT_ACTIVE = 1 and pv.is_active = 1 order by pv.SAPEffectiveDate desc, pv.version_number desc".format(str(prow["Part Number"])))
        try:
            prod = ProductHelper.CreateProduct(int(getprdid.product_ID))
            jsonConfig = GS_FME_CONFIG_MOD.fme2config(host, accessTkn,str(prow["Part Number"]),str(prow["FME"]))
            assignpart,assigntot = assignval(jsonConfig,prod)
            if prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS") is not None:
                prod.Attributes.GetBySystemId("V_RMK_SPECIAL_LABOR_HOURS").AssignValue("0")
        except Exception as e:
            assignpart = None
            assigntot = 0
        if assignpart:
            prow["Message"] = '<label style="color:green">Valid</label>'
        else:
            prow["Message"] = '<label style="color:red">InValid</label>' '''