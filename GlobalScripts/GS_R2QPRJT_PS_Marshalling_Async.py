import GS_APIGEE_Integration_Util
from GS_Curr_ExchRate_Mod import fn_get_curr_exchrate
Log.Info('GS_R2QPRJT_PS_MarshallingResponse Param-->>'+str(Param.ActionName))

WriteinProdCont = Product.GetContainerByName('WriteInProduct')
IoContainerlist = ['C300_RG_Universal_IO_cont_1', 'SerC_RG_Enhanced_Function_IO_Cont', 'C300_CG_Universal_IO_cont_1', 'SerC_CG_Enhanced_Function_IO_Cont', 'C300_RG_Universal_IO_cont_2','C300_CG_Universal_IO_cont_2','SerC_CG_Enhanced_Function_IO_Cont2', 'C300_CG_Universal_IO_Mark_1', 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont', 'C300_CG_Universal_IO_Mark_2', 'C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1', 'SerC_RG_Enhanced_Function_IO_Cont2', 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont', 'C300_SerC_Enhanced_Function_IO_Mark_Group_RG_Cont1']

NISAIIotypelist = ['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)_Iosum', 'SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)_Iosum', 'Series-C: HLAI (16) with HART with differential inputs (0-5000)_Iosum', 'Series-C: LLAI (1) Mux RTD (0-5000)_Iosum', 'Series-C: LLAI (1) Mux TC (0-5000)_Iosum', 'Series-C: LLAI (1) Mux TC Remote CJR (0-5000)_Iosum', 'SCM: HLAI (16) with HART with differential inputs (0-5000)_Iosum']
NISAOIotypelist = ['Series-C: UIO (32) Analog Output (0-5000)_Iosum', 'SCM: UIO (32) Analog Output (0-5000)_Iosum', 'Series-C: AO (16) HART (0-5000)_Iosum', 'SCM: AO (16) HART (0-5000)_Iosum']
NISDIlist = ['Series-C: UIO (32) Digital Input (0-5000)_Iosum', 'SCM: UIO (32) Digital Input (0-5000)_Iosum', 'Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)_Iosum', 'Series-C: DI (32) 24VDC SOE (0-5000)_Iosum', 'Series-C: Pulse Input (8) Single Channel (0-5000)_Iosum', 'Series-C: Pulse Input (4) Dual Channel (0-5000)_Iosum', 'Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)_Iosum','SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)_Iosum','SCM: Pulse Input (8) Single Channel (0-5000)_Iosum','SCM: Pulse Input (4) Dual Channel (0-5000)_Iosum','SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)_Iosum']
NISDOlist = ['Series-C: UIO (32) Digital Output (0-5000)_Iosum', 'SCM: UIO (32) Digital Output (0-5000)_Iosum', 'Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)_Iosum', 'Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)_Iosum', 'SCM: DO (32) 24VDC Bus External Power Supply (0-5000)_Iosum', 'SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)_Iosum']

###red is and non red is -- Red_IS, Non_Red_IS
ISAIlist = ['Series-C: UIO (32) Analog Input (HLAI Adapt) (0-5000)_IoIsSum','SCM: UIO (32) Analog Input (HLAI Adapt) (0-5000)_IoIsSum','Series-C: HLAI (16) with HART with differential inputs (0-5000)_IoIsSum','Series-C: LLAI (1) Mux RTD (0-5000)_IoIsSum','Series-C: LLAI (1) Mux TC (0-5000)_IoIsSum','Series-C: LLAI (1) Mux TC Remote CJR (0-5000)_IoIsSum','SCM: HLAI (16) with HART with differential inputs (0-5000)_IoIsSum']

ISAOlist = ['Series-C: UIO (32) Analog Output (0-5000)_IoIsSum','SCM: UIO (32) Analog Output (0-5000)_IoIsSum','Series-C: AO (16) HART (0-5000)_IoIsSum','SCM: AO (16) HART (0-5000)_IoIsSum']

ISDIlist = ['Series-C: UIO (32) Digital Input (0-5000)_IoIsSum','SCM: UIO (32) Digital Input (0-5000)_IoIsSum','Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)_IoIsSum','Series-C: DI (32) 24VDC SOE (0-5000)_IoIsSum','Series-C: Pulse Input (8) Single Channel (0-5000)_IoIsSum','Series-C: Pulse Input (4) Dual Channel (0-5000)_IoIsSum','Series-C: Pulse Input (2) Fast Cut Off Channel (0-5000)_IoIsSum','SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)_IoIsSum','SCM: Pulse Input (8) Single Channel (0-5000)_IoIsSum','SCM: Pulse Input (4) Dual Channel (0-5000)_IoIsSum','SCM: Pulse Input (2) Fast Cut Off Channel (0-5000)_IoIsSum']

