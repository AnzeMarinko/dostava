import podatkovne_strukture as ps
import umetna_inteligenca as ui
import tkinter
import os




# ==============================:
# TODO:


# velikost igralne plosce
w = 900
h = 500
# naslov datoteke z zapisanom zacetnim stanjem
infile = 'testni_primeri/test-3x3-palacinke.txt'

# uvoz stanja
stanje = ps.Stanje([[]],[])
stanje.uvozi_stanje(infile)
print(stanje)

# izbriši prvotno stanje:
def pozabi_stanje():
	for i in plosca.grid_slaves():
		i.grid_forget()

# osvezi izrisano stanje
def osvezi():
	pozabi_stanje()
	for vrstica in range(stanje.n):
		for polje in range(stanje.m):
			p = stanje.polja[vrstica][polje]
			# obarvaj glede na tip in pripravi text za izpis na polju
			if p.tip in 'garaza':
				background="Yellow"
				text = ''
				if p.atributi:
					text = '{} <= {}'.format(p.atributi.blago, p.atributi.prostor)
			elif p.tip in 'pot':
				background="White"
				text = ''
				if p.atributi:
					text = '{} <= {}'.format(p.atributi.blago, p.atributi.prostor)
			elif p.tip in 'trg':
				background="Blue"
				text = ''
				if p.atributi:
					text = '[Trg]'
					for blago, kolicina in p.atributi.items():
						if kolicina > 0:
							text += '\n{}:{}'.format(blago,kolicina)
			elif p.tip in 'skladisce':
				background="Red"
				text = ''
				if p.atributi:
					text = '[Skladišče]'
					for blago, kolicina in p.atributi.items():
						if kolicina > 0:
							text += '\n{}:{}'.format(blago,kolicina)
			elif p.tip in 'ovira':
				background="Black"
				text = ''
			# definicija objekta
			tkinter.Frame(plosca, width=w//stanje.m, height=h//stanje.n, background = background).grid(row=vrstica,column=polje)
			if len(text) > 0:
				lab = tkinter.Label(plosca,text=text).grid(row=vrstica,column=polje)
				lab.config(fontsize="9")

# stanje nastavi na nov primer:
def novo_stanje(izbrani_primer):
	new_infile = 'testni_primeri/' + izbrani_primer
	stanje.uvozi_stanje(new_infile)
	osvezi()
	print(stanje)

# priprava okna
window = tkinter.Tk()
window.title("Dostava")
window.geometry("{}x{}".format(w,h+200))
# del z ukazi in del, kjer se izrisuje stanje
ukazi = tkinter.Frame(window, width=450, height=50, pady=3)
plosca = tkinter.Frame(window, width=50, height=40, padx=3, pady=3)
ukazi.grid(row=0, sticky="new")
plosca.grid(row=1, sticky="sew")
# vsi potrebni objekti za ukaze
idr = tkinter.Label(ukazi, text='robot')
dx = tkinter.Label(ukazi, text='dx')
dy = tkinter.Label(ukazi, text='dy')
eidr = tkinter.Entry(ukazi)
edx = tkinter.Entry(ukazi)
edy = tkinter.Entry(ukazi)
eidr.insert(tkinter.END,'0')
edx.insert(tkinter.END,'0')
edy.insert(tkinter.END,'0')
blago = tkinter.Label(ukazi, text='blago')
kolicina = tkinter.Label(ukazi, text='kolicina')
eblago = tkinter.Entry(ukazi)
ekolicina = tkinter.Entry(ukazi)
eblago.insert(tkinter.END,'')
ekolicina.insert(tkinter.END,'0')
err = tkinter.Label(ukazi, text='')
button = tkinter.Button(ukazi, text='Osveži', width=25, command=lambda: osvezi())
button2 = tkinter.Button(ukazi, text='Premik(robot,dx,dy)', width=25, command=lambda: premik())
button3 = tkinter.Button(ukazi, text='Nalozi(robot,dx,dy,blago,kolicina)', width=25, command=lambda: nalozi())
button4 = tkinter.Button(ukazi, text='Odlozi(robot,dx,dy)', width=25, command=lambda: odlozi())
button5 = tkinter.Button(ukazi, text='Naključna poteza', width=25, command=lambda: nakljucna_poteza())
# moznosti poganjanja razlicnih algoritmov UI
algoritem = tkinter.StringVar(ukazi)
algoritem.set('Brez algoritma') # default value
lalgoritem = tkinter.Label(ukazi, text='Izberi načini reševanja:')
option_algoritem = tkinter.OptionMenu(ukazi, algoritem, 'Brez algoritma', 'A*', 'Real time A*', 'Reinforcement learning')
# moznost izbire različnih primerov
primer = tkinter.StringVar(ukazi)
<<<<<<< HEAD
primer.set('test-3x3-palacinke.txt') # default value
=======
primer.set('test-3x3-palacinke') # default value
>>>>>>> 9d35c658cc06a0099576b971d45bf2ae8b3dce1c
lprimer = tkinter.Label(ukazi, text='Izberi primer:')
option_primer = tkinter.OptionMenu(ukazi, primer, *os.listdir('testni_primeri'), command=novo_stanje)
# postavitev objektov
idr.grid(row=0, column=0)
dx.grid(row=1, column=0)
dy.grid(row=2, column=0)
eidr.grid(row=0, column=1)
edx.grid(row=1, column=1)
edy.grid(row=2, column=1)
blago.grid(row=3, column=0)
kolicina.grid(row=4, column=0)
eblago.grid(row=3, column=1)
ekolicina.grid(row=4, column=1)
err.grid(row=0, column=3)
button.grid(row=0,column=2)
button2.grid(row=1,column=2)
button3.grid(row=2,column=2)
button4.grid(row=3,column=2)
button5.grid(row=4,column=2)
lalgoritem.grid(row=0,column=3)
option_algoritem.grid(row=0,column=4)
lprimer.grid(row=1,column=3)
option_primer.grid(row=1,column=4)

# premik v skladu z dobljenimi parametri
def premik():
	irobot=int(eidr.get())
	idx=int(edx.get())
	idy=int(edy.get())
	stanje.premakni(irobot,idx,idy)
	osvezi()

# nalaganje v skladu z dobljenimi parametri
def nalozi():
	irobot=int(eidr.get())
	idx=int(edx.get())
	idy=int(edy.get())
	blag = eblago.get()
	kol = int(ekolicina.get())
	stanje.nalaganje(irobot,idx,idy,blag,kol)
	osvezi()

# odlaganje v skladu z dobljenimi parametri
def odlozi():
	irobot=int(eidr.get())
	idx=int(edx.get())
	idy=int(edy.get())
	stanje.odlaganje(irobot,idx,idy)
	osvezi()

def nakljucna_poteza():
	if stanje.ali_je_konec() == False:
		poteza = stanje.random_poteza()
		if poteza[0] == 'premakni':
			stanje.premakni(poteza[1], poteza[2], poteza[3])
		elif poteza[0] == 'nalaganje':
			stanje.nalaganje(poteza[1], poteza[2], poteza[3],poteza[4], poteza[5])
		elif poteza[0] == 'odlaganje':
			stanje.odlaganje(poteza[1], poteza[2], poteza[3])
		osvezi()
		if stanje.ali_je_konec():
			konec = tkinter.Label(plosca, text='Konec') #NE IZPISUJE!!!
			konec.grid(row=1,column=1)

window.mainloop()
