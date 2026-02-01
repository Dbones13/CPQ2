#import System.Decimal as D
from GS_SMIOComponents import IOComponents
#attrs = GS_SM_CG_Component_Attribute.AttrStorage(Product)
#Trace.Write("output="+str(output1))
parts_dict = {}
def roundup(n):
    res = int(n)
    return res if res == n else res+1
def get_partstskuni(Product,parts_dict):
    output = IOComponents(Product)
    output1 = output.getSumMarsh()
    if Product.Name=="SM Control Group":
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
        Trace.Write("hi:"+str(iota))
        marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue
        Trace.Write("hello:"+str(marshaling))
        if iota == "RUSIO" and marshaling == "Hardware Marshalling with Other":
            digout = Product.GetContainerByName("SM_IO_Count_Analog_Input_Cont")
            for row in digout.Rows:
                if row["Analog Input Type"] == "SAI(1)FIRE 3-4 wire current UIO (0-5000)":
                    var1 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
                    var2 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0
                    #Trace.Write(var1)
                    #Trace.Write(var2)
                    #Trace.Write(row["Analog Input Type"])
                    if int(var1) == 0 and int(var2) == 0:
                        #Trace.Write("Anju:"+str(var1))
                        #Trace.Write("Anju2:"+str(var2))
                        Quantity=roundup(float(output1/16.0))
                        Trace.Write(Quantity)
                        parts_dict["FC-TSKUNI-1624"]={'Quantity':int(Quantity),'Description':'SM RIO Safe FTA Knife, 24Vdc,16ch'}
                        #Trace.Write(parts_dict["FC-TSKUNI-1624"])
    elif Product.Name == "SM Remote Group":
        Trace.Write(Product.Name)
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        Trace.Write("hi:"+str(iota))
        Enclosure_type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        Trace.Write("Enclosure_type:"+str(Enclosure_type))
        marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue
        Trace.Write("hello:"+str(marshaling))
        if Enclosure_type == "Cabinet":
            if iota == "RUSIO" and marshaling == "Hardware Marshalling with Other":
                Trace.Write(iota)
                Trace.Write(marshaling)
                digout = Product.GetContainerByName("SM_RG_IO_Count_Analog_Input_Cont")
                #Trace.Write(digout)
                for row in digout.Rows:
                    if row["Analog_Input_Type"] == "SAI(1)FIRE 3-4 wire current  UIO  (0-5000)":
                        var3 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
                        var4 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
                        #Trace.Write(var3)
                        #Trace.Write(var4)
                        #Trace.Write(row["Analog_Input_Type"])
                        if int(var3) == 0 and int(var4) == 0:
                            Quantity=roundup(float(output1/16.0))
                            Trace.Write(Quantity)
                            parts_dict["FC-TSKUNI-1624"]={'Quantity':int(Quantity),'Description':'SM RIO Safe FTA Knife, 24Vdc,16ch'}
    return parts_dict
#Trace.Write("A:"+str(get_partstskuni(output1,parts_dict, attrs)))
def get_partstspkuni(Product,parts_dict):
    output = IOComponents(Product)
    output1 = output.getSumMarsh()
    if Product.Name=="SM Control Group":
        iota = Product.GetContainerByName("SM_CG_Common_Questions_Cont").Rows[0].GetColumnByName("SM_Universal_IOTA").DisplayValue
        Trace.Write("hi:"+str(iota))
        
        marshaling = Product.GetContainerByName("SM_CG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue
        Trace.Write("hello:"+str(marshaling))
        if iota == "RUSIO" and marshaling == "Hardware Marshalling with Other":
            digout = Product.GetContainerByName("SM_IO_Count_Analog_Input_Cont")
            for row in digout.Rows:
                if row["Analog Input Type"] == "SAI(1)FIRE 3-4 wire current UIO (0-5000)":
                    var1 = row["Red (NIS)"] if row["Red (NIS)"] != "" else 0
                    var2 = row["Non Red (NIS)"] if row["Non Red (NIS)"] != "" else 0
                    if int(var1) > 0 and int(var2) > 0:
                        Quantity=roundup(float(output1/16.0))
                        Trace.Write(Quantity)
                        parts_dict["FC-TSPKUNI-1624"]={'Quantity':int(Quantity),'Description':'SM RIO Safe FTA Knife, 3-wire,24Vdc,16ch'}
    elif Product.Name == "SM Remote Group":
        iota = Product.Attr("SM_Universal_IOTA_Type").GetValue()
        Trace.Write("hi:"+str(iota))
        Enclosure_type = Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName('Enclosure_Type').DisplayValue
        Trace.Write("Enclosure_type:"+str(Enclosure_type))
        marshaling = Product.GetContainerByName("SM_RG_Cabinet_Details_Cont_Left").Rows[0].GetColumnByName("Marshalling_Option").DisplayValue
        Trace.Write("hello:"+str(marshaling))
        if Enclosure_type == "Cabinet":
            if iota == "RUSIO" and marshaling == "Hardware Marshalling with Other":
                digout = Product.GetContainerByName("SM_RG_IO_Count_Analog_Input_Cont")
                for row in digout.Rows:
                    if row["Analog_Input_Type"] == "SAI(1)FIRE 3-4 wire current  UIO  (0-5000)":
                        var3 = row["Red_NIS"] if row["Red_NIS"] != "" else 0
                        var4 = row["Non_Red_NIS"] if row["Non_Red_NIS"] != "" else 0
                        if int(var3) > 0 and int(var4) > 0:
                            Quantity=roundup(float(output1/16.0))
                            Trace.Write(Quantity)
                            parts_dict["FC-TSPKUNI-1624"]={'Quantity':int(Quantity),'Description':'SM RIO Safe FTA Knife, 3-wire,24Vdc,16ch'}
    return parts_dict

'''fun=get_partstskuni(Product,parts_dict)
Trace.Write(str(fun))
fun1=get_partstspkuni(Product,parts_dict)
Trace.Write(str(fun1))'''