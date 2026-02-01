#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: To Populate Escalted WriteIns Quote Line Items.
# JIRA Ref.  : CXCPQ-63379,CXCPQ-63380,CXCPQ-72648,CXCPQ-72655
# Author     : H542824
# Created Date : 16-10-2023
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version     Comment
# 04-12-2023	Pratik Sanghani    			27 	        Year 1 to be Escalated Realted Configuration
#----------------------------------------------------------------------------------------------------------

BOM_Cost_Per = 0 if Quote.GetCustomField("CF_Cost_percent").Content == "" else UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField("CF_Cost_percent").Content)

BOM_Price_Per = 0 if Quote.GetCustomField("CF_Sell_Price").Content == "" else UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField("CF_Sell_Price").Content)

LABOR_Cost_Price_Per = 0 if Quote.GetCustomField("CF_Cost_and_Sell_percent").Content == "" else UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField("CF_Cost_and_Sell_percent").Content)

LABOR_Year = float('inf') if Quote.GetCustomField("CF_Starting_Year").Content == "" else UserPersonalizationHelper.ConvertToNumber(Quote.GetCustomField("CF_Starting_Year").Content)

IS_MULTIYEAR = Quote.GetCustomField("CF_Multiyear_Project").Content

BOOKING_LOB = Quote.GetCustomField("Booking LOB").Content

Year_1_to_be_Escalated = Quote.GetCustomField("CF_LCM_Year_1_to_be_Escalated").Content

raw_list = []
NewWriteIns = []

WriteInMasterProduct = "Write-in_Products_cpq"
WriteInIDs = {
    'BOM': "Write-in BOM Escalation",
    'LABOR-LSS': "Write-In Labor Escalation LSS",
    'LABOR-PAS': "Write-In Labor Escalation PAS"
}


def remove_existing_writeins():
    for i in Quote.MainItems:
        if i.PartNumber in WriteInIDs.values():
                i.Delete()

def material_type(item):
    if item.PartNumber.startswith(('SVC','HPS_GES','HPS_SYS')):
        return 'LABOR'
    elif item.QI_Winest_Import.Value == 'True' and item.PartNumber.startswith(('HPS_ADV','ADV_GES')):
        return 'LABOR'
    else:
        return 'BOM'



def group_by_year_and_type(inp):
  out = []
  for year in set([row['Year'] for row in inp]):
    data = [row for row in inp if row['Year'] == year]
        
    obj = {year: {'BOM': {'Cost':0, 'Price':0}, 'LABOR': {'Cost':0, 'Price':0}}}
    for row in data:
        if row['Type'] == 'BOM':
            obj[year]['BOM']['Cost'] += row['Cost']
            obj[year]['BOM']['Price'] += row['Price']
        elif row['Type'] == 'LABOR':
            obj[year]['LABOR']['Cost'] += row['Cost']
            obj[year]['LABOR']['Price'] += row['Price']
    out.append(obj)
  return out


def compound_interest(price,rate,time):
    amt = float(price)*((1+(float(rate)/100))**float(time))
    CI = amt - price
    return CI

def getWriteInProductInfo(writeInPartNumber):
    writeInProduct = SqlHelper.GetFirst("SELECT Description, ProductLine, ProductLineDescription, ProductLineSubGroupDescription, ProductLineSubGroup, UnitofMeasure, ProductCategory, Category from WriteInProducts where Product = '"+writeInPartNumber+"'")
    if writeInProduct is not None:
        return writeInProduct
    return None

# Create dictionary with Periodics WriteIns -- H542826 : CXCPQ-78464 CXCPQ-78469 :start
def CheckWriteInPeriodics():
    queryWriteInLookUp = []
    queryResult = SqlHelper.GetList("SELECT Product FROM WRITEINPRODUCTS WHERE Type!=''")
    for i in queryResult:
        queryWriteInLookUp.append(i.Product)
    return queryWriteInLookUp
# Create dictionary with Periodics WriteIns -- H542826 : CXCPQ-78464 CXCPQ-78469 :end
       
