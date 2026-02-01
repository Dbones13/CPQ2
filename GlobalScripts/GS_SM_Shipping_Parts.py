#CXCPQ-47876 and CXCPQ-47877
import System.Decimal as D

def SM_Shipping_Parts_CG_RG(Prod, parts_dict):
    Trace.Write("Product Name : "+Prod.Name)
    iota_type = ''
    if Prod.Name=="SM Control Group":
        if Prod.GetContainerByName('SM_CG_Common_Questions_Cont').Rows.Count > 0:
            iota_type = Prod.GetContainerByName('SM_CG_Common_Questions_Cont').Rows[0].GetColumnByName("SM_Universal_IOTA").Value
    elif Prod.Name=="SM Remote Group":
        iota_type = Prod.Attr('SM_Universal_IOTA_Type').GetValue()
    else:
        Trace.Write("GS_SM_Shipping_Parts - Product is neither CG nor RG")
        return parts_dict
        
    if iota_type != 'PUIO' and iota_type != 'RUSIO':
        Trace.Write("IOTA type is neither PUIO nor RUSIO. No parts added.")
        Trace.Write("GS_SM_Shipping_Parts - IOTA type is neither PUIO nor RUSIO")
        return parts_dict
    
    Crate_Type = Prod.Attr('Crate Type').GetValue()
    Crate_Design = Prod.Attr('Crate Design').GetValue()
    
    part_qty = 0
    if 'FS-BCU-0036' in parts_dict.keys():
        part_qty = parts_dict['FS-BCU-0036']['Quantity']
    elif 'FS-BCU-0038' in parts_dict.keys():
        part_qty = parts_dict['FS-BCU-0038']['Quantity']
    elif '50154983-001' in parts_dict.keys():
        part_qty = parts_dict['50154983-001']['Quantity']
    if part_qty > 0:
        if Crate_Type == 'Domestic/Truck':
            if Crate_Design == 'Standard':
                parts_dict['CF-SP0001'] = {'Quantity' : part_qty, 'Description': ''}
            elif Crate_Design == 'Premium':
                parts_dict['CF-PP0001'] = {'Quantity' : part_qty, 'Description': ''}
        if Crate_Type == 'Air':
            if Crate_Design == 'Standard':
                parts_dict['CF-CT4A02'] = {'Quantity' : part_qty, 'Description': ''}
            elif Crate_Design == 'Premium':
                parts_dict['CF-CT4A03'] = {'Quantity' : part_qty, 'Description': ''}
        if Crate_Type == 'Ocean':
            if Crate_Design == 'Standard':
                parts_dict['CF-CT4002'] = {'Quantity' : part_qty, 'Description': ''}
            elif Crate_Design == 'Premium':
                parts_dict['CF-CT4003'] = {'Quantity' : part_qty, 'Description': ''}
    return parts_dict
    
def SM_Shipping_Parts_CG(Prod, parts_dict):
    Trace.Write("Product Name : "+Prod.Name)
    iota_type = ''
    if Prod.Name!="SM Control Group":
        Trace.Write("GS_SM_Shipping_Parts - Product is not CG")
        return parts_dict
    
    Crate_Type = Prod.Attr('Crate Type').GetValue()
    Crate_Design = Prod.Attr('Crate Design').GetValue()
    
    io_flag = False
    cont_col_mapping = {'SM_IO_Count_Digital_Input_Cont': 'Total DI Point', 'SM_IO_Count_Digital_Output_Cont':'Total DO Point', 'SM_IO_Count_Analog_Input_Cont':'Total AI Point', 'SM_IO_Count_Analog_Output_Cont': 'Total AO Point', 'SM_CG_DI_RLY_NMR_Cont': 'Total DI NMR Point', 'SM_CG_DO_RLY_NMR_Cont':'Total DO NMR Point'}
    for cont in cont_col_mapping:
        io_cont = Prod.GetContainerByName(cont)
        for cont_row in io_cont.Rows:
            #Trace.Write("Val = "+cont_row.GetColumnByName(cont_col_mapping[cont]).Value)
            if int(cont_row.GetColumnByName(cont_col_mapping[cont]).Value) > 0:
                io_flag = True
                break
        if io_flag:
            break
        
    if io_flag:
        if Crate_Type == 'Domestic/Truck':
            if Crate_Design == 'Standard':
                parts_dict['CF-MSD000'] = {'Quantity' : 1, 'Description': ''}
            elif Crate_Design == 'Premium':
                parts_dict['CF-MSD001'] = {'Quantity' : 1, 'Description': ''}
        if Crate_Type == 'Air':
            if Crate_Design == 'Standard':
                parts_dict['CF-MSA000'] = {'Quantity' : 1, 'Description': ''}
            elif Crate_Design == 'Premium':
                parts_dict['CF-MSA001'] = {'Quantity' : 1, 'Description': ''}
        if Crate_Type == 'Ocean':
            if Crate_Design == 'Standard':
                parts_dict['CF-MSO000'] = {'Quantity' : 1, 'Description': ''}
            elif Crate_Design == 'Premium':
                parts_dict['CF-MSO001'] = {'Quantity' : 1, 'Description': ''}
    return parts_dict

#parts = {}
#x=SM_Shipping_Parts_CG_RG(Product, parts)
#Trace.Write("Parts = "+str(parts))
#y=SM_Shipping_Parts_CG(Product, parts)
#Trace.Write("Parts = "+str(parts))