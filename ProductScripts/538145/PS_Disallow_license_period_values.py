license_period = 1
if Quote:
    contract_duration = Quote.GetCustomField('SC_CF_CONTRACTDURYR').Content
    if contract_duration != "":
        contract_duration = contract_duration.split()
        if int(eval(contract_duration[0])) < float(contract_duration[0]):
            contract_duration[0] = int(eval(contract_duration[0])) + 1
        else:
            contract_duration[0] = int(eval(contract_duration[0]))
        license_period = contract_duration[0]
        if license_period > 5:
            license_period = 5
try:
    license_year = Product.Attr('SC_License_period_Year').GetValue()
    years_support = Product.Attr('SC_Years_of_Support').GetValue()
    disallowed_values = [i for i in range(6) if i>int(license_period)]
    for j in disallowed_values:
        Product.DisallowAttrValues('SC_License_period_Year',str(j))
    SC_Disallowed_Values = Product.Attr('SC_Disallowed_Values').GetValue()
    
    if int(SC_Disallowed_Values) != license_period:
        if int(SC_Disallowed_Values) <= 5 and license_period <= 5:
            Trace.Write('inside if')
            Product.Attr('SC_License_period_Year').SelectValue(str(license_period))
            Product.Attr('SC_Disallowed_Values').AssignValue(str(license_period))
            
        else:
            Trace.Write('inside else')
            Product.Attr('SC_License_period_Year').SelectValue('5')
            Product.Attr('SC_Disallowed_Values').AssignValue('5')
        if license_period <= 3:
            Product.Attr('SC_Years_of_Support').AssignValue(str(license_period))
        else:
            Product.Attr('SC_Years_of_Support').AssignValue('3')
except:
    pass