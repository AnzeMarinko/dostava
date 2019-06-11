from heapq import *
import podatkovne_strukture as ps
import copy
import time
import ql_socasni_premiki as ql


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
	st_robotov = len(stanje.roboti)
	return d/st_robotov

def q_hevristika(q, stanje):
	if stanje.pretvori_v_niz() not in q.keys():
		return 10
	else:
		akcije = q[stanje.pretvori_v_niz()]
		najboljsa_akcija = max(akcije, key=lambda k: akcije[k])
		return akcije[najboljsa_akcija]
 
# algoritem A*
def astar(stanje, hevristika, q):
	kandidati = []
	#začetne poteze
	for poteza in stanje.socasne_poteze():
		auxstanje = copy.deepcopy(stanje)
		if type(poteza[0]) == tuple:
			for pot in poteza:
				stanje.izvedi_potezo(pot)
		else:
			stanje.izvedi_potezo(poteza)
		# hevristika
		if hevristika == 'q_hevristika':
			f = -q_hevristika(q, stanje)+1
		else:
			f = minimal(stanje)+1
		# dodamo v kandidati
		heappush(kandidati, Node([poteza], copy.deepcopy(stanje), f))
		stanje = copy.deepcopy(auxstanje)
		
	while kandidati:
		# vozlišče z najmanjšo vrednostjo
		trenutno = heappop(kandidati)
		#print(trenutno.stanje)
		#input()
		for poteza in trenutno.stanje.socasne_poteze():
			auxstanje = copy.deepcopy(trenutno.stanje)
			if type(poteza[0]) == tuple:
				for pot in poteza:
					trenutno.stanje.izvedi_potezo(pot)
			else:
				trenutno.stanje.izvedi_potezo(poteza)
			#v primeru, da je to zadnja poteza
			if trenutno.stanje.ali_je_konec():
				return trenutno.poteze + [poteza]
			else:
				# hevristika
				if hevristika == 'q_hevristika':
					m = -q_hevristika(q, trenutno.stanje)
				else:
					m = minimal(trenutno.stanje)
				f = m+len(trenutno.poteze)
				heappush(kandidati, Node(trenutno.poteze + [poteza], copy.deepcopy(trenutno.stanje), f))
				trenutno.stanje = copy.deepcopy(auxstanje)
   
# Parameter hevristrika je lahko :
# --minimal
# --q_hevristika
def test(filename, hevristika):
	t = time.time()
	stanje = ps.Stanje()
	stanje.uvozi_stanje(filename)
	if hevristika == 'q_hevristika':
		q = ql.ponavljaj_q_learning(100, 20000)
		stanje.uvozi_stanje(filename)
		sol = astar(stanje,  hevristika, q)
	else:
		sol = astar(stanje,  hevristika, dict())
	print()
	for poteza in sol:
		print(poteza)
	print()
	print(time.time()-t)
	ps.zapisi_zaporedje_potez(filename[:-4]+"resitev.txt",sol)
	return sol

# uvoz stanja
infile = 'testni_primeri/test-3x3-palacinke.txt'
stanje = ps.Stanje([[]],[])
stanje.uvozi_stanje(infile)
#q = ql.ponavljaj_q_learning(100, 20000)
#print(q)

filename = "testni_primeri/test-3x3-palacinke.txt"
#filename = "testni_primeri/test-4x4-palacinkaVelikanka.txt"
#filename = "testni_primeri/test-4x4-sadnaKupa.txt"
# filename = "testni_primeri/test-5x7-postar.txt"
test(filename, 'q_hevristika')
