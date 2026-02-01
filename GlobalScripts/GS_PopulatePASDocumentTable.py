# this action helps to populats Proposal
import GS_PopulatePASPLCDocumentTable
import GS_PopulatePASUOCDocumentTable
import GS_PopulatePASRTUDocumentTable
import GS_PopulatePASSMDocumentTable
import GS_PopulatePAS_EXPENT__DocumentTable
import GS_PAS_C300Documnet_Generater
QT_Table = Quote.QuoteTables["PAS_Document_Data"]
QT_Table.Rows.Clear()
PLCFlag=''
UOCFlag=''
RTUFlag=''
SMFlag=''
ExpEntFlag=''
C300=''
items = [x.ProductName for x in Quote.Items if x.ParentItemGuid == '']
lob = Quote.GetCustomField('Booking LOB').Content
quotetype = Quote.GetCustomField('Quote Type').Content
if lob in ('PAS','LSS','PMC') and quotetype == 'Projects' and 'New / Expansion Project' in items:
	for Item in Quote.MainItems:
		if Item.ProductName == "ControlEdge PLC System":
			PLCFlag = GS_PopulatePASPLCDocumentTable.populatePASData(Quote)
		elif Item.ProductName == "ControlEdge UOC System":
			UOCFlag = GS_PopulatePASUOCDocumentTable.populateUOCData(Quote)
		elif Item.ProductName == "ControlEdge RTU System":
			RTUFlag = GS_PopulatePASRTUDocumentTable.populateRTUData(Quote)
		elif "Safety Manager" in Item.ProductName:
			SMFlag = GS_PopulatePASSMDocumentTable.populateSMData(Quote)
		elif Item.ProductName == "Experion Enterprise System":
			ExpEntFlag = GS_PopulatePAS_EXPENT__DocumentTable.populateEXP_ENTData(Quote)
		elif Item.ProductName == "C300 System":
			C300 = GS_PAS_C300Documnet_Generater.populateC300DataPoP(Quote)
#pmd proposal run
ScriptExecutor.Execute('GS_CA_PAS_PMD_Document')
if (lob in ('PAS','LSS','PMC') and quotetype == 'Projects' and 'New / Expansion Project' in items) or (lob in ('PAS','LSS') and quotetype == 'Projects' and ('Winest Labor Import' in items or 'TPC System Name' in items)):
	#for pricing summery
	ScriptExecutor.Execute('GS_CA_PAS_PRICING_SUMMARY')