#!/usr/bin/env python
"""
Script de migration des données du développement vers la production.
Réassigne tous les contenus à l'utilisateur spécifié en production.
"""

import json
import sys

def migrate_data(input_file, output_file, production_user_id):
    """
    Modifie les IDs utilisateur dans le fichier JSON d'export Django.

    Args:
        input_file: Fichier JSON source (dumpdata)
        output_file: Fichier JSON de sortie modifié
        production_user_id: ID de l'utilisateur en production qui deviendra propriétaire
    """

    print(f"📂 Lecture du fichier {input_file}...")
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"📊 {len(data)} enregistrements trouvés")

    # Compteurs
    modified = 0
    models_modified = {}

    # Parcourir tous les enregistrements
    for record in data:
        model = record.get('model', '')
        fields = record.get('fields', {})

        # Champs qui référencent des utilisateurs (à adapter selon vos modèles)
        user_fields = ['auteur', 'organisateur', 'participant', 'user', 'membre']

        for field in user_fields:
            if field in fields and fields[field] is not None:
                old_id = fields[field]
                fields[field] = production_user_id
                modified += 1

                # Compter par modèle
                if model not in models_modified:
                    models_modified[model] = 0
                models_modified[model] += 1

                print(f"  ✏️  {model}: {field} {old_id} → {production_user_id}")

    print(f"\n✅ {modified} références utilisateur modifiées")
    for model, count in models_modified.items():
        print(f"   - {model}: {count}")

    # Sauvegarder le fichier modifié
    print(f"\n💾 Sauvegarde dans {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Migration terminée ! Fichier prêt pour loaddata")
    print(f"\n📋 Prochaines étapes :")
    print(f"   1. Transférer {output_file} vers le VPS")
    print(f"   2. Sur le VPS: python manage.py loaddata {output_file}")

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python migrate_data.py <input.json> <output.json> <production_user_id>")
        print("Exemple: python migrate_data.py data_export.json data_production.json 1")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    production_user_id = int(sys.argv[3])

    migrate_data(input_file, output_file, production_user_id)
