from GS_MigrationLaborHoursModule import getnumberOfjumpRealease,getRowData,getRowDataIndex,checkForMPACustomer,calculateTotals,getContainer,getFloat
from GS_MigrationLaborHoursModule_2 import getxPMtoC300LabourHours,calculateFinalHours1,reCalAdj
from GS_MigrationLaborHoursModule_3 import getFSCTOSMLabourHours, getFDMLabourHours, getLMtoELMMLabourHours,getXP10LabourHours, getFSCtoSMIOAuditLabourHours
from GS_MigrationLaborHoursModule_4 import getGraphicsMigrationLabourHours, getCDActuatorLabourHours, getFSCTOSMIOLabourHours, getCWSRAEMigrationLabourHours, calculateEMPEfforts
from GS_MigrationLaborHoursUtil import getProjectMangementHours

xPMCon = getContainer(Product,"MSID_Labor_xPM_to_C300_Migration_Con")
fsctosmCon = getContainer(Product,"MSID_Labor_FSC_to_SM_con")
fsctosmauditCon = getContainer(Product,"MSID_Labor_FSC_to_SM_audit_Con")
fdmCon = getContainer(Product,"MSID_Labor_FDM_Upgrade_Con")
lmCon = getContainer(Product,"MSID_Labor_LM_to_ELMM_Con")
XP10Con = getContainer(Product,"MSID_Labor_XP10_Actuator_Upgrade_con")
GraphicsCon = getContainer(Product,"MSID_Labor_Graphics_Migration_con")
CDActuatorCon = getContainer(Product,"MSID_Labor_CD_Actuator_con")
fscsmioCon = getContainer(Product,"MSID_Labor_FSCtoSM_IO_con")
cwsCon = getContainer(Product,"MSID_Labor_CWS_RAE_Upgrade_con")
fsctosmioauditcon = getContainer(Product,'MSID_Labor_FSC_to_SM_IO_Audit_Con')
if xPMCon.Rows.Count > 0:
    felSiteVisitDataGathering,migrationDDS,inHouseEngineering,fatProcedure,preFAT,fat,siteInstallationEaps,siteInstallationEST1,commisioning,sat = getxPMtoC300LabourHours(Product)
    for row in xPMCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan Review & KOM":
            row["Calculated_Hrs"] = "4"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FEL Site Visit Data Gathering":
            row["Calculated_Hrs"] = str(felSiteVisitDataGathering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration DDS":
            row["Calculated_Hrs"] = str(migrationDDS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SW_HW order":
            row["Calculated_Hrs"] = "8"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "In-house engineering":
            row["Calculated_Hrs"] = str(inHouseEngineering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT Procedure":
            row["Calculated_Hrs"] = str(fatProcedure)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Pre FAT":
            row["Calculated_Hrs"] = str(preFAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT":
            row["Calculated_Hrs"] = str(fat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation - EAPS":
            row["Calculated_Hrs"] = str(siteInstallationEaps)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation-EST1":
            row["Calculated_Hrs"] = str(siteInstallationEST1)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Commisioning":
            row["Calculated_Hrs"] = str(commisioning)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(sat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(xPMCon)

if fsctosmCon.Rows.Count > 0 and fsctosmauditCon.Rows.Count > 0:
    documentation, detailHWEngHrs, project_drawing_update, Application_migration_Eng, Fat, OnSiteHours, Sat, PreMigrationAudit, OnSiteMigrationAudit, CreateMigrationAudit = getFSCTOSMLabourHours(Product)
    for row in fsctosmCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Documentation":
            row["Calculated_Hrs"] = str(documentation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Detail HW Engineering":
            row["Calculated_Hrs"] = str(detailHWEngHrs)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Project Drawing Update":
            row["Calculated_Hrs"] = str(project_drawing_update)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Application Migration Eng":
            row["Calculated_Hrs"] = str(Application_migration_Eng)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT":
            row["Calculated_Hrs"] = str(Fat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "On-Site Hours":
            row["Calculated_Hrs"] = str(OnSiteHours)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(Sat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateEMPEfforts(Product,fsctosmCon)

    for row in fsctosmauditCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Pre-Migration Audit":
            row["Calculated_Hrs"] = str(PreMigrationAudit)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "On-Site Migration Audit":
            row["Calculated_Hrs"] = str(OnSiteMigrationAudit)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Create Migration Audit Report":
            row["Calculated_Hrs"] = str(CreateMigrationAudit)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateEMPEfforts(Product,fsctosmauditCon)
    calculateTotals(fsctosmCon)
    calculateTotals(fsctosmauditCon)

if fdmCon.Rows.Count > 0:
    Planning_and_Kom, System_backup, Ordering_Software_Hardware, installation_and_config,Documentation_Workpack_FAT_Checklist_SAT_Checklist, interal_testing, Commissioning, SAT, AS_Built_Documentation_and_Corrective_Actions, Project_Closeout = getFDMLabourHours(Product)
    for row in fdmCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Planning & KOM":
            row["Calculated_Hrs"] = str(Planning_and_Kom)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Ordering Software & Hardware":
            row["Calculated_Hrs"] = str(Ordering_Software_Hardware)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Documentation (Workpack, FAT Checklist, SAT Checklist)":
            row["Calculated_Hrs"] = str(Documentation_Workpack_FAT_Checklist_SAT_Checklist)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Internal Testing & FAT":
            row["Calculated_Hrs"] = str(interal_testing)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "System Backup":
            row["Calculated_Hrs"] = str(System_backup)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Installation and Configuration":
            row["Calculated_Hrs"] = str(installation_and_config)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Commissioning":
            row["Calculated_Hrs"] = str(Commissioning)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(SAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)        
        elif row["Deliverable"] == "AS Built Documentation and Corrective Actions":
            row["Calculated_Hrs"] = str(AS_Built_Documentation_and_Corrective_Actions)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Project Closeout":
            row["Calculated_Hrs"] = str(Project_Closeout)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(fdmCon)

if lmCon.Rows.Count > 0:
    plan_esss, plan_eaps, feldatagathering, migrationdds_esss, migrationdds_eaps, sw_hworder, inhouse_esss, inhouse_eaps, prefat, fat, siteinstallation_eaps, siteinstallation_est, sat = getLMtoELMMLabourHours(Quote,Product)
    for row in lmCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan Review & KOM - ESSS":
            row["Calculated_Hrs"] = str(plan_esss)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Plan Review & KOM - EAPS":
            row["Calculated_Hrs"] = str(plan_eaps)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FEL Site Visit Data Gathering":
            row["Calculated_Hrs"] = str(feldatagathering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration DDS - ESSS":
            row["Calculated_Hrs"] = str(migrationdds_esss)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration DDS - EAPS":
            row["Calculated_Hrs"] = str(migrationdds_eaps)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SW_HW order":
            row["Calculated_Hrs"] = str(sw_hworder)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SW_HW order":
            row["Calculated_Hrs"] = str(sw_hworder)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "In-house engineering - ESSS":
            row["Calculated_Hrs"] = str(inhouse_esss)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "In-house engineering - EAPS":
            row["Calculated_Hrs"] = str(inhouse_eaps)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Pre FAT":
            row["Calculated_Hrs"] = str(prefat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT":
            row["Calculated_Hrs"] = str(fat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation - EAPS":
            row["Calculated_Hrs"] = str(siteinstallation_eaps)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation - EST1":
            row["Calculated_Hrs"] = str(siteinstallation_est)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(sat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(lmCon)

if XP10Con.Rows.Count > 0:
    Site_installation = getXP10LabourHours(Product)
    for row in XP10Con.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "HW SW order to factory":
            row["Calculated_Hrs"] = "4"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation":
            row["Calculated_Hrs"] = str(Site_installation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(XP10Con)


if GraphicsCon.Rows.Count > 0:
    customer_input_Study, Query_Generation_Clarification, Display_Generation, Safeview_Configuration, Testing_system, SAT_Support, Operator_Training, Project_Close_Out, Shapes, Migration_FDS, FAT_Support, GAP_Analysis, FAT_SAT_Documentation, Migration_DDS, Faceplates = getGraphicsMigrationLabourHours(Product)
    for row in GraphicsCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Kick Off Meeting":
            row["Calculated_Hrs"] = str("16")
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Customer Input Study":
            row["Calculated_Hrs"] = str(customer_input_Study)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Query Generation & Clarification":
            row["Calculated_Hrs"] = str(Query_Generation_Clarification)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "GAP Analysis":
            row["Calculated_Hrs"] = str(GAP_Analysis)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Display Generation":
            row["Calculated_Hrs"] = str(Display_Generation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Shapes":
            row["Calculated_Hrs"] = str(Shapes)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Safeview Configuration":
            row["Calculated_Hrs"] = str(Safeview_Configuration)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Testing System Setup":
            row["Calculated_Hrs"] = str(Testing_system)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration FDS":
            row["Calculated_Hrs"] = str(Migration_FDS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Project Close Out":
            row["Calculated_Hrs"] = str(Project_Close_Out)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT Support":
            row["Calculated_Hrs"] = str(FAT_Support)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT Support":
            row["Calculated_Hrs"] = str(SAT_Support)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Operator Training":
            row["Calculated_Hrs"] = str(Operator_Training)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "FAT & SAT Documentation":
            row["Calculated_Hrs"] = str(FAT_SAT_Documentation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration DDS":
            row["Calculated_Hrs"] = str(Migration_DDS)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Faceplates":
            row["Calculated_Hrs"] = str(Faceplates)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)

    calculateTotals(GraphicsCon)


if CDActuatorCon.Rows.Count > 0:
    Additional_Docs,In_house_engineering,Site_Installation,SAT = getCDActuatorLabourHours(Product)
    for row in CDActuatorCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan Review & KOM":
            row["Calculated_Hrs"] = "20"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SW_HW order":
            row["Calculated_Hrs"] = "8"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Additional Docs":
            row["Calculated_Hrs"] = str(Additional_Docs)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration Doc":
            row["Calculated_Hrs"] = "8"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "In-house engineering":
            row["Calculated_Hrs"] = str(In_house_engineering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation":
            row["Calculated_Hrs"] = str(Site_Installation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(SAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)

    calculateTotals(CDActuatorCon)
    

if fscsmioCon.Rows.Count > 0:
    inhouse_prepost_engineering, safety_audit, documentation, inhouse_Engineering, software_fat, onsite_io_migration, sat= getFSCTOSMIOLabourHours(Product)
    for row in fscsmioCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan review & Kick off Meetings":
            row["Calculated_Hrs"] = "8"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Inhouse pre-post engineering":
            row["Calculated_Hrs"] = str(inhouse_prepost_engineering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Inhouse Engineering":
            row["Calculated_Hrs"] = str(inhouse_Engineering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Documentation":
            row["Calculated_Hrs"] = str(documentation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Factory Acceptance Test (FAT)":
            row["Calculated_Hrs"] = str(software_fat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Safety Audit":
            row["Calculated_Hrs"] = str(safety_audit)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "On-Site IO Migration":
            row["Calculated_Hrs"] = str(onsite_io_migration)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(sat)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(fscsmioCon)
    
if cwsCon.Rows.Count > 0:
    additional_docs, site_installation, SAT, in_house_engineering, Server_Station_Build, MD_CD_Configuration = getCWSRAEMigrationLabourHours(Product)
    for row in cwsCon.Rows:
        oldCalHrs = row["Calculated_Hrs"]
        if row["Deliverable"] == "Plan Review & KOM":
            row["Calculated_Hrs"] = "8.0"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SW_HW order":
            row["Calculated_Hrs"] = "4.0"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Additional Docs":
            row["Calculated_Hrs"] = str(additional_docs)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Migration Doc":
            row["Calculated_Hrs"] = "8.0"
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "In-house engineering":
            row["Calculated_Hrs"] = str(in_house_engineering)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Server/Station Build":
            row["Calculated_Hrs"] = str(Server_Station_Build)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "MD CD Configuration":
            row["Calculated_Hrs"] = str(MD_CD_Configuration)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "Site Installation":
            row["Calculated_Hrs"] = str(site_installation)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
        elif row["Deliverable"] == "SAT":
            row["Calculated_Hrs"] = str(SAT)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row["Final_Hrs"] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(cwsCon)
if fsctosmioauditcon.Rows.Count > 0:
    Safety_Audit = getFSCtoSMIOAuditLabourHours(Product)
    for row in fsctosmioauditcon.Rows:
        oldCalHrs = row['Calculated_Hrs']
        if row['Deliverable'] == 'Safety Audit':
            row['Calculated_Hrs'] = str(Safety_Audit)
            row["Adjustment_Productivity"] = reCalAdj(row,oldCalHrs)
            row['Final_Hrs'] = calculateFinalHours1(row,oldCalHrs)
    calculateTotals(fsctosmioauditcon)