def PopulateChildProduct(containerRow,category):
    containerRow.Product.Attributes.GetByName("Writein_Category").SelectValue(category)
    containerRow.Product.Attributes.GetByName("Selected_WriteIn").AssignValue(str(containerRow["Selected_WriteIn"]))
    #containerRow.Product.Attributes.GetByName("WriteInProductsChoices").SelectDisplayValue(str(containerRow["WriteInProducts"]))
    containerRow.Product.Attributes.GetByName("ItemQuantity").AssignValue(str(containerRow["ItemQuantity"]))
    #containerRow.Product.Attributes.GetByName("Extended Description").AssignValue(str(containerRow["ExtendedDescription"]))
    containerRow.Product.Attributes.GetByName("Extended Description").AssignValue(containerRow["ExtendedDescription"])
    containerRow.Product.Attributes.GetByName("Price").AssignValue(str(containerRow["Price"]))
    containerRow.Product.Attributes.GetByName("cost").AssignValue(str(containerRow["Cost"]))
    containerRow.Product.Attributes.GetByName("Description").AssignValue(containerRow["Description"])
    containerRow.Product.Attributes.GetByName("Product Line").AssignValue(str(containerRow["Product Line"]))
    containerRow.Product.Attributes.GetByName("Product Line Description").AssignValue(str(containerRow["Product Line Description"]))
    containerRow.Product.Attributes.GetByName("Product line sub group").AssignValue(str(containerRow["Product Line Sub Group"]))
    containerRow.Product.Attributes.GetByName("PLSG description").AssignValue(str(containerRow["PLSG Description"]))
    containerRow.Product.Attributes.GetByName("Unit of Measure").AssignValue(str(containerRow["Unit of Measure"]))
    
    containerRow.Product.Attributes.GetByName("LCM_WriteIn_Year").AssignValue(str(containerRow["Year"]))

def PopulateValidPartsCon(validPartsCon,partNumber, unitListPrice, unitRegionalCost,Year, writeInProductInfo):
    containerRow = validPartsCon.AddNewRow('WriteIn_cpq')
    containerRow.GetColumnByName('Category').SetAttributeValue(writeInProductInfo.Category)
    containerRow["Selected_WriteIn"]     = partNumber
    containerRow["Price"]               = unitListPrice
    containerRow["Cost"]                = unitRegionalCost
    containerRow["ItemQuantity"]        = "1"
    containerRow["Description"]			= writeInProductInfo.Description
    containerRow["Product Line"]		= writeInProductInfo.ProductLine
    containerRow["Product Line Description"] = writeInProductInfo.ProductLineDescription
    containerRow["Product Line Sub Group"] 	 = writeInProductInfo.ProductLineSubGroup
    containerRow["PLSG Description"]	= writeInProductInfo.ProductLineSubGroupDescription
    containerRow["Unit of Measure"]		= writeInProductInfo.UnitofMeasure
    
    containerRow["Year"]			    = Year
    
    PopulateChildProduct(containerRow,writeInProductInfo.Category)
    #Log.Info("{},{},{},{},{},{}".format(containerRow["Description"],containerRow["Product Line"],containerRow["Product Line Description"],containerRow["Product Line Sub Group"],containerRow["PLSG Description"],containerRow["Unit of Measure"]))
    containerRow.Product.ApplyRules()
    containerRow.ApplyProductChanges()
    containerRow.Calculate()


def EscalatedPrice(price,rate,time):
    amt = float(price)*((1+(float(rate)/100))**float(time))
    return amt

#Log.Write("CA_LCM_MultiYear_Escalation_Writein_Population : Started For Quote - "+Quote.CompositeNumber)

