#CXCPQ-67591: Added script to display costing message. This script is added as a post action to REPRICE
import re


def removeQuoteMessages(Quote):
    pattern = r'^Cost for material[\w\W]*? either Zero or not defined in SAP. Please consider different Plant.$'
    for i in list(Quote.Messages):
        if re.match(pattern, i):
            Quote.Messages.Remove(i)

lv_partnumber_list=[]

#Below logic runs only for PMC Parts & Spot Quote       
if (Quote.GetCustomField('Booking LOB').Content == "PMC" and Quote.GetCustomField("Quote Type").Content == 'Parts and Spot' and Quote.GetCustomField("CF_Plant").Content!=''):
    for i in Quote.Items:
        writein_data = SqlHelper.GetFirst("SELECT Product FROM WRITEINPRODUCTS WHERE Product= '{}'".format(str(i.PartNumber)))
        getprdid = SqlHelper.GetFirst("SELECT IsSyncedFromBackOffice from products where product_catalog_code= '{}' and IsSyncedFromBackOffice = 'True' and PRODUCT_ACTIVE = 1 ".format(str(i.PartNumber)))
        if getprdid is not None and writein_data is None and i.Cost==0:
            lv_partnumber_list.append(i.PartNumber)


#Project Type Quote
if Quote.GetCustomField("Quote Type").Content == 'Projects':
    for i in Quote.Items:
        qry = SqlHelper.GetFirst("SELECT 1 as flag from FME_PARTS WHERE PARTNUMBER = '{}'".format(str(i.PartNumber)))
        if qry is not None and i.Cost==0:
            lv_partnumber_list.append(i.PartNumber)


if lv_partnumber_list:
    Trace.Write('Count:'+str(len(lv_partnumber_list)))
    # Quote.Messages.Clear()
    removeQuoteMessages(Quote)
    if len(lv_partnumber_list)>1:
        Quote.Messages.Add("Cost for materials " + str(lv_partnumber_list)+ " are either Zero or not defined in SAP. Please consider different Plant.")
        Trace.Write("Cost for materials " + str(lv_partnumber_list)+ " are either Zero or not defined in SAP. Please consider different Plant.")
    else:
        Quote.Messages.Add("Cost for material " + str(lv_partnumber_list)+ " is either Zero or not defined in SAP. Please consider different Plant.")
        Trace.Write("Cost for material " + str(lv_partnumber_list)+ " is either Zero or not defined in SAP. Please consider different Plant.")
    Trace.Write('Test')