#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: Script to populate Quote Table Data for Migration & New-Expansion Pricing Summary
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version   Comment
# 01-12-2023	Pratik Sanghani			    7		  Changes for CXCPQ-72619


migTotal = 0
cyberTotal = 0
traceTotal = 0
IAATotal = 0
partDict = dict()
msidList = []
bomDict = dict()
migrationPricingData = dict()
PRJTItemID = ""
PRJTpmTotal = 0

PRJTTotal = 0
PRJTRolledUpQuoteItem = ""
SysGroups = dict()
PRJTMSIDPricing = dict()
MigrationMSIDDict = dict()

Log.Write("CA_Migration_New-Expansion_Pricing_Summary : Started For Quote - "+Quote.CompositeNumber)

def getMsidFromGUID(guid):
    return Quote.GetItemByUniqueIdentifier(guid).PartNumber

def getPricingData(item):
    pricingDict = dict()
    for msid in item.Children:
        pricingDict[msid.QuoteItemGuid] = getMsidPriceDict(msid)
    return pricingDict


def getMsidPriceDict(item):
    migrationTotal = item.ExtendedAmount
    hwPrice = getHwSWPrice(item)
    offSitePrice = getPMPrice(item) + getOffSitePrice(item)
    onSitePrice =  getOnSitePrice(item)
    #auditTotal = getAuditPrice(item)

    #diff = migrationTotal - (hwPrice + offSitePrice + onSitePrice + auditTotal)
    diff = migrationTotal - (hwPrice + offSitePrice + onSitePrice )
    return {
            "Hardware and Software" : hwPrice,
            "Project Management and Off-Site Engineering" : offSitePrice,
            "On-Site Engineering" : onSitePrice + diff
        }


def getHwSWPrice(item):
    total = 0
    services = 0
    for child in filter(lambda x : x.PartNumber != "Project Management" , item.Children):
        total += child.ExtendedAmount
        for childItems in filter(lambda x : x.PartNumber.startswith('SVC') , child.Children):
            services += childItems.ExtendedAmount
    return total - services

def getPMPrice(item):
    for child in filter(lambda x : x.PartNumber == "Project Management" , item.Children):
        return child.ExtendedAmount
    return 0

def getOffSitePrice(item):
    total = 0
    attrs = item.SelectedAttributes
    containerNames = {
        "OPM" : "MSID_Labor_OPM_Engineering",
        "LCN" : "MSID_Labor_LCN_One_Time_Upgrade_Engineering",
        "EBR" : "MSID_Labor_EBR_Con",
        "EHPM/EHPMX/ C300PM" : "MSID_Labor_EHPM_C300PM_Con",
        "ELCN" : "MSID_Labor_ELCN_Con",
        "Orion Console" : "MSID_Labor_Orion_Console_Con",
        "TCMI" : "MSID_Labor_TCMI_Con",
        "TPS_to_EXP" : "MSID_Labor_TPS_TO_EXPERION_Con",
        "C200_Migration" : "MSID_Labor_C200_Migration_Con",
		"CB_EC_Upgrade_to_C300_UHIO" : "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con",
        "FDM Upgrade" : "MSID_Labor_FDM_Upgrade_Con",
        "XP10 Actuator Upgrade" : "MSID_Labor_XP10_Actuator_Upgrade_con",
        "FSC to SM" : "MSID_Labor_FSC_to_SM_con",
        "xPM to C300 Migration" : "MSID_Labor_xPM_to_C300_Migration_Con",
		"LM_ELMM_ControlEdge_PLC" : "MSID_Labor_LM_to_ELMM_Con",
        "Graphics Migration" : "MSID_Labor_Graphics_Migration_con",
		"FSC to SM IO Migration" : "MSID_Labor_FSCtoSM_IO_con",
        "CD Actuator I-F Upgrade" : "MSID_Labor_CD_Actuator_con",
        "Trace Software" : "Trace_Software_Labor_con",
        "CWS RAE Upgrade" : "MSID_Labor_CWS_RAE_Upgrade_con",
        "EHPM HART IO" : "MSID_Labor_EHPM_HART_IO_Con",
        "QCS RAE Upgrade" : "MSID_Labor_QCS_RAE_Upgrade_con",
        "ELEPIU ControlEdge RTU Migration Engineering" : "MSID_Labor_ELEPIU_con",
        "Virtualization System" : "MSID_Labor_Virtualization_con",
        "3rd Party PLC to ControlEdge PLC/UOC" : "3rd_Party_PLC_UOC_Labor",
        "TPA/PMD Migration" : "MSID_Labor_TPA_con",
        "Generic System" : "MSID_Labor_Generic_System1_Cont"
    }
    productDict = dict()
    for partKey , containerName in containerNames.items():
        partDict = dict()
        con = attrs.GetContainerByName(containerName)
        if not con:
            continue
        for row in filter(lambda x: x['Deliverable_Type'] == 'Offsite' , con.Rows):
            partDict[row['FO_Eng']] = round(getFloat(row['Final_Hrs']) * getFloat(row['FO_Eng_Percentage_Split'])/100, 0) + partDict.get(row['FO_Eng'] , 0)
            partDict[row['GES_Eng']] = round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100, 0) + partDict.get(row['GES_Eng'] , 0)
        productDict[partKey] = partDict
    Trace.Write(RestClient.SerializeToJson(productDict))
    for child in item.Children:
        partDict = productDict.get(child.PartNumber)
        if not partDict:
            continue
        for childItem in child.Children:
            if partDict.get(childItem.PartNumber):
                total += childItem.NetPrice * partDict.get(childItem.PartNumber)
                partDict.pop(childItem.PartNumber)

    return total

