from math import ceil
import System.Decimal as d
#import sys
from GS_Load_SM_RIO_Cab_Summary import getLoadSMRIOCabSummary

def Roundup(n):
    Trace.Write(n)
    res= int(n)
    return res if res == n else res+1

def getNoPowerSupply(Product):
    Nos_PSU_Type = 0
    if Product.Name == "SM Control Group":
        cabVolRow = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0]
        cabFeederVoltage = cabVolRow.GetColumnByName('Cabinet_Feeder_Voltage').DisplayValue
        cabPowSupRow = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Left').Rows[0]
        cabPowerSupply = cabPowSupRow.GetColumnByName('Power_Supply').DisplayValue
        if cabFeederVoltage == "Externally Sourced 24VDC":
            Power_calculation_VA = float(getLoadSMRIOCabSummary(Product)*24)#1.949*24=46.776
            Total_load_VA = float(Power_calculation_VA/.947)#46.776/.947=49.39
            if cabPowerSupply == "Redundant":
                Nos_PSU_Type = 2*(Roundup(Total_load_VA/(24*24)))#49.39/576=0.0857=1*2=2
            elif cabPowerSupply == "Non Redundant":
                Nos_PSU_Type = Roundup(Total_load_VA/(24*24))
    elif Product.Name == "SM Remote Group":
        cabVolRow = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0]
        cabFeederVoltage = cabVolRow.GetColumnByName('Cabinet_Feeder_Voltage').DisplayValue
        EnclosureType= Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0]
        EnclosureTypeValue = EnclosureType.GetColumnByName('Enclosure_Type').DisplayValue
        cabPowSupRow = Product.GetContainerByName('SM_RG_Cabinet_Details_Cont_Left').Rows[0]
        cabPowerSupply = cabPowSupRow.GetColumnByName('Power_Supply').DisplayValue
        if EnclosureTypeValue == "Cabinet" and cabFeederVoltage == "Externally Sourced 24VDC":
            Power_calculation_VA = float(getLoadSMRIOCabSummary(Product)*24)#1.984*24=47.616
            Total_load_VA = float(Power_calculation_VA/.947)#47.616/.947=50.28
            if cabPowerSupply == "Redundant":
                Nos_PSU_Type = 2*(Roundup(Total_load_VA/(24*24)))#50.28/576=0.0872=1*2=2
            elif cabPowerSupply == "Non Redundant":
                Nos_PSU_Type = Roundup(Total_load_VA/(24*24))
    return Nos_PSU_Type

def getPowerSupplyPart(Product, parts_dict):
    try:
        qty = getNoPowerSupply(Product)
        if qty > 0:
            parts_dict["50165610-001"] = {'Quantity' : qty, 'Description': 'QUINT4-PS/24DC/24DC/20/SC/+ (SAP Material number 50165610-001)'}
    except Exception as e:
        Trace.Write("Module: GS_SMPartsCalc.getPowerSupplyParts Error:".format(str(e)))
    return parts_dict

