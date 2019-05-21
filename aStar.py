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
					povprasevanje[blago] = povprasevanje.get(blago, []) + [(i,j,kolicina)]
			elif stanje.polja[i][j].tip == 'skladisce':
				for blago, kolicina in stanje.polja[i][j].atributi.items():
					ponudba[blago] = ponudba.get(blago, []) + [(i,j,kolicina)]
			elif type(stanje.polja[i][j].atributi) is ps.Robot:
				atr = stanje.polja[i][j].atributi
				if len(atr.blago[0]) > 0:
					ponudba[atr.blago[0]] = ponudba.get(atr.blago[0], []) + [(i,j,atr.blago[1])]
	for key, value in povprasevanje.items():
		for i, j, kolicina in value:
			pon = sorted([(abs(x[0]-i)+abs(x[1]-j), x[2]) for x in ponudba.get(key,[])])
			for p in pon:
				if p[1] < kolicina:
					kolicina -= p[1]
					d += (p[1] // nosilnost) * p[0]
					d += p[0] if p[1] % nosilnost > 0 else 0
				else:
					d += (kolicina // nosilnost) * p[0]
					d +=  p[0] if kolicina % nosilnost > 0 else 0
					break
	return d
 
# algoritem A*
def aStar(stanje):
	kandidati = []
	#začetne poteze
	for poteza in stanje.dovoljene_poteze():
		stanje.izvedi_potezo(poteza)
		# hevristika
		f = minimal(stanje)
		# dodamo v kandidati
		heappush(kandidati, Node([poteza], copy.deepcopy(stanje), f))
		stanje = stanje.prejsno_stanje
		
	while kandidati:
		# vozlišče z najmanjšo vrednostjo
		trenutno = heappop(kandidati)
		for poteza in trenutno.stanje.dovoljene_poteze():
			trenutno.stanje.izvedi_potezo(poteza)
			#v primeru, da je to zadnja poteza
			if trenutno.stanje.ali_je_konec():
				return trenutno.poteze + [poteza]
			else:
				# hevristika
				f = len(trenutno.poteze) + minimal(trenutno.stanje)
				heappush(kandidati, Node(trenutno.poteze + [poteza], copy.deepcopy(trenutno.stanje), f))
				trenutno.stanje = trenutno.stanje.prejsno_stanje
   
def test(filename):
	t = time.time()
	stanje = ps.Stanje()
	stanje.uvozi_stanje(filename)
	sol = aStar(stanje)
	print()
	for poteza in sol:
		print(poteza)
	print()
	print(time.time()-t)

filename = "testni_primeri/test-3x3-palacinke.txt"
filename = "testni_primeri/test-4x4-palacinkaVelikanka.txt"
# filename = "testni_primeri/test-4x4-sadnaKupa.txt"
# filename = "testni_primeri/test-5x7-postar.txt"
test(filename)
