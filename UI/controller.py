import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.mese_selezionato = 0

    def leggi_mese(self, e):
        self.mese_selezionato = int(e.control.value)

    def get_consumo_medio(self, e):
        if self.mese_selezionato == 0:
            self._view.show_alert("Selezionare un Mese!")
        else:
            consumo_medio = self._model.get_consumo_medio(self.mese_selezionato)
            self._view.lista_visualizzazione.controls.clear()
            self._view.lista_visualizzazione.controls.append(
                ft.Text(f"Il consumo medio nel mese selezionato é:")
            )
            for impianto_media in consumo_medio:
                self._view.lista_visualizzazione.controls.append(ft.Text(f"{impianto_media[0]}: {impianto_media[1]}"))
            self._view.page.update()

    def calcola_sequenza(self, e):
        if self.mese_selezionato == 0:
            self._view.show_alert("Selezionare un Mese!")
        else:
            sequenza_ottima, costo = self._model.get_sequenza_ottima(self.mese_selezionato)
            self._view.lista_visualizzazione.controls.clear()
            self._view.lista_visualizzazione.controls.append(ft.Text(f"La sequenza ottima ha costo {costo},00€ ed è:"))
            for stop in sequenza_ottima:
                self._view.lista_visualizzazione.controls.append(ft.Text(stop))
            self._view.update()
