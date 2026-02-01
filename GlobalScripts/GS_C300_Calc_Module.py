from math import ceil
import GS_Get_Set_AtvQty
from GS_PS_Exp_Ent_BOM import setAtvQty
import GS_PMIO_Variable
import GS_C300_RG_UPC_Calc,GS_C300_RG_UPC_Calc3

def getFloat(val):
	if val:
		return float(val)
	return 0

def getValue(dataDict, val):
	return dataDict.get(val, 0)

def getValueSum(dataDict, values):
	res = 0
	for val in values:
		res += dataDict.get(val, 0)
	return res

def updateFFSegVar(Product, varValueMap):
	cont = Product.GetContainerByName("SerC_CG_FIM_FF_Tot_Seg_transpose")
	if not cont:
		return
	for row in cont.Rows:
		varValueMap["{}{}".format("S",row.RowIndex+1)] = float(row["Final_Tot_Seg"])

def getthequantity(Product,diction,partSummaryAttr,mm):
	var=0
	for i in diction:
		A=GS_Get_Set_AtvQty.getAtvQty(Product, partSummaryAttr,i)* mm
		var=var+A
	return var

def getTotalLoadIOSerC(Product, varValueMap):
	totalLoad = 0
	TUIO41 = 0
	TUIO31 = 0
	if Product.Attr("Dummy_RG_IO_Mounting_Solution").GetValue() == 'Universal Process Cab - 1.3M':
		TUIO41=GS_C300_RG_UPC_Calc.getC300UPC_46087(Product)
		TUIO31=GS_C300_RG_UPC_Calc3.getpartTUIO31(Product)
	totalLoad += getValueSum(varValueMap, ["X21", "X22" ,"X23"])
	totalLoad += getValueSum(varValueMap, ["W41", "W51", "W61", "W42", "W52", "W62", "W23", "Y31", "Y32", "Y33", 'YY31', 'YY32', 'YY33'])
	totalLoad += getValueSum(varValueMap, ["Y21", "Y22", "Y23", "W11", "W21", "W31", "W12", "W22", "W32", "Z91", 'YY21', 'YY22', 'YY23'])
	totalLoad += getValueSum(varValueMap, ["X11","X12","X13"])
	totalLoad += getValueSum(varValueMap, ["Y71", "Y72", "Y73", "W81", "W91", "W82", "W92", "W73"])
	totalLoad += getValueSum(varValueMap, ["X51", "X52", "X53"])
	totalLoad += getValueSum(varValueMap, ["X41", "X42", "X43"])
	totalLoad += getValueSum(varValueMap, ["Y81", "Y82", "Y83", "V21", "V31", "V13", "V22", "V32", "V43"])
	totalLoad += getValueSum(varValueMap, ["Y91", "Y92", "Y93", "V61", "V71", "V53", "V62", "V72", "V83"])
	totalLoad += getValueSum(varValueMap, ["Z11", "Z12", "Z13", "Z23", "Z31", "Z32", "Z33"])
	if Product.Name == "Series-C Control Group" and Product.Attr("FIM_Type").GetValue() == "FIM4":
		totalLoad += (4 * (ceil(getValue(varValueMap, "S4")/4.0) + ceil(getValue(varValueMap, "S5")/4.0) + ceil(getValue(varValueMap, "S6")/4.0)))
	elif Product.Name == "Series-C Control Group":
		totalLoad += (8 * (ceil(getValue(varValueMap, "S4")/8.0) + ceil(getValue(varValueMap, "S5")/8.0) + ceil(getValue(varValueMap, "S6")/8.0)))
	totalLoad += getValueSum(varValueMap, ["Y43", "Y53", "Y63"])
	totalLoad += ceil(1.5 * getValueSum(varValueMap, ["Z81", "Z82", "Z83", "Z84", "Z85", "Z86"]))
	totalLoad += getValueSum(varValueMap, ["X33"])
	totalLoad += getValueSum(varValueMap, ["X61", "X62", "X63", "X71", "X72", "X73", "X81", "X82", "X83"])
	totalLoad += getValueSum(varValueMap, ["Z41", "Z51", "Z61", "Z71", "Z42", "Z43", "Z52", "Z53", "Z62", "Z63", "Z72", "Z73", "V91", "V92"])
	if Product.Name == "Series-C Remote Group":
		totalLoad += (1 * getValueSum(varValueMap, ["XX61", "XX62", "XX63"])) + (TUIO41 + TUIO31)#(2 * getValueSum(varValueMap, ["XX61", "XX62", "XX63"]))
		totalLoad += (1 * getValueSum(varValueMap, ["XX71", "XX72", "XX73", "XX81", "XX82", "XX83"]))#(2 * getValueSum(varValueMap, ["XX71", "XX72", "XX73", "XX81", "XX82", "XX83"]))
	return totalLoad

