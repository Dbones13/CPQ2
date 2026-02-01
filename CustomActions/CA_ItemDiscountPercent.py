import GS_QuoteTotalTablesUtil as qtUtil
from GS_CalculateTotals import getWriteInProductType
quote = Quote
quoteDetails = quote.QuoteTables["Quote_Details"].Rows[0]
productLineDetails = quote.QuoteTables["Product_Line_Details"]
plsgDetails = quote.QuoteTables["Product_Line_Sub_Group_Details"]
ptDetails = quote.QuoteTables["Product_Type_Details"]
writeInProductType = getWriteInProductType(Quote)

new_Discount = float(quoteDetails["New_Discount"]) if quoteDetails["New_Discount"] != '' else 0.0

if new_Discount != 0.0 or (new_Discount == 0.00 and quoteDetails["Quote_Discount_Percent"] == 0.00):
    qtUtil.applyQuoteDiscountToItems(quote , new_Discount)
    quoteDetails["New_Discount"] = '0.0'

for row in productLineDetails.Rows:
    new_discount = row["New_Discount"]
    sell_price_discount_percent = float(row["Sell_Price_Discount_Percent"])
    if new_discount != 0.0 or row["Sell_Price_Discount_Percent"] == 0.00:
        modified_pl = row["Modified_PL"]
        qtUtil.applyDiscountToItems(quote , 'QI_ProductLine' , modified_pl , float(row["New_Discount"] or 0))
        row["New_Discount"] = 0.0
        row["Modified_PL"] = ""

for row in plsgDetails.Rows:
    new_discount = row["New_Discount"]
    sell_price_discount_percent = float(row["Sell_Price_Discount_Percent"])
    if new_discount != 0.0 or sell_price_discount_percent == 0.0:
        modified_plsg = row["Modified_PLSG"]
        qtUtil.applyDiscountToItems(quote , 'QI_PLSG' , modified_plsg , float(row["New_Discount"] or 0))
        row["New_Discount"] = 0.0
        row["Modified_PLSG"] = ""

for row in ptDetails.Rows:
    new_discount = row["New_Discount"]
    sell_price_discount_percent = float(row["Sell_Price_Discount_Percent"])
    if new_discount != 0.0 or sell_price_discount_percent == 0.0:
        modified_pt = row["Modified_PT"]
        qtUtil.applyProductTypeDiscountToItems(quote, modified_pt , row["New_Discount"], writeInProductType)
        row["New_Discount"] = 0.0
        row["Modified_PT"] = ""