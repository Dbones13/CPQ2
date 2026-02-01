#Function returns True when Partnumber is VC product
def IsVCitem(in_partnumber):
    isVCitem =SqlHelper.GetFirst("select 1 from Products where IsSyncedFromBackOffice = 'True' and IsSimple = 'False' and product_catalog_code = '{}'".format(in_partnumber))
    if isVCitem:
        return True
    else:
        return False