def getTotalLoadIOSCM(Product, varValueMap):
	totalLoad = 0
	totalLoad += getValueSum(varValueMap, ["X21", "X22" ,"X23"])
	totalLoad += getValueSum(varValueMap, ["Y31", "Y32" ,"Y33"])
	totalLoad += getValueSum(varValueMap, ["Y21", "Y22" ,"Y23"])
	totalLoad += getValueSum(varValueMap, ["X11", "X12" ,"X13"])
	totalLoad += getValueSum(varValueMap, ['YY21', 'YY22', 'YY23', 'YY31', 'YY32', 'YY33'])
	totalLoad += getValueSum(varValueMap, ["Y71", "Y72" ,"Y73"])
	totalLoad += getValueSum(varValueMap, ["X51", "X52" ,"X53"])
	totalLoad += getValueSum(varValueMap, ["X41", "X42" ,"X43"])
	totalLoad += getValueSum(varValueMap, ["Y81", "Y82" ,"Y83"])
	totalLoad += getValueSum(varValueMap, ["Z11", "Z12" ,"Z13", "Z31", "Z32" ,"Z33"])
	if Product.Name == "Series-C Control Group" and Product.Attr("FIM_Type").GetValue() == "FIM4":
		totalLoad += 4 * (ceil(getValue(varValueMap, "S4")/4.0) + ceil(getValue(varValueMap, "S5")/4.0) + ceil(getValue(varValueMap, "S6")/4.0))
	elif Product.Name == "Series-C Control Group":
		totalLoad += 8 * (ceil(getValue(varValueMap, "S4")/8.0) + ceil(getValue(varValueMap, "S5")/8.0) + ceil(getValue(varValueMap, "S6")/8.0))
	totalLoad += ceil(1.5 * getValueSum(varValueMap, ["Z81", "Z82", "Z83", "Z84", "Z85", "Z86"]))
	totalLoad += getValueSum(varValueMap, ["X33"])
	totalLoad += getValueSum(varValueMap, ["X61", "X62", "X63", "X71", "X72", "X73", "X81", "X82", "X83"])
	totalLoad += getValueSum(varValueMap, ["Z41", "Z51", "Z61", "Z71", "Z42", "Z43", "Z52", "Z53", "Z62", "Z63", "Z72", "Z73"])
	totalLoad += getValueSum(varValueMap, ["W11", "W12", "W13"])
	totalLoad += getValueSum(varValueMap, ["W21", "W22", "W23"])
	totalLoad += getValueSum(varValueMap, ["W31", "W41", "W32", "W42", "W33", "W43"])
	return totalLoad


def getTotalLoadIOTurboM(Product, varValueMap):
	totalLoad = 0
	totalLoad += getValueSum(varValueMap, ["W41", "W51", "W61", "W42", "W52", "W62", "W23", "Y31", "Y32", "Y33"])
	totalLoad += getValueSum(varValueMap, ["Y21", "Y22", "Y23", "W11", "W21", "W31", "W12", "W22", "W32", "Z91"])
	totalLoad += getValueSum(varValueMap, ["Y71", "Y72", "Y73", "W81", "W91", "W82", "W92", "W73"])
	totalLoad += getValueSum(varValueMap, ["Y81", "Y82", "Y83", "V21", "V31", "V13", "V22", "V32", "V43"])
	totalLoad += getValueSum(varValueMap, ["Y91", "Y92", "Y93", "V61", "V71", "V53", "V62", "V72", "V83"])
	totalLoad += getValueSum(varValueMap, ["Z11", "Z12", "Z13", "Z23", "Z31", "Z32", "Z33"])
	totalLoad += getValueSum(varValueMap, ["Y43", "Y53", "Y63"])
	totalLoad += getValueSum(varValueMap, ["X61", "X62", "X63", "X71", "X72", "X73", "X81", "X82", "X83"])
	totalLoad += getValueSum(varValueMap, ["Z41", "Z51", "Z61", "Z71", "Z42", "Z43", "Z52", "Z53", "Z62", "Z63", "Z72", "Z73", "V91", "V92"])
	totalLoad += getValueSum(varValueMap, ["A11"])
	totalLoad += getValueSum(varValueMap, ["A21"])
	return totalLoad

