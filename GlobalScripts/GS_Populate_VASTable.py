#CXCPQ-46820:06/01/2023: GS_Populate_VASTable script inserts VAS WriteIn products into PMC_VAS_WriteIns Quote table. This script is called from a custom action while generating the document.

def populateQuoteTableRow(table , dataDict , row = None):
	if not row:
		row = table.AddNewRow()
	for key , value in dataDict.items():
		row[key] = value

def populateVAS(Quote):
	if Quote.GetCustomField('Booking LOB').Content == "PMC":
		vas_table=Quote.QuoteTables["PMC_VAS_WriteIns"]
		vas_table.Rows.Clear()
		#vas_table.Save()

		#vas_serialnum = 1
		vas_table_row = {}

		for qitem in Quote.Items:
			WriteIn_VAS_Query = SqlHelper.GetFirst("SELECT VASProduct FROM WriteInProducts(nolock) WHERE VASProduct='Yes' and Product='{}'".format(qitem.PartNumber))
			#check whether the item is VAS WriteIn and Item Type as BASE.
			if WriteIn_VAS_Query: # Populate both Base and Optional VAS WriteIns
				vas_table_row["SerialNr_VAS"]=qitem.RolledUpQuoteItem #vas_serialnum
				vas_table_row["PartNumber_VAS"]=qitem.PartNumber
				vas_table_row["Description_VAS"]=qitem.Description
				vas_table_row["Quantity_VAS"]=qitem.Quantity
				vas_table_row["UnitPrice_VAS"]=qitem.ListPrice
				vas_table_row["TotalPrice_VAS"]=qitem.ExtendedListPrice
				vas_table_row["VAS_Flag"] = WriteIn_VAS_Query.VASProduct
				vas_table_row["Codes"]=qitem["QI_ExtendedDescription"].Value
				#Added ItemType field
				vas_table_row["ItemType"] = "Base" if qitem.ItemType == 0 else "Optional"
				populateQuoteTableRow(vas_table,vas_table_row)
				#vas_serialnum += 1
		vas_table.Save()