from datetime import datetime
product = Product
current_year = datetime.now().year
execution_year_dropdown = product.Attr('HCI_PHD_Execution_Year').Values
for value in execution_year_dropdown:
    if str(value.ValueCode) == str(current_year):
        showValues =  [str(year) for year in range(current_year, current_year + 4)]
        Trace.Write('Generated list: ' + str(showValues))
hideValues = [value.ValueCode for value in execution_year_dropdown if str(value.ValueCode) not in showValues]
product.DisallowAttrValues('HCI_PHD_Execution_Year',*hideValues)
product.AllowAttrValues('HCI_PHD_Execution_Year',*showValues)

contRows=Product.GetContainerByName('HCI_PHD_AdditionalDeliverables').Rows
if contRows.Count>1:
    inCompleteFlg=0
    for row in contRows:
        if row['Hidden_lable']!='Total':
            if row['Final Hrs'] and float(row['Final Hrs'])>0:
                if row['Eng']=='None' or row['Deliverable']=='None':
                    inCompleteFlg=1
                    break
    if inCompleteFlg==0:
        Product.Attributes.GetByName('HCI_PHD_IsRequiredUNI').SelectDisplayValue('1')
    else:
        Product.ResetAttr('HCI_PHD_IsRequiredUNI')