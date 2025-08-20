#!/bin/bash
# This script creates a payload file for the specified target.
# Usage: ./create_payload.sh <name_of_script.py>

# Nom du script Python à convertir
SCRIPT_NAME=$1

# Vérifier si le script Python existe
if [ ! -f "$SCRIPT_NAME" ]; then
    echo "Le fichier $SCRIPT_NAME n'existe pas."
    exit 1
fi

# Exécuter PyInstaller pour créer l'exécutable
pyinstaller --onefile "$SCRIPT_NAME" --distpath dist --workpath build --name "opcua_cli" --clean $2

# Vérifier si PyInstaller a réussi
if [ $? -eq 0 ]; then
    echo "PyInstaller a réussi à créer l'exécutable."

    # Supprimer le répertoire build
    rm -rf build
    echo "Le répertoire build a été supprimé."
else
    echo "PyInstaller a échoué."
    exit 1
fi

# Déplace l'exécutable dans le répertoire payload
if [ -d "dist" ]; then
    mv -u dist/opcua_cli ../../payloads/opcua_cli
    echo "L'exécutable a été déplacé dans le répertoire payload."
else
    echo "Le répertoire dist n'existe pas."
    exit 1
fi
# Nettoyer le répertoire dist
rm -rf dist
echo "Le répertoire dist a été nettoyé."

