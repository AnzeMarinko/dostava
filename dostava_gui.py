import podatkovne_strukture as ps
import umetna_inteligenca as ui
import tkinter

w = 600
h = 600
infile = 'testni_primeri/test1.txt'

stanje = ps.Stanje([[]],[])
stanje.uvozi_stanje(infile)
print(stanje)


# TODO:
	# v meni daj moznosti poganjanja razlicnih algoritmov UI, uvoz stanja iz datoteke, izris in print zaporedja potez ...
	
# in na polj dodaj vrste in količine blaga
	# npr. seznam blaga na skladisca in trge ter kjer je robot nakazemo z velikostjo kroga njegovo velikost in noter napisemo kaj nosi

window = tkinter.Tk()
window.title("Dostava")
window.geometry("{}x{}".format(w,h+50))
frame1 = tkinter.Frame(window).grid(row = 0)
button = tkinter.Button(frame1, text='Osveži', width=10, command=lambda: osvezi())
button.grid(column=0,row=0)
frame2 = tkinter.Frame(window).grid(row=1)
def naprej():
	print(stanje.roboti[0].polozaj)
	stanje.roboti[0].polozaj = (0,1)
def osvezi():
	m = len(stanje.polja)
	n = len(stanje.polja[0])
	frames = [[0 for _ in range(n)] for _ in range(m)]
	for vrstica in range(m):
		for polje in range(n):
			p = stanje.polja[vrstica][polje]
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
					text = '  Trg:'
					for blago, kolicina in p.atributi.items():
						if kolicina > 0:
							text += '\n{}:{}'.format(blago,kolicina)
			elif p.tip in 'skladisce':
				background="Red"
				text = ''
				if p.atributi:
					text = '  Skladišče:'
					for blago, kolicina in p.atributi.items():
						if kolicina > 0:
							text += '\n{}:{}'.format(blago,kolicina)
			elif p.tip in 'ovira':
				background="Black"
				text = ''
			frames[vrstica][polje] = tkinter.Frame(frame2, width=w//n, height=h//m, background = background).grid(row=vrstica+1,column=polje)
			if len(text) > 0:
				tkinter.Label(frames[vrstica][polje],text=text).grid(row=vrstica+1,column=polje)
	naprej()
window.mainloop()