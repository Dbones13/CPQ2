import GS_R2Q_Migration_Default_Values

nonR2QAttr = ["FSC_SM_IO_Total_ Calculated_SIC_cables"]

isR2QProduct = True if Quote.GetCustomField("isR2QRequest").Content == "Yes" else False

if isR2QProduct:
    for contColumn in nonR2QAttr:
        Product.Attr('FSC_SM_IO_Total_ Calculated_SIC_cables').Access = AttributeAccess.Hidden