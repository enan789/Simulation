__metaclass__=type
import random
import csv

#define a class called 'Customer'
class Customer:
	def __init__(self,arrival_time,service_start_time,service_time):
		self.arrival_time=arrival_time
		self.service_start_time=service_start_time
		self.service_time=service_time
		self.service_end_time=self.service_start_time+self.service_time
		self.wait=self.service_start_time-self.arrival_time

#a simple function to sample from negative exponential
def neg_exp(lambd):
	return random.expovariate(lambd)


def QSim(lambd=False,mu=False,simulation_time=False):
    """
    This is the main function to call to simulate an MM1 queue.
    """

	#If parameters are not input prompt
	if not lambd:
		lambd=input('Inter arrival rate: ')
	if not mu:
		mu=input('Service rate: ')
	if not simulation_time:
		simulation_time=input('Total simulation time: ')

	#Initialise clock
	t=0

	#Initialise empty list to hold all data
	Customers=[]

#----------------------------------
#The actual simulation happens here:
	while t<simulation_time:

		#calculate arrival date and service time for new customer
		if len(Customers)==0:
			arrival_time=neg_exp(lambd)
			service_start_time=arrival_time
		else:
			arrival_time+=neg_exp(lambd)
			service_start_time=max(arrival_time,Customers[-1].service_end_time)
		service_time=neg_exp(mu)

		#create new customer
		Customers.append(Customer(arrival_time,service_start_time,service_time))

		#increment clock till next end of service
		t=arrival_time
#----------------------------------

	#calculate summary statistics
	Waits=[a.wait for a in Customers]
	Mean_Wait=sum(Waits)/len(Waits)

	Total_Times=[a.wait+a.service_time for a in Customers]
	Mean_Time=sum(Total_Times)/len(Total_Times)

	Service_Times=[a.service_time for a in Customers]
	Mean_Service_Time=sum(Service_Times)/len(Service_Times)

	Utilisation=sum(Service_Times)/t

	#output summary statistics to screen
	print ""
	print "Summary results:"
	print ""
	print "Number of customers: ",len(Customers)
	print "Mean Service Time: ",Mean_Service_Time
	print "Mean Wait: ",Mean_Wait
	print "Mean Time in System: ",Mean_Time
	print "Utilisation: ",Utilisation
	print ""

	#prompt user to output full data set to csv
	if input("Output data to csv (True/False)? "):
		outfile=open('MM1Q-output-(%s,%s,%s).csv' %(lambd,mu,simulation_time),'wb')
		output=csv.writer(outfile)
		output.writerow(['Customer','arrival_time','Wait','service_start_time','Service_Time','service_end_time'])
		i=0
		for customer in Customers:
			i=i+1
			outrow=[]
			outrow.append(i)
			outrow.append(customer.arrival_time)
			outrow.append(customer.wait)
			outrow.append(customer.service_start_time)
			outrow.append(customer.service_time)
			outrow.append(customer.service_end_time)
			output.writerow(outrow)
		outfile.close()
	print ""
	return
