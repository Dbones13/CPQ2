#Calculation For Display count 
import math
import System.Decimal as D
market_seg=TagParserProduct.ParseString('<*CTX( Quote.CustomField(Market Segment))*>')
Trace.Write(market_seg)
if Product.Attr('Is HMI Engineering in Scope?').GetValue()=="Yes":
    display_s=display_m=display_c=display_s1=display_m1=display_c1=0
    display=Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[0].GetColumnByName('Customer Data').Value
    Methodology=Product.Attr('Implementation Methodology').GetValue()
    Trace.Write(Methodology)
    if display=='':
        display=0
    Trace.Write(display)
    if Methodology=="Non-Standard Build Estimate":
        display1=round((math.sqrt(int(float(display))))*8)
        if display1 >300:
            display1=300
        if market_seg=="1000 - Refining":
            display_s=round(0.2* display1)
            display_m=round(0.7* display1)
            display_c=round(0.1* display1)
        elif market_seg=="1400 - Chemicals and Petrochem":
            display_s=round(0.4* display1)
            display_m=round(0.4* display1)
            display_c=round(0.2* display1)
        elif market_seg=="1100 - Oil and Gas":
            display_s=round(0.25* display1)
            display_m=round(0.65* display1)
            display_c=round(0.1* display1)
        elif market_seg=="1600 - Life Sciences":
            display_s=round(0.1* display1)
            display_m=round(0.7* display1)
            display_c=round(0.2* display1)
        elif market_seg=="1200 - Pulp, Paper, Printing & CWS":
            display_s=round(0.25* display1)
            display_m=round(0.4* display1)
            display_c=round(0.35* display1)
        elif market_seg=="1300 - Power Generation":
            display_s=round(0.1* display1)
            display_m=round(0.7* display1)
            display_c=round(0.2* display1)
        elif market_seg!='':
            display_s=round(0.2* display1)
            display_m=round(0.6* display1)
            display_c=round(0.2* display1)
    #for standard
    elif Methodology=="Standard Build Estimate":
        display1=round((math.sqrt(int(float(display))))*0.8)
        if display1 >30:
            display1=30
        if market_seg=="1000 - Refining":
            display_s=round(0.2*display1)
            display_m=round(0.7*display1)
            display_c=round(0.1*display1)
        elif market_seg=="1400 - Chemicals and Petrochem":
            display_s=round(0.4*display1)
            display_m=round(0.4*display1)
            display_c=round(0.2*display1)
        elif market_seg=="1100 - Oil and Gas":
            display_s=round(0.25*display1)
            display_m=round(0.65*display1)
            display_c=round(0.1*display1)
        elif market_seg=="1600 - Life Sciences":
            display_s=round(0.1*display1)
            display_m=round(0.7*display1)
            display_c=round(0.2*display1)
        elif market_seg=="1200 - Pulp, Paper, Printing & CWS":
            display_s=round(0.25*display1)
            display_m=round(0.4*display1)
            display_c=round(0.35*display1)
        elif market_seg=="1300 - Power Generation":
            display_s=round(0.1*display1)
            display_m=round(0.7*display1)
            display_c=round(0.2*display1)
        elif market_seg!='':
            display_s=round(0.2*display1)
            display_m=round(0.6*display1)
            display_c=round(0.2*display1)

    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[4].SetColumnValue('Calculated Value', "0")
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[5].SetColumnValue('Calculated Value', "0")
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[6].SetColumnValue('Calculated Value', str(int(display_s)))
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[7].SetColumnValue('Calculated Value', str(int(display_m)))
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[8].SetColumnValue('Calculated Value', str(int(display_c)))
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[9].SetColumnValue('Calculated Value', "0")
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[10].SetColumnValue('Calculated Value', "0")
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[14].SetColumnValue('Calculated Value', "0")
    Product.GetContainerByName('Experion_Ent_Displays_Shapes_Faceplates').Rows[15].SetColumnValue('Calculated Value', "0")