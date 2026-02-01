Product.Attr('Implementation Methodology').SelectDisplayValue('Standard Build Estimate')
attributes = {
    'Number of FTE Communities': '1',
    'Number of FTE Community Locations': '1',
    'Number of Locations with FTE Switches': '1',
    'Number of Modbus Interfaces Types': '1',
    'Number of Profibus Interface Types': '1',
    'Number of EtherNet IP Interface Types': '1',
    'Number of OPC Interface Types': '1'
}
for attr, val in attributes.items():
    Product.Attr(attr).AssignValue(val)
con_grp = Product.GetContainerByName('Experion_Enterprise_Cont').Rows
Flex_Qty = 0
Esd_Fgs = 0
Nscc = 1
safeview = ""
display_map = {0: "Single", 1: "Single", 2: "Dual", 3: "Triple", 4: "Quad"}
configs = []
orion_is_55 = False
for row in con_grp:
	orion_flex = row.Product.Attr("Flex Station Qty (0-60)").GetValue() or 0
	cms_flex = row.Product.Attr("CMS Flex Station Qty 0_60").GetValue() or 0
	dms_flex = row.Product.Attr("DMS Flex Station Qty 0_60").GetValue() or 0
	Nscc += int(row.Product.Attr('Network Cabinet Required (0-50)').GetValue() or 0)
	Esd_Fgs += int(row.Product.Attr('ESD_FGS_Aux_PanelsConsoles').GetValue() or 0)
	Flex_Qty += int(orion_flex) + int(cms_flex)+ int(dms_flex)
	cabinetyes = row.Product.Attr('CMS Cabinet Mounting Stations required').GetValue().strip().lower()
	deskyes = row.Product.Attr('DMS Desk Mounting Stations required').GetValue().strip().lower()
	orionyes = row.Product.Attr('Orion Stations required').GetValue().strip().lower()
	if cabinetyes != "no":
		cms_display = int(row.Product.Attr('Cabinet_No_of_Displays (0-4)').GetValue() or 0)
		configs.append(display_map.get(cms_display))
	if deskyes != "no":
		dms_display = int(row.Product.Attr('DMS No of Displays 0_4').GetValue() or 0)
		configs.append(display_map.get(dms_display))
	if orionyes != "no":
		orion_disp_size = row.Product.Attr('Orion Console Display Size').GetValue().strip().lower()
		orion_disp_count = int(row.Product.Attr('Orion Console Display Devices (0-4)').GetValue() or 0)
		if "55" in orion_disp_size:
			orion_is_55 = True
			configs.append("Quad")
		elif "23" in orion_disp_size:
			configs.append(display_map.get(orion_disp_count))
configs = [cfg for cfg in configs if cfg]
if orion_is_55:
	if all(c == "Quad" for c in configs):
		safeview = "Quad"
	else:
		safeview = "Combination of SafeView Configurations"
else:
	if configs and all(c == configs[0] for c in configs):
		safeview = configs[0]
	else:
		safeview = "Combination of SafeView Configurations"
safeview = "Quad/Orion" if safeview=="Quad" else safeview # CXCPQ-117670
Product.Attr('SafeView Factor (Max quanity of Monitors in One Station)').SelectDisplayValue(safeview)

Product.Attr('Network and Server Cabinet Count').AssignValue(str(Nscc))
Product.Attr('Number of Console Sections with Hardwired IO').AssignValue(str(Esd_Fgs))
Product.Attr('Number of Station Types').AssignValue('1') if Flex_Qty > 0 else Product.Attr('Number of Station Types').AssignValue('0')