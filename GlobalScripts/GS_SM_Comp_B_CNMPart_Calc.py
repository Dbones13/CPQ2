#CXCPQ-33640
import System.Decimal as D
from GS_SM_CompA1_Calcs import get_CompA1

def Comp_B_CNMPart_Calc(Prod):
    Trace.Write("Product Name : "+Prod.Name)
    #Control Group
    Comp_B_Dict = dict()
    comp_a = {}
    try:
        comp_a = get_CompA1(Prod)
    except:
        Trace.Write("Error getting Component A value")
    if comp_a:
        a6_b1 = {0:8, 1:7, 2:6, 3:5, 4:4, 5:4, 6:4, 7:4, 8:4, 9:3, 10:2, 11:1, 12:0}
        Trace.Write("A comp = "+str(comp_a))
        B1 = a6_b1[comp_a['A6']]
        Trace.Write(B1)
        if comp_a['A2'] > B1:
            B2 = comp_a['A2'] - B1
        else:
            B2 = 0
        Trace.Write(B2)
        if B2 > B1:
            B3 = 1
        else:
            B3 = 0
        Trace.Write(B3)
        if comp_a['A2'] > B1:
            B4 = (comp_a['A2'] - B1) + B3
        else:
            B4 = B3
        Trace.Write(B4)
        B5 = int(D.Ceiling(float(B4)/float(8)))
        Trace.Write(B5)
        B6 = B5
        Trace.Write(B6)
        if B4 <= 4:
            B7 = 0
        else:
            B7 = 1
        Trace.Write(B7)
        Comp_B_Dict={'B1':B1,'B2':B2,'B3':B3,'B4':B4,'B5':B5,'B6':B6,'B7':B7}
    else:
        Trace.Write("Returning empty dictionary for Component B as Component A is empty")
    return Comp_B_Dict