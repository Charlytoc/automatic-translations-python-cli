# Proyecto de Traducciones Automáticas - Guía Completa

Si quieres ver un video sobre cómo usar este repositorio, revisa este [video](https://youtu.be/CA7i_kcks-Q?si=klrLJy5_YdZR0HLZ)

## Requisitos Previos
Asegúrate de que Python 3.x esté instalado:
```bash
python --version
```

### FFmpeg
FFmpeg es necesario para el procesamiento de audio y video. Sigue los pasos a continuación para instalarlo:

#### Windows
1. Descarga el ejecutable de FFmpeg desde el [sitio web oficial de FFmpeg](https://ffmpeg.org/download.html).
2. Extrae el archivo zip descargado a una carpeta (por ejemplo, `C:\ffmpeg`).
3. Agrega el directorio `bin` a la variable PATH de tu sistema:
   - Abre el Menú de Inicio, busca "Variables de Entorno" y selecciona "Editar las variables de entorno del sistema".
   - Haz clic en "Variables de Entorno".
   - Bajo "Variables del sistema", encuentra la variable `Path` y haz clic en "Editar".
   - Haz clic en "Nuevo" y agrega la ruta al directorio `bin` (por ejemplo, `C:\ffmpeg\bin`).
   - Haz clic en "Aceptar" para guardar los cambios.

#### Unix/MacOS
1. Instala FFmpeg usando un gestor de paquetes:
   ```bash
   # Para Ubuntu/Debian
   sudo apt update
   sudo apt install ffmpeg

   # Para MacOS usando Homebrew
   brew install ffmpeg
   ```

## Configuración del Entorno
1. Crea y activa un entorno virtual:
```bash
py -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate      # Unix/MacOS
```
2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Configuración
1. Duplica `.env.example` a `.env` y agrega las credenciales:
```bash
cp .env.example .env
```

## Usando `main.py`
Coloca los videos en `/videos` y ejecuta:
```bash
python main.py --language [IDIOMA_OBJETIVO] --action [ACCIÓN]
```
- `--language` o `-l`: Especifica el idioma objetivo para la traducción (por defecto es inglés).
- `--action` o `-a`: Define la última acción a realizar (opciones: extract, transcribe, translate, all).

### Explicación de Acciones
- Extract: Extrae el audio del video fuente.
- Transcribe: Transcribe el video fuente en formato vtt o json.
- Translate: Traduce la transcripción al idioma objetivo.
- All: Realiza todas las acciones anteriores y genera una nueva versión del video en el idioma objetivo usando ElevenLabs (debes tener la API KEY).

## Usando `record.py`
Graba, transcribe y traduce audio en tiempo real:
1. Elige el ID del micrófono para grabar:
   Primero, la aplicación te mostrará los dispositivos disponibles, solo escribe el ID del que quieres usar.
2. Configura el idioma objetivo:
   Luego, se te pedirá que escribas el idioma al que quieres traducir, puede ser cualquier idioma.
3. Después de eso, solo presiona `Enter` para comenzar a grabar y ¡listo!

## Usando `voice_assistant.py`
Este script actúa como un asistente de voz que graba audio, lo transcribe, genera respuestas usando OpenAI y convierte las respuestas en voz. Permite a los usuarios seleccionar dispositivos de audio, voces y mensajes del sistema. El script también registra los tiempos de transcripción, generación de respuestas y generación de voz, y concatena archivos de audio en un solo archivo de conversación.

## Usando `notetaker.py`
Este script graba audio desde un micrófono seleccionado y lo transcribe. La transcripción se reformatea en un formato más legible usando sintaxis markdown. El script guarda la transcripción formateada en un archivo markdown.

## Salida
- `main.py`: Audio MP3, transcripción, traducción y audio traducido en `/output`, además del video traducido si seleccionaste all.
- `record.py`: Grabaciones WAV, transcripciones, traducciones y audio traducido en `recording_sessions`.
- `voice_assistant.py`: Grabaciones WAV, transcripciones, respuestas y archivos de audio concatenados en `notes`.
- `notetaker.py`: Grabaciones WAV y transcripciones formateadas en `notes`.

## Información Adicional
- `.gitignore` excluye `venv` y `output`.
- Los scripts ignoran `.gitkeep` en `/videos`.

Sigue esta guía para un uso eficiente del Proyecto de Traducciones Automáticas.

