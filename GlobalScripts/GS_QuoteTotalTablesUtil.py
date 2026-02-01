from GS_Labor_Utils import getFloat

def applyDiscountToItems(quote , fieldToCompare , fieldValue , discount):
    nonDiscountableParts = ['CEPS_CAD','CEPS_PE','CEPS_PM','D4418111','D4418113','SVC-PER-DIEM','SVC-PMC-TRAV-AIR','SVC-PMC-TRAV-CAR','SVC-PMC-TRAV-PVT','ECSA-1001','ECSP-1001']
    nonDiscountablePLSG  = ['7725-7D38','7029-7179','7076-7000']
    for item in quote.Items:
        val = item[fieldToCompare].Value
        if val == fieldValue and item.QI_ProductLine.Value not in ("") and item.PartNumber not in nonDiscountableParts and item.QI_PLSG.Value not in nonDiscountablePLSG:
            item.QI_Additional_Discount_Percent.Value = discount

    #quote.Calculate(2)

def applyQuoteDiscountToItems(quote , discount):
    nonDiscountableParts = ['CEPS_CAD','CEPS_PE','CEPS_PM','D4418111','D4418113','SVC-PER-DIEM','SVC-PMC-TRAV-AIR','SVC-PMC-TRAV-CAR','SVC-PMC-TRAV-PVT','ECSA-1001','ECSP-1001']
    nonDiscountablePLSG  = ['7725-7D38','7029-7179','7076-7000']
    for item in quote.Items:
        if item.QI_ProductLine.Value not in ("") and item.PartNumber not in nonDiscountableParts and item.QI_PLSG.Value not in nonDiscountablePLSG:
            item.QI_Additional_Discount_Percent.Value = discount

    #quote.Calculate(2)

def applyProductTypeDiscountToItems(quote , fieldValue , discount, writeInProductType = {}):
    nonDiscountableParts = ['CEPS_CAD','CEPS_PE','CEPS_PM','D4418111','D4418113','SVC-PER-DIEM','SVC-PMC-TRAV-AIR','SVC-PMC-TRAV-CAR','SVC-PMC-TRAV-PVT','ECSA-1001','ECSP-1001']
    nonDiscountablePLSG  = ['7725-7D38','7029-7179','7076-7000']
    for item in quote.Items:
        itemProductTypeName = item.ProductTypeName
        if itemProductTypeName == 'Write-In':
            itemProductTypeName = writeInProductType.get(item.PartNumber, item.ProductTypeName)
        if itemProductTypeName == fieldValue and item.QI_ProductLine.Value not in ("") and item.PartNumber not in nonDiscountableParts and item.QI_PLSG.Value not in nonDiscountablePLSG:
            item.QI_Additional_Discount_Percent.Value = discount

    #quote.Calculate(2)

def applyLaborMPAToItems(quote , fieldValue , productLine , value):
    for item in quote.Items:
        itemProductTypeName = item.ProductTypeName
        if itemProductTypeName == 'Honeywell Labor' and item[fieldValue].Value == productLine:
            item.Training_QI_Gst_KP.Value = value