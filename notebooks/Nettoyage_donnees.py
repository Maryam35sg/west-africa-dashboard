# =============================================================
# PROJET : Tableau de Bord Analytique — Afrique de l'Ouest
# FICHIER : Nettoyage_donnees.py
# AUTEUR  : Maryam Salissou Gomna
# DATE    : Juin 2026
# DESC    : Pipeline ETL — Nettoyage et transformation des
#           données brutes en données exploitables pour Power BI
# =============================================================

import pandas as pd
import os

# =============================================================
# CONFIGURATION — Chemins et paramètres
# =============================================================

RAW       = 'C:/Users/hp/Desktop/west-africa-dashboard/data/raw/'
PROCESSED = 'C:/Users/hp/Desktop/west-africa-dashboard/data/processed/'

# 16 pays d'Afrique de l'Ouest — codes standard
pays_aow = [
    'Niger', 'Nigeria', 'Senegal', "Cote d'Ivoire",
    'Ghana', 'Mali', 'Burkina Faso', 'Benin',
    'Togo', 'Guinea', 'Mauritania', 'Gambia',
    'Sierra Leone', 'Liberia', 'Guinea-Bissau', 'Cabo Verde'
]

# Noms exacts utilisés dans les fichiers UNDP
pays_aow_undp = [
    'Niger', 'Nigeria', 'Senegal', "Côte d'Ivoire",
    'Ghana', 'Mali', 'Burkina Faso', 'Benin',
    'Togo', 'Guinea', 'Mauritania', 'Gambia',
    'Sierra Leone', 'Liberia', 'Guinea-Bissau', 'Cabo Verde'
]

print("=" * 60)
print("  PIPELINE ETL — AFRIQUE DE L'OUEST")
print("=" * 60)

# =============================================================
# SOURCE 1 — BANQUE MONDIALE
# Indicateurs : PIB, démographie, pauvreté, éducation,
#               santé, infrastructures, genre
# Période     : 2001 → 2023
# =============================================================

print("\n [1/4] Traitement — Banque Mondiale...")

# Lecture
wb = pd.read_csv(RAW + 'worldbank/wb_data.csv')

# Renommage des colonnes principales
wb = wb.rename(columns={
    'Country Name' : 'Pays',
    'Country Code' : 'Code_Pays',
    'Series Name'  : 'Indicateur',
    'Series Code'  : 'Code_Indicateur'
})

# Suppression colonne vide fantôme
wb = wb.drop(columns=['Unnamed: 29'], errors='ignore')

# Suppression des lignes sans indicateur
wb = wb.dropna(subset=['Indicateur'])

# Identification des colonnes années
colonnes_annees = [
    col for col in wb.columns
    if col not in ['Pays', 'Code_Pays', 'Indicateur', 'Code_Indicateur']
]

# Transformation format large → format long
wb_long = wb.melt(
    id_vars    = ['Pays', 'Code_Pays', 'Indicateur', 'Code_Indicateur'],
    value_vars = colonnes_annees,
    var_name   = 'Annee',
    value_name = 'Valeur'
)

# Nettoyage format année : "2001 [YR2001]" → 2001
wb_long['Annee'] = wb_long['Annee'].str.extract(r'(\d{4})').astype(int)

# Filtrage période 2001 → 2023
wb_long = wb_long[wb_long['Annee'].between(2001, 2023)]

# Conversion des valeurs en numérique
wb_long['Valeur'] = pd.to_numeric(wb_long['Valeur'], errors='coerce')

# Sauvegarde
wb_long.to_csv(PROCESSED + 'wb_clean.csv', index=False, encoding='utf-8-sig')
print(f"   ✅ wb_clean.csv sauvegardé")
print(f"      {wb_long.shape[0]} lignes | {wb_long['Pays'].nunique()} pays | 2001→2023")

# =============================================================
# SOURCE 2 — UNDP (PNUD)
# Indicateurs : IDH, Espérance de vie, Scolarisation, RNB,
#               Inégalité de Genre
# Période     : 2023 (snapshot annuel)
# =============================================================

print("\n [2/4] Traitement — UNDP...")

# --- Fichier 1 : Indice de Développement Humain (IDH) ---
undp_hdi = pd.read_excel(
    RAW + 'undp/Human Development Index and components.xlsx',
    skiprows=8,
    header=None,
    names=[
        'HDI_Rank', 'Pays',
        'HDI_Valeur', 'Note1',
        'Esperance_vie', 'Note2',
        'Annees_scolarisation_attendues', 'Note3',
        'Annees_scolarisation_moyennes', 'Note4',
        'RNB_par_habitant', 'Note5',
        'RNB_moins_HDI_rank', 'Note6',
        'HDI_rank_2022'
    ]
)

# Suppression colonnes notes
undp_hdi = undp_hdi.drop(
    columns=['Note1','Note2','Note3','Note4','Note5','Note6'],
    errors='ignore'
)

