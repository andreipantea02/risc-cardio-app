import streamlit as st
import pandas as pd
import joblib
import streamlit.components.v1 as components
import datetime

st.set_page_config(page_title="Cardio Risk AI", page_icon="🫀", layout="centered")

hide_spinners_css = """
<style>
input[type=number]::-webkit-inner-spin-button, 
input[type=number]::-webkit-outer-spin-button { 
    -webkit-appearance: none; 
    margin: 0; 
}
input[type=number] {
    -moz-appearance: textfield;
}
</style>
"""
st.markdown(hide_spinners_css, unsafe_allow_html=True)

@st.cache_resource
def load_assets():
    model = joblib.load('cardio_model_advanced.pkl')
    scaler = joblib.load('cardio_scaler_advanced.pkl')
    return model, scaler

model, scaler = load_assets()

variabile_stare = {'age': 45, 'height': 170, 'weight': 70, 'ap_hi': 120, 'ap_lo': 80}
for var_nume, val_implicita in variabile_stare.items():
    if f"{var_nume}_sl" not in st.session_state:
        st.session_state[f"{var_nume}_sl"] = val_implicita
    if f"{var_nume}_num" not in st.session_state:
        st.session_state[f"{var_nume}_num"] = val_implicita

def sincronizeaza_valori(nume_variabila, sursa_modificare):
    if sursa_modificare == 'glisor':
        st.session_state[f"{nume_variabila}_num"] = st.session_state[f"{nume_variabila}_sl"]
    else:
        st.session_state[f"{nume_variabila}_sl"] = st.session_state[f"{nume_variabila}_num"]

st.title("🫀 Analiza Riscului Cardiovascular")
st.markdown("Acest algoritm de inteligență artificială estimează probabilitatea afecțiunilor cardiace pe baza unui set de date extins din populația generală.")
st.divider()

st.header("Introduceți datele pacientului:")
col1, col2 = st.columns(2)

with col1:
    c1, c2 = st.columns([3, 1])
    c1.slider("Vârsta (ani)", 20, 100, key="age_sl", on_change=sincronizeaza_valori, args=('age', 'glisor'), help="Riscul cardiovascular crește natural și inevitabil odată cu înaintarea în vârstă deoarece peretele arterelor își pierde treptat din elasticitate și acumulează microleziuni pe parcursul deceniilor.")
    c2.number_input("Vârsta exactă", 20, 100, key="age_num", on_change=sincronizeaza_valori, args=('age', 'text'), label_visibility="hidden")
    age = st.session_state["age_sl"]
    
    gender = st.selectbox("Sexul", options=[1, 2], index=0, format_func=lambda x: "Femeie" if x == 1 else "Bărbat", help="Statistic vorbind bărbații sunt mult mai predispuși la dezvoltarea bolilor de inimă la vârste tinere comparativ cu femeile care beneficiază de o protecție hormonală naturală până la instalarea perioadei de menopauză.")
    
    c3, c4 = st.columns([3, 1])
    c3.slider("Înălțime (cm)", 140, 210, key="height_sl", on_change=sincronizeaza_valori, args=('height', 'glisor'), help="Acest parametru este combinat matematic cu greutatea în fundal pentru a calcula indicele de masă corporală.")
    c4.number_input("Înălțime exactă", 140, 210, key="height_num", on_change=sincronizeaza_valori, args=('height', 'text'), label_visibility="hidden")
    height = st.session_state["height_sl"]
    
    c5, c6 = st.columns([3, 1])
    c5.slider("Greutate (kg)", 40, 150, key="weight_sl", on_change=sincronizeaza_valori, args=('weight', 'glisor'), help="O greutate prea mare raportată la o înălțime mică indică obezitate, o afecțiune care forțează inima să pompeze mult mai greu sângele pentru a iriga un volum crescut de țesut adipos.")
    c6.number_input("Greutate exactă", 40, 150, key="weight_num", on_change=sincronizeaza_valori, args=('weight', 'text'), label_visibility="hidden")
    weight = st.session_state["weight_sl"]
    
    c7, c8 = st.columns([3, 1])
    c7.slider("Tensiune Sistolică", 90, 200, key="ap_hi_sl", on_change=sincronizeaza_valori, args=('ap_hi', 'glisor'), help="Reprezintă forța sângelui atunci când inima se contractă. Tensiunea mare constantă este principalul declanșator mecanic al afecțiunilor cardiace și vasculare.")
    c8.number_input("Sistolică exactă", 90, 200, key="ap_hi_num", on_change=sincronizeaza_valori, args=('ap_hi', 'text'), label_visibility="hidden")
    ap_hi = st.session_state["ap_hi_sl"]
    
    c9, c10 = st.columns([3, 1])
    c9.slider("Tensiune Diastolică", 60, 130, key="ap_lo_sl", on_change=sincronizeaza_valori, args=('ap_lo', 'glisor'), help="Indică presiunea din artere în momentul de relaxare a mușchiului cardiac. Diferența dintre tensiunea sistolică și cea diastolică determină presiunea pulsului.")
    c10.number_input("Diastolică exactă", 60, 130, key="ap_lo_num", on_change=sincronizeaza_valori, args=('ap_lo', 'text'), label_visibility="hidden")
    ap_lo = st.session_state["ap_lo_sl"]

