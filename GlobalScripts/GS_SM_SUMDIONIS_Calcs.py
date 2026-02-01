import math as m
def Get_SUMDIONIS(Product):
    if Product.Name == "SM Control Group":
        SUMDIONIS=0
        if 1: #puio condition is removed
            #SUMDIONIS
            #digital input
            di_cont = Product.GetContainerByName('SM_IO_Count_Digital_Input_Cont')
            for row in di_cont.Rows:
                if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc DIO (0-5000)":
                    sdi_24vdc_dio_nonredis = row.GetColumnByName("Non Red (IS)").Value
            for row in di_cont.Rows:
                if row.GetColumnByName("Digital Input Type").Value == "SDI(1) 24Vdc Line Mon DIO (0-5000)":
                    sdi_24vdc_line_mon_dio_nonred = row.GetColumnByName("Non Red (IS)").Value
                    
            #digital output
            do_cont = Product.GetContainerByName('SM_IO_Count_Digital_Output_Cont')
            for row in do_cont.Rows:
                if row.GetColumnByName("Digital Output Type").Value == "SDO(1) 24Vdc 500mA DIO (0-5000)":
                    sdo_24vdc_500ma_diononredis = row.GetColumnByName("Non Red (IS)").Value

            SDO_24vdc_500mA_uio_dio = Product.GetContainerByName('SM_CG_Cabinet_Details_Cont_Right').Rows[0].GetColumnByName("Percent_Installed_Spare_IOs").Value
            if SDO_24vdc_500mA_uio_dio == "":
                SDO_24vdc_500mA_uio_dio = 0
                SDO_24vdc_500mA_uio_dio = int(SDO_24vdc_500mA_uio_dio)

            dict_1 ={"sdi_24vdc_dio_nonredis" : sdi_24vdc_dio_nonredis, "sdi_24vdc_line_mon_dio_nonred" : sdi_24vdc_line_mon_dio_nonred, "sdo_24vdc_500ma_diononredis" :sdo_24vdc_500ma_diononredis}

            for i in dict_1:
                if dict_1[i]  == "":
                    dict_1[i] = 0

            Trace.Write("sdi_24vdc_dio_nonredis: " + str(dict_1["sdi_24vdc_dio_nonredis"]))
            Trace.Write("24vdc dio line_mon_dio_nonred: " + str(dict_1["sdi_24vdc_line_mon_dio_nonred"]))
            Trace.Write("sdo_24vdc_500ma_diononredis: " + str(dict_1["sdo_24vdc_500ma_diononredis"]))
            #Trace.Write("SDO_24vdc_500mA_uio_dio" + str(SDO_24vdc_500mA_uio_dio))

            #calculation
            SUMDIONIS= (int(dict_1["sdi_24vdc_dio_nonredis"])+int(dict_1["sdi_24vdc_line_mon_dio_nonred"])+int(dict_1["sdo_24vdc_500ma_diononredis"]))*(1+float(SDO_24vdc_500mA_uio_dio)/100)
            Trace.Write("sumdionis cg: "+ str(float(SUMDIONIS)))
        return m.ceil(SUMDIONIS)
    
    
 
    
    if Product.Name == "SM Remote Group":
        SUMDIONIS=0
        if 1: #puio condition is removed
            #SUMDIONIS
            #digital input
            di_cont = Product.GetContainerByName('SM_RG_IO_Count_Digital_Input_Cont')
            for row in di_cont.Rows:
                if row.GetColumnByName("Digital_Input_Type").Value == "SDI(1) 24Vdc DIO  (0-5000)":
                    sdi_24vdc_dio_nonredis = row.GetColumnByName("Non_Red_IS").Value
            for row in di_cont.Rows:
                if row.GetColumnByName("Digital_Input_Type").Value == "SDI(1) 24Vdc Line Mon DIO (0-5000)":
                    sdi_24vdc_line_mon_dio_nonred = row.GetColumnByName("Non_Red_IS").Value
                    
            #digital output
            do_cont = Product.GetContainerByName('SM_RG_IO_Count_Digital_Output_Cont')
            for row in do_cont.Rows:
                if row.GetColumnByName("Digital_Output_Type").Value == "SDO(1) 24Vdc 500mA DIO  (0-5000)":
                    sdo_24vdc_500ma_diononredis = row.GetColumnByName("Non_Red_IS").Value
            
            if Product.GetContainerByName('SM_RG_ATEX Compliance_and_Enclosure_Type_Cont').Rows[0].GetColumnByName("Enclosure_Type").DisplayValue == "Cabinet":
                SDO_24vdc_500mA_uio_dio =(Product.GetContainerByName('SM_RG_Cabinet_Details_Cont').Rows[0].GetColumnByName("SM_Percent_Installed_Spare_IO").Value)
            else:
                SDO_24vdc_500mA_uio_dio = 0
                
            if SDO_24vdc_500mA_uio_dio == "":
                SDO_24vdc_500mA_uio_dio = 0
                SDO_24vdc_500mA_uio_dio = int(SDO_24vdc_500mA_uio_dio)

            dict_1 ={"sdi_24vdc_dio_nonredis" : sdi_24vdc_dio_nonredis, "sdi_24vdc_line_mon_dio_nonred" : sdi_24vdc_line_mon_dio_nonred, "sdo_24vdc_500ma_diononredis" :sdo_24vdc_500ma_diononredis, "SDO_24vdc_500mA_uio_dio" : SDO_24vdc_500mA_uio_dio }

            for i in dict_1:
                if dict_1[i]  == "":
                    dict_1[i] = 0

            Trace.Write("sdi_24vdc_dio_nonredis: " + str(dict_1["sdi_24vdc_dio_nonredis"]))
            Trace.Write("24vdc dio line_mon_dio_nonred: " + str(dict_1["sdi_24vdc_line_mon_dio_nonred"]))
            Trace.Write("sdo_24vdc_500ma_diononredis: " + str(dict_1["sdo_24vdc_500ma_diononredis"]))
            #Trace.Write("SDO_24vdc_500mA_uio_dio" + str(SDO_24vdc_500mA_uio_dio))

            #calculation
            SUMDIONIS= (int(dict_1["sdi_24vdc_dio_nonredis"])+int(dict_1["sdi_24vdc_line_mon_dio_nonred"])+int(dict_1["sdo_24vdc_500ma_diononredis"]))*(1+float(SDO_24vdc_500mA_uio_dio)/100)
            Trace.Write("sumdionis rg: "+ str(float(SUMDIONIS)))
        return m.ceil(SUMDIONIS)