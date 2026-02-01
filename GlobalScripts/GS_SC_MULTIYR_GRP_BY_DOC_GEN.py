# Script to populate quote table for different document generation templates - CXCPQ-72207,CXCPQ-70309,CXCPQ-68376,CXCPQ-64502
import re
from GS_SC_RNOC_Proposal_Gen import RNOC_Renewal
def clearTable(table):
	table.Rows.Clear()
	table.Save()

def AppendixCheck():
	table = Quote.QuoteTables["QT_KeyValueTable"]
	AppAvail = 'N'
	Identifier1=Identifier2=Identifier3=Identifier5=''
	for record in filter(lambda y : y.PartNumber == "Service Product" and y.RolledUpQuoteItem.startswith("1.1"), Quote.MainItems):
		if record.Description == 'A360 Contract Management' or record.Description == 'Service Contract Management':
			row = table.AddNewRow()
			row["Type"] = 'AppendixA'
			row["Service_Name"] = 'A360'
			table.Save()
		if record.Description.__contains__('P1'):
			Identifier1 = 'P1'
			AppAvail = 'Y'
		if record.Description.__contains__('P2'):
			Identifier2 = 'P2' 
			AppAvail = 'Y'
		if record.Description.__contains__('eplace'):
			Identifier3 = 'Replacement' 
			AppAvail = 'Y'
		if record.Description == 'Preventive Maintenance' :
			Identifier5 = 'PM'
			AppAvail = 'Y'
	if AppAvail == 'Y':
		row = table.AddNewRow()
		row["Type"] = 'AppendixE'
		row["Identifier1"] = Identifier1
		row["Identifier2"] = Identifier2
		row["Identifier3"] = Identifier3
		row["Identifier5"] = Identifier5
		table.Save()

			
def scheduleA_OTU_Load():
	table = Quote.QuoteTables["QT_KeyValueTable"]
	for record in Quote.MainItems:
		if record.ProductName == 'Solution Enhancement Support Program' and record.QI_SC_ItemFlag.Value == 'Hidden':
			OTUScheduleA = record.SelectedAttributes.GetContainerByName('SystemDetails_OTU_SESP')
			if OTUScheduleA != None:
				row = table.AddNewRow()
				row["Type"] = "ScheduleA_Available"
				row["Service_Name"] = 'Available'
				row["Identifier1"] = ''
				row["Identifier2"] = ''
				row["Identifier3"] = ''
				for OTU in OTUScheduleA.Rows:
					if len(OTU['MSID_OTU_SESP']) > 0 :
						MSIDOTU = OTU['MSID_OTU_SESP']
					if len(OTU['CurrentVersion_OTU_SESP']) > 0:
						row = table.AddNewRow()
						row["Type"] = "ScheduleA_OTU"
						row["Service_Name"] = MSIDOTU
						row["Identifier1"] = OTU['System_OTU_SESP']
						row["Identifier2"] = OTU['CurrentVersion_OTU_SESP']
						row["Identifier3"] = OTU['TargetVersion_OTU_SESP']
				table.Save()
	
def SOF():
	matrikonUSD = float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Node(USD)'").Value)
	matrikonClientUSD = float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Matrikon Client(USD)'").Value)
	tpFactor = float(SqlHelper.GetFirst("select * from sc_hardcode_values where name = 'Transfer Price Factor'").Value)
	table = Quote.QuoteTables["QT_KeyValueTable"]
	qCurrency = Quote.GetCustomField('SC_CF_CURRENCY').Content if Quote.GetCustomField('SC_CF_PRICE_TOGGLE').Content != 'USD' else 'USD'
	exRate = float(Quote.GetCustomField('SC_CF_EXCHANGE_RATE').Content)
	AvailableA360 = 'A360'
	maxFinder=list()
	EnableSellPrice=0.0
	MSIDList = ""
	maxFinder = [0,0]
	ServiceName='Enabled Services Unavailable'
	SOFAvailability = 'No'
	OrderValue = 0
	ESValue = 'Empty'
	for record in Quote.MainItems:
		if record.PartNumber.startswith("Year"):
			YearValue = record.PartNumber
		if record.PartNumber =='Enabled Services' and YearValue == 'Year-1' and record.QI_SC_ItemFlag.Value !='Hidden' and record.RolledUpQuoteItem.count('.') == 2 :
			EnableSellPrice= round(record.ExtendedAmount,2) if qCurrency == 'USD' else round(record.ExtendedAmount*exRate,2)
		if record.PartNumber =='Enabled Services' and YearValue == 'Year-1' and Quote.GetCustomField('Quote Type').Content =='Contract Renewal' and record.RolledUpQuoteItem.count('.') == 2 :
			PYEnablePrice = record.QI_SC_Previous_Year_List_Price.Value
			ESValue = 'New' if PYEnablePrice == 0 else 'Renewal'
	for record in Quote.MainItems:
		if record.ProductName in ('Enabled Services','Solution Enhancement Support Program') and record.QI_SC_ItemFlag.Value == 'Hidden' :
			EnableContainer= record.SelectedAttributes.GetContainerByName('Asset_details_ServiceProd')
			if EnableContainer != None:
				SOFAvailability = 'Yes'
				for records in EnableContainer.Rows:
					MSIDList = MSIDList + records['MSID'] + ','
				for attr in record.SelectedAttributes:
					if attr.Name.startswith('#_of_independent_'):
						for att in attr.Values:
							maxFinder.append(float(att.Display))
					if attr.Name=='#_of_recommended_udc_servers_enabledServicesModel':
						for att1 in attr.Values:
							maxFinder.append(float(att1.Display))
					if attr.Name == 'OrderType_EnabledService':
						for att in attr.Values:
							OrderType= att.Display
							if OrderType =='New':
								OrderValue =''
							else:
								OrderValue ='Software Upgrade'
					if attr.Name == 'SC_HWOS_Service_Product_ScopeSummary':
						for att in attr.Values:
							SPName=att.Display
							if SPName == 'Enabled Services - Enhanced':
								ServiceName = 'ENABLED_SVCS_ENH'
							elif SPName == 'Enabled Services - Essential':
								ServiceName = 'ENABLED_SVCS_ESS'
					if attr.Name == 'A360Contract_SESPEnable':
						for att1 in attr.Values:
							AvailableA360 = att1.Display
						if 'A360' in AvailableA360:
							EnableSellPrice = 0
			else:
				MSIDList=''
				maxFinder = [0,0]
				ServiceName='Enabled Services Unavailable'
				SOFAvailability = 'No'
				OrderValue = 0
				ListPrice = 0
	if SOFAvailability == 'Yes':
		Quote.GetCustomField('CF_ProjectId').Content = 'Enabled_Services'
		MSIDList = MSIDList.strip()
		maxValue = max(maxFinder) if ESValue in ('Empty','New') else ''
		SPValue = float(maxValue) * float(matrikonUSD) if ESValue in ('Empty','New') else 0
		ClientSPValue = float(maxValue) * float(matrikonClientUSD) if ESValue in ('Empty','New') else 0
		SumSP = EnableSellPrice + SPValue + ClientSPValue
		TP = EnableSellPrice * float(tpFactor)
		SumTP = TP + SPValue + ClientSPValue + 1
		row = table.AddNewRow()
		row['Type'] = 'SOF'
		row['Service_Name'] = MSIDList
		row['Price'] = maxValue
		row['Identifier1'] = SPValue if SPValue != 0 else ''
		row['Identifier2'] = TP
		row['Identifier3'] = ClientSPValue if ClientSPValue != 0 else ''
		row['Identifier4'] = SumTP
		row['Identifier5'] = ServiceName
		row['Identifier6'] = EnableSellPrice
		row['Identifier7'] = ESValue
		row['Identifier10'] = OrderValue
		table.Save()
	else :
		Quote.GetCustomField('CF_ProjectId').Content = ''


