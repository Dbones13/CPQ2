#Update_System_Labor_Cost_Price
from GS_Labor_Utils import getFloat, add_to_dict, checkForMPACustomer, populatePriceCost
import GS_Pouplate_UOC_Labor_Price_Cost as Labor_Price_Cost
import GS_GetPriceFromCPS as cps

def getYearPrice(Quote,power, partNumber, salesOrg, LOB,TagParserQuote, listPriceDict): #Needs the quote for the pricebook call
    query = "Select * from YOY_INFLATION_RATE where salesOrg = '{0}' and LOB = '{1}'".format(salesOrg,LOB)
    res = SqlHelper.GetFirst(query)
    price = listPriceDict.get(partNumber, 0)
    if power==1 and res is not None:
        inflationRate1 = float(res.Inflation_Rate)
        price = float(price) * getFloat(1 + inflationRate1 )
    elif power==2 and res is not None:
        inflationRate1 = float(res.Inflation_Rate)
        inflationRate2 = float(res.Inflation_Rate_Year2)
        price = float(price) * getFloat(1 + inflationRate1 ) * getFloat(1 + inflationRate2 )
    elif power==3 and res is not None:
        inflationRate1 = float(res.Inflation_Rate)
        inflationRate2 = float(res.Inflation_Rate_Year2)
        inflationRate3 = float(res.Inflation_Rate_Year3)
        price = float(price) * getFloat(1 + inflationRate1 ) * getFloat(1 + inflationRate2 ) * getFloat(1 + inflationRate3 )
    if price:
        return getFloat(price)
    return 0.0

def populateListPrice(Quote,row, salesOrg, LOB, parts_dict, TagParserQuote, fo_dict, listPriceDict): #sets List Price
    final_hours = getFloat(row["Final Hrs"])
    ges_split = getFloat(row["GES Eng % Split"]) * 0.01
    ges_eng = row['GES Eng'] if row['GES Eng'] != '' else 'None'
    try: #For custom deliverables
        fo1_split = getFloat(row["FO Eng % Split"]) * 0.01
        fo2_split = 0.0
        fo1_eng = row.GetColumnByName('FO Eng').DisplayValue
        fo2_eng = 'None'
    except: #For standard labor deliverables
        fo1_split = getFloat(row["FO Eng 1 % Split"]) * 0.01
        fo2_split = getFloat(row["FO Eng 2 % Split"]) * 0.01
        fo1_eng = row.GetColumnByName('FO Eng 1').DisplayValue
        fo2_eng = row.GetColumnByName('FO Eng 2').DisplayValue

    if fo1_eng != 'None':
        fo1_eng = fo_dict.get(fo1_eng, '')
    if fo2_eng != 'None':
        fo2_eng = fo_dict.get(fo2_eng, '')

    currentYear = DateTime.Now.Year
    year_diff = int(row["Execution Year"]) - currentYear
    gesFinalHours = round(getFloat(row["Final Hrs"]) * ges_split)
    fo_ENG1_FinalHours = round(getFloat(row["Final Hrs"]) * fo1_split)
    fo_ENG2_FinalHours = round(getFloat(row["Final Hrs"]) * fo2_split)

    #Calcuates and sets GES List Price
    #Trace.Write("final_hours={} ges_split={} ges_eng={}".format(final_hours, ges_split, ges_eng))
    if final_hours != 0 and ges_split != 0 and ges_eng != "None":
        ges_unit_price = getYearPrice(Quote,year_diff, row["GES Eng"], salesOrg, LOB,TagParserQuote, listPriceDict)
        ges_total_price = round((gesFinalHours * ges_unit_price), 2)
        parts_dict = add_to_dict(parts_dict, ges_eng, 'ListPrice', ges_total_price)
    else: ges_total_price = 0.0

    #Calculates and sets FO List Price
    #Trace.Write("final_hours={} fo1_split={} fo1_eng={}".format(final_hours, fo1_split, fo1_eng))
    if final_hours != 0 and fo1_split != 0 and fo1_eng != "None":
        fo1_unit_price = getYearPrice(Quote,year_diff, fo1_eng, salesOrg, LOB,TagParserQuote, listPriceDict)
        fo1_total_price = round((fo_ENG1_FinalHours * fo1_unit_price), 2)
        parts_dict = add_to_dict(parts_dict, fo1_eng, 'ListPrice', fo1_total_price)
        #Trace.Write("partDICT:{}".format(str(parts_dict)))
    else: fo1_total_price = 0.0

    if final_hours != 0 and fo2_split != 0 and fo2_eng != "None":
        fo2_unit_price = getYearPrice(Quote,year_diff, fo2_eng, salesOrg, LOB,TagParserQuote, listPriceDict)
        fo2_total_price = round((fo_ENG2_FinalHours * fo2_unit_price), 2)
        parts_dict = add_to_dict(parts_dict, fo2_eng, 'ListPrice', fo2_total_price) #add_to_dict is run two separate times because the service materials might be different
    else: fo2_total_price = 0.0

    fo_total_price =  fo1_total_price + fo2_total_price
    #Trace.Write("FO_ListPrice={}".format(fo_total_price))
    row["FO_ListPrice"] = str(fo_total_price)
    row["GES_ListPrice"] = str(ges_total_price)
    return parts_dict

