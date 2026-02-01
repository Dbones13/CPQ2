#Update_Labor_Cost_Price
from GS_Labor_Utils import getFloat, add_to_dict, checkForMPACustomer, laborCostWithConversion
import GS_Pouplate_UOC_Labor_Price_Cost as PM_Price_Cost
import GS_GetPriceFromCPS as cps

"""
def getListPrice(partNumber, containerRows):
    res = {}
    for row in containerRows:
        if row['PartNumber'] in partNumber:
            res[row['PartNumber']] = row['ListPrice']
    return res
"""

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
    ges_eng = row['GES Eng']
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
    ##Trace.Write("final_hours={} ges_split={} ges_eng={}".format(final_hours, ges_split, ges_eng))
    if final_hours != 0 and ges_split != 0 and ges_eng != "None":
        ges_unit_price = getYearPrice(Quote,year_diff, row["GES Eng"], salesOrg, LOB,TagParserQuote, listPriceDict)
        ges_total_price = round((gesFinalHours * ges_unit_price), 2)
        parts_dict = add_to_dict(parts_dict, ges_eng, 'ListPrice', ges_total_price)
    else: ges_total_price = 0.0

    #Calculates and sets FO List Price
    ##Trace.Write("final_hours={} fo1_split={} fo1_eng={}".format(final_hours, fo1_split, fo1_eng))
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
    ##Trace.Write("FO_ListPrice={}".format(fo_total_price))
    row["FO_ListPrice"] = str(fo_total_price)
    row["GES_ListPrice"] = str(ges_total_price)
    return parts_dict

def populatePriceCost(Product, parts_dict, cont):
    rows_by_part_number = {row['Part Number']: row for row in cont.Rows}
    part_numbers_in_dict = set([k for k,i in parts_dict.items() if i["Qty"] > 0 ])
    rows_to_delete = []

    for part, part_info in parts_dict.items():
        if True:
            if part and getFloat(part_info['Qty']) != 0.0:
                existing_row = rows_by_part_number.get(part, None)

                if existing_row:
                    new_row = existing_row
                else:
                    new_row = cont.AddNewRow(part, False)
                    rows_by_part_number[part] = new_row

                new_row['Part Number'] = part
                new_row.GetColumnByName("Qty").ReferencingAttribute.AssignValue(str(part_info['Qty']))
                new_row['Total Cost'] = str(part_info['Cost']) if 'Cost' in part_info else '0.0'
                new_row['Total List Price'] = str(part_info['ListPrice']) if 'ListPrice' in part_info else '0.0'
                new_row['Total WTW Cost'] = str(part_info['WTWCost']) if 'WTWCost' in part_info else '0.0'
                new_row['Total MPA Price'] = str(part_info['MPA']) if 'MPA' in part_info else '0.0'

                item_quantity_attr = next((attr for attr in new_row.Product.Attributes if attr.DisplayType != "Container" and attr.Name == "ItemQuantity"), None)
                if item_quantity_attr:
                    item_quantity_attr.AssignValue(str(part_info['Qty']))

                new_row.ApplyProductChanges()
                new_row.Calculate()

                #except Exception as e:
                #    Trace.Write(str(e))

    part_numbers_in_container = set(rows_by_part_number.keys())
    rows_to_delete = part_numbers_in_container - part_numbers_in_dict
    
    for part_to_delete in rows_to_delete:
        if True:
            row_to_delete = rows_by_part_number[part_to_delete]
            cont.DeleteRow(row_to_delete.RowIndex)
            #except Exception as e:
            
    cont.Calculate()