def getOnSitePrice(item):
    total = 0
    attrs = item.SelectedAttributes
    containerNames = {
        "OPM" : "MSID_Labor_OPM_Engineering",
        "LCN" : "MSID_Labor_LCN_One_Time_Upgrade_Engineering",
        "EBR" : "MSID_Labor_EBR_Con",
        "EHPM/EHPMX/ C300PM" : "MSID_Labor_EHPM_C300PM_Con",
        "ELCN" : "MSID_Labor_ELCN_Con",
        "Orion Console" : "MSID_Labor_Orion_Console_Con",
        "TCMI" : "MSID_Labor_TCMI_Con",
        "TPS_to_EXP" : "MSID_Labor_TPS_TO_EXPERION_Con",
         "C200_Migration" : "MSID_Labor_C200_Migration_Con",
		"CB_EC_Upgrade_to_C300_UHIO" : "MSID_Labor_CB-EC_Upgrade_to_C300-UHIO_con",
        "FDM Upgrade" : "MSID_Labor_FDM_Upgrade_Con",
        "XP10 Actuator Upgrade" : "MSID_Labor_XP10_Actuator_Upgrade_con",
        "FSC to SM" : "MSID_Labor_FSC_to_SM_con",
        "xPM to C300 Migration" : "MSID_Labor_xPM_to_C300_Migration_Con",
		"LM_ELMM_ControlEdge_PLC" : "MSID_Labor_LM_to_ELMM_Con",
        "Graphics Migration" : "MSID_Labor_Graphics_Migration_con",
		"FSC to SM IO Migration" : "MSID_Labor_FSCtoSM_IO_con",
        "CD Actuator I-F Upgrade" : "MSID_Labor_CD_Actuator_con",
        "Trace Software" : "Trace_Software_Labor_con",
        "CWS RAE Upgrade" : "MSID_Labor_CWS_RAE_Upgrade_con",
        "EHPM HART IO" : "MSID_Labor_EHPM_HART_IO_Con",
        "QCS RAE Upgrade" : "MSID_Labor_QCS_RAE_Upgrade_con",
        "ELEPIU ControlEdge RTU Migration Engineering" : "MSID_Labor_ELEPIU_con",
        "Virtualization System" : "MSID_Labor_Virtualization_con",
        "3rd Party PLC to ControlEdge PLC/UOC" : "3rd_Party_PLC_UOC_Labor",
        "TPA/PMD Migration" : "MSID_Labor_TPA_con",
        "Generic System" : "MSID_Labor_Generic_System1_Cont"
    }
    productDict = dict()
    for partKey , containerName in containerNames.items():
        partDict = dict()
        con = attrs.GetContainerByName(containerName)
        if not con:
            continue
        for row in filter(lambda x: x['Deliverable_Type'] == 'Onsite' , con.Rows):
            partDict[row['FO_Eng']] = round(getFloat(row['Final_Hrs']) * getFloat(row['FO_Eng_Percentage_Split'])/100 , 0) + partDict.get(row['FO_Eng'] , 0)
            partDict[row['GES_Eng']] = round(getFloat(row["Final_Hrs"]) * getFloat(row["GES_Eng_Percentage_Split"]) / 100 , 0) + partDict.get(row['GES_Eng'] , 0)
        productDict[partKey] = partDict
    Trace.Write(RestClient.SerializeToJson(productDict))
    for child in item.Children:
        partDict = productDict.get(child.PartNumber)
        if not partDict:
            continue
        for childItem in child.Children:
            if partDict.get(childItem.PartNumber):
                total += childItem.NetPrice * partDict.get(childItem.PartNumber)
                partDict.pop(childItem.PartNumber)

    return total


