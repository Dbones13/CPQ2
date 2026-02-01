#Load Rack Size SIL2 Safety System IO Container
Product.Attr('HC900_Redundant_I/O_Rack_Power_Supplies').SelectValue('Yes')
CT_query = SqlHelper.GetList('select IO_Section,Input_Voting,Output_Validation from HC900_IO_DETAILS_OF_SIL2')
Product.Attr('HC900_Spare_I/O_Slots').AssignValue('0')
container =  Product.GetContainerByName('HC900_IO_Details_of_SIL2')
i=0
for row in CT_query:
    new_row=container.AddNewRow(False)
    new_row['IO_Section'] = row.IO_Section
    new_row['IO_Point_Quantity'] = '0'
    new_row['Barrier_TB'] = '0'
    new_row['Euro_TB'] = '0'
    new_row.GetColumnByName('Input_Voting').SetAttributeValue(row.Input_Voting)
    container.Rows[i].Product.Attr('HC900_Input_Voting').SelectDisplayValue(row.Input_Voting)
    new_row.GetColumnByName('Output_Validation').SetAttributeValue(row.Output_Validation)
    container.Rows[i].Product.Attr('HC900_Output_Validation').SelectDisplayValue(row.Output_Validation)
    i+=1
container.Calculate()

#Load Rack Size SIL2 Safety System
rack_container = Product.GetContainerByName('HC900_Rack_Size_Quantity_Cont')
list = ["4 I/O Slot Rack","8 I/O Slot Rack","12 I/O Slot Rack"]
if Quote.GetCustomField("IsR2QRequest").Content=='Yes':
    row_new = rack_container.AddNewRow(False)
    row_new["Rack Size"] = "8 I/O Slot Rack"
    row_new["Quantity"] = '0'
else:
    for i in range(3):
        row_new = rack_container.AddNewRow(False)
        row_new["Rack Size"] = list[i]
        row_new["Quantity"] = '0'
rack_container.Calculate()

#Load Non-SIL HC900 System IO Container
NSIL_query = SqlHelper.GetList("select IO_Section from HC900_IO_DETAILS where Condition = 'NonSIL'")
NSIL_container =  Product.GetContainerByName('HC900_IO_Details_of_Non-SIL')
for row in NSIL_query:
    new_row=NSIL_container.AddNewRow(False)
    new_row['IO_Section'] = row.IO_Section
    new_row['IO_Point_Quantity'] = '0'
    new_row['Barrier_TB'] = '0'
    new_row['Euro_TB'] = '0'
    new_row['RTP_1_Pt_0M'] = '0'
    new_row['RTP_2_Pt_5M'] = '0'
    new_row['RTP_5_Pt_0M'] = '0'
    new_row['Redun_UIO_Multiplier']='1' # Default UIO multiplier as 1 and set it to 2 when Redun UIO multiplier is Yes #CXCPQ-51170. Refer Attribute trigger
NSIL_container.Calculate()

#Load SIL2 Safety System Additional IO Container
SIL2_add_query = SqlHelper.GetList("select IO_Section from HC900_IO_DETAILS where Condition = 'SIL2'")
SIL2_add_container =  Product.GetContainerByName('HC900_Additional_IO_Details_of_SIL2')
for row in SIL2_add_query:
    new_row=SIL2_add_container.AddNewRow(False)
    new_row['IO_Section'] = row.IO_Section
    new_row['IO_Point_Quantity'] = '0'
    new_row['Barrier_TB'] = '0'
    new_row['Euro_TB'] = '0'
    new_row['RTP_1_Pt_0M'] = '0'
    new_row['RTP_2_Pt_5M'] = '0'
    new_row['RTP_5_Pt_0M'] = '0'
    new_row['Redun_UIO_Multiplier']='1' # Default UIO multiplier as 1 and set it to 2 when Redun UIO multiplier is Yes #CXCPQ-51170. Refer Attribute trigger
SIL2_add_container.Calculate()