Product.Attr('SC_SP_Mismatch').AssignValue("1")
Pmessage=None
sp = Product.Attr('SC_Honeywell_Digital_Prime').GetValue()
CSContainer = Product.GetContainerByName("ComparisonSummary")
if CSContainer.Rows.Count>0:
    for crow in CSContainer.Rows:
        if crow.IsSelected: #scope removal selected
            crow['CY_Service_Product']=None
        else:#Inscope
            if crow['PY_Service_Prod_Status']=='Active': #If previous year SP is active but not configured in the module
                if sp != crow['Service_Product']:
                    crow['CY_Service_Product']=None
                    #Display Error message
                    Pmessage=crow['Service_Product']+' Service Product is not configured in the module.'
                    Product.Attr('SC_SP_Mismatch').AssignValue("0")
                else:
                    crow['CY_Service_Product']=crow['Service_Product']
            else:#Inactive previous year service product
                #validate replacement service product
                if crow['CY_Service_Product'] not in (None,''):
                    if sp != crow['CY_Service_Product']:
                        Pmessage=crow['CY_Service_Product']+' Service Product is not configured in the module.'
                        Product.Attr('SC_SP_Mismatch').AssignValue("0")
                else:
                    Pmessage='Please Choose the CY Service Product(Replacement Product) in Comparison Summary'
                    Product.Attr('SC_SP_Mismatch').AssignValue("0")
CSContainer.Calculate()
if Pmessage is not None:
    if not Product.Messages.Contains(Pmessage):
        Product.Messages.Add(Pmessage)

def getInt(n):
    try:
        return int(n)
    except:
        return 0

#Number of MSID recalculated
cont = Product.GetContainerByName("SC_MSID_Container")
count = 0
for row in cont.Rows:
    if row.IsSelected == True:
        count += 1
msidCount = Product.Attr('SC_Digital_Prime_MSID_Count').GetValue()
if getInt(msidCount) != count:
    Product.Attr('SC_Digital_Prime_MSID_Count').AssignValue(str(count))
    Product.Attr('SC_Num_of_MSID').AssignValue(str(count))