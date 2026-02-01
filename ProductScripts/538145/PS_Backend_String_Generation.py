partgeneratedcode = "AS-UTRACS-M-S-NN-SS-NN-DD-AD-00-06-01-02-01-02-04-00-00-SS-N-S-P-001-N"

def ClassCalculation():
    class_0_new=[]
    class_1_new=[]
    class_2_new=[]
    class_3_new=[]
    #Calculation for a new License
    if  Product.Attr("SC_ESVT").GetValue() != '' : class_0_new.append(int(Product.Attr("SC_ESVT").GetValue()))
    if  Product.Attr("SC_Experion_PKS").GetValue() != '' : class_1_new.append(int(Product.Attr("SC_Experion_PKS").GetValue()))
    if  Product.Attr("SC_Honeywell_TPS").GetValue() != '' : class_1_new.append(int(Product.Attr("SC_Honeywell_TPS").GetValue()))
    if  Product.Attr("SC_Experion_LX_Plantcruise").GetValue() != '' : class_1_new.append(int(Product.Attr("SC_Experion_LX_Plantcruise").GetValue()))
    if  Product.Attr("SC_Honeywell_Safety_Manager_S300").GetValue() != '' : class_2_new.append(int(Product.Attr("SC_Honeywell_Safety_Manager_S300").GetValue()))
    if  Product.Attr("SC_Triconex").GetValue() != '' : class_2_new.append(int(Product.Attr("SC_Triconex").GetValue()))
    if  Product.Attr("SC_FSC").GetValue() != '' : class_2_new.append(int(Product.Attr("SC_FSC").GetValue()))
    if  Product.Attr("SC_Experion_SCADA").GetValue() != '' : class_2_new.append(int(Product.Attr("SC_Experion_SCADA").GetValue()))
    if  Product.Attr("SC_APC_Aspen_DMC_or_ProfitSuite").GetValue() != '' : class_2_new.append(int(Product.Attr("SC_APC_Aspen_DMC_or_ProfitSuite").GetValue()))
    if  Product.Attr("SC_Honeywell_ControlEdge_PLC").GetValue() != '' : class_2_new.append(int(Product.Attr("SC_Honeywell_ControlEdge_PLC").GetValue()))
    if  Product.Attr("SC_Uniformance_PHD").GetValue() != '' : class_3_new.append(int(Product.Attr("SC_Uniformance_PHD").GetValue()))
    if  Product.Attr("SC_OSI_PI").GetValue() != '' : class_3_new.append(int(Product.Attr("SC_OSI_PI").GetValue()))
    if  Product.Attr("SC_SPI_Tools").GetValue() != '' : class_3_new.append(int(Product.Attr("SC_SPI_Tools").GetValue()))
    if  Product.Attr("SC_RS_Logix").GetValue() != '' : class_3_new.append(int(Product.Attr("SC_RS_Logix").GetValue()))
    if  Product.Attr("SC_Custom_User_Defined_System").GetValue() != '' : class_3_new.append(int(Product.Attr("SC_Custom_User_Defined_System").GetValue()))
    sum_class_0=sum(class_0_new)
    sum_class_1=sum(class_1_new)
    sum_class_2=sum(class_2_new)
    sum_class_3=sum(class_3_new)
    class_0_tier1_new=0
    class_0_tier2_new=0
    class_1_tier1_new=0
    class_1_tier2_new=0
    class_2_tier1_new=0
    class_2_tier2_new=0
    class_3_tier1_new=0
    class_3_tier2_new=0
    if sum_class_0 ==1:
        class_0_tier1_new=1
        class_0_tier2_new=0
    if sum_class_0 >1:
        class_0_tier1_new=1
        class_0_tier2_new=sum_class_0-1
    if sum_class_1 ==1:
        class_1_tier1_new=1
        class_1_tier2_new=0
    if sum_class_1 >1:
        class_1_tier1_new=1
        class_1_tier2_new=sum_class_1-1
    if sum_class_2 ==1:
        class_2_tier1_new=1
        class_2_tier2_new=0
    if sum_class_2 >1:
        class_2_tier1_new=1
        class_2_tier2_new=sum_class_2-1
    if sum_class_3 ==1:
        class_3_tier1_new=1
        class_3_tier2_new=0
    if sum_class_3 >1:
        class_3_tier1_new=1
        class_3_tier2_new=sum_class_3-1
    table8 = class_1_tier1_new+(class_0_tier1_new*2)
    table9 = class_1_tier2_new+(class_0_tier2_new*2)
    table10 = class_2_tier1_new
    table11 = class_2_tier2_new
    table12 = class_3_tier1_new
    table13 = class_3_tier2_new
    table14 = 0
    table15 = 0
    table16 = 0
    if table8<10: table8='0'+str(table8)
    if table9<10: table9='0'+str(table9)
    if table10<10: table10='0'+str(table10)
    if table11<10: table11='0'+str(table11)
    if table12<10: table12='0'+str(table12)
    if table13<10: table13='0'+str(table13)
    if table14<10: table14='0'+str(table14)
    if table15<10: table15='0'+str(table15)
    if table16<10: table16='0'+str(table16)
    final_result='-'+str(str(table8)+'-'+str(table9)+'-'+str(table10)+'-'+str(table11)+'-'+str(table12)+'-'+str(table13)+'-'+str(table14)+'-'+str(table15)+'-'+str(table16))
    return final_result