if IS_MULTIYEAR == "Yes" and Quote.GetCustomField("Quote Type").Content == 'Projects':

    remove_existing_writeins()
    queryWriteInLookUp=CheckWriteInPeriodics()
    for i in Quote.MainItems:
        if len(list(i.Children)) == 0:
            YEAR = int(((i["QI_Year"].Value).split())[-1]) if i["QI_Year"].Value else 1
            # Check whether write-ins are periodics or "Write-In Standard Warranty" -- H542826 : CXCPQ-78464 CXCPQ-79160 :start
            if (i.ParentRolledUpQuoteItem in (0, "", None) and i.PartNumber in queryWriteInLookUp) or i.PartNumber == "Write-In Standard Warranty":
                i['QI_Escalated_Price'].Value = i.ExtendedAmount
            # Check whether write-ins are periodics or "Write-In Standard Warranty" -- H542826 : CXCPQ-78464 CXCPQ-79160 :end
            else:    
                if material_type(i) == 'LABOR':
                    if YEAR >= LABOR_Year :
                        i['QI_Escalated_Price'].Value = EscalatedPrice(i.ExtendedAmount,LABOR_Cost_Price_Per,YEAR)
                        raw_list.append({"Type":"LABOR","Part_Number":i.PartNumber,"Year":YEAR,"Cost":i.ExtendedCost, "Price":i.ExtendedAmount})
                    else :
                        i['QI_Escalated_Price'].Value = i.ExtendedAmount
                else :
                    raw_list.append({"Type":"BOM","Part_Number":i.PartNumber,"Year":YEAR,"Cost":i.ExtendedCost, "Price":i.ExtendedAmount})
                    if Year_1_to_be_Escalated == 'Yes':
                        i['QI_Escalated_Price'].Value = EscalatedPrice(i.ExtendedAmount,BOM_Price_Per,YEAR)
                    else:
                        if YEAR > 1:
                            i['QI_Escalated_Price'].Value = EscalatedPrice(i.ExtendedAmount,BOM_Price_Per,YEAR-1)
                        else:
                            i['QI_Escalated_Price'].Value = i.ExtendedAmount

    Quote.Save(False)

    grouped_list = group_by_year_and_type(raw_list)

    for j in grouped_list:
        for year,amount in j.items():
            
            if (amount['LABOR']['Price'] != 0) or (amount['LABOR']['Cost'] != 0):
                if BOOKING_LOB == 'PAS':
                    NewWriteIns.append({ WriteInIDs['LABOR-PAS'] :{'Year': "Year "+str(year) ,'Cost':compound_interest(amount['LABOR']['Cost'],LABOR_Cost_Price_Per,year), 'Price':compound_interest(amount['LABOR']['Price'],LABOR_Cost_Price_Per,year)}})
                    
                if BOOKING_LOB == 'LSS':
                    NewWriteIns.append({ WriteInIDs['LABOR-LSS'] :{'Year': "Year "+str(year) ,'Cost':compound_interest(amount['LABOR']['Cost'],LABOR_Cost_Price_Per,year), 'Price':compound_interest(amount['LABOR']['Price'],LABOR_Cost_Price_Per,year)}})
                    
            if (amount['BOM']['Price'] != 0) or (amount['BOM']['Cost'] != 0):
                if Year_1_to_be_Escalated == 'Yes':
                    NewWriteIns.append({ WriteInIDs['BOM'] :{'Year': "Year "+str(year) ,'Cost':compound_interest(amount['BOM']['Cost'],BOM_Cost_Per,year), 'Price':compound_interest(amount['BOM']['Price'],BOM_Price_Per,year)}})
                else:
                    if year > 1:
                        NewWriteIns.append({ WriteInIDs['BOM'] :{'Year': "Year "+str(year) ,'Cost':compound_interest(amount['BOM']['Cost'],BOM_Cost_Per,year-1), 'Price':compound_interest(amount['BOM']['Price'],BOM_Price_Per,year-1)}})

            
    Product = ProductHelper.CreateProduct(WriteInMasterProduct)
    validPartsCon = Product.GetContainerByName("WriteInProduct")

    for item in NewWriteIns:
        for key,value in item.items():
            writeInProductInfo = getWriteInProductInfo(key)
            if writeInProductInfo is not None:
                PopulateValidPartsCon(validPartsCon,key, str(value['Price']), str(value['Cost']), str(value['Year']),writeInProductInfo)
        
    validPartsCon.MakeAllRowsSelected()
    validPartsCon.Calculate()
    product = Product.AddToQuote()

    
#for i in NewWriteIns:
#    Log.Write("new - "+str(i))

#for i in raw_list:
#    Log.Write("raw_list - "+str(i))
    
#Log.Write("CA_LCM_MultiYear_Escalation_Writein_Population : Ended For Quote - "+Quote.CompositeNumber)