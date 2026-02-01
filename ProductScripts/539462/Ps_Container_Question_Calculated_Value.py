def getContainer(Name):
    return Product.GetContainerByName(Name)

def getRowData(container,column):
    Container = getContainer(container)
    for row in Container.Rows:
        return row[column]
		
if Product.Attr('ATT_NUMXPMC300').GetValue() != "0" and Product.Attr('ATT_NUMXPMC300').GetValue() != "": 
        xPMC300MigrationCont = getContainer('xPM_C300_Migration_Configuration_Cont')
        for row in xPMC300MigrationCont.Rows:
            if row['xPM_C300_split_of_xPM_CL_into_simple_and_complex'] != "Yes":#Split PM Calculated value
                PM_CL = row['xPM_C300_Number_of_xPM_CL']
                if PM_CL != "" and PM_CL != "0":
                    PM_CLNo = int(PM_CL)
                    simplePMCL = int(round(PM_CLNo * 0.7))
                    complexPMCL = PM_CLNo - simplePMCL
                    row.SetColumnValue('xPM_C300_Number_of_Simple_xPM_CL', str(simplePMCL))
                    row.SetColumnValue('xPM_C300_Number_of_Complex_xPM_CL', str(complexPMCL))
                else:
                    row.SetColumnValue('xPM_C300_Number_of_Simple_xPM_CL', str(0))
                    row.SetColumnValue('xPM_C300_Number_of_Complex_xPM_CL', str(0))
            if row['xPM_C300_split_of_AM_CL_into_simple_medium_complex'] != "Yes":#Split AM Calculated value
                AM_CL = row['xPM_C300_Number_of_AM_CL']
                if AM_CL != "" and AM_CL != "0":
                    AM_CLNo = int(AM_CL)
                    simpleAMCL = int(round(AM_CLNo * 0.4))
                    mediumAMCL = int(round(AM_CLNo * 0.3))
                    complexAMCL = AM_CLNo - simpleAMCL - mediumAMCL
                    row.SetColumnValue('xPM_C300_Number_of_Simple_AM_CL', str(int(simpleAMCL)))
                    row.SetColumnValue('xPM_C300_Number_of_medium_AM_CL', str(int(mediumAMCL)))
                    row.SetColumnValue('xPM_C300_Number_of_complex_AM_CL', str(int(complexAMCL)))
                else:
                    row.SetColumnValue('xPM_C300_Number_of_Simple_AM_CL', str(0))
                    row.SetColumnValue('xPM_C300_Number_of_medium_AM_CL', str(0))
                    row.SetColumnValue('xPM_C300_Number_of_complex_AM_CL', str(0))
        xPMC300MigrationCont.Calculate()