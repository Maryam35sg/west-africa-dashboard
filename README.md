# 🌍 Tableau de Bord Analytique — Afrique de l'Ouest

## Description
Projet de fin d'année combinant un pipeline ETL Python et un dashboard Power BI
pour analyser les indicateurs socio-économiques de l'Afrique de l'Ouest.

## Structure du projet
west-africa-dashboard/
│
├── data/
│   ├── raw/                  # Données brutes (non modifiées)
│   │   ├── worldbank/        # Données API Banque Mondiale
│   │   ├── undp/             # Données IDH - PNUD
│   │   ├── fao/              # Données sécurité alimentaire
│   │   └── geojson/          # Fichiers cartographiques
│   └── processed/            # Données nettoyées et transformées
│
├── notebooks/                # Jupyter Notebooks d'exploration
├── scripts/                  # Scripts Python ETL
├── reports/                  # Rapports et exports PDF
└── powerbi/                  # Fichier .pbix Power BI
## Stack technique
- **Python** : wbgapi, pandas, requests
- **Stockage** : CSV / SQLite
- **Visualisation** : Power BI Desktop
- **Versioning** : Git / GitHub

## Sources de données
- [Banque Mondiale](https://data.worldbank.org)
- [PNUD - IDH](https://hdr.undp.org/data-center)
- [FAO](https://www.fao.org/faostat)
- [HDX - WFP](https://data.humdata.org)

## Auteur
Maryam Salissou Gomna - Projet de fin d'année | 2025-2026
