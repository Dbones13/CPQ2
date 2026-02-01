'''New Script is created to manage the visibility of custom fields within the "OPPORTUNITY INFO" tab replacing GS_Custom Field Visibilty'''
from GS_CommonModule import getCF,getCFValue,hideCF

if getCFValue(Quote, "Booking LOB") == "PMC" and getCFValue(Quote, "Quote Type") == "Parts and Spot":
	hideCF(getCF(Quote, 'Opp Prod Desc'))
	if getCFValue(Quote, "Global Major Project") == 'False':
		hideCF(getCF(Quote, "Global Major Project"))

elif getCFValue(Quote, "Booking LOB") != "PMC" or getCFValue(Quote, "Quote Type") != "Parts and Spot":
	hideCF(getCF(Quote, "Opportunity Owner Name"))
	hideCF(getCF(Quote, "Opportunity Owner Phone No"))
	hideCF(getCF(Quote, "Opportunity Owner Email"))


if getCFValue(Quote, "Quote Type") != "Projects":
	hideCF(getCF(Quote, "Systems Price List"))
else:
	hideCF(getCF(Quote, "Parts Price List"))