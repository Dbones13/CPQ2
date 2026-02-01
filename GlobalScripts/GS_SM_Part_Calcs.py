from math import ceil
import System.Decimal as D
import GS_Power_Supply_calcs
import GS_SMPartsCalc

def get_int(val):
	if val:
		return int(val)
	return 0

def get_float(val):
	if val:
		return float(val)
	return 0.0

def try_get_attr(attr, key, default):
	try:
		return getattr(attr, key)
	except AttributeError, e:
		return default

def try_get_int_attr(attr, key, default):
	try:
		return get_int(getattr(attr, key))
	except AttributeError, e:
		return default

def get_di_do_barrier_sil2_pdio_nrd(attr):
	return try_get_int_attr(attr, "sdi1_dio_nrd_is", 0) + try_get_int_attr(attr, "sdi1_line_mon_dio_nrd_is", 0) + try_get_int_attr(attr, "sdo1_dio_nrd_is", 0)

def get_di_do_barrier_sil2_pdio_rd(attr):
	return try_get_int_attr(attr, "sdi1_dio_rd_is", 0) + try_get_int_attr(attr, "sdi1_line_mon_dio_rd_is", 0) + try_get_int_attr(attr, "sdo1_dio_rd_is", 0)

def get_di_do_barrier_sil2_uio_nrd(attr):
	return try_get_int_attr(attr, "sdi1_uio_nrd_is", 0) + try_get_int_attr(attr, "sdi1_line_mon_uio_nrd_is", 0) + try_get_int_attr(attr, "sdo1_uio_nrd_is", 0) + try_get_int_attr(attr, "sdo2_1a_uio_nrd_is", 0) + try_get_int_attr(attr, "sdo4_2a_uio_nrd_is", 0) + try_get_int_attr(attr, "sdo7_line_mon_uio_nrd_is", 0)

def get_di_do_barrier_sil2_uio_rd(attr):
	return try_get_int_attr(attr, "sdi1_uio_rd_is", 0) + try_get_int_attr(attr, "sdi1_line_mon_uio_rd_is", 0) + try_get_int_attr(attr, "sdo1_uio_rd_is", 0) + try_get_int_attr(attr, "sdo2_1a_uio_rd_is", 0) + try_get_int_attr(attr, "sdo4_2a_uio_rd_is", 0) + try_get_int_attr(attr, "sdo7_line_mon_uio_rd_is", 0)

def get_ai_barrier_sil2_uio_nrd(attr):
	return try_get_int_attr(attr, "sai1_uio_nrd_is", 0) + try_get_int_attr(attr, "sai1_fire2_wire_uio_nrd_is", 0) + try_get_int_attr(attr, "sai1_fire34_wire_uio_nrd_is", 0) + try_get_int_attr(attr, "sai1_fire34_wire_sink_uio_nrd_is", 0) + try_get_int_attr(attr, "sai1_gas_uio_nrd_is", 0)

def get_ai_barrier_sil2_uio_rd(attr):
	return try_get_int_attr(attr, "sai1_uio_rd_is", 0) + try_get_int_attr(attr, "sai1_fire2_wire_uio_rd_is", 0) + try_get_int_attr(attr, "sai1_fire34_wire_uio_rd_is", 0) + try_get_int_attr(attr, "sai1_fire34_wire_sink_uio_rd_is", 0) + try_get_int_attr(attr, "sai1_gas_uio_rd_is", 0)


