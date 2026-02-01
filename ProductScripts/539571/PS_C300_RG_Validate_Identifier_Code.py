import re
def formatCheck(code):
    if (len(code) < 25 or len(code) > 27):
        return False
    #ABC-DEFSTUV-G##HJKLM-NP-QRW
    #ABC-DEFSTUV-G#HJKLM-NP-QRW
    pattern = r"^[A-Z0-9]{3}-[A-Z0-9]{7}-[A-Z0-9][0-9]{0,2}[A-Z0-9]{5}-[A-Z0-9]{2}-[A-Z0-9]{3}$"
    return re.match(pattern, code) is not None


def applyConstraintChecks(codePosMap, nums):
    msgSet = set()
    codePosMap["NUMS"] = nums
    codePosMap["NUM_LEN"] = str(len(nums))
    codePosMap["GNUMS"] = "{}{}".format(codePosMap["G"],nums)
    codePosMap["DS"] = "{}{}".format(codePosMap["D"],codePosMap["S"])
    codePosMap["ExpRel"] = Product.Attr("Experion_PKS_Software_Release").GetValue()

    restrictionsMap = {
        "D" : [
            {
                "value" : ["N"],
                "dependent" : "R",
                "allow" : ["0"],
                "disallow" : [],
                "msg" : "Software Licenses will not be required if CN100 is not selected"
            },{
                "value" : ['H', 'R', 'M', 'T', 'A', 'B'],
                "dependent" : "E",
                "allow" : ["0"],
                "disallow" : [],
                "msg" : "When CN100 is selected, FOEs are not used to interconnect other cabinets.<br />CN100 used for IO hive will no longer use the Fiber Optic Extenders. In place of the Fiber Optic Extender, the CNM can be installed for specific communication topologies."
            },{
                "value" : ['H', 'R'],
                "dependent" : "F",
                "allow" : ["S", "0"],
                "disallow" : [],
                "msg" : "To maintain a common communication backbone, if Single-Mode is selected, only Single-Mode can be selected when external FDAP communication is necessary."
            },{
                "value" : ['M', 'T'],
                "dependent" : "F",
                "allow" : ["M", "0"],
                "disallow" : [],
                "msg" : "To maintain a common communication backbone, if Multi-Mode is selected, only Multi-Mode can be selected when external FDAP communication is necessary."
            },{
                "value" : ['H', 'R'],
                "dependent" : "U",
                "allow" : ["A", "C"],
                "disallow" : [],
                "msg" : "The communication backbone is required to be the same for CNM and CN100"
            },{
                "value" : ['M', 'T'],
                "dependent" : "U",
                "allow" : ["B", "D"],
                "disallow" : [],
                "msg" : "The communication backbone is required to be the same for CNM and CN100"
            },{
                "value" : ["N"],
                "dependent" : "S",
                "allow" : ["N"],
                "disallow" : [],
                "msg" : "CNM can only be used when CN100 is installed to ensure IO Link communication is maintained with the installed IO modules."
            },{
                "value" : ["N"],
                "dependent" : "V",
                "allow" : ["N"],
                "disallow" : [],
                "msg" : "EIM can only be used when CN100 and CNM are installed."
            }
        ],
        "E" : [
            {
                "value" : ['S', 'T'],
                "dependent" : "F",
                "allow" : ["S", "0"],
                "disallow" : [],
                "msg" : "To maintain a common communication backbone, if Single-Mode is selected, only Single-Mode can be selected when external FDAP communication is necessary."
            },{
                "value" : ['M', 'N'],
                "dependent" : "F",
                "allow" : ["M", "0"],
                "disallow" : [],
                "msg" : "To maintain a common communication backbone, if Multi-Mode is selected, only Multi-Mode can be selected when external FDAP communication is necessary."
            }
        ],
        "J" : [
            {
                "value" : ['3'],
                "dependent" : "L",
                "allow" : ["0", "1", "2"],
                "disallow" : [],
                "msg" : "Space limited by 1 x 36” CCA for IO mounting."
            },{
                "value" : ['6'],
                "dependent" : "L",
                "allow" : ["0", "1"],
                "disallow" : [],
                "msg" : "Space limited by 1 x 36” CCA for IO mounting."
            },{
                "value" : ['9'],
                "dependent" : "L",
                "allow" : ["0"],
                "disallow" : [],
                "msg" : "Space limited by 1 x 36” CCA and 1 x 18” CCA available for IO mounting."
            }
        ],
        "L" : [
            {
                "value" : ['3', '4', '5', '6', '7', '8'],
                "dependent" : "G",
                "allow" : ["X"],
                "disallow" : [],
                "msg" : "Once over 2 LLAI's are chosen, the LLAI only cabinet build must be used. The UIO2/LLAI mixed cabinet is limited by 1 x 36: CCA for IO mounting."
            },{
                "value" : ['3', '4', '5', '6', '7', '8'],
                "dependent" : "J",
                "allow" : ["0"],
                "disallow" : [],
                "msg" : "Once over 2 LLAI's are chosen, the LLAI only cabinet build must be used. The UIO2/LLAI mixed cabinet is limited by 1 x 36: CCA for IO mounting."
            },{
                "value" : ['3', '4', '5', '6', '7', '8'],
                "dependent" : "F",
                "allow" : ["0"],
                "disallow" : [],
                "msg" : "Once over 2 LLAI's are chosen, the LLAI only cabinet build must be used. The UIO2/LLAI mixed cabinet is limited by 1 x 36: CCA for IO mounting."
            }
        ],
        "GNUMS" : [
            {
                "value" : ['N20', 'N02'],
                "dependent" : "J",
                "allow" : ["3"],
                "disallow" : [],
                "msg" : "32 points of UIO are required."
            },{
                "value" : ['N40', 'N04', 'N22'],
                "dependent" : "J",
                "allow" : ["6"],
                "disallow" : [],
                "msg" : "64 points of UIO are required."
            },{
                "value" : ['N60', 'N06', 'N24', 'N42'],
                "dependent" : "J",
                "allow" : ["9"],
                "disallow" : [],
                "msg" : "96 points of UIO are required."
            },
        ],
        "G" : [
            {
                "value" : ['N'],
                "dependent" : "NUMS",
                "allow" : ["02", "04", "06", "20", "22", "24", "26", "40", "42", "44", "46", "60", "62", "64", "66"],
                "disallow" : ["00"],
                "msg" : "Universal Marshalling is selected, Input the Number of GIIS Bases and/or Non-GIIS Bases required."
            },{
                "value" : ['G'],
                "dependent" : "NUMS",
                "allow" : ["2", "4", "6", "20", "40", "60"],
                "disallow" : ["0", "00"],
                "msg" : "Universal Marshalling GI only is selected, Input the Number of GI Bases required (16 GI Channels/base)."
            },{
                "value" : ['M'],
                "dependent" : "NUMS",
                "allow" : ["0", "00", ""],
                "disallow" : [],
                "msg" : "Values > 0 are only applicable when Universal Marshalling, GIIS (0-6)/ Non-GIIS (0-6) or GI only (0-6) is selected for the Field Termination Assembly."
            },{
                "value" : ['X'],
                "dependent" : "NUMS",
                "allow" : ["0", "00", ""],
                "disallow" : [],
                "msg" : "Values > 0 are only applicable when Universal Marshalling, GIIS (0-6)/ Non-GIIS (0-6) or GI only (0-6) is selected for the Field Termination Assembly."
            },
        ],
        "DS" : [
            {
                "value" : ['HY', 'RY', 'MY', 'TY', 'AY', 'BY'],
                "dependent" : "J",
                "allow" : ["0","3", "6"],
                "disallow" : [],
                "msg" : "Once the CNM is installed the number of IO will be constrained."
            },{
                "value" : ['HN', 'RN', 'MN', 'TN', 'AN', 'BN'],
                "dependent" : "V",
                "allow" : ["N"],
                "disallow" : [],
                "msg" : "EIM can only be used when CN100 and CNM are installed."
            },{
                "value" : ['HN', 'RN', 'MN', 'TN', 'AN', 'BN'],
                "dependent" : "T",
                "allow" : ["N"],
                "disallow" : [],
                "msg" : "The CNM Expansion Module is only available when the CNM is installed."
            }
        ],
        "ExpRel" : [
            {
                "value" : ["R510", "R511"],
                "dependent" : "D",
                "allow" : ["N"],
                "disallow" : [],
                "msg" : "Experion PKS Software Release 'R510' and 'R511' does not support Control & IO Network Module (CN100), Control Network Module (CNM) and Ethernet Interface Module (EIM)"
            },{
                "value" : ["R510", "R511"],
                "dependent" : "S",
                "allow" : ["N"],
                "disallow" : [],
                "msg" : "Experion PKS Software Release 'R510' and 'R511' does not support Control & IO Network Module (CN100), Control Network Module (CNM) and Ethernet Interface Module (EIM)"
            },{
                "value" : ["R510", "R511"],
                "dependent" : "T",
                "allow" : ["N"],
                "disallow" : [],
                "msg" : "Experion PKS Software Release 'R510' and 'R511' does not support Control & IO Network Module (CN100), Control Network Module (CNM) and Ethernet Interface Module (EIM)"
            },{
                "value" : ["R510", "R511"],
                "dependent" : "U",
                "allow" : ["B"],
                "disallow" : [],
                "msg" : "Experion PKS Software Release 'R510' and 'R511' does not support Control & IO Network Module (CN100), Control Network Module (CNM) and Ethernet Interface Module (EIM)"
            },{
                "value" : ["R510", "R511"],
                "dependent" : "V",
                "allow" : ["N"],
                "disallow" : [],
                "msg" : "Experion PKS Software Release 'R510' and 'R511' does not support Control & IO Network Module (CN100), Control Network Module (CNM) and Ethernet Interface Module (EIM)"
            }
        ],
    }

    for ch, restrictions in restrictionsMap.items():
        for restriction in restrictions:
            if codePosMap[ch] in restriction["value"]:
                depCharVal = codePosMap[restriction["dependent"]]
                if depCharVal in restriction["disallow"] or depCharVal not in restriction["allow"]:
                    msgSet.add("{}".format(restriction["msg"]))
    return "<br />".join(msgSet)

