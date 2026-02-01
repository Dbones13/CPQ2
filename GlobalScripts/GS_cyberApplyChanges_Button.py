from GS_CyberProductModule import CyberProduct
cyber = CyberProduct(Quote, Product, TagParserQuote)

if Product.GetContainerByName('Generic_System_Activities').Rows.Count > 0 and Product.GetContainerByName('Generic_System_Activities').HasSelectedRow:
	cyber.applyparts_function('Generic_System_Activities','GENERIC_SYSTEM_Execution_','Execution_Year_Change_Generic')

if Product.GetContainerByName('AR_SMX_Activities').Rows.Count > 0 and Product.GetContainerByName('AR_SMX_Activities').HasSelectedRow:
	cyber.applyparts_function('AR_SMX_Activities','SMX_Execution_','Execution_Year_Change_SMX')

if Product.GetContainerByName('AR_Assessment_Activities').Rows.Count > 0 and Product.GetContainerByName('AR_Assessment_Activities').HasSelectedRow:
	cyber.applyparts_function('AR_Assessment_Activities','Assessments_Execution_','Execution_Year_Change_Ass')

if Product.GetContainerByName('AR_CAC_Activities').Rows.Count > 0 and Product.GetContainerByName('AR_CAC_Activities').HasSelectedRow:
	cyber.applyparts_function('AR_CAC_Activities','CAC_Execution_','Execution_Year_Change_CAC')

if Product.GetContainerByName('AR_MSS_Activities').Rows.Count > 0 and Product.GetContainerByName('AR_MSS_Activities').HasSelectedRow:
	cyber.applyparts_function('AR_MSS_Activities','MSS_Execution_','Execution_Year_Change_MSS')

if Product.GetContainerByName('AR_PCNH_Activities').Rows.Count > 0 and Product.GetContainerByName('AR_PCNH_Activities').HasSelectedRow:
	cyber.applyparts_function('AR_PCNH_Activities','PCNH_Execution_','Execution_Year_Change_PCN')

if Product.GetContainerByName('Cyber_Labor_Project_Management').Rows.Count > 0 and Product.GetContainerByName('Cyber_Labor_Project_Management').HasSelectedRow:
	cyber.projectmanagement_ExecutionCountryTrigger()