def get_cg_parts(Product, attr, attrs, parts_dict, total_rio_cabinet_summary):
	#CXCPQ-31207
	qty = ceil((get_int(attr.sdo7_line_mon_uio_rd_is)+get_int(attr.sdo7_line_mon_uio_rd_nis))/7.0) + ceil((get_int(attr.sdo7_line_mon_uio_nrd_is)+get_int(attr.sdo7_line_mon_uio_nrd_nis))/7.0)
	if qty:
		parts_dict["FC-TDOL-0724U"] = {'Quantity' : qty, 'Description': 'SM RIO DO FTA, loop mon, 2A, 24VDc, 7ch'}

	if attr.saftey_io_switch == "ThirdParty_MOXA":
		part_map = {
			"MOXA: EDS-316-MM-SC-HPS" : "4600112",
			"MOXA: EDS-316-SS-SC-HPS_C" : "4600136",
			"MOXA: EDS-316-SS-SC-HPS" : "4600130",
			"MOXA: EDS-316-MM-SC-HPS_C" : "4600121"
		}
		part = "MOXA: EDS-316-{}-SC-HPS{}"
		k1, k2 = "MM", ""
		if attr.distance_to_module != "<4KM":
			k1 = "SS"
		if attr.extended_temp != "No" or attr.conformally_coated != "No":
			k2 = "_C"
		part = part.format(k1,k2)

		qty = GS_SMPartsCalc.getNoOfEDS316Switches(
			Product,
			parts_dict.get('FC-TUIO11', {'Quantity' : 0})['Quantity'],
			parts_dict.get('FC-TDIO11', {'Quantity' : 0})['Quantity'],
			parts_dict.get('FC-IOTA-NR24', {'Quantity' : 0})['Quantity'],
			parts_dict.get('FC-IOTA-R24', {'Quantity' : 0})['Quantity']
		)
		if qty:
			parts_dict[part_map[part]] = {'Quantity' : qty, 'Description': part}

	if parts_dict.get("FC-GPCS-RIO16-PF"):
		gcps = ceil(parts_dict.get("FC-GPCS-RIO16-PF")["Quantity"] / 3.0)
		parts_dict["4603323"] = {'Quantity' : gcps, 'Description': 'MOB3 MOUNTING CHASSIS IS - 34 INCH'}

	if attr.cabinet_feeder == "Externally_Sourced_24VDC":
		qty = GS_Power_Supply_calcs.getNoPowerSupply(Product)
		Trace.Write(str(qty))
		if get_float(qty):
			parts_dict["FS-PDC-MB24-4P"] = {'Quantity' : 2 * get_float(qty) , 'Description': 'POWER DISTR.CABLE MB-0001 TO QUINT4 PSU'}
	
	if attrs.marshalling_option == "Universal Marshalling":
		qty = (
			get_di_do_barrier_sil2_pdio_nrd(attrs)
			+ get_di_do_barrier_sil2_pdio_rd(attrs)
			+ get_di_do_barrier_sil2_uio_nrd(attrs)
			+ get_di_do_barrier_sil2_uio_rd(attrs)
		)
		if qty:
			parts_dict["FC-UGDA01"] = {'Quantity' : qty, 'Description': "SCA DIGITAL INPUT/OUTPUT SIL 2 BARRIER"}

		qty = (
			get_ai_barrier_sil2_uio_nrd(attrs)
			+ get_ai_barrier_sil2_uio_rd(attrs)
		)
		if qty:
			parts_dict["FC-UGAI01"] = {'Quantity' : qty, 'Description': "SCA ANALOG INPUT SIL2 BARRIER"}

		qty = try_get_int_attr(attrs, "sao1_uio_nrd_is", 0) + try_get_int_attr(attrs, "sao1_uio_rd_is", 0)
		if qty:
			parts_dict["FC-UGAO01"] = {'Quantity' : qty, 'Description': "SCA ANALOG OUTPUT SIL 2 BARRIER"}

	if attr.Marshalling_Opt_cg == "Hardware_Marshalling_with_P+F":
		#CXCPQ-31201

		type_ao = int(attr.type_uio_ai_rd) + int(attr.type_uio_ai_nrd)
		if type_ao > 0 or type_ao != '':
			parts_dict["HIC2025"] = {'Quantity' : type_ao, 'Description': 'P+F SMART transm. power supply SIL2 1ch'}
		#CXCPQ-31199
		sil2_do = int(attr.sil2_uio_di_rd) + int(attr.sil2_uio_di_nrd)
		if sil2_do > 0 or sil2_do != '':
			parts_dict["HIC2831R2"] = {'Quantity' : sil2_do, 'Description': 'P+F Isolator switch ampl. SIL2 LFD 1ch'}
			#parts_dict["HIC2025"] = {'Quantity' : sil2_do, 'Description': 'P+F SMART transm. power supply SIL2 1ch'}
		#CXCPQ-31203
		sil3_do = int(attr.sil3_uio_do_rd) + int(attr.sil3_uio_do_nrd)
		if sil3_do > 0 or sil3_do != '':
			parts_dict["HIC2871"] = {'Quantity' : sil3_do, 'Description': 'P+F Solenoid driver SIL3 1ch'}
		#CXCPQ-31202
		type_ao = int(attr.type_uio_ao_rd) + int(attr.type_uio_ao_nrd)
		if type_ao > 0 or type_ao != '':
			parts_dict["HIC2031"] = {'Quantity' : type_ao, 'Description': 'P+F SMART repeater SIL2 1ch'}
		#CXCPQ-31200
		sil3_di =int(attr.sil3_uio_di_rd) + int(attr.sil3_uio_di_nrd)
		if sil3_di > 0 or sil3_di != '':
			parts_dict["HIC2853R2"] = {'Quantity' : sil3_di, 'Description': 'P+F Isolator switch amplifier SIL3 1ch'}
	#CXCPQ-31794
	if attr.Marshalling_Opt_cg == 'Hardware_Marshalling_with_Other' and attr.Universal_IOTA == 'PUIO':
		sdo7_rd_nis = attr.sdo7_line_mon_uio_rd_nis if attr.sdo7_line_mon_uio_rd_nis else 0
		sdo7_nrd_nis = attr.sdo7_line_mon_uio_nrd_nis if attr.sdo7_line_mon_uio_nrd_nis else 0
		FC_TDOL_0724U_Quantity = ceil(float(sdo7_rd_nis)/7) + ceil(float(sdo7_nrd_nis)/7)
		parts_dict["FC-TDOL-0724U"] = {'Quantity' : FC_TDOL_0724U_Quantity, 'Description': 'SM RIO DO FTA, loop mon, 2A, 24VDc, 7ch / TDOL'}
	return parts_dict

