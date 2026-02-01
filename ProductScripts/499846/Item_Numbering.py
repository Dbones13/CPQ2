PSkidCont = Product.GetContainerByName('PRODUCTIZED _SKID_BOM')
Header_cnt=0
SubHead_cnt=0
Item_cnt=0
Main_str=''
Itm_str=''
lv_Prev_rec_Type=''
for row in PSkidCont.Rows:
    if row["Type"] =='H':
        if Header_cnt==0 and SubHead_cnt==0 and Item_cnt==0:
            #First row
            Header_cnt=Header_cnt+1
        else:
            if Header_cnt>0:
                #If Header record already exists in the container
                Header_cnt=Header_cnt+1
            else:
                if SubHead_cnt>0:
                    #If No Header record exists but sub-header found in the container
                    Header_cnt=SubHead_cnt+1
                else:
                    #Only product record found and No Header/Sub-header in the container
					Header_cnt=Item_cnt+1

        SubHead_cnt=0
        Item_cnt=0
        Main_str=str(Header_cnt)
        Itm_str=Main_str
          
    elif row["Type"] =='S':

        if lv_Prev_rec_Type=='H':
            #IF previous record is header record.
            SubHead_cnt=SubHead_cnt+1
            Main_str=str(Header_cnt)+'.'+str(SubHead_cnt)
            
        else:
            #IF previous record is not a header record.

            if Header_cnt>0: 
                if Item_cnt>0 and SubHead_cnt==0 :
                    # IF header record found and Product record also found in the container.
                    SubHead_cnt=Item_cnt+1
                    Main_str=str(Header_cnt)+'.'+str(SubHead_cnt)
                else:
                    SubHead_cnt=SubHead_cnt+1
                    Main_str=str(Header_cnt)+'.'+str(SubHead_cnt)
                        
            else: 
                if Item_cnt>0 and SubHead_cnt==0:
                    # IF No header record found and Product record found in the container.
                    SubHead_cnt=Item_cnt+1
                    Main_str=str(SubHead_cnt)
                else:
                    SubHead_cnt=SubHead_cnt+1
                    Main_str=str(SubHead_cnt)

        Itm_str=Main_str
        Item_cnt=0

    else:
        Item_cnt=Item_cnt+1
        if Itm_str!='': 
        	Main_str=Itm_str+'.'+str(Item_cnt)
        else:
            Main_str=str(Item_cnt)
     
    
    lv_Prev_rec_Type=str(row["Type"])
    row["Item"] =Main_str