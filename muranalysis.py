# -*- coding: utf-8 -*-
from mursqlite import *
from murelements import *
import numpy

class Muranalyzer:
	def __init__(self, mursqlite):
		self.mursqlite = mursqlite
		self.owner = self.get_owner()
		self.topContacts = list()


	def analyze(self, sqlQuery, graphicalOutput, dataAdapter, title, filename):
		sqlResult = self.mursqlite.query(sqlQuery)
		graphicalOutput(dataAdapter(sqlResult), title, self.owner+"/"+filename)
		return(sqlResult)

	def get_activated_contacts(self):
		return(self.mursqlite.query("SELECT DISTINCT author from Messages"))

	def get_owner(self):
		return(self.mursqlite.query("SELECT skypename from Accounts LIMIT 1")[0][0])

	def get_top_contacts(self, nbContacts):
		return(
			[
				row[0] for row in 
				self.mursqlite.query("SELECT author, count(*) as nb from Messages where author != '{0}' AND author != '' GROUP BY author HAVING nb > 10 ORDER BY nb DESC LIMIT {1}".format(self.owner, nbContacts))
			]
		)

	def an_contact_detailed(self, contact):
		timespans = (
			('%H', 'hour'),
			('%Y%m%d', 'day'),
			('%w', 'weekDay'), #0=sunday (see sqlite doc)
			('%d', 'monthday'),
			('%Y%W', 'week'),
			('%Y%m', 'month')
		)
		for timespan in timespans:
			r = self.analyze(*interaction_by_contact_by_time(contact, *timespan))
			if timespan[1] == 'month':
				self.topContacts.append(r)


	def an_activity_by(self):
		values=(
			(interaction_by_strftime('%w', "Activity by weekDay (0=sunday)", 'activity/weekday'), 'weekday'),
			(interaction_by_strftime('%Y%m%d', "Activity by day", 'activity/day'), 'day'),
			(interaction_by_strftime('%Y%W', "Activity by week (YYYww)", 'activity/week'), 'week'),
			(interaction_by_strftime('%Y%m', "Activity by month", 'activity/month'), 'month'),
			(interaction_by_strftime('%d', "Activity by month day", 'activity/monthday'),'monthday'),
			(interaction_by_strftime('%H', "Activity by hour", 'activity/hour'),'hour')
		)

		print("Activity by:")
		for val in values:
			print("- {0}".format(val[1]))
			self.analyze(*val[0])
		
	def an_detail_top(self, nbContacts):
		print("Detailed analysis for TOP{0} contacts".format(nbContacts))
		i=1
		for contact in self.get_top_contacts(nbContacts):
			if contact:
				print("{0} - {1}".format(i, contact))
				i+=1
				self.an_contact_detailed(contact)

	def an_interactions_contact(self):
		print("Activity by contact")
		self.analyze(*interactions_by_contact)

	def an_rx_tx_contact_top(self, nbContacts):
		print("Activity by contact")
		self.analyze(*rx_tx_by_contact_top(nbContacts))

	def an_matrix(self):
		if self.topContacts is None:
			print("Must exec an_detail_top before")
			return 
		return(matrices_to_matrix(*self.topContacts))	


	def an_rx_tx_top(self):
		matrix = self.an_matrix()
		if(len(self.topContacts) ==0):
			print ("You should have run a top analysis before doing rx_tx analysis!")
			return()
		
		tags = list()
		for d in matrix[1]:
			tags.append(d+' rx')
			tags.append(d+' tx')

		vals = list()
		for m in matrix[2]:
			vals.append([r[0] for r in m])
			vals.append([r[1] for r in m])

		for nb in range(5, 25, 5): #generate 3 more graphs if possible with more contacts
			if(len(self.topContacts)>=nb):		
				export_pyramid((vals[:nb*2], matrix[0], tags[:nb*2]), "Monthly Rx/Tx by top{0} contact".format(nb), self.owner+'/rxtx/{0}'.format(nb))

		return()

	def an_correlations(self): # very experimental
		R = self.an_matrix()
		coeffs = list()

		for r in R[2]: #sum rx and tx
			coeffs.append([int(c[0]+c[1]) for c in r])

		diff = list()
		for i in range(len(coeffs)):
			r = list()
			if(len(coeffs)>3): #rick to avoid substraction with nothing. ANyway, this whole thing absolute nonsense without some volume (more than 3...)
				for j in range(len(coeffs[i])-1):
					r.append(coeffs[i][j+1] - coeffs[i][j])
				diff.append(r)

		corrs = list()
		corrs.append ((numpy.corrcoef(coeffs), "Correlation with nb messages.\n Meaning there is a proportional relationship between the exchanged volumes."))
		corrs.append ((numpy.corrcoef(diff), "Correlation with the difference of messagse. \n Meaning there is a proportional relashioship with the increase/decrease of exchanged volumes."))

		print("Correlations (very experimental):")
		for corr in corrs:
			print(corr[1])
			r = len(corr[0])
			viewed = list()
			for i in range(r):
				for j in range(r-i): #because it is a squarred symetric matrix
					if corr[0][i][j] > 0.5 and i != j and not "{0}-{1}".format(i,j) in viewed:
						print(R[1][i], "\t->\t", R[1][j], "\t", corr[0][i][j] )
						viewed.append("{1}-{0}".format(i,j))


	def an_contacts(self):
		self.analyze(*contacts_country)
		self.analyze(*contacts_identity)
		self.analyze(*contacts_phones)