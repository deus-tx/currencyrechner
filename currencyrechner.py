import tkinter as tk
from tkinter import ttk
import requests  # für frankfurter api

root = tk.Tk()
root.title('Currency Rechner')
window = ttk.Frame(root, padding=10)
window.grid()

# funktionen (ki genutzt)
def betragstext_updater(event):
    selected = curr_dropdown_from.get()
    label_amount.config(text=f"Betrag ({selected}): ")

def umrechnen():
    von_currency = curr_dropdown_from.get()
    nach_currency = curr_dropdown_to.get()
    try:
        betrag = float(amount_from.get())
    except (ValueError, tk.TclError):
        label_ergebnis_von.config(text="Das ist keine Dezimalzahl oder natürliche Zahl!")
        label_ergebnis_nach.config(text="")
        return
    von_code = von_currency.split()[0].upper()
    nach_code = nach_currency.split()[0].upper()
    if von_code == nach_code:
        kurs = 1.0
    else:
        try:
            url = f"https://api.frankfurter.dev/v1/latest?base={von_code}&symbols={nach_code}"
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                kurs = response.json()["rates"].get(nach_code, 1.0)
            else:
                label_ergebnis_von.config(text="Fehler")
                label_ergebnis_nach.config(text="API-Fehler")
                return
        except requests.RequestException:
            label_ergebnis_von.config(text="Fehler")
            label_ergebnis_nach.config(text="Netzwerkfehler")
            return
    ergebnis = betrag * kurs
    label_ergebnis_von.config(text=f"{betrag:.2f} {von_currency}")
    label_ergebnis_nach.config(text=f"{ergebnis:.2f} {nach_currency}")

# texte
ttk.Label(window, text="Von").grid(column=1, row=0)
ttk.Label(window, text=" -> ").grid(column=2, row=1)
ttk.Label(window, text="In").grid(column=3, row=0)

# trennlinien
ttk.Label(window, text="-"*123).grid(column=0, row=2, columnspan=5, sticky="ew")
ttk.Label(window, text="-"*123).grid(column=0, row=4, columnspan=5, sticky="ew")

# dropdowns
currencies = ['EUR €', 'USD $', 'GBP £', 'JPY ¥', 'CHF', 'CAD $', 'AUD $']
curr_dropdown_from = ttk.Combobox(window, values=currencies, state="readonly")
curr_dropdown_to = ttk.Combobox(window, values=currencies, state="readonly")
curr_dropdown_from.current(0)
curr_dropdown_to.current(1)
curr_dropdown_from.grid(column=1, row=1)
curr_dropdown_to.grid(column=3, row=1)

# betragstext updaten
curr_dropdown_from.bind("<<ComboboxSelected>>", betragstext_updater)

# betragstextzeugs
label_amount = ttk.Label(window, text="Betrag (EUR €): ")
label_amount.grid(column=0, row=3)
amount_from = tk.DoubleVar(value=0.0)
entry_from = ttk.Entry(window, textvariable=amount_from)
entry_from.grid(column=2, row=3)

# go button
ttk.Button(window, text="Go", command=umrechnen).grid(column=4, row=3)

# ergebnisse
label_ergebnis_von = ttk.Label(window, text="0.00 EUR €")
label_ergebnis_von.grid(column=1, row=5)
ttk.Label(window, text=" ≙ ").grid(column=2, row=5)
label_ergebnis_nach = ttk.Label(window, text="0.00 USD $")
label_ergebnis_nach.grid(column=3, row=5)

# quit button und mainloop
ttk.Button(window, text="Quit", command=root.destroy).grid(column=4, row=5)
root.mainloop()
