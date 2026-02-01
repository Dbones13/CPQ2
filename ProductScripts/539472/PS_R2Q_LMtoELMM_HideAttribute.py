isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
if isR2Qquote:
	cont = Product.GetContainerByName("LM_to_ELMM_ControlEdge_PLC_Cont")
	hideflag = False
	if cont.Rows.Count > 0:
		for row in cont.Rows:
			Trace.Write(row['LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System'])
			if row['LM_do_you_have_additional_space_in_the_cabinet_room_to_mount_the_CE_System'] == 'Yes':
				hideflag = True
				break
	permission = "Editable" if hideflag else "Hidden"
	Product.ParseString('<*CTX( Container({}).Column({}).SetPermission({}) )*>'.format('LM_to_ELMM_ControlEdge_PLC_Cont','LM_do_the_customer_wants_to_retain_the_wiring', permission ))