def get_rg_parts(Product, attr, attrs, parts_dict, total_rio_cabinet_summary):
	#CXCPQ-31207
	qty = ceil((get_int(attr.sdo7_line_mon_uio_rd_is)+get_int(attr.sdo7_line_mon_uio_rd_nis))/7.0) + ceil((get_int(attr.sdo7_line_mon_uio_nrd_is)+get_int(attr.sdo7_line_mon_uio_nrd_nis))/7.0)
	if attr.enclosure_type == "Cabinet" and qty:
		parts_dict["FC-TDOL-0724U"] = {'Quantity' : qty, 'Description': 'SM RIO DO FTA, loop mon, 2A, 24VDc, 7ch'}

	if attr.enclosure_type == "Cabinet" and attr.saftey_io_switch == "Third Party MOXA":
		part_map = {
			"MOXA: EDS-316-MM-SC-HPS" : "4600112",
			"MOXA: EDS-316-SS-SC-HPS_C" : "4600136",
			"MOXA: EDS-316-SS-SC-HPS" : "4600130",
			"MOXA: EDS-316-MM-SC-HPS_C" : "4600121"
		}
		part = "MOXA: EDS-316-{}-SC-HPS{}"
		k1, k2 = "MM", ""
		if attr.distance_to_module != "<4KM":
			k1 = "SS"
		if attr.extended_temp != "No" or attr.conformally_coated != "No":
			k2 = "_C"
		part = part.format(k1,k2)
		qty = GS_SMPartsCalc.getNoOfEDS316Switches(
			Product,
			parts_dict.get('FC-TUIO11', {'Quantity' : 0})['Quantity'],
			parts_dict.get('FC-TDIO11', {'Quantity' : 0})['Quantity'],
			parts_dict.get('FC-IOTA-NR24', {'Quantity' : 0})['Quantity'],
			parts_dict.get('FC-IOTA-R24', {'Quantity' : 0})['Quantity']
		)
		if qty:
			parts_dict[part_map[part]] = {'Quantity' : qty, 'Description': part}

	if attr.enclosure_type == "Cabinet" and attr.cabinet_feeder == "Externally_Sourced_24VDC":
		qty = GS_Power_Supply_calcs.getNoPowerSupply(Product)
		Trace.Write(str(qty))
		if get_float(qty):
			parts_dict["FS-PDC-MB24-4P"] = {'Quantity' : 2 * get_float(qty) , 'Description': 'POWER DISTR.CABLE MB-0001 TO QUINT4 PSU'}

	if parts_dict.get("FC-GPCS-RIO16-PF"):
		gcps = ceil(parts_dict.get("FC-GPCS-RIO16-PF")["Quantity"] / 3.0)
		parts_dict["4603323"] = {'Quantity' : gcps, 'Description': 'MOB3 MOUNTING CHASSIS IS - 34 INCH'}

	if attr.enclosure_type == "Cabinet" and attrs.marshalling_option == "Universal Marshalling":
		qty = (
			get_di_do_barrier_sil2_pdio_nrd(attrs)
			+ get_di_do_barrier_sil2_pdio_rd(attrs)
			+ get_di_do_barrier_sil2_uio_nrd(attrs)
			+ get_di_do_barrier_sil2_uio_rd(attrs)
		)
		if qty:
			parts_dict["FC-UGDA01"] = {'Quantity' : qty, 'Description': "SCA DIGITAL INPUT/OUTPUT SIL 2 BARRIER"}

		qty = (
			get_ai_barrier_sil2_uio_nrd(attrs)
			+ get_ai_barrier_sil2_uio_rd(attrs)
		)
		if qty:
			parts_dict["FC-UGAI01"] = {'Quantity' : qty, 'Description': "SCA ANALOG INPUT SIL2 BARRIER"}

		qty = try_get_int_attr(attrs, "sao1_uio_nrd_is", 0) + try_get_int_attr(attrs, "sao1_uio_rd_is", 0)
		if qty:
			parts_dict["FC-UGAO01"] = {'Quantity' : qty, 'Description': "SCA ANALOG OUTPUT SIL 2 BARRIER"}

	if attr.Marshalling_Opt_rg == "Hardware_Marshalling_with_P+F":
		#CXCPQ-31201
		if attr.type_uio_ai_rd != '' or attr.type_uio_ai_nrd != '':
			type_ao = int(attr.type_uio_ai_rd) + int(attr.type_uio_ai_nrd)
			if type_ao > 0 or type_ao != '':
				parts_dict["HIC2025"] = {'Quantity' : type_ao, 'Description': 'P+F SMART transm. power supply SIL2 1ch'}
		#CXCPQ-31199
		sil2_di = int(attr.sil2_uio_di_rd) + int(attr.sil2_uio_di_nrd)
		if sil2_di > 0 or sil2_di != '':
			parts_dict["HIC2831R2"] = {'Quantity' : sil2_di, 'Description': 'P+F Isolator switch ampl. SIL2 LFD 1ch'}
			#parts_dict["HIC2025"] = {'Quantity' : sil2_do, 'Description': 'P+F SMART transm. power supply SIL2 1ch'}
		#CXCPQ-31203
		if attr.sil3_uio_do_rd != '' or attr.sil3_uio_do_nrd != '':
			sil3_do = int(attr.sil3_uio_do_rd) + int(attr.sil3_uio_do_nrd)
			if sil3_do > 0 or sil3_do != '':
				parts_dict["HIC2871"] = {'Quantity' : sil3_do, 'Description': 'P+F Solenoid driver SIL3 1ch'}
		#CXCPQ-31202
		if attr.type_uio_ao_rd != '' or attr.type_uio_ao_nrd != '':
			type_ao = int(attr.type_uio_ao_rd) + int(attr.type_uio_ao_nrd)
			if type_ao > 0 or type_ao != '':
				parts_dict["HIC2031"] = {'Quantity' : type_ao, 'Description': 'P+F SMART repeater SIL2 1ch'}
		#CXCPQ-31200
		if attr.sil3_uio_di_rd != '' or attr.sil3_uio_di_nrd != '':
			sil3_di =int(attr.sil3_uio_di_rd) + int(attr.sil3_uio_di_nrd)
			if sil3_di > 0 or sil3_di != '':
				parts_dict["HIC2853R2"] = {'Quantity' : sil3_di, 'Description': 'P+F Isolator switch amplifier SIL3 1ch'}
	#CXCPQ-31794
	if attr.Marshalling_Opt_rg == 'Hardware_Marshalling_with_Other':
		sdo7_rd_nis = attr.sdo7_line_mon_uio_rd_nis if attr.sdo7_line_mon_uio_rd_nis else 0
		sdo7_nrd_nis = attr.sdo7_line_mon_uio_nrd_nis if attr.sdo7_line_mon_uio_nrd_nis else 0
		FC_TDOL_0724U_Quantity = ceil(float(sdo7_rd_nis)/7) + ceil(float(sdo7_nrd_nis)/7)
		parts_dict["FC-TDOL-0724U"] = {'Quantity' : FC_TDOL_0724U_Quantity, 'Description': 'SM RIO DO FTA, loop mon, 2A, 24VDc, 7ch / TDOL'}
	return parts_dict

