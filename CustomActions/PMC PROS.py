from System.Net import HttpWebRequest
from math import ceil
from System.Text import Encoding

def getKeyDict():
    query = "select * from HPS_INTEGRATION_PARAMS"
    keyDict = dict()
    for r in SqlHelper.GetList(query):
        keyDict[r.Key] = r.Value
    return keyDict
def getToken(keyDict):
    url = "https://{}/v2/oauth/accesstoken".format(keyDict['PROS_Host'])
    Get_Query = "select Name, Identifier from sys_CredentialsStore where Name in ('{}')".format("','".join(["PROS_client_id" , "PROS_client_secret"]))
    Get_res = SqlHelper.GetList(Get_Query)
    #Trace.Write("select Keys , Value from HPS_INTEGRATION_PARAMS where Keys in ('{}')".format("','".join(["PROS_client_id" , "PROS_client_secret"]))")
    keyDict = dict()
    for res in Get_res:
        keyDict[res.Name] = res.Identifier
        #Trace.Write("----->" +str(res))
    payload = "grant_type=client_credentials&client_id={0}&client_secret={1}".format(keyDict["PROS_client_id"],keyDict["PROS_client_secret"])
    Trace.Write("----->1" +str(payload))

    data = Encoding.ASCII.GetBytes(payload)

    webRequest = HttpWebRequest.Create(url)
    webRequest.Method = "POST"
    webRequest.ContentType = "application/x-www-form-urlencoded"
    webRequest.ContentLength = data.Length

    requestStream = webRequest.GetRequestStream()
    requestStream.Write(data , 0 , data.Length)

    response = webRequest.GetResponse()
    responseStream = response.GetResponseStream()

    jsonData = StreamReader(responseStream).ReadToEnd()

    json = RestClient.DeserializeJson(jsonData)

    return "{} {}".format(json.token_type , json.access_token)

keyDict =  getKeyDict()
header = {"Authorization" : getToken(keyDict), "GBE":"PM", "SBG":"HPS"}
Final_Url= 'https://{}/v1/pros/guidance'.format(keyDict['PROS_Host'])

