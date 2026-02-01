import GS_PS_Exp_Ent_BOM
Product.ExecuteRulesOnce = True

Terminal_Media_kit_required=Product.Attr('Terminal_Media_kit_required').GetValue()
Terminal_SAP_ERP_BSI_Interface_required=Product.Attr('Terminal_SAP_ERP_BSI_Interface_required?').GetValue()
Terminal_Experion_Client_PC=Product.Attr('Terminal_Experion_Client_PC').GetValue()
Terminal_to_be_integrated_at_Enterprise_level=int(Product.Attr('Terminal_to_be_integrated_at_Enterprise_level').GetValue() or 0)
Terminal_Experion_Server_Hardware=Product.Attr('Terminal_Experion_Server_Hardware').GetValue()
Hazardous_Material_Support=Product.Attr('Hazardous_Material_Support').GetValue()
Aramco_Support=Product.Attr('Aramco_Support').GetValue()
Prod_Demand_Forecasting=Product.Attr('Prod_Demand_Forecasting').GetValue()
Mobile_UI=Product.Attr('Mobile_UI').GetValue()
Analytics=Product.Attr('Analytics').GetValue()
Visual_Display_Unit=Product.Attr('Visual_Display_Unit').GetValue()
SMS_Functionality=Product.Attr('SMS_Functionality').GetValue()
Tank_farm_management_system=Product.Attr('Tank_farm_management_system').GetValue()
Biometric_device=Product.Attr('Biometric_device').GetValue()
National_oil_companies_features=Product.Attr('National_oil_companies_features').GetValue()

MZ_PCWS15=0
MZ_PCSV85=0
MZ_PCSR04=0
MZ_PCST03=0
MZ_PCST04=0
EP_COAS22=0
TM_MK710S_ESD=0
TM_MK710S=0
TM_HMLT01=0
TM_ARAMCO=0
TM_PSLT01=0
TM_MOBL01=0
TM_ANLC01=0
TM_VDUL01=0
TM_SMSL01=0
TM_TFMS01=0
TM_BIOM01=0
TM_NOCL01=0

if Terminal_Media_kit_required == "Electronic":
    TM_MK710S_ESD=1
if Terminal_Media_kit_required == "Physical":
    TM_MK710S=1
if Terminal_SAP_ERP_BSI_Interface_required =="Yes" and Terminal_Experion_Client_PC =="Tower":
    MZ_PCWS15=1
if Terminal_to_be_integrated_at_Enterprise_level > 0 :
    EP_COAS22=1
    if Terminal_Experion_Server_Hardware =="HP DL320 G11":
        MZ_PCSV85=1
    if Terminal_Experion_Server_Hardware =="DELL R760XL":
        MZ_PCSR04=1
    if Terminal_Experion_Server_Hardware =="DELL T160":
        MZ_PCST03=1
    if Terminal_Experion_Server_Hardware =="DELL T360":
        MZ_PCST04=1
if Hazardous_Material_Support=="Yes":
    TM_HMLT01=1
if Aramco_Support=="Yes":
    TM_ARAMCO=1
if Prod_Demand_Forecasting=="Yes":
    TM_PSLT01=1
if Mobile_UI=="Yes":
    TM_MOBL01=1
if Analytics=="Yes":
    TM_ANLC01=1
if Visual_Display_Unit=="Yes":
    TM_VDUL01=1
if SMS_Functionality=="Yes":
    TM_SMSL01=1
if Tank_farm_management_system=="Yes":
    TM_TFMS01=1
if Biometric_device=="Yes":
    TM_BIOM01=1
if National_oil_companies_features=="Yes":
    TM_NOCL01=1

GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-MK710S-ESD",TM_MK710S_ESD)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-MK710S",TM_MK710S)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","MZ-PCWS15",MZ_PCWS15)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","MZ-PCSV85",MZ_PCSV85)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","MZ-PCSR04",MZ_PCSR04)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","MZ-PCST03",MZ_PCST03)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","MZ-PCST04",MZ_PCST04)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","EP-COAS22",EP_COAS22)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-HMLT01",TM_HMLT01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-ARAMCO",TM_ARAMCO)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-PSLT01",TM_PSLT01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-MOBL01",TM_MOBL01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-ANLC01",TM_ANLC01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-VDUL01",TM_VDUL01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-SMSL01",TM_SMSL01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-TFMS01",TM_TFMS01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-BIOM01",TM_BIOM01)
GS_PS_Exp_Ent_BOM.setAtvQty(Product,"Terminal_Part_Summary","TM-NOCL01",TM_NOCL01)

Product.ApplyRules()
Product.ExecuteRulesOnce = False