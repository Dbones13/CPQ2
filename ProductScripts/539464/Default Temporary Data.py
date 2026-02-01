def r2qsetDefaultdrop():
    attr_value = Product.Attr("C200_Select_Migration_Scenario").GetValue()
    containerMapping = {'C200_Migration_General_Qns_Cont': {'C200_Connection _to_Experion_Server': 'FTE','C200_Type_of_UOC':'UOC','C200_Type_of_downlink_communication_UOC':'CNET Redundant','C200_Is_Honeywell_Providing_FTE_cables':'Yes','C200_Average_Cable_Length':'2m'}}
    for contName, colDetails in containerMapping.items():
        system_cont = Product.GetContainerByName(contName).Rows
        for key, val in colDetails.items():
            emptyval=system_cont[0][key]
            if str(emptyval)=='':
                if key == 'C200_Type_of_downlink_communication_UOC':
                    if attr_value == "C200 to ControlEdge UOC":
                        system_cont[0].Product.Attr(key).SelectDisplayValue(str(val))
                else:
                    system_cont[0].Product.Attr(key).SelectDisplayValue(str(val))

tempData = Product.Attr('Temporary Data').GetValue()
if not tempData:
    temp_data= {'C200_UOC_var_9': 0, 'C300_var_2': 0, 'C300_var_11': 0}
    Product.Attr('Temporary Data').AssignValue(str(temp_data))
attr_value = Product.Attr("C200_Select_Migration_Scenario").GetValue()
third_party_cont = Product.GetContainerByName("C200_Third_Party_Items_Cont")
if attr_value == "C200 to C300":
    for row in third_party_cont.Rows:
    	row["WriteIn"] = "3rd Party Hardware - DHRIO"


if Quote.GetCustomField('isR2QRequest').Content == 'Yes':
    productName = Product.Name
    if productName == "C200 Migration":
        r2qsetDefaultdrop()