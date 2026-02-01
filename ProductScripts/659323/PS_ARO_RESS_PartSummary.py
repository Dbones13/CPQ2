import GS_PS_Exp_Ent_BOM
import GS_Get_Set_AtvQty
import GS_ARO_RESS_ConfigParts,GS_ARO_RESS_ConfigParts1
Product.ExecuteRulesOnce = True
Qty_Station_Client=Product.Attr('ERG Read-Only Station Client Licenses (1-40)').GetValue()
Users_Devices_requiring_access=Product.Attr('Number of Users/ Devices requiring access (0- 500)').GetValue()
RDS_CAL_type=Product.Attr('RDS CAL type').GetValue()
Soft_Release=Product.Attr('ERG_Software_Release').GetValue()
EP_T10CAL=0
EP_T09CAL=0

product_type=Product.Attr('New_Expansion').GetValue()
#CXCPQ-112863
qty24dell,qty27dell,qty24NEC,qty27NEC=GS_ARO_RESS_ConfigParts1.Aro_Display_Parts(Product)

ARO_System_Required=Product.Attr('ARO_System_Required').GetValue()
if product_type=="Expansion" and ARO_System_Required=="Yes":
    Aro_flex_station_license=int(Product.Attr('ARO_existing_Flex_station_license').GetValue() or 0)
    Aro_flex_station_license_required=int(Product.Attr('ARO_new_Flex_Station_licenses_required').GetValue() or 0)
    Aro_console_station_license=int(Product.Attr('ARO_new_Console_Station_Extension_License').GetValue() or 0)
    RESS_existing_flex_station_license=int(Product.Attr('RESS_existing_Flex_station_license').GetValue() or 0)
    RESS_existing_flex_station_license_required=int(Product.Attr('RESS_new_Flex_Station_licenses_required').GetValue() or 0)
    RESS_console_station_license_required=int(Product.Attr('RESS_new_Console_Station_Extension_License').GetValue() or 0)
    Total_license=Aro_flex_station_license+Aro_flex_station_license_required+Aro_console_station_license+RESS_existing_flex_station_license+RESS_existing_flex_station_license_required+RESS_console_station_license_required
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-T09CAL",Total_license)
else:
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-T09CAL",0)
    

if Qty_Station_Client!="":
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-ERGB01",1)
	GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-ERGCR1",int(Qty_Station_Client))
else:
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-ERGB01",0)
    GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-ERGCR1",0)
    
if Soft_Release=="R530" and int(Users_Devices_requiring_access)>0:
    if RDS_CAL_type=="Per user CALs":
        EP_T10CAL=int(Users_Devices_requiring_access)
    elif RDS_CAL_type=="Per device CALs":
        EP_T09CAL=int(Users_Devices_requiring_access)
        
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-T10CAL",EP_T10CAL)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-T09CAL",EP_T09CAL)

