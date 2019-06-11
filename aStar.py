from heapq import *
import podatkovne_strukture as ps
import copy
import time
 
class Node:
	def __init__(self, poteze, stanje, hevr):
		self.poteze = poteze # poteze od zacetka igre
		self.stanje = stanje # plosca
		self.hevr = hevr # vrednost hevristicne funkcije

	# primerjanje hevristik
	def __le__(self, other):
		return self.hevr <= other.hevr
	def __lt__(self, other):
		return self.hevr < other.hevr
 
# hevristike
def minimal(stanje):
	d = 0
	nosilnost = max([robot.prostor for robot in stanje.roboti])
	povprasevanje = {}
	ponudba = {}
	for i in range(stanje.n):
		for j in range(stanje.m):
			if stanje.polja[i][j].tip == 'trg':
				for blago, kolicina in stanje.polja[i][j].atributi.items():
					if kolicina > 0:
						povprasevanje[blago] = povprasevanje.get(blago, []) + [(i,j,kolicina)]
			elif stanje.polja[i][j].tip == 'skladisce':
				for blago, kolicina in stanje.polja[i][j].atributi.items():
					if kolicina > 0:
						ponudba[blago] = ponudba.get(blago, []) + [(i,j)]
			elif type(stanje.polja[i][j].atributi) is ps.Robot:
				atr = stanje.polja[i][j].atributi
				if len(atr.blago[0]) > 0 and atr.blago[1]>0:
					ponudba[atr.blago[0]] = ponudba.get(atr.blago[0], []) + [(i,j)]
	for blago, value in povprasevanje.items():
		for i, j, kolicina in value:
			pon = min([abs(x[0]-i)+abs(x[1]-j) for x in ponudba.get(blago,[])])
			d += (kolicina // nosilnost) * pon
			d += pon if kolicina % nosilnost > 0 else 0
	return d

# algoritem A*
def astar(stanje):
	kandidati = []
	#začetne poteze
	for poteza in stanje.dovoljene_poteze():
		auxstanje = copy.deepcopy(stanje)
		stanje.izvedi_potezo(poteza)
		# hevristika
		f = minimal(stanje)+1
		# dodamo v kandidati
		heappush(kandidati, Node([poteza], copy.deepcopy(stanje), f))
		stanje = copy.deepcopy(auxstanje)
		
	while kandidati:
		# vozlišče z najmanjšo vrednostjo
		trenutno = heappop(kandidati)
		#print(trenutno.hevr)
		#print(trenutno.stanje)
		print(trenutno.hevr, len(trenutno.poteze))
		for poteza in trenutno.stanje.dovoljene_poteze():
			auxstanje = copy.deepcopy(trenutno.stanje)
			trenutno.stanje.izvedi_potezo(poteza)
			#v primeru, da je to zadnja poteza
			if trenutno.stanje.ali_je_konec():
				return trenutno.poteze + [poteza]
			else:
				# hevristika
				m = minimal(trenutno.stanje)
				f = m+len(trenutno.poteze)
				heappush(kandidati, Node(trenutno.poteze + [poteza], copy.deepcopy(trenutno.stanje), f))
				trenutno.stanje = copy.deepcopy(auxstanje)
   
def test(filename):
	t = time.time()
	stanje = ps.Stanje()
	stanje.uvozi_stanje(filename)
	sol = astar(stanje)
	print()
	for poteza in sol:
		print(poteza)
	print()
	print(time.time()-t)
	ps.zapisi_zaporedje_potez(filename[:-4]+"resitev.txt",sol)
	return sol

# filename = "testni_primeri/test-4x4-palacinkaVelikanka.txt"
# filename = "testni_primeri/test-4x4-sadnaKupa.txt"
# filename = "testni_primeri/test-5x7-postar.txt"

palacinke3x3 = test("testni_primeri/test-3x3-palacinke.txt")