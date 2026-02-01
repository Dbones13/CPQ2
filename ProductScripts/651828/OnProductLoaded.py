def select_AttrVal(attr,val):
	Product.Attr(attr).SelectDisplayValue(val)
def allow_disallow(attrlist, allow=True):
	for attr in attrlist:
		if allow:
			Product.AllowAttr(attr)
		else:
			Product.DisallowAttr(attr)

attr_dict = {
	'CMS Cabinet Mounting Stations required': {
		'values': ["CMS Flex Station Qty 0_60", "Cabinet_IKB_or_OEP", "Cabinet_Industrial_KB_Mouse", "Cabinet_No_of_Displays (0-4)"]
	},
	'DMS Desk Mounting Stations required': {
		'values': ["DMS Flex Station Qty 0_60", "DMS TPS Station Qty 0_20", "DMS No of Displays 0_4", "DMS IKB or OEP"]
	},
	'Orion Stations required': {
		'values': ["Flex Station Qty (0-60)", "Orion_2P_Base_Unit_Left", "Orion Console Left Auxiliary Equipment Unit (0-40)", "Orion_3P_Base_Unit_Left", "Orion Console Display Size", "Orion Console Display Devices (0-4)", "Orion Console Membrane KB Type", "Orion_Console_Units_Config"]
	},
	'Printer Required?': {
		'values': ['LaserJet Printer - Monochrome (0-99)', 'Colour A4 printer', 'B_W_A3_printer', 'Colour_A3_printer']
	}
}

for key, value in attr_dict.items():
	if Product.Attr(key).GetValue() == 'Yes':
		allow_disallow(value['values'], allow=True)
		if 'attr_value' in value:
			for item in value['attr_value']:
				for att, val in item.items():
					Product.Attr(att).SelectDisplayValue(val)
	else:
		allow_disallow(value['values'], allow=False)

Product.Attr("R2QRequest").AssignValue("Yes")
Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
DeskAttr = ["Server Node Type_desk","Desk _Mount_Server"]
rackAttr = ["Rack_Mount_Server","Server_NodeType"]
if Product.Attr('Server Mounting').GetValue() == "Cabinet":
	allow_disallow(rackAttr,allow=True)
	allow_disallow(DeskAttr,allow=False)
else:
	allow_disallow(DeskAttr,allow=True)
	allow_disallow(rackAttr,allow=False)
if int(Product.Attr('Additional Stations').GetValue()) > 0:
	Product.AllowAttr("Station Type")
else:
	Product.DisallowAttr("Station Type")

if Product.Attr("Opc_server_required").GetValue() == "Yes" or Product.Attr("Domain_Controller_Required").GetValue() == "Yes":
	Product.AllowAttr("Server Type1")
else:
	Product.DisallowAttr("Server Type1")  
Product.Attr("Orion Console 2Position Base Unit (0-20)").AssignValue(Product.Attr("Orion_2P_Base_Unit_Left").GetValue())
Product.Attr("Orion Console 3Position Base Unit (0-20)").AssignValue(Product.Attr("Orion_3P_Base_Unit_Left").GetValue())
Aux_eqp = int(Product.Attr("Orion Console Left Auxiliary Equipment Unit (0-40)").GetValue() or 0)
Flex_qty = int(Product.Attr("Flex Station Qty (0-60)").GetValue() or 0)
Pbase_unit_2 = int(Product.Attr("Orion Console 2Position Base Unit (0-20)").GetValue() or 0)
Pbase_unit_3 = int(Product.Attr("Orion Console 3Position Base Unit (0-20)").GetValue() or 0)

if (3*Aux_eqp) < Flex_qty:
	Product.AllowAttr("Orion_Aux_Qty_Less_Stn_Qty")
else:
	Product.DisallowAttr("Orion_Aux_Qty_Less_Stn_Qty")
if ((2* Pbase_unit_2)+(3* Pbase_unit_3)) < Flex_qty:
	Product.AllowAttr("Orion_Pos_Base_Less_Stn_Qty")
else:
	Product.DisallowAttr("Orion_Pos_Base_Less_Stn_Qty")
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content else False

