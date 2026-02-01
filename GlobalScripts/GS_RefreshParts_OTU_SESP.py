from System.Collections.Specialized import OrderedDictionary
from GS_SESP_OTU_Utilities import OTU_SystemDetails
import GS_SC_SESP_Module
SESP_Models_Cont = Product.GetContainerByName('SystemDetails_OTU_SESP')
SESP_Models_Cont_summry = Product.GetContainerByName('SYSDetails_ScopeSumm_OTU_SESP')
SESP_Models_Cont_Hidden = Product.GetContainerByName('SystemDetails_HIDDEN_OTU_SESP')
SESP_Models_Cont_Hidden.Clear()
SESP_Models_Cont_summry.Clear()
SESP_Models_Cont.Clear()
MSID_container = Product.GetContainerByName('MSIDS_V1_OTU_SESP')

ins_ots = OTU_SystemDetails()
sysNumberDict = GS_SC_SESP_Module.getSiteNumber(Quote, Product, TagParserQuote, Session)
#[{'msid':'xxx','parts':{'DVM':[{},{}]},'EOP':[{},{}]},{'msid1':'xx1','parts':{'DVM':[{},{}]}}]
TPS_OTU_PRICE_TOTAL = 0
GUS_OTU_PRICE_TOTAL = 0
EBR_OTU_PRICE_TOTAL = 0
system_details_table_data = []
for msid_row in MSID_container.Rows:
	if msid_row.IsSelected == True:
		ChildProduct = msid_row.Product
		msid = {}
		msid['msid'] = msid_row['MSIDS_OTU_SESP']
		msid['parts'] = OrderedDictionary()
		# DVM
		dvm_parts = ins_ots.get_dvm_parts(ChildProduct,msid_row)
		msid['parts']['Digital Video Manager'] = dvm_parts
		# Eop
		eop_parts = ins_ots.get_eop_parts(ChildProduct,msid_row)
		msid['parts']['Experion Off process (EOP)'] = eop_parts
		# ESever System
		ESS_Parts = ins_ots.get_eServer_Parts(ChildProduct,msid_row)
		msid['parts']['e-Server System'] = ESS_Parts
		# OTS
		OTS_parts = ins_ots.get_ots_parts(ChildProduct,msid_row)
		msid['parts']['OTS'] = OTS_parts
		# Simulation
		Simulation_parts = ins_ots.get_simulation_parts(ChildProduct,msid_row)
		msid['parts']['Simulation System'] = Simulation_parts
		# HS
		HS_parts = ins_ots.get_hs_parts(ChildProduct,msid_row)
		msid['parts']['HS'] = HS_parts
		# FDM
		FDM_Parts = ins_ots.get_fdm_parts(ChildProduct,msid_row)
		msid['parts']['Field Device Manager'] = FDM_Parts
		# Experion
		EXP_parts = ins_ots.get_experion_parts(ChildProduct,msid_row)
		msid['parts']['Experion PKS'] = EXP_parts
		# TPN
		TPN_parts = ins_ots.get_tpn_parts(ChildProduct,msid_row)
		msid['parts']['Total Plant Network'] = TPN_parts
		# TPS
		TPS_parts = ins_ots.get_tps_parts(ChildProduct,msid_row)
		msid['parts']['Experion-TPS'] = TPS_parts
		# ESVT
		ESVT_parts = ins_ots.get_esvt_parts(ChildProduct,msid_row)
		msid['parts']['Experion PKS for TPS (ESVT)'] = ESVT_parts
		system_details_table_data.append(msid)
		# Calc Additional Prices
		addational_Prices = ins_ots.other_Part_Prices(ChildProduct,msid_row, Quote, TagParserQuote, Session)
		TPS_OTU_PRICE_TOTAL += addational_Prices[0]
		GUS_OTU_PRICE_TOTAL += addational_Prices[1]
		#EBM Prices
		##EBM_Prices = ins_ots.get_ebm_prices(ChildProduct,msid_row)
		##EBM_OTU_PRICE_TOTAL += float(EBM_Prices)
		#EBR
		msid['parts']['EBR System'] = ins_ots.get_ebr_parts(ChildProduct)
