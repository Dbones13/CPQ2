tempData = Product.Attr('Temporary Data').GetValue()
if not tempData:
    temp_data= {'C200_UOC_var_9': 0, 'C300_var_2': 0, 'C300_var_11': 0}
    Product.Attr('Temporary Data').AssignValue(str(temp_data))