if Product.Attributes.GetByName('DMS Desk Mounting Stations required').SelectedValue.Display=="Yes":
    MIB=Product.Attributes.GetByName('MIB Configuration Required?').SelectedValue.Display
    CMS=Product.Attributes.GetByName('CMS Cabinet Mounting Stations required').SelectedValue.Display
    Newexp=Product.Attributes.GetByName('New_Expansion').SelectedValue.Display
    CSEQ0_15=Product.Attributes.GetByName('DMS Console Station Extension Qty 0_15').GetValue()
    Displaysize=Product.Attributes.GetByName('DMS Display size').SelectedValue.Display
    Noofdisplay=Product.Attributes.GetByName('DMS No of Displays 0_4').GetValue()
    try:
        IWT=Product.Attributes.GetByName('Interface with TPS Required?').SelectedValue.Display
        dms_touchscreen=Product.Attributes.GetByName('DMS Touch Screen required?').SelectedValue.Display
        FSQ0_60=Product.Attributes.GetByName('DMS Flex Station Qty 0_60').GetValue()
    except:
        IWT="No"
        dms_touchscreen="No"
        FSQ0_60 = 0
    try:
        FSQ0_60=Product.Attributes.GetByName('DMS Flex Station Qty 0_60').GetValue()
    except:
        FSQ0_60 = 0
    #1
    if IWT=="No":
        Product.AllowAttr('DMS Console Station Qty 0_20')
    else:
        Product.DisallowAttr('DMS Console Station Qty 0_20')

    #2
    if IWT=="Yes" and Newexp=="Expansion":
        Product.AllowAttr('DMS TPS Station Qty 0_20')
        Product.AllowAttr('DMS TPS Station Hardware Selection')
        Product.AllowAttr('DMS Industrial KB Mouse')
    else:
        Product.DisallowAttr('DMS TPS Station Qty 0_20')
        Product.DisallowAttr('DMS TPS Station Hardware Selection')
        Product.DisallowAttr('DMS Industrial KB Mouse')

    #3
    if int(FSQ0_60)>0:
        Product.AllowAttr('DMS Flex Station Hardware Selection')
        #Product.AllowAttr('DMS Multi Window Support Option Required?')
    else:
        Product.DisallowAttr('DMS Flex Station Hardware Selection')
        #Product.DisallowAttr('DMS Multi Window Support Option Required?')

    #5
    try:
        CSQ0_20=Product.Attributes.GetByName('DMS Console Station Qty 0_20').GetValue()
        if CSQ0_20=="":
            CSQ0_20=0
    except:
        CSQ0_20=0
    if int(CSQ0_20)>0 and IWT=="No":
        Product.AllowAttr('DMS Console Station Hardware Selection')
    else:
        Product.DisallowAttr('DMS Console Station Hardware Selection')

    #7
    if int(CSEQ0_15)>0:
        Product.AllowAttr('DMS Console Station Extension Hardware Selection')
    else:
        Product.DisallowAttr('DMS Console Station Extension Hardware Selection')

    #4
    try:
        FSHS=Product.Attributes.GetByName('DMS Flex Station Hardware Selection').SelectedValue.Display
    except:
        FSHS="0"

    #6
    try:
        CSHS=Product.Attributes.GetByName('DMS Console Station Hardware Selection').SelectedValue.Display
    except:
        CSHS="0"

    #8
    try:
        CSEHS=Product.Attributes.GetByName('DMS Console Station Extension Hardware Selection').SelectedValue.Display
    except:
        CSEHS="0"


    #4,6,8
    if FSHS=="STN_PER_DELL_Rack_RAID1":
        Product.AllowAttr('DMS Message 1')
    elif CSHS=="STN_PER_DELL_Rack_RAID1":
        Product.AllowAttr('DMS Message 1')
    elif CSEHS=="STN_PER_DELL_Rack_RAID1":
        Product.AllowAttr('DMS Message 1')
    else:
        Product.DisallowAttr('DMS Message 1')

    #9
    if (FSHS=="STN_PER_DELL_Tower_RAID1" or FSHS=="STN_PER_DELL_Rack_RAID1" or FSHS=="STN_PER_HP_Tower_RAID1") and MIB=="Yes" and IWT=="No":
        Product.AllowAttr('DMS Message 4')
    else:
        Product.DisallowAttr('DMS Message 4')

    #10
    if (CSHS=="STN_PER_DELL_Tower_RAID1" or CSHS=="STN_PER_DELL_Rack_RAID1" or CSHS=="STN_PER_HP_Tower_RAID1") and MIB=="Yes" and IWT=="No":
        Product.AllowAttr('DMS Message 5')
    else:
        Product.DisallowAttr('DMS Message 5')

    #11
    if (CSEHS=="STN_PER_DELL_Tower_RAID1" or CSEHS=="STN_PER_DELL_Rack_RAID1" or CSEHS=="STN_PER_HP_Tower_RAID1") and MIB=="Yes" and IWT=="No":
        Product.AllowAttr('DMS Message 6')
    else:
        Product.DisallowAttr('DMS Message 6')

    #12
    if (FSHS=="STN_STD_DELL_Tower_NonRAID" or CSHS=="STN_STD_DELL_Tower_NonRAID" or CSEHS=="STN_STD_DELL_Tower_NonRAID" or dms_touchscreen=="Touch Screen"):
        Trace.Write('----------iff---')
        Product.DisallowAttrValues("DMS Display size","55 inch NTS")
    else:
        Product.AllowAttrValues("DMS Display size","55 inch NTS")

    #13
    if (Displaysize=="55 inch NTS" or Displaysize=="23 inch NTS" or Displaysize=="21.33 inch NTS") and MIB=="Yes" and IWT=="No":
        Product.AllowAttr('DMS Message 7')
    else:
        Product.DisallowAttr('DMS Message 7')

    #14
    '''try:
        MWSOR=Product.Attributes.GetByName('DMS Multi Window Support Option Required?').SelectedValue.Display
    except:
        MWSOR="No"
    if MWSOR=="No" and (Noofdisplay=="2" or Noofdisplay=="3" or Noofdisplay=="4"):
        Product.Attributes.GetByName('DMS No of Displays 0_4').AssignValue("0")
        Product.AllowAttr('DMS Message 8')
    else:
        Product.DisallowAttr('DMS Message 8')'''