Trace.Write("ESVT======================="+str(GUS_OTU_PRICE_TOTAL))
Trace.Write('????'+str(system_details_table_data))
ebr_parts = ["EP-BRWE06", "EP-BRSE06", "EP-BRVE06"]
for msid in system_details_table_data:
	msid_flag = True
	for sys,parts in zip(msid['parts'].Keys, msid['parts'].Values):
		#Trace.Write('PPPPPPP '+str(sys))
		for part in parts:
			#Trace.Write('ppp '+str(part['Qty']))
			if part['Qty'] != '':
				if int(float(part['Qty'])) > 0:
					Trace.Write(part['Part'])
					row = SESP_Models_Cont.AddNewRow(False)
					#row1 = SESP_Models_Cont_summry.AddNewRow(False)
					if msid_flag:
						row['MSID_OTU_SESP'] = msid['msid']
						row["SystemNumber_OTU_SESP"] = sysNumberDict.get(msid['msid'], '')
						row1 = SESP_Models_Cont_summry.AddNewRow(False)
						row1["MSIDs"] = msid['msid']
						row1["List Price"] = '0'
						row1["System Name"] = sys
						msid_flag = False
					row["System_OTU_SESP"] = sys
					row["Models_OTU_SESP"] = part['Part']
					row.IsSelected = True
					if row.Product:
						row["Description_OTU_SESP"] = row.Product.Name
					else:
						row["Description_OTU_SESP"] = ''
						row["UnitListPrice_OTU_SESP"] = '0'
						row["ListPrice_OTU_SESP"] = '0'
					row["Quantity_OTU_SESP"] = str(part['Qty'])
					row["CurrentVersion_OTU_SESP"] = part["CurrentVersion"]
					row["TargetVersion_OTU_SESP"] = part["TargetVersion"]
					row["IsLicensed"] = str(part['IsLicensed'])
					#row["UnitListPrice_OTU_SESP"] = str(part['Price'])
					#row["ListPrice_OTU_SESP"] = str(float(part['Price']) * float(part['Qty']))
					if row.Product:
						row.Calculate()
					if not msid_flag:
						#row1["System Name"] = sys
						row1["System Number"] = sysNumberDict.get(row1["MSIDs"], '')
						#row1["List Price"] = str(float(part['Price']) * float(part['Qty']))
						row1["List Price"] = str(float(row1["List Price"]) + float(row["ListPrice_OTU_SESP"])) if part['Part'] not in ('HC-HCM520-ESD','HC-UPGCLN') else str(float(row1["List Price"]))
						row1["CurrentVersion_OTU_SESP"] = part["CurrentVersion"]
						row1["TargetVersion_OTU_SESP"] = part["TargetVersion"]
					if part['Part'] in ebr_parts:
						EBR_OTU_PRICE_TOTAL += float(row["ListPrice_OTU_SESP"])

for msid in system_details_table_data:
	for sys,parts in zip(msid['parts'].Keys, msid['parts'].Values):
		for part in parts:
			if part['Qty'] != '':
				if int(float(part['Qty'])) > 0:
					row = SESP_Models_Cont_Hidden.AddNewRow(False)
					#row1 = SESP_Models_Cont_summry.AddNewRow(False)
					row['MSID_OTU_SESP'] = msid['msid']
					row["SystemNumber_OTU_SESP"] = sysNumberDict.get(msid['msid'], '')
					row["System_OTU_SESP"] = sys
					row["CurrentVersion_OTU_SESP"] = part["CurrentVersion"]
					row["TargetVersion_OTU_SESP"] = part["TargetVersion"]
					row["Models_OTU_SESP"] = part['Part']
					row["Description_OTU_SESP"] = part['Part']
					row["Quantity_OTU_SESP"] = str(part['Qty'])
					row["UnitListPrice_OTU_SESP"] = str(part['Price'])
					row["ListPrice_OTU_SESP"] = str(float(part['Price']) * float(part['Qty']))
					row["IsLicensed"] = str(part['IsLicensed'])
					#row1["System Name"] = sys
					#row1["MSIDs"] = part['Part']
					#row1["List Price"] = str(float(part['Price']) * float(part['Qty']))
