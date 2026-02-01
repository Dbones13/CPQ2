# GS_R2QCalculation_Module
# This module contains functions to execute at the product event when a product is added to a quote. 
# It populates the prices and costs in the cart and the respective quote tables for the R2Q process.

import GS_Market_Customer_R2Q as price_calc

"""
Handles R2Q-specific calculations, including pricing, repricing, and document generation.
"""

def Custom_Actionid(system_id):
	"""
	Retrieves the custom action ID using the provided system ID.
	"""
	action_id = SqlHelper.GetFirst("Select ACTION_ID from ACTIONS where SYSTEM_ID = '{}'".format(system_id))
	return action_id.ACTION_ID

def After_Addedtoquote_Reprice(Quote):
	"""
	Triggers the new custom action 'Reprice_New' by setting the 'Reprice Flag' field and executing the action.
	"""
	Quote.GetCustomField('Reprice Flag').Content = 'True'  # This flag triggers the new custom action
	action_id = Custom_Actionid('Reprice_New_cpq')
	Quote.ExecuteAction(action_id)

def Customer_Budget(Quote):
	"""
	Determines the price based on the selection of market price or customer budget
	when an R2Q quote is created.
	"""
	price_calc.market_customer_r2q(Quote)

def Calculate_Reprice(Quote):
	"""
	Triggers the existing custom action 'Reprice' in the system.
	"""
	action_id = Custom_Actionid('Reprice_cpq')
	Quote.ExecuteAction(action_id)

def Generate_R2q_Document(Quote):
	"""
	Triggers the custom action 'Generate_Document_R2Q' to generate the R2Q document.
	"""
	action_id = Custom_Actionid('Trigger_R2Q_Approval_cpq')
	Quote.ExecuteAction(action_id)