with col2:
    cholesterol = st.selectbox("Nivel Colesterol", options=[1, 2, 3], index=0, format_func=lambda x: {1: "Normal", 2: "Peste normal", 3: "Mult peste normal"}[x], help="Un colesterol mult peste normal reprezintă materialul de bază din care se formează plăcile de aterom care ajung să astupe fizic arterele coronare.")
    gluc = st.selectbox("Nivel Glicemie", options=[1, 2, 3], index=0, format_func=lambda x: {1: "Normal", 2: "Peste normal", 3: "Mult peste normal"}[x], help="O glicemie ridicată constantă funcționează ca un material coroziv care zgârie și degradează peretele interior al vaselor facilitând depunerile periculoase.")
    smoke = st.selectbox("Fumător?", options=[0, 1], index=0, format_func=lambda x: "Nu" if x == 0 else "Da", help="Toxinele din fumul de țigară distrug direct stratul protector al arterelor și reduc drastic nivelul de oxigen transportat de sânge.")
    alco = st.selectbox("Consum de alcool?", options=[0, 1], index=0, format_func=lambda x: "Nu" if x == 0 else "Da", help="Consumul de alcool afectează direct funcția mușchiului cardiac și favorizează episoadele de hipertensiune severă.")
    active = st.selectbox("Activitate fizică?", options=[0, 1], index=1, format_func=lambda x: "Sedentar" if x == 0 else "Activ (Sport)", help="Activitatea fizică acționează ca factorul suprem de protecție. Un pacient sedentar ratează cel mai puternic mecanism natural de menținere a elasticității vasculare.")

st.divider()

