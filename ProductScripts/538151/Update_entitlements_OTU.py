"""ent = SqlHelper.GetList("select * from CT_SC_ENTITLEMENTS_DATA where ServiceProduct = N'{0}'".format('OTU'))
con = Product.GetContainerByName('SP_Entitle_ScopeSumm_OTU_SESP')
con.Rows.Clear()
for i in ent:
    row = con.AddNewRow(False)
    row['Service Product'] = 'Software Upgrades'
    row['Entitlement'] = i.Entitlement
    if i.IsMandatory == 'TRUE':
    	row['Type'] = 'Mandatory'
    else:
        row['Type'] = 'Optional'"""
con = Product.GetContainerByName('SP_Entitle_ScopeSumm_OTU_SESP')
con.Rows.Clear()
row = con.AddNewRow(False)
row['Service Product'] = 'Software Upgrades'
row['Entitlement'] = 'Software Upgrades'
row['Type'] = 'Mandatory'