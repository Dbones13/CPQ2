#PMC_MIQ_Update_System_Labor_Cost_Price
from GS_Labor_Utils import getFloat, add_to_dict, getSalesOrg, getExecutionCountry,laborCostWithDoubleConversion,laborCostWithConversion,getFopartsCost, checkForMPACustomer, populatePriceCost, getMPAPrice
import GS_GetPriceFromCPS as cps

def populateCost(Quote, row, parts_dict):
    error_flag = True
    different_salesOrg = False
    FO_Eng_Unit_WTW_Cost = WTW_Markup_Factor = 0.00
    fo_split = getFloat(row["FO Eng % Split"]) * 0.01
    fo_eng = row["FO Eng"]

    fo_ENG_FinalHours = round(getFloat(row["Final Hrs"]) * fo_split)

    salesOrgCountry = getExecutionCountry(Quote)
    salesOrg = getSalesOrg(row["Execution Country"])

    if row["Execution Country"] != salesOrgCountry:
        different_salesOrg = True
        WTW_Markup_Factor = 0.1

    if row["Final Hrs"] not in ('','0'):
        parts_dict = add_to_dict(parts_dict, fo_eng, 'Qty', fo_ENG_FinalHours)
        add_10_percent = 0.00
        foPartsCost = getFopartsCost(Quote, salesOrg,fo_eng,row["Execution Year"])
        if fo_eng in foPartsCost and foPartsCost[fo_eng]:
            unit_regionalCost = round(getFloat(foPartsCost.get(fo_eng,0)),2)

            if different_salesOrg: #Add 10% if execution country is different from sales org country
                add_10_percent = unit_regionalCost * 0.1

            row["FO_Eng_Unit_Regional_Cost"] = str(unit_regionalCost + add_10_percent)
            FO_Eng_Unit_WTW_Cost = getFloat(row["FO_Eng_Unit_Regional_Cost"]) / (1 + WTW_Markup_Factor)
            fo_total_cost = fo_ENG_FinalHours * getFloat(row["FO_Eng_Unit_Regional_Cost"])
            fo_total_wtw_cost = fo_ENG_FinalHours * getFloat(FO_Eng_Unit_WTW_Cost)
            parts_dict = add_to_dict(parts_dict, fo_eng, 'Cost', fo_total_cost)
            parts_dict = add_to_dict(parts_dict, fo_eng, 'WTWCost', fo_total_wtw_cost)

        else:
            row["FO_Eng_Unit_Regional_Cost"] = "0"
            fo_total_cost = fo_total_wtw_cost = 0.0
            error_flag = ""
    else:
        fo_total_cost = fo_total_wtw_cost = 0.0
        row["FO_Eng_Unit_Regional_Cost"] = "0"

    row["FO_Regional_Cost"] = str(fo_total_cost)
    row["FO_WTW_Cost"] = str(fo_total_wtw_cost)
    row["Error_Message"] = str(error_flag)
    return parts_dict

def populate_MPA_Price(row, Product, Quote, parts_dict):
    if row["Final Hrs"] not in ('','0'):
        FO_ENG_MPA = 0
        fo_split = getFloat(row["FO Eng % Split"]) * 0.01
        fo_eng = row["FO Eng"]

        fo_ENG_FinalHours = round(getFloat(row["Final Hrs"]) * fo_split)
		#FO_MPA_Price
        foeng_mpa = getMPAPrice(row, fo_eng, Product, Quote)
        if fo_eng in foeng_mpa and foeng_mpa[fo_eng]:
            unit_mpaPrice = round(getFloat(foeng_mpa.get(fo_eng,0)),2)
            FO_ENG_MPA = unit_mpaPrice * fo_ENG_FinalHours
            parts_dict = add_to_dict(parts_dict, fo_eng, 'MPA', FO_ENG_MPA)

        row["FO_MPA_Price"] = str(FO_ENG_MPA)
    else:
        row["FO_MPA_Price"] = "0"
    return parts_dict


