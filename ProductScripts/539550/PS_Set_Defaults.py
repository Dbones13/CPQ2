import GS_CE_Utils
import datetime
try:
    GS_CE_Utils.setContainerDefaults(Product)
except:
    pass

#Defaults for Labor tab
current_year = datetime.datetime.now().year
if Quote:
    if Quote.GetCustomField('EGAP_Contract_Start_Date').Content != "": #If there is a Contract Start Date in the quote
        c_start_date = Quote.GetCustomField('EGAP_Contract_Start_Date').Content
        contract_start = int("20"+c_start_date[-2:])
        if contract_start > current_year+3: #Maxes out at 3 years in the future. Can't go beyond that.
            contract_start = current_year+3
    else:
        contract_start = current_year
else:
    contract_start = current_year
Product.Attr('CE PMD Engineering Execution Year').SelectValue(str(contract_start), True)
Product.Attr('PMD_CD_LD_Engineering_Execution_Year').SelectValue(str(contract_start), True)