msidContainer = Product.GetContainerByName("Migration_MSID_Selection_Container")
totalManHrs = 0
for row in msidContainer.Rows:
    msidProduct = row.Product
    msidOPMContainer = msidProduct.GetContainerByName('MSID_Labor_OPM_Engineering')
    msidLCNContainer = msidProduct.GetContainerByName('MSID_Labor_LCN_One_Time_Upgrade_Engineering')
    msidPMContainer = msidProduct.GetContainerByName('MSID_Labor_Project_Management')
    for row in msidOPMContainer.Rows:
        if (row['Deliverable'] == 'Total'):
            totalManHrs =  totalManHrs + float(row['Final_Hrs'])
            break
    for row in msidLCNContainer.Rows:
        if (row['Deliverable'] == 'Total'):
            totalManHrs = totalManHrs + float(row['Final_Hrs'])
            break
    for row in msidPMContainer.Rows:
        if (row['Deliverable'] == 'Total'):
            totalManHrs = totalManHrs +  float(row['Final_Hrs'])
            break

Quote.GetCustomField('Migration_Total_Man_Hrs').Content = str(totalManHrs)