def execute_pros_refresh():
    parameters = ['List Price','WTW Cost','Business Model','Market Segment','Market Sub Segment','BRIC Region','Opportunity Destination Country','PMC Competitor','Business Unit','Customer','nodeName']
    item_data = {new_list: [] for new_list in parameters}
    Business_Model1 = Quote.GetCustomField("Business Model").Content
    Market_Segment = Quote.GetCustomField("Market Segment").Content
    Sub_Market_Segment = Quote.GetCustomField("Sub Market Segment").Content
    Destination_Country = Quote.GetCustomField("Destination Country").Content
    Destination_Country1 = Quote.GetCustomField("Destination Country").Content
    Primary_Competitor = Quote.GetCustomField("Primary_Competitor").Content
    Booking_LOB = Quote.GetCustomField("Booking LOB").Content
    Account_ID = Quote.GetCustomField("AccountId").Content



    
    if Business_Model1 == '' or Business_Model1 is None:
        Business_Model1='All'

    if Market_Segment == '' or Market_Segment is None:
        Market_Segment='All'
    
    if Sub_Market_Segment == '' or Sub_Market_Segment is None:
        Sub_Market_Segment='All'
    
    if Destination_Country == '' or Destination_Country is None:
        Destination_Country = Quote.GetCustomField("Booking Country").Content

    if Destination_Country == '' or Destination_Country is None:
        Destination_Country = 'All'

    if Destination_Country1 == '' or Destination_Country1 is None:
        Destination_Country1 = Quote.GetCustomField("Booking Country").Content

    if Destination_Country1 == '' or Destination_Country1 is None:
        Destination_Country1 = 'All'

    if Primary_Competitor == '' or Primary_Competitor is None:
        Primary_Competitor='All'
    
    if Booking_LOB == '' or Booking_LOB is None:
        Booking_LOB='All'

    if Account_ID == '' or Account_ID is None:
        Account_ID = 'All'

    d = []
    iter_dict1 = {"value":None,"name":None}
    vrlist =[]
    itemResList = []

    #Trace.Write("ffffff"+str(bn))
    #for item in Quote.Items:
    body={"batchItems":[]}
    for item in Quote.MainItems:
        a=0
        #iter_dict1["nodeName"]= item.PartNumber
        Trace.Write('--dfcr-->'+str(item.PartNumber))
        if item.QI_ProductLine.Value !='' and item.QI_No_Discount_Allowed.Value == "0":
            for condition in item.VCPricingPayload.Conditions:
                if str(condition.VarcondKey) !='None':
                    x= str(condition.VarcondKey)
                    #vcn = len(x)
                    d.append(x)
                    iter_dict1["value"]= d[a]
                    iter_dict1["name"]= "Variant Attribute"+ " " +str(a+1)
                    a +=1
                    #Trace.Write("-ddxx->"+str(iter_dict1["value"]))
                    #Trace.Write("ffffff"+str(iter_dict1["name"]))
                    vrlist.append(iter_dict1.copy())
        iter_dict1 = {"value":None,"name":None}
        #Trace.Write("special"+str(vrlist))
    for item in Quote.Items:
        if item.QI_ProductLine.Value !='' and item.QI_No_Discount_Allowed.Value == "0":
            item_data['List Price'].append(str(item.ExtendedListPrice))
            item_data['WTW Cost'].append(str(item.QI_ExtendedWTWCost.Value))
            item_data['Business Model'].append(str(Business_Model1))
            item_data['Market Segment'].append(str(Market_Segment))
            item_data['Market Sub Segment'].append(str(Sub_Market_Segment))
            item_data['BRIC Region'].append(str(Destination_Country))
            item_data['Opportunity Destination Country'].append(str(Destination_Country1))
            item_data['PMC Competitor'].append(str(Primary_Competitor))
            item_data['Business Unit'].append(str(Booking_LOB))
            item_data['Customer'].append(str(Account_ID))
            item_data['nodeName'].append(str(item.PartNumber))
        #Trace.Write("------+ItemData "+str(item_data['nodeName']))
        node_len = len(item_data['nodeName'])
        no_of_batches = int(ceil(float(node_len)/50))
        #Trace.Write("-----------+batches"+str(no_of_batches))
        counter_batches = 0
        check = False
        itemResList = []

    for n in range(no_of_batches):
        batch_items = {"overrides":None,"key":None}
        final_request_body = {"batchItems": None}
        final_req_list = []
        iter_dict1 = {"value":None,"name":None}
        iter_dict2 = {"nodeName":None,"dimName":"Product"}
        iter_list1 = []
        iter_list2 = []
        for i in range(counter_batches,node_len):
            #Trace.Write("countbbbb" + str(counter_batches))
            if(check == False and i!=0 and i%50==0):
                counter_batches = i
                check = True
                break
            else:
                for j in range(len(parameters)):
                    if(j==(len(parameters)-1)):
                        iter_dict2["nodeName"]=item_data[parameters[j]][i]
                        iter_list2.append(iter_dict2.copy())
                        batch_items["key"] = iter_list2[:]
                        #Trace.Write("----check2----"+str(iter_dict2["nodeName"])+" at i="+str(i)+" and j="+str(j)+str(iter_dict2.copy())+" and "+str(iter_list2[:]))
                    else:
                        iter_dict1["value"] = item_data[parameters[j]][i]
                        iter_dict1["name"] = parameters[j]
                        iter_list1.append(iter_dict1.copy())
                        batch_items["overrides"] = iter_list1[:] + vrlist
                        #Trace.Write("----check1----"+str(iter_dict1["value"])+"  "+str(iter_dict1["name"])+" at i="+str(i)+" and j="+str(j)+str(iter_dict1.copy())+" and "+str(iter_list1[:]))
                final_req_list.append(batch_items.copy())
                batch_items = {"overrides":None,"key":None}
                iter_list1 = []
                iter_list2 = []
                check = False
				#if(i==node_len-1):
				#	prev_counter_batches = counter_batches
				#	counter_batches = i
				#	#check = True
				#	#break
        final_request_body["batchItems"] = final_req_list[:]

        #Trace.Write("----finalbody----"+str(n)+str(final_request_body))

		#****************************API Call************************************

        res = RestClient.Post(Final_Url , RestClient.SerializeToJson(final_request_body), header)
        #Trace.Write("-----------+Response"+str(res))



        if res:
            for r in res.itemResults:
                dataDict = dict()
                for s in r.elements:
                    if s.name=="Floor Discount" and s.value is not None:
                        dataDict["Floor Discount"] = round(s.value,2)
                    if s.name=="Expert Discount" and s.value is not None:
                        dataDict["Expert Discount"] = round(s.value,2)
                    if s.name=="Target Discount" and s.value is not None:
                        dataDict["Target Discount"] = round(s.value,2)
                    if s.name=="Guidance Status":
                        dataDict["Guidance Status"] = s.value
                itemResList.append(dataDict)
    PROS_Guidance = Quote.GetCustomField("PROS Guidance Recommendation").Content
    res_index = 0 #[r_ind for r_ind in range(len(itemResList))]

    for Item in Quote.MainItems:
        if Item.QI_ProductLine.Value !='' and Item.QI_No_Discount_Allowed.Value == "0":
            if(res_index < len(itemResList)):
                #Trace.Write("------+index "+str(res_index))
                data = itemResList[res_index]
                #Trace.Write("------+Data "+str(len(data)))
                Item.QI_TARGET_DISCOUNT.Value = data["Target Discount"]
                Item.QI_FLOOR_DISCOUNT.Value = data["Floor Discount"]
                Item.QI_EXPERT_DISCOUNT.Value = data["Expert Discount"]
                Item.QI_Guidance_Status.Value = str(data["Guidance Status"])
                Item.QI_Guidance_Discount_Percent.Value = Item.QI_TARGET_DISCOUNT.Value
                '''if Item.QI_Guidance_Discount_Percent.Value != 0:
                    #only assign Target discount always
                    Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice*(100-Item.QI_Guidance_Discount_Percent.Value)/100
                else:
                    Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice'''
                if PROS_Guidance == "Target Discount":
                    #Quote.GetCustomField("PROS Guidance Recommendation").Content="Target Discount"
                    Item.QI_Guidance_Discount_Percent.Value = Item.QI_TARGET_DISCOUNT.Value
                    if Item.QI_Guidance_Discount_Percent.Value != 0:
                        Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice*(100-Item.QI_Guidance_Discount_Percent.Value)/100
                    else:
                        Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice
                if PROS_Guidance == "Floor Discount":
                    Item.QI_Guidance_Discount_Percent.Value = Item.QI_FLOOR_DISCOUNT.Value
                    if Item.QI_Guidance_Discount_Percent.Value != 0:
                        Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice*(100-Item.QI_Guidance_Discount_Percent.Value)/100
                    else:
                        Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice
                if PROS_Guidance == "Expert Discount":
                    Item.QI_Guidance_Discount_Percent.Value = Item.QI_EXPERT_DISCOUNT.Value
                    if Item.QI_Guidance_Discount_Percent.Value != 0:
                        Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice*(100-Item.QI_Guidance_Discount_Percent.Value)/100
                    else:
                        Item.QI_PROS_Guidance_Recommended_Price.Value = Item.ExtendedListPrice
                res_index += 1
            else:
                break

    Quote.Save(False)
pros_execution = Quote.GetCustomField("PROSActionField").Content

if not User.BelongsToPermissionGroup('Estimator-ProsGuidanceAccess') and pros_execution == 'yes':
    execute_pros_refresh()
    Quote.GetCustomField("PROSActionField").Content="no"
elif not User.BelongsToPermissionGroup('Estimator-ProsGuidanceAccess') and pros_execution == 'no':
    pass
    ScriptExecutor.ExecuteGlobal('GS_PROS_Column_Visibility')
else:
    execute_pros_refresh()
    Quote.GetCustomField("PROSActionField").Content ="no"
