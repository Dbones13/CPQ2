def allowAttributes(attrList):
    for attr in attrList:
        Product.AllowAttr(attr)

def disallowAttributes(attrList):
    for attr in attrList:
        Product.DisallowAttr(attr)

container = Product.GetContainerByName('Migration_MSID_Selection_Container')
isLaborSelected = False
isHWSWSelected = False
isValid = True

selectedProducts = set()
for row in filter(lambda x : x.IsSelected , container.Rows):
    if not row['Scope']:
        isValid = False
    if row['Scope'] == 'LABOR':
        isLaborSelected = True
    if row["Scope"] == "HWSW":
        isHWSWSelected = True
        
    selectedProducts.update(row['Selected_Products'].split('<br>'))

if container.HasSelectedRow and isValid:
    allowAttributes(['Migration_Apply_Product_Selection'])
else:
    disallowAttributes(['Migration_Apply_Product_Selection'])
if isLaborSelected or 'Non-SESP Exp Upgrade' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','NON_SESP_EXP')
else:
    Product.AllowAttrValues('Migration_Product_Choices','NON_SESP_EXP')

if 'LCN One Time Upgrade' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','LCN')
else:
    Product.AllowAttrValues('Migration_Product_Choices','LCN')

if 'OPM' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','OPM')
else:
    Product.AllowAttrValues('Migration_Product_Choices','OPM')

if 'EBR' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','EBR')
else:
    Product.AllowAttrValues('Migration_Product_Choices','EBR')

if 'ELCN' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','ELCN')
else:
    Product.AllowAttrValues('Migration_Product_Choices','ELCN')

if 'Orion Console' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','Orion_Console')
else:
    Product.AllowAttrValues('Migration_Product_Choices','Orion_Console')

if 'EHPM/EHPMX/ C300PM' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','EHPM_C300PM')
else:
    Product.AllowAttrValues('Migration_Product_Choices','EHPM_C300PM')

if 'TPS to Experion' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','TPS_to_Experion')
else:
    Product.AllowAttrValues('Migration_Product_Choices','TPS_to_Experion')

if isHWSWSelected or 'TCMI' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','TCMI')
else:
    Product.AllowAttrValues('Migration_Product_Choices','TCMI')

if 'C200 Migration' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','C200_Migration')
else:
    Product.AllowAttrValues('Migration_Product_Choices','C200_Migration')

if 'EHPM HART IO' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','EHPM_HART_IO')
else:
    Product.AllowAttrValues('Migration_Product_Choices','EHPM_HART_IO')
if 'Integrated Automation Assessment (IAA)' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','Integrated_Automation_Assessment_IAA')
else:
    Product.AllowAttrValues('Migration_Product_Choices','Integrated_Automation_Assessment_IAA')

if 'xPM to C300 Migration' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','xPM_to_C300_Migration')
else:
    Product.AllowAttrValues('Migration_Product_Choices','xPM_to_C300_Migration')

if 'FSC to SM' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','FSC_to_SM')
else:
    Product.AllowAttrValues('Migration_Product_Choices','FSC_to_SM')
    
if 'FSC to SM IO Migration' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','FSC_to_SM_IO_Migration')
else:
    Product.AllowAttrValues('Migration_Product_Choices','FSC_to_SM_IO_Migration')

if 'CD Actuator I-F Upgrade' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','CD_Actuator_IF_Upgrade')
else:
    Product.AllowAttrValues('Migration_Product_Choices','CD_Actuator_IF_Upgrade')
    
if 'LM to ELMM ControlEdge PLC' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','LM_ELMM_ControlEdge_PLC')
else:
    Product.AllowAttrValues('Migration_Product_Choices','LM_ELMM_ControlEdge_PLC')

if 'CB-EC Upgrade to C300-UHIO' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','CB-EC_Upgrade_to_C300-UHIO_Objects')
else:
    Product.AllowAttrValues('Migration_Product_Choices','CB-EC_Upgrade_to_C300-UHIO_Objects')

if 'FDM Upgrade' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','FDM_Upgrade')
else:
    Product.AllowAttrValues('Migration_Product_Choices','FDM_Upgrade')

if 'XP10 Actuator Upgrade' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','XP10_Actuator_Upgrade')
else:
    Product.AllowAttrValues('Migration_Product_Choices','XP10_Actuator_Upgrade')
if '3rd Party PLC to ControlEdge PLC/UOC' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','3rd_Party_PLC_to_ControlEdge_PLC/UOC')
else:
    Product.AllowAttrValues('Migration_Product_Choices','3rd_Party_PLC_to_ControlEdge_PLC/UOC')

if isHWSWSelected or 'Graphics Migration' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','Graphics_Migration')
else:
    Product.AllowAttrValues('Migration_Product_Choices','Graphics_Migration')

if 'Virtualization System' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','Virtualization_System_Migration')
else:
    Product.AllowAttrValues('Migration_Product_Choices','Virtualization_System_Migration')
    
if 'Generic System' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','Generic_System_Migration')
else:
    Product.AllowAttrValues('Migration_Product_Choices','Generic_System_Migration')
    
if 'QCS RAE Upgrade' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','QCS_RAE_Upgrade')
else:
    Product.AllowAttrValues('Migration_Product_Choices','QCS_RAE_Upgrade')

if 'CWS RAE Upgrade' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','CWS_RAE_Upgrade')
else:
    Product.AllowAttrValues('Migration_Product_Choices','CWS_RAE_Upgrade')

if 'TPA/PMD Migration' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','TPA/PMD_Migration')
else:
    Product.AllowAttrValues('Migration_Product_Choices','TPA/PMD_Migration')
# On click Configure on Project-->Migration (Migration) product, 'ELEPIU ControlEdge RTU Migration Engineering' should be an option to select under Products list -- Dhrumil Shah : CXCPQ-60040 :start
if isHWSWSelected or 'ELEPIU ControlEdge RTU Migration Engineering' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','ELEPIU_ControlEdge_RTU_Migration_Engineering')
else:
    Product.AllowAttrValues('Migration_Product_Choices','ELEPIU_ControlEdge_RTU_Migration_Engineering')#-- Dhrumil Shah : CXCPQ-60040 :end

if isLaborSelected or 'Spare Parts' in selectedProducts:
    Product.DisallowAttrValues('Migration_Product_Choices','Spare_Parts')
else:
    Product.AllowAttrValues('Migration_Product_Choices','Spare_Parts')

if len(selectedProducts) >1 :
    Product.AllowAttrValues('Migration_Product_Choices','Spare_Parts')
elif len( selectedProducts) ==1 :
    for product in selectedProducts:
        if product:
            Product.AllowAttrValues('Migration_Product_Choices','Spare_Parts')
        else:
            Product.DisallowAttrValues('Migration_Product_Choices','Spare_Parts')
else:
    Product.DisallowAttrValues('Migration_Product_Choices','Spare_Parts')