import math as m
def getFloat(Var):
    if Var:
        return float(Var)
    return 0
doUKnow = Product.Attr('TPA_Do_you_know_the_number_of_huge_and_normal_TPA_PMD_HMI_graphics').GetValue()
if doUKnow == "No":
    value = getFloat (Product.Attr('TPA_Total_Count_of_TPA_PMD_HMI_graphics_and_popups').GetValue())

    huge = m.ceil(value * 0.05 )
    normal = m.ceil(value * 0.25)
    popup = value - huge - normal

    Product.Attr('TPA_Count_of_huge_TPA_PMD_HMI_graphics').AssignValue(str(huge))
    Product.Attr('TPA_Count_of_normal_TPA_PMD_HMI_graphics').AssignValue(str(normal))
    Product.Attr('TPA_Count_of_popup_displays').AssignValue(str(popup))