def getYearPrice(Quote,power, partNumber, salesOrg, LOB,TagParserQuote, listPriceDict): #Needs the quote for the pricebook call
    query = "Select * from YOY_INFLATION_RATE where salesOrg = '{0}' and LOB = '{1}'".format(salesOrg,LOB)
    res = SqlHelper.GetFirst(query)
    price = listPriceDict.get(partNumber, 0)
    if power == 1 and res is not None:
        inflationRate1 = float(res.Inflation_Rate)
        price = float(price) * getFloat(1 + inflationRate1 )
    elif power == 2 and res is not None:
        inflationRate1 = float(res.Inflation_Rate)
        inflationRate2 = float(res.Inflation_Rate_Year2)
        price = float(price) * getFloat(1 + inflationRate1 ) * getFloat(1 + inflationRate2 )
    elif power == 3 and res is not None:
        inflationRate1 = float(res.Inflation_Rate)
        inflationRate2 = float(res.Inflation_Rate_Year2)
        inflationRate3 = float(res.Inflation_Rate_Year3)
        price = float(price) * getFloat(1 + inflationRate1 ) * getFloat(1 + inflationRate2 ) *getFloat(1 + inflationRate3 )
    if price:
        return getFloat(price)
    return 0.0

def populateListPrice(Quote,row, salesOrg, LOB, parts_dict, TagParserQuote, listPriceDict): #sets List Price
    final_hours = getFloat(row["Final Hrs"])
    fo_split = getFloat(row["FO Eng % Split"]) * 0.01
    fo_eng = row["FO Eng"]

    currentYear = DateTime.Now.Year
    year_diff = int(row["Execution Year"]) - currentYear
    fo_ENG_FinalHours = round(getFloat(row["Final Hrs"]) * fo_split)


    #Calculates and sets FO List Price
    if final_hours != 0:
        fo_unit_price = getYearPrice(Quote,year_diff, fo_eng, salesOrg, LOB,TagParserQuote, listPriceDict)
        fo_total_price = round((fo_ENG_FinalHours * fo_unit_price), 2)
        parts_dict = add_to_dict(parts_dict, fo_eng, 'ListPrice', fo_total_price)
    else: fo_total_price = 0.0

    row["FO_ListPrice"] = str(fo_total_price)
    return parts_dict

def consolidateParts(Quote, Product, TagParserQuote, parts_dict, laborCont, checkMPA, salesOrg, LOB, listPriceDict):
    if laborCont.Rows.Count > 0 and Quote:
        for row in laborCont.Rows:
            try:
                parts_dict = populateCost(Quote, row, parts_dict)
                if checkMPA:
                    parts_dict = populate_MPA_Price(row, Product, Quote, parts_dict)
            except Exception,e:
                msg = "Error when Calculating Pricing Error: {0}, Line Number: {1}".format(e, '82')
            try:
                parts_dict = populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, listPriceDict)
            except Exception,e:
                msg = "Error when Calculating ListPice: {0}, Line Number: {1}".format(e, '87')
        laborCont.Calculate()
    return parts_dict



def updateLaborCostPrice(Product, Quote, TagParserQuote, contList, updateParts, partList, Session):
    parts_dict = dict()
    checkMPA = checkForMPACustomer(Quote, TagParserQuote)
    salesOrg = Quote.GetCustomField('Sales Area').Content
    LOB = Quote.GetCustomField("Booking LOB").Content
    listPriceDict = dict()
    if len(partList) > 0:
        listPriceDict = cps.getPrice(Quote, {}, partList, TagParserQuote, Session)
    #Update price information in all labor containers
    for cont in contList:
        laborCont = Product.GetContainerByName(cont)
        if laborCont.Rows.Count > 0:
            parts_dict = consolidateParts(Quote, Product, TagParserQuote, parts_dict, laborCont, checkMPA, salesOrg, LOB, listPriceDict)

    if updateParts:
        populatePriceCost(Product, parts_dict)