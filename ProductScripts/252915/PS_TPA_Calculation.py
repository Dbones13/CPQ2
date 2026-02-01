import math as m
def getContainer(Name):
    return Product.GetContainerByName(Name)
def getFloat(Var):
    if Var:
        return float(Var)
    return 0

selectedProducts = list()
for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.append(row["Product Name"])
if "TPA/PMD Migration" in selectedProducts:
    VPMDSys= Product.Attr('TPA_Non-virtualized_or_virtualized_PMD_system').GetValue()
    mainMSID= Product.Attr('TPA_Is_this_the_main_MSID_system').GetValue()
    PMDserType= Product.Attr('TPA_PMD_server_type_required').GetValue()
    sepFCEcabinet= getFloat(Product.Attr('TPA_How_many_separate_FCE_cabinets_are_required').GetValue())
    separateFirewall= Product.Attr('TPA_Include_and_deliver_new_separate_Firewall_for_ICSS').GetValue()
    AmtFiberOptic= getFloat(Product.Attr('TPA_Amount_of_fiber_optic_convertters_GBICs_required').GetValue())
    ConremoteView= getFloat(Product.Attr('TPA_How_many_Concurrent_remote_view_operation_in_RHS_session').GetValue())
    sepDepart= getFloat(Product.Attr('TPA_How_many_separate_departments_systems_are_under_migration').GetValue())
    OPCcomm= getFloat(Product.Attr('TPA_How_many_existing_OPC_communication_partners_direct_to_DCS_No_PHD_available_or_data_is_not_in_PHD_or_OPC_data_is_used_for_controls').GetValue())
    MDCont= getFloat(Product.Attr('TPA_How_many_MD_control_packages_are_done_in_TPA_PMD').GetValue())
    CDCont= getFloat(Product.Attr('TPA_How_many_CD_control_packages_are_done_in_TPA_PMD').GetValue())
    NonRedFEC_DP= getFloat(Product.Attr('TPA_How_many_new_Non_Redundant_FCE_controllers_DP_are_delivered_in_migration').GetValue())
    NonRedFEC_PN= getFloat(Product.Attr('TPA_How_many_new_Non_Redundant_FCE_controllers_PN_are_delivered_in_migration').GetValue())
    RedFCE_DP= getFloat(Product.Attr('TPA_How_many_new_redundant_FCE_controllers_are_delivered_in_migration').GetValue())
    ssHMIvirt= getFloat(Product.Attr('TPA_How_many_SINGLE_screen_HMI_in_virtualized_desk_configuration_are_in_total').GetValue())
    dsHMIvirt= getFloat(Product.Attr('TPA_How_many_DUAL_screen_HMI_in_virtualized_desk_configuration_are_in_total').GetValue())
    qsHMIvirt= getFloat(Product.Attr('TPA_How_many_QUAD_screen_HMI_in_virtualized_desk_configuration_are_in_total').GetValue())
    ssHMIcab= getFloat(Product.Attr('TPA_How_many_SINGLE_screen_physical_HMI_in_CABINET_are_required').GetValue())
    dsHMIcab= getFloat(Product.Attr('TPA_How_many_DUAL_screen_physical_HMI_in_CABINET_are_required').GetValue())
    qsHMIcab= getFloat(Product.Attr('TPA_How_many_QUAD_screen_physical_HMI_in_CABINET_are_required').GetValue())
    CM_EWS= getFloat(Product.Attr('TPA_How_many_cabinet_mounted_EWS_DxMs_are_in_total').GetValue())
    VDM_EWS= getFloat(Product.Attr('TPA_How_many_virtualized_desk_mounted_EWS_DxMs_are_in_total').GetValue())
    SWI_BOU_16UIO= getFloat(Product.Attr('TPA_Total_Number_of_SWI_and_BOU_cards_to_be_replaced').GetValue())
    SWI_BOU_16UIO_UMS= getFloat(Product.Attr('TPA_Total_Number_of_SWI_and_BOU_cards_to_be_replaced_with_16_ch_UIO_and_Universal_Marshalling_Module').GetValue())
    BOU_32BO= getFloat(Product.Attr('TPA_Total_Number_of_BOU_cards_to_be_combined_replaced').GetValue())
    SWI_32BI= getFloat(Product.Attr('TPA_Total_Number_of_SWI_cards_to_be_combined_and_replaced').GetValue())
    PBI_16DI= getFloat(Product.Attr('TPA_Total_Number_of_PBI_cards_to_be_replaced').GetValue())
    PB0_8DO= getFloat(Product.Attr('TPA_Total_Number_of_PB0_cards_to_be_replaced').GetValue())
    MSI_32BI= getFloat(Product.Attr('TPA_Total_Number_of_MSI_cards_to_be_replaced').GetValue())
    MAI_ACO_16UIO= getFloat(Product.Attr('TPA_Total_Number_of_MAI_ACO_cards_to_be_replaced').GetValue())
    MAI_2x8UAI= getFloat(Product.Attr('TPA_Total_Number_of_MAI_with_active_field_AIs_to_be_replaced').GetValue())
    MAI_ACO_16UIO_UMS= getFloat(Product.Attr('TPA_Total_Number_of_MAI_and_ACO_cards_to_be_replaced_with_16_ch_UIO_and_Universal_Marshalling_Module').GetValue())

    TpaRacksReplace= getFloat(Product.Attr('TPA_Total_number_of_TPA_Racks_to_be_replaced_with_CE900').GetValue())
    UseOnlyCE900= Product.Attr('TPA_Use_only_single_CE900_rack_in_KIT_assembly').GetValue()

    OPCclient = OPCcomm +m.ceil((MDCont+CDCont)/10000)
    VirtHMIworkstn = ssHMIvirt+dsHMIvirt+qsHMIvirt if VPMDSys =="Virtualized" else 0
    VirtRHSser = m.ceil(ConremoteView/10) if VPMDSys =="Virtualized" else 0
    if VPMDSys =="Virtualized" and mainMSID =="Main MSID system" and sepDepart!=0:
        if PMDserType =="Redundant":
            VirtPMDser =2
        else:
            VirtPMDser=1
    else:
        VirtPMDser = 0
    VirtWorkstation = CM_EWS+VDM_EWS if VPMDSys =="Virtualized" else 0
    if VPMDSys =="Non Virtualized" and mainMSID =="Main MSID system" and sepDepart!=0:
        if PMDserType =="Redundant":
            Non_VirtPMDser =2
        else:
            Non_VirtPMDser=1
    else:
        Non_VirtPMDser = 0

    NetworkBasic = 1  if mainMSID =="Main MSID system" and sepDepart == 1 else 0
    NetworkExpand =1  if sepDepart>1 else 0
    Smallfirewall =1 if NetworkBasic == 1 and VPMDSys == "Non Virtualized" else 0
    Largefirewall =1 if NetworkExpand == 1 or VPMDSys == "Virtualized" else 0
    DSSwitches = 2 + m.floor(AmtFiberOptic/8.01) *2
    SUnitDSSwitches = DSSwitches if DSSwitches >2 else 0
    L25L35Switches =2 if NetworkExpand !=0 or VPMDSys =="Virtualized" else 0
    SUnitL25L35Switches = L25L35Switches if L25L35Switches >=2 else 0
    PDCFFCE22 = NonRedFEC_DP +RedFCE_DP*2
    PDCFFCE31 = (NonRedFEC_PN)
    RackForTwoPMD_FCE_Cont = m.ceil((PDCFFCE22+PDCFFCE31)/2)
    max16or20 = m.ceil((RackForTwoPMD_FCE_Cont*2 -8)/20) if (RackForTwoPMD_FCE_Cont *2 >8) else 0
    max16or20+= sepFCEcabinet

    MZPCSR02_1 = m.ceil(ConremoteView/10) if VPMDSys =="Non Virtualized" else 0
    MZPCSR02_2 =  Non_VirtPMDser
    MZPCSR02_3 =0
    if VPMDSys =="Non Virtualized":
        if OPCclient!=0:
            MZPCSR02_3 =1
    MZPCSR02= MZPCSR02_1 + MZPCSR02_2+MZPCSR02_3

    CE900_IOcards = SWI_BOU_16UIO+SWI_BOU_16UIO_UMS +m.ceil(SWI_32BI/2) +m.ceil(BOU_32BO/2)+MSI_32BI+MAI_ACO_16UIO+MAI_2x8UAI+MAI_ACO_16UIO_UMS+PBI_16DI+PB0_8DO
    CE900_IOracks = m.ceil(CE900_IOcards/8)
    UMSmodulesCabinet = SWI_BOU_16UIO_UMS+MAI_ACO_16UIO_UMS
    CE900racksCabinet = CE900_IOracks - TpaRacksReplace if UseOnlyCE900 == "Single" and CE900_IOracks >TpaRacksReplace else max((CE900_IOracks - TpaRacksReplace*2),0)

    NewCabinets_1 = m.floor((0.23809523809523808)*UMSmodulesCabinet*1000)/1000
    NewCabinets_2 = m.floor((0.20)*UMSmodulesCabinet*1000)/1000
    NewCabinets = m.ceil((CE900racksCabinet +NewCabinets_1 +NewCabinets_2)/10)
    DInput24VDC32Ch = m.ceil(SWI_32BI/2)+ MSI_32BI
    DOutput24VDC32Ch = m.ceil(BOU_32BO/2)
    UniversalIOmodules = MAI_ACO_16UIO +SWI_BOU_16UIO+ SWI_BOU_16UIO_UMS+MAI_ACO_16UIO_UMS

    Firepower_1010 = 1 if NetworkBasic == 1 and separateFirewall =="No" else 0
    Firepower_1010 +=Smallfirewall
    Firepower_1120 = 1 if NetworkExpand == 1 and separateFirewall =="No" else 0
    Firepower_1120 +=Largefirewall
    T_900U010100 = UniversalIOmodules
    T_900A010202 = MAI_2x8UAI*2
    T_900G030202 = PBI_16DI
    T_900G320101 = DInput24VDC32Ch
    T_900H030202 = PB0_8DO
    T_900H320102 = DOutput24VDC32Ch

    sumofabove = T_900U010100+T_900A010202+T_900G030202+T_900G320101+T_900H030202+T_900H320102
    T_900R080200 = max(CE900_IOracks,m.ceil((sumofabove)/8))

    Cable_10ch_1m=max((UniversalIOmodules+MAI_2x8UAI*2+PBI_16DI+PB0_8DO-SWI_BOU_16UIO_UMS-MAI_ACO_16UIO_UMS),0)
    Cable_32ch_5m = DInput24VDC32Ch+DOutput24VDC32Ch
    MZPCWS93_1_1 = ssHMIvirt+dsHMIvirt+qsHMIvirt if VPMDSys == "Non Virtualized" else 0
    MZPCWS93_1 = MZPCWS93_1_1 +ssHMIcab+dsHMIcab+qsHMIcab
    MZPCWS93_2 = CM_EWS+VDM_EWS if VPMDSys == "Non Virtualized" else 0
    MZPCWS93 = MZPCWS93_1+ MZPCWS93_2
    MCAFEE = MZPCWS93 + MZPCSR02_1 + Non_VirtPMDser +VirtHMIworkstn+VirtRHSser+VirtPMDser+VirtWorkstation

    #assign value to attribute

    Product.Attr('TPA_Qty_of_MZ_PCSR02').AssignValue(str(MZPCSR02))
    Product.Attr('TPA_OPC_client_Custom_cal').AssignValue(str(OPCclient))
    Product.Attr('TPA_MCAFEE_ACTIVE_VIRUSSCAN').AssignValue(str(MCAFEE))
    Product.Attr('TPA_Firewall_Firepower_1010').AssignValue(str(Firepower_1010))
    Product.Attr('TPA_Firewall_Firepower_1120').AssignValue(str(Firepower_1120))
    Product.Attr('TPA_Stack_unit_for_9200').AssignValue(str(SUnitDSSwitches+SUnitL25L35Switches))
    Product.Attr('TPA_RackForTwoPMD_Custom_Cal').AssignValue(str(RackForTwoPMD_FCE_Cont))
    Product.Attr('TPA_CabinetForMaxSixteen_Custom_cal').AssignValue(str(max16or20))
    Product.Attr('TPA_RequiredCE900RacksInNewCabinet_Custom_cal').AssignValue(str(CE900racksCabinet))
    Product.Attr('TPA_Qty_of_900R08_0200').AssignValue(str(T_900R080200))
    Product.Attr('TPA_EIOCB_IOmigrationCable_10ch_1m').AssignValue(str(Cable_10ch_1m))
    Product.Attr('TPA_EIOCB_IOmigrationCable_32ch_5m').AssignValue(str(Cable_32ch_5m))
    Product.Attr('TPA_New_cabinets_custom_cal').AssignValue(str(NewCabinets))