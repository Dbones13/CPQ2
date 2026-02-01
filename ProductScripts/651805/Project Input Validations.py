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

if Quote.GetCustomField('R2QFlag').Content == 'Yes':
    for i in Product.GetContainerByName('HCI_PHD_USMConfiguration').Rows:
        i.Columns['Number of Historised Monitor Items'].Value='0'
        i.Columns['Number of Monitor Items'].Value='0'
        i.Columns['USM Configuration'].Value='0'
    for i in Product.GetContainerByName('HCI_PHD_VirtualCalculations').Rows:
        i.Columns['Number of medium virtual calculations'].Value='0'
        i.Columns['Virtual Calculations'].Value='0'
    for i in Product.GetContainerByName('HCI_PHD_Hardware').Rows:
        i.Columns['Total number of servers'].Value='2'
        i.Columns['Hardware'].Value='2'
    for i in Product.GetContainerByName('HCI_PHD_MigratedDisplaysforInsight').Rows:
        i.Columns['Number of typical displays migrated from Experion'].Value='0'
        i.Columns['Migrated Displays for Insight'].Value='0'
    for i in Product.GetContainerByName('HCI_PHD_CrystalReports').Rows:
        i.Columns['Number of medium reports'].Value='0'
        i.Columns['Crystal Reports'].Value='0'
    for i in Product.GetContainerByName('HCI_PHD_SSRS_Reports').Rows:
        i.Columns['Number of medium reports'].Value='0'
        i.Columns['SQL Server Reporting Services (SSRS) Reports'].Value='0'
    '''for i in Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows:
        i.GetColumnByName('USM Implementation').SetAttributeValue('No')
        i.Calculate()
		#Log.Info(str(i.Columns['USM Implementation'].Value)+"-----------PHDLabor---------->"+str()+"--->"+str())
	Product.DisallowAttr('HCI_PHD_USMConfiguration')'''

scopeDict2={}
if Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows.Count>0:
    contRows=Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows[0].Columns
    for col in contRows:
        scopeDict2[col.Name]=col.Value
    if scopeDict2['USM Implementation']=='Yes':
        Product.AllowAttr('HCI_PHD_USMConfiguration')
    else:
        Product.DisallowAttr('HCI_PHD_USMConfiguration')
    Trace.Write('-scopedict2-'+str(scopeDict2['Graphics and Reports']))

    if scopeDict2['Graphics and Reports']=='No':
        Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('No')
        '''Product.DisallowAttr('HCI_PHD_NewDisplaysforInsight')
        Product.DisallowAttr('HCI_PHD_ExcelReports')
        Product.DisallowAttr('HCI_PHD_MigratedDisplaysforInsight')
        Product.DisallowAttr('HCI_PHD_CrystalReports')
        Product.DisallowAttr('HCI_PHD_SSRS_Reports')'''
    else:
        Product.Attributes.GetByName('HCI_PHD_IsReports').AssignValue('Yes')
        '''Product.AllowAttr('HCI_PHD_NewDisplaysforInsight')
        Product.AllowAttr('HCI_PHD_ExcelReports')
        Product.AllowAttr('HCI_PHD_MigratedDisplaysforInsight')
        Product.AllowAttr('HCI_PHD_CrystalReports')
        Product.AllowAttr('HCI_PHD_SSRS_Reports')'''
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
        Product.Attributes.GetByName('HCI_PHD_IsRequired').SelectDisplayValue('1')
    else:
        Product.ResetAttr('HCI_PHD_IsRequired')


#if Quote.GetCustomField('IsR2QRequest').Content == 'Yes':
    #Log.Info("---labor---123--------->"+str(Product.Attr('Trigger_r2q_rules').GetValue()))
	#Product.Attributes.GetByName('Trigger_r2q_rules').AssignValue('True')