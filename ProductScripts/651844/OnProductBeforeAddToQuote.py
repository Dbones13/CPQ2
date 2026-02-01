if Quote.GetCustomField('R2Q_Save').Content == 'Submit':
	import GS_APIGEE_Integration_Util

	CpqPrdNames = {"R2Q C300 System": "C300 System","R2Q eServer System": "eServer System", "R2Q Field Device Manager": "Field Device Manager", "R2Q ControlEdge UOC System": "ControlEdge UOC System", "R2Q 3rd Party Devices/Systems Interface (SCADA)": "3rd Party Devices/Systems Interface (SCADA)", "R2Q Safety Manager ESD" :"Safety Manager ESD", "R2Q Safety Manager FGS": "Safety Manager FGS", "R2Q Experion Enterprise System" :"Experion Enterprise System", "R2Q ControlEdge PLC System": "ControlEdge PLC System"}
	excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
	final_request_body={'QuoteNumber': str(Quote.CompositeNumber),'CartId':str(Quote.QuoteId),'RevisionNumber': str(Quote.RevisionNumber),'UserName':str(User.UserName),'Module': 'New/Expansion','Action': 'New', 'Action_List':[{'ActionName':'Generate PartSummary - ' + CpqPrdNames.get(row['Selected_Products'], row['Selected_Products']),'ScriptName':'R2Q_Gs_PartsummaryforPrjt'} for row in  Product.GetContainerByName('R2Q CE_System_Cont').Rows]}
	#final_request_body['Action_List'].append({'ActionName':'Generate PartSummary - System Group','ScriptName':'R2Q_Gs_PartsummaryforPrjt'})
	cont = Product.GetContainerByName('R2Q CE_System_Cont')
	C300Marshalling = SmMarshalling = False
	for row in cont.Rows:
		if 'C300 System' in row['Selected_Products']:
			contGroupCont = row.Product.GetContainerByName('Series_C_Control_Groups_Cont')
			for c300Row in contGroupCont.Rows:
				if c300Row.Product.Attr('SerC_CG_Marshalling_Cabinet_Type').GetValue() == '3rd Party Marshalling':
					C300Marshalling = True
					final_request_body['Action_List'].append({'ActionName':'R2Q C300 System_'+str(c300Row['Series_C_CG_Name']),'ScriptName':'GS_R2QPRJT_PS_Marshalling_Async'})
		if 'Safety Manager' in row['Selected_Products']:
			if Quote.GetGlobal('SM_marshalling') == 'True':
				continue
			else:
				a = Quote.SetGlobal('SM_marshalling','True')
				contGroupCont = row.Product.GetContainerByName('SM_ControlGroup_Cont')
				for smRow in contGroupCont.Rows:
					for items in smRow.Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows:
						if items['Marshalling_Option'] == 'Hardware_Marshalling_with_Other':
							SmMarshalling = True
							final_request_body['Action_List'].append({'ActionName':row['Selected_Products']+'_'+str(smRow['Control Group Name']),'ScriptName':'GS_R2QPRJT_PS_Marshalling_Async'})
		if row['Selected_Products'] in ('Industrial Security (Access Control)', 'Tank Gauging Engineering', 'Small Volume Prover', 'Skid and Instruments', 'Digital Video Manager', 'Fire Detection & Alarm Engineering', 'Operator Training'):
				final_request_body['Action_List'].append({'ActionName':row['Selected_Products']+'_'+'TAGBIT','ScriptName':'GS_R2Q_TAS_SUMMARY'})
	#final_request_body['Action_List'].append({'ActionName':'Experion Calculation','ScriptName':'GS_R2Q_ExperionCalculation'})
	if C300Marshalling or SmMarshalling:
		final_request_body['Action_List'].append({'ActionName':'Cabinet Count','ScriptName':'GS_R2Q_Cabinet_Count'})
		SmMarshalling = C300Marshalling = False
	#final_request_body['Action_List'].append({'ActionName':'Generate PartSummary - System Group','ScriptName':'R2Q_Gs_PartsummaryforPrjt'})
	#final_request_body['Action_List'].append({'ActionName':'Generate PartSummary - New - Expansion Project','ScriptName':'R2Q_Gs_PartsummaryforPrjt'})
	final_request_body['Action_List'].append({'ActionName':'WriteIn','ScriptName':'GS_R2Q_AddWriteIn'})
	final_request_body['Action_List'].append({'ActionName':'System Architecture','ScriptName':'GS_R2Q_System_Architecturediagram'})
	final_request_body['Action_List'].append({'ActionName':'Reprice','ScriptName':'GS_R2QPRJT_Reprice_Documentations'})
	final_request_body['Action_List'].append({'ActionName':'Document Generation','ScriptName':'GS_R2Q_DocumentGeneration'})

	Log.Write('final_request_body -->>'+str(final_request_body))
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)