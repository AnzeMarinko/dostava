# random stanje
import random
import sys

outfile = "testni_primeri/"+sys.argv[1]+".txt"
# primer ukaza v konzoli: python3 random_test.py test1

sirina = random.randint(3,6)  # sirina plosce
visina = random.randint(3,6)  # visina plosce

roboti = random.randint(1,3)  # stevilo robotov
skladisca = random.randint(1,3)  # stevilo skladisc
trgi = random.randint(1,3)   # stevilo trgov
blago = random.randint(1,3) # stavilo razlicnih vrst blaga
ovire = random.randint(0,2)  # stevilo ovir
tipi = ['robot']*roboti + ['skladisce']*skladisca + ['trg']*trgi + ['ovira']*ovire
tipi = tipi[0:min(len(tipi), sirina*(visina-1))]
bl = ['Aa','Bb','Cc','Dd','Ee']
blago = {bl[i]:random.randint(1,10) for i in range(blago)}
kandidati = {(i,j) for i in range(sirina) for j in range(visina)}

polja = [['pot' for i in range(sirina)] for j in range(visina)]
roboti = ""

for tip in tipi:
	(i,j) = kandidati.pop()
	if tip == 'robot':
		polja[j][i] = 'garaza'
		roboti = roboti+"\n{},{},{},,0".format(random.randint(1,5), i, j)
	elif tip == 'skladisce':
		if skladisca == 1:
			ponudba = ""
			for (bl, potreba) in blago.items():
				if potreba > 0:
					ponudba = ponudba+" {}.{}".format(bl, potreba+random.randint(0,3))
		else:
			ponudba = ""
			for (bl, potreba) in blago.items():
				if potreba > 0:
					kolicina = random.randint(0,potreba-1)
					if kolicina > 0:
						ponudba = ponudba+" {}.{}".format(bl, kolicina+random.randint(0,3))
					blago[bl] -= kolicina
		skladisca -= 1
		polja[j][i] = 'skladisce' + ponudba
	elif tip == 'trg':
		if trgi == 1:
			povprasevanje = ""
			for (bl, potreba) in blago.items():
				if potreba > 0:
					povprasevanje=povprasevanje+" {}.{}".format(bl, potreba)
		else:
			povprasevanje = ""
			for (bl, potreba) in blago.items():
				if potreba > 0:
					kolicina = random.randint(0,potreba-1)
					if kolicina > 0:
						povprasevanje=povprasevanje+" {}.{}".format(bl, kolicina)
					blago[bl] -= kolicina
		trgi -= 1
		polja[j][i] = 'trg' + povprasevanje
	elif tip == 'ovira':
		polja[j][i] = 'ovira'

polja = "Nakljucen test\n\n"+"\n".join([",".join(vrstica) for vrstica in polja])+"\n"+roboti+"\n"
print(polja)

with open(outfile, "w") as f:
	f.write(polja)