def getFloat(val):
    if val:
        return float(val)
    return 0


def populatePricingData(dataDict):
    table = Quote.QuoteTables["QT_Merged_PricingSummary"]
    total = 0
    row = table.AddNewRow()
                
    row["MSID"] = "MSID - Migration"
    row["Product_Type"] = "Migration"
    
    for item in Quote.MainItems:
        data = dataDict.get(item.QuoteItemGuid)
        if data:
            MSIDData = MigrationMSIDDict.get(getMsidFromGUID(item.QuoteItemGuid))
            if MSIDData:
                hwsw = MSIDData["Hardware and Software"]
                PMOffEng = MSIDData["Project Management and Off-Site Engineering"]
                OnEng = MSIDData["On-Site Engineering"]

                MigrationMSIDDict[getMsidFromGUID(item.QuoteItemGuid)] = {"Hardware and Software": hwsw+data["Hardware and Software"], "Project Management and Off-Site Engineering":PMOffEng+data["Project Management and Off-Site Engineering"], "On-Site Engineering": OnEng+data["On-Site Engineering"]}

            else:
                hwsw = 0
                PMOffEng = 0
                OnEng = 0

                MigrationMSIDDict[getMsidFromGUID(item.QuoteItemGuid)] = {"Hardware and Software": hwsw+data["Hardware and Software"], "Project Management and Off-Site Engineering":PMOffEng+data["Project Management and Off-Site Engineering"], "On-Site Engineering": OnEng+data["On-Site Engineering"]}


    for key,value in MigrationMSIDDict.items():

        row = table.AddNewRow()
        row["MSID"] = "MSID " + key
        row["Description"] =  "Hardware and Software"
        row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(value["Hardware and Software"])
        #row["Sell_price"] = (value["Hardware and Software"])
        row["Product_Type"] = "Migration"
        total += value["Hardware and Software"]


        row = table.AddNewRow()
        #row["MSID"] = "MSID " + key
        row["Description"] =  "Project Management and Off-Site Engineering"
        row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(value["Project Management and Off-Site Engineering"])
        #row["Sell_price"] = (value["Project Management and Off-Site Engineering"])
        row["Product_Type"] = "Migration"
        total += value["Project Management and Off-Site Engineering"]


        row = table.AddNewRow()
        #row["MSID"] = "MSID " + key
        row["Description"] =  "On-Site Engineering"
        row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(value["On-Site Engineering"])
        #row["Sell_price"] = (value["On-Site Engineering"])
        row["Product_Type"] = "Migration"
        total += value["On-Site Engineering"]

    
    row = table.AddNewRow()
    row["Description"] = "Project Sub-Total"
    row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(total)
    #row["Sell_price"] = (total)
    row["Product_Type"] = "Migration"
    table.Save()
    return total


def getCyberBomDict(cyberPart):
    cyberTotal = 0
    for child in cyberPart.Children:
        if not child.PartNumber.startswith('SVC'):
            cyberTotal += child.ExtendedAmount
    return cyberTotal


