priceCont = Product.GetContainerByName('CBM_Pricing_Container').Rows
SC_Product_Type = Product.Attr("SC_Product_Type").GetValue()
for row in priceCont:
    productFamily = row["CY_ProductFamily"]
    assetType = row["CY_AssetType"]
    if productFamily == "" or productFamily is None or assetType == "" or assetType is None:
        Product.ResetAttr('CBM_INCOMPELETE')
        break
    else:
        Product.Attr("CBM_INCOMPELETE").AssignValue("1")
for row in priceCont:
    productFamilyopb = row["CBM_Product_Family_OPB"]
    assetTypeopb = row["CBM_Asset_Type_OPB"]
    if SC_Product_Type == 'Renewal': #and Quote.GetCustomField('SC_CF_Parent_Quote_Number_Link').Content == "":
        if productFamilyopb == "" or productFamilyopb is None or assetTypeopb == "" or assetTypeopb is None:
            Product.ResetAttr('CBM_INCOMPELETE')
            break