ISDOlist = ['Series-C: UIO (32) Digital Output (0-5000)_IoIsSum','SCM: UIO (32) Digital Output (0-5000)_IoIsSum','Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)_IoIsSum','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)_IoIsSum','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)_IoIsSum','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)_IoIsSum']

### Red_RLY, Non_Red_RLY
RelayDIlist = ['Series-C: UIO (32) Digital Input (0-5000)_IoRLYSum','SCM: UIO (32) Digital Input (0-5000)_IoRLYSum','Series-C: DI (32) 24 VDC with Open Wire Detect (0-5000)_IoRLYSum','Series-C: DI (32) 24VDC SOE (0-5000)_IoRLYSum','SCM: DI (32) 24 VDC with Open Wire Detect (0-5000)_IoRLYSum']

RelayDOlist = ['Series-C: UIO (32) Digital Output (0-5000)_IoRLYSum','SCM: UIO (32) Digital Output (0-5000)_IoRLYSum','Series-C: DO (32) 24VDC Bus External Power Supply (0-5000)_IoRLYSum','Series-C: DO (32) 24VDC Bus Internal Power Supply (0-5000)_IoRLYSum','SCM: DO (32) 24VDC Bus External Power Supply (0-5000)_IoRLYSum','SCM: DO (32) 24VDC Bus Internal Power Supply (0-5000)_IoRLYSum']

installedSpareIO = 0
iospare = 0

SMIOContainerList = ['SM_IO_Count_Analog_Input_Cont', 'SM_IO_Count_Analog_Output_Cont', 'SM_IO_Count_Digital_Input_Cont', 'SM_IO_Count_Digital_Output_Cont', 'SM_CG_Cabinet_Details_Cont_Right', 'SM_CG_Cabinet_Details_Cont_Left', 'SM_RG_Cabinet_Details_Cont_Left', 'SM_RG_Cabinet_Details_Cont','SM_RG_IO_Count_Analog_Input_Cont', 'SM_RG_IO_Count_Analog_Output_Cont', 'SM_RG_IO_Count_Digital_Input_Cont', 'SM_RG_IO_Count_Digital_Output_Cont']

SmNISAIDOList= ['SM_IO_Count_Analog_Output_Cont' , 'SM_IO_Count_Analog_Input_Cont', 'SM_RG_IO_Count_Analog_Input_Cont', 'SM_RG_IO_Count_Analog_Output_Cont']
SmNISAOList= ['SM_IO_Count_Analog_Output_Cont', 'SM_RG_IO_Count_Analog_Output_Cont']
SmNISDIList = ['SM_IO_Count_Digital_Input_Cont', 'SM_RG_IO_Count_Digital_Input_Cont']
SmNISDOList = ['SM_IO_Count_Digital_Output_Cont', 'SM_RG_IO_Count_Digital_Output_Cont']

