ESR = Product.Attr('Experion Software Release').GetValue()
DMSR = Product.Attr('DMS Desk Mounting Stations required').GetValue()
CMSR = Product.Attr('CMS Cabinet Mounting Stations required').GetValue()
DMSFS = Product.Attr('DMS Flex Station Qty 0_60').GetValue()
CMSFS = Product.Attr('CMS Flex Station Qty 0_60').GetValue()
DMSCS = Product.Attr('DMS Console Station Qty 0_20').GetValue()
CMSCS = Product.Attr('CMS Console Station Qty 0_20').GetValue()
DMSCSE = Product.Attr('DMS Console Station Extension Qty 0_15').GetValue()
CMSCSE = Product.Attr('CMS Console Station Extension Qty 0_15').GetValue()
Newexp1=Product.Attributes.GetByName('New_Expansion').GetValue()
IWT=Product.Attributes.GetByName('Interface with TPS Required?').GetValue()
FS=Product.Attributes.GetByName('DMS Flex Station Hardware Selection').GetValue()
CFS=Product.Attributes.GetByName('CMS Flex Station Hardware Selection').GetValue()
CS=Product.Attributes.GetByName('DMS Console Station Hardware Selection').GetValue()
CSE=Product.Attributes.GetByName('DMS Console Station Extension Hardware Selection').GetValue()
PPS=Product.Attributes.GetByName('DMS Remote Peripheral Solution Type RPS').GetValue()
AD=Product.Attributes.GetByName('Additional Stations').GetValue()
#TPS = Product.Attr('DMS TPS Station Qty 0_20').GetValue()

# Point 1 - CXDEV-7712
if ESR == 'R511' or ESR == 'R510'or ESR == 'R520' and DMSR == 'Yes': 
    if DMSFS > 0:
        Product.DisallowAttrValues("DMS Flex Station Hardware Selection","STN_PER_HP_Tower_RAID1")
        Product.DisallowAttrValues("DMS Flex Station Hardware Selection","STN_PER_DELL_Rack_RAID1")
        Product.DisallowAttrValues("DMS Flex Station Hardware Selection","STN_PER_DELL_Tower_RAID1")
        #Product.AllowAttrValues("DMS Flex Station Hardware Selection","None")
    if DMSCS > 0:
        Product.DisallowAttrValues("DMS Console Station Hardware Selection","STN_PER_HP_Tower_RAID1")
        Product.DisallowAttrValues("DMS Console Station Hardware Selection","STN_PER_DELL_Rack_RAID1")
        Product.DisallowAttrValues("DMS Console Station Hardware Selection","STN_PER_DELL_Tower_RAID1")
        #Product.AllowAttrValues("DMS Console Station Hardware Selection","None")
    if DMSCSE > 0:
        Product.DisallowAttrValues("DMS Console Station Extension Hardware Selection","STN_PER_HP_Tower_RAID1")
        Product.DisallowAttrValues("DMS Console Station Extension Hardware Selection","STN_PER_DELL_Rack_RAID1")
        Product.DisallowAttrValues("DMS Console Station Extension Hardware Selection","STN_PER_DELL_Tower_RAID1")
        #Product.AllowAttrValues("DMS Console Station Extension Hardware Selection","None")
    if Newexp1 == "Expansion" and IWT == "Yes":
        TPS = Product.Attr('DMS TPS Station Qty 0_20').GetValue()
        if Newexp1 == "Expansion" and IWT == "Yes" and DMSR == "Yes" and TPS > 0:
            Product.DisallowAttrValues("DMS TPS Station Hardware Selection","STN_PER_HP_Tower_RAID1")
            Product.DisallowAttrValues("DMS TPS Station Hardware Selection","STN_PER_DELL_Rack_RAID1")
            Product.DisallowAttrValues("DMS TPS Station Hardware Selection","STN_PER_DELL_Tower_RAID1")
            #Product.AllowAttrValues("DMS TPS Station Hardware Selection","None")
if ESR == 'R530' and DMSR == 'Yes':
    if DMSFS > 0:
        Product.DisallowAttrValues("DMS Flex Station Hardware Selection","None")
    if DMSCS > 0:
        Product.DisallowAttrValues("DMS Console Station Hardware Selection","None")
    if DMSCSE > 0:
        Product.DisallowAttrValues("DMS Console Station Extension Hardware Selection","None")
    if Newexp1 == "Expansion" and IWT == "Yes":
        TPS = Product.Attr('DMS TPS Station Qty 0_20').GetValue()
        if Newexp1 == "Expansion" and IWT == "Yes" and DMSR == "Yes" and TPS > 0:
            Product.DisallowAttrValues("DMS TPS Station Hardware Selection","None")
