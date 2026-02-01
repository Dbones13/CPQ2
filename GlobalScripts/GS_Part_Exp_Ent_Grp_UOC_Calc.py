#CXCPQ-45551
import System.Decimal as D

def part_qty_100_50(user_input):
	qty_100 = qty_50 = 0
	q_100 = user_input / 100
	r_100 = user_input % 100
	Trace.Write("q_100 = "+str(q_100))
	Trace.Write("r_100 = "+str(r_100))
	if q_100 == 0 and r_100 > 50:
		qty_100 = 1
	elif q_100 > 0 and r_100 > 50:
		qty_100 = q_100 + 1
	elif q_100 > 0 and r_100 <= 50:
		qty_100 = q_100
	if r_100 <= 50 and r_100 != 0:
		qty_50 = 1
	return int(qty_100), int(qty_50)
	
def part_qty_100(user_input):
	qty_100 = 0
	q_100 = user_input / 100
	r_100 = user_input % 100
	Trace.Write("q_100 = "+str(q_100))
	Trace.Write("r_100 = "+str(r_100))
	if r_100 == 0:
		qty_100 = q_100
	elif r_100 > 0:
		qty_100 = q_100 + 1
	return int(qty_100)
	
def part_qty_100_10(user_input):
	qty_100 = qty_10 = 0
	q_100 = user_input / 100
	r_100 = user_input % 100
	Trace.Write("q_100 = "+str(q_100))
	Trace.Write("r_100 = "+str(r_100))
	if q_100 >= 0 and r_100 > 90:
		qty_100 = q_100 + 1
	elif q_100 > 0 and r_100 <= 90:
		qty_100 = q_100
	
	if r_100 <= 90 and r_100 != 0:
		if (r_100 % 10) == 0:
			qty_10 = r_100 / 10
		elif (r_100 % 10) > 0:
			qty_10 = (r_100 / 10) + 1
	return int(qty_100), int(qty_10)

def part_qty_1000_50(user_input):
	q_1000, r_1000 = divmod(user_input,1000) 
	q_100, r_100 = divmod(r_1000,100)
	q_50, r_50 = divmod(r_100,50)
	abt_q_100 = q_100
	if (q_100 > 0 and r_100 > 50) or (q_100 == 0 and r_100 > 50):
		abt_q_100 = q_100 + 1
	if (q_50 > 0 and r_50 > 0) or (q_50 == 0 and r_50 > 0):
		q_50 = q_50 + 1
	return q_1000, q_100, q_50, abt_q_100
#x, y = part_qty_100_50(690)
#i = part_qty_100(290)
#a, b = part_qty_100_10(230)