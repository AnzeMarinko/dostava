import podatkovne_strukture as ps
from collections import defaultdict
import itertools 
from random import choices
from copy import deepcopy

# Generira funkcijo, ki doloca igralno strategijo:
def strategija(q, e): 
    def izberi_akcijo(state): 
        
        akcije = q[state.pretvori_v_niz()]
        sez_akcij = list(akcije.keys()) # Seznam moznih akcij

        najboljsa_akcija = max(akcije, key=lambda k: akcije[k])
        i_najboljsa_akcija = sez_akcij.index(najboljsa_akcija)
        
        st_akcij = len(sez_akcij)
        verjetnosti_akcij =  [e / st_akcij] * st_akcij
        
        if akcije[najboljsa_akcija] != 0:
            verjetnosti_akcij[i_najboljsa_akcija] += (1.0 - e)  # Najboljsa poteza je najbol verjetna
        
        return sez_akcij, verjetnosti_akcij 
   
    return izberi_akcijo 

# Preveri, ali je stanje ze v q:
def ali_je_v_q(stanje, q):
    for st in q.keys():
        if st.polja == stanje.polja and st.roboti == stanje.roboti:
            return True
    else:
        return False

# ce stanja se ni v q ga doda, vsem akcijam iz stanja pripise verjetnosti 0
def dodaj_stanje_v_q(q, stanje, sez_potez):
    shrani_stanje = stanje.pretvori_v_niz()
    if shrani_stanje not in q.keys():
        poteza_verjetnost = dict()
        for poteza in sez_potez:
            poteza_verjetnost[poteza] = 0
        q[shrani_stanje] = poteza_verjetnost
    return q

# Ovrednoti razdalijo do trga:
def razdaljija_do_trga(stanje, prejsno_stanje, poteza):
    robot = prejsno_stanje.roboti[poteza[1]]
    x = robot.polozaj[0] + poteza[2]
    y = robot.polozaj[1] + poteza[3]
    najblizja_stra = 100
    najblizja_nova = 100
    for i in range(stanje.n):
        for j in range(stanje.m):
            if stanje.polja[i][j].tip == 'trg' and robot.blago[0] in stanje.polja[i][j].atributi.keys():
                stara_razdalja = ((robot.polozaj[0] - j) ** 2 + (robot.polozaj[1] - i) ** 2) ** (1/2)
                nova_razdalja = ((x - j) ** 2 + (y - i) ** 2) ** (1/2)
                if nova_razdalja <  najblizja_nova:
                    najblizja_nova = nova_razdalja
                if stara_razdalja < najblizja_stra:
                    najblizja_stara = stara_razdalja
    if  najblizja_stara == 1:
        return -0.1
    if najblizja_stara > najblizja_nova:
        return -0.01
    elif najblizja_stara < najblizja_nova:
        return -1
    else:
        return -0.1

# Ovrednoti razdalijo do skladisca:
def razdaljija_do_skladisca(stanje, prejsno_stanje, poteza):
    robot = prejsno_stanje.roboti[poteza[1]]
    x = robot.polozaj[0] + poteza[2]
    y = robot.polozaj[1] + poteza[3]
    najblizja_stra = 100
    najblizja_nova = 100
    for i in range(stanje.n):
        for j in range(stanje.m):
            if stanje.polja[i][j].tip == 'skladisce':
                stara_razdalja = ((robot.polozaj[0] - j) ** 2 + (robot.polozaj[1] - i) ** 2) ** (1/2)
                nova_razdalja = ((x - j) ** 2 + (y - i) ** 2) ** (1/2)
                if nova_razdalja <  najblizja_nova:
                    najblizja_nova = nova_razdalja
                if stara_razdalja < najblizja_stra:
                    najblizja_stara = stara_razdalja
    if najblizja_stara == 1:
        return -0.1
    elif najblizja_stara > najblizja_nova:
        return -0.001
    elif najblizja_stara < najblizja_nova:
        return -1
    else:
        return -0.1

# Izracuna nagrado:
def poisci_nagrado(stanje, prejsno_stanje, poteza):
    if stanje.ali_je_konec() == True:
        return 100
    if prejsno_stanje == None:
        return 0
    robot = prejsno_stanje.roboti[int(poteza[1])]
    x = robot.polozaj[0] + poteza[2]
    y = robot.polozaj[1] + poteza[3]
    if poteza[0] == 'nalaganje':
        blago_n, kolicina_n = poteza[4], poteza[5]
        for i in range(stanje.n):
            for j in range(stanje.m):
                if stanje.polja[i][j].tip == 'trg':
                    for blago, kolicina in stanje.polja[i][j].atributi.items():
                        if blago == blago_n:
                            return min(kolicina, kolicina_n)
    elif poteza[0] == 'odlaganje' and stanje.polja[y][x].tip == 'trg' and prejsno_stanje.polja[y][x].tip == 'trg':
        blago, kolicina = robot.blago
        if prejsno_stanje.polja[y][x].atributi[blago] - kolicina < 0:
            return -10
        elif stanje.polja[y][x].atributi[blago] == None:
            return(prejsno_stanje.polja[y][x].atributi[blago])
        else:
            return(prejsno_stanje.polja[y][x].atributi[blago] - stanje.polja[y][x].atributi[blago])
    elif poteza[0] == 'premakni' and robot.blago == ('',0):
        return(razdaljija_do_skladisca(stanje, prejsno_stanje, poteza))
    elif poteza[0] == 'premakni':
        return(razdaljija_do_trga(stanje, prejsno_stanje, poteza))
    else:
        return 0



