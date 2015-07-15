# -*- coding: utf-8 -*-
import abc
from mursqlite import *
from muroutput import *


def interaction_by_strftime(format, title, filename):
	return(
		[
			"SELECT count (*) as nb,  strftime('{0}', Messages.timestamp, 'unixepoch') as time FROM Messages GROUP BY time".format(format),
			export_stackedBars,
			lambda sqlResult: (	
				[
					[ [row[0] for row in sqlResult], [] ],
					[row[1] for row in sqlResult],
					["Nb messages"]
				] ),
			title,
			filename
		]
	)


def interaction_by_contact_by_time(username, format, suffix):

	return([
		"SELECT received.nb as received, sent.nb as sent, received.identity as identity, received.date FROM \
		( SELECT count (*) as nb, Conversations.identity as identity, strftime('{0}', Messages.timestamp, 'unixepoch') as date FROM Conversations, Messages \
		WHERE  \
		Conversations.id = Messages.convo_id AND \
		Conversations.type = 1 AND \
		Conversations.identity == Messages.author AND \
		Conversations.identity == '{1}' \
		GROUP BY date ) as received, \
		( SELECT count (*) as nb, Conversations.identity as identity, strftime('{0}', Messages.timestamp, 'unixepoch') as date FROM Conversations, Messages \
		WHERE  \
		Conversations.id = Messages.convo_id AND \
		Conversations.type = 1 AND \
		Conversations.identity != Messages.author AND \
		Conversations.identity == '{1}' \
		GROUP BY date ) as sent \
		WHERE received.identity = sent.identity AND \
		received.date = sent.date \
		ORDER BY received.date ".format(format, username),
		export_lines,
		lambda sqlResult : (
			[
				[ [row[1] for row in sqlResult], [row[0] for row in sqlResult] ],
				[row[3] for row in sqlResult],
				["Sent", "Received"]
			]
		), 
		"Activity with {0} / {1}".format(username, suffix),
		'activity/contact/{1}/{0}'.format(username, suffix)
	])


interactions_by_contact = [
	"SELECT received.nb as received, sent.nb as sent, received.identity as identity FROM \
	( SELECT count (*) as nb, Conversations.identity as identity FROM Conversations, Messages \
	WHERE  \
	Conversations.id = Messages.convo_id AND \
	Conversations.type = 1 AND \
	Conversations.identity == Messages.author \
	GROUP BY Conversations.identity ) as received, \
	( SELECT count (*) as nb, Conversations.identity as identity FROM Conversations, Messages \
	WHERE  \
	Conversations.id = Messages.convo_id AND \
	Conversations.type = 1 AND \
	Conversations.identity != Messages.author \
	GROUP BY Conversations.identity ) as sent \
	WHERE received.identity = sent.identity \
	ORDER BY received.nb+sent.nb ",
	export_stackedBars,
	lambda sqlResult : (
		[
			[ [row[1] for row in sqlResult], [row[0] for row in sqlResult] ],
			[row[2] for row in sqlResult],
			["Sent", "Received"]
		]
	), 
	"Activity by contact",
	'activity/bycontact'
]


rx_tx_by_contact_top_20 = [
	"SELECT received.nb as received, sent.nb as sent, received.identity as identity FROM \
	( SELECT count (*) as nb, Conversations.identity as identity FROM Conversations, Messages \
	WHERE  \
	Conversations.id = Messages.convo_id AND \
	Conversations.type = 1 AND \
	Conversations.identity == Messages.author \
	GROUP BY Conversations.identity ) as received, \
	( SELECT count (*) as nb, Conversations.identity as identity FROM Conversations, Messages \
	WHERE  \
	Conversations.id = Messages.convo_id AND \
	Conversations.type = 1 AND \
	Conversations.identity != Messages.author \
	GROUP BY Conversations.identity ) as sent \
	WHERE received.identity = sent.identity \
	ORDER BY received.nb+sent.nb DESC LIMIT 20",
	export_stackedBars,
	lambda sqlResult : (
		[
			[ [row[1] for row in sqlResult], [row[0] for row in sqlResult] ],
			[row[2] for row in sqlResult],
			["Sent", "Received"]
		]
	), 
	"Activity by contact",
	'activity/bycontact_top20'
]


