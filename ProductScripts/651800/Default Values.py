from GS_CyberProductModule import CyberProduct
from System import DateTime

cyber = CyberProduct(Quote, Product, TagParserQuote)
excecutionCountry = cyber.getExecutionCountry()
salesOrg = Quote.GetCustomField('Sales Area').Content
currentYear = DateTime.Now.Year
if excecutionCountry:
    
    Product.Attr('GENERIC_SYSTEM_Execution_Country').SelectDisplayValue(str(excecutionCountry))
    Product.Attr('GENERIC_SYSTEM_PRODUCTIVITY').AssignValue('1')
    Product.Attr('Sales_Org_Generic').AssignValue(str(salesOrg))
    Product.Attr('GENERIC_SYSTEM_Execution_Year').AssignValue(str(currentYear))

    
    Product.Attr('SMX_Execution_Country').SelectDisplayValue(str(excecutionCountry))
    Product.Attr('SMX_PRODUCTIVITY').AssignValue('1')
    Product.Attr('Sales_Org_SMX').AssignValue(str(salesOrg))
    Product.Attr('SMX_Execution_Year').AssignValue(str(currentYear))
	

    Product.Attr('Assessments_Execution_Country').SelectDisplayValue(str(excecutionCountry))
    Product.Attr('ASSESSMENT_PRODUCTIVITY').AssignValue('1')
    Product.Attr('Sales_Org_Assessments').AssignValue(str(salesOrg))
    Product.Attr('Assessments_Execution_Year').AssignValue(str(currentYear))
	

    Product.Attr('MSS_Execution_Country').SelectDisplayValue(str(excecutionCountry))
    Product.Attr('MSS_PRODUCTIVITY').AssignValue('1')
    Product.Attr('Sales_Org_MSS').AssignValue(str(salesOrg))
    Product.Attr('MSS_Execution_Year').AssignValue(str(currentYear))
	

    Product.Attr('PCNH_Execution_Country').SelectDisplayValue(str(excecutionCountry))
    Product.Attr('PCN_PRODUCTIVITY').AssignValue('1')
    Product.Attr('Sales_Org_PCN').AssignValue(str(salesOrg))
    Product.Attr('PCNH_Execution_Year').AssignValue(str(currentYear))
	

    Product.Attr('CAC_Execution_Country').SelectDisplayValue(str(excecutionCountry))
    Product.Attr('CAC_PRODUCTIVITY').AssignValue('1')
    Product.Attr('Sales_Org_CAC').AssignValue(str(salesOrg))
    Product.Attr('CAC_Execution_Year').AssignValue(str(currentYear))

    Product.Attr('PM_Execution_Country').SelectDisplayValue(str(excecutionCountry))
    Product.Attr('PM_Adjustment_Productivity').AssignValue('1')
    Product.Attr('PM_Execution_Year').AssignValue(str(currentYear))