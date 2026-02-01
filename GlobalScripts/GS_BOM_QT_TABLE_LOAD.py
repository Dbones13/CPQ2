prod_list = ['ControlEdge PLC System','PMD System','ControlEdge RTU System','ControlEdge UOC System','Safety Manager ESD','Safety Manager FGS','Safety Manager BMS','Safety Manager HIPPS','Experion Enterprise System','3rd Party Devices/Systems Interface (SCADA)','ARO, RESS & ERG System','Experion MX System','MXProLine System','Digital Video Manager','Field Device Manager','Electrical Substation Data Collector','Simulation System','eServer System','Experion HS System', 'HC900 System', 'PlantCruise System', 'ControlEdge PCD System','Terminal Manager', 'Measurement IQ System', 'MasterLogic-50 Generic', 'MasterLogic-200 Generic','Experion LX Generic', 'Generic System', 'Virtualization System', 'C300 System','Variable Frequency Drive System','Tank Gauging Engineering','Industrial Security (Access Control)','Fire Detection & Alarm Engineering','Small Volume Prover','Skid and Instruments']
#prod_name = [item.ProductName for item in Quote.MainItems if item.ProductName in prod_list]
experion_misc = 'Miscellaneous Experion'
prod_name = []
for item in Quote.MainItems:
    if item.ProductName in prod_list:
        prod_name.append(item.ProductName)
    if item.QI_Area.Value == 'Experion Write-in' and Quote.GetCustomField('R2QFlag').Content == 'Yes':
        prod_name.append(experion_misc)
prod_name = list(set(prod_name))
products = "<br>".join(prod_name)
Quote.GetCustomField('qt_table_name_dup').Content = 'BOM_Table_for_Proposals_dup'
Quote.GetCustomField('qt_table_prodname').Content = products if products else ""
Quote.GetCustomField('qt_table_name').Content = 'BOM_Table_for_Proposals' if products else ""