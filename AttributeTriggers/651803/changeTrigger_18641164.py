patchingAttr = Product.Attr('Patching and Anti-Virus Required').GetValue()
onsiteSupport = Product.Attr('Onsite Support Implementation Services').GetValue()
Trace.Write("onsiteSupport---->bhc163--->"+str(onsiteSupport))
if onsiteSupport != "Yes":
	Product.DisallowAttr('Empty Section for MSS')
	Product.DisallowAttr('Execution Country')
	'''Product.DisallowAttr('FAT Document Verification and Execution')
	Product.DisallowAttr('FDS & DDS Documentation Required')
	Product.DisallowAttr('SAT Document Verification and Execution')'''
	Product.Attr('FDS & DDS Documentation Required').Access = AttributeAccess.Hidden
	Product.Attr('FAT Document Verification and Execution').Access = AttributeAccess.Hidden
	Product.Attr('SAT Document Verification and Execution').Access = AttributeAccess.Hidden
	Product.GetContainerByName('Activities').Rows.Clear()
	Product.DisallowAttr('Activities')
else:
	Product.AllowAttr('Empty Section for MSS')
	Product.AllowAttr('Execution Country')
	'''Product.AllowAttr('FAT Document Verification and Execution')
	Product.AllowAttr('FDS & DDS Documentation Required')
	Product.AllowAttr('SAT Document Verification and Execution')'''
	Product.Attr('FDS & DDS Documentation Required').Access = AttributeAccess.ReadOnly
	Product.Attr('FAT Document Verification and Execution').Access = AttributeAccess.ReadOnly
	Product.Attr('SAT Document Verification and Execution').Access = AttributeAccess.ReadOnly
	Product.AllowAttr('Activities')

if onsiteSupport != "Yes" or patchingAttr!= "Yes":
	Product.DisallowAttr('Microsoft Updates Install')
else:
	Product.AllowAttr('Microsoft Updates Install')


if onsiteSupport != "Yes" or patchingAttr!= "Yes":
	Trace.Write('---------iff--wind------')
	Product.DisallowAttr('Number of Windows Assets')
else:
	Trace.Write('---------wind------')
	Product.AllowAttr('Number of Windows Assets')
	Product.Attr('Number of Windows Assets').AssignValue('0')
	
from GS_Populate_Labour_WTW import populateWTW
from System import DateTime
import GS_UTILITY_CONTAINER_SORT as con

activity = Product.GetContainerByName('Activities')

def getExecutionCountry():
	salesOrg = Quote.GetCustomField('Sales Area').Content
	currency = Quote.GetCustomField('Currency').Content
	query = SqlHelper.GetFirst("select Execution_County from NEW_EXECUTION_COUNTRY_SALES_ORG_MAPPING where Sales_Area = '{}' and Currency = '{}'".format(salesOrg,currency))
	if query is not None:
		Execution_County = query.Execution_County
	return Execution_County,salesOrg,currency

excecutionCountry,salesOrg,currency = getExecutionCountry()
currentYear = DateTime.Now.Year

if Product.Attr('Onsite Support Implementation Services').GetValue() == '':
	for row in activity.Rows:
		if row['Identifier'] == 'A5':
			activity.DeleteRow(row.RowIndex)
			break