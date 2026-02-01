percentage = Product.Attr('SerC_CG_R2Q_Percent_Installed_Spare').GetValue()
if percentage:
    Product.Attr('SerC_CG_Percent_Installed_Spare').AssignValue(percentage)