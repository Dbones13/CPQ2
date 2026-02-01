lv_System_Type=Product.Attributes.GetByName("HC900_System_Type").GetValue()
if lv_System_Type=='SIL2 Safety System':
    specific_OutputValidation = {'Analog Outputs (4 channel, 10 modules/rack)': ['900G02-0202', '900G03-0202', '900G04-0101', '900G32-0301','None'], 'Analog Outputs (8 channel, 5 modules/rack)': ['900G02-0202', '900G03-0202', '900G04-0101', '900G32-0301','None'],'Analog Outputs (16 channel, 2 modules/rack)':['900G02-0202', '900G03-0202', '900G04-0101', '900G32-0301','None'],'Digital Outputs -Relay (8 channel)':['900G32-0301', '900A16-0103', '900A01-0202', 'Process I/O (No Validation)','None'],'Digital Outputs -24 VDC (16 channel)':['900G04-0101', '900G03-0202', '900A16-0103', '900A01-0202', 'None'],'Digital Outputs -24 VDC (32 channel)':['900G04-0101', '900G03-0202', '900A16-0103', '900A01-0202','None'],'Digital Outputs -120/240 VAC (8 channel)':['900G04-0101', '900G02-0202', '900A16-0103', '900A01-0202', '900G32-0301','None']}
    input_voting_list = ["Analog Inputs (Universal, 8 channel)","Analog Input HI level 100 millisecond (16 channel)","Digital Inputs - contact (16 channel)","Digital Inputs -24 VDC (16 channel)","Digital Inputs -24 VDC (32 channel)","Digital Inputs -120/240 VAC (16 channel)","Digital inputs -120/240 VAC - 125 VDC (16 channel isolated)"]

    def disallow(location, dropdownlist):
        if location:
            for i in dropdownlist:
                if i.ValueCode in location:
                    i.Allowed = False
                elif i.ValueCode not in location:
                    i.Allowed = True

    deliverables = Product.GetContainerByName('HC900_IO_Details_of_SIL2')
    for row in deliverables.Rows:
        if Quote.GetCustomField("R2QFlag").Content != 'Yes':
            if specific_OutputValidation.get(row['IO_Section']):
                out_valid= row.GetColumnByName('Output_Validation')
                value_list = out_valid.ReferencingAttribute.Values
                disallow(specific_OutputValidation[row['IO_Section']], value_list)
            if row['IO_Section'] in input_voting_list:
                input_voting = row.GetColumnByName('Input_Voting')
                value_list1 = input_voting.ReferencingAttribute.Values
                disallow(["None"], value_list1)
        else:
            r2qspecific_OutputValidation = {'Analog Outputs (16 channel, 2 modules/rack)':['900A01-0202','900A16-0103','900G02-0202', '900G03-0202', '900G04-0101', '900G32-0301','None'],'Digital Outputs -24 VDC (32 channel)':['900G04-0101', '900G03-0202','900G02-0202', '900G32-0301', '900A16-0103', '900A01-0202','None']}
            r2qinput_voting_list = {'Analog Input HI level 100 millisecond (16 channel)':['Safety I/O (2oo3)','Safety I/O (1oo2)','None'],'Digital Inputs -24 VDC (32 channel)':['Safety I/O (2oo3)','Safety I/O (1oo2)','None']}

            if r2qspecific_OutputValidation.get(row['IO_Section']):
                out_valid= row.GetColumnByName('Output_Validation')
                value_list = out_valid.ReferencingAttribute.Values
                disallow(r2qspecific_OutputValidation[row['IO_Section']], value_list)
            if row['IO_Section'] in r2qinput_voting_list:
                input_voting = row.GetColumnByName('Input_Voting')
                value_list1 = input_voting.ReferencingAttribute.Values
                disallow(r2qinput_voting_list[row['IO_Section']], value_list1)
    deliverables.Calculate()