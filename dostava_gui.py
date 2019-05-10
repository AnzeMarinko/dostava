import podatkovne_strukture as ps
import umetna_inteligenca as ui
import tkinter




# ==============================:
# TODO:
	# v meni daj moznosti poganjanja razlicnih algoritmov UI, uvoz stanja iz datoteke, izris in print zaporedja potez ...
	# novi testni primeri



# velikost igralne plosce
w = 600
h = 500
# naslov datoteke z zapisanom zacetnim stanjem
infile = 'testni_primeri/test1.txt'

# uvoz stanja
stanje = ps.Stanje([[]],[])
stanje.uvozi_stanje(infile)
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

# osvezi izrisano stanje
def osvezi():
	for vrstica in range(stanje.m):
		for polje in range(stanje.n):
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
			tkinter.Frame(plosca, width=w//stanje.n, height=h//stanje.m, background = background).grid(row=vrstica,column=polje)
			if len(text) > 0:
				tkinter.Label(plosca,text=text).grid(row=vrstica,column=polje)

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

window.mainloop()