contacts_identity = [
	"SELECT Skypename, fullname, displayname, birthday, gender, country, province, city, emails, homepage  from Contacts",
	export_html,
	lambda sqlResult : (
			("Contacts"),
			(("Skypename"), ("fullname"), ("displayname"), ("birthday"),("gender"),("country"), ("province"), ("city"), ("emails"), ("homepage")),
			sqlResult
		),
	"Contacts identity",
	'contacts/identies'
	]


contacts_phones = [
	"SELECT Skypename, phone_home, phone_office, phone_mobile from Contacts",
	export_html,
	lambda sqlResult : (
			("Contacts phones"),
			(("Skypename"), ("home"), ("office"), ("mobile")),
			[ row for row in sqlResult if row[1] or row[2] or row[3] is not None ]
		),
	"Contacts phones",
	'contacts/phones'
	]


contacts_country = [
	"SELECT country, count(*) as nb from Contacts where country != '' group by country ",
	export_map,
	lambda sqlResult : [("Nb. contacts", dict(sqlResult)),],
	"Contact by country",
	'contacts/worldmap'
]




#  function to transform several matrices as:
#
#     a1-1 b1-1 c1-1 d1   a2-1 b2-1 c2-1 d2          aN-1 bN-1 cN-1 dN 
#     a1-2 b1-2 c1-2 d1   a2-2 b2-2 c2-2 d2          aN-2 bN-2 cN-2 dN
#       .    .    .   .   .    .    .   .            
#       .    .    .   .   .    .    .   .            
#     a1-x b1-x c1-x d1   a2-x b2-x c2-x d2  . . . . aN-x bN-x cN-x dN
#       .    .    .   .   .    .    .   .            
#       .    .    .   .   .    .    .   .            
#     a1-n b1-n c1-n d1   a2-n b2-n c2-n d2          aN-n bN-n cN-n dN
#     
#     INTO only one matrix :
#     
#              a1            a2                   a4
#     d1  (b1-1, c1-1)  (b1-2, c1-2) .  .  . (b1-n, c1-n)
#     d2  (b2-1, c2-1)  (b2-2, c2-2) .  .  . (b2-n, b2-n)
#     .
#     .
#     .
#     dx  (bn-1, cn-1)  (bn-2, cn-2) .  .  . (bn-n, cn-n)
#     .
#     .
#     dN  (bN-1, cN-1)  (bN-2, cN-2) .  .  . (bN-n, cN-n)
#     
#     with : a=date, b=sent, c=received, d = identity
#     
#     Note that the 'n' will probably not be the same among all the input matrices.
#     In the output matrix, all the possible 'a' will be represented.
#     If an input matrix has not a specific line with  (0,0) will be put instead of 'None'
def matrices_to_matrix(*matrices):
	
	matrices = [i for i in matrices if i]

	A = []
	for mat in matrices:
		A = A+ [r[3] for r in mat]
	A = sorted(set(A))

	R = list()
	
	D = [mat[0][2] for mat in matrices if (len(mat) > 0 and len(mat[0]) > 2) ]

	for mat in matrices:
		mat_s = sorted(mat, key=lambda m: m[3] )
		values = [row[3] for row in mat_s]
		if len(values) == len(A):
			R.append(values)
		else:
			r = [[0,0]]*len(A)

			j=0
			for i in range(len(A)):
				
				
				if mat[j][3] == A[i]:
					r[i] = (mat[j][0], mat[j][1])
					j = j+1

					if j>=len(mat):
						break
			R.append(r)

	return (A, D, R)