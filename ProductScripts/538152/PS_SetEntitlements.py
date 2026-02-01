HIF_Cont = Product.GetContainerByName("SC_WEP_Entitlement_HIF")
IFS_Cont = Product.GetContainerByName("SC_WEP_Entitlement_IFS")
Halo_Cont = Product.GetContainerByName("SC_WEP_Entitlement_Halo")
TNA_Cont = Product.GetContainerByName("SC_WEP_Entitlement_TNA")
Training_Cont = Product.GetContainerByName("SC_WEP_Entitlement_Training")
OM_Cont = Product.GetContainerByName("SC_WEP_Entitlement_OM")
OCP_Cont = Product.GetContainerByName("SC_WEP_Entitlement_OCP")
HIF_Cont.Rows.Clear()
IFS_Cont.Rows.Clear()
Halo_Cont.Rows.Clear()
TNA_Cont.Rows.Clear()
Training_Cont.Rows.Clear()
OM_Cont.Rows.Clear()
OCP_Cont.Rows.Clear()

entitlementQuery = SqlHelper.GetList("select Entitlement from CT_SC_ENTITLEMENTS_DATA where ServiceProduct='Workforce Excellence Program'")
if entitlementQuery is not None:
    for row in entitlementQuery:
        hif = HIF_Cont.AddNewRow(False)
        hif["Entitlement"] = row.Entitlement
        ifs = IFS_Cont.AddNewRow(False)
        ifs["Entitlement"] = row.Entitlement
        halo = Halo_Cont.AddNewRow(False)
        halo["Entitlement"] = row.Entitlement
        tna = TNA_Cont.AddNewRow(False)
        tna["Entitlement"] = row.Entitlement
        ocp = OCP_Cont.AddNewRow(False)
        ocp["Entitlement"] = row.Entitlement

trainingEntitlementQuery = SqlHelper.GetList("select Entitlement from CT_SC_ENTITLEMENTS_DATA where ServiceProduct='Training'")
if trainingEntitlementQuery is not None:
    for row in trainingEntitlementQuery:
        training = Training_Cont.AddNewRow(False)
        training["Entitlement"] = row.Entitlement

om = OM_Cont.AddNewRow(False)
om["Entitlement"] = "E-Learning Subscription - O&M"