def populateCyberPricingData(cyberTotal):
    table = Quote.QuoteTables["QT_Merged_PricingSummary"]
    row = table.AddNewRow()
    row["Description"] = "Cyber Products"
    row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(cyberTotal)
    #row["Sell_price"] = (cyberTotal)
    row["Product_Type"] = "Cyber Products"
    table.Save()


def getTraceBomDict(tracePart):
    traceTotal = tracePart.ExtendedAmount
    #for child in tracePart.Children:
    #    subChild=False 
    #    for i in child.Children:
    #        subChild=True
    #        traceTotal += child.ExtendedAmount
    #    if subChild == False:
    #        traceTotal += child.ExtendedAmount
    return traceTotal



def populateTracePricingData(traceTotal):
    table = Quote.QuoteTables["QT_Merged_PricingSummary"]
    row = table.AddNewRow()
    row["Description"] = "Trace Software"
    row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(traceTotal)
    #row["Sell_price"] = (traceTotal)
    row["Product_Type"] = "Trace Software"
    table.Save()


def getIAABomDict(IAAPart):
    IAATotal = 0
    for child in IAAPart.Children:
        IAATotal += child.ExtendedAmount
    return IAATotal

def populateIAAPricingData(IAATotal):
    table = Quote.QuoteTables["QT_Merged_PricingSummary"]
    row = table.AddNewRow()
    row["Description"] = "Integrated Automation Assessment (IAA)/System Performance Baseline (SPB)"
    row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(IAATotal)
    #row["Sell_price"] = (IAATotal)
    row["Product_Type"] = "IAA/SPB"
    table.Save()


def populateAdditionalItemsPricingData(AdditionalItemsTotal):
    table = Quote.QuoteTables["QT_Merged_PricingSummary"]
    #removeKeyRow(table , [
    #    "DOC_KEY_Total_AdditionalItems"
    #])
    row = table.AddNewRow()
    row["Description"] = "Additional Items"
    row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(AdditionalItemsTotal)
    #row["Sell_price"] = (AdditionalItemsTotal)
    row["Product_Type"] = "Additional Items"
    table.Save()



def populateProjectTotalPricingData(projectTotal):
    table = Quote.QuoteTables["QT_Merged_PricingSummary"]
    #removeKeyRow(table , [
    #    "DOC_KEY_Total_Project"
    #])
    row = table.AddNewRow()
    row["Description"] = "Project Total"
    row["Sell_price"] = (projectTotal)
    row["Product_Type"] = "Project Total"
    table.Save()


def getPRJTpmPricingData(PRJTItemID):
    PRJTpmTotal = 0
    for item in Quote.MainItems:
        if item.PartNumber.startswith('HPS_SYS') and item.ParentItemGuid == PRJTItemID:
            PRJTpmTotal += item.ExtendedAmount

    return PRJTpmTotal
   
def getPRJTMSIDs(Items):
     for item in Items.Children:
        if item.ProductSystemId == "System_Group_cpq":
            #CXCPQ-72619 : Grouping should be based on System Group Name
            SysGroups[item.RolledUpQuoteItem] = item.PartNumber

def CalculatePRJTMSIDPricing(SysGroups):
    for key,value in SysGroups.items():
        data = PRJTMSIDPricing.get(value)
        if not data :
            hwswPrice = 0
            EngSvcPrice = 0
            for item in Quote.MainItems:
                if item.RolledUpQuoteItem.startswith(key + '.') and len(list(item.Children)) == 0:
                    if item.PartNumber.startswith('HPS_SYS'):
                        EngSvcPrice += item.ExtendedAmount
                    else:
                        hwswPrice += item.ExtendedAmount
            
            PRJTMSIDPricing[value] = {"Hardware and Software":hwswPrice, "Engineering Services":EngSvcPrice}
        
        else:
            hwswPrice = data["Hardware and Software"]
            EngSvcPrice = data["Engineering Services"]
            for item in Quote.MainItems:
                if item.RolledUpQuoteItem.startswith(key + '.') and len(list(item.Children)) == 0:
                    if item.PartNumber.startswith('HPS_SYS'):
                        EngSvcPrice += item.ExtendedAmount
                    else:
                        hwswPrice += item.ExtendedAmount
            
            PRJTMSIDPricing[value] = {"Hardware and Software":hwswPrice, "Engineering Services":EngSvcPrice}