####Part1####
partString = "AS-UTRACS" # Using S at last for standard model (HardCoded)
partString += "-N"       #because of New License (HardCoded)
partString += "-S"       #because of Standard Pricing Model (HardCoded)
partString += "-NN"      #Base System (HardCoded)
partString += "-SS"      #System Factor (HardCoded)
partString += "-NN"      #System Upgrade Factor(HardCoded)

####Part2####
users = Product.Attr("SC_Number_of_Concurrent_Users").GetValue()
if users == "Up to 5 users":
    partString += "-AA"
elif users == "6 to 10 user":
    partString += "-BB"
elif users == "11 to 15 user":
    partString += "-CC"
elif users == "More than 15 user":
    partString += "-DD"
else:
    partString += "NN"

####Part3####
partString += "-NN"      #User Size Upgrade Factor (HardCoded)

####Part4####
partString += ClassCalculation()         #Calculated Value based on UI

####Part5####
partString += "-NN"      #Prev Base System (HardCoded)

####Part6####
L4Trace = Product.Attr("SC_L4_Trace_Server_Option").GetValue()
if L4Trace == "Yes":
    partString += "-A"
else:
    partString += "-N"

####Part7####
BookingCountry = ""
if Quote:
    BookingCountry = Quote.GetCustomField("Booking Country").Content
if BookingCountry != "":
    y = ""
    x = BookingCountry.Split()
    for i in x:
        y += i.capitalize() + " "
        BookingCountry = y[:-1]
if BookingCountry == "India" or BookingCountry == "China":
    partString += "-A"
else:
    partString += "-S"

####Part8####
License = Product.Attr("SC_License_type").GetValue()
if License == "Term":
    partString += "-Q"
else:
    partString += "-P"

####Part9####
partString += "-001"     #Quantity always 1

####Part10####
L4Trace = Product.Attr("SC_L4_Trace_Server_Option").GetValue()
if L4Trace == "Yes":
    partString += "-A"
else:
    partString += "-N"



Trace.Write(len(partgeneratedcode))
Trace.Write(len(partString))
Trace.Write(partString)
#AS-UTRACS-N-S-NN-SS-NN-AA-NN-00-06-01-02-01-02-04-00-00-NN-N-A-P-001-N
#AS-UTRACS-N-S-NN-SS-NN-CC-NN-00-06-01-02-01-02-04-00-00-NN-A-A-Q-001-A
Product.Attr("SC_Trace_Backend_String").AssignValue(partString)