if Product.Attr("DMS Flex Station Hardware Selection").GetValue()=="STN_PER_DELL_Rack_RAID1" and isR2Qquote:
	Product.Attr('DMS Remote Peripheral Solution Type RPS').SelectDisplayValue('Pepperl+Fuchs BTC12')
else:
	Product.Attr('DMS Remote Peripheral Solution Type RPS').SelectDisplayValue('None')

if Product.Attr("CMS Flex Station Hardware Selection").GetValue()=="STN_PER_DELL_Rack_RAID1":
	Product.Attr('CMS Remote Peripheral Solution Type RPS').SelectDisplayValue('Pepperl+Fuchs BTC12')
else:
	Product.Attr('CMS Remote Peripheral Solution Type RPS').SelectDisplayValue('None')

if Product.Attr("CMS Flex Station Hardware Selection").GetValue()=="STN_PER_DELL_Rack_RAID1" and Product.Attr("CMS Remote Peripheral Solution Type RPS").GetValue()!="Pepperl_Fuchs_BTC12" and not isR2Qquote:
	Product.AllowAttr("Remote Peripheral validation message")
else:
	Product.DisallowAttr("Remote Peripheral validation message")

station_qty = Product.Attr('Flex Station Qty (0-60)').GetValue() if Product.Attr('Flex Station Qty (0-60)').GetValue() else 0
if int(station_qty) > 0:
	Product.AllowAttr('Flex Station Hardware Selection TPS')
else:
	Product.DisallowAttr('Flex Station Hardware Selection TPS')
DMSstation_qty = Product.Attr('DMS Flex Station Qty 0_60').GetValue() if Product.Attr('DMS Flex Station Qty 0_60').GetValue() else 0
if int(DMSstation_qty) > 0:
	Product.AllowAttr('DMS Flex Station Hardware Selection')
else:
	Product.DisallowAttr('DMS Flex Station Hardware Selection')
cmsstation_qty = Product.Attr('CMS Flex Station Qty 0_60').GetValue() if Product.Attr('CMS Flex Station Qty 0_60').GetValue() else 0
if Product.Attr('CMS Cabinet Mounting Stations required').GetValue() == "No" or (Product.Attr('CMS Cabinet Mounting Stations required').GetValue() == "Yes" and int(cmsstation_qty) == 0):
	Product.DisallowAttr("CMS Flex Station Hardware Selection")
else:
	Product.AllowAttr("CMS Flex Station Hardware Selection")

dmsStation_qty = Product.Attr('DMS Flex Station Qty 0_60').GetValue() if Product.Attr('DMS Flex Station Qty 0_60').GetValue() else 0
if Product.Attr('DMS Desk Mounting Stations required').GetValue() == "No" or (Product.Attr('DMS Desk Mounting Stations required').GetValue() == "Yes" and int(dmsStation_qty) == 0):
	Product.DisallowAttr("DMS Flex Station Hardware Selection")
else:
	Product.AllowAttr("DMS Flex Station Hardware Selection")

orionStation_qty = Product.Attr('Flex Station Qty (0-60)').GetValue() if Product.Attr('Flex Station Qty (0-60)').GetValue() else 0
if Product.Attr('Orion Stations required').GetValue() == "No" or (Product.Attr('Orion Stations required').GetValue() == "Yes" and int(orionStation_qty) == 0):
	Product.DisallowAttr("Flex Station Hardware Selection TPS")
else:
	Product.AllowAttr("Flex Station Hardware Selection TPS")
EBR_Experion = Product.Attr('Experion Backup & Restore (Experion Server)').GetValue()
EBR_flex = Product.Attr('Experion Backup & Restore (Flex Station ES-F)').GetValue()
if EBR_Experion == 'Yes' or EBR_flex == 'Yes':
    Product.AllowAttr('Server Node Type EBR')
    Product.AllowAttr('EBR Server')
else:
    Product.DisallowAttr('Server Node Type EBR')
    Product.DisallowAttr('EBR Server')
if Product.Attr('CMS Cabinet Mounting Stations required').GetValue() == "Yes" and isR2Qquote:
	Product.Attr('CMS Remote Peripheral Solution Type RPS').SelectDisplayValue('Pepperl+Fuchs BTC22')
	Trace.Write('CMS RPSTYPE ---- '+str(Product.Attr('CMS Remote Peripheral Solution Type RPS').GetValue()))