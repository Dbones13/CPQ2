from GS_CommonConfig import CL_CommonSettings as CS
from GS_GetPriceFromCPS import getCYBERPrice
from GS_ItemCalculations import CalculateListPrice,assignLeadTime,calculatePublishedLeadTime,calculateLTDevileryDate,calculateExpediteFee,calculateItemDiscountFromPercent
from GS_Validate_Product_Type import IsVCitem
from GS_VcModel_Update import VcModelupdate
from GS_ExtendedETOCal import ExtendedETOCal
from CF_UTILS import CF_CONSTANTS, get_custom_field_value, split_after_comma

def getFloat(Var):
	return float(Var) if Var else 0

if Quote.GetGlobal('PerformanceUpload') != 'Yes':
    if Quote.GetCustomField("Booking LOB").Content == 'PMC':
        res = SqlHelper.GetFirst("select PartNumber,family_code from PMC_GASETO_YSPEC_MARINE_PRODUCTS where PartNumber = '{}'".format(Item.PartNumber))
        if (res is not None and res.family_code=='Field Instruments' and Item.QI_FME.Value and not str(Item.QI_FME.Value).startswith('Y')) or (res is None and Item.QI_FME.Value and not str(Item.QI_FME.Value).startswith('Y')):
            Item['QI_Ace_Quote_Number'].Value,Item['QI_Ace_Description'].Value,Item['QI_Adder_LP'].Value='','',''
            Item.MrcListPrice,Item.MrcCost=0,0
            Item.ListPrice = Item.ProductModelPrice
        else:
            Trace.Write("---PMC--y_quote->"+str(Quote.GetGlobal('y_quote')))
            if Quote.GetGlobal('y_quote') or Quote.GetGlobal('y_desc'):
                Item['QI_Ace_Quote_Number'].Value=Quote.GetGlobal('y_quote')
                Item['QI_Ace_Description'].Value=Quote.GetGlobal('y_desc')
            if Quote.GetGlobal('y_adder'):
                Item['QI_Adder_LP'].Value=Quote.GetGlobal('y_adder')
            if Quote.GetGlobal('y_list'):
                Item.MrcListPrice = getFloat(Quote.GetGlobal('y_list'))
            if Quote.GetGlobal('y_cost'):
                Item.MrcCost = getFloat(Quote.GetGlobal('y_cost'))
            Trace.Write(str(Item['QI_Adder_LP'].Value)+"--->"+str(Item.ListPrice)+"--->"+str(Quote.GetGlobal('y_list'))+"---recheck--->"+str(Item.MrcListPrice))
            if Quote.GetGlobal('y_adder')=='Adder' or str(Item['QI_Adder_LP'].Value)=='Adder':
                Trace.Write(str(Item.ProductModelPrice)+"---recheck---111--->"+str(Item.MrcListPrice))
                Item.ListPrice = Item.ProductModelPrice + Item.MrcListPrice
                #Item.ListPrice = Item.ProductModelPrice + getFloat(Quote.GetGlobal('y_list')) if Quote.GetGlobal('y_list') else Item.MrcListPrice
                #Item.Cost += getFloat(Quote.GetGlobal('y_cost')) if Quote.GetGlobal('y_cost') else Item.MrcCost
            elif Quote.GetGlobal('y_adder')=='Total LP' or str(Item['QI_Adder_LP'].Value)=='Total LP':
                Item.ListPrice = getFloat(Quote.GetGlobal('y_list')) if Quote.GetGlobal('y_list') else Item.MrcListPrice
                #Item.Cost = getFloat(Quote.GetGlobal('y_cost')) if Quote.GetGlobal('y_cost') else Item.MrcCost
            
            # Product Bulk Upload
            if Quote.GetGlobal('BU_AdderTotalETO'):
                adderDic = eval(Quote.GetGlobal('BU_AdderTotalETO'))
                Item['QI_Adder_LP'].Value = str(adderDic['adder'])
                if adderDic['adder'] == 'Adder':
                    Item.ListPrice += getFloat(adderDic['listprice'])
                    Item.Cost += getFloat(adderDic['cost'])
                elif adderDic['adder'] == 'Total LP':
                    Item.ListPrice = getFloat(adderDic['listprice'])
                    Item.Cost = getFloat(adderDic['cost'])
                Item.MrcListPrice = getFloat(adderDic['listprice'])
                Item.MrcCost = getFloat(adderDic['cost'])
                Quote.SetGlobal('BU_AdderTotalETO','')

            if Quote.GetCustomField('Quote Type').Content == 'Parts and Spot':
                calculateItemDiscountFromPercent(Quote, Item)
    #CC_BeforeItemLoad_CCC - deactivated
    if Quote.GetCustomField("Booking LOB").Content == 'CCC' and  len(CS.setBeforeQuoteItems)>0: #CC_BeforeItemLoad_CCC - deactivated
        values = CS.setBeforeQuoteItems[Item.QuoteItemGuid].split('~')
        Item.Quantity = int(values[0])
        Item.MrcCost = float(values[3])
        Item['QI_Project_Price_Adjustment_Percent'].Value = float(values[5])
        Item['QI_Frame_Discount_Percent'].Value = float(values[6])
        Item['QI_Service_Discount_Percent'].Value = float(values[7])
        Item['QI_Regional_Discount_Percent'].Value = float(values[8])
        Item['QI_Business_Discount_Percent'].Value = float(values[9])
        Item['QI_Application_Discount_Percent'].Value = float(values[10])
        Item['QI_Defect_Discount_Percent'].Value = float(values[11])
        Item['QI_Competitive_Discount_Percent'].Value = float(values[12])
        Item['QI_Other_Discount_Percent'].Value = float(values[13])
        Item['QI_Additional_Discount_Percent'].Value = float(values[13])
        Item['QI_Solution_CCC'].Value = str(values[14])
        Item['QI_Package_CCC'].Value = str(values[15])

    #CC_updateExperionQty - Deactivated.
    if Item.ParentItemGuid == '' and Item.PartNumber in ('Experion Station Upgrade', 'Experion Server Upgrade', 'Experion Controller Upgrade'):
            for item in Item.AsMainItem.Children:
                for attr in item.SelectedAttributes:
                    if attr.Name=="ItemQuantity":
                        for value in attr.Values:
                            item.Quantity= float(Item.Quantity) * float(value.Display)
                        break
    if Item.ProductName == 'WriteIn':
        for attr in Item.SelectedAttributes:
            if attr.Name == 'Writein_Category':
                Item.QI_Writein_Category.Value = attr.Values[0].Display

    #CC_UpdateListPrice - Deactivated   
    CalculateListPrice(Quote, Item, dict(), TagParserQuote, Session)
    Item.ExtendedListPrice = Item.ListPrice * Item.Quantity
    if Item.ProductName in('OPM','Non-SESP Exp Upgrade'):
        Session['ListPrice_WISSP'] = ((Item.ListPrice * 0.05) - ((Item.ListPrice * 0.05) * (Item.QI_MPA_Discount_Percent.Value / 100)))
        Session['WISSP_FLAG']=1
    elif not Item.IsLineItem and Item.PartNumber == "Write-in Site Support Labor" and Session['WISSP_FLAG']:
        Session['RollupValue'] = Item.RolledUpQuoteItem
    if Session['RollupValue']:
        Quote.GetItemByQuoteItem(Session['RollupValue']).ListPrice = Session['ListPrice_WISSP']

    #Cyber_BundlePricelist - Deactivated
    if len(CS.cyberProductfromtable) == 0:
        part_number_list = SqlHelper.GetList('SELECT Part_Number FROM CT_CYBER_PRICINGLISTTYPE')
        CS.cyberProductfromtable = [i.Part_Number for i in part_number_list]
    if Item.PartNumber in CS.cyberProductfromtable and Item.ListPrice == 0:
        Item.ListPrice = float(getCYBERPrice(Quote,dict(),Item.PartNumber,TagParserQuote, dict()) or 0)

    #CC_GetCost_Plant_Change --> Item
    if Session["prevent_execution"] != "true" and (Quote.GetCustomField('CF_Plant_Prevent_Calc').Content != 'true' or Quote.GetCustomField('Booking LOB').Content != 'PMC'):
        #Get cost from SAP
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
        if Quote.GetCustomField("CF_Plant").Content!='' and ((Quote.GetCustomField("Quote Type").Content == 'Parts and Spot' and Quote.GetCustomField('Booking LOB').Content == "PMC")):


            #Observed PMC writeIn products are created in SAP. Hence, adding extra condition to not to override writeIn cost via API
            writein_data = SqlHelper.GetFirst("SELECT Product FROM WRITEINPRODUCTS(NOLOCK) WHERE Product= '{}'".format(str(Item.PartNumber)))
            getprdid = SqlHelper.GetFirst("SELECT IsSyncedFromBackOffice from products(NOLOCK) where product_catalog_code= '{}' and IsSyncedFromBackOffice = 'True' and PRODUCT_ACTIVE = 1 ".format(str(Item.PartNumber)))
            if getprdid is not None and writein_data is None:
                if Item.QI_Plant.Value == '' or Item.QI_prev_plant_value.Value!=Item.QI_Plant.Value or Item.QI_SAP_UnitCost.Value==0:
                    #call cost API only when there is plant change at Item level or when cost is zero.
                    host=getHost()
                    if Item.QI_Plant.Value=='':#Set only when Quote Item Plant is blank
                        custom_field_name = CF_CONSTANTS.get("QUOTE_LEVEL_PLANT_FIELD")
                        full_plant_value = get_custom_field_value(Quote, custom_field_name)
                        plant_code,plant_name = split_after_comma(full_plant_value)
                        Item.QI_Plant.Value = plant_name
                    if host!='':
                        full_plant_value = Item.QI_Plant.Value
                        plant_code,plant_name = split_after_comma(full_plant_value)
                        fn_getCost(host,Item.PartNumber,Item.QI_FME.Value,plant_name)
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
        if Quote.GetCustomField('Booking LOB').Content != 'HCP' and Quote.GetCustomField("Quote Type").Content == 'Projects' and SqlHelper.GetFirst("select 1 from Products where IsSyncedFromBackOffice = 'True' and IsSimple = 'False' and product_catalog_code = '{}'".format(Item.PartNumber)):
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

    #CC_Product_Validation - Deactivated
    if Item.ProductName == 'MSID_New':
        Session["MSID"]=Item.PartNumber
        Session["msid_QInumber"]=Item.RolledUpQuoteItem
    elif Session["MSID"] and Session["msid_QInumber"] and Item.RolledUpQuoteItem.startswith(str(Session["msid_QInumber"])):
        if len(list(Item.AsMainItem.Children))==0:
            Item.QI_Area.Value = Session["MSID"]

    assignLeadTime(Quote,Item)
    calculatePublishedLeadTime(Quote,Item)
    calculateLTDevileryDate(Quote,Item)

    if Quote.GetCustomField('Booking Lob').Content == "LSS" and Quote.GetCustomField('Quote Type').Content == 'Parts and Spot':
        #calculateExpediteFee(Quote,Item)
        account_name=Quote.GetCustomField("Account Name").Content
        if Item and Item.AsMainItem and Item.AsMainItem.VCItemPricingPayload and Item.AsMainItem.VCItemPricingPayload.Conditions:
            conditions = Item.AsMainItem.VCItemPricingPayload.Conditions
            for cond in conditions:
                if cond.ConditionType == "ZTSC":
                    Item['QI_Tariff_PCT'].Value = cond.ConditionRate if cond.ConditionRate else 0.00
    elif Quote.GetCustomField('Booking Lob').Content == "PMC" and Quote.OrderStatus.Id == 32:
        if IsVCitem(Item.PartNumber)==True:
            VcModelupdate(Quote,Item)
        if Item and Item.AsMainItem and Item.AsMainItem.VCItemPricingPayload and Item.AsMainItem.VCItemPricingPayload.Conditions:
            conditions = Item.AsMainItem.VCItemPricingPayload.Conditions
            for cond in conditions:
                if cond.ConditionType == "ZTSC":
                    Item['QI_Tariff_PCT'].Value = cond.ConditionRate if cond.ConditionRate else 0.00
    #CC_Calculate_Regional_Margin - Deactivated
    if Item.ProductSystemId == 'Write-In_Tariff_cpq':
        if Item.ExtendedAmount != 0:
            Item['QI_WTWMargin'].Value = (Item.ExtendedAmount - Item['QI_ExtendedWTWCost'].Value)
            Item['QI_RegionalMarginPercent'].Value = (Item.ExtendedAmount - Item.ExtendedCost)/Item.ExtendedAmount * 100
            Item['QI_RegionalMargin'].Value = (Item.ExtendedAmount - Item.ExtendedCost)
            Item['QI_WTWMarginPercent'].Value = (Item.ExtendedAmount - Item['QI_ExtendedWTWCost'].Value)/Item.ExtendedAmount * 100

    #CC_FactoryDataCalculation - Deactivated
	def filterRecord(Part_number=None, MRP_indicator=None,FixedVender=None,records=None):
		result = []
		if records is None: return result
		if Part_number!=None:
			for i in records:
				if i.Material==Part_number:
					result.append(i)
			return result
		if MRP_indicator!=None:
			for i in records:
				if i.MRP_Indicator==MRP_indicator:
					result.append(i)
			return result
		if FixedVender!=None:
			for i in records:
				if i.Fixed_vendor==FixedVender:
					result.append(i)
			return result


	if Quote.GetCustomField("CF_Factory_Data_Applicable").Content == "Y":
		quote_expiry_date = str(Quote.EffectiveDate.Date).split(' ')[0]
		# Filter custom table data
		query = "Select Vendor, Vendor_Name, Material, MRP_Indicator, Fixed_vendor from CT_VENDOR_INFORMATION WHERE Valid_from <= '{}' and Valid_to >= '{}' and Material = '{}'".format(quote_expiry_date, quote_expiry_date,Item.PartNumber)
		result = SqlHelper.GetList(query)
		# iterate cart items
		if len(list(Item.AsMainItem.Children))==0:
			if len(result)!=0:
					if len(result) > 1:
						result2=filterRecord(FixedVender='X',records=result) # filtered result by Fixed vender 
						if(len(result2)!=0):
							Item.QI_FactoryCode.Value=result2[0].Vendor
							Item.QI_FactoryName.Value = result2[0].Vendor_Name
						else:
							result3=filterRecord(MRP_indicator='1',records=result) # filtered result by  MRP_Indicator
							if(len(result3)!=0):
								Item.QI_FactoryCode.Value = result3[0].Vendor
								Item.QI_FactoryName.Value = result3[0].Vendor_Name
							else:
								Item.QI_FactoryCode.Value = result[0].Vendor
								Item.QI_FactoryName.Value = result[0].Vendor_Name
					else:
						Item.QI_FactoryCode.Value = result[0].Vendor
						Item.QI_FactoryName.Value = result[0].Vendor_Name
		else:
			Item.QI_FactoryCode.Value = ""
			Item.QI_FactoryName.Value = ""

    #CC_ExtendedETOCal - Deactivated
    if Quote.GetCustomField('Booking LOB').Content == "PMC":
        ExtendedETOCal(Quote,Item)
	Session["ItemGUID"].append(Item.QuoteItemGuid)