if ESR == 'R511' or ESR == 'R510'or ESR == 'R520' and CMSR == 'Yes': 
    if CMSFS > 0:
        Product.DisallowAttrValues("CMS Flex Station Hardware Selection","STN_PER_DELL_Rack_RAID1")
        Product.DisallowAttrValues("CMS Flex Station Hardware Selection","STN_PER_DELL_Tower_RAID1")
        #Product.AllowAttrValues("CMS Flex Station Hardware Selection","None")
    if CMSCS > 0:
        Product.DisallowAttrValues("CMS Console Station Hardware Selection","STN_PER_DELL_Rack_RAID1")
        Product.DisallowAttrValues("CMS Console Station Hardware Selection","STN_PER_DELL_Tower_RAID1")
        #Product.AllowAttrValues("CMS Console Station Hardware Selection","None")
    if CMSCSE > 0:
        Product.DisallowAttrValues("CMS Console Station Extension Hardware Selection","STN_PER_DELL_Rack_RAID1")
        Product.DisallowAttrValues("CMS Console Station Extension Hardware Selection","STN_PER_DELL_Tower_RAID1")
        #Product.AllowAttrValues("CMS Console Station Extension Hardware Selection","None")
    if Newexp1 == "Expansion" and IWT == "Yes":
        CMSTPS = Product.Attr('CMS TPS Station Qty 0_20').GetValue()
        if Newexp1 == "Expansion" and IWT == "Yes" and CMSR == "Yes" and CMSTPS > 0:
            Product.DisallowAttrValues("CMS TPS Station Hardware Selection","STN_PER_DELL_Rack_RAID1")
            Product.DisallowAttrValues("CMS TPS Station Hardware Selection","STN_PER_DELL_Tower_RAID1")
            #Product.AllowAttrValues("CMS TPS Station Hardware Selection","None")
if ESR == 'R530' and CMSR == 'Yes':
    if CMSFS > 0:
        Product.DisallowAttrValues("CMS Flex Station Hardware Selection","None")
    if CMSCS > 0:
        Product.DisallowAttrValues("CMS Console Station Hardware Selection","None")
    if CMSCSE > 0:
        Product.DisallowAttrValues("CMS Console Station Extension Hardware Selection","None")
    if Newexp1 == "Expansion" and IWT == "Yes":
        CMSTPS = Product.Attr('CMS TPS Station Qty 0_20').GetValue()
        if Newexp1 == "Expansion" and IWT == "Yes" and CMSR == "Yes" and CMSTPS > 0:
            Product.DisallowAttrValues("CMS TPS Station Hardware Selection","None")
# Point 2 & 3 - CXDEV-7712
if ESR == 'R520' or ESR == 'R510' or ESR == 'R511' and DMSR == 'Yes' and DMSFS > 0: 
    Product.DisallowAttrValues("DMS Flex Station Hardware Selection","STN_STD_DELL_Tower_NonRAID")
    #Product.Attr('DMS Flex Station Hardware Selection').SelectDisplayValues('STN_PER_DELL_Tower_RAID1')
    #Product.SelectAttrValues("DMS Flex Station Hardware Selection", "STN_PER_DELL_Tower_RAID1")
"""elif ESR == 'R530' and DMSR == 'Yes' and DMSFS >= 1:
    Product.SelectAttrValues("DMS Flex Station Hardware Selection", "STN_STD_DELL_Tower_NonRAID")"""

# Point 4 & 5 - CXDEV-7712
if ESR == 'R520' or ESR == 'R510' or ESR == 'R511' and DMSR == 'Yes' and DMSCS > 0: 
    Product.DisallowAttrValues("DMS Console Station Hardware Selection","STN_STD_DELL_Tower_NonRAID")
    #Product.SelectAttrValues("DMS Console Station Hardware Selection", "STN_PER_DELL_Tower_RAID1")
"""elif ESR == 'R530' and DMSR == 'Yes' and DMSCS > 0:
    Product.SelectAttrValues("DMS Console Station Hardware Selection", "STN_STD_DELL_Tower_NonRAID")"""


# Point 6 & 7 - CXDEV-7712
if ESR == 'R520' or ESR == 'R510' or ESR == 'R511' and DMSR == 'Yes' and DMSCSE > 0: 
    Product.DisallowAttrValues("DMS Console Station Extension Hardware Selection","STN_STD_DELL_Tower_NonRAID")
    #Product.SelectAttrValues("DMS Console Station Extension Hardware Selection", "STN_PER_DELL_Tower_RAID1")
"""elif ESR == 'R530' and DMSR == 'Yes' and DMSCSE > 0:
    Product.SelectAttrValues("DMS Console Station Hardware Selection", "STN_STD_DELL_Tower_NonRAID")"""

