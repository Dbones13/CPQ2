def getContainer(Name):
	return Product.GetContainerByName(Name)

def getattvalue(attName):
	return Product.Attr(attName)
country = Quote.GetCustomField('Account Address Country').Content
opmBasicInfoCon = getContainer('OPM_Basic_Information')
#migrationPlatform = getContainer("OPM_Migration_platforms")
#servicesCon = getContainer("OPM_Services")
#msidcommon = getContainer("MSID_CommonQuestions")
selectedProducts = Product.Name
if "OPM" in selectedProducts:
	for row in opmBasicInfoCon.Rows:
		Trace.Write(row["OPM_Is_the_Experion_System_LCN_Connected"])
		if row["OPM_Is_the_Experion_System_LCN_Connected"] == "No":
			#for row1 in migrationPlatform.Rows:
			attr_lcn = getattvalue("OPM_Experion_Server_Hardware_Selection")
			for value in attr_lcn.Values:
				if value.Display in ('Dell R740XL'):
					Trace.Write("check5")
					value.Allowed = False
		row.ApplyProductChanges()
		break
'''	#for Row2 in migrationPlatform.Rows:
	attr1 = getattvalue("OPM_Experion_Server_Hardware_Selection")
	attr2 = getattvalue("OPM_Other_Servers_Hardware_Selection")
	attr3 = getattvalue("OPM_Select_RESS_platform_configuration")
	attr4 = getattvalue("OPM_ACET_EAPP_Server_Hardware_Selection")
		
	for values in attr1.Values:
		if country not in ('china','China'):
			Trace.Write("This is hi2.2.0:{0}".format(values.Display))
			if values.Display in ('DELL T360','DELL R450 STD No TPM','HP DL360 G10'):
				values.Allowed = False
			
				Trace.Write("Done1")
		#Row2.ApplyProductChanges()
		#break
	for values in attr2.Values:
		if country not in ('china','China'):
			if values.Display in ('DELL T360','DELL R450 STD No TPM','HP DL360 G10'):
				values.Allowed = False
				Trace.Write("Done2")
		#Row2.ApplyProductChanges()
	for values in attr3.Values:
		if country not in ('china','China'):
			if values.Display in ('DELL T360','DELL R450 STD No TPM','HP DL360 G10'):
				values.Allowed = False
				Trace.Write("Done3")
		#Row2.ApplyProductChanges()
	for values in attr4.Values:
		if country not in ('china','China'):
			if values.Display in ('DELL T360','DELL R450 STD No TPM','HP DL360 G10'):
				values.Allowed = False
				Trace.Write("Done3")
			#Row2.ApplyProductChanges()'''