def extractProductContainer(attrName, product):
	containerList = []
	containerProductList = []
	containerRows = product.GetContainerByName(attrName).Rows
	if containerRows.Count > 0:
		sumofcount = {'Iosum': 0, 'IoIsSum': 0, 'IoRLYSum': 0}
		keydict = {
			'Red_NIS': 'Iosum',
			'Non_Red_NIS': 'Iosum',
			'Red_ISLTR': 'Iosum',
			'Non_Red_ISLTR': 'Iosum',
			'Red_IS': 'IoIsSum',
			'Non_Red_IS': 'IoIsSum',
			'Red_RLY': 'IoRLYSum',
			'Non_Red_RLY': 'IoRLYSum',
		}
		key_Dict = {
			'Red (NIS)': 'Asum',
			'Non Red (NIS)': 'Asum',
			'Red_NIS': 'Asum',
			'Non_Red_NIS': 'Asum',
			'Non Red (IS)': 'BSum',
			'Red (IS)': 'BSum',
			'Red_IS': 'BSum',
			'Non_Red_IS': 'BSum',
			'Red (RLY)': 'CSum',
			'Non Red (RLY)': 'CSum',
			'Red_RLY': 'CSum',
			'Non_Red_RLY': 'CSum',
		}
		Iotype_ = ""
		DItype = ''
		installedSpare = ''
		RMinstalledSpare = ''
		relaytypeforesd = ''
		RMrelaytypeforesd = ''

		for contanierRow in containerRows:
			contanierRowDict = {}
			if attrName in IoContainerlist:
				for col in contanierRow.Columns:
					if contanierRow[col.Name] != '':
						if col.Name in keydict:
							sumofcount[keydict[col.Name]] = sumofcount[keydict[col.Name]] +  int(contanierRow[col.Name])
						if col.Name == 'IO_Type':
							Iotype_ = contanierRow[col.Name]

				if Iotype_:
					contanierRowDict[Iotype_ + '_Iosum'] = sumofcount.get('Iosum') or 0
					contanierRowDict[Iotype_ + '_IoIsSum'] = sumofcount['IoIsSum'] or 0
					contanierRowDict[Iotype_ + '_IoRLYSum'] = sumofcount['IoRLYSum'] or 0
					sumofcount = {'Iosum': 0, 'IoIsSum': 0, 'IoRLYSum': 0}
				containerList.append(contanierRowDict)

	
			#safetymanger
			if attrName in SMIOContainerList:
				sum_of_count = {'Asum': 0, 'BSum': 0, 'CSum': 0}
				relaytypeforesd = ''
				for col in contanierRow.Columns:
					if col.Name == 'SM_CG_RelayTypeForESD':
						relaytypeforesd = contanierRow.Product.Attr('SM_General_RelayTypeForESD').GetValue()
					if contanierRow[col.Name] != '':
						if col.Name in key_Dict:
							sum_of_count[key_Dict[col.Name]] = sum_of_count[key_Dict[col.Name]] +  int(contanierRow[col.Name])

						if col.Name == 'Digital Input Type' or col.Name == 'Analog Input Type' or col.Name == 'Analog Output Type' or col.Name == 'Digital Output Type' or col.Name == 'Analog_Output_Type' or col.Name == 'Analog_Input_Type' or col.Name == 'Digital_Input_Type' or col.Name == 'Digital_Output_Type':
							DItype = contanierRow[col.Name]

						elif col.Name == 'Percent_Installed_Spare_IOs' or col.Name == 'SM_CG_Percentage_SSM_Cabinet(0-100%)':
							installedSpare = contanierRow[col.Name]

						#elif col.Name == 'SM_CG_RelayTypeForESD':
							#relaytypeforesd = contanierRow[col.Name]

						elif col.Name in ['SM_RG_Percentage_SSM_Cabinet(0-100%)', 'SM_Percent_Installed_Spare_IO']:
							RMinstalledSpare = contanierRow[col.Name]

						#elif col.Name == 'SM_RG_RelayTypeForESD':
							#RMrelaytypeforesd = contanierRow[col.Name]

				if DItype:
					contanierRowDict[DItype + '_Asum'] = sum_of_count['Asum'] or 0
					contanierRowDict[DItype + '_BSum'] = sum_of_count['BSum'] or 0
					contanierRowDict[DItype + '_CSum'] = sum_of_count['CSum'] or 0

				if installedSpare:
					contanierRowDict['Percent_Installed_Spare_IOs'] = installedSpare
					contanierRowDict['SM_CG_Percentage_SSM_Cabinet(0-100%)'] = installedSpare
					contanierRowDict['SM_CG_RelayTypeForESD'] = relaytypeforesd
				if RMinstalledSpare:
					contanierRowDict['SM_Percent_Installed_Spare_IO'] = RMinstalledSpare
					#contanierRowDict['Marshalling_Option'] = RMinstalledSpare
					contanierRowDict['SM_RG_Percentage_SSM_Cabinet(0-100%)'] = RMinstalledSpare
					contanierRowDict['SM_RG_RelayTypeForESD'] = RMrelaytypeforesd

				containerList.append(contanierRowDict)

			if contanierRow.Product:
				selectAttributedict_level = {}
				extractProductAttributes(selectAttributedict_level, contanierRow.Product)
				containerProductList.append(selectAttributedict_level)

	return [containerList , containerProductList]

def extractProductAttributes(attributedict, product):
	for attr in product.Attributes:
		if attr.DisplayType == 'Container' and attr.Name not in attributedict:
			attributedict[attr.Name] = extractProductContainer(attr.Name, product)
		else:
			if product.Attr(attr.Name).GetValue() != '' and attr.Name not in attributedict:
				attributedict[attr.Name] = product.Attr(attr.Name).GetValue()