Product.Attr("SYSDETAILS_SEARCHBOX_OTU_SESP").AssignValue("")

##pricing 
dvm_prices = 0
eop_prices = 0
eserver_prices = 0
experion_prices = 0
ots_prices = 0
simulation_prices = 0
fdm_prices = 0
hs_prices = 0
tpn_prices = 0
esvt_prices = 0
thirdParty_Price = 0
#for row in SESP_Models_Cont_Hidden.Rows:
for row in SESP_Models_Cont.Rows:
    if int(float(row['Quantity_OTU_SESP'])) > 0:
        Trace.Write(row['System_OTU_SESP'] + '  -  ' + str(row['IsLicensed']))
        if row['System_OTU_SESP'] == 'Digital Video Manager' and str(row['IsLicensed']) == 'True':
            dvm_prices += float(row['ListPrice_OTU_SESP'])
        elif row['System_OTU_SESP'] == 'Experion Off process (EOP)' and str(row['IsLicensed']) == 'True':
            eop_prices += float(row['ListPrice_OTU_SESP'])
        elif row['System_OTU_SESP'] == 'e-Server System' and str(row['IsLicensed']) == 'True':
            eserver_prices += float(row['ListPrice_OTU_SESP'])
        elif row['System_OTU_SESP'] == 'Experion PKS' and str(row['IsLicensed']) == 'True':
            experion_prices += float(row['ListPrice_OTU_SESP'])
        elif row['System_OTU_SESP'] == 'OTS' and str(row['IsLicensed']) == 'True':
            ots_prices += float(row['ListPrice_OTU_SESP'])
        elif row['System_OTU_SESP'] == 'Simulation System' and str(row['IsLicensed']) == 'True':
            simulation_prices += float(row['ListPrice_OTU_SESP'])
        elif row['System_OTU_SESP'] == 'Field Device Manager' and str(row['IsLicensed']) == 'True':
            fdm_prices += float(row['ListPrice_OTU_SESP'])
        elif row['System_OTU_SESP'] == 'HS' and str(row['IsLicensed']) == 'True':
            hs_prices += float(row['ListPrice_OTU_SESP'])
        elif row['System_OTU_SESP'] == 'Experion PKS for TPS (ESVT)' and str(row['IsLicensed']) == 'True':
            esvt_prices += float(row['ListPrice_OTU_SESP'])
        elif row['System_OTU_SESP'] == 'Total Plant Network' and str(row['IsLicensed']) == 'False':
            tpn_prices += float(row['ListPrice_OTU_SESP'])
        if row['Models_OTU_SESP'] in ["MZ-SQLCL4","EP-MSVS10","EP-IADDVM","EP-T09CAL"]:
            thirdParty_Price += float(row['ListPrice_OTU_SESP'])
GUS_OTU_PRICE_TOTAL = GUS_OTU_PRICE_TOTAL + esvt_prices
Trace.Write("ESVT PRICE------------->"+str(GUS_OTU_PRICE_TOTAL))
Service_Product = Product.Attr("SC_Service_Product").GetValue()
discounts = SqlHelper.GetList('select * from SC_CT_OTU_DISCOUNTS')
def get_discount(system,year,total,Service_Product):
	dis_total = 0
	Service_Product = str(Service_Product.replace('SESP', '')).strip() if Service_Product != '' else ''
	for dis in discounts:
		if dis.SESP_CONTRACT == Service_Product and dis.SYSTEM_NAME == system and dis.SESP_COMMITMENT == year:
			dis_total += float(dis.DISCOUNT)
			break
	return dis_total

