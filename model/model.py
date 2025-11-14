from database.impianto_DAO import ImpiantoDAO
from database.consumo_DAO import ConsumoDAO

'''
    MODELLO:
    - Rappresenta la struttura dati
    - Si occupa di gestire lo stato dell'applicazione
    - Interagisce con il database
'''

class Model:
    def __init__(self):
        self._impianti = None
        self.load_impianti()

        self.__sequenza_ottima = []
        self.__costo_ottimo = -1

    def load_impianti(self):
        """ Carica tutti gli impianti e li setta nella variabile self._impianti """
        self._impianti = ImpiantoDAO.get_impianti()

    def get_consumo_medio(self, mese:int):
        """
        Calcola, per ogni impianto, il consumo medio giornaliero per il mese selezionato.
        :param mese: Mese selezionato (un intero da 1 a 12)
        :return: lista di tuple --> (nome dell'impianto, media), es. (Impianto A, 123)
        """
        risultati = ConsumoDAO.get_consumo_medio_per_mese(mese) #nome impianto e consumo medio
        consumi_medi = []
        for row in risultati:
            nome_impianto = row['nome']
            media = row['AVG(consumo.kwh)']
            consumi_medi.append((nome_impianto, media))

        return consumi_medi
        # TODO

    def get_sequenza_ottima(self, mese:int):
        """
        Calcola la sequenza ottimale di interventi nei primi 7 giorni
        :return: sequenza di nomi impianto ottimale
        :return: costo ottimale (cioè quello minimizzato dalla sequenza scelta)
        """
        self.__sequenza_ottima = []
        self.__costo_ottimo = -1
        consumi_settimana = self.__get_consumi_prima_settimana_mese(mese)

        self.__ricorsione([], 1, None, 0, consumi_settimana)

        # Traduci gli ID in nomi
        id_to_nome = {impianto.id: impianto.nome for impianto in self._impianti}
        sequenza_nomi = [f"Giorno {giorno}: {id_to_nome[i]}" for giorno, i in enumerate(self.__sequenza_ottima, start=1)]
        return sequenza_nomi, self.__costo_ottimo

    def __ricorsione(self, sequenza_parziale, giorno, ultimo_impianto, costo_corrente, consumi_settimana):
        """ Implementa la ricorsione """
        #1) imposto la condizione di uscita
        if giorno > 7:
            if self.__costo_ottimo == -1 or costo_corrente < self.__costo_ottimo:
                self.__sequenza_ottima = sequenza_parziale.copy()
                self.__costo_ottimo = costo_corrente
            return
        else:
            #2) imposto un ciclo per valutare i costi di entambi gli impianti
            for impianto in self._impianti:
                id_impianto = impianto.id
                #considero il costo di spostamento da un impianto all'altro
                costo_spostamento = 5 if (ultimo_impianto is not None
                                          and ultimo_impianto != id_impianto) else 0
                #prelevo il dato dal dizionario, usando come chiave l'id dell'impianto considerato
                costo_consumo = consumi_settimana[id_impianto][giorno-1]
                costo_giorno = costo_spostamento + costo_consumo
                nuovo_costo = costo_corrente + costo_giorno
                sequenza_parziale.append(id_impianto)

                #3) uso la ricorsione per passare al giorno successivo
                self.__ricorsione(sequenza_parziale, giorno + 1, id_impianto,
                                nuovo_costo, consumi_settimana)

        #4) uso il backtraking per provare l'altra opzione
                sequenza_parziale.pop()
        # TODO

    def __get_consumi_prima_settimana_mese(self, mese: int):
        """
        Restituisce i consumi dei primi 7 giorni del mese selezionato per ciascun impianto.
        :return: un dizionario: {id_impianto: [kwh_giorno1, ..., kwh_giorno7]}
        """
        consumi_settimana = {}
        # Per ogni impianto, recupera i consumi dei primi 7 giorni del mese
        for impianto in self._impianti:
            id_impianto = impianto.id
            consumi = ConsumoDAO.get_consumi(id_impianto)
            if consumi is None:  # ← Gestisci il caso None
                continue

        # Filtra i consumi per il mese selezionato e prendi solo i primi 7 giorni
            consumi_mese = []
            for consumo in consumi:
              # Verifica che il consumo sia del mese selezionato
                if consumo.data.month == mese:
                    giorno = consumo.data.day
          # Considera solo i primi 7 giorni
                    if 1 <= giorno <= 7:
                        consumi_mese.append((giorno, consumo.kwh))
         # Ordina per giorno e crea la lista dei consumi
            consumi_mese.sort(key=lambda x: x[0])
        # Estrai solo i valori kWh mantenendo l'ordine dei giorni
            kwh_settimana = [] # Inizializza con 7 zeri
            for row in consumi_mese:
                kwh_settimana.append(row[1])
            consumi_settimana[id_impianto] = kwh_settimana

        return consumi_settimana
        # TODO

