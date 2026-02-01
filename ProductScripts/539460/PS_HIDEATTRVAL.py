xPMMigrationGeneralQnsCont = Product.GetContainerByName('xPM_Migration_General_Qns_Cont')
xPMMigratonScenarioCont = Product.Attr('xPM_Select_the_migration_scenario').GetValue()
for row in xPMMigrationGeneralQnsCont.Rows:
    attribute1 = row.GetColumnByName("xPM_TPN_SW_Release_at_time_of_xPM_migration").ReferencingAttribute
    attribute2 = row.GetColumnByName("xPM_EPKS_SW_Release_at_time_of_xPM_migration").ReferencingAttribute
    attribute3 = row.GetColumnByName("xPM_On_Process_Red_HPMs_or_Off_Process_Migration").ReferencingAttribute
    attribute4 = row.GetColumnByName("xPM_On_Process_Red_HPMs_EHPMs_only").ReferencingAttribute
    attribute5 = row.GetColumnByName("xPM_On_Process_Red_HPMs_EHPMs_for_EHPMX_mig").ReferencingAttribute
    for value in attribute1.Values:
        if (value.Display in ('TPN R684.2','TPN R685.1','TPN R685.2','TPN R685.3','TPN R686.2 or later','-') and xPMMigratonScenarioCont == "xPM to EHPM") or (value.Display in ('TPN R690.2 or later','-') and xPMMigratonScenarioCont in ["xPM to C300PM",'xPM to EHPMX']):
            value.Allowed = True
        else:
            value.Allowed = False
    for value in attribute2.Values:
        if (value.Display in ('None','EPKS R400/R410','EPKS R430','EPKS R431.1 / R431.2','EPKS R432.1 or later','EPKS R500 or later','-') and xPMMigratonScenarioCont == "xPM to EHPM") or (value.Display in ('EPKS R520.2 TCU1 or later','-') and xPMMigratonScenarioCont in ["xPM to C300PM",'xPM to EHPMX']):
            value.Allowed = True
        else:
            value.Allowed = False
    for value in attribute3.Values:
        if row["xPM_TPN_SW_Release_at_time_of_xPM_migration"] == "TPN R686.2 or later" and row["xPM_EPKS_SW_Release_at_time_of_xPM_migration"] == "EPKS R432.1 or later" and value.Display == "HPM to EHPM On Process":
            value.Allowed = True
        elif value.Display == "HPM to EHPM On Process":
            value.Allowed = False
    for value in attribute4.Values:
        if row["xPM_TPN_SW_Release_at_time_of_xPM_migration"] == "TPN R690.2 or later" and row["xPM_EPKS_SW_Release_at_time_of_xPM_migration"] == "EPKS R520.2 TCU1 or later" and value.Display == "HPM/EHPM/EHPMX to C300PM On Process":
            value.Allowed = True
        elif value.Display == "HPM/EHPM/EHPMX to C300PM On Process":
            value.Allowed = False
    for value in attribute5.Values:
        if row["xPM_TPN_SW_Release_at_time_of_xPM_migration"] == "TPN R690.2 or later" and row["xPM_EPKS_SW_Release_at_time_of_xPM_migration"] == "EPKS R520.2 TCU1 or later" and value.Display == "HPM/EHPM to EHPMX On Process":
            value.Allowed = True
        elif value.Display == "HPM/EHPM to EHPMX On Process":
            value.Allowed = False
    row.Calculate()

qty_of_red_pair = Product.Attr('ATT_QRPCF9IOTA')
if qty_of_red_pair.GetValue() == '':
	qty_of_red_pair.AssignValue('0')
#TagParserProduct.ParseString('<*CTX( Container({0}).Column({1}).SetPermission(Hidden) )*>'.format("xPM_Config_Asset_DB_Cont","xPM_CE_Mark_or_Not"))