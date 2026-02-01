#from GS_SC_SFDCD_STRUCTURE_OTU import dummyresponse_structure
from CPQ_SF_SC_Modules import CL_SC_Modules
class OTU_SFDC():
	#part_qty_dict = dict()
	def __init__(self):
		#self.get_sfdc_dummy_response = self.SFDC_Dummy_response()
		self.part_qty_dict = dict()
		#pass
	def sfdc_response(self,Quote,Product,TagParserQuote,Session,Selected_MSID,selectedSite):
		class_contact_modules = CL_SC_Modules(Quote, TagParserQuote, None, Session)
		AccountName = Quote.GetCustomField('Account Name').Content
		AccountId = Quote.GetCustomField('AccountId').Content
		pAccountName = Quote.GetCustomField('SC_CF_PARENT_ACCOUNT_NAME').Content
		isParent = False
		#selectedSites = Product.Attr('SC_MultiSites_Selected').GetValue()
		#AccountSite = selectedSites.split('<,>')
		AccountSite = selectedSite
		if not pAccountName:
			isParent = True
		if Selected_MSID:
			Trace.Write('111111111111111111'+str(Selected_MSID) + " == "+str(AccountSite))
			SummaryTable = class_contact_modules.get_siteID_assets(AccountId, AccountSite, Selected_MSID, isParent)
			return SummaryTable
	'''def SFDC_Dummy_response(self):
		res_total_size = 0
		res_records = []
		sys_msids = dummyresponse_structure()
		for sys,msids in sys_msids.items():
			for msid,parts in msids.items():
				for part in parts:
					for partnum,qty in part.items():
						attr = {
					"attributes": {
					"type": "Asset",
					"url": "/services/data/v55.0/sobjects/Asset/02i02000001wg4CAAQ"
					},
					"AccountId": "",
					"Name": "",
					"Quantity": '',
					"SiteLicSeqSys__c": 'System '+ str(res_total_size),
					"ProductCode": "",#part
					"Parent": {
					"attributes": {
						"type": "Asset",
						"url": "/services/data/v55.0/sobjects/Asset/02i02000001wg47AAA"
					},
					"Name": "", #msid
					"ProductCode": "" #system name
					},
					"Account": {
					"attributes": {
						"type": "Account",
						"url": "/services/data/v55.0/sobjects/Account/0010200000EV01EAAT"
					},
					"Site": "",
					"Id": ""
					}
				}
						attr['Parent']['ProductCode'] = sys
						attr['Parent']['Name'] = msid
						attr['Name'] = sys + ' - ' + msid
						attr['ProductCode'] = partnum
						attr['Quantity'] = qty
						res_records.append(attr)
						res_total_size += 1
		response = {}
		response['records'] = res_records
		response['done'] = True
		response['totalSize'] = res_total_size
		return response'''

	def get_qty(self,sys_name,msid,part,get_sfdc_response):
		if get_sfdc_response is not None and get_sfdc_response != '':
			if len(self.part_qty_dict) == 0:
				for i in get_sfdc_response['records']:
					prod_code = str(i['ProductCode']).strip()
					qty = str(i['Quantity']).strip() or '0'
					if i['Parent']['Name'] == msid and prod_code != '':
						if prod_code in self.part_qty_dict.keys():
							self.part_qty_dict[prod_code] += int(float(qty))
						else:
							self.part_qty_dict[prod_code] = int(float(qty))
		return self.part_qty_dict.get(part, 0)
		"""if get_sfdc_response is not None and get_sfdc_response != '':
			for i in get_sfdc_response['records']:
				#Trace.Write(i['Parent']['Name'] + ' ====== '+ str(i['ProductCode']))
				if i['Parent']['Name'] == msid and i['ProductCode'] == part:
					return str(i['Quantity'])
			else:
				return 0"""
	def assign_value(self,Product,attr,qty):
		Product.Attr(attr).AssignValue(str(qty))
	def dvm_cameras_sf_value(self,Product,attr,sys_name,msid,part,get_sfdc_response):
		qty = self.get_qty(sys_name,msid,part,get_sfdc_response)
		self.assign_value(Product,attr,qty)
	def dvm_intExplr_sf_value(self,Product,attr,sys_name,msid,part,get_sfdc_response):
		qty = self.get_qty(sys_name,msid,part,get_sfdc_response)
		self.assign_value(Product,attr,qty)
	def eop_base_units_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Base Units= 160 + (Qty of EP-ETS001*5 + EP-ETSU01*1 + EP-ETSU05*5 + EP-ETSU10*10 + EP-ETSU50*50)*35
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			if i == 'EP-ETS001':
				if qty:
					cal_qty += float(qty) * 5
			elif i == 'EP-ETSU01':
				if qty:
					cal_qty += float(qty) * 1
			elif i == 'EP-ETSU05':
				if qty:
					cal_qty += float(qty) * 5
			elif i == 'EP-ETSU10':
				if qty:
					cal_qty += float(qty) * 10
			elif i == 'EP-ETSU50':
				if qty:
					cal_qty += float(qty) * 50
		cal_qty =  160 + (cal_qty * 35)
		self.assign_value(Product,attr,cal_qty)
	def hs_experionHsPoints_sf_value(self,Product,attr,sys_name, msid,parts,get_sfdc_response):
		#Experion HS Points= EP-HME01K*1000 + EP-HME02K*2000 + EP-HME05K*5000 + EP-HME08K*8000 + EP- HME100*100 + EP-HME16K*16000 + EP-HSTA01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			#qty = 8
			if i == 'EP-HME01K':
				cal_qty += float(qty) * 1000
			elif i == 'EP-HME02K':
				cal_qty += float(qty) * 2000
			elif i == 'EP-HME05K':
				cal_qty += float(qty) * 5000
			elif i == 'EP-HME08K':
				cal_qty += float(qty) *  8000
			elif i == 'EP-HME100':
				cal_qty += float(qty) * 100
			elif i == 'EP-HME16K':
				cal_qty += float(qty) * 16000
			elif i == 'EP-HSTA01':
				cal_qty += float(qty)
			else:
				cal_qty += 1
		else:
			self.assign_value(Product,attr,cal_qty)
	def hs_EP_BRWE06_sf_value(self,Product,attr,sys_name, msid,parts,get_sfdc_response):
		#P-BRWE06= Qty of EP-BRWE06 + EP-BRWE05 + EP-BRWE04 + EP-BRWE03 + EP-BRWE02 + EP-BRWE01 + ES-BRWR06 + ES-BRWR05 + ES-BRWR04 + ES-BRWR03 + ES-BRWR02 + ES-BRWR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def hs_EP_BRVE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRVE06= Qty of EP-BRVE06 + EP-BRVE05 + EP-BRVE04 + EP-BRVE03 + EP-BRVE02 + EP-BRVE01 + ES- BRVR06 + ES-BRVR05 + ES-BRVR04 + ES-BRVR03 + ES-BRVR02 + ES-BRVR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		Trace.Write("#######"+str(cal_qty))
		self.assign_value(Product,attr,cal_qty)
	def hs_EP_BRSE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRSE06= EP-BRSE06 + EP-BRSE05 + EP-BRSE04 + EP-BRSE03 + EP-BRSE02 + EP-BRSE01 + ES-BRSR06 +ES-BRSR05 + ES-BRSR04 + ES-BRSR03 + ES-BRSR062 + ES-BRSR06
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def experion_experionProcessPoints_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Experion Process Points= EP-DPR01K*1000 + EP-DPR02K*2000 + EP-DPR05K*5000 + EP-DPR100*100 + EP- DPR10K*10000 + ES-DPR01K*1000 + ES-DPR02K*2000 + ES-DPR05K*5000 + ES- DPR100*100 + ES-DPR10K*10000
		cal_qty = 0
		for i in parts:
			i = i
			if i == 'EP-DPR01K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 1000
			elif i == 'EP-DPR02K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 2000
			elif i == 'EP-DPR05K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 5000
			elif i == 'EP-DPR100':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 100
			elif i == 'EP- DPR10K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 10000
			elif i == 'ES-DPR01K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 1000
			elif i == 'ES-DPR02K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 2000
			elif i == 'ES-DPR05K*5000':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 5000
			elif i == 'ES-DPR100*100':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 100
			elif i == 'ES-DPR10K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 10000
		self.assign_value(Product,attr,cal_qty)
	def experion_experionScadaPoints_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Experion SCADA Points= EP-DSC01K*1000 + EP-DSC02K*2000 + EP-DSC05K*5000 + EP-DSC100*100 + EP-DSC10K*10000 + ES-DSC01K*1000 + ES-DSC02K*2000 + ES-DSC05K*5000 + ES-DSC100*100 + ES-DSC10K*10000
		cal_qty = 0
		for i in parts:
			if i == 'EP-DSC01K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 1000
			elif i == 'EP-DSC02K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 2000
			elif i == 'EP-DSC05K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 5000
			elif i == 'EP-DSC100':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 100
			elif i == 'EP-DSC10K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 10000
			elif i == 'ES-DSC01K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 1000
			elif i == 'ES-DSC02K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 2000
			elif  i == 'ES-DSC05K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 5000
			elif i == 'ES-DSC100':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 100
			elif i == 'ES-DSC10K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 10000
		self.assign_value(Product,attr,cal_qty)
	
	def experion_experionFlexStations_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Flex stations= EP-STAT01 + EP-STAT05*5 + EP-STAT10*10 + ES-STAT01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			if i == 'EP-STAT05':
				cal_qty += float(qty) * 5
			elif i == 'EP-STAT10':
				cal_qty += float(qty) * 10
			else:
				cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	
	def experion_experionConsoleStations_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Console stations= EP-STAC01 + EP-STAC05*5 + EP-STAC10*10 + ES-STAC01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			if i == 'EP-STAC05':
				cal_qty += float(qty) * 5
			elif i == 'EP-STAC10':
				cal_qty += float(qty) * 10
			else:
				cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	
	def experion_EP_BRWE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRWE06= Qty of EP-BRWE06 + EP-BRWE05 + EP-BRWE04 + EP-BRWE03 + EP-BRWE02 + EP-BRWE01 + ES-BRWR06 + ES-BRWR05 + ES-BRWR04 + ES-BRWR03 + ES-BRWR02 + ES-BRWR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	
	def experion_EP_BRVE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRVE06= Qty of EP-BRVE06 + EP-BRVE05 + EP-BRVE04 + EP-BRVE03 + EP-BRVE02 + EP-BRVE01 + ES- BRVR06 + ES-BRVR05 + ES-BRVR04 + ES-BRVR03 + ES-BRVR02 + ES-BRVR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	
	def experion_EP_BRSE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRSE06= EP-BRSE06 + EP-BRSE05 + EP-BRSE04 + EP-BRSE03 + EP-BRSE02 + EP-BRSE01 + ES-BRSR06 +ES-BRSR05 + ES-BRSR04 + ES-BRSR03 + ES-BRSR062 + ES-BRSR06
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	
	def experion_serverRedundency_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Server Redundancy= If any of the part (EP-RBASE1 or ES-RBASE1) is present, then Server Redundancy= Yes
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			if float(qty) > 0:
				self.assign_value(Product,attr,'Yes')
				break
	
	def eServer_PremiumAccesUser_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#eServer Premium Access User= Qty of EP-ESPREM + EP-ETPREM
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	
	def eServer_EP_BRWE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRWE06= Qty of EP-BRWE06 + EP-BRWE05 + EP-BRWE04 + EP-BRWE03 + EP-BRWE02 + EP-BRWE01 + ES-BRWR06 + ES-BRWR05 + ES-BRWR04 + ES-BRWR03 + ES-BRWR02 + ES-BRWR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	
	def eServer_EP_BRVE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRVE06= Qty of EP-BRVE06 + EP-BRVE05 + EP-BRVE04 + EP-BRVE03 + EP-BRVE02 + EP-BRVE01 + ES- BRVR06 + ES-BRVR05 + ES-BRVR04 + ES-BRVR03 + ES-BRVR02 + ES-BRVR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def eServer_EP_BRSE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRSE06= EP-BRSE06 + EP-BRSE05 + EP-BRSE04 + EP-BRSE03 + EP-BRSE02 + EP-BRSE01 + ES-BRSR06 +ES-BRSR05 + ES-BRSR04 + ES-BRSR03 + ES-BRSR02 + ES-BRSR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def simulation_EP_BRWE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRWE06= Qty of EP-BRWE06 + EP-BRWE05 + EP-BRWE04 + EP-BRWE03 + EP-BRWE02 + EP-BRWE01 + ES-BRWR06 + ES-BRWR05 + ES-BRWR04 + ES-BRWR03 + ES-BRWR02 + ES-BRWR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def simulation_EP_BRVE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRVE06= Qty of EP-BRVE06 + EP-BRVE05 + EP-BRVE04 + EP-BRVE03 + EP-BRVE02 + EP-BRVE01 + ES- BRVR06 + ES-BRVR05 + ES-BRVR04 + ES-BRVR03 + ES-BRVR02 + ES-BRVR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def simulation_EP_BRSE06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRSE06= EP-BRSE06 + EP-BRSE05 + EP-BRSE04 + EP-BRSE03 + EP-BRSE02 + EP-BRSE01 + ES-BRSR06 +ES-BRSR05 + ES-BRSR04 + ES-BRSR03 + ES-BRSR02 + ES-BRSR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def fdm_baseLicense_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#FDM Base license= HC-SV0001 + HC-SV0000
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def fdm_ServiceDevicePoints_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Service Device points= HC-SV0016*16+ HC-SV0032*32+ HC-SV0064*64+HC-SV0128*128+ HC-SV0256*256+HC-SV0512*512+ HC-SV1024*1024+ HC-SV2048*2048+ HC-SV4096*4096+ HC-SV8192*8192+ HC-SV016K*16000
		cal_qty = 0
		for i in parts:
			if i == 'HC-SV0016':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 16
			elif i == 'HC-SV0032':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 32
			elif i == 'HC-SV0064':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 64
			elif i == 'HC-SV0128':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 128
			elif i == 'HC-SV0256':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 256
			elif i == 'HC-SV0512':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 512
			elif i == 'HC-SV1024':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 1024
			elif i == 'HC-SV2048':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 2048
			elif i == 'HC-SV4096':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 4096
			elif i == 'HC-SV8192':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 8192
			elif i == 'HC-SV016K':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				cal_qty += float(qty) * 16000
		self.assign_value(Product,attr,cal_qty)
	
	def fdm_auditTrailDevicePoints_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Audit Trail Device points= HC-AT0016*16+ HC-AT0032*32+ HC-AT0064*64+ HC-AT0128*128+ HC-AT0256*256+ HC-AT0512*512+ HC-AT1024*1024+ HC-AT2048*2048+ HC-AT4096*4096+ HC-AT8192*8196+ HC-AT016K*16000
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			if i == 'HC-AT0016':
				cal_qty += float(qty) * 16
			elif i == 'HC-AT0032':
				cal_qty += float(qty) * 32
			elif i == 'HC-AT0064':
				cal_qty += float(qty) * 64
			elif i == 'HC-AT0128':
				cal_qty += float(qty) * 128
			elif i == 'HC-AT0256':
				cal_qty += float(qty) * 256
			elif i == 'HC-AT0512':
				cal_qty += float(qty) * 512
			elif i == 'HC-AT1024':
				cal_qty += float(qty) * 1024
			elif i == 'HC-AT2048':
				cal_qty += float(qty) * 2048
			elif i == 'HC-AT4096':
				cal_qty += float(qty) * 4096
			elif i == 'HC-AT8196':
				cal_qty += float(qty) * 8196
			elif i == 'HC-AT016K':
				cal_qty += float(qty) * 16000
		self.assign_value(Product,attr,cal_qty)
	def fdm_RciInterfaces__sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#RCI Interfaces= IF(IF(HC-RIOMX1>0 then 25, else 0)=25 then 25, else HC-SM0000+HC-RI0000)
		cal_qty = 0
		fl = '' 
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			if i == 'HC-RIOMX1':
				if float(qty) > 0:
					self.assign_value(Product,attr,25)
					fl = False
					break
		for i in parts:
			if fl != False:
				if i == 'HC-SM0000' or i == 'HC-RI0000':
					qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
					cal_qty += float(qty)
		else:
			if fl != False:
				self.assign_value(Product,attr,cal_qty)
	
	def fdm_fdmClients_sf_value(self,Product,attr,sys_name,msid,part,get_sfdc_response):
		#FDM Clients= qty of HC-CLNT00
		qty = self.get_qty(sys_name,msid,part,get_sfdc_response)
		self.assign_value(Product,attr,qty)
	def fdm_fdmMuxInterfaces_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#MUX interfaces= IF(HC-HMOMX1>0 then 25 , else qty of HC-HM0000)
		fl = ''
		for i in parts:
			if i == 'HC-HMOMX1':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				if float(qty) > 0:
					self.assign_value(Product,attr,25)
					fl = False
					break
		for i in parts:
			if fl != False:
				if i == 'HC-HM0000':
					qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
					self.assign_value(Product,attr,qty)
					break
	def fdm_fdmMuxInterfaces_sf_value1(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#MUX interfaces= IF(HC-MMOMX1>0, then 25 else qty of HC-MM0000)
		fl = ''
		for i in parts:
			if i == 'HC-MMOMX1':
				qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
				if float(qty) > 0:
					self.assign_value(Product,attr,25)
					fl = False
					break
		for i in parts:
			if fl != False:
				if i == 'HC-MM0000':
					qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
					self.assign_value(Product,attr,qty)
					break
	
	def evst_ExperionProcessPoints_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Experion Process Points= EP-DPR01K*1000 + EP-DPR02K*2000 + EP-DPR05K*5000 + EP-DPR100*100 + EP- DPR10K*10000 + ES-DPR01K*1000 + ES-DPR02K*2000 + ES-DPR05K*5000 + ES-DPR100*100 + ES-DPR10K*10000
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			if i == 'EP-DPR01K':
				cal_qty += float(qty) * 1000
			if i == 'EP-DPR02K':
				cal_qty += float(qty) * 2000
			if i == 'EP-DPR05K':
				cal_qty += float(qty) * 5000
			if i == 'EP-DPR100':
				cal_qty += float(qty) * 100
			if i == 'EP- DPR10K':
				cal_qty += float(qty) * 10000
			if i == 'ES-DPR01K':
				cal_qty += float(qty) * 1000
			if i == 'ES-DPR02K':
				cal_qty += float(qty) * 2000
			if i == 'ES-DPR05K':
				cal_qty += float(qty) * 5000
			if i == 'ES-DPR100':
				cal_qty += float(qty) * 100
			if i == 'ES-DPR10K':
				cal_qty += float(qty) * 10000
		self.assign_value(Product,attr,cal_qty)
	def evst_experionScadaPoints_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Experion SCADA Points= EP-DSC01K*1000 + EP-DSC02K*2000 + EP-DSC05K*5000 + EP-DSC100*100 + EP-DSC10K*10000 + ES-DSC01K*1000 + ES-DSC02K*2000 + ES-DSC05K*5000 + ES-DSC100*100 + ES-DSC10K*10000
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			if i == 'EP-DSC01K':
				cal_qty += float(qty) * 1000
			if i == 'EP-DSC02K':
				cal_qty += float(qty) * 2000
			if i == 'EP-DSC05K':
				cal_qty += float(qty) * 5000
			if i == 'EP-DSC100':
				cal_qty += float(qty) * 100
			if i == 'EP-DSC10K':
				cal_qty += float(qty) * 10000
			if i == 'ES-DSC10K':
				cal_qty += float(qty) * 10000
			if i == 'ES-DSC100':
				cal_qty += float(qty) * 100
			if i == 'ES-DSC05K':
				cal_qty += float(qty) * 5000
			if i == 'ES-DSC02K':
				cal_qty += float(qty) * 2000
			if i == 'ES-DSC01K':
				cal_qty += float(qty) * 1000
		self.assign_value(Product,attr,cal_qty)
	def evst_FlexStations_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Flex stations= EP-STAT01 + EP-STAT05*5 + EP-STAT10*10 + ES-STAT01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			if i == 'EP-STAT01':
				cal_qty += float(qty)
			if i == 'EP-STAT05':
				cal_qty += float(qty) * 5
			if i == 'EP-STAT10':
				cal_qty += float(qty) * 10
			if i == 'ES-STAT01':
				cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def evst_consoleStations_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Console stations= EP-STAC01 + EP-STAC05*5 + EP-STAC10*10 + ES-STAC01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			if i == 'EP-STAC01':
				cal_qty += float(qty)
			if i == 'EP-STAC05':
				cal_qty += float(qty) * 5
			if i == 'EP-STAC10':
				cal_qty += float(qty) * 10
			if i == 'ES-STAC01':
				cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def evst_ep_brwe06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRWE06= Qty of EP-BRWE06 + EP-BRWE05 + EP-BRWE04 + EP-BRWE03 + EP-BRWE02 + EP-BRWE01 + ES-BRWR06 + ES-BRWR05 + ES-BRWR04 + ES-BRWR03 + ES-BRWR02 + ES-BRWR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	
	def evst_ep_brve06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRVE06= Qty of EP-BRVE06 + EP-BRVE05 + EP-BRVE04 + EP-BRVE03 + EP-BRVE02 + EP-BRVE01 + ES- BRVR06 + ES-BRVR05 + ES-BRVR04 + ES-BRVR03 + ES-BRVR02 + ES-BRVR01
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def evst_ep_brse06_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-BRSE06= EP-BRSE06 + EP-BRSE05 + EP-BRSE04 + EP-BRSE03 + EP-BRSE02 + EP-BRSE01 + ES-BRSR06 +ES-BRSR05 + ES-BRSR04 + ES-BRSR03 + ES-BRSR062 + ES-BRSR06
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)
	def evst_serverRedundancy_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#Server Redundancy= If any of the part (EP-RBASE1 or ES-RBASE1) is present, then Server Redundancy= Yes
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		if cal_qty > 0:
			self.assign_value(Product,attr,'Yes')
	def evst_mz_sqlcl4_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#MZ-SQLCL4- Not added with EP-UPANR1. Qty= If (Server redundancy= "Yes",2,1) + Number of Flex stations + Number of Console stations
		server_redundancy = Product.Attr('ServerRedundancy_ESTVC_OTU_SESP').GetValue #give attr name
		if server_redundancy == 'Yes':
			cal_qty = 2
		else:
			cal_qty = 1
		flex_stations = Product.Attr('flexStations_ESTVC_OTU_SESP').GetValue()
		console_stations = Product.Attr("ConsoleStations_ESTVC_OTU_SESP").GetValue()
		cal_qty += float(flex_stations)
		cal_qty += float(console_stations)
		self.assign_value(Product,attr,cal_qty)
	def evst_ep_iaddvm_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-IADDVM- Qty= If (Experion DVM Integration="Yes",1,0)
		qty = Product.Attr("ExpDVMIntr_ESTVC_OTU_SESP").GetValue() # dvm intgr attr name
		if qty == 'Yes':
			r = 1
		else:
			r = 0 
		self.AssignValue(Product,attr,r)
	def evst_ep_coas16_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#EP-COAS16= Not added with EP-UPANR1. Qty= If (system redundancy= "Yes",2,1)
		qty = Product.Attr('ServerRedundancy_ESTVC_OTU_SESP').GetValue()
		if qty == 'Yes':
			r = 2
		else:
			r = 1
		self.assign_value(Product,attr,r)
	
	def evst_ep_coaw10_sf_value(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		#h.) EP-COAW10- Not added with EP-UPANR1. Qty= Number of Flex stations + Number of Console stations
		qty = float(Product.Attr('flexStations_ESTVC_OTU_SESP').GetValue) + float(Product.Attr('ConsoleStations_ESTVC_OTU_SESP').GetValue)
		self.assign_value(Product,attr,qty)
	def experionTPS_mz_sqlcl4_sf_value(self,Product,attr,sys_name,msid,parts):
		#MZ-SQLCL4- qty as per the qty of EP-CONTPS
		qty = float(Product.Attr(attr).GetValue())
		self.assign_value(Product,attr,qty)
	def experionTPS_ep_coas16_sf_value(self,Product,attr,sys_name,msid,part,get_sfdc_response):
		#EP-COAS16- qty as per the qty of EP-ABV020
		qty = float(self.get_qty(sys_name,msid,part,get_sfdc_response))
		self.assign_value(Product,attr,qty)
	def experionTps_ep_coaw10_sf_value(self,Product,attr,sys_name,msid,part,get_sfdc_response):
		#EP-COAW10- qty as per the qty of EP-CONTPS
		qty = float(self.get_qty(sys_name,msid,part,get_sfdc_response))
		self.assign_value(Product,attr,qty)

	def common_calculation(self,Product,attr,sys_name,msid,parts,get_sfdc_response):
		cal_qty = 0
		for i in parts:
			qty = self.get_qty(sys_name,msid,i,get_sfdc_response)
			cal_qty += float(qty)
		self.assign_value(Product,attr,cal_qty)