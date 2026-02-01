import math

def get_int(n):
	try:
		return int(float(n)) if n else 0
	except:
		return 0

#CXCPQ-39151
def Get_RG_IOTA(Product):
	HN = HN2 = 0
	Total_load_iota = int(float(Product.Attr('C300_RG_Total_IO_Load').GetValue())) if Product.Attr('C300_RG_Total_IO_Load').GetValue() != '' or Product.Attr('C300_RG_Total_IO_Load').GetValue() != None else 0
	Trace.Write(Total_load_iota)
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	Fibre_optic = Product.Attr('SerC_RG_CN100/_FOE_Fiber_Type').GetValue()
	CN100_HOVE = Product.Attr('SerC_RG_CN100_I/O_HOVE').GetValue()
	Distance_SeriesC = Product.Attr('SerC_RG_Distance_for_SeriesC_Remote_Group').GetValue()
	io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	A1 = int(Total_load_iota)
	A2=A3= 0

	if io_family != "Turbomachinery" and (IO_Mount != "Cabinet" or Fibre_optic != "Multi Mode" or CN100_HOVE != "None"):
		return 0,0,0,0
	elif io_family == "Turbomachinery" and Fibre_optic != "Multi Mode":
		return 0,0,0,0
	else:
		A2 = math.ceil(A1/40.0) if (A1/40.0) > 0 else 0
		A3 = math.ceil(A1/40.0) if (A1/40.0) > 0 else 0
		if io_family == "Turbomachinery" :
			A2 = math.ceil(A1/6.0) if (A1/6.0) > 0 else 0
			A3 = math.ceil(A1/6.0) if (A1/6.0) > 0 else 0
		if Distance_SeriesC == "1.5 KM":
			HN = 2*A3
			HN2 = 2*A2
		elif Distance_SeriesC == "3.0 KM":
			HN = 2*A3 + 2*A3
			HN2 = 2*A2 + 2*A2
		elif Distance_SeriesC == "4.0 KM":
			HN = 2*A3 + 4*A3
			HN2 = 2*A2 + 4*A2
	return int(HN), int(HN2), int(A2), int(A3)

def Get_CG_IOTA(Product):
	HN = HN2 = 0
	rg_cont = Product.GetContainerByName('Series_C_Remote_Groups_Cont').Rows
	for rgs in rg_cont:
		rg_prod = rgs.Product
		#Trace.Write(rg_prod)
		rg_HN = get_int(rg_prod.Attr('RG_HN').GetValue())
		rg_HN2 = get_int(rg_prod.Attr('RG_HN2').GetValue())
		#Adding value to CG
		HN += 2 * rg_HN
		HN2 += 2 * rg_HN2
	return int(HN), int(HN2)


def getPmioCgIota(Product):
	iOFamilyType = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	typeOfControllerRequired = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
	pMIOSolutionRequired = Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()

	if iOFamilyType != "Series C" or (typeOfControllerRequired != "C300 CEE" or typeOfControllerRequired == "") or pMIOSolutionRequired != "Yes":
		return 0, 0, 0, 0, 0

	hn = hn2 = 0
	rg_cont = Product.GetContainerByName('Series_C_Remote_Groups_Cont').Rows
	#totalLoad = 0
	qty1 = qty2 = 0
	case_3_Qty = 0
	for row in rg_cont:
		load = get_int(row.Product.Attr("C300_RG_PMIO_Total_IO_Load").GetValue())
		#totalLoad += load
		load = math.ceil(load/40.0)
		isMultiMode = row.Product.Attr("SerC_RG_Fiber_Optic_IO_Link_Extender_Type_for_PMIO").GetValue() == "Multi Mode"
		distance = row.Product.Attr("SerC_RG_Distance_for_PM_Remote_Group").GetValue()
		case_3_Qty = case_3_Qty + get_int(row.Product.Attr('Control_Group_FOE_Module_qty_case3').GetValue())

		if not isMultiMode:
			q1 = 4 * load
			qty1 += q1
			qty2 += math.ceil(q1 / 2.0)
			continue

		hn += 2 * load
		if distance == "1.5 KM":
			pass
		elif distance == "3 KM":
			hn += 2
		elif distance == "4.5 KM":
			hn += 4
		elif distance == "6 KM":
			hn += 6
		elif distance == "8 KM":
			hn += 8
		elif distance == "10 KM":
			hn += 10
	hn2 = hn
	return hn, hn2, qty1, qty2, case_3_Qty

