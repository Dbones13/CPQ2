# this action helps to populats Proposal
import GS_PopUOC_Proposal
import GS_PopSM_Proposal
import GS_PopC300_Proposal
import R2Q_Cabinet_PLC_UOC
import GS_PopPLC_Proposal
def PAS_DocumentTable(Quote,TagParserQuote):
	QT_Table = Quote.QuoteTables["PAS_Document_Data"]
	QT_Table.Rows.Clear()
	UOCFlag=''
	PLCFlag = ''
	SMFlag_ESD=''
	SMFlag_FGS=''
	cab_count_no=0
	cab_count_yes=0
	C300=''
	guid = dict()
	lst = ["CE_Site_Voltage", "PLC_IO_Filler_Module", "PLC_IO_Spare", "PLC_IO_Slot_Spare", "PLC_Shielded_Terminal_Strip", "CE_Selected_Products", "CE_Add_System_Rows", "CE_Apply_System_Number", "CE_Scope_Choices", "New_Expansion", "Sys_Group_Name", "PLC_Software_Release","PLC_CG_Name","PLC_RG_Name", "CE PLC Engineering Execution Year"]

	proj_columns = ['Labor_Loop_Drawings', 'Labor_Percentage_FAT', 'Labor_Marshalling_Database', 'New_Expansion']
	proj_columns_seq = ['Labor_Loop_Drawings', 'Labor_Percentage_FAT', 'Labor_Marshalling_Database', 'New_Expansion']

	sysgrp_columns = ['CE_System_Asset', 'CE_System_Number', 'New_Expansion']
	sysgrp_columns_seq = ['CE_System_Asset', 'CE_System_Number', 'New_Expansion']

	Cond = TagParserQuote.ParseString("[AND]([OR](([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PAS)),([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,LSS)),([EQ](<*CTX( Quote.CustomField(Booking LOB) )*>,PMC))),[EQ](<*CTX( Quote.CustomField(Quote Type) )*>,Projects), [GT](<*Table(select COUNT(*) from cart_item i where i.CATALOGCODE = 'PRJT' and i.cart_id=<*CTX(Quote.CartId)*> and i.USERID=<*CTX(Quote.OwnerId)*>)*>,0))")
	if Cond == '1':
		for Item in filter(lambda item: item.ProductName in ("New / Expansion Project", "System Group"), Quote.MainItems):
			#for level 0
			if Item.ProductName == "New / Expansion Project":
				newRow = QT_Table.AddNewRow()
				newRow["Project"] = Item.PartNumber
				newRow["Project_GUID"] = Item.QuoteItemGuid
				newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem
				projdic = {}
				for attr in Item.SelectedAttributes:
					if attr.Name not in lst and "UOC" not in attr.Name:
						try:
							attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
							for column in attr_containers:
								if column.Name in proj_columns:
									projdic[column.Name] = column.Value
						except:
							pass

				expectedResult = [projdic[d] for d in proj_columns_seq if d in projdic.keys()]
				newRow['Project_Info'] = "|".join(expectedResult)

			#for level 1
			elif Item.ProductName == "System Group":
				Parent_guid=Item.QuoteItemGuid
				newRow = QT_Table.AddNewRow()
				newRow["System_Group"] = Item.PartNumber
				newRow["System_Grp_GUID"] = Item.QuoteItemGuid
				newRow["RolledUpQuoteItem"] = Item.RolledUpQuoteItem
				guid[Item.QuoteItemGuid] = Item.PartNumber
				Sysgrpdic = {}
				for attr in Item.SelectedAttributes:
					if attr.Name not in lst and "UOC" not in attr.Name:
						try:
							attr_containers = Item.SelectedAttributes.GetContainerByName(attr.Name).Rows[0].Columns
							for column in attr_containers:
								if column.Name in sysgrp_columns:
									Sysgrpdic[column.Name] = column.Value
						except:
							pass

				expectedResult = [Sysgrpdic[d] for d in sysgrp_columns_seq if d in Sysgrpdic.keys()]
				newRow['System_grp'] = "|".join(expectedResult)

		for Item in filter(lambda item: item.ProductName in ("ControlEdge UOC System", "ControlEdge PLC System", "C300 System") or item.ProductName.startswith("Safety Manager"), Quote.MainItems):
			if Item.ProductName == "ControlEdge UOC System" and UOCFlag == '':
				UOCFlag = GS_PopUOC_Proposal.populateUOCproposal(Quote, Item, guid)
				R2Q_Cabinet_PLC_UOC.cab_plc_uoc(Item,Quote,cab_count_no,cab_count_yes)
			elif Item.ProductName == "ControlEdge PLC System" and PLCFlag == '' and Parent_guid==Item.ParentItemGuid:
				PLCFlag = GS_PopPLC_Proposal.populatePLCproposal(Quote, Item, guid)
				R2Q_Cabinet_PLC_UOC.cab_plc_uoc(Item,Quote,cab_count_no,cab_count_yes)
			elif Item.ProductName == "Safety Manager ESD" and SMFlag_ESD == '':
				SMFlag_ESD = GS_PopSM_Proposal.populateSMproposal(Quote, Item, guid)
			elif Item.ProductName == "Safety Manager FGS" and SMFlag_FGS == '':
				SMFlag_FGS = GS_PopSM_Proposal.populateSMproposal(Quote, Item, guid)
			elif Item.ProductName == "C300 System" and C300 == '':
				C300 = GS_PopC300_Proposal.populateC300proposal(Quote, Item, guid)

def BOM_Table(Quote):
	systems_list1 = ['ControlEdge UOC System','Safety Manager ESD','Safety Manager FGS','Experion Enterprise System','3rd Party Devices/Systems Interface (SCADA)','ControlEdge PLC System']
	systems_list2 = ['Field Device Manager','eServer System','Digital Video Manager']
	systems_list3 = ['C300 System','Terminal Manager','HC900 System']
	systems_list4 = ['Tank Gauging Engineering','Industrial Security (Access Control)','Fire Detection & Alarm Engineering','Skid and Instruments','Small Volume Prover']
	ScriptExecutor.ExecuteGlobal('GS_BOM_QT_TABLE_LOAD')
	quoteTable = Quote.QuoteTables["BOM_Table_for_Proposals"]
	quoteTable.Rows.Clear()
	names_table = Quote.QuoteTables["PAS_BOM_Group_Names"]
	names_table.Rows.Clear()
	if Quote.GetCustomField("Quote Type").Content=='Projects':
		execute1= ''
		execute2= ''
		execute3= ''
		execute4= ''
		for item in Quote.Items:
			if item.ProductName in systems_list1:
				execute1 = 'true'
			elif item.ProductName in systems_list2:
				execute2 = 'true'
			elif item.ProductName in systems_list3:
			 	execute3 = 'true'
			elif item.ProductName in systems_list4:
			 	execute4 = 'true'
			if execute1 != '' and execute2 != '' and execute3 != '' and execute4 != '':
			 	break
		if execute1 !="":
			ScriptExecutor.ExecuteGlobal('GS_PAS_BOM_Quote_Table_Generator')
		if execute2 != "":
			ScriptExecutor.ExecuteGlobal('GS_PAS_BOM_Quote_Table_Generator_2')
		if execute3 != "":
		 	ScriptExecutor.ExecuteGlobal('GS_PAS_BOM_Quote_Table_Generator_PMC')
		if execute4 != "":
		 	ScriptExecutor.ExecuteGlobal('GS_R2Q_TAS_NewExapansion_BOM_Generator')