# Filtrage lignes valides
undp_hdi = undp_hdi[
    undp_hdi['HDI_Rank'].apply(
        lambda x: str(x).replace('.0','').strip().isdigit()
    )
]

# Nettoyage colonne Pays
undp_hdi['Pays'] = undp_hdi['Pays'].astype(str).str.strip()

# Filtrage pays Afrique de l'Ouest
undp_hdi = undp_hdi[undp_hdi['Pays'].isin(pays_aow_undp)]

# Sauvegarde
undp_hdi.to_csv(PROCESSED + 'undp_hdi_clean.csv', index=False, encoding='utf-8-sig')
print(f"   ✅ undp_hdi_clean.csv sauvegardé")
print(f"      {undp_hdi.shape[0]} pays | {undp_hdi.shape[1]} indicateurs")

# --- Fichier 2 : Indice d'Inégalité de Genre (IIG) ---
undp_gii = pd.read_excel(
    RAW + 'undp/Gender Inequality Index.xlsx',
    skiprows=8,
    header=None,
    names=[
        'HDI_Rank', 'Pays',
        'GII_Valeur', 'Note1',
        'GII_Rank', 'Note2',
        'Mortalite_maternelle', 'Note3',
        'Taux_naissances_adolescentes', 'Note4',
        'Sieges_parlement_femmes_pct', 'Note5',
        'Education_secondaire_femmes_pct', 'Note6',
        'Education_secondaire_hommes_pct', 'Note7',
        'Participation_travail_femmes_pct', 'Note8',
        'Participation_travail_hommes_pct', 'Note9'
    ]
)

# Suppression colonnes notes
undp_gii = undp_gii.drop(
    columns=['Note1','Note2','Note3','Note4',
             'Note5','Note6','Note7','Note8','Note9'],
    errors='ignore'
)

# Filtrage lignes valides
undp_gii = undp_gii[
    undp_gii['HDI_Rank'].apply(
        lambda x: str(x).replace('.0','').strip().isdigit()
    )
]

# Nettoyage colonne Pays
undp_gii['Pays'] = undp_gii['Pays'].astype(str).str.strip()

# Filtrage pays Afrique de l'Ouest
undp_gii = undp_gii[undp_gii['Pays'].isin(pays_aow_undp)]

# Sauvegarde
undp_gii.to_csv(PROCESSED + 'undp_gii_clean.csv', index=False, encoding='utf-8-sig')
print(f"   ✅ undp_gii_clean.csv sauvegardé")
print(f"      {undp_gii.shape[0]} pays | {undp_gii.shape[1]} indicateurs")

# =============================================================
# SOURCE 3 — FAO
# Indicateurs : Sécurité alimentaire, Nutrition,
#               Apport calorique, Sous-alimentation
# Période     : 2001 → 2023
# =============================================================

print("\n [3/4] Traitement — FAO...")

# Lecture
fao = pd.read_csv(
    RAW + 'fao/fao_food_security.csv',
    encoding='latin-1'
)

# Renommage des colonnes
fao = fao.rename(columns={
    'ï»¿Domain Code'   : 'Code_Domaine',
    'Domain'           : 'Domaine',
    'Area Code (M49)'  : 'Code_Pays',
    'Area'             : 'Pays',
    'Element Code'     : 'Code_Element',
    'Element'          : 'Element',
    'Item Code'        : 'Code_Item',
    'Item'             : 'Item',
    'Year Code'        : 'Code_Annee',
    'Year'             : 'Annee',
    'Unit'             : 'Unite',
    'Value'            : 'Valeur',
    'Flag'             : 'Flag',
    'Flag Description' : 'Description_Flag',
    'Note'             : 'Note'
})

# Sélection des colonnes utiles
fao = fao[['Pays', 'Element', 'Item', 'Annee', 'Unite', 'Valeur']]

# Conversion et filtrage des années
fao['Annee'] = pd.to_numeric(fao['Annee'], errors='coerce')
fao = fao.dropna(subset=['Annee'])
fao['Annee'] = fao['Annee'].astype(int)
fao = fao[fao['Annee'].between(2001, 2023)]

# Suppression des lignes sans valeur
fao = fao.dropna(subset=['Valeur'])

# Sauvegarde
fao.to_csv(PROCESSED + 'fao_clean.csv', index=False, encoding='utf-8-sig')
print(f"   ✅ fao_clean.csv sauvegardé")
print(f"      {fao.shape[0]} lignes | {fao['Pays'].nunique()} pays | 2001→2023")

# =============================================================
# RÉSUMÉ FINAL
# =============================================================

print("\n" + "=" * 60)
print("  ✅ PIPELINE ETL TERMINÉ AVEC SUCCÈS !")
print("=" * 60)
print(f"\n Fichiers sauvegardés dans : {PROCESSED}")
print("   ├── wb_clean.csv")
print("   ├── undp_hdi_clean.csv")
print("   ├── undp_gii_clean.csv")
print("   └── fao_clean.csv")
print("\n Données prêtes pour Power BI !")