#CXCPQ-39152
def Get_HN(Product):
	GR5 = VR5 = 0
	X = math.ceil(get_int(Product.Attr('CG_HN').GetValue())/2.0)
	G = math.ceil(X/2.0)
	V = X-G
	GR5 = G
	VR5 = V
	return int(GR5),int(VR5)

#CXCPQ-39268
def RG_iota(Product):
	Total_load_iota = int(float(Product.Attr('C300_RG_Total_IO_Load').GetValue())) if Product.Attr('C300_RG_Total_IO_Load').GetValue() != '' or Product.Attr('C300_RG_Total_IO_Load').GetValue() != None else 0
	Trace.Write(Total_load_iota)
	IO_Mount = Product.Attr('SerC_IO_Mounting_Solution').GetValue()
	Fibre_optic = Product.Attr('SerC_RG_CN100/_FOE_Fiber_Type').GetValue()
	CN100_HOVE = Product.Attr('SerC_RG_CN100_I/O_HOVE').GetValue()
	single_mode_remote = Product.Attr('SerC_RG_Single_Mod_FOE_Type_for_Remote_Grp_Cabinet').GetValue()
	single_mode_control = Product.Attr('SerC_RG_Single_Mod_FOE_Type_for_Control_Grp_Cabt').GetValue()
	io_family=Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	A1 = int(Total_load_iota)
	A2 = 0
	SDRX_qty = HPSC_qty = qty_100 = 0
	if (IO_Mount != "Cabinet" or Fibre_optic != "Single Mode" or CN100_HOVE != "None") and io_family == "Series C":
		return 0,0,0
	elif io_family == "Turbomachinery" and Fibre_optic != "Single Mode":
		return 0, 0, 0
	else:
		A2 = math.ceil(A1/40.0) if (A1/40.0) > 0 else 0
		if io_family == "Turbomachinery" :
			A2 = math.ceil(A1/6.0) if (A1/6.0) > 0 else 0
		if single_mode_remote == "Separate IOTA":
			SDRX_qty = 2 * A2
			HPSC_qty = 2 * A2
		elif single_mode_remote == "Single IOTA":
			SDRX_qty = A2
			HPSC_qty = 2 * A2
		elif single_mode_remote == "DIN RAIL":
			qty_100 = A2
			HPSC_qty = 2 * A2
	return int(SDRX_qty), int(HPSC_qty), int(qty_100)

def CG_iota(Product):
	SDRX_qty = 0
	HPSC_qty = 0
	qty_100 = 0
	A3 = 0
	case_3_Qty = 0
	rg_cont = Product.GetContainerByName('Series_C_Remote_Groups_Cont').Rows
	for rgs in rg_cont:
		rg_prod = rgs.Product
		#Trace.Write(rg_prod)
		rg_A3 = get_int(rg_prod.Attr('qty_hpsc').GetValue())
		rg_foe_mod_qty = get_int(rg_prod.Attr('Control_Group_FOE_Module_qty').GetValue())
		Trace.Write('rg_foe_mod_qty=='+str(rg_foe_mod_qty))
		case_3_Qty = case_3_Qty + get_int(rg_prod.Attr('Control_Group_FOE_Module_qty_case3').GetValue())
		A3 = A3 + rg_A3 + rg_foe_mod_qty
		Trace.Write('A3=='+str(A3))
		IO_Mounting_Solution = rg_prod.Attr('SerC_IO_Mounting_Solution').GetValue()
		single_mode_control = rg_prod.Attr('C300_RG_UPC_Single_Mode_FOE_Type_CG_Cab').GetValue() if IO_Mounting_Solution == 'Universal Process Cab - 1.3M' else rg_prod.Attr('SerC_RG_Single_Mod_FOE_Type_for_Control_Grp_Cabt').GetValue()
		Trace.Write('single_mode_control=='+str(single_mode_control))
		if single_mode_control == "Separate IOTA":
			SDRX_qty += A3
			HPSC_qty += A3
		elif single_mode_control == "Single IOTA":
			SDRX_qty += math.ceil(A3/2.0)
			HPSC_qty += A3
		elif single_mode_control == "DIN RAIL":
			qty_100 += math.ceil(A3/2.0)
			HPSC_qty += A3
	return int(SDRX_qty), int(HPSC_qty), int(qty_100), int(case_3_Qty)