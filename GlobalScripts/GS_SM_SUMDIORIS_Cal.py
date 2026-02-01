import math as m
def Get_SUMDIORIS(Product):
    if Product.Name == "SM Control Group":
        SUMDIORIS=0
        if 1: #iota== puio condition is removed
            #SUMDIORIS
            #digital input
            di_cont = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
            for row in di_cont.Rows:
                if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc DIO (0-5000)":
                    sdi_24vdc_dio_redis = row.GetColumnByName("Red (IS)").Value
            for row in di_cont.Rows:
                if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc Line Mon DIO (0-5000)":
                    sdi_24vdc_line_mon_dio_red = row.GetColumnByName("Red (IS)").Value
                
            #digital output
            do_cont = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont')
            for row in do_cont.Rows:
                if row.GetColumnByName("Digital Output Type").Value == "SDO(1) 24Vdc 500mA DIO (0-5000)":
                    sdo_24vdc_500ma_dioredis = row.GetColumnByName("Red (IS)").Value

            SDO_24vdc_500mA_uio_dio = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("Percent_Installed_Spare_IOs").Value
            if SDO_24vdc_500mA_uio_dio == "":
                SDO_24vdc_500mA_uio_dio = 0
                SDO_24vdc_500mA_uio_dio = int(SDO_24vdc_500mA_uio_dio)

            dict_1 ={"sdi_24vdc_dio_redis" : sdi_24vdc_dio_redis, "sdi_24vdc_line_mon_dio_red" : sdi_24vdc_line_mon_dio_red, "sdo_24vdc_500ma_dioredis" :sdo_24vdc_500ma_dioredis}

            for i in dict_1:
                if dict_1[i]  == "":
                    dict_1[i] = 0

            Trace.Write("sdi_24vdc_dio_redis: " + str(dict_1["sdi_24vdc_dio_redis"]))
            Trace.Write("24vdc dio line_mon_dio_red: " + str(dict_1["sdi_24vdc_line_mon_dio_red"]))
            Trace.Write("sdo_24vdc_500ma_dioredis: " + str(dict_1["sdo_24vdc_500ma_dioredis"]))
            #Trace.Write("SDO_24vdc_500mA_uio_dio" + str(SDO_24vdc_500mA_uio_dio))

            #calculation
            SUMDIORIS= (int(dict_1["sdi_24vdc_dio_redis"])+int(dict_1["sdi_24vdc_line_mon_dio_red"])+int(dict_1["sdo_24vdc_500ma_dioredis"]))*(1+float(SDO_24vdc_500mA_uio_dio)/100)
            Trace.Write("sumdioris cg: "+ str(float(SUMDIORIS)))
        return m.ceil(SUMDIORIS)
    if Product.Name == "SM Remote Group":
        SUMDIORIS=0
        if 1: #iota== puio condition is removed
            #SUMDIORIS
            #digital input
            di_cont = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
            for row in di_cont.Rows:
                if row.GetColumnByName("Digital_Input_Type").Value == "SDI(1) 24Vdc DIO  (0-5000)":
                    sdi_24vdc_dio_redis = row.GetColumnByName("Red_IS").Value
                    #Trace.Write(sdi_24vdc_dio_redis)
            for row in di_cont.Rows:
                if row.GetColumnByName("Digital_Input_Type").Value == "SDI(1) 24Vdc Line Mon DIO (0-5000)":
                    sdi_24vdc_line_mon_dio_red = row.GetColumnByName("Red_IS").Value

            #digital output
            do_cont = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont')
            for row in do_cont.Rows:
                if row.GetColumnByName("Digital_Output_Type").Value == "SDO(1) 24Vdc 500mA DIO  (0-5000)":
                    sdo_24vdc_500ma_dioredis = row.GetColumnByName("Red_IS").Value

            if Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName("Enclosure_Type").DisplayValue == "Cabinet":
                SDO_24vdc_500mA_uio_dio =(Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_Percent_Installed_Spare_IO").Value)
            else:
                SDO_24vdc_500mA_uio_dio = 0

            if SDO_24vdc_500mA_uio_dio == "":
                SDO_24vdc_500mA_uio_dio = 0
                SDO_24vdc_500mA_uio_dio = int(SDO_24vdc_500mA_uio_dio)

            dict_1 ={"sdi_24vdc_dio_redis" : sdi_24vdc_dio_redis, "sdi_24vdc_line_mon_dio_red" : sdi_24vdc_line_mon_dio_red, "sdo_24vdc_500ma_dioredis" :sdo_24vdc_500ma_dioredis, "SDO_24vdc_500mA_uio_dio" : SDO_24vdc_500mA_uio_dio }

            for i in dict_1:
                if dict_1[i]  == "":
                    dict_1[i] = 0
 
            Trace.Write("sdi_24vdc_dio_redis: " + str(dict_1["sdi_24vdc_dio_redis"]))
            Trace.Write("24vdc dio line_mon_dio_red: " + str(dict_1["sdi_24vdc_line_mon_dio_red"]))
            Trace.Write("sdo_24vdc_500ma_dioredis: " + str(dict_1["sdo_24vdc_500ma_dioredis"]))
            #Trace.Write("SDO_24vdc_500mA_uio_dio" + str(SDO_24vdc_500mA_uio_dio))

            #calculation
            SUMDIORIS= (int(dict_1["sdi_24vdc_dio_redis"])+int(dict_1["sdi_24vdc_line_mon_dio_red"])+int(dict_1["sdo_24vdc_500ma_dioredis"]))*(1+float(SDO_24vdc_500mA_uio_dio)/100)
            Trace.Write("sumdioris rg: "+ str(float(SUMDIORIS)))
        return m.ceil(SUMDIORIS)
#fun=Get_SUMDIORIS(Product)
#Trace.Write(str(fun))