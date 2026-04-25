import streamlit as st
import time
import random
from pyvis.network import Network
import streamlit.components.v1 as components

#  1. Config
st.set_page_config(layout="wide", page_title="SKADI | Next-Gen Intelligence")

# 2. Advanced CSS 
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    
    /* Стилизация простой подписи в левом верхнем углу */
    .corner-signature {
        position: fixed;
        top: 10px;
        left: 10px;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
        font-weight: 400;
        color: rgba(0, 0, 0, 0.4);
        z-index: 999999;
        pointer-events: none; /* Чтобы не мешала кликам */
    }

    /* Стилизация выпадающего списка внутри XARID */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 8px;
        border: 1px solid #3b82f6;
    }

    .xarid-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 25px; border-radius: 15px 15px 0 0;
        display: flex; align-items: center; color: white;
        border-bottom: 4px solid #3b82f6;
    }

    .portal-card { 
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 0 0 15px 15px; 
        padding: 30px; color: #1a222d; margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    .dossier-card {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(0, 86, 179, 0.1);
        border-radius: 12px; padding: 25px; color: #1a222d;
        position: relative; transition: 0.3s; min-height: 200px;
    }
    .dossier-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    
    .tag-blue { background: #dbeafe; color: #1e40af; font-size: 10px; font-weight: 800; padding: 3px 10px; border-radius: 20px; text-transform: uppercase; }
    
    .evidence-alert { 
        background: #fff5f5; border: 2px dashed #ef4444; 
        padding: 2px 5px; border-radius: 4px; font-weight: bold; color: #b91c1c;
        animation: blinker 1.5s linear infinite;
    }
    @keyframes blinker { 50% { opacity: 0.6; } }

    .verdict-box {
        background: #0f172a; color: #f8fafc; padding: 35px;
        border-radius: 15px; border-right: 10px solid #ef4444;
        margin-top: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }

    .verdict-safe {
        background: #f0fdf4; color: #166534; padding: 35px;
        border-radius: 15px; border-right: 10px solid #22c55e;
        margin-top: 30px;
    }
    
    .metric-val { font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 700; color: #3b82f6; }
    </style>
    
    <div class="corner-signature">Brauser</div>
""", unsafe_allow_html=True)

# 3. База Данных 
if 'case_data' not in st.session_state:
    st.session_state.case_data = {
        "Дело №1: Супружеский Сговор": {
            "id": f"LOT-UZ-{random.randint(100000, 999999)}",
            "date": "24.04.2026", "sum": "4.2 млрд сум",
            "customer": "Министерство Здравоохранения (Андижан)",
            "official": "Назаров Дамир Т.", "win_inn": "301111111", "sub_inn": "302222222",
            "dossiers": {
                "301111111": {"name": "MED-STROY EXPORT", "dir": "Ахмедов С.", "addr": "Ташкент, пр. Навои 10", "rating": "A", "founder": "Ахмедов С."},
                "302222222": {"name": "HEALTH-SERVIS OOO", "dir": "Назарова М.Т.", "addr": "Андижан, ул. Темура 44", "rating": "B", "founder": "Назарова М.Т."}
            },
            "evidence": "Выявлена прямая родственная связь (супруги). Заказчик (Назаров Д.Т.) передал бюджет компании жены.",
            "type": "danger"
        },
        "Дело №2: Техническая Аффилированность": {
            "id": f"LOT-UZ-{random.randint(100000, 999999)}",
            "date": "22.04.2026", "sum": "1.8 млрд сум",
            "customer": "Хокимият г. Самарканд",
            "official": "Каримов А.", "win_inn": "401111111", "sub_inn": "402222222",
            "dossiers": {
                "401111111": {"name": "SAM-BUILD", "dir": "Умаров П.", "addr": "ул. Регистанская 5", "rating": "A", "founder": "Умаров П."},
                "402222222": {"name": "RESERVE-STROY", "dir": "Ботиров К.", "addr": "ул. Регистанская 5 (оф. 2)", "rating": "A", "founder": "Ботиров К."}
            },
            "evidence": "Регистрация в одном здании и использование одной IP-сети. Имитация конкуренции.",
            "type": "warning"
        },
        "Дело №3: Конфликт Учредителей": {
            "id": f"LOT-UZ-{random.randint(100000, 999999)}",
            "date": "20.04.2026", "sum": "3.5 млрд сум",
            "customer": "АО 'Узбекгидроэнерго'",
            "official": "Саидов Р.М.", "win_inn": "501111111", "sub_inn": "502222222",
            "dossiers": {
                "501111111": {"name": "HYDRO-TECH", "dir": "Махмудов Ж.", "addr": "Ташкент, Юнусабад", "rating": "A", "founder": "Бакиров Тимур"},
                "502222222": {"name": "ENERGY-CONSULT", "dir": "Ли И.", "addr": "Ташкент, Чиланзар", "rating": "A", "founder": "Бакиров Тимур"}
            },
            "evidence": "Оба участника тендера имеют одного конечного бенефициара (Бакиров Т.).",
            "type": "danger"
        },
        "Дело №4: Госзакупка": {
            "id": f"LOT-UZ-{random.randint(100000, 999999)}",
            "date": "18.04.2026", "sum": "890 млн сум",
            "customer": "Университет Мировой Экономики",
            "official": "Ганиев Ф.", "win_inn": "601111111", "sub_inn": "602222222",
            "dossiers": {
                "601111111": {"name": "IT-SOLUTIONS", "dir": "Волков А.", "addr": "ул. Мукими 1", "rating": "A", "founder": "Волков А."},
                "602222222": {"name": "SOFT-SERVICE", "dir": "Алимов Д.", "addr": "ул. Шота Руставели 40", "rating": "A", "founder": "Алимов Д."}
            },
            "evidence": "Аффилированности не выявлено. Рыночные условия соблюдены.",
            "type": "safe"
        },
        "Дело №5: Поставка Оборудования": {
            "id": f"LOT-UZ-{random.randint(100000, 999999)}",
            "date": "15.04.2026", "sum": "1.2 млрд сум",
            "customer": "РКБ №1",
            "official": "Тураев Б.", "win_inn": "701111111", "sub_inn": "702222222",
            "dossiers": {
                "701111111": {"name": "MEDICAL-GEAR", "dir": "Ким С.", "addr": "Ташкент, Яшнабад", "rating": "A", "founder": "Ким С."},
                "702222222": {"name": "LOGISTIC-PRO", "dir": "Хасанов М.", "addr": "Бухара, ул. Навои", "rating": "B", "founder": "Хасанов М."}
            },
            "evidence": "Контрагенты независимы. Географическое распределение подтверждено.",
            "type": "safe"
        }
    }

CASES = st.session_state.case_data

st.title("SKADI Intelligence Panel")

tab1, tab2 = st.tabs(["XARID.UZ", "SKADI AI"])

# Вкладка 1: Данные портала 
with tab1:
    st.markdown(f"""
        <div class="xarid-header">
            <img src="https://upload.wikimedia.org/wikipedia/commons/7/77/Emblem_of_Uzbekistan.svg" width="60" style="margin-right:20px;">
            <div>
                <h2 style="margin:0; font-size:22px; color:white;">O'ZBEKISTON DAVLAT XARIDLARI</h2>
                <p style="margin:0; opacity:0.8; font-size:12px;">Единый реестр государственных контрактов</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Контейнер для выбора лота внутри визуального блока XARID
    with st.container():
        st.write("")
        selected_name = st.selectbox("📂 Выберите лот из реестра для просмотра деталей:", list(CASES.keys()))
        c = CASES[selected_name]

    st.markdown(f"""
        <div class="portal-card">
            <div style="display:flex; justify-content:space-between;">
                <div>
                    <span style="color:#64748b; font-size:13px;">ЛОТ: <b>{c['id']}</b> | Дата публикации: <b>{c['date']}</b></span>
                    <h3 style="margin:10px 0;">{c['customer']}</h3>
                    <p style="margin:0; color:#475569;">Ответственное лицо (Заказчик): <b>{c['official']}</b></p>
                </div>
                <div style="text-align:right;">
                    <small style="color:#64748b;">Сумма сделки:</small><br>
                    <span style="font-size:24px; font-weight:800; color:#10b981;">{c['sum']}</span>
                </div>
            </div>
            <hr style="opacity:0.1; margin:20px 0;">
            <div style="display:flex; gap:20px;">
                <div style="background:#f1f5f9; padding:15px; border-radius:8px; flex:1; border-left:4px solid #3b82f6;">
                    <small>ИНН победителя тендера</small><br><span class="metric-val">{c['win_inn']}</span>
                </div>
                <div style="background:#f1f5f9; padding:15px; border-radius:8px; flex:1; border-left:4px solid #ef4444;">
                    <small>ИНН Второго участника</small><br><span class="metric-val" style="color:#ef4444;">{c['sub_inn']}</span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.warning("Для  проверки связей скопируйте ИНН и перейдите во вкладку 'SKADI AI'.")

# Вкладка 2: SKADI AI 
with tab2:
    st.markdown("### Центр глубокого сканирования iHamkor")
    col_i1, col_i2 = st.columns(2)
    
    # Поля ввода ПУСТЫЕ
    inn1 = col_i1.text_input("Введите ИНН Победителя:", placeholder="Напр: 301111111")
    inn2 = col_i2.text_input("Введите ИНН Конкурента:", placeholder="Напр: 302222222")
    
    if st.button("расследование"):
        if not inn1 or not inn2:
            st.error("введите оба инн")
        else:
            placeholder = st.empty()
            with placeholder.container():
                st.write("сбор данных из ihamkor...")
                time.sleep(0.8)
                st.write("проверка связей в реестре бенефициаров")
                time.sleep(0.8)
            placeholder.empty() 

            # Используем данные из выбранного в первой вкладке кейса
            if inn1 == c['win_inn'] and inn2 == c['sub_inn']:
                ihamkor_db = c['dossiers']
                st.markdown("#### Результаты проверки iHamkor")
                res_col1, res_col2 = st.columns(2)
                
                for i, (col, target_inn) in enumerate(zip([res_col1, res_col2], [inn1, inn2])):
                    data = ihamkor_db[target_inn]
                    n_alert = 'class="evidence-alert"' if "Назарова" in data['dir'] else ""
                    a_alert = 'class="evidence-alert"' if "Регистанская" in data['addr'] else ""
                    f_alert = 'class="evidence-alert"' if "Бакиров" in data['founder'] and selected_name == "Кейс №3: Конфликт Учредителей (🚨)" else ""

                    col.markdown(f"""
                        <div class="dossier-card">
                            <span class="tag-blue">iHamkor Report</span>
                            <h4 style="margin:5px 0;">{data['name']}</h4>
                            <p style="font-size:14px; color:#475569;">
                                <b>Директор:</b> <span {n_alert}>{data['dir']}</span><br>
                                <b>Учредитель:</b> <span {f_alert}>{data['founder']}</span><br>
                                <b>Адрес:</b> <span {a_alert}>{data['addr']}</span><br>
                                Рейтинг: <b>{data['rating']}</b>
                            </p>
                            <hr style="opacity:0.1;">
                            <small>ИНН: {target_inn}</small>
                        </div>
                    """, unsafe_allow_html=True)

                # Вердикт
                if c['type'] in ["danger", "warning"]:
                    st.markdown(f"""<div class="verdict-box">
                        <h2 style="color:#ef4444; margin:0;"> Заключение: {c['type'].upper()} RISK</h2>
                        <p style="margin-top:15px; font-size:16px;">{c['evidence']}</p>
                    </div>""", unsafe_allow_html=True)
                    
                    # Граф
                    net = Network(height='350px', width='100%', bgcolor='#0f172a', font_color='white')
                    if "Супружеский" in selected_name:
                        net.add_node("Z", label=f"Заказчик\n({c['official']})", color='#3b82f6', size=25)
                        net.add_node("P", label="Победитель", color='#ffffff')
                        net.add_node("S", label="Подрядчик\n(Жена)", color='#ef4444', size=30)
                        net.add_edge("Z", "P"); net.add_edge("P", "S"); net.add_edge("S", "Z", label="СВЯЗЬ (БРАК)", color='#ef4444', width=3)
                    else:
                        net.add_node("F", label="Общий Владелец", color='#ef4444', size=30)
                        net.add_node("C1", label="Компания А", color='#ffffff')
                        net.add_node("C2", label="Компания Б", color='#ffffff')
                        net.add_edge("F", "C1"); net.add_edge("F", "C2")
                    net.save_graph("skadi_graph.html")
                    components.html(open("skadi_graph.html", 'r').read(), height=370)
                else:
                    st.markdown(f"""<div class="verdict-safe">
                        <h2 style="margin:0;"> Нарушений не выявлено</h2>
                        <p style="margin-top:15px;">{c['evidence']}</p>
                    </div>""", unsafe_allow_html=True)
            else:
                st.error("Введенные ИНН не соответствуют данным лота, выбранного на Портале.")