def discounted_price(discount,total):
	return (1 - float(discount) / 100) * total
dis = {"DVM":dvm_prices,'EOP':eop_prices,"eServer":eserver_prices,'Experion':experion_prices,'OTS':ots_prices,'Simulation':simulation_prices,'FDM':fdm_prices,'HS':hs_prices,'TPN':tpn_prices,'TPS':TPS_OTU_PRICE_TOTAL,'ESVT':GUS_OTU_PRICE_TOTAL,"ThirdParty":thirdParty_Price,"EBR":EBR_OTU_PRICE_TOTAL}
Trace.Write("$$$$$$$$$$$$"+str(dis))
yearly_prices = []
commitment_con = Product.GetContainerByName('Commitment_OTU_SESP')
discount_price_1 = 0
discount_price_3 = 0
discount_price_5 = 0
discounted_Prices = {"Year_1":{},"Year_3":{},"Year_5":{}}
for sys in dis:
	for i in range(1,4):
		if i == 1:
			sys_disc = get_discount(sys,'1 Year',dis[sys],Service_Product)
			dis_Price_1 = discounted_price(sys_disc,dis[sys])
			discounted_Prices["Year_1"][sys] = dis_Price_1
			discount_price_1 += dis_Price_1
		elif i == 2:
			sys_disc = get_discount(sys,'3 Year',dis[sys],Service_Product)
			dis_Price_3 = discounted_price(sys_disc,dis[sys])
			discounted_Prices["Year_3"][sys] = dis_Price_3
			discount_price_3 += dis_Price_3
		elif i == 3:
			sys_disc = get_discount(sys,'5 Year',dis[sys],Service_Product)
			dis_Price_5 = discounted_price(sys_disc,dis[sys])
			discounted_Prices["Year_5"][sys] = dis_Price_5
			discount_price_5 += dis_Price_5
year = ''
for i in commitment_con.Rows:
	if i.IsSelected == True:
		year = i['SESP_Commitment_OTU']
	if i['SESP_Commitment_OTU'] == '1-Year SESP commitment':
		i['SESP_Prices_OTU'] = str(discount_price_1)
	elif i['SESP_Commitment_OTU'] == '3-Year SESP commitment':
		i['SESP_Prices_OTU'] = str(discount_price_3)
	elif i['SESP_Commitment_OTU'] == '5-Year SESP commitment':
		i['SESP_Prices_OTU'] = str(discount_price_5)
Trace.Write("discounted_Prices - "+str(discounted_Prices))
def assignPrices(year):
	attrs = {'DVM':'ListPrice_DVM_OTU_SESP','EOP':'ListPrice_EOP_OTU_SESP','eServer':'ListPrice_ESS_OTU_SESP','Simulation':'ListPrice_SS_OTU_SESP','OTS':'ListPrice_OTS_OTU_SESP','HS':'ListPrice_HS_OTU_SESP','FDM':'ListPrice_FDM_OTU_SESP','Experion':'ListPrice_EXP_OTU_SESP','TPN':'ListPrice_TPN_OTU_SESP','TPS':'ListPrice_ExTPS_OTU_SESP','ESVT':'ListPrice_ESVT_OTU_SESP','ThirdParty':'ListPrice_ThirdParty_OTU_SESP','EBR':'ListPrice_EBR_OTU_SESP'}
	for i in attrs:
		price = discounted_Prices[year].get(i)
		if price:
			Product.Attr(attrs[i]).AssignValue(str(price))
		else:
			Product.Attr(attrs[i]).AssignValue('')

if year == '1-Year SESP commitment':
	assignPrices('Year_1')
elif year == '3-Year SESP commitment':
	assignPrices('Year_3')
elif year == '5-Year SESP commitment':
	assignPrices('Year_5')