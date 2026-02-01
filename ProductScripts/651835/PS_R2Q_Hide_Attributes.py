Product.Attr('R2QRequest').AssignValue('Yes')
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))

def hideContainerColumns(contColumnList):
	for contColumn in contColumnList:
		for col in contColumnList[contColumn]:
			Product.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format(contColumn,col))

def delete_rows_from_container(container_name, columnname):
	container = Product.GetContainerByName(container_name)
	rows_to_delete = []
	for row in container.Rows:
		field_value = row['Third_Party_Devices_Systems_Interface_SCADA'].split('<')[0].strip()
		if field_value in columnname:
			rows_to_delete.append(row.RowIndex)
	for row_index in sorted(rows_to_delete, reverse=True):
		container.DeleteRow(row_index)


nonR2QContColumn = {"Modbus/OPC Interfaces":["Devices","Default_Network_type","Default_Network_Interface"],"OPC Application Instances":["Devices","Default_Network_type","Default_Network_Interface"],"IEC/DNP3 Interfaces":["Devices","Default_Network_type","Default_Network_Interface"],"Leak Detection System Interfaces":["Devices","Default_Network_type","Default_Network_Interface"],"Allen-Bradley/Siemens Interfaces":["Devices","Default_Network_type","Default_Network_Interface"],"Flow Computer Interfaces":["Devices","Default_Network_type","Default_Network_Interface"]}
containers = [
	("Modbus/OPC Interfaces", "SELECT Identifiers FROM CT_CCR WHERE Container_Name = 'Modbus/OPC Interfaces'"),
	("OPC Application Instances", "SELECT Identifiers FROM CT_CCR WHERE Container_Name = 'OPC Application Instances'"),
	("IEC/DNP3 Interfaces", "SELECT Identifiers FROM CT_CCR WHERE Container_Name = 'IEC/DNP3 Interfaces'"),
	("Leak Detection System Interfaces", "SELECT Identifiers FROM CT_CCR WHERE Container_Name = 'Leak Detection System Interfaces'"),
	("Allen-Bradley/Siemens Interfaces", "SELECT Identifiers FROM CT_CCR WHERE Container_Name = 'Allen-Bradley/Siemens Interfaces'"),
	("Flow Computer Interfaces", "SELECT Third_Party_Devices_Systems_Interface_SCADA, Identifiers FROM CT_CCR WHERE Container_Name = 'Flow Computer Interfaces'")
]

delete_column = { 'Modbus/OPC Interfaces': ["Enron Modbus Interface EFM Support"], 'OPC Application Instances': [ "OPC UA DA Server Enabler, Per Client", "OPC UA HA Server Enabler, Per Client", "OPC UA HA Server Upgrade, Per Client" ], 'Leak Detection System Interfaces': ["Gas Operations Leak Detection Option License"], 'Allen-Bradley/Siemens Interfaces': ["Allen-Bradley RS- Linx Software"], 'IEC/DNP3 Interfaces': ["IEC 62439-3 Network Drivers", "DNP3 Protocol Interface", "DNP3 History Backfill functionality"], 'Flow Computer Interfaces': [ "Flow-X Flow Computer EFM Export option", "Fisher ROC Interface (0-50)", "Fisher ROC EFM Export Option", "ABB Totalflow Interface (0-50)", "ABB Totalflow EFM Export Option" ] }

#to hide the container columns
hideContainerColumns(nonR2QContColumn)

#to load from database
load_container = lambda name, query: (Product.GetContainerByName(name).LoadFromDatabase(query, 'Identifiers') if Product.GetContainerByName(name).Rows.Count == 0 else None)
for name, query in containers:
	load_container(name, query)

#to hide the questions in container
for container_name, columnname in delete_column.items():
	delete_rows_from_container(container_name, columnname)