def Schedule_B_Entitlements():
	table = Quote.QuoteTables["QT_KeyValueTable"]
	SespEntitlement=""
	sespDict={}
	for record in Quote.MainItems:
		if record.ProductName == 'Solution Enhancement Support Program' and record.QI_SC_ItemFlag.Value == 'Hidden':
			for attr in record.SelectedAttributes:
				if attr.Name =="SC_Service_Product_Model":
					for att in attr.Values:
						SPName=att.Display
			SespContainer = record.SelectedAttributes.GetContainerByName('SC_Entitlements_Model')
			for rows in SespContainer.Rows:
				SespEntitlement = SespEntitlement +  rows["Entitlement"] + "
"
			SespEntitlement = SespEntitlement.strip()
			sespSummaryContainer = record.SelectedAttributes.GetContainerByName('SC_SESP Models Hidden')
			for rows in sespSummaryContainer.Rows:
					sespDict.setdefault(rows['System_Name'], []).append(rows['MSID'])
			for row1 in sespDict:
					MSIDList='
'.join(set(sespDict[row1]))
					row = table.AddNewRow()
					row["Type"] = "Entitlement"
					row["Service_Name"] = "SESP"
					row["Identifier1"] = row1
					row["Identifier2"] = MSIDList
					row["Identifier3"] = SPName
					row["Identifier4"] = SespEntitlement
			SESPEntList = SespEntitlement.split("
")
			SESPAtt1 = "(" + "'{}', " * (len(SESPEntList) - 1) + "'{}')"
			SESPAtt2 = SESPAtt1.format(*SESPEntList)
			CustomTableQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE SERVICE in " +SESPAtt2+ " AND INVOICE_ITEM='{}'".format(SPName))
			for values in CustomTableQuery:
				row = table.AddNewRow()
				row["Type"] = "ScheduleB"
				row["Service_Name"] = "SESP"
				row["Identifier1"] = values.INVOICE_ITEM
				row["Identifier2"] = values.SERVICE
			table.Save()
			EnaMSID=''
			EnaEntitlement=''
			EnaContainer = record.SelectedAttributes.GetContainerByName('Asset_details_ServiceProd')
			if EnaContainer != None:
				for rows in EnaContainer.Rows:
					EnaMSID = EnaMSID +  rows["MSID"] + "
"
				EnaMSID = EnaMSID.strip()
				for attr in record.SelectedAttributes:
					if attr.Name =="SC_HWOS_Service_Product_ScopeSummary":
						for att in attr.Values:
							EnaSPName=att.Display
					if attr.Name =="EnabledService_Entitlement":
						for att in attr.Values:
							EnaEntitlement=att.Display
				if len(EnaMSID) >0 :
					row = table.AddNewRow()
					row["Type"] = "Entitlement"
					row["Service_Name"] = "SESP Enabled Services"
					row["Identifier2"] = EnaMSID
					row["Identifier3"] = EnaSPName
					row["Identifier4"] = EnaEntitlement
				EnaTableQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE SERVICE ='{}' AND INVOICE_ITEM='{}'".format(EnaEntitlement,EnaSPName))
				for values in EnaTableQuery:
					row = table.AddNewRow()
					row["Type"] = "ScheduleB"
					row["Service_Name"] = "SESP Enabled Services"
					row["Identifier1"] = values.INVOICE_ITEM
					row["Identifier2"] = values.SERVICE
				table.Save()
			OTUDict={}
			OTUContainer = record.SelectedAttributes.GetContainerByName('SystemDetails_OTU_SESP')
			if OTUContainer != None:
				for row in OTUContainer.Rows:
					if len(row['MSID_OTU_SESP']) > 0:
						MSID_Value = row['MSID_OTU_SESP']
					OTUDict.setdefault(MSID_Value, []).append(row['System_OTU_SESP'])
				for attr in record.SelectedAttributes:
					if attr.Name =="Service_Product_OTU_SESP":
						for att in attr.Values:
							OTUSPName=att.Display
				for attr in record.SelectedAttributes:
					if attr.Name =="Entitlement_OTU_SESP":
						for att in attr.Values:
							OTUEntitlement=att.Display
				if OTUDict :
					for key in OTUDict:
						row = table.AddNewRow()
						row["Type"] = "Entitlement"
						row["Service_Name"] = "OTU SESP"
						row["Identifier1"] = '
'.join(set(OTUDict[key]))
						row["Identifier2"] = key
						row["Identifier3"] = OTUSPName
						row["Identifier4"] = OTUEntitlement
				OTUTableQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE SERVICE ='{}' AND INVOICE_ITEM='{}'".format(OTUEntitlement,OTUSPName))
				for values in OTUTableQuery:
					row = table.AddNewRow()
					row["Type"] = "ScheduleB"
					row["Service_Name"] = "OTU SESP"
					row["Identifier1"] = values.INVOICE_ITEM
					row["Identifier2"] = values.SERVICE
				table.Save()
		if record.ProductName == 'Parts Management' and record.QI_SC_ItemFlag.Value == 'Hidden':
			P1Replenish = 0
			P2SharedParts = 0
			PartsReplacementU = 0
			PartsContainer = record.SelectedAttributes.GetContainerByName('SC_P1P2_ServiceProduct_Entitlement')
			for rows in PartsContainer.Rows:
				row = table.AddNewRow()
				row["Type"] = "Entitlement"
				row["Service_Name"] = "Parts"
				row["Identifier3"] = rows['Service Product']
				row["Identifier4"] = rows['Entitlement']
			for records in PartsContainer.Rows:
				PartsQuery =  SqlHelper.GetFirst("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE INVOICE_ITEM = '{}' AND SERVICE='{}'".format(records['Service Product'],records['Entitlement']))
				if PartsQuery is not None:
					if P1Replenish == 0 and PartsQuery.INVOICE_ITEM == 'Parts Holding P1':
						row = table.AddNewRow()
						row["Type"] = "ScheduleB"
						row["Service_Name"] = "Parts"
						row["Identifier1"] = PartsQuery.INVOICE_ITEM
						row["Identifier2"] = 'P1 - Replenishment from P2'
						P1Replenish = 1
					elif P2SharedParts == 0 and PartsQuery.INVOICE_ITEM == 'Parts Holding P2':
						row = table.AddNewRow()
						row["Type"] = "ScheduleB"
						row["Service_Name"] = "Parts"
						row["Identifier1"] = PartsQuery.INVOICE_ITEM
						row["Identifier2"] = 'Shared Parts'
						P2SharedParts = 1
					elif PartsReplacementU == 0 and PartsQuery.INVOICE_ITEM == 'Parts Replacement':
						row = table.AddNewRow()
						row["Type"] = "ScheduleB"
						row["Service_Name"] = "Parts"
						row["Identifier1"] = PartsQuery.INVOICE_ITEM
						row["Identifier2"] = 'Parts Replacement  Unlimited'
						PartsReplacementU = 1
					row = table.AddNewRow()
					row["Type"] = "ScheduleB"
					row["Service_Name"] = "Parts"
					row["Identifier1"] = PartsQuery.INVOICE_ITEM
					row["Identifier2"] = PartsQuery.SERVICE
				else:
					if records['Service Product'] == 'Parts Holding P2' and P2SharedParts == 0:
						row = table.AddNewRow()
						row["Type"] = "ScheduleB"
						row["Service_Name"] = "Parts"
						row["Identifier1"] = records['Service Product']
						row["Identifier2"] = 'Shared Parts'
						P2SharedParts = 1
			table.Save()
		if record.ProductName == 'Labor' and record.QI_SC_ItemFlag.Value == 'Hidden':
			LaborContainer = record.SelectedAttributes.GetContainerByName('SC_Labor_Summary_Container')
			for rows in LaborContainer.Rows:
				row = table.AddNewRow()
				row["Type"] = "Entitlement"
				row["Service_Name"] = "Labor"
				row["Identifier3"] = rows['Service_Product']
				row["Identifier4"] = rows['Entitlement']
				LaborQuery =  SqlHelper.GetFirst("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE INVOICE_ITEM = '{}' AND SERVICE='{}'".format(rows['Service_Product'],rows['Entitlement']))
				if LaborQuery is not None:
					row = table.AddNewRow()
					row["Type"] = "ScheduleB"
					row["Service_Name"] = "Labor"
					row["Identifier1"] = LaborQuery.INVOICE_ITEM
					row["Identifier2"] = LaborQuery.SERVICE
			table.Save()
		if record.ProductName == 'QCS 4.0' and record.QI_SC_ItemFlag.Value == 'Hidden':
			QcsContainer = record.SelectedAttributes.GetContainerByName('SC_QCS_Product_Container')
			for rows in QcsContainer.Rows:
				row = table.AddNewRow()
				row["Type"] = "Entitlement"
				row["Service_Name"] = "QCS"
				row["Identifier3"] = rows['Service Product']
				row["Identifier4"] = rows['Entitlement']
				QCSQuery =  SqlHelper.GetFirst("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE INVOICE_ITEM = '{}' AND SERVICE='{}'".format(rows['Service Product'],rows['Entitlement']))
				if QCSQuery is not None:
					row = table.AddNewRow()
					row["Type"] = "ScheduleB"
					row["Service_Name"] = "QCS 4.0"
					row["Identifier1"] = QCSQuery.INVOICE_ITEM
					row["Identifier2"] = QCSQuery.SERVICE
			table.Save()
		if record.ProductName == 'Honeywell Digital Prime' and record.QI_SC_ItemFlag.Value == 'Hidden':
			HDPMSID1=''
			HDPEntitlement=''
			HDPContainer1 = record.SelectedAttributes.GetContainerByName('SC_MSID_Container')
			if HDPContainer1 != None:
				for rows in HDPContainer1.Rows:
					if rows.IsSelected==True:
						HDPMSID1 = HDPMSID1 +  rows["MSIDs"] + "
"
					if rows['Base MSID']=='True':
						HDPMSID1 = HDPMSID1 +  rows["MSIDs"] + "
"
					if rows['Additional MSID']=='True':
						HDPMSID1 = HDPMSID1 +  rows["MSIDs"] + "
"
				HDPMSID1 = HDPMSID1.strip()
			for attr in record.SelectedAttributes:
				if attr.Name =="SC_Honeywell_Digital_Prime":
					for att in attr.Values:
						DGName=att.Display
			DigiContainer = record.SelectedAttributes.GetContainerByName('SC_Entitlements_Model')
			DigiEntitlement=""
			for rows in DigiContainer.Rows:
				DigiEntitlement = DigiEntitlement +  rows["Entitlement"] + "
"
			DigiEntitlement = DigiEntitlement.strip()
			row = table.AddNewRow()
			row["Type"] = "Entitlement"
			row["Service_Name"] = "Digital Prime"
			row["Identifier2"] = HDPMSID1
			row["Identifier3"] = DGName
			row["Identifier4"] = DigiEntitlement
			HDPEntList = DigiEntitlement.split("
")
			HDPAtt1 = "(" + "'{}', " * (len(HDPEntList) - 1) + "'{}')"
			HDPAtt2 = HDPAtt1.format(*HDPEntList)
			HDPQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE SERVICE in " +HDPAtt2+ " AND INVOICE_ITEM='{}'".format(DGName))
			for values in HDPQuery:
				row = table.AddNewRow()
				row["Type"] = "ScheduleB"
				row["Service_Name"] = "Honeywell Digital Prime"
				row["Identifier1"] = values.INVOICE_ITEM
				row["Identifier2"] = values.SERVICE
			table.Save()
		if record.ProductName == 'Workforce Excellence Program' and record.QI_SC_ItemFlag.Value == 'Hidden':
			WFContainer = record.SelectedAttributes.GetContainerByName('SC_WEP_Offering_Entitlement')
			WFEntitlement =""
			TrainEntitlement=""
			for rows in WFContainer.Rows:
				if rows['Offering_Name'] in ('Training','Operations and Maintenance'):
					TrainEntitlement = TrainEntitlement +  rows["Entitlements"] + "
"
				if rows['Offering_Name'] not in ('Training','Operations and Maintenance'):
					WFEntitlement = WFEntitlement +  rows["Entitlements"] + "
"
			TrainEntitlement = TrainEntitlement.strip()
			if len(TrainEntitlement) > 0 :
				row = table.AddNewRow()
				row["Type"] = "Entitlement"
				row["Service_Name"] = "Training"
				row["Identifier3"] = "Training"
				row["Identifier4"] = TrainEntitlement
			WFEntitlement = WFEntitlement.strip()
			if len(WFEntitlement) > 0 :
					row = table.AddNewRow()
					row["Type"] = "Entitlement"
					row["Service_Name"] = "WEP"
					row["Identifier3"] = "Workforce Excellence Program"
					row["Identifier4"] = WFEntitlement
			TrainEntList = TrainEntitlement.split("
")
			TrainAtt1 = "(" + "'{}', " * (len(TrainEntList) - 1) + "'{}')"
			TrainAtt2 = TrainAtt1.format(*TrainEntList)
			TrainTableQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE INVOICE_ITEM='{}'".format('Training'))
			for values in TrainTableQuery:
				row = table.AddNewRow()
				row["Type"] = "ScheduleB"
				row["Service_Name"] = "Training"
				row["Identifier1"] = values.INVOICE_ITEM
				row["Identifier2"] = values.SERVICE
			WFEntList = WFEntitlement.split("
")
			WFAtt1 = "(" + "'{}', " * (len(WFEntList) - 1) + "'{}')"
			WFAtt2 = WFAtt1.format(*WFEntList)
			WFTableQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE SERVICE in " +WFAtt2+ " AND INVOICE_ITEM='{}'".format('Workforce Excellence'))
			for values in WFTableQuery:
				row = table.AddNewRow()
				row["Type"] = "ScheduleB"
				row["Service_Name"] = "Workforce"
				row["Identifier1"] = values.INVOICE_ITEM
				row["Identifier2"] = values.SERVICE
			table.Save()
		if record.ProductName == 'MES Performix' and record.QI_SC_ItemFlag.Value == 'Hidden':
				for attr in record.SelectedAttributes:
					if attr.Name =="SC_MES_ServiceProduct":
						for att in attr.Values:
							MESName=att.Display
				if MESName == 'MES Batch Services Term - Perpetual':
					MSName = 'MES Batch Services Term'
				elif MESName == 'MES Batch Maintenance Services - Term Based':
					MSName = 'MES Batch Maintenance Services'
				else:
					MSName =''
				MesContainer = record.SelectedAttributes.GetContainerByName('SC_MES_Entitlements')
				MesEntitlement=""
				for rows in MesContainer.Rows:
					MESQuery =  SqlHelper.GetFirst("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE INVOICE_ITEM = '{}' AND SERVICE='{}'".format(MSName,rows['Entitlement']))
					if MESQuery is not None:
						row = table.AddNewRow()
						row["Type"] = "ScheduleB"
						row["Service_Name"] = "MES"
						row["Identifier1"] = MESQuery.INVOICE_ITEM
						row["Identifier2"] = MESQuery.SERVICE
					MesEntitlement = MesEntitlement +  rows["Entitlement"] + "
"
				MesEntitlement = MesEntitlement.strip()
				row = table.AddNewRow()
				row["Type"] = "Entitlement"
				row["Service_Name"] = "MES"
				row["Identifier3"] = MESName
				row["Identifier4"] = MesEntitlement
				table.Save()
		if record.ProductName == 'Hardware Refresh' and record.QI_SC_ItemFlag.Value == 'Hidden':
				HWRContainer = record.SelectedAttributes.GetContainerByName('HWOS_Entitlement_Optional')
				HWREntitlement=""
				for rows in HWRContainer.Rows:
					HWREntitlement = HWREntitlement +  rows["Entitlement"] + "
"
				HWREntitlement = HWREntitlement.strip()
				if len(HWREntitlement) > 0:
					row = table.AddNewRow()
					row["Type"] = "Entitlement"
					row["Service_Name"] = "HWR"
					row["Identifier3"] = "Hardware Refresh"
					row["Identifier4"] = HWREntitlement
				HWREntList = HWREntitlement.split("
")
				HWRAtt1 = "(" + "'{}', " * (len(HWREntList) - 1) + "'{}')"
				HWRAtt2 = HWRAtt1.format(*HWREntList)
				HWRQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE  SERVICE in " +HWRAtt2+ " AND INVOICE_ITEM = '{}'".format('Hardware Refresh'))
				for queries in HWRQuery:
						row = table.AddNewRow()
						row["Type"] = "ScheduleB"
						row["Service_Name"] = "HWR"
						row["Identifier1"] = queries.INVOICE_ITEM
						row["Identifier2"] = queries.SERVICE
				table.Save()
		if record.ProductName == 'Hardware Warranty' and record.QI_SC_ItemFlag.Value == 'Hidden':
				HWWContainer = record.SelectedAttributes.GetContainerByName('HWOS_Entitlement_Optional')
				HWWEntitlement=""
				for rows in HWWContainer.Rows:
					HWWEntitlement = HWWEntitlement +  rows["Entitlement"] + "
"
				HWWEntitlement = HWWEntitlement.strip()
				if len(HWWEntitlement) > 0:
					row = table.AddNewRow()
					row["Type"] = "Entitlement"
					row["Service_Name"] = "HWW"
					row["Identifier3"] = "Hardware Warranty"
					row["Identifier4"] = HWWEntitlement
					HWWEntList = HWWEntitlement.split("
")
					HWWAtt1 = "(" + "'{}', " * (len(HWWEntList) - 1) + "'{}')"
					HWWAtt2 = HWWAtt1.format(*HWWEntList)
					HWWQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE  SERVICE in " +HWWAtt2+ " AND INVOICE_ITEM = '{}'".format('Hardware Warranty'))
					for queries in HWWQuery:
						row = table.AddNewRow()
						row["Type"] = "ScheduleB"
						row["Service_Name"] = "HWW"
						row["Identifier1"] = queries.INVOICE_ITEM
						row["Identifier2"] = queries.SERVICE
				table.Save()
		if  record.ProductName == 'Condition Based Maintenance' and record.QI_SC_ItemFlag.Value == 'Hidden':
			for attr in record.SelectedAttributes:
				if attr.Name =="CBM_Service_Product":
					for att in attr.Values:
						CBName=att.Display
				if attr.Name =="CBM_PM_Level":
					for att in attr.Values:
						CycleValue=att.Display
			CBMEntitlement=''
			CBMContainer = record.SelectedAttributes.GetContainerByName('CBM_Service_Products&Entitlements_Cont')
			for rows in CBMContainer.Rows:
				CBMEntitlement = CBMEntitlement +  rows["Entitlement"] + "
"
			CBMEntitlement = CBMEntitlement.strip()
			if len(CBMEntitlement) >0 :
				row = table.AddNewRow()
				row["Type"] = "Entitlement"
				row["Service_Name"] = "CBM"
				row["Identifier3"] = CBName
				row["Identifier4"] = CBMEntitlement
			CBMEntList = CBMEntitlement.split("
")
			CBMAtt1 = "(" + "'{}', " * (len(CBMEntList) - 1) + "'{}')"
			CBMAtt2 = CBMAtt1.format(*CBMEntList)
			CBMTableQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE INVOICE_ITEM='{}' AND SERVICE = '{}'".format(CBName,CycleValue))
			for values in CBMTableQuery:
				row = table.AddNewRow()
				row["Type"] = "ScheduleB"
				row["Service_Name"] = "CBM"
				row["Identifier1"] = values.INVOICE_ITEM
				row["Identifier2"] = values.SERVICE
			table.Save()
		if record.ProductName == 'Third Party Services' and record.QI_SC_ItemFlag.Value == 'Hidden':
			for attr in record.SelectedAttributes:
				if attr.Name =="SC_TPS_Service_Product":
					for att in attr.Values:
						TPSName=att.Display
			TPSContainer = record.SelectedAttributes.GetContainerByName('SC_TPS_Entitlements_Scope_summary')
			TPSEntitlement=""
			for rows in TPSContainer.Rows:
				TPSEntitlement = TPSEntitlement +  rows["Entitlement"] + "
"
			TPSEntitlement = TPSEntitlement.strip()
			row = table.AddNewRow()
			row["Type"] = "Entitlement"
			row["Service_Name"] = "TPS"
			row["Identifier3"] = TPSName
			row["Identifier4"] = TPSEntitlement
			table.Save()
		if record.ProductName == 'Trace' and  record.QI_SC_ItemFlag.Value == 'Hidden':
			TraEntitlement=''
			TraContainer = record.SelectedAttributes.GetContainerByName('SC_Trace_ServiceProduct_Entitlement')
			for rows in TraContainer.Rows:
				TraEntitlement = TraEntitlement +  rows["Entitlement"] + "
"
				TraSPName = rows['Service_Product']
			TraEntitlement = TraEntitlement.strip()
			if len(TraEntitlement) >0 :
				row = table.AddNewRow()
				row["Type"] = "Entitlement"
				row["Service_Name"] = "Trace"
				row["Identifier3"] = TraSPName
				row["Identifier4"] = TraEntitlement
			TraEntList = TraEntitlement.split("
")
			TraAtt1 = "(" + "'{}', " * (len(TraEntList) - 1) + "'{}')"
			TraAtt2 = TraAtt1.format(*TraEntList)
			TraTableQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE SERVICE in " +TraAtt2+ " AND INVOICE_ITEM='{}'".format(TraSPName))
			for values in TraTableQuery:
				row = table.AddNewRow()
				row["Type"] = "ScheduleB"
				row["Service_Name"] = "Trace"
				row["Identifier1"] = values.INVOICE_ITEM
				row["Identifier2"] = values.SERVICE
			table.Save()
		if record.ProductName == 'Enabled Services' and  record.QI_SC_ItemFlag.Value == 'Hidden':
			EnaMSID1=''
			EnaEntitlement=''
			EnaContainer1 = record.SelectedAttributes.GetContainerByName('Asset_details_ServiceProd')
			if EnaContainer1 != None:
				for rows in EnaContainer1.Rows:
					EnaMSID1 = EnaMSID1 +  rows["MSID"] + "
"
				EnaMSID1 = EnaMSID1.strip()
				for attr in record.SelectedAttributes:
					if attr.Name =="SC_HWOS_Service_Product_ScopeSummary":
						for att in attr.Values:
							EnaSPName=att.Display
					if attr.Name =="EnabledService_Entitlement":
						for att in attr.Values:
							EnaEntitlement=att.Display
				if len(EnaMSID1) >0 :
					row = table.AddNewRow()
					row["Type"] = "Entitlement"
					row["Service_Name"] = "Enabled Services"
					row["Identifier2"] = EnaMSID1
					row["Identifier3"] = EnaSPName
					row["Identifier4"] = EnaEntitlement
				EnaTableQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE SERVICE ='{}' AND INVOICE_ITEM='{}'".format(EnaEntitlement,EnaSPName))
				for values in EnaTableQuery:
					row = table.AddNewRow()
					row["Type"] = "ScheduleB"
					row["Service_Name"] = "Enabled Services"
					row["Identifier1"] = values.INVOICE_ITEM
					row["Identifier2"] = values.SERVICE
				table.Save()
		if record.ProductName == 'Cyber' and record.QI_SC_ItemFlag.Value == 'Hidden':
			CyberDict1={}
			CyberDict={}
			CyberContainer = record.SelectedAttributes.GetContainerByName('SC_Cyber_Models_Scope_Cont')
			if CyberContainer !=None:
				for row in CyberContainer.Rows:
					CyberDict.setdefault(row['Service_Product'], []).append(row['Asset No'])
			CyberContainer1 = record.SelectedAttributes.GetContainerByName('SC_Cyber_Product_Entitlement_Cont')
			if CyberContainer1 !=None:
				for row in CyberContainer1.Rows:
					CyberDict1.setdefault(row['Service_Product'], []).append(row['Entitlement'])
				if CyberDict and CyberDict1 :
					for key in CyberDict:
						row = table.AddNewRow()
						row["Type"] = "Entitlement"
						row["Service_Name"] = "Cyber"
						row["Identifier1"] = ''
						row["Identifier2"] = '
'.join(set(CyberDict[key]))
						row["Identifier3"] = key
						if key not in CyberDict1.keys():
								row["Identifier4"] = ''
						else:
								row["Identifier4"] = '
'.join(set(CyberDict1[key]))
					for key in CyberDict1:
						for values in CyberDict1[key]:
							CyberQuery =  SqlHelper.GetFirst("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE INVOICE_ITEM = '{}' AND SERVICE='{}'".format(key,values))
							if CyberQuery != None:
								row = table.AddNewRow()
								row["Type"] = "ScheduleB"
								row["Service_Name"] = "Cyber"
								row["Identifier1"] = CyberQuery.INVOICE_ITEM
								row["Identifier2"] = CyberQuery.SERVICE
					table.Save()
		if record.ProductName == 'Generic Module' and record.QI_SC_ItemFlag.Value == 'Hidden':
			CyberDict1={}
			CyberDict={}
			CyberContainer = record.SelectedAttributes.GetContainerByName('SC_GN_AT_Models_Scope_Cont')
			GMProductName = record.PartNumber
			if CyberContainer !=None:
				for row in CyberContainer.Rows:
					CyberDict.setdefault(row['Service_Product'], []).append(row['Asset No'])
			CyberContainer1 = record.SelectedAttributes.GetContainerByName('SC_GN_AT_Product_Entitlement_Cont')
			if CyberContainer1 !=None:
				for row in CyberContainer1.Rows:
					CyberDict1.setdefault(row['Service_Product'], []).append(row['Entitlement'])
				if CyberDict and CyberDict1 :
					for key in CyberDict:
						row = table.AddNewRow()
						row["Type"] = "Entitlement"
						row["Service_Name"] = GMProductName
						row["Identifier1"] = ''
						row["Identifier2"] = '
'.join(set(CyberDict[key]))
						row["Identifier3"] = key
						if key not in CyberDict1.keys():
								row["Identifier4"] = ''
						else:
								row["Identifier4"] = '
'.join(set(CyberDict1[key]))
					for key in CyberDict1:
						for values in CyberDict1[key]:
							CyberQuery =  SqlHelper.GetFirst("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE INVOICE_ITEM = '{}' AND SERVICE='{}'".format(key,values))
							if CyberQuery != None:
								row = table.AddNewRow()
								row["Type"] = "ScheduleB"
								row["Service_Name"] = GMProductName
								row["Identifier1"] = CyberQuery.INVOICE_ITEM
								row["Identifier2"] = CyberQuery.SERVICE
					table.Save()
        if record.ProductName == 'BGP inc Matrikon' and record.QI_SC_ItemFlag.Value == 'Hidden':
			BGPDict1={}
			BGPDict={}
			BGPEntListChk=list()
			BGPEntListChk1=list()
			BGPContainer = record.SelectedAttributes.GetContainerByName('SC_BGP_Models_Scope_Cont')
			if BGPContainer !=None:
				for row in BGPContainer.Rows:
					BGPDict.setdefault(row['Service_Product'], []).append(row['Asset No'])
			BGPContainer1 = record.SelectedAttributes.GetContainerByName('SC_BGP_Product_Entitlement_Cont')
			if BGPContainer1 !=None:
				for row in BGPContainer1.Rows:
					BGPDict1.setdefault(row['Service_Product'], []).append(row['Entitlement'])
				if BGPDict and BGPDict1 :
					for key in BGPDict:
						row = table.AddNewRow()
						row["Type"] = "Entitlement"
						row["Service_Name"] = "BGP"
						row["Identifier1"] = ''
						row["Identifier2"] = '
'.join(set(BGPDict[key]))
						row["Identifier3"] = key
						if key not in BGPDict1.keys():
								row["Identifier4"] = ''
						else:
								row["Identifier4"] = '
'.join(set(BGPDict1[key]))
					for key in BGPDict1:
						BGPSPValue=key
						for values in BGPDict1[key]:
							if BGPSPValue.endswith("BGP"):
								BGPQuery =  SqlHelper.GetFirst("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE INVOICE_ITEM ='{}' AND SERVICE='{}'".format('Benefits Guardianship Program (BGP)',values))
								if BGPQuery != None and values not in BGPEntListChk:
									row = table.AddNewRow()
									row["Type"] = "ScheduleB"
									row["Service_Name"] = "BGP"
									row["Identifier1"] = BGPQuery.INVOICE_ITEM
									row["Identifier2"] = BGPQuery.SERVICE
									BGPEntListChk.append(values)
							elif BGPSPValue.endswith("Plus"):
								BGPQuery =  SqlHelper.GetFirst("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE INVOICE_ITEM ='{}' AND SERVICE='{}'".format('Benefits Guardianship Program (BGP Plus)',values))
								if BGPQuery != None and values not in BGPEntListChk1:
									row = table.AddNewRow()
									row["Type"] = "ScheduleB"
									row["Service_Name"] = "BGP"
									row["Identifier1"] = BGPQuery.INVOICE_ITEM
									row["Identifier2"] = BGPQuery.SERVICE
									BGPEntListChk1.append(values)
					table.Save()
        if record.ProductName == 'Experion Extended Support - RQUP ONLY' and record.QI_SC_ItemFlag.Value == 'Hidden':
				for attr in record.SelectedAttributes:
					if attr.Name =="SC_Exp_Ext_Supp_RQUP_summary":
						for att in attr.Values:
							EXPName=att.Display
				EXPEntitlement=''
				EXPContainer = record.SelectedAttributes.GetContainerByName('SC_Entitlements_Exp_Ext_Supp')
				for rows in EXPContainer.Rows:
					EXPEntitlement = EXPEntitlement +  rows["Entitlement"] + "
"
				EXPEntitlement = EXPEntitlement.strip()
				if len(EXPEntitlement) >0 :
					row = table.AddNewRow()
					row["Type"] = "Entitlement"
					row["Service_Name"] = "Experion RQUP"
					row["Identifier3"] = EXPName
					row["Identifier4"] = EXPEntitlement
				EXPEntList = EXPEntitlement.split("
")
				EXPAtt1 = "(" + "'{}', " * (len(EXPEntList) - 1) + "'{}')"
				EXPAtt2 = EXPAtt1.format(*EXPEntList)
				EXPTableQuery =  SqlHelper.GetList("SELECT * FROM CT_SC_GSM_SCHEDULEB_MAPPING WHERE SERVICE in " +EXPAtt2+ " AND INVOICE_ITEM='{}'".format(EXPName))
				for values in EXPTableQuery:
					row = table.AddNewRow()
					row["Type"] = "ScheduleB"
					row["Service_Name"] = "Experion RQUP"
					row["Identifier1"] = values.INVOICE_ITEM
					row["Identifier2"] = values.SERVICE
				table.Save()
        if record.ProductName == 'Local Support Standby' and record.QI_SC_ItemFlag.Value == 'Hidden':
				LSS_Entitlement = "Local Support Standby"
				if LSS_Entitlement:
					row = table.AddNewRow()
					row["Type"] = "Entitlement"
					row["Service_Name"] = "Local Support"
					row["Identifier3"] = "Local Support Standby"
					row["Identifier4"] = LSS_Entitlement
					row["Identifier1"] = "Local Support Standby"
					row["Identifier2"] = " "
				table.Save()
		

def singleYearCalc():
	TotalSellPrice=PrefixYear=00
	Availability = 'No'
	for record in filter(lambda y : len(y.QI_PartNumber.Value) > 1 and y.RolledUpQuoteItem.startswith("1.1"), Quote.MainItems):
		row = table.AddNewRow()
		row["Type"] = "Document_Template_" + "Multi"
		if record.PartNumber == 'Third Party Services' :
			Desc = record.PartNumber
		else:
			Desc = record.Description
		row["Service_Name"] = Desc
		ab= float(record.ExtendedAmount)
		row["Price"] = 1
		row["Identifier1"] = Currency + " " + str("{:.2f}".format(float(record.ExtendedAmount)))
		Trace.Write("row[Price]  : " +str("{:.2f}".format(float(record.ExtendedAmount))))
		TotalSellPrice = TotalSellPrice + record.ExtendedAmount
		Availability = 'Yes'
	if Availability == 'Yes':
		row = table.AddNewRow()
		row["Type"] = "Document_Template_" + "Multi" + "_Total"
		row["Identifier1"] = Currency + " " + str("{:.2f}".format(float(TotalSellPrice)))
	if Availability == 'Yes':
		row = table.AddNewRow()
		row["Price"] = 1
		row["Type"] ="Document_Template_" + "Multi" + "_Header"
		row["Identifier1"] ="Year 1"
		table.Save()

def multiYearCalc():
	TotalSellPrice=PrefixYear=0
	FinalList=list()
	NewDict={}
	Availability = 'No'
	for record in filter(lambda y : y.QI_SC_ItemFlag.Value != "Hidden", Quote.MainItems):
		if record.PartNumber.startswith("Year"):
			YearValue = record.PartNumber
		if (len(record.QI_PartNumber.Value) > 1 and YearValue =="Year-1") and int(record.Quantity) > 0:
			row = table.AddNewRow()
			row["Type"] = "Document_Template_" + yeartype
			if record.PartNumber == 'Third Party Services' :
				Desc = record.PartNumber
			else:
				Desc = record.Description
			row["Service_Name"] = Desc
			row["Identifier1"] = Currency + " " + str("{:.2f}".format(float(record.ExtendedAmount)))
			TotalSellPrice = TotalSellPrice + record.ExtendedAmount
			Availability = 'Yes'
		if len(record.QI_PartNumber.Value) > 1 and YearValue !="Year-1" and int(record.Quantity) > 0:
			PrefixYear=YearValue.Split('-')[1]
			for rows in table.Rows:
				if record.PartNumber == 'Third Party Services' :
					Desc = record.PartNumber
				else:
					Desc = record.Description
				if rows["Service_Name"] == Desc and len(rows["Identifier" + str(PrefixYear)]) == 0:
					rows["Identifier" + str(PrefixYear)]  = Currency + " " + str("{:.2f}".format(float(record.ExtendedAmount)))
					if ("Identifier" + str(PrefixYear)) in NewDict:
						NewDict["Identifier" + str(PrefixYear)] += float("{:.2f}".format(float(record.ExtendedAmount)))
					else:
						NewDict["Identifier" + str(PrefixYear)] = float("{:.2f}".format(float(record.ExtendedAmount)))
			Availability = 'Yes'
	if Availability == 'Yes':		
		row = table.AddNewRow()
		row["Type"] = "Document_Template_" + yeartype + "_Total"
		row["Identifier1"] = Currency + " " + str("{:.2f}".format(float(TotalSellPrice)))
		table.Save()
		for record in filter(lambda y : y["Type"] == "Document_Template_Multi_Total", table.Rows):
			for values in NewDict:
				record[values] = Currency + " " + str("{:.2f}".format(float(float(NewDict[values]))))
				Trace.Write("record[values]  : " +str(record[values]))
				table.Save()
		HeaderValue = 1
		if HeaderValue == 1:
			row = table.AddNewRow()
			row["Type"] = "Document_Template_" + yeartype + "_Header"
			for record in filter(lambda y : y["Type"] in ("Document_Template_Multi_Total","Document_Template_Multi"), table.Rows):
				for i in range(10):
					value=i+1
					record["Price"] = PrefixYear
					if len(record["Identifier" + str(value)]) == 0:
						record["Identifier" + str(value)] = "NA"
						for records in filter(lambda y : y["Type"] =="Document_Template_Multi_Header", table.Rows):
							records["Identifier" + str(value)] = "NA"
							records["Price"] = PrefixYear
					elif len(record["Identifier" + str(value)]) > 0:
						for records in filter(lambda y : y["Type"] =="Document_Template_Multi_Header", table.Rows):
							records["Identifier" + str(value)] = "Year " + str(value)
							records["Price"] = PrefixYear
			table.Save()

####>> Due to This script Char limit RNOC Function is removed from this place and added to "GS_SC_RNOC_Proposal_Gen" GS.####

if Quote.GetCustomField('Quote Type').Content in ('Contract New','Contract Renewal'):
	duration=Quote.GetCustomField("EGAP_Project_Duration_Months").Content
	if Quote.GetCustomField("SC_CF_IS_CONTRACT_EXTENSION").Content=="True": # added logic for EXTENSION quote
		duration= Quote.GetCustomField("SC_CF_Term_duration_Months").Content
	Currency=Quote.GetCustomField("SC_CF_CURRENCY").Content
	table = Quote.QuoteTables["QT_KeyValueTable"]
	if len(duration) > 0 :
		if int(duration) <= 12:
			yeartype = "Single"
		else:
			yeartype = "Multi"
		table = Quote.QuoteTables["QT_KeyValueTable"]
		clearTab = clearTable(table)
		table.Save()
		if yeartype == "Single":
			TotalSellPrice=0
			SingleYear=singleYearCalc()
			table.Save()
		if yeartype == "Multi":
			TotalSellPrice=0
			MultiYear=multiYearCalc()
			table.Save()
		PopulateOTU = scheduleA_OTU_Load()
		SofCheck = SOF()
		ScheduleB_Call = Schedule_B_Entitlements()
		AppendixCall = AppendixCheck()
	if Quote.GetCustomField('Quote Type').Content == 'Contract Renewal':
		RenewalUpdate = RNOC_Renewal(Quote,TagParserQuote)
		table.Save()