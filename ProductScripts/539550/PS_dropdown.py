import datetime

#CXCPQ-23784
#The following sets the proper value of 'Execution Year' in the Labor Container, based on the Contract Start Date in the Quote:
current_year = datetime.datetime.now().year

years_list = Product.Attr('CE PMD Engineering Execution Year').Values
for year in years_list:
    if int(year.ValueCode) in range(current_year + 4, 2037):
        Product.DisallowAttrValues('CE PMD Engineering Execution Year', year.ValueCode)
    elif int(year.ValueCode) < current_year:
        Product.DisallowAttrValues('CE PMD Engineering Execution Year', year.ValueCode)
years_list_cd = Product.Attr('PMD_CD_LD_Engineering_Execution_Year').Values
for year in years_list_cd:
    if int(year.ValueCode) in range(current_year + 4, 2037):
        Product.DisallowAttrValues('PMD_CD_LD_Engineering_Execution_Year', year.ValueCode)
    elif int(year.ValueCode) < current_year:
        Product.DisallowAttrValues('PMD_CD_LD_Engineering_Execution_Year', year.ValueCode)

now = datetime.datetime.now().year

psupply = Product.GetContainerByName('PMD_labour_cont_1').Rows[0].GetColumnByName('PMD_exe_year')
value_list = psupply.ReferencingAttribute.Values

for i in value_list:
    if int(i.ValueCode) in range(now+4,2036):
    	i.Allowed = False