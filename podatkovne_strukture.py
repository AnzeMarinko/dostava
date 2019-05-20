# definicije objektov polje (tipa garaza, pot, skladisce, trg, ovira), robot in stanje
from random import randint
from copy import deepcopy



# =============================================:
# TODO:

# razred Polje ima tip in atribute, ki povedo, nekaj lastnosti o polju odvisno od tipa
class Polje:
	def __init__(self, tip, atributi=None):
		self.tip = tip
		self.atributi = atributi
		# polja tipa garaza in pot imajo le to lastnost, da lahko vsebujejo nekega robota ali pa ne,
		# garaza je posebna le v tem, da morajo biti na koncu vsi robotki v garazi,
		# polja tipa trg vsebujejo slovar s povprasevanjem (blago in kolicina),
		# polja tipa skladisce vsebujejo slovar s ponudbo (blago in kolicina),
		# polja tipa ovira ne dovoljujejo premika robota na to polje
		if (tip in "garaza" or tip in 'pot') and atributi and type(atributi) is not Robot:
			raise Exception("{} ne vsebuje atributa tipa robot.".format(tip))
		elif (tip in "trg" or tip in 'skladisce') and (type(atributi) is not dict):
			raise Exception("{} ne vsebuje atributa tipa dict.".format(tip))
		elif tip not in ['garaza', 'pot', 'skladisce', 'trg', 'ovira']:
			raise Exception("Polja tipa {} ne obstajajo.".format(tip))
	
	# objekt pretvori v niz
	def __repr__(self):
		if self.tip in "garaza":
			return "Garaza ({})".format(self.atributi)
		elif self.tip in "pot":
			return "Pot ({})".format(self.atributi)
		elif self.tip in "trg":
			return "Trg {}".format(self.atributi)
		elif self.tip in "skladisce":
			return "Skladisce {}".format(self.atributi)
		elif self.tip in "ovira":
			return "Ovira"
	'''
	mozna definicija funkcije dostavi, ce dovolimo, da robotu ostane nekaj blaga:
	def dostavi(self, blago_1):
		vrni = self.atributi[blago_1[0]] - blago_1[1]
		self.atributi[blago_1[0]] = max([vrni, 0])
		return ('' if max(-vrni, 0) == 0 else blago_1[0], max(-vrni, 0)) '''
	
	# dostavi blago na trg, kolikor ima robot blaga prevec, zavrzi
	def dostavi(self, blago_1):
		if self.tip != "trg" or len(blago_1[0]) == 0:
			raise Exception("Blaga ni mogoce dostaviti (polje ni trg ali robot nima blaga).")
		vrni = self.atributi[blago_1[0]] - blago_1[1]
		self.atributi[blago_1[0]] = max([vrni, 0])
		return ('', 0)

	# prevzemi neko kolicino blaga iz skladisca
	def prevzemi(self, blago, kolicina):
		if self.tip != "skladisce":
			raise Exception("Prevzeti zelis s polja, ki ni skladisce.")
		kolicina = min([self.atributi[blago], kolicina])
		self.atributi[blago] -= kolicina
		return (blago, kolicina)

# razred robot vsebuje lastnosti o najvecji kolicini blaga (prostor),
# vsebovanem blagu (tip blaga, kolicina) in polozaju na plosci (i, j)
class Robot:
	def __init__(self, prostor, polozaj, blago):
		self.prostor = prostor
		self.polozaj = polozaj
		self.blago = blago
		if  (type(prostor) is not int) or (type(blago[0]) is not str or type(blago[1]) is not int) or (type(polozaj[0]) is not int or type(polozaj[1]) is not int):
			raise Exception("Blago ne vsebuje atributa tipa (str, int).")			

	def __repr__(self):
		return "Robot ({} <= {}, {})".format(self.blago, self.prostor, self.polozaj)

	# odlozi vsebovano blago na trgu
	def odlozi(self, trg_1):
		self.blago = trg_1.dostavi(self.blago)

	# nalozi neko kolicino blaga iz skladisca
	def nalozi(self, skladisce_1, blago, kolicina):
		self.blago = skladisce_1.prevzemi(blago, min([kolicina, self.prostor]))
	
	# premakne robota in vrne (star polozaj, nov polozaj)
	def premakni(self, dx, dy):
		stari = self.polozaj
		self.polozaj = (self.polozaj[0]+dx,self.polozaj[1]+dy)
		return stari, self.polozaj

