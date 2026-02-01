class Hcireport():
	def __init__(self,Quote):
		self.Quote = Quote
	def attributevalue(self,getattrs):
		for getval in getattrs.Values:
			return getval.Display 
	def gethciproductdetails(self):
		phdproduct,productchoice = [],[]
		phdproduct,scopeval,includehard,licensemodel = '','','',''
		finaldict = {'UniformancePHD':'False','UniformanceInsight':'False','AdvanceFormulaManagerOnly':'False','License Deployment Model':'False','Include hardware':'False','AFM':'False','LaborOnly':'False','ScopeUpgrade':'False','EDM_AFM':'False','CEJ_Req':'False','AFM Labor selected':'False','HCI_Insight_Users_NoEvents':'No','HCI_Insight_Users_WithEvents':'No','Software':'False','Labor':'False','HCI_PHD_OrderType':'False','R2QScope':'','HCI_PHD_Availability_Redundancy':'No','HCI_PHD_Archive_Extracto_ Tool':'No','HCI_PHD_Clustering_Option': 'No','HCI_PHD_Scout_Express':'No','HCI_PHD_Modbus_RDI':'No','HCI_PHD_API_RDI':'No','HCI_PHD_System_Monitoring_RDI':'No','HCI_PHD_RDI_File_Access':'None','HCI_PHD_Classic_RDI_OPC':'None','HCI_PHD_RDI_OPC_UA':'None','HCI_PHD_CEJ_Required':'No'}
		isupgardephd,phdselected,Uniformanceselected,AFMselected,usmimple = 'No','No','No','No','No'
		phd_loborid = ''
		for item in self.Quote.Items:
			if (item.PartNumber == 'HCI_EDM'):
				for getattrs in item.SelectedAttributes:
					if(getattrs.Name == 'HCI_PHD_Product'):
						phdproduct = self.attributevalue(getattrs)
						#Trace.Write(str(getattrs.Name)+"---recheck---1111-->"+str(phdproduct))
						finaldict[getattrs.Name] = self.attributevalue(getattrs)
			if (item.PartNumber == 'R2QHCI'):
				for getattrs in item.SelectedAttributes:
					if(getattrs.Name == 'AR_HCI_SCOPE'):
						finaldict['R2QScope'] = self.attributevalue(getattrs)
			if (item.PartNumber == 'HCI_Labor_config'):
				finaldict['Labor'] = 'True'
				phd_loborid = item.RolledUpQuoteItem
				productchoice = [ getval.Display for getattrs in item.SelectedAttributes  if(getattrs.Name == 'HCI_Product_Choices') for getval in getattrs.Values if(getval.Display).find('Labor') !=0]
				for getattrs in item.SelectedAttributes:
					if(getattrs.Name == 'HCI_PHD_Prd_Family'):
						laborproduct = self.attributevalue(getattrs)
						finaldict['Product Family'] = 'True' if(str(laborproduct) == 'Enterprise Data Management') else 'False'
					if getattrs.Name == "HCI_PHD_Fo_Eng":
						for row in item.SelectedAttributes.GetContainerByName('HCI_PHD_Fo_Eng').Rows:
							finaldict['Travel Time'] = 'True' if(str(row['Number of trips per engineer']) > '0') else 'False'
					if getattrs.Name == "HCI_Labor_common_prj_input1":
						for chilrow in item.SelectedAttributes.GetContainerByName('HCI_Labor_common_prj_input1').Rows:
							#Trace.Write(str(chilrow['Functional Design'])+"--------yss-------"+str(dir(chilrow)))
							finaldict['Kick Of Meeting'] = 'True' if(str(chilrow['Project Set Up']) == 'Yes') else 'False'
							finaldict['Functional Design Spec'] = 'True' if(str(chilrow['Functional Design']) == 'Yes') else 'False'
							finaldict['Detailed Design Spec'] = 'True' if(str(chilrow['Detailed Design']) == 'Yes') else 'False'
					if getattrs.Name == "HCI_Labor_common_prj_input2":
						for chilrow in item.SelectedAttributes.GetContainerByName('HCI_Labor_common_prj_input2').Rows:
							finaldict['Fact Test'] = 'True' if(str(chilrow['Factory Acceptance Test (FAT)']) == 'Yes') else 'False'
							#finaldict['Fact Test'] = 'True' if(str(chilrow['Factory Acceptance Test (FAT) and Post FAT']) == 'Yes') else 'False'
							finaldict['Client Training'] = 'True' if(str(chilrow['Client Training']) == 'Yes') else 'False'
							finaldict['Site Test'] = 'True' if(str(chilrow['Site Acceptance Testing (SAT)']) == 'Yes') else 'False'
							finaldict['Site spec Doc'] = 'True' if(str(chilrow['Site Specific Documentation']) == 'Yes') else 'False'
					if getattrs.Name == "HCI_PHD_Selected_Products":
						for row in item.SelectedAttributes.GetContainerByName('HCI_PHD_Selected_Products').Rows:
							Trace.Write(str(row.Columns['Product'].Value)+"------rechecking--rpoduct-->"+str(dir(row)))
							if(row.Columns['Product'].Value  == 'PHD Labor'):
								phdselected = 'Yes'
								finaldict['PHD Labor selected'] = 'True'
							elif(row.Columns['Product'].Value  == 'Uniformance Insight Labor'):
								Uniformanceselected = 'Yes'
								finaldict['Uniformance Labor selected'] = 'True'
							elif(row.Columns['Product'].Value  == 'AFM Labor'):
								AFMselected = 'Yes' 
								finaldict['AFM Labor selected'] = 'True'
					if getattrs.Name == "AR_HCI_PHD_ProjectInputs1":
						for chilrow in item.SelectedAttributes.GetContainerByName('AR_HCI_PHD_ProjectInputs1').Rows:
							isupgardephd = str(chilrow['Upgrade/Update-PHD'])
							#Trace.Write(str(chilrow['Upgrade/Update-PHD']))
							finaldict['update-PHD'] = 'True' if(str(isupgardephd) == 'Yes') else 'False'
							finaldict['LAN Setup'] = 'True' if(str(chilrow['Staging Area Hardware and LAN Setup']) == 'Yes') else 'False'
					if getattrs.Name == "AR_HCI_PHD_ProjectInputs2":
						for chilrow in item.SelectedAttributes.GetContainerByName('AR_HCI_PHD_ProjectInputs2').Rows:
							finaldict['Graphics and Reports'] = 'True' if(str(chilrow['Graphics and Reports']) == 'Yes') else 'False'
							finaldict['USM Implementation'] = 'True' if(str(chilrow['USM Implementation']) == 'Yes') else 'False'
							#finaldict['Travel Time'] = 'True' if(str(chilrow['Travel Time']) == 'Yes') else 'False'
							finaldict['Uni Insight Implementation'] = 'True' if(str(chilrow['Uniformance Insight Implementation']) == 'Yes') else 'False'
							finaldict['Uni Insight Implementation'] = 'True' if(str(chilrow['Uniformance Insight Implementation']) == 'Yes') else 'False'
					if getattrs.Name == "HCI_PHD_ExcelReports":
						for chilrow in item.SelectedAttributes.GetContainerByName('HCI_PHD_ExcelReports').Rows:
							finaldict['Reports'] = str(int(float(chilrow['Reports'])))
					if getattrs.Name == "HCI_PHD_NewDisplaysforInsight":
						for chilrow in item.SelectedAttributes.GetContainerByName('HCI_PHD_NewDisplaysforInsight').Rows:
							finaldict['New Displays for Insight'] = str(int(float(chilrow['New Displays for Insight'])))
					if getattrs.Name == "HCI_NoOf3rdPartyClients":
						finaldict[getattrs.Name] = self.attributevalue(getattrs)
						#attrvallist = ['HCI_NoOf3rdPartyClients']
						#for eachattr in attrvallist:
						#   finaldict[eachattr] = row.Product.Attr(eachattr).GetValue()
					#Trace.Write("-------rechecking---111--->"+str(getattrs.Name))
			elif (item.PartNumber == 'HCI_EDM'):
				finaldict['Software'] = 'True'
				for getattrs in item.SelectedAttributes:
					Trace.Write(getattrs.Name)
					if(getattrs.Name == 'HCI_PHD_CEJ_Required'):
						finaldict['HCI_PHD_CEJ_Required'] = self.attributevalue(getattrs)
						finaldict['CEJ_Req'] = 'True' if 'Yes' in [getval.Display for getval in getattrs.Values] else 'False'
					#if(getattrs.Name == 'HCI_PHD_Product'):
					#	phdproduct = self.attributevalue(getattrs)
					#	finaldict[getattrs.Name] = self.attributevalue(getattrs)
					elif(getattrs.Name == 'HCI_PHD_Scope'):
						scopeval = self.attributevalue(getattrs)
					elif(getattrs.Name == 'Trace_Software_Do_you_need_hardware'):
						includehard = self.attributevalue(getattrs)
						finaldict[getattrs.Name] = self.attributevalue(getattrs)
					elif(getattrs.Name == 'HCI_PHD_LicenseModel'):
						licensemodel = self.attributevalue(getattrs)
					elif(phdproduct in ['Insight','PHD & Insight','PHD & Insight & AFM']) and (getattrs.Name in ['HCI_Insight_Users_NoEvents','HCI_Insight_Users_WithEvents']):
						finaldict[getattrs.Name] = self.attributevalue(getattrs)
					elif(getattrs.Name == 'HCI_PHD_Base_System_Size'):
						finaldict[getattrs.Name] = str(self.attributevalue(getattrs).split(" ")[1]+' tags')
					elif(getattrs.Name in ['HCI_PHD_Modbus_RDI','HCI_PHD_API_RDI','HCI_PHD_System_Monitoring_RDI','HCI_PHD_RDI_File_Access','HCI_PHD_Classic_RDI_OPC','HCI_PHD_RDI_OPC_UA','HCI_PHD_RDI_Web_Client','HCI_PHD_CEJ_Required','HCI_PHD_CEJ_TPN_Area_Wide','HCI_PHD_CEJ_Experion_Area_Wide','HCI_PHD_CEJ_OPC_Area_Wide','SC_Central_Managed_SQL','HCI_PHD_OrderType','HCI_PHD_Availability_Redundancy','HCI_PHD_Archive_Extracto_ Tool','HCI_PHD_Clustering_Option','HCI_PHD_Scout_Express']):
						finaldict[getattrs.Name] = self.attributevalue(getattrs)
					elif(getattrs.Name in ['HCI_PHD_Standard_User_CALs','HCI_PHD_Standard Device','HCI_PHD_Standard_Cores','HCI_Insight_Single_User','HCI_Insight_Five_User_Pack','HCI_Insight_Ten_User_Pack','HCI_Insight_TwentyFive_User_Pack','HCI_Insight_Fifty_User_Pack','HCI_Insight_Hundred_User_Pack','HCI_Insight_250_User_Pack','HCI_Insight_Standard_User_CALs','HCI_Insight_Standard_Device_CALs','HCI_Insight_Standard_Cores','HCI_AFM_Tag_License_1000','HCI_AFM_Tag_License_2000','HCI_AFM_Tag_License_5000','HCI_AFM_Tag_License_10000','HCI_AFM_Tag_License_50000','HCI_AFM_Tag_License_Unlimited','HCI_Insight_Events_Single_User','HCI_Insight_Events_Five_User_Pack','HCI_Insight_Events_Ten_User_Pack','HCI_Insight_Events_TwentyFive_User_Pack','HCI_Insight_Events_Fifty_User_Pack','HCI_Insight_Events_Hundred_User_Pack','HCI_Insight_Events_250_User_Pack']):
						#finaldict[getattrs.Name] = [int(float(getval.Display)) for getval in getattrs.Values][0]
						val = [getval.Display for getval in getattrs.Values]
						finaldict[getattrs.Name] = int(float(val[0])) if val[0] else ''
		'''#isupgardephd,phdselected,Uniformanceselected,AFMselected,usmimple = 'No','No','No','No','No'
		if(phd_loborid !=''):
			self.Quote.GetItemByQuoteItem(phd_loborid).Edit()
			#Trace.Write(str(dir(self.Product)))
			ContFoEng = Product.GetContainerByName('HCI_PHD_Fo_Eng')
			for row in ContFoEng.Rows:
				if(str(row['Number of trips per engineer']) > '0'):
					finaldict['Travel Time'] = 'True'
			Conrow = Product.GetContainerByName('HCI_PHD_Selected_Products')
			if Conrow.Rows.Count>0:
				for row in Conrow.Rows:
					Trace.Write(str(row['Product']))
					if(row['Product']  == 'PHD Labor'):
						phdselected = 'Yes'
						finaldict['PHD Labor selected'] = 'True'
						childConrow1 = row.Product.GetContainerByName('AR_HCI_PHD_ProjectInputs1')
						childConrow2 = row.Product.GetContainerByName('AR_HCI_PHD_ProjectInputs2')
						childConrow3 = row.Product.GetContainerByName('HCI_PHD_ExcelReports')
						childConrow4 = row.Product.GetContainerByName('HCI_PHD_NewDisplaysforInsight')
						for chilrow in childConrow1.Rows:
							isupgardephd = str(chilrow['Upgrade/Update-PHD'])
							#Trace.Write(str(chilrow['Upgrade/Update-PHD']))
							finaldict['update-PHD'] = 'True' if(str(isupgardephd) == 'Yes') else 'False'
							finaldict['LAN Setup'] = 'True' if(str(chilrow['Staging Area Hardware and LAN Setup']) == 'Yes') else 'False'
						for chilrow in childConrow2.Rows:
							finaldict['Graphics and Reports'] = 'True' if(str(chilrow['Graphics and Reports']) == 'Yes') else 'False'
							finaldict['USM Implementation'] = 'True' if(str(chilrow['USM Implementation']) == 'Yes') else 'False'
							#finaldict['Travel Time'] = 'True' if(str(chilrow['Travel Time']) == 'Yes') else 'False'
							finaldict['Uni Insight Implementation'] = 'True' if(str(chilrow['Uniformance Insight Implementation']) == 'Yes') else 'False'
							finaldict['Uni Insight Implementation'] = 'True' if(str(chilrow['Uniformance Insight Implementation']) == 'Yes') else 'False'
						for chilrow in childConrow3.Rows:
							finaldict['Reports'] = str(chilrow['Reports']) 
						for chilrow in childConrow4.Rows:
							finaldict['New Displays for Insight'] = str(chilrow['New Displays for Insight']) 
						attrvallist = ['HCI_NoOf3rdPartyClients']
						for eachattr in attrvallist:
							finaldict[eachattr] = row.Product.Attr(eachattr).GetValue()
					elif(row['Product']  == 'Uniformance Insight Labor'):
						Uniformanceselected = 'Yes'
						finaldict['Uniformance Labor selected'] = 'True'
					elif(row['Product']  == 'AFM Labor'):
						AFMselected = 'Yes' 
						finaldict['AFM Labor selected'] = 'True'
			childConrow3 = Product.GetContainerByName('HCI_Labor_common_prj_input1')
			childConrow4 = Product.GetContainerByName('HCI_Labor_common_prj_input2')
			for chilrow in childConrow3.Rows:
				finaldict['Kick Of Meeting'] = 'True' if(str(chilrow['Project Set Up']) == 'Yes') else 'False'
				finaldict['Functional Design Spec'] = 'True' if(str(chilrow['Functional Design']) == 'Yes') else 'False'
				finaldict['Detailed Design Spec'] = 'True' if(str(chilrow['Detailed Design']) == 'Yes') else 'False'
			for chilrow in childConrow4.Rows:    
				finaldict['Fact Test'] = 'True' if(str(chilrow['Factory Acceptance Test (FAT)']) == 'Yes') else 'False'
				#finaldict['Fact Test'] = 'True' if(str(chilrow['Factory Acceptance Test (FAT) and Post FAT']) == 'Yes') else 'False'
				finaldict['Client Training'] = 'True' if(str(chilrow['Client Training']) == 'Yes') else 'False'
				finaldict['Site Test'] = 'True' if(str(chilrow['Site Acceptance Testing (SAT)']) == 'Yes') else 'False'
				finaldict['Site spec Doc'] = 'True' if(str(chilrow['Site Specific Documentation']) == 'Yes') else 'False' '''
		if(phdproduct in ['Process History Database (PHD)','PHD & Insight','PHD & Insight & AFM'] or phdselected == 'Yes'):
			finaldict['UniformancePHD'] = 'True'
		if(phdproduct in ['Insight','PHD & Insight','PHD & Insight & AFM'] or Uniformanceselected == 'Yes'):
			finaldict['UniformanceInsight'] = 'True'
		if(phdproduct == 'Advanced Formula Manager (AFM)' or AFMselected == 'Yes'):
			finaldict['AdvanceFormulaManagerOnly'] = 'True'
		if(includehard =='Yes'):
			finaldict['Include hardware'] = 'True'
		if(licensemodel in ['Perpetual','Term']):
			finaldict['License Deployment Model'] = 'True'
		#Trace.Write("---phdproduct--->"+str(phdproduct))
		if(phdproduct in ['Advanced Formula Manager (AFM)','PHD & Insight & AFM']) or AFMselected == 'Yes':#  or len(productchoice)>0):
			finaldict['AFM'] = 'True'
		if(phdproduct in ['Advanced Formula Manager (AFM)','PHD & Insight & AFM']):
			finaldict['EDM_AFM'] = 'True'
		if(len(productchoice)>0):
			finaldict['LaborOnly'] = 'True'
		if(scopeval in ['Upgrade']  or isupgardephd == 'Yes'):
			finaldict['ScopeUpgrade'] = 'True'
		if(phdproduct in ['Process History Database (PHD)','PHD & Insight','PHD & Insight & AFM'] and scopeval =='New Implementation'  ):
			finaldict['UniformanceSW'] = 'True'
		if(phdproduct in ['Process History Database (PHD)','PHD & Insight','PHD & Insight & AFM'] and phdselected == 'Yes' and scopeval =='New Implementation'  ):
			finaldict['UniformancePHDSW'] = 'True'
		if(phdselected == 'Yes' and scopeval =='New Implementation'  ):
			finaldict['UniformancePHDImpement'] = 'True'
		if(phdproduct in ['Process History Database (PHD)','PHD & Insight','PHD & Insight & AFM'] and scopeval in ['Upgrade']  ):
			finaldict['upgradeUnifor'] = 'True'
		if(phdproduct in ['Process History Database (PHD)','PHD & Insight','PHD & Insight & AFM'] and scopeval in ['Upgrade'] and isupgardephd == 'Yes' ):
			finaldict['upgradeUniforPHDService'] = 'True'
		if(phdproduct in ['Insight','PHD & Insight','PHD & Insight & AFM'] and Uniformanceselected == 'Yes'):
			finaldict['UniformanceInsightwithlabor'] = 'True'
		if(isupgardephd == 'Yes'):
			finaldict['upgradeservice'] = 'True'
		if(Uniformanceselected == 'Yes'):
			finaldict['Uniformancelabor'] = 'True'
		if(AFMselected == 'Yes'):
			finaldict['UniformanceAFM'] = 'True'
		#Trace.Write(str(finaldict))
		hcifirm = self.Quote.QuoteTables['HCI_FIRM_Proposal']
		hcifirm.Rows.Clear()
		for key, value in finaldict.items():
			newrow = hcifirm.AddNewRow()
			newrow['ConditionKey'] = key
			newrow['ConditionValue'] = value
		hcifirm.Save()
gethci = Hcireport(Quote)
gethci.gethciproductdetails()