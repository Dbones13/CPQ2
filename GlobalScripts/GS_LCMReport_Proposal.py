#Check/Return module name
def getModuleName(ModuleList, key, item=None):
    exceptionValue = ["MSID","System Group"]
    if item != None:
        return item.ProductNameTranslated
    if key in ModuleList.keys():
        if ModuleList[key] in exceptionValue:
            return ""
        return ModuleList[key]
    return ""
#Check/Return project type
def getProjectType(ModuleList, key, item=None):
    key= key.split(".")[0] if "." in key else key
    if item != None:
        return item.ProductNameTranslated
    if key in ModuleList.keys():
        return ModuleList[key]
    return ""
#Check if Booking LOB is LSS/PAS and Quote type is Projects
if Quote.GetCustomField("Quote Type").Content == 'Projects' and (Quote.GetCustomField("Booking LOB").Content in ('LSS', 'PAS')):
    #Query CT
    queryResult = SqlHelper.GetList("SELECT Product, Description, ProductCategory, Type, Category FROM WRITEINPRODUCTS")
    #Temp List for changing Module/Project Name
    ModuleList = dict()
    queryWriteInLookUp = dict()
    #PRJT/System Group - system group as parent, store temp module names
    systemGroupFound=False
    systemGroupDetails={
        "itemNumber":"",
        "moduleName":"",
        "partName":""
        }
    MaterialTypeException = ["Migration","Migration_New", "New / Expansion Project", "Trace Software", "Cyber", "Integrated Automation Assessment (IAA) - Project", "Integrated Automation Assessment (IAA)"]
    WriteInLookUp = {"Write-In Contingency": "Contingency", "Write-In LCM Admin Fee LSS": "LCM Admin", "Write-In LCM Admin Fee PAS": "LCM Admin", "Write-In Labor Escalation LSS": "LCM Labor Escalation", "Write-In Labor Escalation PAS": "LCM Labor Escalation", "Write-in BOM Escalation": "LCM BOM Escalation"}
    #Product Category for Material Type
    ProductCategoryLoopUp = {"Honeywell Material": "Hardware and Software", "Honeywell Software": "Hardware and Software", "Third-Party Material": "Hardware and Software", "Other" : "Hardware and Software", "Honeywell Labor" : "Project Services", "Third Party Labor":"Project Services"}
    #Iterate items in Cart
    for i in queryResult:
        tempDict = dict()
        tempDict["Description"] = i.Description
        tempDict["ProductCategory"] = i.ProductCategory
        tempDict["Type"] = i.Type
        tempDict["Category"] = i.Category
        queryWriteInLookUp[i.Product] = tempDict
    for item in Quote.MainItems:
        PeriodicTypeName = ""
        WriteInCategory = ""
        HCIWriteInName = ""
        WriteInProductCategory = ""
        if item.PartNumber in queryWriteInLookUp.keys():
            #add condition to check description.
            PeriodicTypeName = queryWriteInLookUp[item.PartNumber]["Type"]
            WriteInCategory = queryWriteInLookUp[item.PartNumber]["Category"]
            HCIWriteInName = queryWriteInLookUp[item.PartNumber]["Description"]
            WriteInProductCategory = queryWriteInLookUp[item.PartNumber]["ProductCategory"]
        #To Assign Parent Project Type
        if item.ParentRolledUpQuoteItem in ("", 0, None) and item.PartNumber == "Cyber Products":
            item['QI_ProjectType'].Value = "Cyber"
        else:
            item['QI_ProjectType'].Value = getProjectType(ModuleList, str(item.ParentRolledUpQuoteItem), item) if item.ParentRolledUpQuoteItem in (None, "") else getProjectType(ModuleList, str(item.ParentRolledUpQuoteItem))
        #To assign Contract Type not HCI Write-In
        if item.ParentRolledUpQuoteItem in (0, "", None) and PeriodicTypeName != "":
            item['QI_ContractType'].Value = "Periodic"
        elif item.PartNumber == "Write-In Standard Warranty":
            item['QI_ContractType'].Value = "Others"
        else:
            item['QI_ContractType'].Value = "Projects"
        #iterate child items
        if len(list(item.AsMainItem.Children)) == 0:
            #Project Type - logic start
            if "Write-In" in item.ProductTypeName and item.ParentRolledUpQuoteItem in (0, "", None):
                if PeriodicTypeName != "":
                    item['QI_ProjectType'].Value = PeriodicTypeName 
                elif item.PartNumber in WriteInLookUp.keys():
                    item['QI_ProjectType'].Value = WriteInLookUp[item.PartNumber]
                elif WriteInCategory.upper() == "HCI":
                    item['QI_ProjectType'].Value = "Migration"
                    item['QI_ModuleName'].Value = HCIWriteInName
                elif WriteInCategory == "Cyber" or getProjectType(ModuleList, str(item.ParentRolledUpQuoteItem)) == "Cyber Products":
                    item['QI_ProjectType'].Value = "Cyber"
                else:
                    item['QI_ProjectType'].Value = "Others" if item.PartNumber != "Write-In Standard Warranty" else ""
            else:
                if getProjectType(ModuleList, str(item.ParentRolledUpQuoteItem)) == "Cyber Products":
                    item['QI_ProjectType'].Value = "Cyber"
                else:
                    item['QI_ProjectType'].Value = "Others" if item.ParentRolledUpQuoteItem in (0, "", None) else getProjectType(ModuleList, str(item.ParentRolledUpQuoteItem))
            #Project Type - logic end
            #Module Type - logic start
            if item['QI_ModuleName'].Value in (0, "", None):
                if getModuleName(ModuleList,str(item.RolledUpQuoteItem).split(".")[0])=="New / Expansion Project":
                    item['QI_ModuleName'].Value=systemGroupDetails['moduleName']
                    item['QI_Area'].Value= systemGroupDetails['partName']
                elif item.ParentRolledUpQuoteItem in (0, "", None) and item['QI_ProjectType'].Value == "Others":
                    item['QI_ModuleName'].Value = ""
                else:
                    item['QI_ModuleName'].Value = "" if "." not in (str(item.ParentRolledUpQuoteItem)) else getModuleName(ModuleList, item.ParentRolledUpQuoteItem)
            #Module Type - logic end 
            #Material Type - logic start
            if item.ParentRolledUpQuoteItem in (None, "") and WriteInCategory != "" and PeriodicTypeName == "" and item['QI_ProjectType'].Value !="Others":
                if item.PartNumber in WriteInLookUp.keys():
                    item['QI_MaterialType'].Value = ""
                else:    
                    item['QI_MaterialType'].Value = ProductCategoryLoopUp[WriteInProductCategory] if WriteInProductCategory in ProductCategoryLoopUp.keys() else ""
            elif item['QI_ProjectType'].Value in MaterialTypeException:
                if item.PartNumber.startswith('HPS') or item.PartNumber.startswith('SVC'):
                    item['QI_MaterialType'].Value = "Project Services"
                elif item.PartNumber == "Project Management":
                    item['QI_MaterialType'].Value = ""
                else:
                    item['QI_MaterialType'].Value = "Hardware and Software"
            else:
                item['QI_MaterialType'].Value = ""
            #Material Type - logic end
            #estimator summary type - logic start
            if item['QI_ProjectType'].Value in MaterialTypeException:
                if item.PartNumber == "Project Management":
                    item['QI_LCMSummaryType'].Value = ""
                else:    
                    item['QI_LCMSummaryType'].Value = "Honeywell HW & SW" if item['QI_MaterialType'].Value == "Hardware and Software" else "Honeywell Labor"
            elif item.ParentRolledUpQuoteItem in (0, "", None) and PeriodicTypeName != "":
                item['QI_LCMSummaryType'].Value = PeriodicTypeName
            elif item.PartNumber == "Write-In Standard Warranty":
                item['QI_LCMSummaryType'].Value = "Standard Warranty"
            elif item['QI_ProjectType'].Value == "Others":
                item['QI_LCMSummaryType'].Value = "Others"
            else:
                if item.PartNumber in WriteInLookUp.keys():
                    if item.PartNumber == "Write-in BOM Escalation":
                        item['QI_LCMSummaryType'].Value = "Escalation HW & SW"
                    elif item.PartNumber in ("Write-In Labor Escalation PAS","Write-In Labor Escalation LSS"):
                        item['QI_LCMSummaryType'].Value = "Escalation Labor"
                    else:
                        item['QI_LCMSummaryType'].Value = WriteInLookUp[item.PartNumber]
            #estimator summary type - logic end
        else:
            #New/Expansion-System Group logic for module name
            if systemGroupFound==True:
                if str(item.RolledUpQuoteItem).split(".")[0]!= str(systemGroupDetails['itemNumber']).split(".")[0] or item.ProductNameTranslated=="System Group":
                    systemGroupFound=False
                    systemGroupDetails['itemNumber']=""
                    systemGroupDetails['moduleName']=""
                    systemGroupDetails['partName']=""
                else:
                    if item.ParentRolledUpQuoteItem==systemGroupDetails['itemNumber']:
                        systemGroupDetails['moduleName']=item.ProductNameTranslated
            if item.ProductNameTranslated=="System Group":
                systemGroupFound=True
                systemGroupDetails['itemNumber']=item.RolledUpQuoteItem
                systemGroupDetails['partName']=item.PartNumber
            #Module Name/Project Type logic - list of Super Parents and Parents
            ModuleList[item.RolledUpQuoteItem]=item.ProductNameTranslated
    Quote.Save(False)