def PopulatePRJTMSIDPricing(PRJTMSIDPricing):
    table = Quote.QuoteTables["QT_Merged_PricingSummary"]
    if PRJTMSIDPricing != dict():
        for key,value in PRJTMSIDPricing.items():

            row = table.AddNewRow()
            row["MSID"] = "MSID " + key
            row["Description"] =  "Hardware and Software"
            row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(value["Hardware and Software"])
            #row["Sell_price"] = (value["Hardware and Software"])
            row["Product_Type"] = "New/Expansion"

            row = table.AddNewRow()
            #row["MSID"] = "MSID " + key
            row["Description"] =  "Engineering Services"
            row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(value["Engineering Services"])
            #row["Sell_price"] = (value["Engineering Services"])
            row["Product_Type"] = "New/Expansion"
    
    table.Save()

IsMigration = False
IsPRJT = False
IsAdditionalItems = False
IsCyberItem = False
IsTraceItem = False
IsIAAItem = False

table = Quote.QuoteTables["QT_Merged_PricingSummary"]
table.Rows.Clear()
table.Save()

for item in Quote.MainItems:
    if item.PartNumber == "Migration":
        
        migrationPricingData.update(getPricingData(item))
        #migTotal = populatePricingData(migrationPricingData)
        continue

    if item.PartNumber == "PRJT":
        PRJTItemID = item.QuoteItemGuid
        PRJTTotal += item.ExtendedAmount
        PRJTRolledUpQuoteItem = item.RolledUpQuoteItem
        getPRJTMSIDs(item)
        PRJTpmTotal += getPRJTpmPricingData(PRJTItemID)
        continue
    
    if item.PartNumber == "Cyber Products":
        cyberTotal += getCyberBomDict(item)
        IsCyberItem = True
        continue

    
    if item.PartNumber == "Trace Software":
        traceTotal += getTraceBomDict(item)
        IsTraceItem = True
        continue

    #CXCPQ-66236 : IAA-Project Pricing of Migration Module should not be considered
    if (item.PartNumber == "IAA -Project") and (not (item.ParentItemGuid)):
        IAATotal += getIAABomDict(item)
        IsIAAItem = True
        continue

    if '.' not in item.RolledUpQuoteItem and ( item.PartNumber != "Migration" and item.PartNumber != "PRJT" and item.PartNumber != "Cyber Products" and item.PartNumber != "Trace Software" and item.PartNumber != "IAA -Project" ):
        IsAdditionalItems = True
        continue



migTotal = populatePricingData(migrationPricingData)


if PRJTItemID != "":
    row = table.AddNewRow()
    row["MSID"] = "MSID - New/Expansion"
    row["Product_Type"] = "New/Expansion"

    CalculatePRJTMSIDPricing(SysGroups)
    PopulatePRJTMSIDPricing(PRJTMSIDPricing)

    row = table.AddNewRow()
    row["Description"] = "Project Management – New/Expansion"
    row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(PRJTpmTotal)
    #row["Sell_price"] = (getPRJTpmPricingData(PRJTItemID))
    row["Product_Type"] = "New/Expansion"

    row = table.AddNewRow()
    row["Description"] = "Project Sub-Total"
    row["Sell_price"] = UserPersonalizationHelper.ToUserFormat(PRJTTotal)
    #row["Sell_price"] = (PRJTTotal)
    row["Product_Type"] = "New/Expansion"

    table.Save()


projectTotal = Quote.GetCustomField('Total Sell Price').Content

if IsAdditionalItems:
    populateAdditionalItemsPricingData(UserPersonalizationHelper.ConvertToNumber(projectTotal) - migTotal - PRJTTotal - cyberTotal - traceTotal - IAATotal )

if IsIAAItem:
    populateIAAPricingData(IAATotal)

if IsTraceItem:
    populateTracePricingData(traceTotal)

if IsCyberItem:
    populateCyberPricingData(cyberTotal)

populateProjectTotalPricingData((projectTotal))

Log.Write("CA_Migration_New-Expansion_Pricing_Summary : Ended For Quote - "+Quote.CompositeNumber)
