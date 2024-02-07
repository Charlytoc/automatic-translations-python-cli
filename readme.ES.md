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
python main.py --language [IDIOMA_OBJETIVO] --action [ACCIÓN]
```
- `--language` o `-l`: Especifica el idioma objetivo para la traducción (por defecto es inglés).
- `--action` o `-a`: Define la última acción a realizar (opciones: extract, transcribe, translate, all).

Selecciona un video e idioma, luego comienza el procesamiento.

## Uso de `record.py`
Graba, transcribe y traduce audio en tiempo real:
1. Elige el ID del micrófono para grabar:
   Primero, la aplicación te mostrará los dispositivos disponibles, solo escribe el ID del que quieras usar.
2. Establece el idioma objetivo:
   Luego, se te pedirá que escribas el idioma al que quieres traducir, puede ser cualquier idioma.
3. ¡Después de eso, solo presiona `Enter` para comenzar a grabar y listo!

## Salida
- `main.py`: Audio MP3, transcripción, traducción y audio traducido en `/output`.
- `record.py`: Grabaciones WAV, transcripciones, traducciones y audio traducido en `recording_sessions`.

## Información Adicional
- `.gitignore` excluye `venv` y `output`.
- Los scripts ignoran `.gitkeep` en `/videos`.

Sigue esta guía para un uso eficiente del Proyecto de Traducciones Automáticas.