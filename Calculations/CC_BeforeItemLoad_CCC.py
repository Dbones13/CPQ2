from GS_CommonConfig import CL_CommonSettings as CS
if Quote.GetCustomField("Booking LOB").Content == 'CCC' and Quote.GetGlobal('PerformanceUpload') != 'Yes' and len(CS.setBeforeQuoteItems)>0:
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