#CXCPQ-31193
def get_parts(Product,total_rio_cabinet_summary,parts_dict):
	Cabinet_feeder_volt = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Cabinet_Feeder_Voltage').DisplayValue
	Power_supply = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Power_Supply').DisplayValue
	Load_SM_RIO_cabinet_summary = get_int(total_rio_cabinet_summary)
	Trace.Write(Load_SM_RIO_cabinet_summary)
	Trace.Write(Cabinet_feeder_volt)
	Trace.Write(Power_supply)

	if Cabinet_feeder_volt == "Externally Sourced 24VDC":
		power_calculation_VA = (Load_SM_RIO_cabinet_summary)*24
		Trace.Write(power_calculation_VA)
		Total_load_VA = D.Ceiling(get_float(power_calculation_VA)/0.947)
		Trace.Write("Total Load: "+str(Total_load_VA))

		if Power_supply == "Redundant":
			Quitn_sc1 = D.Ceiling(2 * (Total_load_VA) / (24*24))
			Trace.Write(Quitn_sc1)
			parts_dict["50165610-001"] = {'Quantity' : int(Quitn_sc1), 'Description': 'QUINT4-PS/24DC/24DC/20/SC/+ (SAP Material number 50165610-001)'}
			#CCEECOMMBR-6976
			#parts_dict["5SY4220-7"] = {'Quantity' : int(Quitn_sc1), 'Description': 'Main Circuit breakers'}
			parts_dict["51454944-100"] = {'Quantity' : int(Quitn_sc1), 'Description': 'QUINT4-S-ORING/12-24DC/1X40/+ (SAP Material number 51454944-100)'}
			Qtyt1=(parts_dict["50165610-001"]["Quantity"])+(parts_dict["51454944-100"]["Quantity"])
			parts_dict["FS-PDC-MB24-4P"]={'Quantity' : Qtyt1 , 'Description': 'POWER DISTR.CABLE MB-0001 TO QUINT4 PSU'}
		elif Power_supply == "Non Redundant":
			Quitn_sc2 = D.Ceiling((Total_load_VA) / (24*24))
			Trace.Write(Quitn_sc2)
			parts_dict["50165610-001"] = {'Quantity' : int(Quitn_sc2), 'Description': 'QUINT4-PS/24DC/24DC/20/SC/+ (SAP Material number 50165610-001)'}
			#CCEECOMMBR-6976
			#parts_dict["5SY4220-7"] = {'Quantity' : int(Quitn_sc2), 'Description': 'Main Circuit breakers'}
			parts_dict["51454944-100"] = {'Quantity' : int(Quitn_sc2), 'Description': 'QUINT4-S-ORING/12-24DC/1X40/+ (SAP Material number 51454944-100)'}
			Qtyt1=(parts_dict["50165610-001"]["Quantity"])+(parts_dict["51454944-100"]["Quantity"])
			parts_dict["FS-PDC-MB24-4P"]={'Quantity' : Qtyt1 , 'Description': 'POWER DISTR.CABLE MB-0001 TO QUINT4 PSU'}
	return parts_dict

def get_total_parts(Product,total_rio_cabinet_summary,parts_dict):
	Enclosure_type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
	Cabinet_feeder_volt = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Cabinet_Feeder_Voltage').DisplayValue
	Power_supply = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0].GetColumnByName('Power_Supply').DisplayValue
	Load_SM_RIO_cabinet_summary = get_int(total_rio_cabinet_summary)
	Trace.Write(Load_SM_RIO_cabinet_summary)
	Trace.Write(Cabinet_feeder_volt)
	Trace.Write(Power_supply)
	if Enclosure_type == "Cabinet":
		if Cabinet_feeder_volt == "Externally Sourced 24VDC":
			power_calculation_VA = (Load_SM_RIO_cabinet_summary)*24
			Trace.Write(power_calculation_VA)
			Total_load_VA = D.Ceiling(get_float(power_calculation_VA)/0.947)
			Trace.Write("Total Load: "+str(Total_load_VA))
			if Power_supply == "Redundant":
				Quitn_sc1 = D.Ceiling(2 * (Total_load_VA) / (24*24))
				Trace.Write(Quitn_sc1)

				#CCEECOMMBR-6976
				#parts_dict["5SY4220-7"] = {'Quantity' : int(Quitn_sc1), 'Description': 'Main Circuit breakers'}
				parts_dict["51454944-100"] = {'Quantity' : int(Quitn_sc1), 'Description': 'QUINT4-S-ORING/12-24DC/1X40/+ (SAP Material number 51454944-100)'}
				parts_dict["50165610-001"] = {'Quantity' : int(Quitn_sc1), 'Description': 'QUINT4-PS/24DC/24DC/20/SC/+ (SAP Material number 50165610-001)'}
				Qtyt1=(parts_dict["50165610-001"]["Quantity"])+(parts_dict["51454944-100"]["Quantity"])
				parts_dict["FS-PDC-MB24-4P"]={'Quantity' : Qtyt1 , 'Description': 'POWER DISTR.CABLE MB-0001 TO QUINT4 PSU'}
			elif Power_supply == "Non Redundant":
				Quitn_sc2 = D.Ceiling((Total_load_VA) / (24*24))
				Trace.Write(Quitn_sc2)
				parts_dict["50165610-001"] = {'Quantity' : int(Quitn_sc2), 'Description': 'QUINT4-PS/24DC/24DC/20/SC/+ (SAP Material number 50165610-001)'}
				#CCEECOMMBR-6976
				#parts_dict["5SY4220-7"] = {'Quantity' : int(Quitn_sc2), 'Description': 'Main Circuit breakers'}
				parts_dict["51454944-100"] = {'Quantity' : int(Quitn_sc2), 'Description': 'QUINT4-S-ORING/12-24DC/1X40/+ (SAP Material number 51454944-100)'}
				Qtyt1=(parts_dict["50165610-001"]["Quantity"])+(parts_dict["51454944-100"]["Quantity"])
				parts_dict["FS-PDC-MB24-4P"]={'Quantity' : Qtyt1 , 'Description': 'POWER DISTR.CABLE MB-0001 TO QUINT4 PSU'}
	return parts_dict
