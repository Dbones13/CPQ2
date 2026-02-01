def getContainer(Name):
    return Product.GetContainerByName(Name)

attrs = ["ExpProject_Que_Right","CE_Project_Questions_Cont"]
Product.ExecuteRulesOnce = True
for attr in attrs:
    container = getContainer(attr)
    Trace.Write(attr)
    if container.Rows.Count != 0:
        for row in container.Rows:
            if attr == 'ExpProject_Que_Right':
                row.SetColumnValue('NonStandard TC_Used', '0')
                row.GetColumnByName('NonStandard TC_Used').SetAttributeValue('No')
                row.SetColumnValue('Estimated_Project_Value_Cost', '2')
                row.GetColumnByName('Estimated_Project_Value_Cost').SetAttributeValue('$250K - $1M')
                row.SetColumnValue('Liquidated Damages Included', '0')
                row.GetColumnByName('Liquidated Damages Included').SetAttributeValue('No')
                for col_name in ['Number of Subcontracts', 'Number of Extra Progress Reports or Meetings', 'Project Duration in weeks', 'FAT Duration in weeks', 'SAT Duration in weeks']:
                    row.SetColumnValue(col_name, '0')
            if attr=="CE_Project_Questions_Cont":
                row.SetColumnValue('Project Category', '3')
                row.GetColumnByName('Project Category').SetAttributeValue('B')
                row.SetColumnValue('Project Type', 'Fixed Price')
                row.GetColumnByName('Project Type').SetAttributeValue('Fixed Price')
                row.SetColumnValue('Contracting Parties', '2')
                row.GetColumnByName('Contracting Parties').SetAttributeValue('Customer + EPC or Consultant')
                row.SetColumnValue('Internal Parties', '1')
                row.GetColumnByName('Internal Parties').SetAttributeValue('HPS')
                row.SetColumnValue('Internal Parties', 'HPS')
                row.GetColumnByName('Internal Parties').SetAttributeValue('HPS')
                row.SetColumnValue('Project Exeuction Locations', '2')
                row.GetColumnByName('Project Exeuction Locations').SetAttributeValue('Home +1')
                row.SetColumnValue('Project Team Size', '2')
                row.GetColumnByName('Project Team Size').SetAttributeValue('3 - 5  Members')
                #row.GetColumnByName('Cabinet').SetAttributeValue('Dual Access')
            row.Calculate()
            container.Calculate()
Product.ExecuteRulesOnce = False