def consolidateParts(Quote, Product, TagParserQuote, parts_dict, laborCont, fo_dict, checkMPA, salesOrg, LOB, listPriceDict):
    if laborCont.Rows.Count > 0 and Quote:
        for row in laborCont.Rows:
            try:
                Trace.Write("ebr--3--"+str([parts_dict, fo_dict]))
                parts_dict = Labor_Price_Cost.populateCost(Quote, row, parts_dict, fo_dict)
                if checkMPA:
                    parts_dict = Labor_Price_Cost.populate_MPA_Price(row, Product, Quote, parts_dict, fo_dict)
            except Exception,e:
                msg = "Error when Calculating Pricing Error: {0}, Line Number: {1}".format(e, '82')
                Trace.Write(msg)
            try:
                parts_dict = populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, fo_dict, listPriceDict)
            except Exception,e:
                msg = "Error when Calculating ListPice: {0}, Line Number: {1}".format(e, '87')
                Trace.Write(msg)
        laborCont.Calculate()
    return parts_dict

def getUniqueParts(Quote, TagParserQuote, laborCont, columnDict, fo_dict, partList):
    fo_eng = columnDict['fo_eng']
    fo1_eng = columnDict['fo1_eng']
    fo2_eng = columnDict['fo2_eng']
    ges_eng = columnDict['ges_eng']
    partSet = set()
    for row in laborCont.Rows:
        if fo_eng != '':
            if row.GetColumnByName('FO Eng').DisplayValue != '':
                partSet.add(row['FO Eng'])
        else:
            if row.GetColumnByName('FO Eng 1').DisplayValue != '':
                partSet.add(fo_dict.get(row.GetColumnByName('FO Eng 1').DisplayValue))
            if row.GetColumnByName('FO Eng 2').DisplayValue != '':
                partSet.add(fo_dict.get(row.GetColumnByName('FO Eng 2').DisplayValue))
        if ges_eng != '':
            if row['GES Eng'] != '':
                partSet.add(row['GES Eng'])

    if len(partSet) > 0:
        for partNumber in partSet:
            if partNumber not in partList:
                partList.append(partNumber)

#contList = ['System_Network_Engineering_Labor_Container', 'System_Interface_Engineering_Labor_Container', 'Hardware Engineering Labour Container', 'HMI_Engineering_Labor_Container', 'Additional_CustomDev_Labour_Container']
#foEngColumn = {'System_Network_Engineering_Labor_Container':'System_Network_Labor_FO_Eng', 'System_Interface_Engineering_Labor_Container':'System_Interface_Labor_FO_Eng', 'Hardware Engineering Labour Container':'Hardware_Eng_FO_Eng_one', 'HMI_Engineering_Labor_Container':'HMI_Labor_FO_Eng', 'Additional_CustomDev_Labour_Container':'Additional_CustomDev_FO_Eng'}
#gesLoc = None/IN/CN/RO/UZ
#updateParts = True/False

def updateLaborCostPrice(Product, Quote, TagParserQuote, contList, foEngColumn, gesLoc, updateParts, Session=dict()):
    parts_dict = dict()
    checkMPA = checkForMPACustomer(Quote, TagParserQuote)
    salesOrg = Quote.GetCustomField('Sales Area').Content
    LOB = Quote.GetCustomField("Booking LOB").Content
    columnDict =  dict()
    listPriceDict = dict()
    partList = []
    EBRvalue=''
    EBRvalue1=''
    #Get unique list of price from all labor containers
    for cont in contList:
        if Product.Name =='Experion Enterprise System' and cont=='EBR_Engineering_Labor_Container':
            EBRvalue = Product.Attr('EBR_Software_Required').GetValue()
        if EBRvalue!='Yes':
            laborCont = Product.GetContainerByName(cont)
            if laborCont.Rows.Count > 0:
                foEngColumnName = foEngColumn[cont]
                row0 = laborCont.Rows[0]
                fo_dict = dict()
                fo_ld = row0.Product.Attr(foEngColumnName)
                fo_dict = Labor_Price_Cost.buildDict(fo_ld)
                try:
                    foEng = row0.GetColumnByName('FO Eng').DisplayValue
                    columnDict['fo_eng'] = 'FO Eng'
                    columnDict['fo1_eng'] = ''
                    columnDict['fo2_eng'] = ''
                except:
                    columnDict['fo_eng'] = ''
                    columnDict['fo1_eng'] = 'FO Eng 1'
                    columnDict['fo2_eng'] = 'FO Eng 2'
                columnDict['ges_eng'] = ''
                if gesLoc != 'None':
                    columnDict['ges_eng'] = 'GES Eng'
                getUniqueParts(Quote, TagParserQuote, laborCont, columnDict, fo_dict, partList)
    #Get price for all unique labor parts
    if len(partList) > 0:
        listPriceDict = cps.getPrice(Quote, {}, partList, TagParserQuote, Session)
    #Update price information in all labor containers
    for cont in contList:
        if Product.Name =='Experion Enterprise System' and cont=='EBR_Engineering_Labor_Container':
            EBRvalue1 = Product.Attr('EBR_Software_Required').GetValue()
        if EBRvalue1!='Yes':
            laborCont = Product.GetContainerByName(cont)
            if laborCont.Rows.Count > 0:
                foEngColumnName = foEngColumn[cont]
                row0 = laborCont.Rows[0]
                fo_dict = dict()
                fo_ld = row0.Product.Attr(foEngColumnName)
                fo_dict = Labor_Price_Cost.buildDict(fo_ld)
                Trace.Write("EBR--1--"+str([parts_dict,laborCont,fo_dict,checkMPA,salesOrg,LOB,listPriceDict]))
                parts_dict = consolidateParts(Quote, Product, TagParserQuote, parts_dict, laborCont, fo_dict, checkMPA, salesOrg, LOB, listPriceDict)
                Trace.Write("in--ebr2--"+str(parts_dict))

    if updateParts:
        populatePriceCost(Product, parts_dict)