def getTotalLoadIOSerC_CN100CEE(Product, varValueMap):
	totalLoad = 0
	totalLoad += getValueSum(varValueMap, ["X21", "X22", "X23"])
	totalLoad += getValueSum(varValueMap, ["W41", "W51", "W61", "W42", "W52", "W62", "W23", "Y31", "Y32", "Y33", 'YY31', 'YY32', 'YY33'])
	totalLoad += getValueSum(varValueMap, ["Y21", "Y22", "Y23", "W11", "W21", "W31", "W12", "W22", "W32", "Z91", 'YY21', 'YY22', 'YY23'])
	totalLoad += getValueSum(varValueMap, ["X11", "X12", "X13"])
	totalLoad += getValueSum(varValueMap, ["Y71", "Y72", "Y73", "W81", "W91", "W82", "W92", "W73"])
	totalLoad += getValueSum(varValueMap, ["X51", "X52", "X53"])
	totalLoad += getValueSum(varValueMap, ["X41", "X42", "X43"])
	totalLoad += getValueSum(varValueMap, ["Y81", "Y82", "Y83", "V21", "V31", "V13", "V22", "V32", "V43"])
	totalLoad += getValueSum(varValueMap, ["Y91", "Y92", "Y93", "V61", "V71", "V53", "V62", "V72", "V83"])
	totalLoad += getValueSum(varValueMap, ["Z11", "Z12", "Z13", "Z23", "Z31", "Z32", "Z33"])
	totalLoad += getValueSum(varValueMap, ["Y43", "Y53", "Y63"])
	totalLoad += ceil(1.5 * getValueSum(varValueMap, ["Z81", "Z82", "Z83", "Z84", "Z85", "Z86"]))
	totalLoad += getValueSum(varValueMap, ["X33"])
	totalLoad += getValueSum(varValueMap, ["X61", "X62", "X63",  "X71", "X72", "X73", "X81", "X82", "X83"])
	totalLoad += getValueSum(varValueMap, ["Z41", "Z51", "Z61", "Z71", "Z42", "Z43", "Z52", "Z53", "Z62", "Z63", "Z72", "Z73", "V91", "V92"])
	return totalLoad

def getTotalLoadIO_PMIO(Product):
	if Product.Name not in ("Series-C Remote Group", "Series-C Control Group"):
		return 0
	resDict = GS_PMIO_Variable.partCalc(Product)
	varValueMap = GS_Get_Set_AtvQty.getAllAtvQty(Product,'SerC_IO_Params')
	updateFFSegVar(Product, varValueMap)

	ioFamily = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	controllerType = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
	pmioSolunRequired = Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()

	totalLoad = 0
	if ioFamily == "Series C" and (controllerType == "C300 CEE" or controllerType == "") and pmioSolunRequired == "Yes":
		for key in resDict.keys():
			varValueMap[key] = resDict.get(key, 0)
		totalLoad += getValueSum(varValueMap, ["X11", "X12", "X13", "X21", "X22", "X41", "X42", "LX81", "LX83", "MX81", "MX83", "NX81", "NX83"])
		totalLoad += getValueSum(varValueMap, ["X31", "X32", "X33", "OX81", "OX83", "PX81", "PX83"])
		totalLoad += getValueSum(varValueMap, ["X53"])
		totalLoad += getValueSum(varValueMap, ["X63", "X73", "X83"])
		totalLoad += getValueSum(varValueMap, ["X93"])
		totalLoad += getValueSum(varValueMap, ["Y11", "Y12", "Y13", "Y22", "QX81", "QX83", "RX81", "RX82", "SX81", "SX83"])
		totalLoad += getValueSum(varValueMap, ["Y31", "Y32", "Y41", "Y42", "CX81", "CX82"])
		totalLoad += getValueSum(varValueMap, ["Y51", "Y52", "DX81", "DX82"])
		totalLoad += getValueSum(varValueMap, ["Y63", "Y93", "Z23", "EX83", "HX83"])
		totalLoad += getValueSum(varValueMap, ["Y71", "Y72"])
		totalLoad += getValueSum(varValueMap, ["Y81", "Y83", "Z11", "Z13", "Z31", "Z33", "FX81", "FX83", "GX81", "GX83"])
		totalLoad += getValueSum(varValueMap, ["Z43", "Z63", "Z73", "Z83", "AX83", "BX83", "IX83", "JX83"])
		totalLoad += getValueSum(varValueMap, ["Z51", "Z52", "Z91", "Z92", "KX83"])
	return totalLoad


