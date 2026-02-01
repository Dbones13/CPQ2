import GS_SC_OPB_SESP_Module as OSM
productType = Product.Attr('SC_Product_Type').GetValue()

if productType == "Renewal" and Product.Attr('SC_SESP_Renewal_Check').GetValue() == "0":
    OSM.insertVRWInfo(Product, Quote, TagParserQuote, Session)
    Product.Attr('SC_SESP_Renewal_Check').AssignValue('1')