def validateModifierCode(code):
    MESSAGE_MAP = {
        "INVALID_FORMAT" : "Identifier specified is invalid. Please specify valid Identifier of format ABC-DEFSTUV-G##HJKLM-NP-QRW. Please refer the info icon for valid & detailed Identifier structure.",
        "INVALID_CHAR" : "Identifier specified is invalid. Please specify valid Identifier of format ABC-DEFSTUV-G##HJKLM-NP-QRW. Please refer the info icon for valid & detailed Identifier structure. The character entered in positions {} is invalid."
    }
    invalidPositionList = list()
    if not formatCheck(code):
        return MESSAGE_MAP["INVALID_FORMAT"]
    code = code.replace("-","")
    nums = ""
    removeChar = 0
    if len(code) >= 22:
        nums += code[11]
        if code[11] not in ('0', '2', '4', '6'):
            invalidPositionList.append("G#")
        removeChar = 1
    if len(code) == 23:
        nums += code[12]
        if code[12] not in ('0', '2', '4', '6'):
            invalidPositionList.append("G##")
        removeChar = 2

    code = code[:11] + code[11+removeChar:]
    #consider numbers as one char
    posMap = [
        'A', 'B', 'C', 'D', 'E', 'F', 'S', 'T', 'U', 'V', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'W'
    ]
    validPositionEntryMap = [
        ['P'],
        ['S'],
        ['A', 'B'],
        ['N', 'H', 'R', 'M', 'T', 'A', 'B'],
        ['S', 'T', 'M', '0'],
        ['S', 'M', '0'],
        ['N', 'Y'],
        ['N', 'Y'],
        ['A', 'B', 'C', 'D'],
        ['N', 'Y'],
        ['N', 'M', 'G', 'X'],
        ['N', 'P'],
        ['0', '3', '6', '9'],
        ['R', 'N'],
        ['0', '1', '2', '3', '4', '5', '6', '7', '8'],
        ['0', '1'],
        ['Q', 'A', 'R', 'D'],
        ['R'],
        ['M', 'N'],
        ['0', '2', '8'],
        ['N', 'Y']
    ]

    codePosCharMap = dict()
    for i, ch in enumerate(code):
        codePosCharMap[posMap[i]] = ch
        if ch not in validPositionEntryMap[i]:
            invalidPositionList.append(posMap[i])

    if invalidPositionList:
        return MESSAGE_MAP["INVALID_CHAR"].format(", ".join(invalidPositionList))

    return applyConstraintChecks(codePosCharMap, nums)

msgAttr = Product.Attr('C300_RG_UPC_Modifier_ID_Validation_Error')
msg = ""
if Product.Attr("SerC_IO_Mounting_Solution").GetValue() == "Universal Process Cab - 1.3M" and Product.Attr("C300_RG_UPC_Specify_Id_Modifier").GetValue() == "Yes":
    modeAttr = Product.Attr('C300_RG_UPC_Id_Modifier')

    modifierCode = modeAttr.GetValue().upper()
    modeAttr.AssignValue(modifierCode)

    msg = validateModifierCode(modifierCode)
msgAttr.AssignValue(msg)