from datetime import datetime
product = Product
# Get the current year
current_year = datetime.now().year
execution_year = product.Attr('AR_HCI_EXECUTION_YEAR').GetValue()
execution_year_dropdown = product.Attr('AR_HCI_EXECUTION_YEAR').Values
for value in execution_year_dropdown:
    if str(value.ValueCode) == str(current_year):
        showValues =  [str(year) for year in range(current_year, current_year + 4)]
        Trace.Write('Generated list: ' + str(showValues))
hideValues = [value.ValueCode for value in execution_year_dropdown if str(value.ValueCode) not in showValues]
product.DisallowAttrValues('AR_HCI_EXECUTION_YEAR',*hideValues)
product.AllowAttrValues('AR_HCI_EXECUTION_YEAR',*showValues)