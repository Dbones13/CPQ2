#---------------------------------------------------------------------------------------------------------
#					Change History Log
#---------------------------------------------------------------------------------------------------------
# Description: Main script for R2Q Parts and Spot Quote product addition
#----------------------------------------------------------------------------------------------------------
# Date 			Name					    Version   Comment
# 05-07-2023	Saswat Kumar Mishra			8		  Initial Creation
class CL_R2Q_Integration_ErrorMessages:
    ProductAdditionError = "Error occured while adding product(s)."
    OtherError = "Unknown error occured during quote processing."
    ProposalDocGenerationError = "Error occured during generating documents."
    GetItemError = "Error occured while fetching products from SFDC."
    InvalidQuote = "Not a valid quote for R2Q Parts and Spot."
    MultiExecutionError = "R2Q automation script can execute only once."
    Rejected = "Quote Rejected."
    R2Q_SalesPriceError = "Error occured while sales price calculation"

class CL_R2Q_Integration_SuccessMessages:
    ProposalDocGenerated = "Proposal document has been generated successfully."
    ApprovalInitiated = "Approval request sent to SFDC successfully."
    Submitted = "Quote submitted to customer successfully"
    ItemsFetched = "Successfully fetched products from SFDC."