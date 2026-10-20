import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # creazione dei campi di input e del contatore, preparo i componenti grafici (Textfield e pulsanti) che serviranno
    #all'utente per digitare i dati del nuovo strumento
    #l'interfaccia ha bisogno di raccogliere 3 informazioni str o int e di un sistema contatore con bottoni + e -

    #campi per l'aggiunta di un nuovo strumento
    input_tipo= ft.TextField(label="Tipo", expand=True)
    input_marca= ft.TextField(label="Marca", expand=True)
    input_anno= ft.TextField(label="Anno", expand=True)

    #contatore per il valore in euro dello strumento
    valore_euro= 0
    txt_valore= ft.Text(value= "0", size=16)

    def decrementa_valore(e):
        nonlocal valore_euro   #NONLOCAL????
        if valore_euro >= 50:
            valore_euro -= 50
            txt_valore.value = str(valore_euro)
            page.update()

    def incrementa_valore(e):
        nonlocal valore_euro
        valore_euro += 50
        txt_valore.value = str(valore_euro)
        page.update()

    cnt_valore = ft.Row(
        controls=[
            ft.IconButton(ft.Icons.REMOVE, on_click=decrementa_valore),
            txt_valore,
            ft.IconButton(ft.Icons.ADD, on_click=incrementa_valore),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # controllo dei campi vuoti: si verifica che l'utente non abbia lasciato caselle vuote
    #si verifica che l'anno inserito sia un numero valido convertendolo in int
    #gestione dell'errore se si mette non un numero nell'anno
    #se i controlli vanno a buon fine si aggiornano i dati per aggiungerli alla lista generale
    #si svuotano i campi di testo (Textfield) e si richiama la funzione che aggiorna la schermata (ListView)
    #per mostrare subito lo strumento appena aggiunto

    def aggiungi_strumento_click(e):
        # mettiamo i campi in una lista
        campi = [input_tipo.value, input_marca.value, input_anno.value]

        # controllo con un ciclo for se c'è un campo vuoto
        for campo in campi:
            if not campo or not campo.strip():
                alert.show_alert("Errore: compila tutti i campi prima di procedere.")
                return

        # Estraiamo i valori puliti dai campi di testo
        tipo = input_tipo.value.strip()
        marca = input_marca.value.strip()
        anno_str = input_anno.value.strip()

        # Validazione numerica per l'anno di acquisto
        try:
            anno = int(anno_str)
        except ValueError:
            alert.show_alert("Errore: inserisci valori numerici validi per l'anno.")
            return

        # Aggiunta dello strumento all'interno della struttura dati del deposito
        deposito.aggiungi_strumento(tipo=tipo, marca=marca, anno_acquisto=anno, valore=float(valore_euro))

        # Pulizia dei campi di input dell'interfaccia
        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""

        # Aggiornamento grafico della lista a schermo
        aggiorna_lista_strumenti()


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # si crea fisicamente l'oggetto bottone grafico perché bisogna associare il bottone alla funzione logica
    #creata nell'on_click=aggiungi_strumento_click scritto in precedenza in modo tale che premendolo si attivi tutto il codice
    #di controllo e inserimento

    pulsante_aggiungi_strumento = ft.ElevatedButton("Aggiungi Strumento", on_click= aggiungi_strumento_click)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # inserimento del layout nella pagina, si posizionano gli elementi grafici creati all'interno della struttura della pagina
        # lo si fa perché Flet ha bisogno che Titolo della sezione, la riga con i campi di input e il contatore, e il pulsante di conferma
        #vengano aggiunti esplicitamente così che vengano visualizzati correttamente sullo schermo del computer

        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(controls=[input_tipo, input_marca, input_anno, cnt_valore],
               alignment=ft.MainAxisAlignment.CENTER,
               ),
        pulsante_aggiungi_strumento,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.app(target=main)