def q_learning(zacetno_stanje, st_poiskusov,q=dict(), diskontiraj = 0.06, 
                            alpha = 0.6, e = 0.1): 
    """ 
    Q-Learning algorithm: Off-policy TD control. 
    Finds the optimal greedy policy while improving 
    following an epsilon-greedy policy"""

    # Seznam vseh moznih potez iz zacetnega stanja
    sez_potez = zacetno_stanje.socasne_poteze()

    # q je tipa slovar slovarjev: stanje -> akcija -> verjetnost
    # q privzeto vraca vrednosti 0
    q = dodaj_stanje_v_q(q, zacetno_stanje, sez_potez)

    policy = strategija(q, e)
       

    for iti_poiskus in range(st_poiskusov): 
        #print('st. piskuasa: ', iti_poiskus)
        # Shrani zacetno stanje: 
        stanje = zacetno_stanje 
        #print(stanje)
               
        # Iz danega stanja vrne slovar akcija -> verjetnost 
        sez_akcij, verjetnosti_akcij = policy(stanje) 
        socasne_pot = stanje.socasne_poteze()
        #print(socasne_pot)
        #print(sez_akcij, verjetnosti_akcij)
        # Izbere akcijo glede na utezi (podane verjetnosti):
        poteza = choices(sez_akcij, weights = verjetnosti_akcij, k=1)
        poteza = poteza[0]
        #if poteza[0] == 'nalaganje':
        #    print(poteza)
        # izvede potezo in dobi nagrado:
        prejsno_stanje = deepcopy(stanje)
        nagrada = 0
        if type(poteza[0]) == tuple:
            for pot in poteza:
                pr_stanje = deepcopy(stanje)
                stanje.izvedi_potezo(pot)
                nag = poisci_nagrado(stanje, pr_stanje, pot)
                nagrada += nag
        else:
            stanje.izvedi_potezo(poteza)
            nagrada = poisci_nagrado(stanje, prejsno_stanje, poteza)
        #print(nagrada)
        # ce novega stanja se ni v q ga doda, vsem akcijam iz stanja pripise verjetnosti 0
        sez_potez = stanje.socasne_poteze()
        q = dodaj_stanje_v_q(q, stanje, sez_potez)

        # TD Update
        nove_poteze = q[stanje.pretvori_v_niz()]
        nova_najboljsa_poteza = max(nove_poteze, key=lambda k: nove_poteze[k]) 
  
        td_target = nagrada + diskontiraj * q[stanje.pretvori_v_niz()][nova_najboljsa_poteza] 
        td_delta = td_target - q[prejsno_stanje.pretvori_v_niz()][poteza]
        q[prejsno_stanje.pretvori_v_niz()][poteza] += alpha * td_delta 
        #print(q[prejsno_stanje.pretvori_v_niz()][poteza])
        # Preveri ali je konec   
        if stanje.ali_je_konec():
            print('st. piskuasa: ', iti_poiskus)
            print('Konec!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            return q
        zacetno_stanje = stanje

    return q

def ponavljaj_q_learning(st_poiskusov, st):
    infile = 'testni_primeri/test-3x3-palacinke.txt'
    stanje = ps.Stanje([[]],[])
    stanje.uvozi_stanje(infile)
    q = q_learning(stanje, st_poiskusov,q = dict(), diskontiraj = 0.6, alpha = 0.6, e = 0.2)
    for i in range(st):
        print(i)
        stanje = ps.Stanje([[]],[])
        stanje.uvozi_stanje(infile)
        q = q_learning(stanje, st_poiskusov,q = q, diskontiraj = 0.6, alpha = 0.6, e = 0.2)
    return q


def poisci_pot(q, stanje):
    sez_potez = list()
    i = 0
    while stanje.ali_je_konec() == False and i<250:
        if stanje.pretvori_v_niz() in q.keys():
            akcije = q[stanje.pretvori_v_niz()]
            najboljsa_akcija = max(akcije, key=lambda k: akcije[k])
            print(najboljsa_akcija)
            sez_potez.append(najboljsa_akcija)
            if type(najboljsa_akcija[0]) == tuple:
                for poteza in najboljsa_akcija:
                    stanje.izvedi_potezo(poteza)
            else:
                stanje.izvedi_potezo(najboljsa_akcija)

        else:
            print('Stanja ni v slovarju q!!')
            #print(q, stanje)
            break
        i += 1
    ps.zapisi_zaporedje_potez('resitve/q_l_test-3x3-palacinke.txt', sez_potez)
    print('Resitev shranjena')


# naslov datoteke z zapisanom zacetnim stanjem
#infile = 'testni_primeri/test-3x3-palacinke.txt'
infile = 'testni_primeri/test-3x3-palacinke.txt'


# uvoz stanja
#stanje = ps.Stanje([[]],[])
#stanje.uvozi_stanje(infile)

#q = ql.q_learning(stanje, 30, diskontiraj = 0.6, alpha = 0.6, e = 0.1)
#q = ponavljaj_q_learning(100, 1000000)
#print(q)

#poisci_pot(q, stanje)
