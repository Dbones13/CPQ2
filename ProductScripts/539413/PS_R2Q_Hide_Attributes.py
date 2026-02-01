def getContainer(Name):
    return Product.GetContainerByName(Name)
isR2Qquote = True if Quote.GetCustomField("isR2QRequest").Content =='Yes' else False
if isR2Qquote:
	Product.Attr('R2QRequest').AssignValue('Yes')
	Product.Attr("R2Q_QuoteNumber").AssignValue(str(Quote.CompositeNumber))
    
nonSESPDesignInputsExpCon = getContainer("NONSESP_Design_Inputs_for_Experion_Upgrade_License")
attributeset = {'NONSESP_Sever_Redundancy': 'No','NONSESP_Should_RSLinx_be_added': 'No','NONSESP_No_of_process_points': '0','NONSESP_No_of_SCADA_points': '0',
'NONSESP_No_of_Flex_Console_Ext_Stations_ESF_ESCE': '0', 'NONSESP_No_of_Console_Stations_ESC_and_EST': '0','NONSESP_No_of_TPS_Connections_LCNP_Cards': '0',
'NONSESP_No_of_3rdParty_MS_SQL_Client_License': '0','NONSESP_No_of_3rd_Party_MS_Visual_Studio_License': '0','NONSESP_No_of_CAB_Developer_Licenses': '0',
'NONSESP_No_of_RESS_Remote_Users': '0'}
row = nonSESPDesignInputsExpCon.Rows[0]
for key, value in attributeset.items():
    emptyvalue = row[key]
    if str(emptyvalue).strip() == '': 
        if key in ('NONSESP_Sever_Redundancy', 'NONSESP_Should_RSLinx_be_added'):
            row.GetColumnByName(key).SetAttributeValue(value)  
            row[key] = value
        else:
            row.SetColumnValue(key, value)
nonSESPDesignInputsExpCon.Calculate()


nonSESPDesignInputsEServerCon = getContainer("NONSESP_Design_Inputs_for_eServer_Upgrade_License")
for row in nonSESPDesignInputsEServerCon.Rows:
    if row['NONSESP_No_of_Premium_Access_Connections'] == '':
        row.SetColumnValue("NONSESP_No_of_Premium_Access_Connections",'0')
    break
nonSESPDesignInputsEServerCon.Calculate()
