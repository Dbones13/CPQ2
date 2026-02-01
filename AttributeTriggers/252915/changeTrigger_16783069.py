import math as m
def getFloat(Var):
    if Var:
        return float(Var)
    return 0
C24 = getFloat (Product.Attr('TPA_Count_of_application_blocks_in_department').GetValue())
C18 = getFloat (Product.Attr('TPA_Total_IO_Count_in_existing_system').GetValue())
C43 = getFloat (Product.Attr('TPA_Total_amount_of_IOC_cards_which_are_now_in_existing_system').GetValue())
C25 = getFloat (Product.Attr('TPA_How_many_MD_control_packages_are_done_in_TPA_PMD').GetValue())
C26 = getFloat (Product.Attr('TPA_How_many_CD_control_packages_are_done_in_TPA_PMD').GetValue())
C27 = getFloat (Product.Attr('TPA_How_many_Line_drive_packages_are_done_in_TPA').GetValue())
value = 0
value += max(C24/2000,C18/2000,C43/8)
if C25 == 0 and C26 > 0:
    value+=1
else:
    value += C25
value += C27

finalvalue = m.ceil( value)
Product.Attr('TPA_Calculated_amount_of_FCEs_to_be_included_in_new_system').AssignValue(str(finalvalue))