# Point 7(1)(2) - CXDEV-7712
if ESR == 'R520' or ESR == 'R510' or ESR == 'R511' and DMSR == 'Yes' and Newexp1 == "Expansion" and IWT == "Yes":
    TPS = Product.Attr('DMS TPS Station Qty 0_20').GetValue()
    if Newexp1 == "Expansion" and IWT == "Yes" and DMSR == "Yes" and TPS > 0:
        Product.DisallowAttrValues("DMS TPS Station Hardware Selection","STN_STD_DELL_Tower_NonRAID")
        #Product.SelectAttrValues("DMS TPS Station Hardware Selection", "STN_PER_DELL_Tower_RAID1")

"""if ESR == 'R530' and Newexp1 == "Expansion" and IWT == "Yes" and DMSR == "Yes":
    TPS = Product.Attr('DMS TPS Station Qty 0_20').GetValue()
    if  Newexp1 == "Expansion" and IWT == "Yes" and DMSR == "Yes" and TPS > 0:
        Product.SelectAttrValues("DMS TPS Station Hardware Selection", "STN_STD_DELL_Tower_NonRAID")"""

# Point 8 - CXDEV-7712
if ESR == 'R530' and DMSR == 'Yes' and DMSFS > 0 or DMSCS > 0 or DMSCSE > 0:
    if FS == "STN_STD_DELL_Tower_NonRAID" or CS == "STN_STD_DELL_Tower_NonRAID" or CSE == "STN_STD_DELL_Tower_NonRAID":
        Product.DisallowAttrValues("DMS Remote Peripheral Solution Type RPS","Extio3_Single_Mode_Fiber")
        Product.DisallowAttrValues("DMS Remote Peripheral Solution Type RPS","Extio3_Multi_Mode_Fiber")
else:
    Product.AllowAttrValues("DMS Remote Peripheral Solution Type RPS","Extio3_Single_Mode_Fiber")
    Product.AllowAttrValues("DMS Remote Peripheral Solution Type RPS","Extio3_Multi_Mode_Fiber")

# Point 9 - CXDEV-7712
if ESR == 'R530' and DMSR == 'Yes' and FS == "STN_STD_DELL_Tower_NonRAID" or CS == "STN_STD_DELL_Tower_NonRAID" or CSE == "STN_STD_DELL_Tower_NonRAID":
    Product.DisallowAttr('DMS RPS Quad Video Support Required')

# Point 10 - CXDEV-7712
if ESR == 'R520' or ESR == 'R510' or ESR == 'R511' or ESR == 'R530' and DMSR == "Yes" and PPS == "Wyse 5070 Optiplex 3000":
    Product.DisallowAttrValues("DMS RPS Mounting Furniture","Orion_Console")

# Point 11 - CXDEV-7712
if ESR in ('R520','R510','R511') and AD > 0:
    Product.DisallowAttrValues("Station Type","STN_PER_HP_Tower_RAID1")
    Product.DisallowAttrValues("Station Type","STN_STD_DELL_Tower_NonRAID")
    Product.DisallowAttrValues("Station Type","STN_PER_DELL_Rack_RAID1")
    Product.DisallowAttrValues("Station Type","STN_PER_DELL_Tower_RAID1")
elif ESR == 'R530':
    Product.DisallowAttrValues("CMS Console Station Extension Hardware Selection","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("CMS Console Station Hardware Selection","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("CMS Flex Station Hardware Selection","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("CMS TPS Station Hardware Selection","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("Console Station Extension Hardware Selection","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("Console Station Hardware Selection","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("Flex Station Hardware Selection TPS","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("TPS Station Hardware Selection","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("DMS Console Station Extension Hardware Selection","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("DMS Console Station Hardware Selection","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("DMS Flex Station Hardware Selection","STN_PER_DELL_Tower_RAID2")
    Product.DisallowAttrValues("DMS TPS Station Hardware Selection","STN_PER_DELL_Tower_RAID2")
    if AD > 0:
        Product.DisallowAttrValues("Station Type","None")
        Product.DisallowAttrValues("Station Type","STN_PER_DELL_Tower_RAID2")

#CXCPQ-120018
if ESR == 'R520':
    Product.DisallowAttrValues("Station Type","None")
    Product.DisallowAttrValues("CMS Console Station Extension Hardware Selection","None")
    Product.DisallowAttrValues("CMS Console Station Hardware Selection","None")
    Product.DisallowAttrValues("CMS Flex Station Hardware Selection","None")
    Product.DisallowAttrValues("CMS TPS Station Hardware Selection","None")
    Product.DisallowAttrValues("Console Station Extension Hardware Selection","None")
    Product.DisallowAttrValues("Console Station Hardware Selection","None")
    Product.DisallowAttrValues("Flex Station Hardware Selection TPS","None")
    Product.DisallowAttrValues("TPS Station Hardware Selection","None")
    Product.DisallowAttrValues("DMS Console Station Extension Hardware Selection","None")
    Product.DisallowAttrValues("DMS Console Station Hardware Selection","None")
    Product.DisallowAttrValues("DMS Flex Station Hardware Selection","None")
    Product.DisallowAttrValues("DMS TPS Station Hardware Selection","None")