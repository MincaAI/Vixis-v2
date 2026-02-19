#!/usr/bin/env python3
"""
Script de test pour queryCompany.py - Test avec noms de compagnies
"""

import sys
import os
sys.path.append('utils')
from queryCompany import query_company

def test_company(name):
    """Test une entreprise et affiche les résultats"""
    print(f"\n🔍 Test: {name}")
    print("-" * 60)
    
    try:
        result = query_company(name)
        if result and len(result) > 1:  # Plus que juste l'URL
            print(f"✅ SUCCÈS - Données récupérées!")
            print(f"🌐 URL trouvée: {result.get('Main url', 'N/A')}")
            
            # Vérifier les données importantes
            data_found = []
            
            # Objectif de cours
            if result.get('Objectif de cours') and result.get('Objectif de cours') != 'Price data unavailable':
                data_found.append(f"🎯 Objectif: {result['Objectif de cours']}")
            
            # Performances
            for period in ['1 an', '3 ans', '5 ans']:
                if period in result:
                    data_found.append(f"📈 {period}: {result[period]}")
            
            # Dividendes et PER
            for key, value in result.items():
                if 'Dividende' in key or 'PER' in key:
                    data_found.append(f"💰 {key}: {value}")
                    if len(data_found) >= 8:  # Limiter l'affichage
                        break
            
            if data_found:
                print("📊 Données extraites:")
                for data in data_found[:6]:  # Afficher max 6 éléments
                    print(f"   {data}")
                if len(data_found) > 6:
                    print(f"   ... et {len(data_found) - 6} autres données")
            else:
                print("⚠️  URL trouvée mais peu de données extraites")
                
        else:
            print("❌ ÉCHEC - Aucune donnée récupérée")
            if result:
                print(f"   URL: {result.get('Main url', 'Aucune URL')}")
            
    except Exception as e:
        print(f"❌ ERREUR: {str(e)}")

if __name__ == "__main__":
    # Tests avec des NOMS DE COMPAGNIES
    test_cases = [
        "APPLE",           # Apple Inc
        "SANOFI",          # Sanofi (français)
        "NVIDIA",          # Nvidia Corporation
        "MICROSOFT",       # Microsoft Corporation
        "LVMH",            # LVMH (français)
        "TESLA",           # Tesla Inc
        "TOTAL",           # TotalEnergies (français)
        "GOOGLE",          # Alphabet/Google
        "AMAZON",          # Amazon
        "META",            # Meta (Facebook)
    ]
    
    print("🚀 TEST UNIVERSEL - Noms de compagnies → Données Boursorama")
    print("=" * 70)
    print("🎯 Objectif: Vérifier que chaque nom trouve les bonnes données")
    
    success_count = 0
    total_count = len(test_cases)
    
    for test_case in test_cases:
        test_company(test_case)
        # Compter les succès (simple check si on a récupéré des données)
        try:
            result = query_company(test_case)
            if result and len(result) > 1:
                success_count += 1
        except:
            pass
    
    print("\n" + "=" * 70)
    print(f"📊 RÉSULTATS: {success_count}/{total_count} compagnies trouvées")
    print(f"📈 Taux de succès: {(success_count/total_count)*100:.1f}%")
    
    if success_count == total_count:
        print("🎉 PARFAIT! Toutes les compagnies ont été trouvées!")
    elif success_count >= total_count * 0.8:
        print("✅ TRÈS BIEN! La plupart des compagnies fonctionnent")
    else:
        print("⚠️  À améliorer - Plusieurs compagnies ne fonctionnent pas")
