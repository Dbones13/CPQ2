import datetime
import math as m
def getFloat(Var):
    if Var:
        return float(Var)
    else:
        return 0

def scadalabor(Product):
    Number_of_Control_Rooms = getFloat(Product.Attr('Scada_Number_of_Control_Rooms').GetValue())
    Number_of_Distinct_Equipment_Templates = getFloat(Product.Attr('Scada_Number_of_Distinct_Equipment_Templates').GetValue())
    Development_of_any_custom_applications = Product.Attr('Scada_Development_of_any_custom_applications').GetValue()
    Telecommunications_infrastructure_review = Product.Attr('Scada_Telecommunications_infrastructure_review').GetValue()
    Are_there_unknown_or_unfamilar_protocols = Product.Attr('Scada_Are_there_unknown_or_unfamilar_protocols').GetValue()
    Are_migration_of_existing_SCADA_System = Product.Attr('Scada_Are_migration_of_existing_SCADA_System').GetValue()
    Is_SCADA_System_Interface_with_Enterprise = Product.Attr('Scada_Is_SCADA_System_Interface_with_Enterprise').GetValue()
    Development_of_Custom_Standards = Product.Attr('Scada_Development_of_Custom_Standards').GetValue()
    Site_Survey_Required = Product.Attr('Is Site Survey Required').GetValue()

    ss = 1 if(Site_Survey_Required == "Yes") else 0
    cm_sa = ("Simple" if(Number_of_Control_Rooms == 1) else ("Medium" if(Number_of_Control_Rooms == 2) else ("Complex" if(Number_of_Control_Rooms == 3) else "Simple")))
    np_complex = ("Simple" if(Number_of_Distinct_Equipment_Templates<=15) else ("Medium" if(Number_of_Distinct_Equipment_Templates>15 and Number_of_Distinct_Equipment_Templates<30) else ("Complex" if(Number_of_Distinct_Equipment_Templates>30) else "Simple")))
    cm_cust= "Simple" if(Development_of_any_custom_applications == "No") else ("Medium" if(Development_of_any_custom_applications == "Yes, but it is familiar") else ("Complex") if(Development_of_any_custom_applications == "Yes and it is unfaliliar") else "Simple")
    cm_tl= "Simple" if(Telecommunications_infrastructure_review == "No") else ("Medium" if(Telecommunications_infrastructure_review == "Yes (One Telco involved OR infrastructure is NOT obsolete)") else ("Complex") if(Telecommunications_infrastructure_review == "Yes (Multiple Telco involved OR infrastructure is obsolete)") else "Simple")
    cm_pr = "Simple" if(Are_there_unknown_or_unfamilar_protocols == "No") else("Complex" if(Are_there_unknown_or_unfamilar_protocols == "Yes") else "Simple")
    cm_gr = "Simple" if(Are_migration_of_existing_SCADA_System == "No") else("Complex" if(Are_migration_of_existing_SCADA_System == "Yes") else "Simple")
    cm_apps = "Simple" if(Is_SCADA_System_Interface_with_Enterprise == "No") else("Complex" if(Is_SCADA_System_Interface_with_Enterprise == "Yes") else "Simple")
    cm_std = "Simple" if(Development_of_Custom_Standards == "Use Existing or Honeywell Standard") else("Complex" if(Development_of_Custom_Standards == "Custom Standards to be Developed") else "Simple")

    list = [cm_sa, np_complex, cm_cust,cm_tl,cm_pr,cm_gr,cm_apps,cm_std]
    Simple = 0
    Medium = 0
    Complex = 0
    for i in list:
        if i == "Simple":
            Simple = Simple + 1
        if i == "Medium":
            Medium = Medium + 1
        if i == "Complex":
            Complex = Complex + 1
    cm_calc = 3 if(Complex>0) else (2 if(Medium>0) else 1)
    CM = cm_calc
    #=ss*(IF(CM=1,40,IF(CM=2,60,IF(CM=3,80,0))))
    scada_site_survey_report = (40 if(CM == 1) else (60 if(CM == 2) else (80 if(CM == 3) else 0)) ) * ss

    # SCADA DS
    scada_ds = 80 if(CM == 1) else (160 if(CM == 2) else 320)

    # SADA SPECIALS
    Number_of_New_Simple_Equipment_Templates = getFloat(Product.Attr('Scada_Number_of_New_Simple_Equipment_Templates').GetValue())
    Number_of_New_Medium_Equipment_Templates = getFloat(Product.Attr('Scada_Number_of_New_Medium_Equipment_Templates').GetValue())
    Number_of_New_Complex_Equipment_Templates = getFloat(Product.Attr('Scada_Number_of_New_Complex_Equipment_Templates').GetValue())
    Scada_Includes_Elevate = Product.Attr('Scada_Includes_Elevate').GetValue()
    CL = 1 if(Scada_Includes_Elevate == "Yes") else 0

    sp_s = m.ceil((Number_of_Distinct_Equipment_Templates * Number_of_New_Simple_Equipment_Templates)/100)
    sp_m = m.ceil((Number_of_Distinct_Equipment_Templates * Number_of_New_Medium_Equipment_Templates)/100)
    sp_c = m.ceil((Number_of_Distinct_Equipment_Templates * Number_of_New_Complex_Equipment_Templates)/100)
    #=(((sp_s*0.1)+(sp_m*0.2)+(sp_c*1))*40)+(IF(sp_s>0,(sp_s*CL*2),0))+(IF(sp_m>0,(sp_m*CL*4),0))+(IF(sp_c>0,(sp_c*CL*8),0))

    scada_special1 = (sp_s*CL*2) if(sp_s>0) else 0
    scada_special2 = (sp_m*CL*4) if(sp_m>0) else 0
    scada_special3 = (sp_c*CL*8) if(sp_c>0) else 0
    scada_special = (((sp_s*0.1)+(sp_m*0.2)+(sp_c*1))*40) + scada_special1 + scada_special2 + scada_special3
    #Trace.Write(sp_s)
    # SCADA ORDER= IF(CL=1, (8 + (8*CM)), 0)
    scada_order = (8 + (8*CM)) if(CL == 1) else 0

    #SCADA app build =(NP * 1) + (NC * 0.025)    NP     NC
    NP = Number_of_Distinct_Equipment_Templates
    NC = getFloat(Product.Attr('Scada_Number_of_Instances').GetValue())
    scada_app_build = (NP * 1) + (NC * 0.025)
    #=(it*(it_sb*40)+(2+(i*0.5))) + ((pft_sb*0.25*40)*(2+(0.25*((pf_p*NP)+(pf_c*NC))))) + ((ft_sb*0.25*40)*(2+(0.25*((f_p*NP)+(f_c*NC))))) + (CL*6)
    #SCADA TEST
    Is_Integration_Testing_Required = Product.Attr('Scada_Is_Integration_Testing_Required').GetValue()
    it = 1 if(Is_Integration_Testing_Required == "Yes") else 0
    Usage_for_Integration_Test = Product.Attr('Scada_Standard_Build_Usage_for_Integration_Test_Plan').GetValue()
    it_sb = 1 if(Usage_for_Integration_Test == "Less than 25% change from SB") else (2 if(Usage_for_Integration_Test == "Between 25% to 75% change from SB") else (4 if(Usage_for_Integration_Test == "More than 75% change from SB") else 1))
    i = getFloat(Product.Attr('Scada_Number_of_Third_Party_Interface_to_test').GetValue())
    i_setup = 2
    Usage_for_Pre_FAT_Test_Plan = Product.Attr('Scada_Standard_Build_Usage_for_Pre_FAT_Test_Plan').GetValue()
    pft_sb = 1 if(Usage_for_Pre_FAT_Test_Plan == "Less than 25% change from SB") else (2 if(Usage_for_Pre_FAT_Test_Plan == "Between 25% to 75% change from SB") else (4 if(Usage_for_Pre_FAT_Test_Plan == "More than 75% change from SB") else 1))
    pf_setup = 2
    pf_p = getFloat(Product.Attr('Scada_%_of_Equip_Template_to_be_Tested_During_Pre_FAT').GetValue()) / 100
    pf_c = getFloat(Product.Attr('Scada_%_of_Instances_to_be_Tested_During_Pre_FAT').GetValue()) / 100

    Usage_for_FAT_Test_Plan = Product.Attr('Scada_Standard_Build_Usage_for_FAT_Test_Plan').GetValue()
    ft_sb = 1 if(Usage_for_FAT_Test_Plan == "Less than 25% change from SB") else (2 if(Usage_for_FAT_Test_Plan == "Between 25% to 75% change from SB") else (4 if(Usage_for_FAT_Test_Plan == "More than 75% change from SB") else 1))
    f_setup = 2
    f_p = getFloat(Product.Attr('Scada_%_of_Equipment_Templates_to_be_Tested_During_FAT').GetValue()) / 100
    f_c = getFloat(Product.Attr('Scada_%_of_Instances_to_be_Tested_During_FAT').GetValue()) / 100


    scada_test = (it*(it_sb*40)+(2+(i*0.5))) + ((pft_sb*0.25*40)*(2+(0.25*((pf_p*NP)+(pf_c*NC))))) + ((ft_sb*0.25*40)*(2+(0.25*((f_p*NP)+(f_c*NC))))) + (CL*6)
    #scada sat
    Site_Survey_Required = Product.Attr('Labor_Site_Activities').GetValue()
    sat = 1 if(Site_Survey_Required == "Yes") else 0
    #sat =1
    sat_travel = 0.25
    Usage_for_SAT_Test_Plan = Product.Attr('Scada_Standard_Build_Usage_for_SAT_Test_Plan').GetValue()
    sat_sb = 1 if(Usage_for_SAT_Test_Plan == "Less than 25% change from SB") else (2 if(Usage_for_SAT_Test_Plan == "Between 25% to 75% change from SB") else (4 if(Usage_for_SAT_Test_Plan == "More than 75% change from SB") else 1))
    sat_p = getFloat(Product.Attr('Scada_%_of_Equipment_Templates_to_be_Tested_During_SAT').GetValue()) / 100
    sat_c = getFloat(Product.Attr('Scada_%_of_Instances_to_be_Tested_During_SAT').GetValue()) / 100
    scada_sat = sat * (( (sat_sb *0.25 * 40 )) + ( 0.25 * ( ( sat_p * NP ) + (sat_c * NC) +  sat_travel ) ) + ( CL * 6 ) )
    #dic_deliverable = {"scada_sat":scada_sat, "scada_site_survey_report":scada_site_survey_report, "scada_ds":scada_ds, "scada_special":scada_special, "scada_order":scada_order, "scada_app_build": scada_app_build, "scada_test":scada_test}
    #return dic_deliverable
    return scada_sat, scada_site_survey_report, scada_ds, scada_special, scada_order, scada_app_build, scada_test