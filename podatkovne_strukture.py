# definicije objektov polje (tipa garaza, pot, skladisce, trg, ovira), robot in stanje
# razred Polje ima tip in atribute, ki povedo, nekaj lastnosti o polju odvisno od tipa
class Polje:
    def __init__(self, tip, atributi):
        self.tip = tip
        self.atributi = atributi
		# polja tipa garaza in pot imajo le to lastnost, da lahko vsebujejo nekega robota ali pa ne,
		# garaza je posebna le v tem, da morajo biti na koncu vsi robotki v garazi,
		# polja tipa trg vsebujejo slovar s povprasevanjem (blago in kolicina),
		# polja tipa skladisce vsebujejo slovar s ponudbo (blago in kolicina),
		# polja tipa ovira ne dovoljujejo premika robota na to polje
        if (tip in "garaza" or tip in 'pot') and type(atributi) is not Robot:
            raise Exception("{} ne vsebuje atributa tipa robot.".format(tip))
        elif (tip = "trg" or tip in 'skladisce') and len(atributi) != 2 and (type(atributi) is not dict):
            raise Exception("{} ne vsebuje atributa tipa dict.".format(tip))
		elif tip not in ['garaza', 'pot', 'skladisce', 'trg', 'ovira']:
			raise Exception("Polja tipa {} ne obstajajo.".format(tip))
    '''
	mozna definicija funkcije dostavi, ce dovolimo, da robotu ostane nekaj blaga:
    def dostavi(self, blago_1):
        vrni = self.atributi[blago_1[0]] - blago_1[1]
        self.atributi[blago_1[0]] = max([vrni, 0])
        return ('' if max(-vrni, 0) == 0 else blago_1[0], max(-vrni, 0)) '''
	
	# dostavi blago na trg, kolikor ima robot blaga prevec, zavrzi
    def dostavi(self, blago_1):
        if tip != "trg":
            raise Exception("Blaga ni mogoce dostaviti na polje, ki ni trg.")
        vrni = self.atributi[blago_1[0]] - blago_1[1]
        self.atributi[blago_1[0]] = max([vrni, 0])
        return ('', 0)
    
	# prevzemi neko kolicino blaga iz skladisca
    def prevzemi(self, blago, kolicina):
        if tip != "skladisce":
            raise Exception("Prevzeti zelis s polja, ki ni skladisce.")
        kolicina = min([self.atributi[blago], kolicina])
        self.atributi[blago] -= kolicina
        return (blago, kolicina)

# razred robot vsebuje lastnosti o najvecji kolicini blaga (prostor),
# vsebovanem blagu (tip blaga, kolicina) in polozaju na plosci (i, j)
class Robot:
    def __init__(self, prostor, blago, polozaj):
        self.prostor = prostor
        self.blago = blago
        self.polozaj = polozaj
        if  (type(prostor) is not int) or (type(blago[0]) is not str or type(blago[1]) is not int) 
        or (type(polozaj[0]) is not int or type(polozaj[1]) is not int):
            raise Exception("Blago ne vsebuje atributa tipa (str, int).")			
	
	# odlozi vsebovano blago na trgu
    def odlozi(self, trg_1):
        self.blago = trg_1.dostavi(self.blago)
	
	# nalozi neko kolicino blaga iz skladisca
    def nalozi(self, skladisce_1, blago, kolicina):
        self.blago = skladisce_1.prevzemi(blago, min([kolicina, self.prostor]))

# stanje vsebuje tabelo polj in seznam robotov
class Stanje:
	# definicija zacetnega stanja
	# na poljih se ne rabimo podatka o zasedenosti z roboti
	def __init__(self, polja, roboti):
        self.polja = polja
		self.roboti = roboti
		for robot in roboti:
			if self.polja[robot.polozaj[0],robot.polozaj[1]].tip is in ['garaza', 'pot']:
				self.polja[robot.polozaj[0],robot.polozaj[1]].atributi = robot
			else:
				print('Robot {} ne more biti postavljen na izbrano polje'.format(robot))
	
	# TODO:
	# preveri, ce je konec (vsi trgi brez povprasevanj in roboti v garazah)
	# dovoljene poteze (vsi mozni premiki robotov z upostevanjem razlicnih moznih nalaganj)

# TODO:
# uvoz stanja iz tekstovne datoteke oblike:
# 
# tip atributi,tip atributi,tip atributi, ... ,tip atributi
# tip atributi,tip atributi,tip atributi, ... ,tip atributi
# tip atributi,tip atributi,tip atributi, ... ,tip atributi
#
# prostor, blago, kolicina, i, j
# prostor, blago, kolicina, i, j
# prostor, blago, kolicina, i, j
#
# kjer je tip dejanski tip, atributi pa so s presledki locene vrednosti blago.kolicina, kjer je to potrebno

# npr.:
# garaza, pot, skladisce moka.3 jajca.5
# garaza, pot, pot
# trg moka.2 jajca.3 mleko.4, pot, skladisce mleko.6
#
# 3, , , 0, 0
# 3, , , 1, 0