def getTotalLoadIO(Product):
	if Product.Name not in ("Series-C Remote Group", "Series-C Control Group"):
		return 0
	varValueMap = GS_Get_Set_AtvQty.getAllAtvQty(Product,'SerC_IO_Params')
	updateFFSegVar(Product, varValueMap)

	ioFamily = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	controllerType = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()
	pmioSolunRequired = Product.Attr('SerC_CG_PM_IO_Solution_required').GetValue()

	totalLoad = 0
	if ioFamily == "Series-C Mark II":
		totalLoad = getTotalLoadIOSCM(Product, varValueMap)
	elif ioFamily == "Turbomachinery":
		totalLoad = getTotalLoadIOTurboM(Product, varValueMap)
	elif ioFamily == "Series C" and controllerType == "CN100 CEE":
		totalLoad = getTotalLoadIOSerC_CN100CEE(Product, varValueMap)
	else:
		totalLoad = getTotalLoadIOSerC(Product, varValueMap)
	return totalLoad


def getTotalIoPointLoad(Product):
	if Product.Name not in ("Series-C Remote Group", "Series-C Control Group"):
		return 0
	if Product.Name == "Series-C Control Group":
		partSummaryAttr = "Series_C_CG_Part_Summary"
	else:
		partSummaryAttr = "Series_C_RG_Part_Summary"

	ioFamily = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	controllerType = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()

	if ioFamily != "Series C" or controllerType not in ("CN100 CEE", "CN100 I/O HIVE - C300 CEE"):
		return 0

	dic1=["CC-TAIN01","CC-TAIX51","CC-TAIL51","CC-TAON01","CC-TAOX51","CC-TAIN11","CC-TAIX61","CC-TAON11","CC-TAOX61","CC-TAID11","CC-TAOX11","CC-TAID01","CC-TAOX01","CC-GAIX11","CC-GAIX21","CC-GAOX11","CC-GAOX21","CC-TAIX01","CC-TAIX11"]
	dic2=["CC-TUIO41","CC-TUIO31","CC-TUIO11","CC-TUIO01","CC-TDIL11","CC-TDI120","CC-TDI230","CC-TDOB11","CC-TDIL01","CC-TDI110","CC-TDI151","CC-TDI220","CC-TDOB01","CC-GDIL11","CC-GDIL21","CC-GDIL01","CC-GDOL11","CC-TDOR11","CC-TDOR01"]
	dic3=["CC-TAIM01"]
	dic4=["CC-TPIX11"]

	a1=getthequantity(Product,dic1,partSummaryAttr,16)
	a2=getthequantity(Product,dic2,partSummaryAttr,32)
	a3=getthequantity(Product,dic3,partSummaryAttr,64)
	a4=getthequantity(Product,dic4,partSummaryAttr,8)

	return (a1+a2+a3+a4)


def getBayQuantities(Product, cabinet_parts=None):
	if Product.Name not in ("Series-C Remote Group", "Series-C Control Group"):
		return 0, 0, 0, 0

	isMarkII = Product.Attr("SerC_CG_IO_Family_Type").GetValue() == "Series-C Mark II"
	if not isMarkII:
		return 0, 0, 0, 0

	if Product.Name == "Series-C Control Group":
		partSummaryAttr = "Series_C_CG_Part_Summary"
	else:
		partSummaryAttr = "Series_C_RG_Part_Summary"

	if cabinet_parts is None:
		cabinet_parts = ["CC-CBDD01", "CC-CBDS01","CC-C8SS01","CC-C8DS01","CC-CASS02","CC-CASS12","CC-CADS02","CC-CADS12"]#added cabinet parts based on this story#CXCPQ-119727
	partQtyMap = GS_Get_Set_AtvQty.getAllAtvQty(Product, partSummaryAttr)
	A = getValueSum(partQtyMap, cabinet_parts)
	B = int(A) // 4
	rem = A % 4
	E = 1 if rem == 3 else 0
	D = 1 if rem == 2 else 0
	F = 1 if rem == 1 else 0
	return B, D, E, F