#CXCPQ-112914
Qty_EPCOAW21=GS_ARO_RESS_ConfigParts1.getpart_EPCOAW21(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-COAW21",Qty_EPCOAW21)
#CXCPQ-112914

Qty=GS_ARO_RESS_ConfigParts.getpart_TPFPW271(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-FPW271",Qty+qty27NEC)
Qty1=GS_ARO_RESS_ConfigParts.getpart_MZPCWS94(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCWS94",Qty1)
Qty2=GS_ARO_RESS_ConfigParts.getpart_MZPCWS14(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCWS14",Qty2)
Qty3=GS_ARO_RESS_ConfigParts.getpart_MZPCWS84(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCWS84",Qty3)
Qty4=GS_ARO_RESS_ConfigParts.getpart_EPCOAW10(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-COAW10",Qty4)
Qty5=GS_ARO_RESS_ConfigParts.getpart_TPFPD211200(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-FPD211-200",Qty5)
Qty6=GS_ARO_RESS_ConfigParts.getpart_TPFPD211100(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-FPD211-100",Qty6)
Qty7=GS_ARO_RESS_ConfigParts.getpart_TPFPW231(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-FPW231",Qty7)
#Qty8=GS_ARO_RESS_ConfigParts.getpart_MZPCSR02(Product)
#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSR02",Qty8)
Qty9=GS_ARO_RESS_ConfigParts.getpart_TPFPW241(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-FPW241",Qty9+qty24NEC)
#Qty10=GS_ARO_RESS_ConfigParts.getpart_MZPCST01(Product)
#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCST01",Qty10)
#Qty_PCST81=GS_ARO_RESS_ConfigParts.getpart_MZPCST81(Product)
#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCST81",Qty_PCST81)
Qty11=GS_ARO_RESS_ConfigParts.getpart_EPCOAW19(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-COAW19",Qty11)
Qty12=GS_ARO_RESS_ConfigParts.getpart_MZPCSV65(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSV65",Qty12)
#Qty13=GS_ARO_RESS_ConfigParts.getpart_MZPCST82(Product)
#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCST82",Qty13)
Qty14=GS_ARO_RESS_ConfigParts.getpart_MZPCWS77(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCWS77",Qty14)
#Qty15=GS_ARO_RESS_ConfigParts.getpart_MZPCSR82(Product)
#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSR82",Qty15)
Qty16=GS_ARO_RESS_ConfigParts.getpart_MZPCSV84(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSV84",Qty16)
Qty17=GS_ARO_RESS_ConfigParts.getpart_MZPCIS02(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCIS02",Qty17)
Qty18=GS_ARO_RESS_ConfigParts.getpart_EPCOAS19(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-COAS19",Qty18)
Qty19=GS_ARO_RESS_ConfigParts1.getpart_EPCOAS16(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-COAS16",Qty19)
Qty20=GS_ARO_RESS_ConfigParts1.getpart_MZSQLCL4(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-SQLCL4",Qty20)
Qty21=GS_ARO_RESS_ConfigParts1.getpart_TPFPW272(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-FPW272",Qty21+qty27dell)
EP_PKS530_ESD,EP_PKS530,EP_BRM520_ESD,EP_BRM520=GS_ARO_RESS_ConfigParts1.getpart_EP(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-PKS530-ESD",EP_PKS530_ESD)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-PKS530",EP_PKS530)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-BRM520-ESD",EP_BRM520_ESD)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-BRM520",EP_BRM520)
#MZ_PCSR01,MZ_PCSR81=GS_ARO_RESS_ConfigParts1.getpart_MZ_PCSR01_PCSR81(Product)
#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSR01",MZ_PCSR01)
#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSR81",MZ_PCSR81)
Qty22=GS_ARO_RESS_ConfigParts.getpart_EPCOAS22(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-COAS22",Qty22)
#Qty23=GS_ARO_RESS_ConfigParts.getpart_MZPCSR03(Product) # 40K Limit
Qty23=GS_ARO_RESS_ConfigParts1.getpart_MZPCSR03(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSR03",Qty23)
Qty24=GS_ARO_RESS_ConfigParts1.getpart_TPFPW242(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-FPW242",Qty24+qty24dell)
Qty25=GS_ARO_RESS_ConfigParts1.getpart_EPBRSE06(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-BRSE06",Qty25)
#Qty26=GS_ARO_RESS_ConfigParts.getpart_MZPCST02(Product)
#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCST02",Qty26)

MZ_PCSR05,MZ_PCSR06,MZ_PCST03,MZ_PCST04,MZ_PCSR04,MZ_PCSV85=GS_ARO_RESS_ConfigParts1.getpart_server(Product) #CXCPQ-112913 MZ_PCSR04,MZ_PCSV85
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSR05",MZ_PCSR05)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSR06",MZ_PCSR06)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCST03",MZ_PCST03)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCST04",MZ_PCST04)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSR04",MZ_PCSR04) #CXCPQ-112913
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCSV85",MZ_PCSV85) #CXCPQ-112913
# CXCPQ-112864 - Starts
TPTHNR01_100,TPTHNR02_100,TPTHNCL9_100,EP_SMWIN1,TPTHNCL5_400,TP_OTP231,EP_OCOTP1,EP_STAT10,EP_STAT05,EP_STAT01,EP_STACEX,EP_RNW000=GS_ARO_RESS_ConfigParts1.getpart_AROClients(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-THNR01-100",TPTHNR01_100)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-THNR02-100",TPTHNR02_100)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-THNCL9-100",TPTHNCL9_100)
#GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-SMWIN1",EP_SMWIN1) # CXCPQ-112916 - removed and summed up below
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-OTP231",TP_OTP231) # CXCPQ-112918
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","TP-THNCL5-400",TPTHNCL5_400) # CXCPQ-112918
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-OCOTP1",EP_OCOTP1) # CXCPQ-112918
# CXCPQ-112864 - Ends
#CXCPQ-112865 - Starts
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-STAT10",EP_STAT10)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-STAT05",EP_STAT05)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-STAT01",EP_STAT01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-STACEX",EP_STACEX)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-RNW000",EP_RNW000)
#CXCPQ-112865 - Ends
# CXCPQ-112916 Start
MZ_PCWT01, MZ_PCWR01, MZ_PCWS86, MZ_PCWS15 = GS_ARO_RESS_ConfigParts1.getpart_RESSClients(Product)
EP_SMWIN1_RESS = GS_ARO_RESS_ConfigParts1.getpart_RESSDisplays(Product)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCWT01",MZ_PCWT01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCWR01",MZ_PCWR01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCWS86",MZ_PCWS86)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","MZ-PCWS15",MZ_PCWS15)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"ARO_Sys_Grp_Part_Summary","EP-SMWIN1",EP_SMWIN1+EP_SMWIN1_RESS)
# CXCPQ-112916 End

Product.ApplyRules()
Product.ExecuteRulesOnce = False

import GS_DropDown_Implementation
GS_DropDown_Implementation.SetDropDownDefaultvalue(Product)