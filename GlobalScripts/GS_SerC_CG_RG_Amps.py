import math as m
import GS_Get_Set_AtvQty
from GS_PS_Exp_Ent_BOM import setAtvQty
from GS_C300_Calc_Module import getValueSum, getValue, getBayQuantities
def gettotalamps(Product):
	amps=Product.Attributes.GetByName('SerC_CG_Current_required_for_each_DO').GetValue()
	if amps=="":
		amps=0
	amps=int(amps)
	x=0
	def getqtof (partnum):
		if Product.Name=="Series-C Control Group":
			qnt=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_CG_Part_Summary',partnum)
		elif Product.Name=="Series-C Remote Group":
			qnt=GS_Get_Set_AtvQty.getAtvQty(Product,'Series_C_RG_Part_Summary',partnum)
		return int(qnt)

	a1=0.271* getqtof ("CC-SCMB05")
	a2=0.271* getqtof ("51454475-100")
	a3=0.15* getqtof ("CC-PCF901")
	a4=0.479* getqtof ("CC-PAOH01")

	a5=0.095* getqtof ("CC-PDIL01")
	a6=0.19* getqtof ("DC-TDIL01")
	a7=0.19* getqtof ("DC-TDIL11")
	a9=0.05* getqtof ("CC-PDIH01")

	a10=0.8* getqtof ("CC-PDOB01")
	a11=0.147* getqtof ("CC-SDOR01")
	a12=0.212* getqtof ("CC-PFB402")
	a13=0.346* getqtof ("CC-PDIS01")
	a14=0.32*  getqtof ("DC-TAID01")
	a15=0.32*  getqtof ("DC-TAID11")
	a16=0.18*  getqtof ("CC-PAIX02")
	a17=0.18* getqtof ("CC-PAIH02")

	a18=0.18*  getqtof ("DC-TDIL51")
	a19=0.18*  getqtof ("DC-TDIL61")

	a20=0.18* getqtof ("CC-PAIH51")
	a21=0.48* getqtof ("CC-PAOH51")
	a22=0.07*  getqtof ("DC-PDIL51")
	a23=0.075*  getqtof ("DC-PDOD51")
	a24=0.18* getqtof ("CC-PAIN01")
	a25=0.18* getqtof ("CC-PAIL51")
	a26=0.48* getqtof ("CC-PAON01")
	#a27=1.2* getqtof ("CC-PPIX01")
	a28=0.5* getqtof ("DC-TPIX11")
	a29=0.32* getqtof ("CC-PCNT02")
	a30=0.32* getqtof ("CC-PCNT05")
	a31=0.39* getqtof ("CC-IP0101")
	a32=0.38* getqtof ("CC-PFB801")
	a33=0.157*  getqtof ("CC-PEIM01")
	a34=0.085*  getqtof ("DC-PDIS51")
	a35=0.3 * getqtof ("DC-SDRX01")
	a36=0.32 * getqtof("‘DC-TAIX01")
	a37=0.32 * getqtof("DC-TAIX11")

	def getFloat(val):
		if val:
			return float(val)
		return 0.00

	def getAtvQty1(Product,AttrName,sv):
		pvs=Product.Attr(AttrName).Values
		for av in pvs:
			if av.Display == sv:
				return av.Quantity
		return 0


	def getIOCount(Product, AttrName, params):
		resDict = dict()
		for sv in params:
			resDict[sv] = getAtvQty1(Product, AttrName, sv)
		return resDict

	def divideByX(Product, AttrName, paramList, X):
		res = 0
		if X == 0:
			return res
		resDict = getIOCount(Product, AttrName, paramList)
		for key in resDict.keys():
			if resDict[key] > 0:
				res += m.ceil(getFloat(resDict[key]/X))
		return res

	Z51= divideByX(Product, 'SerC_IO_Params', ['G51','G52','G53','G54'], 32.0)
	Z52= divideByX(Product, 'SerC_IO_Params', ['H51','H52','H53','H54'], 32.0)
	Z53= divideByX(Product, 'SerC_IO_Params', ['I51','I52','I53','I54'], 32.0)
	#CXDEV-6771
	param1 = getIOCount(Product, 'SerC_IO_Params', ['Z81','Z82','Z83'])
	param2 = getIOCount(Product, 'SerC_IO_Params', ['Z84','Z85','Z86'])
	a27 = (1.02 * (param1['Z81'] + param1['Z82']+ param1['Z83'])) +(0.68 * (param2['Z84'] +param2['Z85'] + param2['Z86']))
	Var1=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X61_V1')
	Var2=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X61_V2')
	Var3=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X62_V1')
	Var4=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X62_V2')
	Var5=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X63_V1')
	Var6=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X63_V2')
	Var7=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X81_V1')
	Var8=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X81_V2')
	Var9=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X82_V1')
	Var10=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X82_V2')
	Var11=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X83_V1')
	Var12=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X83_V2')
	Var13=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X71_V1')
	Var14=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X71_V2')
	Var15=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X72_V1')
	Var16=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X72_V2')
	Var17=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X73_V1')
	Var18=GS_Get_Set_AtvQty.getAtvQty(Product, 'SerC_IO_Params', 'X73_V2')

	x2= m.ceil ((Var1 +Var2)/1000.0) + m.ceil ((Var3 +Var4)/1000.0) + m.ceil ((Var5 +Var6)/1000.0) + m.ceil ((Var7 +Var8)/1000.0)  + m.ceil ((Var9 +Var10)/1000.0)  + m.ceil ((Var11 +Var12)/1000.0) + m.ceil ((Var13 +Var14)/1000.0)  + m.ceil ((Var15 +Var16)/1000.0) + m.ceil ((Var17 +Var18)/1000.0) 

	zsum=(Z51* m.ceil (amps/1000.0)) + (Z52* m.ceil (amps/1000.0)) + (Z53*m.ceil (amps/1000.0))

	totalamps=a1+a2+a3+a4+a5+a6+a7+a9+a10+a11+a12+a13+a14+a15+a16+a17+a18+a19+a20+a21+a22+a23+a24+a25+a26+a27+a28+a29+a30+a31+a32+a33+a34+a35+a36+a37+x2+zsum
	totalamps=m.ceil(totalamps)
	Trace.Write(totalamps)
	listone=[a1,a2,a3,a4,a5,a6,a7,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24,a25,a26,a27,a28,a29,a30,a31,a32,a33,a34,a35,a36,a37,x2,zsum]
	X=0
	for i in listone:
		Trace.Write("Value at "+ str(X)+ " is " + str(i))
		X=X+1
	return totalamps
