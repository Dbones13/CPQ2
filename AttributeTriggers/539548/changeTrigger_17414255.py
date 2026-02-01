contObj = Product.GetContainerByName('CONT_MSID_SUBPRD')
val = Product.Attr('MSID_Current_Experion_Release').GetValue()
Trace.Write('--attributeValue_MSID--'+str(val))


for row in contObj.Rows:
	try:
		row['MSID_Current_Experion_Release'] = val
		if row.Product.Name == 'OPM':
			row.Product.Attr('MSID_Current_Experion_Release').AssignValue(val)
			row.Product.Attr('PERF_ExecuteScripts').AssignValue('Execute')
			Trace.Write("product"+str(row.Product.Attr('PERF_ExecuteScripts').GetValue()))
			
			row.ApplyProductChanges()
			row.Product.ApplyRules()
			if row.Product.ParseString('<*CTX( Container(OPM_Basic_Information).Column(OPM_Is_this_is_a_Remote_Migration_Service_RMS).GetPermission )*>') == 'Editable':
				Trace.Write("visibleproduct")
				opmBasicInfoCon = row.Product.GetContainerByName('OPM_Basic_Information')
				for row in opmBasicInfoCon.Rows:
					Trace.Write("remote"+row['OPM_Is_this_is_a_Remote_Migration_Service_RMS'])
					if row['OPM_Is_this_is_a_Remote_Migration_Service_RMS'] == '':
						Trace.Write("opmvisible")
						row['OPM_Is_this_is_a_Remote_Migration_Service_RMS'] = 'Yes'
						row.GetColumnByName('OPM_Does_the_customer_have_EBR_installed').SetAttributeValue('No')
						Trace.Write("remotevalue"+row['OPM_Is_this_is_a_Remote_Migration_Service_RMS']+"customervalue"+row['OPM_Does_the_customer_have_EBR_installed'])
	except Exception as e:
		Trace.Write('Error'+str(e))
contObj.Calculate()