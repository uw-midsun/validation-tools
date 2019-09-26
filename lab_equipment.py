# -*- coding: utf-8 -*-
import visa
import numpy as np
import time

'''
Updated by Micah Black July 2019:
Changes:
	BK8600 E-Load:
		- Support CV, CR, CP modes
		- Support use of Remote Sense Features
		- Support triggering timers
		- Support Transients (current, voltage, resistance, power)
		- Support for lists of current values
	
	34410A DMM:
		- Support for timed interval measurements
	
	To Verify:
		- What happens at the end of a list in the load?
		- What is returned by DATA:REM? command on the DMM - a list or an array?
		
	Resources:
		BK8600 Programming Guide: https://bkpmedia.s3.amazonaws.com/downloads/programming_manuals/en-us/8600_Series_programming_manual.pdf
		E3631A Users and Programming Guide: http://engineering.case.edu/lab/circuitslab/sites/engineering.case.edu.lab.circuitslab/files/docs/Agilent_E3631_Power_Supply_Users_Guide.pdf
		
	Reminder - When programming, make sure all parameters are within the models' parameters (not trying to overload the PSU, e-load, etc)
'''

################################# E-Load ################################
class BK8600:
	# Initialize to the bay's BK8600 address through USB
	def __init__(self, resource_id='USB0::65535::34816::602197010707510034::0::INSTR'):
		rm = visa.ResourceManager()
		self.inst = rm.open_resource(resource_id)
		print("Connected to %s\n" % self.inst.query("*IDN?"))
		self.inst.write("*RST")
		
	def reset(self):
		self.inst.write("*RST")

	# To Set E-Load in Constant Current Mode
	def set_current(self, current_setpoint_A):		
		self.inst.write("FUNCtion CURRent; :CURR:LEV %s" % current_setpoint_A)
		self.inst.query("*OPC?")
		self.inst.write("INPut ON")
		
	# To Set E-Load in Constant Voltage Mode 
	def set_voltage(self, voltage_setpoint_V, min_current_A = 0, max_current_A = 30):	
		self.inst.write("FUNCtion VOLTage; :VOLT:LEV %s;LOW %s;HIGH %s" % (voltage_setpoint_V, min_current_A, max_current_A))
		self.inst.query("*OPC?")
		self.inst.write("INPut ON")
		
	# To Set E-Load in Constant Power Mode
	def set_power(self, power_setpoint_W):		
		self.inst.write("FUNCtion POWer; :POWer:LEV %s" % power_setpoint_W)
		self.inst.query("*OPC?")
		self.inst.write("INPut ON")

	# To Set E-Load in Constant Resistance Mode
	def set_resistance(self, resistance_setpoint_R):		
		self.inst.write("FUNCtion RESistance; :RESistance:LEV %s" % resistance_setpoint_R)
		self.inst.query("*OPC?")
		self.inst.write("INPut ON")

	#setup any type of transient, start the transient with trigger()
	#func = "CURR" | "POW" | "RES" | "VOLT"
	#mode = "CONT" | "PULS" | "TOGG" - pulse will execute 1 cycle on trigger, toggle will toggle state (a->b) on trigger
	#level_units = "S" | "mS" | "uS"
	def transient_setup(self, func = "CURR", mode = "PULSE", alevel = 1, blevel = 1, awidth = 1, awidth_units = "S", bwidth = 1, bwidth_units = "S"):
		#guard for unacceptable values
		if(func != "CURR" or func != "POW" or func != "RES" or func != "VOLT"):
			return False
		if(mode != "CONT" or mode != "PULS" or mode != "TOGG"):
			return False
		if(awidth_units != "S" or awidth_units != "mS" or awidth_units != "uS"):
			return False
		if(bwidth_units != "S" or bwidth_units != "mS" or bwidth_units != "uS"):
			return False
		
		self.inst.write("FUNC:%s; :%s:TRAN:MODE %s; ALEV %s; BLEV %s; AWID %s %s; BWID %s %s; " % (func, func, mode, alevel, blevel, awidth, awidth_units, bwidth, bwidth_units))
		self.inst.query("*OPC?")
		self.set_transient(True)
		return True

	#setup a list of current sink values for specific time intervals
	#count specifies the number of times to iterate through the list
	#list_width can be 20uS to 3600s. Units are always seconds
	#start the list with a trigger command
	def list_setup(self, range = 30, count = 10, list_current = [0], list_width_S = [10]):
		if(len(list_current) != len(list_width_S)):
			return False

		self.inst.write("FUNC:MODE:LIST; :LIST:RANG %s; COUN %s; STEP %s" % (range, count, len(list_current)))
		self.inst.query("*OPC?")
		
		for step in range(1,len(list_current)+1):
			self.list_set_step(step, list_current[step-1], list_width_S[step-1])
		#save list to memory location 2
		self.inst.write("LIST:SAV 2; :TRIG:SOUR BUS")
	
	def list_set_step(self, step, current, time_S, slew = "MAX"):
		self.inst.write("LIST:LEV %s,%s; SLEW %s,%s; WID %s,%s" %(step, current, step, slew, step, time_S))
		self.inst.query("*OPC?")
	
	#Change output state of e-Load
	def toggle_eload(self, state):
		if state:
			self.inst.write("INPut ON")
		else:
			self.inst.write("INPut OFF")
	
	#Send a trigger signal
	def trigger(self):
		self.inst.write("TRIG:IMMediate")
	
	#setup timer-based recurring trigger, 10ms to 1000s
	#use reset() to stop the timer defined triggering
	def trigger_timer(self, interval_s):
		if(interval_s < 0.01):
			interval_s = 0.01
		elif (interval_s > 999.99):
			interval_s = 999.99
		self.inst.write("TRIG:TIM %s; SOURce TIMer" % interval_s)
	
	#Turn transients behaviour on or off
	def set_transient(self,state):
		if state:
			self.inst.write("TRANsient ON")
		else:
			self.inst.write("TRANsient OFF")
	
	#Use the remote sense connections to eliminate the effects of voltage drop on the wires
	def set_remote_sense(self, state):
		if state:
			self.inst.write("REMote:SENSe ON")
		else:
			self.inst.write("REMote:SENSe OFF")

	#Immediately acquire and return a new measurement
	def measure_voltage(self):
		return float(self.inst.query("MEAS:VOLT:DC?"))

	def measure_current(self):
		return float(self.inst.query("MEAS:CURR:DC?"))