#parts_dict={}
def get_identifier_RG(Product,parts_dict):
    if Product.Name=="SM Remote Group":
        Enclosure_Type=Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue 
        if Enclosure_Type == "Universal Safety Cab-1.3M":
            Specify_Identifier=Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Specify_Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').DisplayValue
            Material_Type_Ingress=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Cabinet_Material_Type_Ingress_Protection').DisplayValue
            S300=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('S300').DisplayValue
            PUIO_Count=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('PUIO_Count').DisplayValue
            PDIO_Count=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('PDIO_Count').DisplayValue
            IO_Redundancy=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('IO_Redundancy').DisplayValue
            Power_Supply_Type=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Power_Supply_Type').DisplayValue
            Power_Supply_Redundancy=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Power_Supply_Redundancy').DisplayValue
            Ambient_Temperature_Range=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Ambient_Temperature_Range').DisplayValue
            Field_for_PUIO=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PUIO').DisplayValue
            Field_for_PDIO=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Field_Termination_Assembly_for_PDIO').DisplayValue
            Abu_Dhabi=Product.GetContainerByName('SM_SC_Universal_Safety_Cab_1_3M_Details_cont').Rows[0].GetColumnByName('Abu_Dhabi_Build_Loc').DisplayValue
            try:
                Identifier_Modifier=Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Identifier_Modifier_for_SM_SC_Universal_Safety_Cabinet').Value
                Trace.Write(Identifier_Modifier)
            except:
                Identifier_Modifier=0
            Safety_Cabinets_qnt=Product.GetContainerByName('SM_RG_Universal_Safety_Cabinet_1.3M_Cont').Rows[0].GetColumnByName('Number_of_SM_SC_1.3M_Universal_Safety_Cabinets_(0-63)').Value
            if Safety_Cabinets_qnt !='':
                Safety_Cabinets_qnt=int(Safety_Cabinets_qnt)
            else:
                Safety_Cabinets_qnt=0
            if len(Identifier_Modifier)>20 and Specify_Identifier=="Yes" and Safety_Cabinets_qnt >0:
                if (Identifier_Modifier[3]=="S" or Identifier_Modifier[3]=="X") and Identifier_Modifier[13]=="R":
                    var=0
                    if (Identifier_Modifier[5]=="I") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="X": #1
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[5]=="I" or Identifier_Modifier[5]== "C") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="X": #3
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[5]=="I") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="X": #5
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[5]=="I") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #7
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[5]=="I" or Identifier_Modifier[5]=="C") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #9
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[6]=="I" or Identifier_Modifier[6]=="A" or Identifier_Modifier[6]=="B") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="C": #11
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[5]=="I") and (Identifier_Modifier[6]=="C" or Identifier_Modifier[6]=="I") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #13
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="I") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #15
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[5]=="I" or Identifier_Modifier[5]=="C") and (Identifier_Modifier[6]=="U" or Identifier_Modifier[6]=="I") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #17
                        var= Safety_Cabinets_qnt * 1
                    if Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #19
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[6]=="I") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="A": #21
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[6]=="I" or Identifier_Modifier[6]=="C") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="B": #23
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[5]=="I") and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #25
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="I" or Identifier_Modifier[6]=="C") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #27
                        var= Safety_Cabinets_qnt * 1
                    if (Identifier_Modifier[5]=="I" or Identifier_Modifier[5]=="A" or Identifier_Modifier[5]=="B") and Identifier_Modifier[8]=="C" and Identifier_Modifier[9]=="X": #29
                        var= Safety_Cabinets_qnt * 1
                    parts_dict["51196426-100"] = {"Quantity" : int(var), "Description" : "Din Rail, 39 INCH"}
                elif (Identifier_Modifier[3]=="S" or Identifier_Modifier[3]=="X" or Identifier_Modifier[3]=="N") and Identifier_Modifier[13]=="X":
                    var=0
                    if (Identifier_Modifier[5]=="I") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="X": #2
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[5]=="I" or Identifier_Modifier[5]=="C") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="X": #4
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[5]=="I") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #6
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[5]=="I") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #8
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[5]=="I" or Identifier_Modifier[5]=="C") and (Identifier_Modifier[6]=="M") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #10
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[6]=="I" or Identifier_Modifier[6]=="A" or Identifier_Modifier[6]=="B") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="C": #12
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[5]=="I") and (Identifier_Modifier[6]=="C" or Identifier_Modifier[6]=="I") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #14
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="I") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #16
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[5]=="I" or Identifier_Modifier[5]=="C") and (Identifier_Modifier[6]=="U" or Identifier_Modifier[6]=="I") and Identifier_Modifier[8]=="B" and Identifier_Modifier[9]=="A": #18
                        var= Safety_Cabinets_qnt * 1
                    elif Identifier_Modifier[5]=="M" and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #20
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[6]=="I") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="A": #22
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[6]=="I" or Identifier_Modifier[6]=="C") and Identifier_Modifier[8]=="X" and Identifier_Modifier[9]=="B": #24
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[5]=="I") and Identifier_Modifier[6]=="I" and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="A": #26
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[5]=="M") and (Identifier_Modifier[6]=="I" or Identifier_Modifier[6]=="C") and Identifier_Modifier[8]=="A" and Identifier_Modifier[9]=="B": #28
                        var= Safety_Cabinets_qnt * 1
                    elif (Identifier_Modifier[5]=="I" or Identifier_Modifier[5]=="A" or Identifier_Modifier[5]=="B") and Identifier_Modifier[8]=="C" and Identifier_Modifier[9]=="X": #30
                        var= Safety_Cabinets_qnt * 1
                    parts_dict["51196426-100"] = {"Quantity" : int(var), "Description" : "Din Rail, 39 INCH"}
            elif Specify_Identifier=="No" and (S300=="Redundant S300" or S300=="No S300") and IO_Redundancy=="Redundant IO" and Safety_Cabinets_qnt >0:
                var=0
                if Field_for_PUIO=="Intrinsically Safe" and (PUIO_Count=="32")and PDIO_Count=="0": #1
                    var= Safety_Cabinets_qnt
                elif (Field_for_PUIO=="32 IS, 32 Non-IS" or Field_for_PUIO=="Intrinsically Safe") and (PUIO_Count=="64")and PDIO_Count=="0": #3
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO=="Intrinsically Safe" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52" and (PUIO_Count=="32")and PDIO_Count=="0": #5
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO=="Intrinsically Safe" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52"  and (PUIO_Count=="32")and PDIO_Count=="64": #7
                    var= Safety_Cabinets_qnt
                elif (Field_for_PUIO=="32 IS, 32 Non-IS" or Field_for_PUIO=="Intrinsically Safe") and Field_for_PDIO=="Default Marshalling FC-TDIO51/52"  and (PUIO_Count=="64")and PDIO_Count=="32": #9
                    var= Safety_Cabinets_qnt
                elif (Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 64 Non-IS" or Field_for_PDIO=="64 IS, 32 Non-IS") and (PUIO_Count=="0")and PDIO_Count=="96": #11
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO=="Intrinsically Safe" and (Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and (PUIO_Count=="32")and PDIO_Count=="64": #13
                    var= Safety_Cabinets_qnt
                elif (Field_for_PDIO=="Intrinsically Safe") and Field_for_PUIO=="Default Marshalling FC-TUIO51/52"  and (PUIO_Count=="64")and PDIO_Count=="32": #15
                    var= Safety_Cabinets_qnt
                elif (Field_for_PUIO=="32 IS, 32 Non-IS" or Field_for_PUIO=="Intrinsically Safe" or Field_for_PUIO=="Universal Marshalling, PTA") and (Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="Universal Marshalling, PTA") and (PUIO_Count=="64")and PDIO_Count=="32": #17
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" and (PUIO_Count=="32")and PDIO_Count=="32": #19
                    var= Safety_Cabinets_qnt
                elif Field_for_PDIO=="Intrinsically Safe" and (PUIO_Count=="0")and PDIO_Count=="32": #21
                    var= Safety_Cabinets_qnt
                elif (Field_for_PDIO=="32 IS, 32 Non-IS" or Field_for_PDIO=="Intrinsically Safe") and (PUIO_Count=="0")and PDIO_Count=="64": #23
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="32": #25
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52"  and (Field_for_PDIO=="32 IS, 32 Non-IS" or Field_for_PDIO=="Intrinsically Safe") and PUIO_Count=="32" and PDIO_Count=="64": #27
                    var= Safety_Cabinets_qnt
                elif (Field_for_PUIO =="Intrinsically Safe" or Field_for_PUIO =="32 IS, 64 Non-IS" or Field_for_PUIO =="64 IS, 32 Non-IS") and PUIO_Count=="96" and PDIO_Count=="0": #29
                    var= Safety_Cabinets_qnt
                parts_dict["51196426-100"] = {"Quantity" : int(var), "Description" : "Din Rail, 39 INCH"}
            elif Specify_Identifier=="No" and (S300=="Redundant S300" or S300=="No S300" or S300=="Non Redundant S300") and IO_Redundancy=="Non Redundant IO" and Safety_Cabinets_qnt !='' and Safety_Cabinets_qnt >0:
                var=0
                if Field_for_PUIO=="Intrinsically Safe" and (PUIO_Count=="32")and PDIO_Count=="0": #2
                    var= Safety_Cabinets_qnt
                elif (Field_for_PUIO=="32 IS, 32 Non-IS" or Field_for_PUIO=="Intrinsically Safe") and (PUIO_Count=="64")and PDIO_Count=="0": #4
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO=="Intrinsically Safe" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52"  and (PUIO_Count=="32")and PDIO_Count=="32": #6
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO=="Intrinsically Safe" and Field_for_PDIO=="Default Marshalling FC-TDIO51/52"  and (PUIO_Count=="32")and PDIO_Count=="64": #8
                    var= Safety_Cabinets_qnt
                elif (Field_for_PUIO=="32 IS, 32 Non-IS" or Field_for_PUIO=="Intrinsically Safe") and Field_for_PDIO=="Default Marshalling FC-TDIO51/52"  and (PUIO_Count=="64")and PDIO_Count=="32": #10
                    var= Safety_Cabinets_qnt
                elif (Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 64 Non-IS" or Field_for_PDIO=="64 IS, 32 Non-IS") and (PUIO_Count=="0")and PDIO_Count=="96": #12
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO=="Intrinsically Safe" and (Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and (PUIO_Count=="32")and PDIO_Count=="64": #14
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" and (PUIO_Count=="64")and PDIO_Count=="32": #16
                    var= Safety_Cabinets_qnt
                elif (Field_for_PUIO=="32 IS, 32 Non-IS" or Field_for_PUIO=="Intrinsically Safe") and Field_for_PDIO=="Universal Marshalling, PTA" and (PUIO_Count=="64")and PDIO_Count=="32": #18
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO=="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" and (PUIO_Count=="32")and PDIO_Count=="32": #20
                    var= Safety_Cabinets_qnt
                elif Field_for_PDIO=="Intrinsically Safe"  and (PUIO_Count=="0")and PDIO_Count=="32": #22
                    var= Safety_Cabinets_qnt
                elif (Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS") and (PUIO_Count=="0")and PDIO_Count=="64": #24
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO =="Intrinsically Safe" and Field_for_PDIO=="Intrinsically Safe" and PUIO_Count=="32" and PDIO_Count=="32": #26
                    var= Safety_Cabinets_qnt
                elif Field_for_PUIO =="Default Marshalling FC-TUIO51/52" and Field_for_PDIO=="Intrinsically Safe" or Field_for_PDIO=="32 IS, 32 Non-IS" and PUIO_Count=="32" and PDIO_Count=="64": #28
                    var= Safety_Cabinets_qnt
                elif (Field_for_PUIO =="Intrinsically Safe" or Field_for_PUIO =="32 IS, 64 Non-IS" or Field_for_PUIO =="64 IS, 32 Non-IS") and PUIO_Count=="96" and PDIO_Count=="0": #30
                    var= Safety_Cabinets_qnt
                parts_dict["51196426-100"] = {"Quantity" : int(var), "Description" : "Din Rail, 39 INCH"}
	return parts_dict

def getFieldSum(attrs, fields):
    res = 0
    for field in fields:
        res += try_get_int_attr(attrs, field, 0)
    return res

def getIntermediateCalcDict(attrs):
    calcDict = {
        "a" : [
            "sdi1_uio_rd_sil3_rly",
            "sdi1_uio_rd_nmr",
            "sdi1_uio_rd_nmr_safety",
            "sdo1_uio_rd_sil3_rly",
            "sdi1_5k_resistor_uio_rd_nis",
            "sdi1_5k_resistor_uio_rd_rly",
            "sdi1_uio_rd_rly",
            "sdo1_uio_rd_rly"
        ],
        "b" : [
            "sdi1_uio_nrd_sil3_rly",
            "sdi1_uio_nrd_nmr",
            "sdi1_uio_nrd_nmr_safety",
            "sdo1_uio_nrd_sil3_rly",
            "sdi1_5k_resistor_uio_nrd_nis",
            "sdi1_5k_resistor_uio_nrd_rly",
            "sdi1_uio_nrd_rly",
            "sdo1_uio_nrd_rly"
        ],
        "c" : [
            "sdi1_dio_rd_sil3_rly",
            "sdi1_dio_rd_nmr",
            "sdi1_dio_rd_nmr_safety",
            "sdo1_dio_rd_sil3_rly",
            "sdi1_5k_resistor_dio_rd_nis",
            "sdi1_5k_resistor_dio_rd_rly"
        ],
        "d" : [
            "sdi1_dio_nrd_sil3_rly",
            "sdi1_dio_nrd_nmr",
            "sdi1_dio_nrd_nmr_safety",
            "sdo1_dio_nrd_sil3_rly",
            "sdi1_5k_resistor_dio_nrd_nis",
            "sdi1_5k_resistor_dio_nrd_rly"
        ],
        "e" : [
            "sdo1_uio_rd_sil2_rly",
            "sai1_uio_rd_nis",
            "sai1_fire2_wire_uio_rd_nis",
            "sai1_gas_uio_rd_nis",
            "sao1_uio_rd_nis",
            "sdi1_uio_rd_nis",
            "sdi1_line_mon_uio_rd_nis",
            "sdo1_uio_rd_nis",
            "sdo2_1a_uio_rd_nis",
            "sdo4_2a_uio_rd_nis",
            "sdo7_line_mon_uio_rd_nis",
            "sdo16_sil23_uio_rd_nis",
            "sdo12_sil23_com_uio_rd_nis",
            "sai1_fire34_wire_uio_rd_nis",
            "sai1_fire34_wire_sink_uio_rd_nis"
        ],
        "f" : [
            "sdo1_uio_nrd_sil2_rly",
            "sai1_uio_nrd_nis",
            "sai1_fire2_wire_uio_nrd_nis",
            "sai1_gas_uio_nrd_nis",
            "sao1_uio_nrd_nis",
            "sdi1_uio_nrd_nis",
            "sdi1_line_mon_uio_nrd_nis",
            "sdo1_uio_nrd_nis",
            "sdo2_1a_uio_nrd_nis",
            "sdo4_2a_uio_nrd_nis",
            "sdo7_line_mon_uio_nrd_nis",
            "sdo16_sil23_uio_nrd_nis",
            "sdo12_sil23_com_uio_nrd_nis",
            "sai1_fire34_wire_uio_nrd_nis",
            "sai1_fire34_wire_sink_uio_nrd_nis"
        ],
        "g" : [
            "sdo1_dio_rd_sil2_rly",
            "sdi1_dio_rd_nis",
            "sdi1_line_mon_dio_rd_nis",
            "sdo1_dio_rd_nis",
            "sdo16_sil23_dio_rd_nis",
            "sdo16_sil23_com_dio_rd_nis"
        ],
        "h" : [
            "sdo1_dio_nrd_sil2_rly",
            "sdi1_dio_nrd_nis",
            "sdi1_line_mon_dio_nrd_nis",
            "sdo1_dio_nrd_nis",
            "sdo16_sil23_dio_nrd_nis",
            "sdo16_sil23_com_dio_nrd_nis"
        ],
        "i" : [
            "sai1_uio_rd_is",
            "sai1_fire2_wire_uio_rd_is",
            "sai1_fire34_wire_uio_rd_is",
            "sai1_fire34_wire_sink_uio_rd_is",
            "sai1_gas_uio_rd_is",
            "sao1_uio_rd_is",
            "sdi1_uio_rd_is",
            "sdi1_line_mon_uio_rd_is",
            "sdo1_uio_rd_is",
            "sdo2_1a_uio_rd_is",
            "sdo4_2a_uio_rd_is",
            "sdo7_line_mon_uio_rd_is"
        ],
        "j" : [
            "sai1_uio_nrd_is",
            "sai1_fire2_wire_uio_nrd_is",
            "sai1_fire34_wire_uio_nrd_is",
            "sai1_fire34_wire_sink_uio_nrd_is",
            "sai1_gas_uio_nrd_is",
            "sao1_uio_nrd_is",
            "sdi1_uio_nrd_is",
            "sdi1_line_mon_uio_nrd_is",
            "sdo1_uio_nrd_is",
            "sdo2_1a_uio_nrd_is",
            "sdo4_2a_uio_nrd_is",
            "sdo7_line_mon_uio_nrd_is"
        ],
        "k" : [
            "sdi1_dio_rd_is",
            "sdi1_line_mon_dio_rd_is",
            "sdo1_dio_rd_is"
        ],
        "l" : [
            "sdi1_dio_nrd_is",
            "sdi1_line_mon_dio_nrd_is",
            "sdo1_dio_nrd_is"
        ]
    }
    responseDict = dict()
    spare = (100 + try_get_int_attr(attrs, "marshalling_percent_spare_io", 0)) / 100.00
    for key, fields in calcDict.items():
        responseDict[key] = ceil((spare * getFieldSum(attrs, fields)) / 16.00)
    return responseDict

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