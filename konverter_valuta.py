from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import requests


def dohvati_sve_valute():
    url = "https://api.exchangerate-api.com/v4/latest/EUR"
    response = requests.get(url)
    if response.status_code == 200:
        podaci = response.json()
        valute = list(podaci["rates"].keys())
        return valute
    else:
        messagebox.showerror("Greška", "Neuspješno dohvaćanje valuta")
        return None


def dohvati_tecaj(valuta):
    url = f"https://api.exchangerate-api.com/v4/latest/EUR"
    response = requests.get(url)
    if response.status_code == 200:
        podaci = response.json()
        if valuta in podaci["rates"]:
            tecaj = podaci["rates"][valuta]
            return float(tecaj)
        else:
            messagebox.showerror("Greška", "Podaci za valutu nisu dostupni")
            return None
    else:
        messagebox.showerror("Greška", "Neuspješno dohvaćanje tečaja")
        return None


def konvertiraj():
    krajnji_iznos_entry.delete(0, END)
    ime_valute = unos_vlaute_za_konverziju.get()
    tecaj = dohvati_tecaj(ime_valute)
    if tecaj is None:
        messagebox.showerror("Greška", "Neuspješno dohvaćanje tečaja")
        return
    iznos = float(iznos_entry.get())
    konv = iznos * tecaj
    konv = round(konv, 2)
    konv = "{:,}".format(konv)
    krajnji_iznos_entry.insert(0, konv)


def clear():
    iznos_entry.delete(0, END)
    krajnji_iznos_entry.delete(0, END)


# Kreiranje glavnog prozora
root = Tk()
root.title("Konverter valuta")
root.geometry("500x500")

# Kreiranje taba
moj_tab = ttk.Notebook(root)
moj_tab.pack(pady=5)

# Kreiranje okvira
okvir_valuta = Frame(moj_tab, width=480, height=480)
okvir_konverzije = Frame(moj_tab, width=480, height=480)

okvir_valuta.pack(fill="both", expand=1)
okvir_konverzije.pack(fill="both", expand=1)

# Dodavanje okvira tabovima
moj_tab.add(okvir_valuta, text="Valute")
moj_tab.add(okvir_konverzije, text="Konverzija")

# Onemogućenje drugog taba
moj_tab.tab(1, state="disabled")


def zakljucaj():
    # Ako obje valute nisu unesene, prikaži error
    if not vasa_valuta_entry.get() or not unos_vlaute_za_konverziju.get():
        messagebox.showwarning("PAŽNJA!", "Niste ispunili sva polja!")
    else:
        vasa_valuta_entry.config(state="disabled")
        unos_vlaute_za_konverziju.config(state="disabled")
        unos_tecaja.config(state="normal")
        tecaj_za_konverziju = dohvati_tecaj(unos_vlaute_za_konverziju.get())
        if tecaj_za_konverziju is not None:
            unos_tecaja.delete(0, END)
            unos_tecaja.insert(
                0,
                f"1 {vasa_valuta_entry.get()} = {tecaj_za_konverziju} {unos_vlaute_za_konverziju.get()}",
            )
            unos_tecaja.config(state="disabled")
            moj_tab.tab(1, state="normal")
        else:
            messagebox.showerror("Greška", "Neuspješno dohvaćanje tečaja")


def otkljucaj():
    vasa_valuta_entry.config(state="normal")
    unos_vlaute_za_konverziju.config(state="normal")
    unos_tecaja.configure(state="normal")
    unos_tecaja.delete(0, END)
    unos_tecaja.configure(state="disabled")
    tecaj_label.config(text="Trenutni tečaj:")


# Odabir prve valute
vasa_valuta_label = LabelFrame(
    okvir_valuta, text="Unesite valutu koju želite konvertirati: "
)
vasa_valuta_label.pack(pady=20)

valute = dohvati_sve_valute()

vasa_valuta_entry = ttk.Combobox(
    vasa_valuta_label, values=valute, font=("Helvetica", 24)
)
vasa_valuta_entry.pack(padx=10, pady=10)

# Unos druge valute
konverzija = LabelFrame(okvir_valuta, text="Konverzija valute")
konverzija.pack(pady=20)

konverzija_label = Label(konverzija, text="Konvertiraj u: ")
konverzija_label.pack(pady=10)

unos_vlaute_za_konverziju = ttk.Combobox(
    konverzija, values=valute, font=("Helvetica", 24)
)
unos_vlaute_za_konverziju.pack(padx=10, pady=10)

# Ispis tečaja
tecaj_label = Label(konverzija, text="Trenutni tečaj:")
tecaj_label.pack(pady=10)

unos_tecaja = Entry(konverzija, font=("Helvetica", 24), state="disabled")
unos_tecaja.pack(padx=10, pady=10)

# Buttons
okvir_gumba = Frame(okvir_valuta)
okvir_gumba.pack(pady=20)

zakljucaj_button = Button(okvir_gumba, text="Zaključaj", command=zakljucaj)
zakljucaj_button.grid(row=0, column=0, padx=10)

otkljucaj_button = Button(okvir_gumba, text="Otključaj", command=otkljucaj)
otkljucaj_button.grid(row=0, column=1, padx=10)

######################################################################################


iznos_konvertiranja_label = LabelFrame(okvir_konverzije, text="Iznos za konverziju: ")
iznos_konvertiranja_label.pack(pady=20)

iznos_entry = Entry(iznos_konvertiranja_label, font=("Helvetica", 24))
iznos_entry.pack(padx=10, pady=10)

konvertiraj_button = Button(
    iznos_konvertiranja_label, text="Konvertiraj", command=konvertiraj
)
konvertiraj_button.pack(pady=20)

krajnji_iznos_label = LabelFrame(okvir_konverzije, text="Krajnji iznos: ")
krajnji_iznos_label.pack(pady=20)

krajnji_iznos_entry = Entry(
    krajnji_iznos_label, font=("Helvetica", 24), bd=0, bg="systembuttonface"
)
krajnji_iznos_entry.pack(padx=10, pady=10)

clear_button = Button(okvir_konverzije, text="Ocisti", command=clear)
clear_button.pack(pady=20)

prostor_label = Label(okvir_konverzije, text="", width=70)
prostor_label.pack()

root.mainloop()
