cont = Product.GetContainerByName("CBM_Pricing_Container")
cont1 = Product.GetContainerByName("CBM_Models_Cont")
for row in cont.Rows:
    for row1 in cont1.Rows:
        if row1['Product Family'] == row['Product Family']:
            row1['PY_LevelOffering'] = row['PY_LevelOffering']
            row1['PY_PMCBM'] = row['PY_PMCBM']
            row1['PY_ListPrice'] = row['PY_ListPrice']
            row1['CY_LevelOffering'] = row['CY_LevelOffering']
            row1['CY_PMCBM'] = row['CY_PMCBM']
            row1['CY_ListPrice'] = row['CY_ListPrice']
            if float(row1['PY_ListPrice']) > float(row1['CY_ListPrice']):
                row1['Comments'] = "Scope Reduction"
            elif float(row1['PY_ListPrice']) < float(row1['CY_ListPrice']):
                row1['Comments'] = "Scope Addition"
            elif float(row1['PY_ListPrice']) == float(row1['CY_ListPrice']):
                row1['Comments'] = "No Scope Change"
cont1.Calculate()