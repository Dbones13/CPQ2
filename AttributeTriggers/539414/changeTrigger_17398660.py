if Product.Attr('CWS_Mig_Number_of_die_bolts').GetValue() == '':
    Product.Attr('CWS_Mig_Number_of_die_bolts').AssignValue('1')