def populateCabinetParts(Product):
	if Product.Name not in ("Series-C Remote Group", "Series-C Control Group"):
		return

	isMarkII = Product.Attr("SerC_CG_IO_Family_Type").GetValue() == "Series-C Mark II"
	if not isMarkII:
		return

	crateType = Product.Attr("Crate Type").GetValue()
	crateDesign = Product.Attr("Crate Design").GetValue()
	siteVoltage = Product.Attr("CE_Site_Voltage").GetValue()
	if Product.Name == "Series-C Control Group":
		partSummaryAttr = "Series_C_CG_Part_Summary"
		isSingleAccess = Product.Attr("SerC_CG_Cabinet_Access").GetValue() == "Single Access"
		cabinetColorDefault = Product.Attr("SerC_CG_Cabinet_Color_Default").GetValue()
		cabinetDoorDefault = Product.Attr("SerC_CG_Cabinet_Doors_Default").GetValue()
		cabinetDoorKeylock = Product.Attr("SerC_CG_Cabinet_Door_Keylock _Default").GetValue()
		cabinetBase = Product.Attr("SerC_CG_Cabinet_Base_(Plinth)").GetValue()
		cabinetBaseSize = Product.Attr("SerC_CG_Cabinet_Base_Size").GetValue()
		fanOption = Product.Attr("SerC_CG_Fan_Option").GetValue()
		complexing = Product.Attr("SerC_CG_Complexing").GetValue()
	else:
		partSummaryAttr = 'Series_C_RG_Part_Summary'
		isSingleAccess = Product.Attr("SerC_RG_Cabinet_Access").GetValue() == "Single Access"
		cabinetColorDefault = Product.Attr("SerC_RG_Cabinet_Color_Default").GetValue()
		cabinetDoorDefault = Product.Attr("SerC_RG_Cabinet_Doors_Default").GetValue()
		cabinetDoorKeylock = Product.Attr("SerC_RG_Cabinet_Door_Keylock_Default").GetValue()
		cabinetBase = Product.Attr("SerC_RG_Cabinet_Base_(Plinth)").GetValue()
		cabinetBaseSize = Product.Attr("SerC_RG_Cabinet_Base_Size").GetValue()
		fanOption = Product.Attr("SerC_RG_Fan_Option").GetValue()
		complexing = Product.Attr("SerC_RG_Complexing").GetValue()

	partQtyMap = GS_Get_Set_AtvQty.getAllAtvQty(Product, partSummaryAttr)

	qty_CC_CBDS01, qty_CC_CBDD01 = 0, 0
	if isSingleAccess:
		qty_CC_CBDS01 = getValueSum(partQtyMap, ["CC-PWRR01", "CC-PWRB01", "CU-PWMR20", "CU-PWPR20"])
		qty_CC_CBDS01 = max(qty_CC_CBDS01, ceil(getValue(partQtyMap, "51454909-100") / 6.0))
		qty_CC_CBDS01 = max(qty_CC_CBDS01, getValueSum(partQtyMap, ["CC-PCNT02", "CC-PCNT05"]))

		setAtvQty(Product, partSummaryAttr, "CC-CBDS01", qty_CC_CBDS01)
	else:
		qty_CC_CBDD01 = ceil(getValueSum(partQtyMap, ["CC-PWRR01", "CC-PWRB01", "CU-PWMR20", "CU-PWPR20"]) / 2.0)
		qty_CC_CBDD01 = max(qty_CC_CBDD01, ceil(ceil(getValue(partQtyMap, "51454909-100") / 6.0) / 2.0))
		qty_CC_CBDD01 = max(qty_CC_CBDD01, ceil(getValueSum(partQtyMap, ["CC-PCNT02", "CC-PCNT05"]) / 2.0))

		setAtvQty(Product, partSummaryAttr, "CC-CBDD01", qty_CC_CBDD01)

	qty_cab = qty_CC_CBDS01 + qty_CC_CBDD01
	qty_1_isto_2 = qty_CC_CBDS01 + 2 * qty_CC_CBDD01

	setAtvQty(Product, partSummaryAttr, "51199948-100", qty_1_isto_2)

	if cabinetColorDefault == "Gray-RAL 7032":
		setAtvQty(Product, partSummaryAttr, "51197174-200", qty_cab)
	elif cabinetColorDefault == "Custom":
		setAtvQty(Product, partSummaryAttr, "51197174-100", qty_cab)

	if cabinetDoorKeylock == "Standard":
		setAtvQty(Product, partSummaryAttr, "51197165-100", qty_1_isto_2)
	else:
		setAtvQty(Product, partSummaryAttr, "51197165-200", qty_1_isto_2)

	if cabinetDoorDefault == "Double":
		qty = qty_cab
		if not isSingleAccess:
			qty *= 2
		setAtvQty(Product, partSummaryAttr, "MU-C8DRD1", qty)
	else:
		qty = qty_cab
		if not isSingleAccess:
			if cabinetDoorDefault == "Reverse Front":
				setAtvQty(Product, partSummaryAttr, "51197150-400", qty)
			if cabinetDoorDefault == "Reverse Rear":
				setAtvQty(Product, partSummaryAttr, "51197150-300", qty)
			if cabinetDoorDefault == "Reverse Front & Rear":
				setAtvQty(Product, partSummaryAttr, "51197150-200", qty)
			qty *= 2
		else:
			if cabinetDoorDefault == "Reverse Front":
				setAtvQty(Product, partSummaryAttr, "51197150-600", qty)
			else:
				setAtvQty(Product, partSummaryAttr, "51197150-500", qty)
		setAtvQty(Product, partSummaryAttr, "MU-C8DRS1", qty)

	if fanOption == "Assembly":
		if siteVoltage == "120V":
			setAtvQty(Product, partSummaryAttr, "51199947-175", qty_1_isto_2)
		elif siteVoltage == "240V":
			setAtvQty(Product, partSummaryAttr, "51199947-275", qty_1_isto_2)
	elif fanOption == "Assembly - Universal Fan":
		setAtvQty(Product, partSummaryAttr, "51199947-375", qty_1_isto_2)

	if isSingleAccess and cabinetBase == "Yes" and cabinetBaseSize == "100mm":
		setAtvQty(Product, partSummaryAttr, "MU-C8SBA1", qty_cab)
	elif isSingleAccess and cabinetBase == "Yes" and cabinetBaseSize == "200mm":
		setAtvQty(Product, partSummaryAttr, "MU-C8SBA2", qty_cab)
	elif not isSingleAccess and cabinetBase == "Yes" and cabinetBaseSize == "100mm":
		setAtvQty(Product, partSummaryAttr, "MU-C8DBA1", qty_cab)
	elif not isSingleAccess and cabinetBase == "Yes" and cabinetBaseSize == "200mm":
		setAtvQty(Product, partSummaryAttr, "MU-C8DBA2", qty_cab)

	B, D, E, F = getBayQuantities(Product)

	if not isSingleAccess:
		setAtvQty(Product, partSummaryAttr, "MU-C8DSS1", 2 * (B + D + E + F))
	else:
		setAtvQty(Product, partSummaryAttr, "MU-C8SSS1", 2 * (B + D + E + F))

	if complexing == "Field":
		setAtvQty(Product, partSummaryAttr, "51196958-400", qty_cab)
	elif complexing == "Factory":
		setAtvQty(Product, partSummaryAttr, "51196958-401", D)
		setAtvQty(Product, partSummaryAttr, "51196958-402", E)
		setAtvQty(Product, partSummaryAttr, "51196958-403", B)
		setAtvQty(Product, partSummaryAttr, "51196958-400", F)

	if complexing == "Field":
		parts = {
			"CF-SC0000" : 0, "CF-SC0001" : 0, "CF-SC0002" : 0, "CF-SC0003" : 0, "CF-SC0004" : 0, "CF-SC0005" : 0, "CF-PC0000" : 0, "CF-PC0001" : 0, "CF-PC0002" : 0, "CF-PC0003" : 0, "CF-PC0004" : 0, "CF-PC0005" : 0, "CF-CT7A00" : 0, "CF-CT7A02" : 0, "CF-CT8A00" : 0, "CF-CT8A02" : 0, "CF-CT9A00" : 0, "CF-CT9A02" : 0, "CF-CT7A01" : 0, "CF-CT7A03" : 0, "CF-CT8A01" : 0, "CF-CT8A03" : 0, "CF-CT9A01" : 0, "CF-CT9A03" : 0, "CF-CT7000" : 0, "CF-CT7002" : 0, "CF-CT8000" : 0, "CF-CT8002" : 0, "CF-CT9000" : 0, "CF-CT9002" : 0, "CF-CT7001" : 0, "CF-CT7003" : 0, "CF-CT8001" : 0, "CF-CT8003" : 0, "CF-CT9001" : 0, "CF-CT9003" : 0}
		for part, qty in parts.items():
			setAtvQty(Product, partSummaryAttr, part, qty)
		
	elif complexing == "Factory":
		parts = {
			"CF-SC0000" : 0, "CF-SC0001" : 0, "CF-SC0002" : 0, "CF-SC0003" : 0, "CF-SC0004" : 0, "CF-SC0005" : 0, "CF-PC0000" : 0, "CF-PC0001" : 0, "CF-PC0002" : 0, "CF-PC0003" : 0, "CF-PC0004" : 0, "CF-PC0005" : 0, "CF-CT7A00" : 0, "CF-CT7A02" : 0, "CF-CT8A00" : 0, "CF-CT8A02" : 0, "CF-CT9A00" : 0, "CF-CT9A02" : 0, "CF-CT7A01" : 0, "CF-CT7A03" : 0, "CF-CT8A01" : 0, "CF-CT8A03" : 0, "CF-CT9A01" : 0, "CF-CT9A03" : 0, "CF-CT7000" : 0, "CF-CT7002" : 0, "CF-CT8000" : 0, "CF-CT8002" : 0, "CF-CT9000" : 0, "CF-CT9002" : 0, "CF-CT7001" : 0, "CF-CT7003" : 0, "CF-CT8001" : 0, "CF-CT8003" : 0, "CF-CT9001" : 0, "CF-CT9003" : 0,"CF-SP0000" : 0, "CF-SP0001" : 0, "CF-PP0000" : 0, "CF-PP0001" : 0, "CF-CT4A00" : 0, "CF-CT4A02" : 0, "CF-CT4A01" : 0, "CF-CT4A03" : 0, "CF-CT4000" : 0, "CF-CT4002" : 0, "CF-CT4001" : 0, "CF-CT4003" : 0
		}
		if crateType == "Domestic/Truck" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-SC0000"] = D
		if crateType == "Domestic/Truck" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-SC0001"] = D
		if crateType == "Domestic/Truck" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-SC0002"] = E
		if crateType == "Domestic/Truck" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-SC0003"] = E
		if crateType == "Domestic/Truck" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-SC0004"] = B
		if crateType == "Domestic/Truck" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-SC0005"] = B
		if crateType == "Domestic/Truck" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-PC0000"] = D
		if crateType == "Domestic/Truck" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-PC0001"] = D
		if crateType == "Domestic/Truck" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-PC0002"] = E
		if crateType == "Domestic/Truck" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-PC0003"] = E
		if crateType == "Domestic/Truck" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-PC0004"] = B
		if crateType == "Domestic/Truck" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-PC0005"] = B
		if crateType == "Air" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-CT7A00"] = D
		if crateType == "Air" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-CT7A02"] = D
		if crateType == "Air" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-CT8A00"] = E
		if crateType == "Air" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-CT8A02"] = E
		if crateType == "Air" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-CT9A00"] = B
		if crateType == "Air" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-CT9A02"] = B
		if crateType == "Air" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-CT7A01"] = D
		if crateType == "Air" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-CT7A03"] = D
		if crateType == "Air" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-CT8A01"] = E
		if crateType == "Air" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-CT8A03"] = E
		if crateType == "Air" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-CT9A01"] = B
		if crateType == "Air" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-CT9A03"] = B
		if crateType == "Ocean" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-CT7000"] = D
		if crateType == "Ocean" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-CT7002"] = D
		if crateType == "Ocean" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-CT8000"] = E
		if crateType == "Ocean" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-CT8002"] = E
		if crateType == "Ocean" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-CT9000"] = B
		if crateType == "Ocean" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-CT9002"] = B
		if crateType == "Ocean" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-CT7001"] = D
		if crateType == "Ocean" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-CT7003"] = D
		if crateType == "Ocean" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-CT8001"] = E
		if crateType == "Ocean" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-CT8003"] = E
		if crateType == "Ocean" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-CT9001"] = B
		if crateType == "Ocean" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-CT9003"] = B
		if crateType == "Domestic/Truck" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-SP0000"] = F
		if crateType == "Domestic/Truck" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-SP0001"] = F
		if crateType == "Domestic/Truck" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-PP0000"] = F
		if crateType == "Domestic/Truck" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-PP0001"] = F
		if crateType == "Air" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-CT4A00"] = F
		if crateType == "Air" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-CT4A02"] = F
		if crateType == "Air" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-CT4A01"] = F
		if crateType == "Air" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-CT4A03"] = F
		if crateType == "Ocean" and crateDesign == "Standard" and cabinetBaseSize == "100mm":
			parts["CF-CT4000"] = F
		if crateType == "Ocean" and crateDesign == "Standard" and cabinetBaseSize == "200mm":
			parts["CF-CT4002"] = F
		if crateType == "Ocean" and crateDesign == "Premium" and cabinetBaseSize == "100mm":
			parts["CF-CT4001"] = F
		if crateType == "Ocean" and crateDesign == "Premium" and cabinetBaseSize == "200mm":
			parts["CF-CT4003"] = F
		for part, qty in parts.items():
			setAtvQty(Product, partSummaryAttr, part, qty)

	if Product.Name=="Series-C Control Group":
		parts = {
			"CF-MSD000" : 0, "CF-MSD001" : 0, "CF-MSA000" : 0, "CF-MSA001" : 0, "CF-MSO000" : 0, "CF-MSO001" : 0
		}
		io_flag = False
		cont_col_mapping = {'C300_C IO MS2': 'Labor_IS', 'C300_C IO MS3':'Labor_IS','C300_CG_Universal_IO_Mark_1':'Labor_IS','C300_CG_Universal_IO_Mark_2':'Labor_IS','C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont':'Labor_IS','C300_SerC_Enhanced_Function_IO_Mark_Group_CG_Cont1':'Labor_IS'}
		for cont in cont_col_mapping:
			io_cont = Product.GetContainerByName(cont)
			for cont_row in io_cont.Rows:
				if getFloat(cont_row.GetColumnByName(cont_col_mapping[cont]).Value) > 0:
					io_flag = True
					break
			if io_flag:
				break
		if io_flag and crateType == "Domestic/Truck" and crateDesign == "Standard":
			parts["CF-MSD000"] = 2
		if io_flag and crateType == "Domestic/Truck" and crateDesign == "Premium":
			parts["CF-MSD001"] = 2
		if io_flag and crateType == "Air" and crateDesign == "Standard":
			parts["CF-MSA000"] = 2
		if io_flag and crateType == "Air" and crateDesign == "Premium":
			parts["CF-MSA001"] = 2
		if io_flag and crateType == "Ocean" and crateDesign == "Standard":
			parts["CF-MSO000"] = 2
		if io_flag and crateType == "Ocean" and crateDesign == "Premium":
			parts["CF-MSO001"] = 2
		for part, qty in parts.items():
			setAtvQty(Product, partSummaryAttr, part, qty)
