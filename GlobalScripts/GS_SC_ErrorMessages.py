###############################################################################################
# Class CL_CustomerModules:
#       Class to handle error messages for service contract
###############################################################################################
class MessageHandler:

    def __init__(self, Quote):
        self.Quote = Quote
    # Message Structure
    # ErrorMsg = {"TeamRoles" : [{"Id": 1, "Type" : "Error", "Text" : ""}, {"Id": 2,"Type" : "Warning", "Text" : ""}, {"Id": 3, "Type" : "Info", "Text" : ""}], "FlexiHours":[{"Id": 1, "Type" : "Error", "Text" : ""}]}
    ###############################################################################################
    # Function to Add error messages
    ###############################################################################################
    def GetMessage(self, MsgName, MsgId = 0):
        ErrorMsg = self.Quote.GetCustomField('SC_CF_Error_Msg').Content
        ErrorMsgDist = {}
        msg = None
        if ErrorMsg:
            ErrorMsgDist = eval(ErrorMsg)
            if type(ErrorMsgDist) is not dict:
                ErrorMsgDist =  {}
        msgList = ErrorMsgDist.get(MsgName, [])
        Trace.Write("Val: {}, Type: {}".format(MsgId, type(MsgId)))
        if MsgId:
            msg = next((mitem for mitem in msgList if mitem.get("Id", '') == MsgId), None) #next(mitem for mitem in msgList if mitem["Id"] == MsgId) #next(mitem for mitem in msgList if mitem["Id"] == MsgId)
        return ErrorMsgDist, msgList, msg

    def RemoveMessage(self, msgList, MsgId):
        delList = []
        Trace.Write('123')
        for i in range(len(msgList)):
            if msgList[i]['Id'] == MsgId:
                Trace.Write(i)
                delList.append(i)
        for index in sorted(delList, reverse=True):
            del msgList[index]
        return msgList

    def AddMessage(self, MsgName, MsgType, MsgText, MsgId = 0):
        ErrorMsgDist, msgList, msg = self.GetMessage(MsgName, MsgId)
        if msg:
            msgList = self.RemoveMessage(msgList, MsgId)
        msgList.append({"Id": MsgId, "Type": MsgType, "Text": MsgText})
        ErrorMsgDist[MsgName] =  msgList
        self.Quote.GetCustomField('SC_CF_Error_Msg').Content = str(ErrorMsgDist).replace("'", '"')

    def DeleteMessageByName(self, MsgName):
        ErrorMsgDist, msgList, msg = self.GetMessage(MsgName)
        if msgList:
            del ErrorMsgDist[MsgName]
        self.Quote.GetCustomField('SC_CF_Error_Msg').Content = str(ErrorMsgDist).replace("'", '"')

    def DeleteMessage(self, MsgName, MsgId = 0):
        ErrorMsgDist, msgList, msg = self.GetMessage(MsgName)
        if MsgId and msgList:
            msgList = self.RemoveMessage(msgList, MsgId)
            ErrorMsgDist[MsgName] =  msgList
        else:
            if ErrorMsgDist.get(MsgName, ''): del ErrorMsgDist[MsgName]
        self.Quote.GetCustomField('SC_CF_Error_Msg').Content = str(ErrorMsgDist).replace("'", '"')

    def DeleteAllMessage(self, Name, Message):
        self.Quote.GetCustomField('SC_CF_Error_Msg').Content = ""