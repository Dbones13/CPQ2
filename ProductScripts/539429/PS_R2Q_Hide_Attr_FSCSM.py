def hideAttr(attrList):
    for attr in attrList:
        Product.Attr(attr).Access = AttributeAccess.Hidden

nonR2QAttr = ["FSC_to_SM_Has_the_System_Audit_been_performed","ATT_FSC_to_SM_On_Site_Eng_hours", "ATT_FSC_to_SM_In_Office_Eng_hours"]

isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
    Product.Attr('R2QRequest').AssignValue('Yes')
    Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
    hideAttr(nonR2QAttr)