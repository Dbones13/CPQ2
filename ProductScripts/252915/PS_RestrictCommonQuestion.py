
def hideColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Hidden) )*>'.format(container,Column))
    Product.ParseString('<*CTX( Container({}).Row(1).Column({}).Set() )*>'.format(container,Column))

def visibleColumn(container,Column):
    Product.ParseString('<*CTX( Container({}).Column({}).SetPermission(Editable) )*>'.format(container,Column))

def getContainer(Name):
    return Product.GetContainerByName(Name)

selectedProducts = set()

for row in getContainer("MSID_Product_Container").Rows:
    selectedProducts.add(row["Product Name"])

columnvisibilityDict = {"MSID_FEL_Data_Gathering_Required": {'OPM','ELCN','EHPM/EHPMX/ C300PM','TPS to Experion'},"MSID_Current_Experion_Release":{'OPM','Non-SESP Exp Upgrade'},"MSID_Future_Experion_Release":{'OPM','Non-SESP Exp Upgrade','TPS to Experion','xPM to C300 Migration','C200 Migration','CB-EC Upgrade to C300-UHIO'},"MSID_Current_TPN_Release":{'LCN One Time Upgrade'},"MSID_Future_TPN_Release":{'LCN One Time Upgrade'},"MSID_Acceptance_Test_Required":{'CB-EC Upgrade to C300-UHIO','TPS to Experion'}, "MSID_Is_FTE_based_System_already_installed_on_Site":{'LM to ELMM ControlEdge PLC','C200 Migration','3rd Party PLC to ControlEdge PLC/UOC'}, "LM_ELMM_Does_the_customer_want_Honeywell_to_configure_the_switches":{'LM to ELMM ControlEdge PLC'},"LM_ELMM_Construction_work_package_document_prepared_by_Honeywell":{'LM to ELMM ControlEdge PLC','Orion Console'},'MSID_Is_Switch_Configuration_in_Honeywell_Scope':{'TPS to Experion','xPM to C300 Migration','C200 Migration'}}#,"MSID_Will_Honeywell_perform_equipment_installation":{'EHPM/ C300PM'}}

for key,products in columnvisibilityDict.items():
    x = selectedProducts.intersection(products)
    if len(x) == 0:
        hideColumn("MSID_CommonQuestions",key)
    else:
        visibleColumn("MSID_CommonQuestions",key)

if ("OPM" in selectedProducts or "ELCN" in selectedProducts or "EHPM/EHPMX/ C300PM" in selectedProducts or "Orion Console" in selectedProducts or "TPS to Experion" in selectedProducts) and Product.Attr('MIgration_Scope_Choices').GetValue() == "HW/SW":
    hideColumn("MSID_CommonQuestions","MSID_FEL_Data_Gathering_Required")
    hideColumn("MSID_CommonQuestions","MSID_Is_Site_Acceptance_Test_Required")
    hideColumn("MSID_CommonQuestions","MSID_Acceptance_Test_Required")
    hideColumn("MSID_CommonQuestions",'MSID_Is_Switch_Configuration_in_Honeywell_Scope')
    hideColumn("MSID_CommonQuestions","LM_ELMM_Construction_work_package_document_prepared_by_Honeywell")
if ("3rd Party PLC to ControlEdge PLC/UOC" in selectedProducts) and Product.Attr('MIgration_Scope_Choices').GetValue() == "HW/SW":
    hideColumn("MSID_CommonQuestions","MSID_Is_FTE_based_System_already_installed_on_Site")    
