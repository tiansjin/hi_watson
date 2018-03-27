discardPile=[]
totalCards=[]
##makes sure your input is a card on the board
cityChecker=['LAGOS', 'SYDNEY', 'TAIWAN', 'SAN FRANCISCO', 'LOS ANGELES', 'ESSEN']
newCity=[]

def deck(newCity):
	epidemicCount=0
	newCity=raw_input('New Infection Card: ').upper()
	if newCity=='EPIDEMIC':
		epidemicCount+=1
		print ('THERE HAS BEEN '+ str(epidemicCount)+' EPIDEMIC(S)')
		draws=0
		while draws!=len(discardPile) and len(totalCards)!=0:
			newCity=raw_input('New Infection Card: ').upper()
			if newCity in discardPile:
				discardPile.remove(newCity)
				totalCards.remove(newCity)
				my_dict={i:totalCards.count(i) for i in totalCards}
				print my_dict
			elif newCity=='EPIDEMIC':
				epidemicCount+=2
				print ('THERE HAS BEEN '+ str(epidemicCount)+' EPIDEMIC(S)')
				draws=0
				while draws!=len(discardPile) and len(totalCards)!=0:
					newCity=raw_input('New Infection Card: ').upper()
					if newCity in discardPile:
						discardPile.remove(newCity)
						totalCards.remove(newCity)
						my_dict={i:totalCards.count(i) for i in totalCards}
						print my_dict
			elif newCity not in cityChecker or newCity not in discardPile:
				print 'Invalid City'
		return epidemicCount
	elif newCity not in cityChecker:
		print 'Invalid City'
	else:
		discardPile.append(newCity)
		totalCards.append(newCity)
		print totalCards


while len(totalCards)<49:
	deck(newCity)




		
