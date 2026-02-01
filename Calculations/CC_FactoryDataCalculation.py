if Quote.GetGlobal('PerformanceUpload') != 'Yes':
	def filterRecord(Part_number=None, MRP_indicator=None,FixedVender=None,records=None):
		result = []
		if records is None: return result
		if Part_number!=None:
			for i in records:
				if i.Material==Part_number:
					result.append(i)
			return result
		if MRP_indicator!=None:
			for i in records:
				if i.MRP_Indicator==MRP_indicator:
					result.append(i)
			return result
		if FixedVender!=None:
			for i in records:
				if i.Fixed_vendor==FixedVender:
					result.append(i)
			return result


	if Quote.GetCustomField("CF_Factory_Data_Applicable").Content == "Y":
		quote_expiry_date = str(Quote.EffectiveDate.Date).split(' ')[0]
		# Filter custom table data
		query = "Select * from CT_VENDOR_INFORMATION WHERE Valid_from <= '{}' and Valid_to >= '{}' and Material = '{}'".format(quote_expiry_date, quote_expiry_date,Item.PartNumber)
		result = SqlHelper.GetList(query)
		# iterate cart items
		if len(list(Item.AsMainItem.Children))==0:
			if len(result)!=0:
					if len(result) > 1:
						result2=filterRecord(FixedVender='X',records=result) # filtered result by Fixed vender 
						if(len(result2)!=0):
							Item.QI_FactoryCode.Value=result2[0].Vendor
							Item.QI_FactoryName.Value = result2[0].Vendor_Name
						else:
							result3=filterRecord(MRP_indicator='1',records=result) # filtered result by  MRP_Indicator
							if(len(result3)!=0):
								Item.QI_FactoryCode.Value = result3[0].Vendor
								Item.QI_FactoryName.Value = result3[0].Vendor_Name
							else:
								Item.QI_FactoryCode.Value = result[0].Vendor
								Item.QI_FactoryName.Value = result[0].Vendor_Name
					else:
						Item.QI_FactoryCode.Value = result[0].Vendor
						Item.QI_FactoryName.Value = result[0].Vendor_Name
		else:
			Item.QI_FactoryCode.Value = ""
			Item.QI_FactoryName.Value = ""