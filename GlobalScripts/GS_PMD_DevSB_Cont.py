def loadContFromDB(container):
    container.Clear()
    container.LoadFromDatabase("SELECT * FROM PMD_Profibus_SB_Cont_Data WHERE Container = '"+container.Name+"'", 'Code')

def loadContFromDict(container):
    # "PMD_Profibus_Drives_Cont"
    drives_cont = {"PMD_ABB": "SWFP1002-Device Support Block Set for ABB Drives v.C.",
                   "PMD_Siemans": "SWFP1003 -Device Support Block Set for Siemens Drive v.2",
                   "PMD_Danfoss": "SWFP1004-Device Support Block Set for Danfoss VTL Drives",
                   "PMD_Lenze": "SWFP110249 -Device Support Block Set for Lenze Drives",
                   "PMD_VaconNX": "SWFP1012-Device Support Block Set for VACON NX Frequency Converter",
                   "PMD_VaconCX": "SWFP110099-Device Support Block Set for VACON CX Frequency Converters",
                   "PMD_Toshiba": "SWFP110335-Device Support Block Set for Toshiba Tosvert Drives",
                   "PMD_Control": "SWFP110373-Device Support Block Set for Control Techniques Drive",
                   "PMD_Eurotherm": "SWFP110617-Device Support Block Set for Eurotherm Drives",
                   "PMD_SIEISPA": "SWFP110975 -Device Support Block Set for SIEI SPA Drives",
                   "PMD_PDL": "SWFP111160-Device Support Block Set for PDL Electronics Drives",
                   "PMD_Telemecanique": "SWFP111162-Device Support Block Set for Telemecanique Drives",
                   "PMD_SD700": "SWFP112209-Device Support Block Set for Power Electronics SD700 Drive"}

    # "PMD_Profibus_Links_and_Gateways_Cont1"
    links_gates_cont = {
        "PMD_SiemensPA": "SWFP1006-Device Support Block Set for PROFIBUS PA Device Access via Siemens DP/PA Link",
        "PMD_SiemensDP": "SWFP1007-Device Support Block Set for PROFIBUS DP Device Access via Siemens DP/DP Coupler",
        "PMD_Siemens_20E": "SWFP1009-Device Support Block Set for Siemens DP/ASi link 20E",
        "PMD_GEASi": "SWFP110087-Device Support Block Set for GE ASi DP Gateway",
        "PMD_ASiDP": "SWFP110088-Device Support Block Set for Ifm Electric ASi-DP Controller",
        "PMD_CU9600": "SWFP110103-Device Support Block Set for Åkerströms Remotus CU 9600 Radiolink System",
        "PMD_CANCBM": "SWFP110279 -Device Support Block Set for esd CAN-CBM-DP Gateway",
        "PMD_SiemensCPU": "SWFP110336-Device Support Block Set for Siemens CPU316-2 DP PLC via CP342-5 module",
        "PMD_ToshibaS3": "SWFP110396-Device Support Block Set for Toshiba S3 PLC via PF312 module",
        "PMD_GEFanuc": "SWFP110096-Device Support Block Set for GE Fanuc 90 70 PLC via SST PFB GE board, FC Profibus",
        "PMD_ASiCon": "SWFP110755-Device Support Block Set for Ifm Electronic ASi Controller e, FC Profibus",
        "PMD_SiemensS7": "SWFP110976 -Device Support Block Set for Siemens S7-400 CPU416-3",
        "PMD_Anybus": "SWFP111159-Device Support Block Set for HMS Anybus-S interface module",
        "PMD_SiemensIM": "SWFP111163-Device Support Block Set for Siemens IM 308-C DP",
        "PMD_GE_FANUC": "SWFP110756-DEVICE SUPPORT BLOCK SET FOR GE FANUC 90 70 PLC VIA SST PFB GE BOARD"}

    # "PMD_Profibus_Motor_Starters and_CD_Cont"
    motor_cd_cont = {"PMD_ABBINSUM": "SWFP110176-Device Support Block Set for ABB INSUM Gateway",
                     "PMD_SiemensSc": "SWFP111548-Device Support Block Set for Siemens Simocode v.3",
                     "PMD_UMC22": "SWFP110371-Device Support Block Set for ABB UMC22-FBP",
                     "PMD_SiemensSPD": "SWFP110701-Device Support Block Set for  Siemens Siprotec Protection Devices",
                     "PMD_UMC22V2": "SWFP111155-Device Support Block Set for ABB UMC22-FBP v.2",
                     "PMD_Metso": "SWFP111156-Device Support Block Set for Metso ND9000PA Valve Controller",
                     "PMD_Norgren": "SWFP111214-Device Support Block Set for Norgren V18/V26 Valves",
                     "PMD_ABBMNS": "SWFP110176-Device Support Block Set for ABB MNS iS (ABMNS101)",
                     "PMD_SiemensSSS": "SWFP112235-Device Support Block Set for Siemens Sirius Soft Starter",
                     "PMD_MNSIS": "SWFP111858-DEVICE SUPPORT BLOCK SET FOR ABB MNS IS"}

    # "PMD_Other_Profibus_DP-Devices_Cont"
    other_dp_cont = {"PMD_AiRanger": "SWFP110175-Device Support Block Set for Milltronics AiRanger XPL Plus Level monitor",
                     "PMD_Eilersen": "SWFP110320-Device Support Block Set for Eilersen Electric MCE9635 Loadcell",
                     "PMD_RAUTE": "SWFP110089-Device Support Block  Set for RAUTE Dosing/Weighing controllers WB-930 and WB-951",
                     "PMD_HNC100": "SWFP110174-Device Support Block  Set for Rexroth Digital Controller HNC 100",
                     "PMD_VMAC260": "SWFP110090-Device Support Block Set for Vaasa Electronics VMAC 260 Power Monitoring Unit",
                     "PMD_Auma": "SWFP110101-Device Support Block Set for Auma Actuator",
                     "PMD_EM277": "SWFP110357 -Device Support Block Set for Siemens EM277 Profibus-DP Module",
                     "PMD_DIRIS": "SWFP110337-Device Support Block Set for Socomec DIRIS AP Power Monitoring Unit",
                     "PMD_SiemensS7-315": "SWFP110338-Device Support Block Set for Siemens S7-315-2 DP",
                     "PMD_Vogel": "SWFP110395-Device Support Block Set for Vogel IPM-12 pulse meter via XPS-E gateway",
                     "PMD_Numatics": "SWFP110618-Device Support Block Set for Numatics Valves via G2-2 communication module",
                     "PMD_Rexroth": "SWFP110619-Device Support Block Set for Mannesmann Rexroth valves via bus direct module",
                     "PMD_GWT": "SWFP110702-Device Support Block Set for GWT Weighing Instrument via PR 5210 Module",
                     "PMD_RexrothDC": "SWFP110973-Device Support Block Set for Rexroth Digital Controller HNC100 v.2",
                     "PMD_ELCIS": "SWFP110974 -Device Support Block Set for ELCIS Encoder",
                     "PMD_BurnerCon": "SWFP111157-Device Support Block Set for Kromschöder Burner Control via PFA700 module",
                     "PMD_ABBTE": "SWFP111161-Device Support Block Set for ABB Tension Electronics",
                     "PMD_applicom": "SWFP111213-Device Support Block Set for applicom PC interface via PCI-DPIO board",
                     "PMD_VAMP255": "SWFP111216-Device Support Block Set for Feeder Manager VAMP 255",
                     "PMD_DPSlaves": "SWFP111217-Generic Device Support Block Set for Profibus DP Slaves",
                     "PMD_SiemensDR": "SWFP110368-Device Support Block Set for Siemens Diagnostic Repeater",
                     "PMD_AtlasCC": "SWFP111343-Device Support Block Set for Atlas Copco Compressor",
                     "PMD_IDEACOD": "SWFP111344-Device Support Block Set for BEI IDEACOD Encoder",
                     "PMD_MTS": "SWFP111348-Device Support Block Set for MTS Sensor ",
                     "PMD_RauteDos": "SWFP112691-DEVICE SUPPORT BLOCK SET FOR RAUTE DOSING/WEIGHING CONTROLLERS WA80XX"}

    # "PMD_Profibus_Modular_IO_Cont"
    mod_io_cont = {"PMD_GEFanucSS": "SWFP1013-Device Support Block Set for GE-Fanuc 90-30 I/O Modules (Small Systems)",
                   "PMD_GEFanucMS": "SWFP1013-Device Support Block Set for GE-Fanuc 90-30 I/O Modules (Medium Systems)",
                   "PMD_GEFanucLS": "SWFP1013-Device Support Block Set for GE-Fanuc 90-30 I/O Modules (Large Systems)",
                   "PMD_MTLSS": "SWFP110281-Device Support Block Set for Measurement Technology Ltd MTL 8000 I/O  v.2.0 (Small systems)",
                   "PMD_MTLMS": "SWFP110281-Device Support Block Set for Measurement Technology Ltd MTL 8000 I/O  v.2.0 (Medium systems)",
                   "PMD_MTLLS": "SWFP110281-Device Support Block Set for Measurement Technology Ltd MTL 8000 I/O  v.2.0 (Large systems)",
                   "PMD_SiemensETSS": "SWFP110335-Device Support Block Set for Siemens ET 200M I/O (IM 153-1) (Small systems)",
                   "PMD_SiemensETMS": "SWFP1019-Device Support Block Set for Siemens ET 200M I/O (IM 153-1) (Medium systems)",
                   "PMD_SiemensETLS": "SWFP1019-Device Support Block Set for Siemens ET 200M I/O (IM 153-1) (Large systems)",
                   "PMD_SmETSS": "SWFP110703-Device Support Block Set for Siemens ET 200M I/O (IM 153-2) (Small systems)",
                   "PMD_SmETMS": "SWFP110703-Device Support Block Set for Siemens ET 200M I/O (IM 153-2) (Medium systems)",
                   "PMD_SmETLS": "SWFP110703-Device Support Block Set for Siemens ET 200M I/O (IM 153-2) (Large systems)",
                   "PMD_ET200SSS": "SWFP110280-Device Support Block Set for Siemens ET200S I/O (Small systems)",
                   "PMD_ET200SMS": "SWFP110280-Device Support Block Set for Siemens ET200S I/O (Medium systems)",
                   "PMD_ET200SLS": "SWFP110280-Device Support Block Set for Siemens ET200S I/O (Large systems)",
                   "PMD_VersamaxSS": "SWFP1022-Device Support Block Set for GE Versamax I/O (Small systems)",
                   "PMD_VersamaxMS": "SWFP1022-Device Support Block Set for GE Versamax I/O (Medium systems)",
                   "PMD_VersamaxLS": "SWFP1022-Device Support Block Set for GE Versamax I/O (Large systems)",
                   "PMD_BechoffSS": "SWFP110091-Device Support Block Set for Beckhoff I/O (Small systems)",
                   "PMD_BechoffMS": "SWFP110091-Device Support Block Set for Beckhoff I/O (Medium systems)",
                   "PMD_BechoffLS": "SWFP110091-Device Support Block Set for Beckhoff I/O (Large systems)",
                   "PMD_WagoSS": "SWFP110102-Device Support Block Set for Wago I/O (Small systems)",
                   "PMD_WagoMS": "SWFP110102-Device Support Block Set for Wago I/O (Medium systems)",
                   "PMD_WagoLS": "SWFP110102-Device Support Block Set for Wago I/O (Large systems)",
                   "PMD_PhoenixSS": "SWFP110104-Device Support Block Set for Phoenix IL PB BK I/O (Small systems)",
                   "PMD_PhoenixMS": "SWFP110104-Device Support Block Set for Phoenix IL PB BK I/O (Medium systems)",
                   "PMD_PhoenixLS": "SWFP110104-Device Support Block Set for Phoenix IL PB BK I/O (Large systems)",
                   "PMD_PhoenixILSS": "SWFP111818-Device Support Block Set for Phoenix IL PB BK I/O v.2  (Small systems)",
                   "PMD_PhoenixILMS": "SWFP111818-Device Support Block Set for Phoenix IL PB BK I/O v.2  (Medium systems)",
                   "PMD_PhoenixILLS": "SWFP111818-Device Support Block Set for Phoenix IL PB BK I/O v.2  (Large systems)",
                   "PMD_SattConSS": "SWFP110389-Device Support Block Set for SattCon I/O via Elektroautomatik PBI board(v. 200.000, Small systems)",
                   "PMD_SattConMS": "SWFP110389-Device Support Block Set for SattCon I/O via Elektroautomatik PBI board(v. 200.000, Medium systems)",
                   "PMD_SattConLS": "SWFP110389-Device Support Block Set for SattCon I/O via Elektroautomatik PBI board(v. 200.000, Large systems)",
                   "PMD_SiemSS": "SWFP111158-Device Support Block Set for Siemens ET200B I/O (Small Systems)",
                   "PMD_SiemMS": "SWFP111158-Device Support Block Set for Siemens ET200B I/O (Medium Systems)",
                   "PMD_SiemLS": "SWFP111158-Device Support Block Set for Siemens ET200B I/O (Large Systems)",
                   "PMD_CEAGSS": "SWFP111345-Device Support Block Set for CEAG I/O (Small Systems)",
                   "PMD_CEAGMS": "SWFP111345-Device Support Block Set for CEAG I/O (Medium Systems)",
                   "PMD_CEAGLS": "SWFP111345-Device Support Block Set for CEAG I/O (Large Systems)",
                   "PMD_TURCKSS": "SWFP111349-Device Support Block Set for TURCK I/O (Small Systems)",
                   "PMD_TURCKMS": "SWFP111349-Device Support Block Set for TURCK I/O (Medium Systems)",
                   "PMD_TURCKLS": "SWFP111349-Device Support Block Set for TURCK I/O (Large Systems)",
                   "PMD_CerabarPT": "SWFP111346-Device Support Block Set for E+H Cerabar S PA Pressure Transmitter",
                   "PMD_ValmetCT": "SWFP111347-Device Support Block Set for Metso Valmet SP PA Consistency Transmitter",
                   "PMD_PnixSS": "SWFP111547-Device Support Block Set for Phoenix IL PB BK DI8 DO4 I/O (Small Systems)",
                   "PMD_PnixMS": "SWFP111547-Device Support Block Set for Phoenix IL PB BK DI8 DO4 I/O (Medium Systems)",
                   "PMD_PnixLS": "SWFP111547-Device Support Block Set for Phoenix IL PB BK DI8 DO4 I/O (Large Systems)",
                   "PMD_ABBS800SS": "SWFP111215-Device Support Block Set for ABB S800 I/O (Small Systems)",
                   "PMD_ABBS800MS": "SWFP111215-Device Support Block Set for ABB S800 I/O (Medium Systems)",
                   "PMD_ABBS800LS": "SWFP111215-Device Support Block Set for ABB S800 I/O (Large)",
                   "PMD_HoneywellSS": "SWFP111819-Device Support Block Set for Honeywell Smart I/O (Small Systems)",
                   "PMD_HoneywellMS": "SWFP111819-Device Support Block Set for Honeywell Smart I/O (Medium Systems)",
                   "PMD_HoneywellLS": "SWFP111819-Device Support Block Set for Honeywell Smart I/O (Large Systems)",
                   "PMD_HoneywellML": "SWFP112597-Device Support Block Set for Honeywell Master Logic ML200  I/O ",
                   "PMD_SIETCSS": "SWFP111820-Device Support Block Set for Siemens ET200M I/O DPV1 (SIETC101) (Small Systems)",
                   "PMD_SIETCMS": "SWFP111820-Device Support Block Set for Siemens ET200M I/O DPV1 (SIETC101) (Medium Systems)",
                   "PMD_SIETCLS": "SWFP111820-Device Support Block Set for Siemens ET200M I/O DPV1 (SIETC101) (Large Systems)",
                   "PMD_DPV1SS": "SWFP112281-Device Support Block Set for Siemens ET200M I/O DPV1 High feature (Small Systems)",
                   "PMD_DPV1MS": "SWFP112281-Device Support Block Set for Siemens ET200M I/O DPV1 High feature (Medium Systems)",
                   "PMD_DPV1LS": "SWFP112281-Device Support Block Set for Siemens ET200M I/O DPV1 High feature (Large Systems)",
                   "PMD_PepperlSS": "SWFP112245-Device Support Block Set for Pepperl + Fuchs RPI I/O (Small Systems)",
                   "PMD_PepperlMS": "SWFP112245-Device Support Block Set for Pepperl + Fuchs RPI I/O (Medium Systems)",
                   "PMD_PepperlLS": "SWFP112245-Device Support Block Set for Pepperl + Fuchs RPI I/O (Large Systems)",
                   "PMD_ET200iSPSS": "SWFP112246-Device Support Block Set for Siemens ET200iSP I/O (Small Systems)",
                   "PMD_ET200iSPMS": "SWFP112246-Device Support Block Set for Siemens ET200iSP I/O (Medium Systems)",
                   "PMD_ET200iSPLS": "SWFP112246-Device Support Block Set for Siemens ET200iSP I/O (Large Systems)",
                   "PMD_EXCOMSS": "SWFP111645/SWFP112936-DEVICE SUPPORT BLOCK SET FOR TURCK EXCOM IO (Small Systems)",
                   "PMD_EXCOMMS": "SWFP111645/SWFP112936-DEVICE SUPPORT BLOCK SET FOR TURCK EXCOM IO (Medium Systems)",
                   "PMD_EXCOMLS": "SWFP111645/SWFP112936-DEVICE SUPPORT BLOCK SET FOR TURCK EXCOM IO (Large Systems)",
                   "PMD_BK31XXXSS": "SWFP112692-DEVICE SUPPORT BLOCK SET FOR BECKHOFF I/O VER BK31XXX (Small Systems)",
                   "PMD_BK31XXXMS": "SWFP112692-DEVICE SUPPORT BLOCK SET FOR BECKHOFF I/O VER BK31XXX (Medium Systems)",
                   "PMD_BK31XXXLS": "SWFP112692-DEVICE SUPPORT BLOCK SET FOR BECKHOFF I/O VER BK31XXX (Large Systems)",
                   "PMD_AXIOLINESS": "SWFP112934-DEVICE SUPPORT BLOCK SET FOR PHOENIX AXIOLINE I/O (Small Systems)",
                   "PMD_AXIOLINEMS": "SWFP112934-DEVICE SUPPORT BLOCK SET FOR PHOENIX AXIOLINE I/O (Medium Systems)",
                   "PMD_AXIOLINELS": "SWFP112934-DEVICE SUPPORT BLOCK SET FOR PHOENIX AXIOLINE I/O (Large Systems)",
                   "PMD_EXTSS": "SWFP112602-DEVICE SUPPORT BLOCK SET FOR SIEMENS ET200S I/O EXTENSION (Small Systems)",
                   "PMD_EXTMS": "SWFP112602-DEVICE SUPPORT BLOCK SET FOR SIEMENS ET200S I/O EXTENSION (Medium Systems)",
                   "PMD_EXTLS": "SWFP112602-DEVICE SUPPORT BLOCK SET FOR SIEMENS ET200S I/O EXTENSION (Large Systems)"}

    # "PMD_Profibus_Displays_cont"
    displays_cont = {"PMD_Siebert": "SWFP110177-Device Support Block Set for Siebert SX502 display",
                     "PMD_ESAVT": "SWFP110282 -Device Support Block Set for ESA VTXXXW Displays",
                     "PMD_PP17": "SWFP110247 -Device Support Block Set for Siemens PP17 II panel",
                     "PMD_ProFace": "SWFP110334-Device Support Block Set for Pro-face GP377 PF-21  Displays",
                     "PMD_SiebertS302": "SWFP110620 -Device Support Block Set for Siebert S302 Display",
                     "PMD_SiemPP7": "SWFP110700-Device Support Block Set for Siemens PP7 panel",
                     "PMD_SiemOP": "SWFP110972 -Device Support Block Set for Siemens OP/TP Panel"}

    # "PMD_Profinet_Device_Support_blocks_cont"
    profin_sb_cont = {"PMD_DSBGEN": "SWFP112998-PROFINET DSB SET FOR for GENERIC PROFINET Slaves",
                      "PMD_ET200MPSS": "SWFP113110-PROFINET DSB SET FOR SIEMENS ET200MP HIGH FEATURE IO (Small Systems)",
                      "PMD_ET200MPMS": "SWFP113110-PROFINET DSB SET FOR SIEMENS ET200MP HIGH FEATURE IO (Medium Systems)",
                      "PMD_ET200MPLS": "SWFP113110-PROFINET DSB SET FOR SIEMENS ET200MP HIGH FEATURE IO (Large Systems)",
                      "PMD_ET200SSS": "SWFP112966-PROFINET DSB SET FOR SIEMENS ET200S I/O (Small Systems)",
                      "PMD_ET200SMS": "SWFP112966-PROFINET DSB SET FOR SIEMENS ET200S I/O (Medium Systems)",
                      "PMD_ET200SLS": "SWFP112966-PROFINET DSB SET FOR SIEMENS ET200S I/O (Large Systems)",
                      "PMD_ET200SPSS": "SWFP113061-PROFINET DSB SET FOR SIEMENS ET200SP I/O (Small Systems)",
                      "PMD_ET200SPMS": "SWFP113061-PROFINET DSB SET FOR SIEMENS ET200SP I/O (Medium Systems)",
                      "PMD_ET200SPLS": "SWFP113061-PROFINET DSB SET FOR SIEMENS ET200SP I/O (Large Systems)",
                      "PMD_ET200MSS": "SWFP112899-PROFINET DSB SET FOR SIEMENS ET200M I/O High feature (Small Systems)",
                      "PMD_ET200MMS": "SWFP112899-PROFINET DSB SET FOR SIEMENS ET200M I/O High feature (Medium Systems)",
                      "PMD_ET200MLS": "SWFP112899-PROFINET DSB SET FOR SIEMENS ET200M I/O High feature (Large Systems)",
                      "PMD_BL20SS": "SWFP113120-PROFINET DSB SET FOR TURCK BL20 I/O (Small Systems)",
                      "PMD_BL20MS": "SWFP113120-PROFINET DSB SET FOR TURCK BL20 I/O (Medium Systems)",
                      "PMD_BL20LS": "SWFP113120-PROFINET DSB SET FOR TURCK BL20 I/O (Large Systems)",
                      "PMD_AXIOSS": "SWFP113190-PROFINET DSB SET FOR PHOENIX AXIOLINE I/O (Small Systems)",
                      "PMD_AXIOMS": "SWFP113190-PROFINET DSB SET FOR PHOENIX AXIOLINE I/O (Medium Systems)",
                      "PMD_AXIOLS": "SWFP113190-PROFINET DSB SET FOR PHOENIX AXIOLINE I/O (Large Systems)",
                      "PMD_ProV": "SWFP113060-PROFINET DSB SET FOR SIEMENS Simocode Pro V",
                      "PMD_VaconFC": "SWFP113062-PROFINET DSB SET FOR VACON FREQUENCY CONVERTER",
                      "PMD_900IO": "SWFP112701-PROFINET DSB SET FOR HONEYWELL CONTROLEDGE 900IO",
                      "PMD_ABBFC": "SWFP113143-PROFINET DSB SET FOR ABB FREQUENCY CONVERTER",
                      "PMD_IBPROXY": "SWFP113053-PROFINET DSB SET FOR PHOENIX CONTACT FL NP PND 4TX IB PROXY ",
                      "PMD_PFCoupler": "SWFP113154 -PROFINET DSB SET FOR P_F PN/PA COUPLER"}
    
    cont_attrs = {"PMD_Profibus_Drives_Cont": drives_cont,
              "PMD_Profibus_Links_and_Gateways_Cont": links_gates_cont,
              "PMD_Profibus_Motor_Starters and_CD_Cont": motor_cd_cont,
              "PMD_Other_Profibus_DP-Devices_Cont": other_dp_cont,
              "PMD_Profibus_Modular_IO_Cont": mod_io_cont,
              "PMD_Profibus_Displays_cont": displays_cont,
              "PMD_Profinet_Device_Support_blocks_cont": profin_sb_cont}
    
    cont = cont_attrs[container.Name]
    for device in cont:
        row = container.AddNewRow(False)
        row.GetColumnByName("Device").Value = cont[device]
        #row.GetColumnByName("Type").Value = "None"
        #row.GetColumnByName("Devices").Value = '0'
        #row.GetColumnByName("AI").Value = '0'
        #row.GetColumnByName("AO").Value = '0'
        #row.GetColumnByName("DI").Value = '0'
        #row.GetColumnByName("DO").Value = '0'
        #row.GetColumnByName("LF").Value = '0'