#CXCPQ-31853
def get_parts1(Product,parts_dict):
	if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
		iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA")
		Trace.Write("Product = "+str(Product.Name))
		marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option")
		digout = Product.GetContainerByName("SM_IO_Count_Digital_Output_Cont")
		for row in digout.Rows:
			if row["Digital Output Type"] == "SDO(7) 24Vdc Line Mon UIO (0-5000)":
				var1 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
				var2 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0
		if iota.Value == "RUSIO" and marshaling.Value == "Hardware_Marshalling_with_Other":
			var = (D.Ceiling(float(var1)/7)) + (D.Ceiling(float(var2)/7))
			parts_dict["FC-TDOL-0724U"] = {"Quantity" : int(var), "Description" : "SM RIO DO FTA, loop mon, 2A, 24VDc, 7ch"}
		return parts_dict
	if Product.Name == "SM Remote Group":
		iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
		Trace.Write("Product = "+str(Product.Name))
		marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option")
		digout = Product.GetContainerByName("SM_RG_IO_Count_Digital_Output_Cont")
		for row in digout.Rows:
			if row["Digital_Output_Type"] == "SDO(7) 24Vdc Line Mon UIO  (0-5000)":
				var1 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
				var2 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
				Trace.Write(var1)
				Trace.Write(var2)
		if iota == "RUSIO" and marshaling.Value == "Hardware_Marshalling_with_Other":
			var = (D.Ceiling(float(var1)/7)) + (D.Ceiling(float(var2)/7))
			parts_dict["FC-TDOL-0724U"] = {"Quantity" : int(var), "Description" : "SM RIO DO FTA, loop mon, 2A, 24VDc, 7ch"}
		return parts_dict

#CXCPQ-31854
def get_parts2(Product,parts_dict):
	if Product.Name in ["SM Control Group", "R2Q SM Control Group"]:
		iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA")
		marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option")
		digout = Product.GetContainerByName("SM_IO_Count_Digital_Output_Cont")
		for row in digout.Rows:
			if row["Digital Output Type"] == "SDO(16) SIL 2/3 250Vac/Vdc UIO (0-5000)":
				var1 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
				var2 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0

		if iota.Value == "RUSIO" and marshaling.Value == "Hardware_Marshalling_with_Other":
			var = 2 * (D.Ceiling(float(var1)/16)) + 2 * (D.Ceiling(float(var2)/16))
			parts_dict["FC-TSRO-0824"] = {"Quantity" : int(var), "Description" : "DO(RELAY) FTA FOR SIL3 APPL. 8CH CC"}
		return parts_dict
	if Product.Name=="SM Remote Group":
		iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
		marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option")
		digout = Product.GetContainerByName("SM_RG_IO_Count_Digital_Output_Cont")
		for row in digout.Rows:
			if row["Digital_Output_Type"] == "SDO(16) SIL 2/3 250Vac/Vdc UIO   (0-5000)":
				var1 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
				var2 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
		if iota == "RUSIO" and marshaling.Value == "Hardware_Marshalling_with_Other":
			var = 2 * (D.Ceiling(float(var1)/16)) + 2 * (D.Ceiling(float(var2)/16))
			parts_dict["FC-TSRO-0824"] = {"Quantity" : int(var), "Description" : "DO(RELAY) FTA FOR SIL3 APPL. 8CH CC"}
		return parts_dict
#CXCPQ-31812
def get_FC_TDIO52(attrs,parts_dict,SUMMARCHDIO):
	if attrs.universal_iota=="PUIO" and attrs.marshalling_option=="Hardware Marshalling with Other":
		Qty=ceil(SUMMARCHDIO/16)
		parts_dict["FC-TDIO52"]={'Quantity':Qty,'Description':'SC SAFETY FTA KNIFE, EOL, 24VDC, 16CH, R / TDIO52'}
	return parts_dict
#CXCPQ-31793
def get_FC_TUIO52(attrs,SUMMARSHUIO,parts_dict):
	if attrs.universal_iota == "RUSIO" or attrs.marshalling_option != "Hardware Marshalling with Other":
		return parts_dict
	if attrs.universal_iota == "PUIO" or attrs.marshalling_option == "Hardware Marshalling with Other":
		Quantity=ceil(SUMMARSHUIO/16)
		if Quantity>0:
			parts_dict["FC-TUIO52"]={'Quantity':Quantity,'Description':'SC FTA FC-PUIO01 KNIFE,EOL,24VDC,16CH,R / TUIO52'}
	return parts_dict
