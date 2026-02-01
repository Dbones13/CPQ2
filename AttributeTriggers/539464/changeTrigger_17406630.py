def r2qsetDefaultdrop():
    attr_value = Product.Attr("C200_Select_Migration_Scenario").GetValue()
    containerMapping = {'C200_Migration_General_Qns_Cont': {'C200_Connection _to_Experion_Server': 'FTE','C200_Type_of_UOC':'UOC','C200_Type_of_downlink_communication_UOC':'CNET Redundant','C200_FTE_Switch_to_connect_required_exp_servers':'None','C200_Is_Honeywell_Providing_FTE_cables':'Yes','C200_Average_Cable_Length':'2m'}}
    for contName, colDetails in containerMapping.items():
        system_cont = Product.GetContainerByName(contName).Rows
        for key, val in colDetails.items():
            emptyval=system_cont[0][key]
            #Trace.Write("bbb"+emptyval)
            if str(emptyval)=='':
                if key == 'C200_Type_of_downlink_communication_UOC':
                    if attr_value == "C200 to ControlEdge UOC":
                        system_cont[0].Product.Attr(key).SelectDisplayValue(str(val))
                else:
                    system_cont[0].Product.Attr(key).SelectDisplayValue(str(val))


attr_value = Product.Attr("C200_Select_Migration_Scenario").GetValue()
scope_value = Product.Attr("Scope").GetValue()

Config_Cont = Product.GetContainerByName('C200_Migration_Config_Cont').Rows
for rows in Config_Cont:
	rows['C200_UOC_Number_of_Series_A_IO_Racks'] = '0'
third_party_cont = Product.GetContainerByName("C200_Third_Party_Items_Cont")
third_party_cont.Clear()
if scope_value in ["HW/SW", "HW/SW/LABOR"]:
	if attr_value == "C200 to C300":
		Trace.Write("C200 to C300")
		row = third_party_cont.AddNewRow(False)
		row["WriteIn"] = "3rd Party Hardware - DHRIO"
		
	elif attr_value == "C200 to ControlEdge UOC":
		Trace.Write("C200 to ControlEdge UOC")
		#third_party_cont.AddNewRow(False)
		new_rows = ["3rd Party Hardware - 1756-EN2TR", "3rd Party Hardware - RM2", "3rd Party Hardware - CN2R", "3rd Party Hardware - Cabinet" ]
		#CXCPQ-91570 Start
		new_rows_hint = ['This must be procured locally through sourcing department - quote currency','This must be procured locally through sourcing department - quote currency','This must be procured locally through sourcing department - quote currency','Only add third party cabinets if there is not enough space to install the new racks. Cabinets calculated in Parts Summary include 4 racks per side. This must be procured locally through sourcing department - quote currency']

		for i in new_rows:
			row = third_party_cont.AddNewRow(False)
			hint_data = str(i)+" <i class='fa fa-info-circle' style='color: #106cc6' title='"+str(new_rows_hint[new_rows.index(i)])+"' ></i>"
			row["WriteIn"] = str(hint_data)
		#CXCPQ-91570 End
if Quote.GetCustomField('isR2QRequest').Content == 'Yes':
    productName = Product.Name
    if productName == "C200 Migration":
        r2qsetDefaultdrop()