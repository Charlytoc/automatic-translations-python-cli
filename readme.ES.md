# Proyecto de Traducciones Automáticas - Guía Completa

## Prerrequisitos
Asegúrate de que Python 3.x esté instalado:
```bash
python --version
```

## Configuración del Entorno
1. Crea y activa un entorno virtual:
```bash
py -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Unix/MacOS
```

## Configuración
1. Duplica `.env.example` a `.env` y añade las credenciales:
```bash
cp .env.example .env
```

## Uso de `main.py`
Coloca los videos en `/videos` y ejecuta:
```bash
python main.py
```
Selecciona un video y un idioma, luego comienza el procesamiento.

## Uso de `record.py`
Graba, transcribe y traduce audio en tiempo real:
1. Elige el ID del micrófono para grabar:
Primero la aplicación te va a mostrar los dispositivos disponibles, tan solo debes escribir el id del que te interesa usar.

2. Establece el idioma objetivo:
Luego te pedirá que escribas el idioma al que quieres traducir, puede ser cualquiera.

3. ¡Luego solo debes presionar `Enter` para empezar a grabar y ya está!

## Salida
- `main.py`: Audio MP3, transcripción, traducción y audio traducido en `/output`.
- `record.py`: Grabaciones WAV, transcripciones, traducciones y audio traducido en `recording_sessions`.

## Información Adicional
- `.gitignore` excluye `venv` y `output`.
- Los scripts ignoran `.gitkeep` en `/videos`.

Sigue esta guía para un uso eficiente del Proyecto de Traducciones Automáticas.