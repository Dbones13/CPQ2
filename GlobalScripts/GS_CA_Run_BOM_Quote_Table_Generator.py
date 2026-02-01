systems_list1 = ['ControlEdge PLC System','PMD System','ControlEdge RTU System','ControlEdge UOC System','Safety Manager ESD','Safety Manager FGS','Safety Manager BMS','Safety Manager HIPPS','Experion Enterprise System','3rd Party Devices/Systems Interface (SCADA)']
systems_list2 = ['ARO, RESS & ERG System','Experion MX System','MXProLine System','Digital Video Manager','Field Device Manager','Electrical Substation Data Collector','Simulation System','eServer System']
systems_list3 = ['Experion HS System', 'HC900 System', 'PlantCruise System', 'ControlEdge PCD System','Terminal Manager', 'Measurement IQ System', 'MasterLogic-50 Generic', 'MasterLogic-200 Generic','Experion LX Generic', 'Generic System', 'Virtualization System', 'C300 System','Variable Frequency Drive System']
systems_list4 = ['Tank Gauging Engineering','Industrial Security (Access Control)','Fire Detection & Alarm Engineering','Skid and Instruments','Small Volume Prover']
ScriptExecutor.ExecuteGlobal('GS_BOM_QT_TABLE_LOAD')
quoteTable = Quote.QuoteTables["BOM_Table_for_Proposals"]
quoteTable.Rows.Clear()
names_table = Quote.QuoteTables["PAS_BOM_Group_Names"]
names_table.Rows.Clear()
if Quote.GetCustomField("Quote Type").Content=='Projects':
    execute1= ''
    execute2= ''
    execute3= ''
    execute4=''
    for item in Quote.Items:
        if item.ProductName in systems_list1:
            execute1 = 'true'
        elif item.ProductName in systems_list2:
            execute2 = 'true'
        elif item.ProductName in systems_list3:
            execute3 = 'true'
        elif item.ProductName in systems_list4:
            execute4 = 'true'
        if execute1 != '' and execute2 != '' and execute3 != '' and execute4 != '':
            break
    if execute1 !="":
        ScriptExecutor.ExecuteGlobal('GS_PAS_BOM_Quote_Table_Generator')
    if execute2 != "":
        ScriptExecutor.ExecuteGlobal('GS_PAS_BOM_Quote_Table_Generator_2')
    if execute3 != "":
        ScriptExecutor.ExecuteGlobal('GS_PAS_BOM_Quote_Table_Generator_PMC')
    if execute4 != "":
        ScriptExecutor.ExecuteGlobal('GS_R2Q_TAS_NewExapansion_BOM_Generator')