import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Configuration de la page
st.set_page_config(
    page_title="🏠 Prédiction Prix Immobilier Casablanca",
    page_icon="🏠",
    layout="centered"
)

# Fonction pour charger le modèle
@st.cache_resource
def charger_modele():
    try:
        import os
        # Chemin absolu pour être sûr
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'models', 'mon_modele_immobilier.pkl')
        model = joblib.load(model_path)
        st.success("✅ Modèle ML chargé avec succès!")
        return model
    except Exception as e:
        st.error(f"❌ Erreur chargement modèle: {e}")
        return None

# Titre principal
st.title("🏠 Prédicteur de Prix Immobilier - Casablanca")
st.markdown("**Estimez le prix de votre bien immobilier avec notre intelligence artificielle**")

# Sidebar pour les inputs utilisateur
with st.sidebar:
    st.header("📋 Caractéristiques du bien")
    
    surface = st.slider("**Surface (m²)**", min_value=30, max_value=500, value=100, step=10)
    pieces = st.slider("**Nombre de pièces**", min_value=1, max_value=10, value=3)
    chambres = st.slider("**Nombre de chambres**", min_value=1, max_value=8, value=2)
    salles_bain = st.slider("**Salles de bain**", min_value=1, max_value=6, value=1)
    etage = st.slider("**Étage**", min_value=0, max_value=20, value=2)
    
    # Bouton de prédiction
    if st.button("🎯 **Estimer le prix**", type="primary", use_container_width=True):
        st.session_state.prediction = True

# Section principale - PRÉDICTION AVEC VRAI MODÈLE
if 'prediction' in st.session_state and st.session_state.prediction:
    # Charger le modèle
    model = charger_modele()
    
    if model:
        # Préparer les données pour la prédiction
        input_data = [[surface, pieces, chambres, salles_bain, etage]]
        
        # Faire la prédiction avec le vrai modèle ML
        prix_estime = model.predict(input_data)[0]
        
        # Affichage du résultat
        st.success(f"### 💰 Prix estimé: **{prix_estime:,.0f} DH**")
        
        # Détails dans un tableau
        st.subheader("📊 Détails de l'estimation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Surface", f"{surface} m²")
            st.metric("Nombre de pièces", pieces)
            st.metric("Nombre de chambres", chambres)
            
        with col2:
            st.metric("Salles de bain", salles_bain)
            st.metric("Étage", etage)
            st.metric("Prix au m²", f"{prix_estime/surface:,.0f} DH")
            
        st.info("🔍 *Cette estimation utilise un modèle de Machine Learning entraîné sur des données réelles*")
    
    else:
        st.error("🚨 Le modèle n'a pas pu être chargé. Utilisation d'une estimation de base.")
        prix_estime = surface * 12000 + pieces * 50000
        st.warning(f"💰 Estimation de base: **{prix_estime:,.0f} DH**")

# Section informations
with st.expander("ℹ️ **À propos de cette application**"):
    st.write("""
    **Cette application utilise un véritable modèle de Machine Learning (Random Forest) 
    entraîné sur plus de 3,000 propriétés à Casablanca.**
    
    🎯 **Technologies utilisées :**
    - Machine Learning : Random Forest Regressor
    - Framework : Scikit-learn
    - Interface : Streamlit
    - Données : Marché immobilier réel Casablanca
    
    📈 **Avantages :**
    - Prédictions basées sur des patterns réels
    - Apprentissage automatique
    - Mise à jour possible avec nouvelles données
    """)

# Pied de page
st.markdown("---")
st.caption("Projet de Machine Learning End-to-End - Prédiction immobilière © 2024")