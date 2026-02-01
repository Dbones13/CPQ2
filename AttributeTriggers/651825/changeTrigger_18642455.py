getval = Product.Attr('SerC_CG_Percent_SpareSpace_Marshalling_Cabinet').GetValue()
if Product.Attr('SerC_CG_Marshalling_Cabinet_Type').GetValue() in ('Universal Marshalling'):
    Product.Attr('SerC_CG_Percentage_of_Spare_Space_required(0-100%)').AssignValue(getval)