#ab=gettotalamps(Product)
#Trace.Write("amps are " + str(ab))

#Generic Cabinet - #CXCPQ-119726 - #CXCPQ-119727 - Start
def generic_type_markII(Product):
	if Product.Name not in ("Series-C Remote Group", "Series-C Control Group"):
		return
	isMarkII = Product.Attr("SerC_CG_IO_Family_Type").GetValue() == "Series-C Mark II"
	if not isMarkII:
		return
	
	crateType = Product.Attr("Crate Type").GetValue()
	crateDesign = Product.Attr("Crate Design").GetValue()
	if Product.Name == "Series-C Control Group":
		partSummaryAttr = "Series_C_CG_Part_Summary"
		isSingleAccess = Product.Attr("SerC_CG_Cabinet_Access").GetValue() == "Single Access"
		cabinetColorDefault = Product.Attr("SerC_CG_Cabinet_Color_Default").GetValue()
		cabinetDoorDefault = Product.Attr("SerC_CG_Cabinet_Doors_Default").GetValue()
		cabinetDoorKeylock = Product.Attr("SerC_CG_Cabinet_Door_Keylock _Default").GetValue()
		cabinetBase = Product.Attr("SerC_CG_Cabinet_Base_(Plinth)").GetValue()
		cab_size = Product.Attr("SerC_CG_Cabinet_Base_Size").GetValue()
		cab_typ=Product.Attr('SerC_CG_Cabinet_Type_03').GetValue()
		complexing = Product.Attr("SerC_CG_Complexing").GetValue()
	else:
		partSummaryAttr = 'Series_C_RG_Part_Summary'
		isSingleAccess = Product.Attr("SerC_RG_Cabinet_Access").GetValue() == "Single Access"
		cabinetColorDefault = Product.Attr("SerC_RG_Cabinet_Color_Default").GetValue()
		cabinetDoorDefault = Product.Attr("SerC_RG_Cabinet_Doors_Default").GetValue()
		cabinetDoorKeylock = Product.Attr("SerC_RG_Cabinet_Door_Keylock_Default").GetValue()
		cabinetBase = Product.Attr("SerC_RG_Cabinet_Base_(Plinth)").GetValue()
		cab_size = Product.Attr("SerC_RG_Cabinet_Base_Size").GetValue()
		cab_typ=Product.Attr('SerC_RG_Cabinet_Type').GetValue()
		complexing = Product.Attr("SerC_RG_Complexing").GetValue()
	partQtyMap = GS_Get_Set_AtvQty.getAllAtvQty(Product, partSummaryAttr)

	qty_CC_CASS02, qty_CC_CASS12,qty_CC_CADS02,qty_CC_CADS12,qty_MU_CADRS1,qty_MU_CADRD1,qty_MU_CASBA1,qty_MU_CASBA2,qty_MU_CADBA1,qty_MU_CADBA2,bay_qtys,qty_field_factory = 0, 0, 0, 0,0,0,0,0,0,0,0,0

	setAtvQty(Product,partSummaryAttr,"MU-CASSS1",0)
	setAtvQty(Product,partSummaryAttr,"MU-CADSS1",0)
	
	for parts in ["51109524-500","51109524-700","51109524-200","51109524-600","CF-SP0000", "CF-SP0001", "CF-PP0000", "CF-PP0001", "CF-CT4A00", "CF-CT4A02", "CF-CT4A01", "CF-CT4A03", "CF-CT4000", "CF-CT4002", "CF-CT4001", "CF-CT4003","CC-CASS02","CC-CASS12","MU-CADRS1","MU-CADRD1","MU-CASBA1","MU-CASBA2","CC-CADS02","CC-CADS12","MU-CADBA1","MU-CADBA2","50182411-500","50182411-600","50182411-200","50182411-700"]:
		setAtvQty(Product, partSummaryAttr, parts, 0)
	#cab_typ = 'Generic Cabinet'

	if cab_typ == 'Generic Cabinet':
		if isSingleAccess:
			qty_CC_CBDS01 = getValueSum(partQtyMap, ["CC-PWRR01", "CC-PWRB01", "CU-PWMR20", "CU-PWPR20"])
			qty_CC_CBDS01 = max(qty_CC_CBDS01, m.ceil(getValue(partQtyMap, "51454909-100") / 6.0))
			qty_CC_CBDS01 = max(qty_CC_CBDS01, getValueSum(partQtyMap, ["CC-PCNT02", "CC-PCNT05"]))
			cabinet_parts = ['CC-CASS02','CC-CASS12']

			if cabinetDoorDefault == 'Reverse Front' or cabinetDoorDefault == 'Double' or cabinetColorDefault == 'Gray-RAL 7032' or cabinetColorDefault == 'Custom' or cabinetDoorKeylock == 'Pushbutton':
				qty_CC_CASS02 = qty_CC_CBDS01				
			elif (cabinetDoorDefault == 'Standard' or cabinetDoorDefault == 'Reverse Front & Rear' or cabinetDoorDefault == 'Reverse Rear') and cabinetColorDefault == 'Gray-RAL 7035' and cabinetDoorKeylock == 'Standard':
				qty_CC_CASS12 = qty_CC_CBDS01
			if cabinetDoorDefault == 'Standard' or cabinetDoorDefault == 'Reverse Front & Rear' or cabinetDoorDefault == 'Reverse Rear' or cabinetDoorDefault == 'Reverse Front':
				qty_MU_CADRS1 = 1 * (qty_CC_CASS02 + qty_CC_CASS12)				
			elif cabinetDoorDefault == 'Double':
				qty_MU_CADRD1 = 1 * (qty_CC_CASS02 + qty_CC_CASS12)				
			if cabinetBase == 'Yes' and cab_size == "100mm":
				qty_MU_CASBA1 = 1 * (qty_CC_CASS02 + qty_CC_CASS12)				
			elif cabinetBase == 'Yes' and cab_size == "200mm":
				qty_MU_CASBA2 = 1 * (qty_CC_CASS02 + qty_CC_CASS12)

		else:
			qty_CC_CBDD01 = m.ceil(getValueSum(partQtyMap, ["CC-PWRR01", "CC-PWRB01", "CU-PWMR20", "CU-PWPR20"]) / 2.0)
			qty_CC_CBDD01 = max(qty_CC_CBDD01, m.ceil(m.ceil(getValue(partQtyMap, "51454909-100") / 6.0) / 2.0))
			qty_CC_CBDD01 = max(qty_CC_CBDD01, m.ceil(getValueSum(partQtyMap, ["CC-PCNT02", "CC-PCNT05"]) / 2.0))
			cabinet_parts = ['CC-CADS02','CC-CADS12']

			if cabinetDoorDefault == 'Reverse Front' or cabinetDoorDefault == 'Double' or cabinetColorDefault == 'Gray-RAL 7032' or cabinetColorDefault == 'Custom' or cabinetDoorKeylock == 'Pushbutton':
				qty_CC_CADS02 = qty_CC_CBDD01
				
			elif (cabinetDoorDefault == 'Standard' or cabinetDoorDefault == 'Reverse Front & Rear' or cabinetDoorDefault == 'Reverse Rear') and cabinetColorDefault == 'Gray-RAL 7035' and cabinetDoorKeylock == 'Standard':
				qty_CC_CADS12 = qty_CC_CBDD01
				
			if cabinetDoorDefault == 'Standard' or cabinetDoorDefault == 'Reverse Front & Rear' or cabinetDoorDefault == 'Reverse Rear' or cabinetDoorDefault == 'Reverse Front':
				qty_MU_CADRS1 = 2 * (qty_CC_CADS02 + qty_CC_CADS12)
				
			elif cabinetDoorDefault == 'Double':
				qty_MU_CADRD1 = 2 * (qty_CC_CADS02 + qty_CC_CADS12)
			if cabinetBase == 'Yes' and cab_size == "100mm":
				qty_MU_CADBA1 = 1 * (qty_CC_CADS02 + qty_CC_CADS12)
				
			elif cabinetBase == 'Yes' and cab_size == "200mm":
				qty_MU_CADBA2 = 1 * (qty_CC_CADS02 + qty_CC_CADS12)

		setAtvQty(Product, partSummaryAttr, "CC-CASS02", qty_CC_CASS02)
		setAtvQty(Product, partSummaryAttr, "CC-CASS12", qty_CC_CASS12)
		setAtvQty(Product, partSummaryAttr, "MU-CADRS1", qty_MU_CADRS1)
		setAtvQty(Product, partSummaryAttr, "MU-CADRD1", qty_MU_CADRD1)
		setAtvQty(Product, partSummaryAttr, "MU-CASBA1", qty_MU_CASBA1)
		setAtvQty(Product, partSummaryAttr, "MU-CASBA2", qty_MU_CASBA2)
		setAtvQty(Product, partSummaryAttr, "CC-CADS02", qty_CC_CADS02)
		setAtvQty(Product, partSummaryAttr, "CC-CADS12", qty_CC_CADS12)
		setAtvQty(Product, partSummaryAttr, "MU-CADBA1", qty_MU_CADBA1)
		setAtvQty(Product, partSummaryAttr, "MU-CADBA2", qty_MU_CADBA2)
		B, D, E, F = getBayQuantities(Product,cabinet_parts)
		bay_qtys = 2*(B+D+E+F)
		qty_field_factory = 3*B +1*D +2*E
		#Trace.Write("bay--aty--"+str(bay_qtys))
		if isSingleAccess:
			setAtvQty(Product,partSummaryAttr,"MU-CASSS1",bay_qtys)
			if complexing == "Factory":
				setAtvQty(Product, partSummaryAttr, "50182411-500", qty_field_factory)
			elif complexing == "Field":
				setAtvQty(Product, partSummaryAttr, "50182411-700", qty_field_factory)
		else:
			#Trace.Write("bay--aty-else--"+str(bay_qtys))
			setAtvQty(Product,partSummaryAttr,"MU-CADSS1",bay_qtys)
			if complexing == "Factory":
				setAtvQty(Product, partSummaryAttr, "50182411-200", qty_field_factory)
			elif complexing == "Field":
				setAtvQty(Product, partSummaryAttr, "50182411-600", qty_field_factory)

	if cab_typ == "Normal Cabinet" or cab_typ == "Generic Cabinet":
		part = ""
		complex_field_qty = getValueSum(partQtyMap, ["CC-CBDD01", "CC-CBDS01", "CC-C8DS01", "CC-C8SS01","CC-CASS02","CC-CASS12","CC-CADS02","CC-CADS12"])
		B, D, E, F = getBayQuantities(Product)
		 
		if isSingleAccess:
			cabinet_parts = ['CC-CBDS01', 'CC-C8SS01'] if cab_typ == "Normal Cabinet" else ['CC-CASS02', 'CC-CASS12']
			B, D, E, F = getBayQuantities(Product,cabinet_parts)
			if complexing == "Factory":
				setAtvQty(Product, partSummaryAttr, "51109524-500", (3*B + 1*D + 2*E))
			elif complexing == "Field":
				setAtvQty(Product, partSummaryAttr, "51109524-700", (3*B + 1*D + 2*E))
		else:
			cabinet_parts = ['CC-CBDD01', 'CC-C8DS01'] if cab_typ == "Normal Cabinet" else ['CC-CADS02', 'CC-CADS12']
			B, D, E, F = getBayQuantities(Product,cabinet_parts)
			if complexing == "Factory":
				setAtvQty(Product, partSummaryAttr, "51109524-200", (3*B + 1*D + 2*E))
			elif complexing == "Field":
				setAtvQty(Product, partSummaryAttr, "51109524-600", (3*B + 1*D + 2*E))
		if complexing == "Field":
			if crateType == "Domestic/Truck":
				if crateDesign == "Standard":
					if cab_size == "100mm":
						part = "CF-SP0000"
					elif cab_size == "200mm":
						part = "CF-SP0001"
				elif crateDesign == "Premium":
					if cab_size == "100mm":
						part = "CF-PP0000"
					elif cab_size == "200mm":
						part = "CF-PP0001"
			elif crateType == "Air":
				if crateDesign == "Standard":
					if cab_size == "100mm":
						part = "CF-CT4A00"
					elif cab_size == "200mm":
						part = "CF-CT4A02"
				elif crateDesign == "Premium":
					if cab_size == "100mm":
						part = "CF-CT4A01"
					elif cab_size == "200mm":
						part = "CF-CT4A03"
			elif crateType == "Ocean":
				if crateDesign == "Standard":
					if cab_size == "100mm":
						part = "CF-CT4000"
					elif cab_size == "200mm":
						part = "CF-CT4002"
				elif crateDesign == "Premium":
					if cab_size == "100mm":
						part = "CF-CT4001"
					elif cab_size == "200mm":
						part = "CF-CT4003"
			qty_cab = 1 * complex_field_qty
			if part:
				setAtvQty(Product, partSummaryAttr, part, qty_cab)
			setAtvQty(Product, partSummaryAttr, "51196958-400", qty_cab)
		elif complexing == "Factory":
			setAtvQty(Product, partSummaryAttr, "51196958-401", D)
			setAtvQty(Product, partSummaryAttr, "51196958-402", E)
			setAtvQty(Product, partSummaryAttr, "51196958-403", B)
			setAtvQty(Product, partSummaryAttr, "51196958-400", F)
#CXCPQ-119726 - #CXCPQ-119727 - end