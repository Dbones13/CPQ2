'''New Script is created to manage the visibility of custom fields within the "ACCOUNT " tab replacing GS_Custom Field Visibilty'''

from GS_CommonModule import getCFValue,hideCF,getCF

Customfields = ['Expedite Fee Waiver','Access to Inventory','Minimum Order Fee Waiver','Entitlement']
if getCFValue(Quote, "Booking LOB") == "PMC":
	hideCF(getCF(Quote,"MPA Price Plan"))
	if getCFValue(Quote, "Quote Type") == "Parts and Spot":
		for field in Customfields:
			hideCF(getCF(Quote , field))

if getCFValue(Quote,'Quote Tab Booking LOB') == 'LSS' and getCFValue(Quote, "Quote Type") == 'Parts and Spot':
	exchangeRate = getCFValue(Quote,'Exchange Rate') if getCFValue(Quote,'Exchange Rate').strip() !='' else 1.0
	sellPrice	 = float(UserPersonalizationHelper.ConvertToNumber(getCFValue(Quote,"Total Sell Price"))) / float(exchangeRate)
	getCF(Quote,'Minimum Order Fee').Visible = True
	if  ((sellPrice > 600 )or getCFValue(Quote,'Minimum Order fee Waiver reason') or getCFValue(Quote,'Minimum Order Fee Waiver')== 'True'):
		setCFValue(Quote, 'Minimum Order Fee', '0')
	elif ((sellPrice < 600 )or not(getCFValue(Quote,'Minimum Order fee Waiver reason') or getCFValue(Quote,'Minimum Order Fee Waiver')== 'True')):
		getCF(Quote,'Minimum Order Fee').Visible = True

if getCFValue(Quote, "Booking LOB") not in ('LSS','PAS') and getCFValue(Quote, "Quote Type") != "Projects":
	if not getCFValue(Quote , "MPA") and  not getCFValue(Quote , "MPA Price Plan"):
		hideCF(getCF(Quote,"MPA Price Plan"))