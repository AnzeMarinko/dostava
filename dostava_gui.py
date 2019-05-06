import podatkovne_strukture as ps
import umetna_inteligenca as ui
import tkinter

#stanje = ps.uvozi_stanje("testni_primeri/test1.txt")
stanje = ps.Stanje([[]],[])
#print(stanje)

w = 600
h = 600


# TODO:
	# prestavi gumbe za osveževanje in drugo v meniin na polj dodaj vrste in količine blaga
	# npr. seznam blaga na skladisca in trge ter kjer je robot nakazemo z velikostjo kroga njegovo velikost in noter napisemo kaj nosi


window = tkinter.Tk()
window.title("Dostava")
window.geometry("{}x{}".format(w+50,h+100))
frame1 = tkinter.Frame(window).grid(row = 0)
tkinter.Label(frame1, text='Inputfile:').grid(row=0,column=0)
infile = tkinter.Entry(frame1)
infile.grid(row=0, column=1)
button = tkinter.Button(frame1, text='Uvozi', width=10, command=lambda: stanje.uvozi_stanje("testni_primeri/test1.txt")) #infile.get()))
button.grid(row=0,column=2)
button2 = tkinter.Button(frame1, text='Osveži', width=10, command=lambda: osvezi())
button2.grid(row=0,column=3)
tkinter.Label(window, text='Vrstica z ukazi ... poženi UI1, UI2 ...\n').grid(row=1)
frame2 = tkinter.Frame(window).grid(row=2)
def osvezi():
	m = len(stanje.polja)
	n = len(stanje.polja[0])
	for vrstica in range(len(stanje.polja)):
		for polje in range(len(stanje.polja[vrstica])):
			tip = stanje.polja[vrstica][polje].tip
			if tip in 'garaza':
				background="Blue"
			elif tip in 'pot':
				background="White"
			elif tip in 'trg':
				background="Green"
			elif tip in 'skladisce':
				background="Red"
			elif tip in 'ovira':
				background="Black"
			tkinter.Frame(frame2, width=w//n, height=h//m, background = background).grid(row=vrstica+2,column=polje)
			# text=stanje.polja[vrstica][polje]
window.mainloop()