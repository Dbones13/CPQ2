if Product.Attr('QCS_Mig_Number_of_die_bolts').GetValue() == '':
    Product.Attr('QCS_Mig_Number_of_die_bolts').AssignValue('1')