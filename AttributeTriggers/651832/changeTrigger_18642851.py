gesloc = Product.Attr('MSID_GES_Location').GetValue()
gLoc = {'GES Egypt':'GESEgypt','GES Uzbekistan':'GESUzbekistan','GES Romania':'GESRomania','GES India':'GESIndia','GES China':'GESChina','None':'None'}
if gesloc:
    Product.GetContainerByName('SM_Labor_Cont').Rows[0].SetColumnValue('GES_Location',gLoc.get(str(gesloc)))
    Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('GES_Location').SetAttributeValue(str(gesloc))
    Product.GetContainerByName('SM_Labor_Cont').Rows[0].SetColumnValue('Implementation_Methodology','StandardBuildEstimate')
    Product.GetContainerByName('SM_Labor_Cont').Rows[0].GetColumnByName('Implementation_Methodology').SetAttributeValue('Standard Build Estimate')