def WirteinItemsCreation(row, installedSpareIO, iospare, NISAI, NISAO, NISDI, NISDO, ISAI, ISAO, ISDI, ISDO, RelayDI, RelayDO, execountry, ActionName, relayesd= '', SMproductline = ''):
	APIGEE_Credentials = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_Credentials'").Value
	APIGEE_R2Q_URL = SqlHelper.GetFirst("Select Value from HPS_INTEGRATION_PARAMS Where [Key]='APIGEE_URL'").Value
	tokenUrl = "{}/v2/oauth/accesstoken".format(APIGEE_R2Q_URL)
	responseToken=AuthorizedRestClient.GetClientCredentialsGrantOAuthToken(APIGEE_Credentials,tokenUrl)
	Req_Token = "{} {}".format(responseToken["token_type"] , responseToken["access_token"])
	excel_Url="https://it.api-beta.honeywell.com/cpq/r2q/sfdc/v1/excel-data"
	header = {"Content-Type" : "application/json","Authorization" : "{}".format(Req_Token),"HON-Org-Id" : "PMT-HPS" }
	if 'Series_C_CG_Name' in row:
		controlgroup = row['Series_C_CG_Name']
		productLine = 'DCS'
		cabinetType = 'C300'
	else:
		controlgroup = row['SM_CG_Name']
		productLine = SMproductline
		cabinetType = 'Safety Manager'
	final_request_body=("{{'quoteNumber' : '{0}', 'parentConfig' : '', 'config' : '{1}', 'module' : 'Marshalling', 'executionCountry': '{16}', 'cabinetType' : '{15}', 'productLine' : '{18}', 'installedSpareIO' : '{3}', 'IOSpare' : '{4}', 'RelayTypeForESD' : '{17}', 'NISAI' : '{5}', 'NISAO' : '{6}', 'NISDI' : '{7}', 'NISDO' : '{8}', 'ISAI' : '{9}', 'ISAO' : '{10}', 'ISDI' : '{11}', 'ISDO' : '{12}', 'RelayDI' : '{13}', 'RelayDO' : '{14}', 'ActionName': '{19}', 'SFQuoteID':'1234'}}").format(Quote.CompositeNumber, controlgroup.decode("utf-8"), '', installedSpareIO, iospare, NISAI, NISAO, NISDI, NISDO, ISAI, ISAO, ISDI, ISDO, RelayDI, RelayDO, cabinetType, execountry, relayesd, productLine, ActionName)
	Log.Info("request body--->" +str(final_request_body))
	Trace.Write("request body--->" +str(final_request_body))
	res = RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)
	Log.Write('Response for Marshalling from Apigee 2== '+ str(res))
	
