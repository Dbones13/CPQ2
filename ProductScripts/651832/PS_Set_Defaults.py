def getContainer(Name):
    return Product.GetContainerByName(Name)

Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))

application = Product.Name.split(" ")[-1]
attrs = ["SM_Hardware_Builder_Station_Cont", "SM_Hardware_Simulation_Station_Cont", "SM_Hardware_Historian_Station_Cont", "Number_SM_Control_Groups_Cont","SM_Common_Questions","SM_Labor_Cont"]
for attr in attrs:
    container = getContainer(attr)
    #Trace.Write(attr)
    if container.Rows.Count == 0:
        row = container.AddNewRow(False)
        if attr == 'SM_Labor_Cont':
                row['GES_Location'] = 'None'
        elif attr == 'SM_Common_Questions':
            common_questions = {'SM_System_Scope':'Hardware and Software', 'SM_Historian_Basic_SW':'None', 'SM_Historian_Basic_Database_Ext':'None', 'SM_Historian_Basic_Server_1Client':'None', 'SM_Historian_Server_Upgrade':'0', 'SM_Physical_Media_Kit': '0', 'SM_Controller_Simulation_License':'0', 'SM_Builder_Concurrent_User_License':'0','Experion Software Release':'R530',  'SM_Cluster':'Cluster 1'}
            for col in common_questions.keys():
                default_value = common_questions[col]
                row.SetColumnValue(col, default_value)
                if default_value != '0':
                    row.GetColumnByName(col).SetAttributeValue(default_value)
        elif attr in ['SM_Hardware_Builder_Station_Cont', 'SM_Hardware_Simulation_Station_Cont', 'SM_Hardware_Historian_Station_Cont']:
            questions = {'SM_Builder_Station_Required':'0','SM_Simulation_Station_Required': '0','SM_Historian_Station_Required':'0', 'Station_Type':'STN_STD_DELL_Tower_NonRAID', 'Node_Supplier':'Honeywell'}
            if attr == 'SM_Hardware_Builder_Station_Cont':
                del questions['SM_Historian_Station_Required']
                del questions['SM_Simulation_Station_Required']
                del questions['Node_Supplier']
            elif attr == 'SM_Hardware_Historian_Station_Cont':
                del questions['SM_Builder_Station_Required']
                del questions['SM_Simulation_Station_Required']
                del questions['Node_Supplier']
            elif attr == 'SM_Hardware_Simulation_Station_Cont':
                del questions['SM_Builder_Station_Required']
                del questions['SM_Historian_Station_Required']
                del questions['Node_Supplier']
            for col in questions.keys():
                default_value = questions[col]
                row.SetColumnValue(col, default_value)
                if default_value != '0':
                    row.GetColumnByName(col).SetAttributeValue(default_value)
        elif  attr == 'Number_SM_Control_Groups_Cont':
            row.SetColumnValue('Number_SM_Control_Groups', '1')
        row.Calculate()
    container.Calculate()
if Product.GetContainerByName('Number_SM_Control_Groups_Cont').Rows.Count > 0:
    label = Product.GetContainerByName('Number_SM_Control_Groups_Cont').Rows[0]
    label.GetColumnByName('Number_SM_Control_Groups').HeaderLabel = "Number of Safety Manager System Control Groups (1-10)"
Product.GetContainerByName('SM_Labor_Cont').Rows[0].SetColumnValue('Implementation_Methodology','StandardBuildEstimate')
Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('Implementation_Methodology').SetAttributeValue('Standard Build Estimate')