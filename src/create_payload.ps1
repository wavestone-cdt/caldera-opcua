<#
.SYNOPSIS
Ce script PowerShell génère un exécutable avec PyInstaller pour un script Python donné,
puis le place dans le répertoire payloads de ton plugin Caldera.

.EXAMPLE
.\create_payload.ps1 my_script.py
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$ScriptName,

    [string]$ExtraArgs = ""
)

# Vérifier si le script Python existe
if (-Not (Test-Path -Path $ScriptName)) {
    Write-Host "Le fichier $ScriptName n'existe pas."
    exit 1
}

# Exécuter PyInstaller
Write-Host "Exécution de PyInstaller pour créer l'exécutable..."

$pyinstallerCmd = "pyinstaller --onefile `"$ScriptName`" --distpath dist --workpath build --name `opcua_cli` --clean $ExtraArgs"
Write-Host "Commande : $pyinstallerCmd"

Invoke-Expression $pyinstallerCmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "PyInstaller a réussi à créer l'exécutable."

    # Supprimer le répertoire build
    if (Test-Path -Path "build") {
        Remove-Item -Recurse -Force build
        Write-Host "Le répertoire build a été supprimé."
    }
} else {
    Write-Host "PyInstaller a échoué."
    exit 1
}

# Déplacer l'exécutable dans le répertoire payloads
if (Test-Path -Path "dist") {
    $sourcePath = Join-Path -Path "dist" -ChildPath "opcua_cli.exe"
    $destPath = "..\..\payloads\opcua_cli.exe"

    Move-Item -Force -Path $sourcePath -Destination $destPath
    Write-Host "L'exécutable a été déplacé dans le répertoire payloads."
} else {
    Write-Host "Le répertoire dist n'existe pas."
    exit 1
}

# Nettoyer le répertoire dist
if (Test-Path -Path "dist") {
    Remove-Item -Recurse -Force dist
    Write-Host "Le répertoire dist a été nettoyé."
}

Write-Host "✅ Fini !"