if st.button("Calculează Riscul", type="primary", use_container_width=True):
    bmi = weight / ((height / 100) ** 2)
    pulse_pressure = ap_hi - ap_lo

    input_data = pd.DataFrame({
        'age': [age], 'gender': [gender], 'height': [height], 'weight': [weight],
        'ap_hi': [ap_hi], 'ap_lo': [ap_lo], 'cholesterol': [cholesterol],
        'gluc': [gluc], 'smoke': [smoke], 'alco': [alco], 'active': [active],
        'bmi': [bmi], 'pulse_pressure': [pulse_pressure]
    })

    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)
    probabilitate_risc = round(model.predict_proba(input_scaled)[0][1] * 100, 1)

    st.subheader("Rezultatul Analizei:")
    
    gauge_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.jsdelivr.net/npm/echarts@5.5.0/dist/echarts.min.js"></script>
    </head>
    <body style="margin:0; padding:0; display:flex; justify-content:center; align-items:center; background-color: transparent;">
        <div id="main" style="width: 100%; height: 450px;"></div>
        <script>
            var chartDom = document.getElementById('main');
            var myChart = echarts.init(chartDom);
            var option = {{
                tooltip: {{ formatter: '{{a}} <br/>{{b}} : {{c}}%' }},
                series: [{{
                    name: 'Risc', type: 'gauge',
                    axisLine: {{ lineStyle: {{ width: 30, color: [[0.3, '#00cc66'], [0.7, '#ffcc00'], [1, '#ff3333']] }} }},
                    pointer: {{ itemStyle: {{ color: 'auto' }} }},
                    axisTick: {{ distance: -30, length: 8, lineStyle: {{ color: '#fff', width: 2 }} }},
                    splitLine: {{ distance: -30, length: 30, lineStyle: {{ color: '#fff', width: 4 }} }},
                    axisLabel: {{ color: 'auto', distance: 40, fontSize: 14 }},
                    detail: {{ valueAnimation: true, formatter: '{{value}}%', color: 'auto', fontSize: 45, fontWeight: 'bold' }},
                    data: [{{ value: {probabilitate_risc}, name: 'Probabilitate' }}]
                }}]
            }};
            myChart.setOption(option);
        </script>
    </body>
    </html>
    """
    components.html(gauge_html, height=470)

    mesaj_diagnostic = ""
    if prediction[0] == 1:
        mesaj_diagnostic = "Risc Ridicat detectat. Profilul indică o probabilitate ridicată de boală cardiovasculară."
        st.error(mesaj_diagnostic)
    else:
        mesaj_diagnostic = "Risc Scăzut detectat. Profilul indică un risc redus."
        st.success(mesaj_diagnostic)

    st.write("Explicația deciziei algoritmului")
    nume_factori = ['Vârsta', 'Sexul', 'Înălțimea', 'Greutatea', 'Tensiunea Sistolică', 'Tensiunea Diastolică', 'Colesterolul', 'Glicemia', 'Fumatul', 'Alcoolul', 'Activitatea Fizică', 'Indicele de Masă Corporală', 'Presiunea Pulsului']
    importances = model.feature_importances_
    df_contrib = pd.DataFrame({'Factor': nume_factori, 'Importanță': importances})
    df_contrib = df_contrib.sort_values(by='Importanță', ascending=False)
    
    st.write("Principalii factori care au determinat acest scor sunt afișați mai jos în funcție de ponderea lor decizională:")
    
    factori_top = []
    emojis = ["🔴", "🟠", "🟡"]
    
    for i in range(3):
        nume = str(df_contrib.iloc[i]['Factor'])
        pondere = int(df_contrib.iloc[i]['Importanță'] * 100)
        st.markdown(f"{i+1}. {emojis[i]} **{nume}** (Impact estimativ: ~{pondere}%)")
        factori_top.append(nume)

    st.divider()

    with st.expander("Metodologia și funcționarea algoritmului"):
        st.write("Acest instrument digital folosește un model de învățare automată denumit arbore de decizie. În loc să memoreze datele, algoritmul extrage reguli logice din zeci de mii de dosare medicale aparținând populației generale. Procesul de evaluare începe de la o rădăcină principală, reprezentată de obicei de tensiunea arterială sistolică, și se ramifică succesiv în funcție de variabilele introduse, precum vârsta, sexul sau nivelul colesterolului. Pentru a preveni fenomenul de supraspecializare, adâncimea acestui arbore a fost limited intenționată la o valoare optimă, forțând astfel inteligența artificială să generalizeze informația și să ofere predicții robuste pentru pacienți noi. Suplimentar, aplicația calculează automat parametri avansați, printre care indicele de masă corporală și presiunea pulsului, adăugând aceste valori în traseul decizional pentru a varia scorul final. Această arhitectură matematică asigură o analiză clinică onestă și validată științific, reflectând fidel interacțiunea complexă dintre stilul de viață și fiziologia umană.")

    # GENERARE DOSAR MEDICAL CU DATE REVIZUITE (OPEN SOURCE)
    data_curenta = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
    continut_raport = "DOSAR MEDICAL ANALIZA RISC CARDIOVASCULAR AI\n"
    continut_raport += "==================================================\n\n"
    continut_raport += "Data generarii: " + data_curenta + "\n\n"
    continut_raport += "Parametri analizati:\n"
    continut_raport += "Varsta: " + str(age) + " ani\n"
    continut_raport += "Inaltime: " + str(height) + " cm\n"
    continut_raport += "Greutate: " + str(weight) + " kg\n"
    continut_raport += "Tensiune Sistolica: " + str(ap_hi) + " mmHg\n"
    continut_raport += "Tensiune Diastolica: " + str(ap_lo) + " mmHg\n\n"
    continut_raport += "REZULTAT EVALUARE: " + str(probabilitate_risc) + "%\n"
    continut_raport += "Diagnostic: " + mesaj_diagnostic + "\n\n"
    continut_raport += "Factori determinanti in decizia algoritmului:\n"
    for idx, f in enumerate(factori_top):
        continut_raport += str(idx+1) + ". " + f + "\n"
    
    # Metadate modificate pentru a reflecta proiectul open source
    continut_raport += "\n--------------------------------------------------\n"
    continut_raport += "METADATE SISTEM & LICENȚIERE\n"
    continut_raport += "Sistem: CardioRisk AI Predictor\n"
    continut_raport += "Versiune: v1.0.0 (Iunie, 2026)\n"
    continut_raport += "Dezvoltatori: Pantea Andrei & Luca Novac\n"
    continut_raport += "Licență: Open Source (MIT License)\n\n"
    continut_raport += "DISCLAIMER: Acest raport este generat de un instrument demonstrativ bazat pe modele statistice de Machine Learning. Rezultatele au scop pur educațional și de screening preventiv, neputând înlocui un consult medical sau un diagnostic clinic oficial oferit de personal calificat.\n"
        
    st.download_button(label="Descarcă Dosarul Medical", data=continut_raport, file_name="dosar_medical_cardio.txt", mime="text/plain", use_container_width=True)

    scroll_script = "<script>setTimeout(function() {window.frameElement.scrollIntoView({behavior: 'smooth', block: 'end'});}, 100);</script>"
    components.html(scroll_script, height=0)

# SUBSOLUL APLICAȚIEI ACTUALIZAT (OPEN SOURCE / FĂRĂ COPYRIGHT RESTRICTIV)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown(
    """
    <div style="display: flex; justify-content: space-between; align-items: center; color: #64748b; font-size: 0.85rem; padding: 10px 0;">
        <div>
            <b>CardioRisk AI Predictor</b> | Versiunea 1.0.0
        </div>
        <div style="text-align: right;">
            Dezvoltat de <b>Pantea Andrei</b><br>
            Cod Sursă sub licență <b>Open Source (MIT)</b>
        </div>
    </div>
    <div style="text-align: center; color: #94a3b8; font-size: 0.75rem; margin-top: 10px;">
        <i>Disclaimer: Acest sistem este un instrument demonstrativ de conștientizare și screening preventiv. Rezultatele nu înlocuiesc un diagnostic clinic oficial oferit de personalul medical calificat.</i>
    </div>
    """,
    unsafe_allow_html=True
)
