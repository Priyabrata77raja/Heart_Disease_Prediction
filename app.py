from datetime import datetime
from pathlib import Path
import pickle, uuid, re, json, os, urllib.parse, urllib.request
import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"
MODEL_PATH = BASE_DIR / "heart_model.pkl"
HISTORY_PATH = BASE_DIR / "prediction_history.csv"
CONTACTS_PATH = BASE_DIR / "saved_contacts.csv"
CONTACT_EMAIL = "Priya07@heartcare.in"  # Replace with your contact details
CONTACT_PHONE = "+91 82807 87920"
CONTACT_LOCATION = "Bhubaneswar, Odisha, India"
HISTORY_COLUMNS = ["PredictionID","Date","Age","Sex","ChestPainType","RestingBP","Cholesterol","FastingBS","RestingECG","MaxHR","ExerciseAngina","Oldpeak","ST_Slope","Prediction","Probability"]
CONTACT_COLUMNS = ["Date","Name","Email","Phone","Note"]

st.set_page_config(page_title="HeartCare | Predict. Prevent. Live Better.", page_icon="❤️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
:root{--teal:#0799A8;--dark:#07566B;--light:#E4F7FA;--ink:#102A43;--muted:#627D98;--border:#CFE8EF;--red:#F23B4B}
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{background:linear-gradient(135deg,#F4FBFD,#E8F7FA);color:var(--ink)}
header[data-testid="stHeader"]{background:transparent}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#063B50,#07566B);border-right:1px solid #15576A}
[data-testid="stSidebar"] *{color:#F5FCFF}
.brand{font-size:27px;font-weight:800;letter-spacing:-1px;padding-top:8px}.brand span{color:#31C4CE}
.brand-sub{font-size:12px;color:#c7edf2;margin-bottom:18px}
[data-testid="stSidebar"] [data-testid="stRadio"] label{border-radius:10px;padding:10px 12px;margin:3px 0;font-weight:600}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:#155e73}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){background:linear-gradient(90deg,#F23B4B,#D91E42)}
[data-testid="stSidebar"] [data-testid="stRadio"] label>div:first-child{display:flex}
.hero,.panel,.feature-card{background:white;border:1px solid var(--border);border-radius:18px;padding:22px;box-shadow:0 7px 22px #0799a814;margin-bottom:14px}
.hero{background:linear-gradient(115deg,#fff,#d9f5f8);padding:30px}
.eyebrow{color:var(--teal);font-size:11px;font-weight:800;letter-spacing:2px;text-transform:uppercase}
.hero-title{font-size:clamp(38px,4vw,58px);font-weight:800;line-height:1.05;margin:10px 0;color:var(--ink)}.hero-title span{color:var(--teal)}
.hero-sub{font-size:20px;font-weight:600}.muted,.page-subtitle{color:var(--muted);line-height:1.7}
.page-title{font-size:30px;font-weight:800;color:var(--ink);margin-bottom:3px}.page-subtitle{font-size:13px;margin-bottom:22px}
.feature-card{min-height:112px}.feature-icon{font-size:28px}.feature-card h4{margin:4px 0 6px;color:var(--ink)}.feature-card p{font-size:13px;color:var(--muted);line-height:1.6;margin:0}
.food-emoji{height:155px;display:flex;align-items:center;justify-content:center;font-size:65px;background:var(--light);border-radius:12px;margin-bottom:8px}.food-switch{display:flex;gap:12px;margin:10px 0 20px}.advice-hero{background:linear-gradient(115deg,#fff,#d9f5f8);border:1px solid var(--border);border-radius:18px;padding:18px;margin-bottom:18px}.advice-card{background:#fff;border:1px solid var(--border);border-radius:16px;padding:20px;height:100%;box-shadow:0 7px 22px #0799a814}.advice-card h4{color:var(--ink);margin:4px 0 8px}.advice-icon{font-size:27px}
.tag{display:inline-block;background:var(--light);color:var(--dark);font-size:11px;font-weight:700;padding:3px 10px;border-radius:20px}
.stButton>button,.stFormSubmitButton>button,.stDownloadButton>button{border-radius:10px;min-height:43px;font-weight:700;background:linear-gradient(90deg,#F23B4B,#D91E42);color:white;border:0}
.stButton>button:hover,.stFormSubmitButton>button:hover,.stDownloadButton>button:hover{color:white;box-shadow:0 6px 18px #f23b4b40;transform:translateY(-1px)}
div[data-testid="stMetric"]{background:white;border:1px solid var(--border);padding:15px;border-radius:14px}
div[data-testid="stExpander"]{background:white;border-radius:12px}hr{border-color:var(--border)}
</style>
""", unsafe_allow_html=True)

def asset(name):
    for ext in (".png",".jpg",".jpeg",".webp",".svg"):
        p=ASSETS/f"{name}{ext}"
        if p.exists(): return p
    return None

def show_asset(name, emoji="❤️"):
    p=asset(name)
    if p: st.image(str(p),use_container_width=True)
    else: st.markdown(f'<div class="food-emoji">{emoji}</div>',unsafe_allow_html=True)

@st.cache_resource
def load_model():
    if not MODEL_PATH.exists(): return None
    with open(MODEL_PATH,"rb") as f: return pickle.load(f)

def load_history():
    if HISTORY_PATH.exists():
        try:
            d=pd.read_csv(HISTORY_PATH)
            for c in HISTORY_COLUMNS:
                if c not in d.columns: d[c]=None
            return d[HISTORY_COLUMNS]
        except Exception: pass
    return pd.DataFrame(columns=HISTORY_COLUMNS)

def save_prediction(row):
    d=load_history(); new=pd.DataFrame([row],columns=HISTORY_COLUMNS)
    (new if d.empty else pd.concat([d,new],ignore_index=True)).to_csv(HISTORY_PATH,index=False)

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_food_image(query):
    """Fetch a food image using Pexels when configured, then Wikimedia Commons."""
    try:
        api_key = st.secrets.get("PEXELS_API_KEY", "")
    except Exception:
        api_key = ""
    api_key = api_key or os.getenv("PEXELS_API_KEY", "")
    if api_key:
        try:
            url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
                {"query": query + " food", "per_page": 1, "orientation": "landscape"}
            )
            req = urllib.request.Request(url, headers={"Authorization": api_key, "User-Agent": "HeartCare/1.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                photos = json.loads(response.read().decode("utf-8")).get("photos", [])
            if photos:
                return photos[0].get("src", {}).get("medium")
        except Exception:
            pass
    try:
        params = urllib.parse.urlencode({
            "action": "query", "generator": "search", "gsrsearch": f'filetype:bitmap "{query}" food',
            "gsrnamespace": 6, "gsrlimit": 5, "prop": "imageinfo", "iiprop": "url",
            "iiurlwidth": 640, "format": "json", "origin": "*",
        })
        req = urllib.request.Request(
            "https://commons.wikimedia.org/w/api.php?" + params,
            headers={"User-Agent": "HeartCare/1.0 (food image lookup)"},
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            pages = json.loads(response.read().decode("utf-8")).get("query", {}).get("pages", {})
        for item in pages.values():
            infos = item.get("imageinfo", [])
            if infos:
                return infos[0].get("thumburl") or infos[0].get("url")
    except Exception:
        pass
    return None

def go_to(page): st.session_state["page"]=page

PAGES=["Home","Heart Disease Prediction","Heart-Healthy Food","Doctor Advice","Contact & Emergency","Healthy Lifestyle","Health Dashboard"]
if "page" not in st.session_state: st.session_state["page"]="Home"
with st.sidebar:
    st.markdown('<div class="brand">❤️ Heart<span>Care</span></div>',unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Predict · Prevent · Live Better</div>',unsafe_allow_html=True)
    st.radio("NAVIGATION",PAGES,key="page",label_visibility="collapsed")
    st.markdown("---"); st.markdown("### ❤️ Better choices"); st.caption("Small steps today. A healthier tomorrow.")
page=st.session_state["page"]

if page=="Home":
    a,b=st.columns([1.15,1],gap="large")
    with a:
        st.markdown('<div class="hero"><div class="eyebrow">Heart health solution Model</div><div class="hero-title">Heart<span>Care</span></div><div class="hero-sub">Predict · Prevent · Live Better</div><p class="muted">Your heart works for you every second. Explore an educational machine-learning prediction project, heart-friendly food suggestions, and practical lifestyle guidance.</p></div>',unsafe_allow_html=True)
        x,y=st.columns(2)
        with x: st.button("❤️ Start Prediction",use_container_width=True,on_click=go_to,args=("Heart Disease Prediction",))
        with y: st.button("Explore Features →",use_container_width=True,on_click=go_to,args=("Heart-Healthy Food",))
    with b: show_asset("heart_hero","❤️")
    st.write("")
    features=[("🧠","Early Detection","Machine-learning model demonstration."),("🩺","Health Guidance","General educational information."),("🌿","Healthy Living","Practical everyday habits."),("💙","Track Results","Review saved model outputs.")]
    cols=st.columns(4)
    for col,(ico,title,desc) in zip(cols,features):
        with col: st.markdown(f'<div class="feature-card"><div class="feature-icon">{ico}</div><h4>{title}</h4><p>{desc}</p></div>',unsafe_allow_html=True)
    st.markdown("### Explore HeartCare")
    for row in [[("❤️","Heart Disease Prediction","Enter the clinical inputs.","Heart Disease Prediction"),("🥗","Heart-Healthy Food","Browse food suggestions.","Heart-Healthy Food")],[("🩺","Doctor Advice","General health guidance.","Doctor Advice"),("📊","Health Dashboard","Review prediction history.","Health Dashboard")]]:
        cols=st.columns(2)
        for col,(ico,title,desc,target) in zip(cols,row):
            with col:
                with st.container(border=True):
                    st.markdown(f"### {ico} {title}"); st.caption(desc)
                    st.button(f"Open {title} →",key=f"home_{target}",use_container_width=True,on_click=go_to,args=(target,))
    st.info("For severe chest pain, difficulty breathing, fainting, or other emergency symptoms, seek immediate medical care. India emergency number: 112.")

elif page=="Heart Disease Prediction":
    st.markdown('<div class="page-title">❤️ Heart Disease Prediction</div><div class="page-subtitle">Enter clinical inputs expected by your saved model. Successful results are stored in the dashboard.</div>',unsafe_allow_html=True)
    try: model=load_model()
    except Exception as e: model=None; st.error(f"Could not load model: {e}")
    if model is None: st.warning("heart_model.pkl was not found. Copy your trained model beside app.py.")
    else:
        with st.form("prediction_form"):
            st.markdown("### Patient Information"); c1,c2,c3=st.columns(3)
            with c1:
                age=st.number_input("Age",1,120,45); sex=st.selectbox("Sex",["M","F"]); chest=st.selectbox("Chest Pain Type",["ATA","NAP","ASY","TA"]); bp=st.number_input("Resting Blood Pressure",0,300,120)
            with c2:
                chol=st.number_input("Cholesterol (mg/dL)",0,1000,200); fasting=st.selectbox("Fasting Blood Sugar > 120 mg/dL",[0,1]); ecg=st.selectbox("Resting ECG",["Normal","ST","LVH"]); maxhr=st.number_input("Maximum Heart Rate",0,250,150)
            with c3:
                angina=st.selectbox("Exercise-Induced Angina",["N","Y"]); oldpeak=st.number_input("ST Depression (Oldpeak)",-5.0,10.0,0.0,step=.1); slope=st.selectbox("ST Slope",["Up","Flat","Down"])
            submit=st.form_submit_button("🔍 Predict Now",use_container_width=True)
        if submit:
            if bp==0 or chol==0: st.warning("Please check the blood pressure and cholesterol values.")
            else:
                inputs=pd.DataFrame([{"Age":age,"Sex":sex,"ChestPainType":chest,"RestingBP":bp,"Cholesterol":chol,"FastingBS":fasting,"RestingECG":ecg,"MaxHR":maxhr,"ExerciseAngina":angina,"Oldpeak":oldpeak,"ST_Slope":slope}])
                try:
                    pred=int(model.predict(inputs)[0]); prob=None
                    if hasattr(model,"predict_proba"):
                        probs=model.predict_proba(inputs)[0]; classes=list(getattr(model,"classes_",range(len(probs))))
                        if 1 in classes: prob=float(probs[classes.index(1)])
                    st.markdown("### Prediction Result")
                    if pred==1: st.error("The model predicts the positive class for heart disease. This is not a diagnosis.")
                    else: st.success("The model predicts the negative class. This does not rule out disease or replace medical evaluation.")
                    if prob is not None: st.metric("Estimated positive-class probability",f"{prob:.1%}")
                    row={"PredictionID":str(uuid.uuid4()),"Date":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),**inputs.iloc[0].to_dict(),"Prediction":pred,"Probability":round(prob,4) if prob is not None else None}
                    save_prediction(row); st.success("Saved to Health Dashboard.")
                    st.button("📊 Open Health Dashboard",on_click=go_to,args=("Health Dashboard",))
                    with st.expander("View submitted inputs"): st.dataframe(inputs,use_container_width=True,hide_index=True)
                except Exception as e:
                    st.error("Model could not process the inputs. Ensure your saved model includes the preprocessing used during training.")
                    st.code(str(e))
    st.caption("Educational project only. Not a clinically validated diagnostic tool.")

elif page=="Heart-Healthy Food":
    st.markdown('<div class="page-title">🥗 Heart-Healthy Food</div><div class="page-subtitle">Choose balanced, minimally processed foods. Individual needs vary.</div>',unsafe_allow_html=True)
    if "food_preference" not in st.session_state: st.session_state["food_preference"]="Vegetarian"
    if "food_category" not in st.session_state: st.session_state["food_category"]="All"
    def set_food_preference(value):
        st.session_state["food_preference"]=value
        st.session_state["food_category"]="All"
    st.markdown("**Food preference**")
    vcol,ncol=st.columns(2)
    with vcol:
        st.button("🥬  Vegetarian",key="food_veg_button",use_container_width=True,type="primary" if st.session_state["food_preference"]=="Vegetarian" else "secondary",on_click=set_food_preference,args=("Vegetarian",))
    with ncol:
        st.button("🍗  Non-Vegetarian",key="food_nonveg_button",use_container_width=True,type="primary" if st.session_state["food_preference"]=="Non-Vegetarian" else "secondary",on_click=set_food_preference,args=("Non-Vegetarian",))
    pref=st.session_state["food_preference"]
    foods=[
        # ---- Vegetarian
        ("apple","🍎","Apple","Fruits","veg","Fibre-rich fruit.","Choose whole fruit rather than sweetened juice; the skin carries much of the fibre."),
        ("orange","🍊","Orange","Fruits","veg","Vitamin C and fibre.","Eat the whole fruit instead of juice to keep the fibre and avoid added sugar."),
        ("pomegranate","🍎","Pomegranate","Fruits","veg","Juicy seeds rich in plant antioxidants.","Choose fresh seeds; if you drink the juice, pick unsweetened and keep portions small."),
        ("berries","🫐","Blueberries","Fruits","veg","Antioxidant-rich berries.","Fresh or frozen without added sugar make an easy snack or breakfast topping."),
        ("broccoli","🥦","Broccoli","Vegetables","veg","Fibre and micronutrients.","Steam or lightly cook with modest salt to keep it crisp and nutritious."),
        ("carrot","🥕","Carrot","Vegetables","veg","Crunchy and fibre-rich.","Eat raw, steamed or in dal and sabzi with little oil."),
        ("tomato","🍅","Tomato","Vegetables","veg","Light, juicy and versatile.","Use fresh in salads or cooked in curries with modest oil and salt."),
        ("vegetables","🥬","Mixed Vegetables","Vegetables","veg","Colourful variety of greens and veggies.","Aim for a variety of colours; steam or lightly cook with modest salt."),
        ("brown_rice","🍚","Brown Rice","Whole Grains","veg","Whole grain with more fibre than white rice.","Keep portions moderate and pair with dal and vegetables."),
        ("whole_grains","🌾","Whole Grains","Whole Grains","veg","Millets, oats and whole-wheat options.","Choose whole grains over refined flour and limit added sugar and salt."),
        ("almonds","🌰","Almonds","Nuts & Seeds","veg","Healthy fats in small portions.","A small handful is enough; avoid heavily salted or fried nuts."),
        ("walnuts","🥜","Walnuts","Nuts & Seeds","veg","Plant-based omega-3 fats.","Choose unsalted walnuts and keep to a small handful."),
        ("rajma","🫘","Rajma (Kidney Beans)","Plant Proteins","veg","Protein and fibre.","Cook with modest oil and salt and pair with brown rice or roti."),
        ("tofu","⬜","Tofu","Plant Proteins","veg","Soy-based plant protein.","Grill, steam or stir-fry with vegetables instead of deep-frying."),
        ("yogurt","🥛","Plain Yogurt","Dairy","veg","Protein and calcium.","Choose plain, unsweetened yogurt; low-fat versions may suit some people."),
        # ---- Non-vegetarian
        ("mackerel","🐟","Mackerel","Fish & Seafood","nonveg","Oily fish with omega-3 fats.","Grill, bake or lightly curry; avoid deep-frying."),
        ("rohu","🐟","Rohu","Fish & Seafood","nonveg","Lean freshwater fish popular in eastern India.","Steam, grill or cook in a light curry with little oil."),
        ("tuna","🐟","Tuna","Fish & Seafood","nonveg","Lean, high-protein fish.","Choose fresh or canned in water rather than oil; vary the fish you eat."),
        ("prawns","🍤","Prawns","Fish & Seafood","nonveg","Low-fat seafood protein.","Steam, grill or sauté lightly with herbs; avoid batter-fried preparations."),
        ("turkey","🦃","Turkey","Poultry & Eggs","nonveg","Lean protein when skinless.","Choose roasted or grilled skinless portions and limit salty gravy and butter.")]
    staples={"Fruits","Vegetables","Whole Grains","Nuts & Seeds"}
    foods=[f for f in foods if f[4]==("veg" if pref=="Vegetarian" else "nonveg")]
    cats=["All"]+list(dict.fromkeys(f[3] for f in foods))
    if st.session_state["food_category"] not in cats: st.session_state["food_category"]="All"
    cat=st.selectbox("Category",cats,key="food_category")
    if cat!="All": foods=[f for f in foods if f[3]==cat]
    for i in range(0,len(foods),3):
        cols=st.columns(3)
        for col,(key,emoji,title,category,diet,short,more) in zip(cols,foods[i:i+3]):
            with col:
                with st.container(border=True):
                    p=asset(key)
                    if p:
                        st.image(str(p),use_container_width=True)
                    else:
                        image_url=fetch_food_image(title)
                        if image_url:
                            st.image(image_url,use_container_width=True,caption="Food photo")
                        else:
                            st.markdown(f'<div class="food-emoji">{emoji}</div>',unsafe_allow_html=True)
                    st.markdown(f"**{title}**"); st.markdown(f'<span class="tag">{category}</span>',unsafe_allow_html=True); st.caption(short)
                    with st.expander("View more"): st.write(more)
    if pref=="Vegetarian":
        st.markdown("### Foods to limit (vegetarian)")
        limits=[("🍟","Deep-fried snacks","Keep samosa, pakora, puri and other fried snacks occasional."),("🧂","Excess salt","Limit pickles, papad, namkeen and salty packaged foods."),("🍬","Sweets & sugary drinks","Limit mithai, sweetened lassi and cold drinks; choose water or unsweetened drinks.")]
    else:
        st.markdown("### Foods to limit (non-vegetarian)")
        limits=[("🌭","Processed meats","Limit sausages, bacon, salami and other cured meats; they are high in salt and saturated fat."),("🥩","Fatty red meat & skin","Keep fatty red meat and chicken or turkey skin occasional; choose lean, skinless cuts."),("🍗","Fried foods & rich gravies","Avoid deep-fried fish or chicken and heavy oil or cream gravies; grill, bake or steam instead.")]
    a,b,c=st.columns(3)
    for col,(ico,title,desc) in zip((a,b,c),limits):
        with col: st.markdown(f'<div class="feature-card"><div class="feature-icon">{ico}</div><h4>{title}</h4><p>{desc}</p></div>',unsafe_allow_html=True)

elif page=="Doctor Advice":
    st.markdown('<div class="page-title">🩺 Doctor Advice</div><div class="page-subtitle">Practical ways to prepare for a visit and care for your heart, guided by a qualified clinician.</div>',unsafe_allow_html=True)
    left,right=st.columns([0.9,1.3],gap="large")
    with left:
        p=asset("doctor_consultation")
        if p: st.image(str(p),use_container_width=True)
        else: show_asset("doctor","🩺")
    with right:
        st.markdown('<div class="advice-hero"><div class="eyebrow">Your next step</div><h3>Make your appointment count</h3><p class="muted">Bring your questions, recent readings, medication list, and notes about any symptoms. Your clinician can tailor advice to your health history.</p></div>',unsafe_allow_html=True)
        st.info("This page offers general education, not personal medical advice. Follow your clinician’s guidance.")
    tips=[("🩺","Know your numbers","Ask whether you need checks for blood pressure, cholesterol, and blood sugar—and how often to repeat them."),("🏃","Choose safe activity","Discuss a suitable activity level, especially if you have symptoms or a long-term condition."),("🥗","Build balanced meals","Ask how to adapt vegetables, fruit, whole grains, legumes, and protein choices to your needs."),("🚭","Get help to quit tobacco","A healthcare professional can suggest practical support and treatment options."),("😴","Talk about sleep and stress","Share sleep concerns or ongoing stress and ask what support may help.")]
    for i in range(0,len(tips),3):
        cols=st.columns(3)
        for col,(icon,title,desc) in zip(cols,tips[i:i+3]):
            with col: st.markdown(f'<div class="advice-card"><div class="advice-icon">{icon}</div><h4>{title}</h4><p class="muted">{desc}</p></div>',unsafe_allow_html=True)
    st.error("Urgent symptoms? Severe chest pain, difficulty breathing, fainting, or sudden concerning symptoms need urgent medical attention. Call local emergency services.")
elif page=="Contact & Emergency":
    st.markdown('<div class="page-title">📞 Contact & Emergency</div><div class="page-subtitle">Emergency details and optional saved contacts.</div>',unsafe_allow_html=True)
    a,b,c=st.columns(3)
    with a: st.markdown('<div class="panel" style="text-align:center"><div style="font-size:36px">🚑</div><h3>Emergency Helpline (India)</h3><div style="font-size:48px;font-weight:800;color:#F23B4B">112</div><p>Ambulance / medical emergency: 108</p></div>',unsafe_allow_html=True)
    with b: st.markdown(f'<div class="panel"><h3>Contact Us</h3><p>✉️ <b>Email</b><br>{CONTACT_EMAIL}</p><p>☎️ <b>Phone</b><br>{CONTACT_PHONE}</p><p>📍 <b>Location</b><br>{CONTACT_LOCATION}</p></div>',unsafe_allow_html=True)
    with c: st.markdown('<div class="panel"><h3>Important</h3><p>Keep your medication list and allergies available for appointments.</p><p>Never delay emergency treatment to use this app.</p></div>',unsafe_allow_html=True)
    with st.form("contact_form"):
        st.markdown("### Save contact details"); name=st.text_input("Name (optional)"); email=st.text_input("Email"); phone=st.text_input("Phone"); note=st.text_area("Note (optional)")
        save=st.form_submit_button("💾 Save details",use_container_width=True)
    if save:
        digits=re.sub(r"\D","",phone)
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$",email): st.error("Enter a valid email address.")
        elif not 10<=len(digits)<=13: st.error("Enter a valid phone number (10–13 digits).")
        else:
            old=pd.read_csv(CONTACTS_PATH,dtype=str).fillna("") if CONTACTS_PATH.exists() else pd.DataFrame(columns=CONTACT_COLUMNS)
            row={"Date":datetime.now().strftime("%Y-%m-%d %H:%M"),"Name":name,"Email":email,"Phone":phone,"Note":note}
            pd.concat([old,pd.DataFrame([row])],ignore_index=True).to_csv(CONTACTS_PATH,index=False); st.success("Contact saved locally.")
    def delete_contact(idx):
        df=pd.read_csv(CONTACTS_PATH,dtype=str).fillna("")
        if 0<=idx<len(df): df.drop(index=idx).to_csv(CONTACTS_PATH,index=False)
        st.session_state["contact_deleted"]=True
    def delete_all_contacts():
        pd.DataFrame(columns=CONTACT_COLUMNS).to_csv(CONTACTS_PATH,index=False)
        st.session_state["contact_deleted"]=True
    if st.session_state.pop("contact_deleted",False): st.success("Contact deleted.")
    contacts=pd.read_csv(CONTACTS_PATH,dtype=str).fillna("") if CONTACTS_PATH.exists() else pd.DataFrame(columns=CONTACT_COLUMNS)
    if contacts.empty:
        st.info("No saved contacts yet.")
    else:
        st.markdown("### Saved contacts")
        widths=[1.5,1.5,2.4,1.5,1.8,0.9]
        for col,h in zip(st.columns(widths),["Date","Name","Email","Phone","Note",""]): col.markdown(f"**{h}**")
        for idx in reversed(range(len(contacts))):
            r=contacts.iloc[idx]
            cols=st.columns(widths)
            cols[0].write(r["Date"]); cols[1].write(r["Name"]); cols[2].write(r["Email"]); cols[3].write(r["Phone"]); cols[4].write(r["Note"])
            cols[5].button("🗑️ Delete",key=f"del_contact_{idx}",on_click=delete_contact,args=(idx,),help="Delete this contact")
        d1,d2=st.columns([1,1])
        with d1: st.download_button("Download contacts CSV",contacts.to_csv(index=False).encode(),"heartcare_contacts.csv","text/csv")
        with d2: st.button("🗑️ Delete all contacts",key="del_all_contacts",on_click=delete_all_contacts)

elif page=="Healthy Lifestyle":
    st.markdown('<div class="page-title">🏃 Healthy Lifestyle</div><div class="page-subtitle">Small, sustainable habits support overall health.</div>',unsafe_allow_html=True)
    tips=[("🏃","Move daily","Aim for regular physical activity appropriate for your health."),("😴","Sleep well","Many adults need around 7–9 hours of sleep."),("🥗","Eat balanced meals","Choose vegetables, fruits, whole grains, and varied protein sources."),("💧","Stay hydrated","Choose water and limit sugary drinks."),("🚭","Avoid tobacco","Seek support to stop tobacco use."),("🧘","Manage stress","Try breathing exercises, hobbies, and time with supportive people.")]
    for i in range(0,len(tips),3):
        cols=st.columns(3)
        for col,(ico,title,desc) in zip(cols,tips[i:i+3]):
            with col: st.markdown(f'<div class="feature-card"><div class="feature-icon">{ico}</div><h4>{title}</h4><p>{desc}</p></div>',unsafe_allow_html=True)

elif page=="Health Dashboard":
    st.markdown('<div class="page-title">📊 Health Dashboard</div><div class="page-subtitle">Every saved prediction report from this app, with full inputs. Open a report to download or delete it.</div>',unsafe_allow_html=True)

    def delete_report(pid):
        d_=load_history()
        d_=d_[d_["PredictionID"].astype(str)!=str(pid)]
        d_[HISTORY_COLUMNS].to_csv(HISTORY_PATH,index=False)
        st.session_state["flash"]="Report deleted."

    def delete_all_reports():
        pd.DataFrame(columns=HISTORY_COLUMNS).to_csv(HISTORY_PATH,index=False)
        st.session_state["confirm_delete_all_reports"] = False
        st.session_state["flash"]="All reports deleted."

    flash=st.session_state.pop("flash",None)
    if flash: st.success(flash)

    raw=load_history()
    if not raw.empty:   # make sure every saved report has an ID so it can be deleted
        ids=raw["PredictionID"].astype(str).str.strip()
        if (raw["PredictionID"].isna() | ids.isin(["","nan","None"])).any():
            raw["PredictionID"]=[v if (pd.notna(v) and str(v).strip() not in ("","nan","None")) else str(uuid.uuid4()) for v in raw["PredictionID"]]
            raw.to_csv(HISTORY_PATH,index=False)
    hist=raw
    if hist.empty:
        st.info("No predictions saved yet. Run a prediction to see it here.")
        st.button("❤️ Go to Prediction",on_click=go_to,args=("Heart Disease Prediction",))
    else:
        hist=hist.copy()
        hist["Date"]=pd.to_datetime(hist["Date"],errors="coerce")
        for c in ["Prediction","Probability","Age","RestingBP","Cholesterol","FastingBS","MaxHR","Oldpeak"]:
            hist[c]=pd.to_numeric(hist[c],errors="coerce")
        hist["PredictionID"]=hist["PredictionID"].astype(str)
        hist=hist.sort_values("Date",kind="stable",na_position="first").reset_index(drop=True)
        hist["Report"]=hist.index+1
        hist["Label"]=hist["Prediction"].map({1:"Positive class",0:"Negative class"}).fillna("Unknown")
        pos=int((hist["Prediction"]==1).sum()); neg=int((hist["Prediction"]==0).sum()); latest=hist.iloc[-1]
        probs=hist["Probability"].dropna()

        a,b,c,d_,e=st.columns(5)
        a.metric("Total reports",len(hist)); b.metric("Positive class",pos); c.metric("Negative class",neg)
        d_.metric("Average probability",f"{probs.mean():.1%}" if not probs.empty else "N/A")
        e.metric("Latest probability",f"{latest['Probability']:.1%}" if pd.notna(latest["Probability"]) else "N/A")
        when=f"{latest['Date']:%d %b %Y, %H:%M}" if pd.notna(latest["Date"]) else "unknown time"
        if latest["Prediction"]==1: st.error(f"Latest output ({when}): positive class predicted. This is not a diagnosis; please consult a doctor.")
        elif latest["Prediction"]==0: st.success(f"Latest output ({when}): negative class predicted. This does not replace medical evaluation.")
        else: st.info(f"Latest report ({when}) has no valid prediction value.")

        x,y=st.columns(2)
        with x:
            p=hist.dropna(subset=["Probability","Date"])
            if not p.empty:
                fig=px.line(p,x="Date",y="Probability",markers=True,title="Positive-class probability over time",color_discrete_sequence=["#0799A8"]); fig.update_yaxes(tickformat=".0%",range=[0,1]); fig.update_layout(paper_bgcolor="white",plot_bgcolor="white",font_color="#102A43"); st.plotly_chart(fig,use_container_width=True)
            else: st.caption("This model does not provide probability scores.")
        with y:
            counts=pd.DataFrame({"Result":["Negative class","Positive class"],"Count":[neg,pos]}); counts=counts[counts["Count"]>0]
            if not counts.empty:
                fig=px.pie(counts,names="Result",values="Count",hole=.55,title="Result distribution",color="Result",color_discrete_map={"Negative class":"#0799A8","Positive class":"#F23B4B"}); fig.update_layout(paper_bgcolor="white",font_color="#102A43"); st.plotly_chart(fig,use_container_width=True)

        # ---------- all stored predictions (full table)
        st.markdown("### All saved predictions")
        table=hist.drop(columns=["PredictionID","Prediction","Label"]).copy()
        table.insert(1,"Result",hist["Label"])
        table["Date"]=table["Date"].dt.strftime("%Y-%m-%d %H:%M:%S").fillna("—")
        table["Probability"]=table["Probability"].map(lambda v:f"{v:.1%}" if pd.notna(v) else "N/A")
        table=table.rename(columns={"Report":"Report #"})
        table=table[["Report #","Date","Result"]+[c for c in table.columns if c not in ("Report #","Date","Result")]]
        st.dataframe(table.iloc[::-1],use_container_width=True,hide_index=True)
        st.download_button("⬇️ Download all reports (CSV)",load_history().to_csv(index=False).encode(),"heartcare_prediction_history.csv","text/csv",use_container_width=True)

        # ---------- individual reports with delete button
        st.markdown("### Prediction reports")
        f1,f2=st.columns(2)
        with f1: view=st.selectbox("Show results",["All","Positive class","Negative class"],key="rep_filter")
        with f2:
            limit_col, delete_col = st.columns([2,1])
            with limit_col:
                limit=st.selectbox("Reports to show",["Latest 10","Latest 25","All"],key="rep_limit")
            with delete_col:
                st.markdown("<div style='height:28px'></div>",unsafe_allow_html=True)
                st.button("🗑️ Delete All Reports",key="request_delete_all_reports",use_container_width=True,
                          disabled=load_history().empty,
                          on_click=lambda: st.session_state.__setitem__("confirm_delete_all_reports", True))
        if st.session_state.get("confirm_delete_all_reports", False):
            st.warning("This will permanently remove every report in prediction_history.csv.")
            confirm_col,cancel_col=st.columns(2)
            with confirm_col:
                st.button("Confirm deletion",key="confirm_delete_all_reports_btn",type="primary",on_click=delete_all_reports)
            with cancel_col:
                st.button("Cancel",key="cancel_delete_all_reports_btn",on_click=lambda: st.session_state.__setitem__("confirm_delete_all_reports", False))
        shown=hist if view=="All" else hist[hist["Label"]==view]
        shown=shown.iloc[::-1]
        if limit!="All": shown=shown.head(int(limit.split()[1]))
        if shown.empty: st.info("No reports match this filter.")

        def val(r,k,suffix=""):
            v=r[k]
            if pd.isna(v) or str(v)=="": return "—"
            if isinstance(v,float) and k in ("Age","RestingBP","Cholesterol","MaxHR"): v=int(v)
            return f"{v}{suffix}"

        for _,r in shown.iterrows():
            when=f"{r['Date']:%d %b %Y, %H:%M}" if pd.notna(r["Date"]) else "Unknown date"
            prob=f"{r['Probability']:.1%}" if pd.notna(r["Probability"]) else "N/A"
            icon="🔴" if r["Prediction"]==1 else ("🟢" if r["Prediction"]==0 else "⚪")
            pid=r["PredictionID"]
            fields=[("Age",val(r,"Age")),("Sex",val(r,"Sex")),("Chest pain type",val(r,"ChestPainType")),("Resting BP",val(r,"RestingBP"," mmHg")),
                    ("Cholesterol",val(r,"Cholesterol"," mg/dL")),("Fasting BS > 120",{1:"Yes",0:"No"}.get(r["FastingBS"],"—")),("Resting ECG",val(r,"RestingECG")),("Max heart rate",val(r,"MaxHR"," bpm")),
                    ("Exercise angina",{"Y":"Yes","N":"No"}.get(r["ExerciseAngina"],val(r,"ExerciseAngina"))),("Oldpeak",val(r,"Oldpeak")),("ST slope",val(r,"ST_Slope")),("Estimated probability",prob)]
            with st.expander(f"{icon} Report #{r['Report']} · {when} · {r['Label']} · {prob}"):
                if r["Prediction"]==1: st.error("The model predicted the positive class for heart disease. This is not a diagnosis.")
                elif r["Prediction"]==0: st.success("The model predicted the negative class. This does not rule out disease or replace medical evaluation.")
                else: st.info("No valid prediction value was stored for this report.")
                for i in range(0,len(fields),4):
                    cols=st.columns(4)
                    for col,(lab,v) in zip(cols,fields[i:i+4]):
                        with col: st.caption(lab); st.markdown(f"**{v}**")
                st.caption(f"Report ID: {pid}")
                text="HeartCare Prediction Report\n"+"="*28+f"\nReport #: {r['Report']}\nReport ID: {pid}\nDate: {when}\nResult: {r['Label']}\nEstimated probability: {prob}\n\nInputs\n------\n"+"\n".join(f"{lab}: {v}" for lab,v in fields[:-1])+"\n\nEducational project only. This is a model output, not a medical diagnosis.\n"
                b1,b2=st.columns(2)
                with b1: st.download_button("⬇️ Download this report",text.encode(),f"heartcare_report_{r['Report']}.txt","text/plain",key=f"dl_{pid}",use_container_width=True)
                with b2: st.button("🗑️ Delete this report",key=f"del_{pid}",on_click=delete_report,args=(pid,),use_container_width=True)

        st.caption("This dashboard stores model outputs, not verified clinical measurements. Results are not a diagnosis.")