#parts=populateCabinetParts(Product)
#Trace.Write("SK:"+str(parts))
def getIoSum(container, columns):
	ioSum = 0

	for row in container.Rows:
		for col in row.Columns:
			if col.Name in columns:
				ioSum += getFloat(row[col.Name])

	return ioSum

def getSWHSQty(Product):
	ioFamily = Product.Attr('SerC_CG_IO_Family_Type').GetValue()
	controllerType = Product.Attr('SerC_CG_Type_of_Controller_Required').GetValue()

	if ioFamily != "Series C" or controllerType != "CN100 CEE":
		return 0, 0
	
	contColMap = {
		"C300_C IO MS" : ["Red_IS", "Future_Red_IS", "Non_Red_IS", "Red_NIS", "Future_Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Future_Red_ISLTR", "Non_Red_ISLTR"],
		"C300_CG_Universal_IO_cont_1" : ["Red_IS", "Future_Red_IS", "Non_Red_IS", "Red_NIS", "Future_Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Future_Red_ISLTR", "Non_Red_ISLTR"],
		"C300_CG_Universal_IO_cont_2" : ["Red_IS", "Future_Red_IS", "Non_Red_IS", "Red_NIS", "Future_Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Future_Red_ISLTR", "Non_Red_ISLTR", "Red_RLY", "Future_Red_RLY", "Non_Red_RLY"],
		"SerC_CG_Enhanced_Function_IO_Cont" : ["Red_IS", "Future_Red_IS", "Non_Red_IS", "Red_NIS", "Future_Red_NIS", "Non_Red_NIS", "Red_ISLTR", "Future_Red_ISLTR", "Non_Red_ISLTR"],
		"SerC_CG_Enhanced_Function_IO_Cont2" : ["Red_IS" ,"Future_Red_IS" ,"Non_Red_IS" ,"Red_NIS" ,"Future_Red_NIS" ,"Non_Red_NIS" ,"Red_ISLTR" ,"Future_Red_ISLTR" ,"Non_Red_ISLTR" ,"Red_RLY" ,"Future_Red_RLY" ,"Non_Red_RLY"],
		"C300_SerC_GIIS_CG_Cont" : ["Red_IS" ,"Future_Red_IS" ,"Non_Red_IS"]
	}
	ioSum = 0
	for contName, cols in contColMap.items():
		cont = Product.GetContainerByName(contName)
		ioSum += getIoSum(cont, cols)

	qty_SWHS02 = int(ioSum / 800)
	qty_SWHS01 = ceil((ioSum % 800) / 240.0)

	if ioSum <= 800 and ioSum >= 241:
		qty_SWHS02= 1
		qty_SWHS01= 0 
	if ioSum <= 240 and ioSum >= 1:
		qty_SWHS01= 1
		qty_SWHS02= 0

	return qty_SWHS01, qty_SWHS02