import math
def setAtvQty(AttrName,Model_Number,qty):
	product_attr_val=Product.Attr(AttrName).Values
	for av in product_attr_val:
		if av.Display == Model_Number:
			if float(qty)>0:
				av.IsSelected=True
				av.Quantity=float(qty)
			else:
				av.IsSelected=False
				av.Quantity=0
			break

def deleteRowsByCondition(container_name, io_types):
	cont = Product.GetContainerByName(container_name)
	io_type_set = set(io_types)  # Faster lookup
	rows_to_delete = [row.RowIndex for row in cont.Rows if row['IO_Section'] in io_type_set]

	for row_index in sorted(rows_to_delete, reverse=True):
		cont.DeleteRow(row_index)

if Quote.GetCustomField("R2QFlag").Content=='Yes':
	tas_system = Quote.GetCustomField("R2Q_Type_of_TAS_System").Content
	Product.Attr('R2Q_Type_of_TAS_System').SelectValue(tas_system)
	rack_quantity = 0.0
	HC900_Rack_Cont = Product.GetContainerByName('HC900_Rack_Size_Quantity_Cont')
	if HC900_Rack_Cont.Rows.Count>0:
		for row in HC900_Rack_Cont.Rows:
			if row['Rack Size'] == "8 I/O Slot Rack":
				if row['Quantity']:
					rack_quantity = float(row['Quantity'])
					setAtvQty('HC900_PART_SUMMARY','900R08R-0300',rack_quantity)
				
	lv_System_Type=Product.Attributes.GetByName("HC900_System_Type").GetValue()
	Product.Attr('R2QRequest').AssignValue('Yes')
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
	if tas_system == 'Non-Red':
		Product.DisallowAttr('HC900_Controller_(CPU)_Module')
		Product.DisallowAttr('HC900_Controller_(CPU)_Module_NSIL2')
		Product.Attr('HC900_Controller_(CPU)_Module').SelectValue('')
		Product.Attr('HC900_Controller_(CPU)_Module_NSIL2').SelectValue('')
		Product.Attr('HC900 Ethernet Switching Hub').AssignValue('1')
		
	else:
		Product.Attr('HC900 Ethernet Switching Hub').AssignValue('2')
		if lv_System_Type=='SIL2 Safety System':
			Product.AllowAttr('HC900_Controller_(CPU)_Module_NSIL2')
			Product.Attr('HC900_Controller_(CPU)_Module_NSIL2').SelectValue('Redundant Controller C75 CPU - SIL2')
			Product.DisallowAttr('HC900_Controller_(CPU)_Module')

		elif lv_System_Type=='Non-SIL HC900 System':
			Product.AllowAttr('HC900_Controller_(CPU)_Module')
			Product.Attr('HC900_Controller_(CPU)_Module').SelectValue('Redundant Controller C75 CPU')
			Product.DisallowAttr('HC900_Controller_(CPU)_Module_NSIL2')

	io_types_by_container = {
		'HC900_IO_Details_of_SIL2': [
			"Analog Inputs (Universal, 8 channel)",
			"Analog Outputs (4 channel, 10 modules/rack)",
			"Analog Outputs (8 channel, 5 modules/rack)",
			"Digital Inputs - contact (16 channel)",
			"Digital Inputs -24 VDC (16 channel)",
			"Digital Inputs -120/240 VAC (16 channel)",
			"Digital inputs -120/240 VAC - 125 VDC (16 channel isolated)",
			"Digital Outputs -Relay (8 channel)",
			"Digital Outputs -24 VDC (16 channel)",
			"Digital Outputs -120/240 VAC (8 channel)"
		],
		'HC900_IO_Details_of_Non-SIL': [
			"Analog Inputs (Universal, 8 channel)",
			"SIL Universal IO Module (AI/DO/DI, 4-20mA, 16 channel)",
			"Analog Outputs (4 channel, 10 modules/rack)",
			"Analog Outputs (8 channel, 5 modules/rack)",
			"SIL Universal Analog Outputs 4-20 mA (8 channel)",
			"Digital Inputs - contact (16 channel)",
			"Digital Inputs -24 VDC (16 channel)",
			"Digital Inputs -120/240 VAC (16 channel)",
			"Digital Inputs -120/240 VAC (16 channel)",  # Duplicate
			"Digital inputs -120/240 VAC - 125 VDC (16 channel isolated)",
			"Digital Outputs -Relay (8 channel)",
			"Digital Outputs -24 VDC (16 channel)",
			"Digital Outputs -120/240 VAC (8 channel)",
			"Pulse/Frequency (PFM, 4 channel, 4 modules per rack)"
		]
	}

	for container, io_types in io_types_by_container.items():
		deleteRowsByCondition(container, io_types)
	Product.ApplyRules()
