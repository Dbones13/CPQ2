NumofTPA = Product.Attr('TPA_Do_you_know_the_number_of_huge_and_normal_TPA_PMD_HMI_graphics').GetValue()
if NumofTPA == "Yes":
    Product.Attr('TPA_Count_of_huge_TPA_PMD_HMI_graphics').AssignValue(str(0))
    Product.Attr('TPA_Count_of_normal_TPA_PMD_HMI_graphics').AssignValue(str(0))
    Product.Attr('TPA_Count_of_popup_displays').AssignValue(str(0))
else:
    Product.Attr('TPA_Total_Count_of_TPA_PMD_HMI_graphics_and_popups').AssignValue(str(0))