import GS_R2Q_FunctionalUtil
from GS_FinalizedActivities import PopulateFinalizedActivities

Session['R2Q_CompositeNumber'] = Quote.CompositeNumber
SellPricesStrategy = Product.Attr('Sell Price Strategy').SelectedValue.Display
customerBudget = Product.Attr('Customer_Budget_TextField').GetValue()
Quote.GetCustomField("SellPricestrategy").Content = SellPricesStrategy
Quote.GetCustomField("CustomerBudget").Content= customerBudget

try:
	
	if (Product.Attr('R2QRequest').GetValue() == 'Yes' and Quote.GetCustomField("R2Q_Save").Content == "Submit") or Product.Attr('R2QRequest').GetValue() != 'Yes':
		WTWQTDetails = Quote.QuoteTables['WTW_Prices_Calculation']
		WTWQTDetails.Rows.Clear()

		def getFloat(Var):
			if Var:
				return float(Var)
			return 0

		#PM deselect items on Add To Quote
		for row in Product.GetContainerByName('Cyber_Labor_Project_Management').Rows:
			if row.IsSelected:
				row.IsSelected = False

		SelectedProducts = Product.GetContainerByName('Cyber Configurations')
		for data in SelectedProducts.Rows:
			if data["Part Desc"] not in ['Project Management','Cyber Generic System']:
				laborCont = data.Product.GetContainerByName('Activities')
			elif data["Part Desc"] == 'Project Management':
				laborCont = Product.GetContainerByName('Cyber_Labor_Project_Management')
			elif data["Part Desc"] == 'Cyber Generic System':
				laborCont = Product.GetContainerByName('Generic_System_Activities')
			if data["Part Desc"] == 'Project Management':
				PartNumber = 'FO_Eng'
				Pricing = 'FOUnitWTWCost'
				FOWTWCost = 'FOUnitWTWCost'
				FO_List_Price = 'FO_ListPrice'
				FO_MPA_Price = 'FO_MPA_Price'
				Regional_Cost = 'Regional_Cost'
				hours = 'Final_Hrs'
			else:
				PartNumber = 'PartNumber'
				Pricing = 'Pricing'
				FOWTWCost = 'FOWTWCost'
				FO_List_Price = 'FO_List_Price'
				FO_MPA_Price = 'FO_MPA_Price'
				Regional_Cost = 'Regional_Cost'
				hours = 'Edit Hours'
			if laborCont:
				if laborCont.Rows.Count > 0:
					partsData = {}
					for item in laborCont.Rows:
						if item[PartNumber] != '':
							prices = {}
							if item[PartNumber] in partsData:
								item1 = partsData[item[PartNumber]]
								prices['unitcost'] = float(item1['unitcost']) + round(float(item[Pricing]),2) if item[Pricing] != '' else 0.00
								prices['FOWTWCost'] = float(item1['FOWTWCost']) + round(float(item[FOWTWCost]),2)if item[FOWTWCost] != '' else 0.00
								prices['listprice'] = float(item1['listprice']) + round(float(item[FO_List_Price]),2) if item[FO_List_Price] != '' else 0.00
								prices['MPAPrice'] = float(item1['MPAPrice']) + round(float(item[FO_MPA_Price]),2) if item[FO_MPA_Price] != '' else 0.00
								prices['regCost'] = float(item1['regCost']) + round(float(item[Regional_Cost]),2) if item[Regional_Cost] != '' else 0.00
								prices['Qty'] = float(item1['Qty']) + round(float(item[hours]),2) if item[hours] != '' else 0.00
								partsData[item[PartNumber]] = prices
							else:
								Trace.Write(item[PartNumber])
								prices['unitcost'] = round(float(item[Pricing]),2) if item[Pricing] != '' else 0.00
								prices['FOWTWCost'] = round(float(item[FOWTWCost]),2) if item[FOWTWCost] != '' else 0.00
								prices['listprice'] = round(float(item[FO_List_Price]),2) if item[FO_List_Price] != '' else 0.00
								prices['MPAPrice'] = round(float(item[FO_MPA_Price]),2) if item[FO_MPA_Price] != '' else 0.00
								prices['regCost'] = round(float(item[Regional_Cost]),2) if item[Regional_Cost] != '' else 0.00
								prices['Qty'] = round(float(item[hours]),2) if item[hours] != '' else 0.00
								partsData[item[PartNumber]] = prices
					Final_Activities = data.Product.GetContainerByName('Final_Activities')
					for row1 in Final_Activities.Rows:
						if row1.Product.PartNumber in partsData.keys():
							WTWPrices = WTWQTDetails.AddNewRow()
							WTWPrices['GUID'] = row1.UniqueIdentifier
							partsDataval = partsData[row1.Product.PartNumber]
							if partsDataval['Qty'] >0:
								WTWPrices['QI_FoWTWCost'] =  partsDataval['FOWTWCost']/partsDataval['Qty']
								WTWPrices['QI_GESRegionalCost'] = partsDataval['regCost']/partsDataval['Qty']
								WTWPrices['QI_LaorPartsListPrice'] = partsDataval['listprice']/partsDataval['Qty']
								WTWPrices['QI_MPA_Price'] = partsDataval['MPAPrice']/partsDataval['Qty']
							else:
								WTWPrices['QI_FoWTWCost'] =  0.00
								WTWPrices['QI_GESRegionalCost'] = 0.00
								WTWPrices['QI_LaorPartsListPrice'] = 0.00
								WTWPrices['QI_MPA_Price'] = 0.00
		WTWQTDetails.Save()
	Quote.GetCustomField('CF_CYBER_DEFINE_PRICELIST').Content = ''
	Quote.GetCustomField('CF_CYBER_DEFINE_PRICELIST_CPS').Content = ''
	Quote.GetCustomField('cyberProductPresent').Content = "Yes"

except Exception as ex:
	msg = 'Error Occured, {"ErrorCode": "PartsLaborConfig", "ErrorDescription": "Failed at: Add to Quote"}'
	GS_R2Q_FunctionalUtil.UpdateStatusMessage(Quote, "Error", "Notification", msg)
	raise