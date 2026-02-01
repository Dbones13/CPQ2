incomplete = []

def getContainer(containerName):
	return Product.GetContainerByName(containerName)

def getFloat(Var):
	if Var:
		return float(Var)
	return 0

def getContainerColSum(containerName , rowId):
	container = getContainer(containerName)
	sum = 0
	for row in container.Rows:
		if row.RowIndex == rowId:
			for col in row.Columns:
				try:
					sum += getFloat(row[col.Name])
				except:
					pass
	return sum > 0


monitor_attrs = [
	"TPS_EX_Number_FPD_Lower_Tier_OEP_NON_TS",
	"TPS_EX_Number_FPD_Lower_Tier_OEP_TS",
	"TPS_EX_Number_FPD_Lower_Tier_IKB_Non_TS",
	"TPS_EX_Number_FPD_Lower_Tier_IKB_TS",
	"TPS_EX_Number_FPD_Upper_Tier_Non_TS",
	"TPS_EX_Number_FPD_Lower_Tier_TS",
	"TPS_EX_Desktop_Number_55in_FPD_Non_TS",
	"TPS_EX_Desktop_Number_23in_FPD_Non_TS",
	"TPS_EX_Desktop_Number_22in_FPD_TS",
	"TPS_EX_Desktop_Number_21_3in_FPD_Non_TS",
	"TPS_EX_Desktop_Number_21_3in_FPD_TS",
	"TPS_EX_Z_Console_Number_22in_FPD_Non_TS",
	"TPS_EX_Z_Console_Number_22in_FPS_TS",
	"TPS_EX_EZ_Console_Number_21_3in_FPD_TS",
	"TPS_EX_EZ_Console_Number_22in_FPD_NON_TS",
	"TPS_EX_EZ_Console_Number_22in_FPD_TS",
	"TPS_EX_Icon_Console_Number_21_3in_FPD_Non_TS",
	"TPS_EX_Icon_Console_Number_21_3in_FPD_TS"
]

esvt_attr = [
	"TPS_EX_TDC_US_ESVT",
	"TPS_EX_TDC_AM_ESVT",
	"TPS_EX_TDC_APP_ESVT",
	"TPS_EX_TDC_GUS_ESVT",
	"TPS_EX_ESVT_WO_Trade_Ins"
]

esvt_with_cabinet = esvt_attr + [
	"TPS_EX_Qty_Of_Cabinet_Slide_Mounting_For_Servers",
	"TPS_EX_Qty_Of_Cabinet_Fix_Mounting_For_Servers"
]

'''for attr in monitor_attrs:
	val = Product.Attributes.GetByName(attr).GetValue()
	if int(val) > 0:
		pass
	else:
		incomplete.append("TPSmonitorValidation")
		break'''

AcetCon = getContainer("TPS_EX_Conversion_ACET_EAPP")
acet = 0
acet = sum([int(Product.Attributes.GetByName(i).GetValue()) for i in esvt_with_cabinet])

for row in AcetCon.Rows:
	acet += getFloat(row["TPS_EX_Conversion_ACET_EAPP_Qty"])

Trace.Write("acet234"+str(acet))
if not getContainerColSum("TPS_EX_Station_Conversion_EST" , 0):
	if acet <= 0:
		Trace.Write("sadcdv1234"+str(acet))
		# if not getContainerColSum("TPS_EX_Conversion_ESVT_Server",0):
		incomplete.append("TPSserverValidation")
qty1 = 0
qty2 = 0

if Product.Attributes.GetByName("TPS_EX_Non_Reduntant_Conversion_ESVT").GetValue() == "Yes" or Product.Attributes.GetByName("TPS_EX_Redundant_Conversion_ESVT").GetValue() == "Yes":
	qty1 = 1

for row in esvt_attr:
	attr_val = Product.Attributes.GetByName(row).GetValue()
	qty2 += getFloat(attr_val)

esvt_qty = qty1 + qty2
if esvt_qty > 5:
	incomplete.append("ESVT_msg")
Trace.Write("incomplete >>" + str(incomplete))

Product.Attr('Incomplete').AssignValue(",".join(incomplete))