# stanje vsebuje tabelo polj in seznam robotov
class Stanje:
	# definicija zacetnega stanja
	# na poljih se ne rabimo podatka o zasedenosti z roboti
	def __init__(self, polja=[[]], roboti=[], prejsno_stanje = None):
		self.polja = polja
		self.n = len(polja)
		self.m = len(polja[0])
		self.roboti = roboti
		self.prejsno_stanje = prejsno_stanje
		# na polja postavi robote
		for robot in roboti:
			if self.polja[robot.polozaj[1]][robot.polozaj[0]].tip in ['garaza', 'pot']:
				self.polja[robot.polozaj[1]][robot.polozaj[0]].atributi = robot
			else:
				print('Robot {} ne more biti postavljen na izbrano polje'.format(robot))

	def __repr__(self):
		opis = "Stanje:    " + str(self.roboti) + "\n"
		for vrstica in self.polja:
			opis += str(vrstica) + "\n"
		return opis
	
	def pretvori_v_niz(self):
		opis = "Stanje:    " + str(self.roboti) + "\n"
		for vrstica in self.polja:
			opis += str(vrstica) + "\n"
		return opis
	
	# robota iz seznama self.roboti z indeksom irobot premakni za dx desno in dy dol
	def premakni(self, irobot, dx, dy):
		# preveri ce ta robot obstaja
		if irobot < 0 or irobot >= len(self.roboti):
			print("Nepravilen indeks robota.")
			return None
		(x,y)=self.roboti[irobot].polozaj
		# premik mora biti dovoljen (dolzine 1, na polje garaza ali pot, znotraj plosce)
		if dx + x < 0 or dx + x >= self.m or dy + y < 0 or dy + y >= self.n or self.polja[dy+y][dx+x].tip not in ['garaza','pot'] or abs(dx)+abs(dy)!=1:
			print("Nepravilen premik.")
			return None
		# Shrani prejšno stanje in izvede premik:
		prejsno_st = deepcopy(self)
		premik = self.roboti[irobot].premakni(dx,dy)
		self.prejsno_stanje = prejsno_st
		# poleg spremembe polozaja robota popravi tudi lastnosti polj
		self.polja[premik[0][1]][premik[0][0]].atributi = None
		self.polja[premik[1][1]][premik[1][0]].atributi = self.roboti[irobot]
	
	# robotu iz seznama self.roboti z indeksom irobot nalozi podano kolicino blaga iz skladisca dx desno in dy dol od robota
	def nalaganje(self, irobot, dx, dy, blago, kolicina):
		# preveri ce robot obstaja
		if irobot < 0 or irobot >= len(self.roboti):
			print("Nepravilen indeks robota.")
			return None
		(x,y)=self.roboti[irobot].polozaj
		# nalaganje mora biti dovoljeno (na razdalji 1, na polje skladisce, znotraj plosce)
		if dx + x < 0 or dx + x >= self.m or dy + y < 0 or dy + y >= self.n or self.polja[dy+y][dx+x].tip != 'skladisce' or abs(dx)+abs(dy)!=1:
			print("Nepravilno skladisce.")
			return None
		# ali je to blago sploh v skladiscu
		if self.polja[dy+y][dx+x].atributi.get(blago,0) <= 0:
			print("Nedosegljivo blago.")
			return None
		# Shrani prejšno stanje in izvede nalaganje:
		prejsno_st = prejsno_st = deepcopy(self)
		self.roboti[irobot].nalozi(self.polja[y+dy][x+dx], blago, kolicina)
		self.prejsno_stanje = prejsno_st
	
	# robot iz seznama self.roboti z indeksom irobot odlozi blago na trg dx desno in dy dol od robota
	def odlaganje(self, irobot, dx, dy):
		# preveri ce robot obstaja
		if irobot < 0 or irobot >= len(self.roboti):
			print("Nepravilen indeks robota.")
			return None
		(x,y)=self.roboti[irobot].polozaj
		# nalaganje mora biti dovoljeno (na razdalji 1, na polje skladisce, znotraj plosce)
		if dx + x < 0 or dx + x >= self.m or dy + y < 0 or dy + y >= self.n or self.polja[dy+y][dx+x].tip != 'trg' or abs(dx)+abs(dy)!=1:
			print("Nepravilen trg.")
			return None
		# Shrani prejšno stanje in izvede odlaganje:
		prejsno_st = prejsno_st = deepcopy(self)
		self.roboti[irobot].odlozi(self.polja[y+dy][x+dx])
		self.prejsno_stanje = prejsno_st
	
	# uvoz stanja iz datoteke (za obliko datoteke glej spodaj)
	def uvozi_stanje(self, filename):
		plosca = []
		roboti = []
		with open(filename,"r") as f:
			print(f.readline())
			f.readline()
			while True:
				polja = [polje.split(" ") for polje in f.readline()[:-1].split(",")]
				if len(polja[0][0]) == 0:
					break
				vrstica = []
				for polje in polja:
					if len(polje) == 1:
						vrstica.append(Polje(polje[0]))
					else:
						vrstica.append(Polje(polje[0],{blago:int(kolicina) for blago,kolicina in [x.split(".") for x in polje[1:]]}))
				plosca.append(vrstica)
			while True:
				robot = f.readline()[:-1].split(",")
				if len(robot[0]) == 0:
					break
				roboti.append(Robot(int(robot[0]),(int(robot[1]),int(robot[2])),(robot[3],int(robot[4]))))
		self.polja = plosca
		self.roboti = roboti
		for robot in roboti:
			if self.polja[robot.polozaj[1]][robot.polozaj[0]].tip in ['garaza', 'pot']:
				self.polja[robot.polozaj[1]][robot.polozaj[0]].atributi = robot
			else:
				print('Robot {} ne more biti postavljen na izbrano polje'.format(robot))
		self.n = len(self.polja)
		self.m = len(self.polja[0])
	
	# seznam dovoljenih potez (vsi mozni premiki robotov z upostevanjem razlicnih moznih nalaganj)
	def dovoljene_poteze(self):
		poteze = list()
		for irobot in range(0,len(self.roboti)):
			(x,y)=self.roboti[irobot].polozaj
			# PREMAKNI:
			if x+1 < self.m and self.polja[y][x+1].tip in ['garaza', 'pot'] and self.polja[y][x+1].atributi == None:
				poteze.append(('premakni',irobot, 1, 0))
			if x-1 >= 0 and  self.polja[y][x-1].tip in ['garaza', 'pot'] and self.polja[y][x-1].atributi == None:
				poteze.append(('premakni',irobot, -1, 0))
			if y+1 < self.n and self.polja[y+1][x].tip in ['garaza', 'pot'] and self.polja[y+1][x].atributi == None:
				poteze.append(('premakni',irobot, 0, 1))
			if y-1 >= 0 and self.polja[y-1][x].tip in ['garaza', 'pot'] and self.polja[y-1][x].atributi == None:
				poteze.append(('premakni',irobot, 0, -1))
			# NALAGANJE:
			if self.roboti[irobot].blago == ('',0):
				max_kol = self.roboti[irobot].prostor
				if x+1 < self.m and self.polja[y][x+1].tip == 'skladisce':
					for i in range(1,max_kol + 1):
						for blago, kolicina in self.polja[y][x+1].atributi.items():
							if i <= kolicina:
								poteze.append(('nalaganje', irobot, 1, 0, blago,i))
				if x-1 >= 0 and self.polja[y][x-1].tip == 'skladisce':
					for i in range(1,max_kol + 1):
						for blago, kolicina in self.polja[y][x-1].atributi.items():
							if i <= kolicina:
								poteze.append(('nalaganje', irobot, -1, 0, blago,i))
				if y+1 < self.n and self.polja[y+1][x].tip == 'skladisce':
					for i in range(1,max_kol + 1):
						for blago, kolicina in self.polja[y+1][x].atributi.items():
							if i <= kolicina:
								poteze.append(('nalaganje', irobot, 0, 1, blago,i))
				if y-1 >= 0 and self.polja[y-1][x].tip == 'skladisce':
					for i in range(1,max_kol + 1):
						for blago, kolicina in self.polja[y-1][x].atributi.items():
							if i <= kolicina:
								poteze.append(('nalaganje', irobot, 0, -1, blago,i))
			# ODLAGANJE:
			if self.roboti[irobot].blago != ('',0):
				if x+1 < self.m and self.polja[y][x+1].tip == 'trg':
					poteze.append(('odlaganje',irobot, 1, 0)) 
				if x-1 >= 0 and self.polja[y][x-1].tip == 'trg':
					poteze.append(('odlaganje',irobot, -1, 0)) 
				if y+1 < self.n and self.polja[y+1][x].tip == 'trg':
					poteze.append(('odlaganje',irobot, 0, 1)) 
				if y-1 >= 0 and self.polja[y-1][x].tip == 'trg':
					poteze.append(('odlaganje',irobot, 0, -1)) 
		return poteze

	# preveri, ce je konec (vsi trgi brez povprasevanj in roboti v garazah)
	def ali_je_konec(self):
		for i in range(self.n):
			for j in range(self.m):
				if self.polja[i][j].tip == 'trg':
					for blago, kolicina in self.polja[i][j].atributi.items():
						if kolicina != 0:
							#print('Trg {} potrebuje še {} enot {}.'.format(self.polja[i][j],kolicina, blago))
							return False
		for robot in self.roboti:
			(x,y)=robot.polozaj
			if self.polja[y][x].tip != 'garaza':
				#print('Robot {} ni v garaži.'.format(robot))
				return False
		print('KONEC!')
		return True

	def random_poteza(self):
		sez_potez = self.dovoljene_poteze()
		i = randint(0, len(sez_potez)-1)
		return sez_potez[i]
	
	#Izvede sprejeto potezo:
	def izvedi_potezo(self, poteza):
		if poteza[0] == 'premakni':
			self.premakni(poteza[1], poteza[2], poteza[3])
		elif poteza[0] == 'nalaganje':
			self.nalaganje(poteza[1], poteza[2], poteza[3],poteza[4], poteza[5])
		elif poteza[0] == 'odlaganje':
			self.odlaganje(poteza[1], poteza[2], poteza[3])
	
	# Prebere zaporedje potez iz datoteke:
	def preberi_zaporedje_potez(self, file_name):
		with open(file_name,"r") as f:
			poteza = f.readline()[:-1].split(",")
			if poteza[0] == 'premakni':
				self.premakni(poteza[1], poteza[2], poteza[3])
			elif poteza[0] == 'nalaganje':
				self.nalaganje(poteza[1], poteza[2], poteza[3],poteza[4], poteza[5])
			elif poteza[0] == 'odlaganje':
				self.odlaganje(poteza[1], poteza[2], poteza[3])
			#osvezi()
	
