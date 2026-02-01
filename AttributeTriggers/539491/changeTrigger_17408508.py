def get_container(name):
	return Product.GetContainerByName(name)


def manage_rows(contner, required_count):
	row_count = contner.Rows.Count
	if row_count < required_count:
		for _ in range(row_count, required_count):
			contner.AddNewRow(False)
	elif row_count > required_count:
		flag = 0
		for _ in range(required_count, row_count):
			flag += 1
			contner.DeleteRow(row_count - flag)

def manage_plc_configuration(msid_scope, count):
	cont = get_container('LSS_Configuration_for_Rockwell_transpose')
	manage_rows(cont, count)

			

msid_scope = Product.Attr('Scope').GetValue()
count = int(Product.Attr("LSS_PLC_Number_of_ControlEdge_PLC_UOC_vUOC_confi").GetValue() or 0)
manage_plc_configuration(msid_scope, count)

'''def valueassign(Attributename):
	Product.Attr(Attributename).AssignValue('0')
Listofatr = ['LSS_PLC_Total_of_3rd_Party_PLC_via_PCDI','LSS_PLC_Total_of_3rd_Party_PLC_via_Scada','LSS_PLC_Total_of_3rd_Party_PLC_via_HPM_SI','LSS_PLC_Total_of_3rd_Party_PLC_via_EPLCG']
if Product.Attr('LSS_PLC_Number_of_ControlEdge_PLC_UOC_vUOC_confi').GetValue() > 0:
	for i in Listofatr:
		valueassign(i)'''