def consolidateParts(Quote, Product, TagParserQuote,parts_dict, laborCont, fo_dict, checkMPA, salesOrg, LOB, gesloc, listPriceDict):
    if laborCont.Rows.Count > 0 and Quote:
        for row in laborCont.Rows:
            try:
                parts_dict = PM_Price_Cost.populateCost(Quote, row, parts_dict, fo_dict)
                if checkMPA:
                    parts_dict = PM_Price_Cost.populate_MPA_Price(row, Product, Quote, parts_dict, fo_dict)
            except Exception,e:
                msg = "Error when Calculating Pricing Error: {0}, Line Number: {1}".format(e, '110')
                Trace.Write(msg)
            try:
                parts_dict = populateListPrice(Quote,row, salesOrg, LOB, parts_dict,TagParserQuote, fo_dict, listPriceDict)
            except Exception,e:
                msg = "Error when Calculating ListPice: {0}, Line Number: {1}".format(e, '117')
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

def updateLaborCostPrice(Product, Quote, TagParserQuote, contList, updateParts, Session=dict()):
    parts_dict = dict()
    checkMPA = checkForMPACustomer(Quote, TagParserQuote)
    salesOrg = Quote.GetCustomField('Sales Area').Content
    LOB = Quote.GetCustomField("Booking LOB").Content
    gesloc = 'None'
    if Product.GetContainerByName('Labor_Details_New/Expansion_Cont').Rows.Count > 0:
        gesloc = Product.GetContainerByName('Labor_Details_New/Expansion_Cont').Rows[0].GetColumnByName('GES_Location').Value
    ##contList = ['Project_management_Labor_Container', 'Labor_Container', 'PLE_Labor_Container', 'PM_Additional_Custom_Deliverables_Labor_Container']
    foEngColumn = {'Project_management_Labor_Container': 'PM_Labor_FO_Eng_1', 'Labor_Container': 'New_Expansion_Labor_FO_Eng1', 'PLE_Labor_Container':'PLE_Labor_FO1_Eng', 'PM_Additional_Custom_Deliverables_Labor_Container':'Additional_Project_FOENG_Deliverables'}
    columnDict =  dict()
    listPriceDict = dict()
    partList = []
    #Get unique list of price from all labor containers
    for cont in contList:
        laborCont = Product.GetContainerByName(cont)
        if laborCont.Rows.Count > 0:
            foEngColumnName = foEngColumn[cont]
            row0 = laborCont.Rows[0]
            fo_dict = dict()
            fo_ld = row0.Product.Attr(foEngColumnName)
            fo_dict = PM_Price_Cost.buildDict(fo_ld)
            columnDict['fo_eng'] = 'FO Eng' if cont == 'PM_Additional_Custom_Deliverables_Labor_Container' else ''
            columnDict['ges_eng'] = 'GES Eng' if gesloc != "None" and gesloc != "" else ''
            columnDict['fo1_eng'] = 'FO Eng 1' if cont != 'PM_Additional_Custom_Deliverables_Labor_Container' else ''
            columnDict['fo2_eng'] = 'FO Eng 2' if cont != 'PM_Additional_Custom_Deliverables_Labor_Container' else ''
            getUniqueParts(Quote, TagParserQuote, laborCont, columnDict, fo_dict, partList)
    #Get price for all unique labor parts
    if len(partList) > 0:
        listPriceDict = cps.getPrice(Quote, {}, partList, TagParserQuote, Session)
    #Update price information in all labor containers
    for cont in contList:
        laborCont = Product.GetContainerByName(cont)
        if laborCont.Rows.Count > 0:
            foEngColumnName = foEngColumn[cont]
            row0 = laborCont.Rows[0]
            fo_dict = dict()
            fo_ld = row0.Product.Attr(foEngColumnName)
            fo_dict = PM_Price_Cost.buildDict(fo_ld)
            parts_dict = consolidateParts(Quote, Product, TagParserQuote, parts_dict, laborCont, fo_dict, checkMPA, salesOrg, LOB, gesloc, listPriceDict)

    if updateParts:
        cont = Product.GetContainerByName('Labor_PM_PriceCost_Cont')
        #cont.Rows.Clear()
        populatePriceCost(Product, parts_dict, cont)