#CXCPQ-33265
def get_partsiota(parts_dict,IOTAR,IOTANR,FC_TUIO11,FC_TDIO11):
	Quant=IOTAR+IOTANR+FC_TUIO11+FC_TDIO11
	if Quant>0 and Quant<=10:
		parts_dict["51153818-201"]={'Quantity':1 ,"Description":'IOL1 GRAY JUMPERS 1-10 & RED JUMPER E'}
	if Quant>=11 and Quant<=20:
		parts_dict["51153818-201"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 1-10 & RED JUMPER E'}
		parts_dict["51153818-202"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 11-20 & RED JUMPER E'}
	if Quant>=21 and Quant<=30:
		parts_dict["51153818-201"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 1-10 & RED JUMPER E'}
		parts_dict["51153818-202"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 11-20 & RED JUMPER E'}
		parts_dict["51153818-203"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 21-30 & RED JUMPER E'}
	if Quant>=31 and Quant<=40:
		parts_dict["51153818-201"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 1-10 & RED JUMPER E'}
		parts_dict["51153818-202"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 11-20 & RED JUMPER E'}
		parts_dict["51153818-203"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 21-30 & RED JUMPER E'}
		parts_dict["51153818-204"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 31-40 & RED JUMPER E'}
	if Quant>=41 and Quant<=50:
		parts_dict["51153818-201"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 1-10 & RED JUMPER E'}
		parts_dict["51153818-202"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 11-20 & RED JUMPER E'}
		parts_dict["51153818-203"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 21-30 & RED JUMPER E'}
		parts_dict["51153818-204"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 31-40 & RED JUMPER E'}
		parts_dict["51153818-205"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 41-50 & RED JUMPER E'}
	if Quant>=51 and Quant<=60:
		parts_dict["51153818-201"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 1-10 & RED JUMPER E'}
		parts_dict["51153818-202"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 11-20 & RED JUMPER E'}
		parts_dict["51153818-203"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 21-30 & RED JUMPER E'}
		parts_dict["51153818-204"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 31-40 & RED JUMPER E'}
		parts_dict["51153818-205"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 41-50 & RED JUMPER E'}
		parts_dict["51153818-206"]={'Quantity':1,"Description":'IOL1 GRAY JUMPERS 51-60 & RED JUMPER E'}
	return parts_dict
def get_TCNT11(parts_dict,TCNT12):
	Quantity=TCNT12*2
	Trace.Write("Quantity "+str(Quantity))
	parts_dict["FC-SCNT02"]={'Quantity':Quantity,'Description':'SC S300 SAFETY CONTROLLER SIL3'}
	return parts_dict

def getPartQty(parts_dict, part):
	part_data = parts_dict.get(part)
	if part_data:
		return part_data["Quantity"]
	return 0

def getPartsQty(parts_dict, parts):
	res = 0
	for part in parts:
		res += getPartQty(parts_dict, part)
	return res

def calculate_loads(parts_dict):
	res = dict()
	res["FAN_LOAD"] = getPartQty(parts_dict, "FC-FANWR-24R") * 400
	res["CNM_SWITCH_LOAD"] = (getPartsQty(parts_dict, ["CC-INWM01", "CC-INWE01"]))*450 + (getPartsQty(parts_dict, ["CC-TNWD01", "CC-TNWC01"]))*900
	res["GIIS_INTEGRATION_BOARD_LOAD"] = (
		getPartQty(parts_dict, "FC-GPCS-RIO16-PF") * 21
		+ getPartQty(parts_dict, "HIC2831R2") * 46
		+ getPartQty(parts_dict, "HIC2853R2") * 30
		+ getPartQty(parts_dict, "HIC2025") * 46
		+ getPartQty(parts_dict, "HIC2031") * 30
		+ getPartQty(parts_dict, "HIC2871") * 42
	)
	res["TELD_LOAD"] = getPartQty(parts_dict, "FC-TELD-0001") * 10
	res["MOXA_LOAD"] = (
		getPartQty(parts_dict, "4600116") * 1120
		+ getPartQty(parts_dict, "4600131") * 160
		+ getPartQty(parts_dict, "4600117") * 160
		+ getPartQty(parts_dict, "4600132") * 170
		+ getPartQty(parts_dict, "4600118") * 170
		+ getPartQty(parts_dict, "4600133") * 250
		+ getPartsQty(parts_dict, ["4600112", "4600136", "4600130", "4600121"])*440
		+ getPartsQty(parts_dict, ["4600122", "4600113"])*160
		+ getPartsQty(parts_dict, ["4600114", "4600123"])*250
	)
	return res

def addParts(attrs, parts_dict,Tot_qty_FC_USCH01,cable_qty_L3):
	if attrs.marshalling_option != "Universal Marshalling":
		return parts_dict
	indermediatCalcDict = GS_Power_Supply_calcs.getIntermediateCalcDict(attrs)
	Trace.Write(str(indermediatCalcDict))

	#CXCPQ-33117
	Total_SCA_NIS = sum(indermediatCalcDict[key] for key in ["a", "b", "c", "d", "e", "f", "g", "h"])
	#CXCPQ-33118
	Total_SCA_IS = sum(indermediatCalcDict[key] for key in ["i", "j", "k", "l"])
	parts_dict["FC-USCA01"] = {'Quantity' : int(Total_SCA_NIS), 'Description': 'INTEGRATED FTA-HIGH CURRENT'}

	if 'FC-USCH01' in parts_dict.keys():
		qty_FC_USCH01 = int(parts_dict['FC-USCH01']['Quantity']) if parts_dict['FC-USCH01']['Quantity'] else 0
	else:
		qty_FC_USCH01 = 0

	if attrs.cabinet_access == "Dual Access" and attrs.cabinet_layout == "3 Column" and attrs.cabinet_power == "120/230 VAC" and attrs.mounting_option == "Bracket Mounting":
		#CXCPQ-33121
		parts_dict["MCD-PS-3I-672"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/42.0)),"Description":'Marsh Cab Dual Side 672 IO'}
		parts_dict["MCD-PS-3I-672IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/42.0)),"Description":'Marsh Cab Dual Side 672 GIIS IO'}
		parts_dict["MCD-PS-3I-576H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/36.0)),"Description":'MARSH CAB DUAL SIDE 576 IO'}
	if attrs.cabinet_access == "Dual Access" and attrs.cabinet_layout == "3 Column" and attrs.cabinet_power == "ExternallySource 24VDC" and attrs.mounting_option == "Bracket Mounting":
		#CXCPQ-33122
		parts_dict["MCD-ES-3I-720"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/45.0)),"Description":'Marsh Cab Dual Side 720 IO'}
		parts_dict["MCD-ES-3I-720IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/45.0)),"Description":'Marsh Cab Dual Side 720 GIIS IO'}
		parts_dict["MCD-ES-3I-624H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/39.0)),"Description":'MARSH CAB DUAL SIDE 624 IO'}
	if attrs.cabinet_access == "Dual Access" and attrs.cabinet_layout == "2 Column" and attrs.cabinet_power == "120/230 VAC" and attrs.mounting_option == "Plate Mounting":
		#CXCPQ-33123
		parts_dict["MCD-PS-2P-488"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/28.0)),"Description":'Marsh Cab Dual Side 488 IO'}
		parts_dict["MCD-PS-2P-488IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/28.0)),"Description":'Marsh Cab Dual Side 488 GIIS IO'}
		parts_dict["MCD-PS-2P-384H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/24.0)),"Description":'MARSH CAB DUAL SIDE 384 IO'}
	if attrs.cabinet_access == "Dual Access" and attrs.cabinet_layout == "2 Column" and attrs.cabinet_power == "120/230 VAC" and attrs.mounting_option == "Bracket Mounting":
		#CXCPQ-33124
		parts_dict["MCD-PS-2I-488"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/28.0)),"Description":'Marsh Cab Dual Side 488 IO'}
		parts_dict["MCD-PS-2I-488IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/28.0)),"Description":'Marsh Cab Dual Side 488 GIIS IO'}
		parts_dict["MCD-PS-2I-384H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/24.0)),"Description":'MARSH CAB DUAL SIDE 384 IO'}
	if attrs.cabinet_access == "Dual Access" and attrs.cabinet_layout == "2 Column" and attrs.cabinet_power == "ExternallySource 24VDC" and attrs.mounting_option == "Plate Mounting":
		#CXCPQ-33125
		parts_dict["MCD-ES-2P-488"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/30.0)),"Description":'Marsh Cab Dual Side 488 IO'}
		parts_dict["MCD-ES-2P-488IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/30.0)),"Description":'Marsh Cab Dual Side 488 GIIS IO'}
		parts_dict["MCD-ES-2P-416H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/26.0)),"Description":'MARSH CAB DUAL SIDE 416 IO'}
	if attrs.cabinet_access == "Dual Access" and attrs.cabinet_layout == "2 Column" and attrs.cabinet_power == "ExternallySource 24VDC" and attrs.mounting_option == "Bracket Mounting":
		#CXCPQ-33129
		parts_dict["MCD-ES-2I-480"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/30.0)),"Description":'Marsh Cab Dual Side 480 IO'}
		parts_dict["MCD-ES-2I-480IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/30.0)),"Description":'Marsh Cab Dual Side 480 GIIS IO'}
		parts_dict["MCD-ES-2I-416H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/26.0)),"Description":'MARSH CAB DUAL SIDE 416 IO'}
	if attrs.cabinet_access == "Single Access" and attrs.cabinet_layout == "3 Column" and attrs.cabinet_power == "120/230 VAC" and attrs.mounting_option == "Bracket Mounting":
		#CXCPQ-33130
		parts_dict["MCS-PS-3I-288"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/18.0)),"Description":'Marsh Cab Dual Side 288 IO'}
		parts_dict["MCS-PS-3I-288IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/18.0)),"Description":'Marsh Cab Dual Side 288 GIIS IO'}
		#CXDEV-8766
		parts_dict["MCS-PS-3I-240H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/15.0)),"Description":'MARSH CAB SINGLE SIDE 240 IO'}
	if attrs.cabinet_access == "Single Access" and attrs.cabinet_layout == "3 Column" and attrs.cabinet_power == "ExternallySource 24VDC" and attrs.mounting_option == "Bracket Mounting":
		#CXCPQ-33134
		parts_dict["MCS-ES-3I-336"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/21.0)),"Description":'Marsh Cab Dual Side 336 IO'}
		parts_dict["MCS-ES-3I-336IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/21.0)),"Description":'Marsh Cab Dual Side 336 GIIS IO'}
		#CXDEV-8769
		parts_dict["MCS-ES-3I-288H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/18.0)),"Description":'MARSH CAB SINGLE SIDE 288 IO'}
	if attrs.cabinet_access == "Single Access" and attrs.cabinet_layout == "2 Column" and attrs.cabinet_power == "120/230 VAC" and attrs.mounting_option == "Plate Mounting":
		#CXCPQ-33135
		parts_dict["MCS-PS-2P-192"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/12.0)),"Description":'Marsh Cab Dual Side 192 IO'}
		parts_dict["MCS-PS-2P-192IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/12.0)),"Description":'Marsh Cab Dual Side 192 GIIS IO'}
		parts_dict["MCS-PS-2P-160H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/10.0)),"Description":'MARSH CAB SINGLE SIDE 160 IO'}
	if attrs.cabinet_access == "Single Access" and attrs.cabinet_layout == "2 Column" and attrs.cabinet_power == "120/230 VAC" and attrs.mounting_option == "Bracket Mounting":
		#CXCPQ-33136
		parts_dict["MCS-PS-2I-192"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/12.0)),"Description":'Marsh Cab Dual Side 192 IO'}
		parts_dict["MCS-PS-2I-192IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/12.0)),"Description":'Marsh Cab Dual Side 192 GIIS IO'}
		parts_dict["MCS-PS-2I-160H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/10.0)),"Description":'MARSH CAB SINGLE SIDE 160 IO'}
	if attrs.cabinet_access == "Single Access" and attrs.cabinet_layout == "2 Column" and attrs.cabinet_power == "ExternallySource 24VDC" and attrs.mounting_option == "Plate Mounting":
		#CXCPQ-33137
		parts_dict["MCS-ES-2P-224"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/14.0)),"Description":'Marsh Cab Dual Side 224 IO'}
		parts_dict["MCS-ES-2P-224IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/14.0)),"Description":'Marsh Cab Dual Side 224 GIIS IO'}
		#CXDEV-8767
		parts_dict["MCS-ES-2P-192H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/12.0)),"Description":'MARSH CAB SINGLE SIDE 192 IO'}
	if attrs.cabinet_access == "Single Access" and attrs.cabinet_layout == "2 Column" and attrs.cabinet_power == "ExternallySource 24VDC" and attrs.mounting_option == "Bracket Mounting":
		#CXCPQ-33143
		parts_dict["MCS-ES-2I-224"]={'Quantity':int(D.Ceiling(Total_SCA_NIS/14.0)),"Description":'Marsh Cab Dual Side 224 IO'}
		parts_dict["MCS-ES-2I-224IS"]={'Quantity':int(D.Ceiling(Total_SCA_IS/14.0)),"Description":'Marsh Cab Dual Side 224 GIIS IO'}
		#CXDEV-8768
		parts_dict["MCS-ES-2I-192H"]={'Quantity':int(D.Ceiling(qty_FC_USCH01/12.0)),"Description":'MARSH CAB SINGLE SIDE 192 IO'}

	cable_qty = sum(indermediatCalcDict[key] for key in ["c", "d", "g", "h", "k", "l"])
	cable_pin_qty = sum(indermediatCalcDict[key] for key in ["a", "b", "e", "f", "i", "j"])
	Trace.Write("cable_qty="+str(cable_qty)+"	"+str(cable_pin_qty))
	Trace.Write("indermediatCalcDict="+str(indermediatCalcDict))
	cable_sic_qty = cable_qty+Tot_qty_FC_USCH01
	Trace.Write("Tot_qty_FC_USCH01="+str(Tot_qty_FC_USCH01))
	Trace.Write("cable_sic_qty="+str(cable_sic_qty))
	cable_qty_L3=0
	if attrs.sic_cable_length and cable_pin_qty>0:
		if 'FC-USCH01' in parts_dict.keys():
			cable_qty_L3 = int(cable_qty_L3) if parts_dict['FC-USCH01']['Quantity'] else 0
		if 'CC-USCA01' in parts_dict.keys():
			cable_qty_L3 += int(parts_dict['CC-USCA01']['Quantity']) if parts_dict['CC-USCA01']['Quantity'] else 0
		if 'FC-USCA01' in parts_dict.keys():
			cable_qty_L3 += int(parts_dict['FC-USCA01']['Quantity']) if parts_dict['FC-USCA01']['Quantity'] else 0
		if 'CC-UGIA01' in parts_dict.keys():
			cable_qty_L3 += int(parts_dict['CC-UGIA01']['Quantity']) if parts_dict['CC-UGIA01']['Quantity'] else 0
	Trace.Write("-^^^^cable_qty_L3^^^-"+str(cable_qty_L3)+"	"+str(int(cable_qty)>0.0))
	if int(cable_qty)>0 and cable_qty_L3 > 0:
		cable_qty_L3 = cable_qty - cable_qty_L3
		Trace.Write("Inside if"+str(cable_qty_L3))
	Trace.Write("cable_qty_L3--->"+str(cable_qty_L3)+"	"+str(cable_qty))
	if attrs.sic_cable_length == "0.8M":
		parts_dict["FC-SIC5008"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L0.8M"}
		parts_dict["FS-SICC-1011/L3"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 3 M"}
	if attrs.sic_cable_length == "1M":
		parts_dict["FC-SIC5010"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L1M"}
		parts_dict["FS-SICC-1011/L3"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 3 M"}
	if attrs.sic_cable_length == "2M":
		parts_dict["FC-SIC5020"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L2M"}
		parts_dict["FS-SICC-1011/L3"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 3 M"}
	if attrs.sic_cable_length == "3M":
		parts_dict["FC-SIC5030"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L3M"}
		parts_dict["FS-SICC-1011/L3"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 3 M"}
	if attrs.sic_cable_length == "4M":
		parts_dict["FC-SIC5040"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L4M"}
		parts_dict["FS-SICC-1011/L4"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 4 M"}
	if attrs.sic_cable_length == "5M":
		parts_dict["FC-SIC5050"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L5M"}
		parts_dict["FS-SICC-1011/L5"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 5 M"}
	if attrs.sic_cable_length == "6M":
		parts_dict["FC-SIC5060"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L6M"}
		parts_dict["FS-SICC-1011/L6"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 6 M"}
	if attrs.sic_cable_length == "10M":
		parts_dict["FC-SIC5100"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L10M"}
		parts_dict["FS-SICC-1011/L10"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 10 M"}
	if attrs.sic_cable_length == "15M":
		parts_dict["FC-SIC5150"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L15M"}
		parts_dict["FS-SICC-1011/L15"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 15 M"}
	if attrs.sic_cable_length == "20M":
		parts_dict["FC-SIC5200"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L20M"}
		parts_dict["FS-SICC-1011/L20"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 20 M"}
	if attrs.sic_cable_length == "25M":
		parts_dict["FC-SIC5250"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L25M"}
		parts_dict["FS-SICC-1011/L25"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 25 M"}
	if attrs.sic_cable_length == "30M":
		parts_dict["FC-SIC5300"] = {"Quantity" : cable_sic_qty, "Description" : "SC SIC CABLE SCA L30M"}
		parts_dict["FS-SICC-1011/L30"] = {"Quantity" : cable_pin_qty, "Description" : "RUSIO SIC CABLE TO FEMALE SUB-D 37PINS 30 M"}
	Trace.Write("parts_dict==>"+str(parts_dict))
	return parts_dict