# Zapisi zaporedje potez v datoteko:
def zapisi_zaporedje_potez(file_name, sez_potez):
	f_w = open(file_name,"w")
	for poteza in sez_potez:
		vrstica = ''
		for i in poteza:
			vrstica += str(i)
		f_w.write(vrstica + '\n')
	
# stanje1 = Stanje([[Polje("garaza",None),Polje("pot",None),Polje("pot",None)],[Polje("pot",None),Polje("ovira"),Polje("pot",None)],[Polje("trg",{"moka":3,"voda":2,"jajca":4}),Polje("ovira"),Polje("skladisce",{"moka":1,"voda":1})]],[Robot(2,(0,0),("",0))])

# uvoz iz tekstovne datoteke oblike:
'''
pomenljiv naslov stanja

tip atributi,tip atributi,tip atributi, ... ,tip atributi
tip atributi,tip atributi,tip atributi, ... ,tip atributi
tip atributi,tip atributi,tip atributi, ... ,tip atributi

prostor, i, j, blago, kolicina
prostor, i, j, blago, kolicina
prostor, i, j, blago, kolicina

'''
# kjer je tip dejanski tip, atributi pa so s presledki locene vrednosti blago.kolicina, kjer je to potrebno
# npr.:
'''
majhen test

garaza, pot, skladisce moka.3 jajca.5
garaza, pot, pot
trg moka.2 jajca.3 mleko.4, pot, skladisce mleko.6

3,0,0,,0
3,1,0,,0

'''