###################################### DMM #################################
class DMM_34410A:
	def __init__(self, resource_id = 'USB0::2391::1543::MY47018348::0::INSTR'):
		rm = visa.ResourceManager()
		self.inst = rm.open_resource(resource_id)
		print("Connected to %s\n" % self.inst.query("*IDN?"))
		self.inst.write("*RST")

	def measure_voltage(self):
		return float(self.inst.query("MEASure:VOLTage?"))

	def measure_current(self):
		return float(self.inst.query("MEASure:CURRent?"))
		
	#This will perform a certain number of measurements (count) at defined intervals.
	#Measurements are stored to the internal memory (RDG_STORE). Data can be fetched with get_data()
	def measure_timed_interval_setup(self, interval_S = 1, count = 10, range = 10):
		self.reset()
		self.inst.write("SAMPle:COUNt %s; SOURce TIMer; TIMer %s" % (count, interval_S))
		#set to wait for trigger mode
		self.inst.write("CONF:VOLT:DC %s; :INIT" % range)
		
	def get_data(self):
		num_points = int(self.inst.query("DATA:POINts? RDG_STORE"))
		#this will either return a long string, or an array, not sure which yet
		return self.inst.query("DATA:REMove? %s" % num_points)
		
	def trigger(self):
		self.inst.write("*TRG")
		
	#this clears memory as well
	def reset(self):
		self.inst.write("*RST")

################################### BENCH PSU ################################
class E3631A:
	def __init__(self, resource_id = 'ASRL6::INSTR'):
		rm = visa.ResourceManager()
		self.inst = rm.open_resource(resource_id, query_delay=0.5)
		self.inst.baud_rate = 9600
		print("Connected to %s\n" % self.inst.query("*IDN?"))
		self.inst.write("SYSTem:REMote")
		time.sleep(0.1)
		self.inst.write("*RST")

	#the delays (time.sleep) are in here because the power supply would behave strangely without them.
	def measure_voltage(self, output="P25V"):
		time.sleep(0.75)
		self.inst.write(":MEASure:VOLTage:DC? %s" % output)
		time.sleep(0.3)
		self.inst.write("*OPC")
		return float(self.inst.read())

	def measure_current(self, output="P25V"):
		time.sleep(0.75)
		self.inst.write(":MEASure:CURRent:DC? %s" % output)
		time.sleep(0.3)
		self.inst.write("*OPC")
		return float(self.inst.read())
		#return self.inst.query(":MEASure:VOLTage:DC? P25V")

	def set_output(self, output = "P25V", voltage = 0, current = 0):
		query = "APPL %s, %s, %s" % (output, voltage, current)
		self.inst.write(("APPL %s, %s, %s") % (output, voltage, current))

	def output_on(self):
		self.inst.write("OUTP ON")

	def output_off(self):
		self.inst.write("OUTP OFF")

	def close(self):
		self.inst.write("SYSTem:LOCal")


################################### 150V 22A PSU ##############################
class N8740A:
	def __init__(self, resource_id = ''):
		rm = visa.ResourceManager()
		self.inst = rm.open_resource(resource_id)
		print("Connected to %s\n" % self.inst.query("*IDN?"))
		self.inst.write("*RST")

	def measure_voltage(self):
		return float(self.inst.query(""))

	def measure_current(self):
		return float(self.inst.query("MEASure:CURRent:DC?"))

	def set_output(self, voltage = 0, current = 0):
		if (voltage > 150) or (voltage < 0):
			print("Voltage Set Point Out of Range\n")
			return False	

		# set current limitß
		self.inst.write("SOURce:CURRent:IMM %s" % (current))
		#self.inst.write("SOURce:CURRent:TRIG %s" % (current))

		# set current protection
		self.inst.write("SOURce:CURRent:PROT:STATe ON")
		state = str(self.inst.query("SOURce:CURRent:PROT:STATe?"))
		if state == 'ON':
			# set voltage level
			self.inst.write("SOURce:VOLTage:IMM %s" % (voltage))
			voltage_level = self.inst.query("SOURce:VOLTage:IMM?")
			#self.inst.write("SOURce:VOLTage:TRIG %s" % (voltage))
			#self.inst.write("SOURce:VOLTage:TRIG?")

if __name__ == "__main__":
	psu = E3631A()
	psu.set_output(output="P6V", voltage=1, current=0.1)
	psu.set_output(output="P25V", voltage = 12, current=0.1)
	psu.output_on()
	#print psu.measure_voltage()
	#print psu.measure_current()
	#psu.close()
	#print psu.measure_voltage()
	#eload = BK8600()
	#eload.set_current(0.1)
	#eload.toggle_eload(True)
	#print eload.measure_voltage()
	#print eload.measure_current()

	#dmm = DMM_34410A()
	#print dmm.measure_voltage()