excel_Url, header = GS_APIGEE_Integration_Util.GetR2QAPIGEEAuthDetails()
try:
	QuoteNumber = Param.QuoteNumber
	Quote = QuoteHelper.Edit(QuoteNumber)
	Quote_Currency = Quote.GetCustomField("SC_CF_CURRENCY").Content
	exchange_rate = fn_get_curr_exchrate("USD", Quote_Currency)
	if Quote.ContainsAnyProduct('Project_cpq'):
		for item in Quote.MainItems:
			if item.PartNumber == 'PRJT R2Q':
				Product = item.EditConfiguration()
				WriteinProdCont = Product.GetContainerByName('WriteInProduct')
				saveAction = Quote.GetCustomField("R2Q_Save").Content
				isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False
				if saveAction != 'Save':
					res2 = []
					selectAttributedict = {}
					extractProductAttributes(selectAttributedict,Product)
					containerValues = str(selectAttributedict)
					remotegroupcheck = False
					SmIoInsatlledSpare = 0
					SmCabinetspare = 0
					rmcabinet = ''
					rminstalledspare = ''
					relayesd = ''
					SmMarshallingvalue = ''
					SMremotegroupcheck = False
					SMproductline = ''
					RmMarshalling = ''
					#ActionName = 'R2Q C300 System_C300 Control Group 1'
					Log.Info('GS_R2QPRJT_PS_Marshalling Log4'+str(selectAttributedict['R2Q CE_System_Cont']))
					for data in selectAttributedict['R2Q_Project_Questions_Cont'][1]:
						executionCountry = data['R2Q_Alternate_Execution_Country'] if 'R2Q_Alternate_Execution_Country' in data else ''
					for data in selectAttributedict['R2Q CE_System_Cont'][1]:
						#C300
						if 'Series_C_Control_Groups_Cont' in data:
							for mainproduct in Product.GetContainerByName('R2Q CE_System_Cont').Rows:
								if mainproduct.Product.Name == Param.ActionName.split('_')[0] and mainproduct.Product.Name == 'R2Q C300 System':
									for item in mainproduct.Product.GetContainerByName('Series_C_Control_Groups_Cont').Rows:
										if item['Series_C_CG_Name'] == Param.ActionName.split('_')[1]:
											CGinstalledSpareIO = 0
											CGIoSpare =0
											for key, val in data.items():
												if key == 'Series_C_Control_Groups_Cont':
													for row in data[key][1]:
														if row['Series_C_CG_Name'] == Param.ActionName.split('_')[1]:
															Log.Info('inside = Series_C_CG_Name')
															sums = {
															'NISAI': 0, 'NISAO': 0, 'NISDI':0, 'NISDO':0,
																'ISAI': 0, 'ISAO': 0, 'ISDI': 0, 'ISDO': 0,
																'RelayDI': 0, 'RelayDO': 0, 
																'RMNISAI': 0, 'RMNISAO': 0, 'RMNISDI':0, 'RMNISDO':0,
																'RMISAI': 0, 'RMISAO': 0, 'RMISDI': 0, 'RMISDO': 0,
																'RMRelayDI': 0, 'RMRelayDO': 0
															}
															marshalling = '3rd Party Marshalling' if row.get('SerC_CG_Marshalling_Cabinet_Type') == '3rd Party Marshalling' else ''
															if marshalling == '':
																break
															CGinstalledSpareIO = int(row.get('SerC_CG_Percent_Installed_Spare') or 0)
															CGIoSpare = int(row.get('SerC_CG_Percent_SpareSpace_Marshalling_Cabinet') or 0)
															if marshalling:
																Log.Info('inside = marshalling')
																for ciotype, cioval in row.items():
																	if ciotype in IoContainerlist and len(row[ciotype]) > 0 and all(row[ciotype]):
																		for index in range(len(row[ciotype][0])):
																			item = row[ciotype][0][index]
																			for k, v in item.items():
																				if k in NISAIIotypelist:
																					sums['NISAI'] += v
																				if k in NISAOIotypelist:
																					sums['NISAO'] += v
																				if k in NISDIlist:
																					sums['NISDI'] += v
																				if k in NISDOlist:
																					sums['NISDO'] += v
																				if k in ISAIlist:
																					sums['ISAI'] += v
																				if k in ISAOlist:
																					sums['ISAO'] += v
																				if k in ISDIlist:
																					sums['ISDI'] += v
																				if k in ISDOlist:
																					sums['ISDO'] += v
																				if k in RelayDIlist:
																					sums['RelayDI'] += v
																				if k in RelayDOlist:
																					sums['RelayDO'] += v
																WirteinItemsCreation(row, CGinstalledSpareIO, CGIoSpare, sums['NISAI'], sums['NISAO'], sums['NISDI'], sums['NISDO'], sums['ISAI'], sums['ISAO'], sums['ISDI'], sums['ISDO'], sums['RelayDI'], sums['RelayDO'], executionCountry, str(Param.ActionName))
						#safety manager
						if 'ProductLine' in data:
							SMproductline = data['ProductLine']
						#ActionName = 'R2Q Safety Manager FGS_SM Control Group1'
						if 'SM_ControlGroup_Cont' in data:
							for mainproduct in Product.GetContainerByName('R2Q CE_System_Cont').Rows:
								if mainproduct.Product.Name == Param.ActionName.split('_')[0] and mainproduct.Product.Name in ("R2Q Safety Manager ESD", "R2Q Safety Manager FGS"):
									for item in mainproduct.Product.GetContainerByName('SM_ControlGroup_Cont').Rows:
										if item['Control Group Name'] == Param.ActionName.split('_')[1]:
											relayesd = ''
											for key, values in data.items():
												if key == 'SM_ControlGroup_Cont':
													SM_sums = {
														'SMNISAI': 0, 'SMNISAO': 0, 'SMNISDI': 0, 'SMNISDO': 0,
														'SMNISAIB': 0, 'SMNISAOB': 0, 'SMNISDIB': 0, 'SMNISDOB': 0,
														'SMRelayDI': 0, 'SMRelayDO': 0, 'RMSMNISAI': 0, 'RMSMNISAO': 0, 'RMSMNISDI': 0, 'RMSMNISDO': 0,
														'RMSMNISAIB': 0, 'RMSMNISAOB': 0, 'RMSMNISDIB': 0, 'RMSMNISDOB': 0,
														'RMSMRelayDI': 0, 'RMSMRelayDO': 0
													}

													for SMcontDetails in data[key][1]:
														Log.Info("inside for loop")
														if SMcontDetails['SM_CG_Name'] == Param.ActionName.split('_')[1]:
															if 'Universal Marshalling Cabinet' in SMcontDetails:
																SmMarshallingvalue = 'Hardware Marshalling with Other' if SMcontDetails['Universal Marshalling Cabinet'] == 'Hardware Marshalling with Other' else ''
															if SmMarshallingvalue == '':
																break
															if SmMarshallingvalue:
																Log.Info("marshalling value " +str(SmMarshallingvalue))
																for cont, contVal in SMcontDetails.items():
																	if cont in SMIOContainerList:
																		if 'SM_CG_Cabinet_Details_Cont_Right' == cont and 'Percent_Installed_Spare_IOs' in contVal[0][0]:
																			SmIoInsatlledSpare = contVal[0][0]['Percent_Installed_Spare_IOs']
																		elif 'SM_CG_Cabinet_Details_Cont_Left' == cont and 'SM_CG_RelayTypeForESD' in contVal[0][0]:
																			relayesd = contVal[0][0]['SM_CG_RelayTypeForESD']
																			if 'SM_CG_Percentage_SSM_Cabinet(0-100%)' in contVal[0][0]:
																				SmCabinetspare = contVal[0][0]['SM_CG_Percentage_SSM_Cabinet(0-100%)']
																		if len(contVal[0]) > 0 and all(contVal[0]):
																			for count in range(len(contVal[0])):
																				for smk, smv in contVal[0][count].items():
																					if '_Asum' in smk:
																						if cont in SmNISAIDOList:
																							SM_sums['SMNISAI'] += contVal[0][count][smk]
																						if cont in SmNISAOList:
																							SM_sums['SMNISAO'] += contVal[0][count][smk]
																						if cont in SmNISDIList:
																							SM_sums['SMNISDI'] += contVal[0][count][smk]
																						if cont in SmNISDOList:
																							SM_sums['SMNISDO'] += contVal[0][count][smk]
																					elif '_BSum' in smk:
																						if cont in SmNISAIDOList:
																							SM_sums['SMNISAIB'] += contVal[0][count][smk]
																						if cont in SmNISAOList:
																							SM_sums['SMNISAOB'] += contVal[0][count][smk]
																						if cont in SmNISDIList:
																							SM_sums['SMNISDIB'] += contVal[0][count][smk]
																						if cont in SmNISDOList:
																							SM_sums['SMNISDOB'] += contVal[0][count][smk]
																					elif '_CSum' in smk:
																						if cont in SmNISDIList:
																							SM_sums['SMRelayDI'] += contVal[0][count][smk]
																						if cont in SmNISDIList:
																							SM_sums['SMRelayDO'] += contVal[0][count][smk]

															if SmMarshallingvalue:
																Log.Info("MArshhalling value inside if " +str(SmMarshallingvalue))
																WirteinItemsCreation(SMcontDetails, SmIoInsatlledSpare, SmCabinetspare, SM_sums['SMNISAI'], SM_sums['SMNISAO'], SM_sums['SMNISDI'], SM_sums['SMNISDO'], SM_sums['SMNISAIB'], SM_sums['SMNISAOB'], SM_sums['SMNISDIB'], SM_sums['SMNISDOB'], SM_sums['SMRelayDI'], SM_sums['SMRelayDO'], executionCountry, str(Param.ActionName), relayesd, SMproductline)

except Exception as ex:
	Log.Info('GS_R2QPRJT_PS_Marshalling Error-->>'+str(ex))
	final_request_body={'QuoteNumber':str(Param.QuoteNumber),'CartId':str(Param.CartId),'RevisionNumber': str(Param.RevisionNumber),'UserName':str(User.UserName),'Module':'New/Expansion','Action':'Update','Status':'Fail','Action_List':[{'ActionName':str(Param.ActionName),'ScriptName':'GS_R2QPRJT_PS_Marshalling_Async','ErrorMessage':str(ex)}]}
	RestClient.Post(excel_Url, RestClient.SerializeToJson(str(final_request_body)),header)