import argparse
import os
from openai import OpenAI
from pathlib import Path
import sys
from dotenv import load_dotenv, find_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

def generate_audio(input_file):
    """
    Generate audio from a markdown file using OpenAI's Text-to-Speech API.
    
    Args:
        input_file (str): Path to the markdown file
    """
    try:
        # Verifica se a API key está configurada
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("Error: OPENAI_API_KEY não encontrada no arquivo .env")
            print("Por favor, crie um arquivo .env baseado no .env.example e configure sua API key")
            sys.exit(1)
            
        # Debug: Verifica os primeiros e últimos caracteres da API key
        print(f"API key encontrada (primeiros/últimos 4 caracteres): {api_key[:4]}...{api_key[-4:]}")

        # Read the markdown file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()

        # Create output directory if it doesn't exist
        output_dir = Path('audio_files')
        output_dir.mkdir(exist_ok=True)

        # Generate output filename
        input_path = Path(input_file)
        output_file = output_dir / f"{input_path.stem}.mp3"

        # Initialize OpenAI client with API key from .env
        client = OpenAI(api_key=api_key)

        print(f"Generating audio for {input_file}...")
        
        # Generate speech using OpenAI's API
        response = client.audio.speech.create(
            model="tts-1-hd",  # Using HD model for better quality
            voice="nova",  # 'nova' has good Brazilian Portuguese pronunciation
            input=text
        )

        # Save the audio file
        response.stream_to_file(str(output_file))
        
        print(f"Audio generated successfully: {output_file}")

    except Exception as e:
        print(f"Error generating audio: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate audio from markdown files using OpenAI TTS')
    parser.add_argument('input_file', help='Path to the markdown file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: File {args.input_file} not found")
        sys.exit(1)
        
    generate_audio(args.input_file)

if __name__ == "__main__":
    main()
