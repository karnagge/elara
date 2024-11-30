import argparse
import tiktoken
import sys

def count_tokens(file_path, model="gpt-3.5-turbo"):
    """
    Conta a quantidade de tokens em um arquivo usando o tokenizador da OpenAI.
    
    Args:
        file_path (str): Caminho para o arquivo a ser analisado
        model (str): Modelo do tokenizador (default: gpt-3.5-turbo)
    
    Returns:
        tuple: (número de tokens, texto do arquivo, número de palavras)
    """
    try:
        # Inicializa o tokenizador
        encoding = tiktoken.encoding_for_model(model)
        
        # Lê o arquivo
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        
        # Conta os tokens
        tokens = encoding.encode(text)
        num_tokens = len(tokens)
        
        # Conta palavras (aproximado)
        words = len(text.split())
        
        return num_tokens, text, words
        
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {str(e)}")
        sys.exit(1)

def main():
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(description='Conta tokens em um arquivo usando o tokenizador da OpenAI')
    parser.add_argument('arquivo', help='Caminho para o arquivo a ser analisado')
    parser.add_argument('--modelo', default='gpt-3.5-turbo', 
                      help='Modelo do tokenizador (default: gpt-3.5-turbo)')
    
    # Parse os argumentos
    args = parser.parse_args()
    
    # Conta os tokens
    num_tokens, text, num_words = count_tokens(args.arquivo, args.modelo)
    
    # Tamanho das janelas de contexto
    gpt4_context = 16385  # GPT-4
    claude_context = 200000  # Claude 3.5 Sonnet
    
    # Calcula porcentagens
    gpt4_percentage = (num_tokens / gpt4_context) * 100
    claude_percentage = (num_tokens / claude_context) * 100
    
    # Exibe o resultado
    print(f"\nResultado da análise:")
    print(f"Arquivo: {args.arquivo}")
    print(f"Modelo do tokenizador: {args.modelo}")
    print(f"Número de tokens: {num_tokens}")
    print(f"Número aproximado de palavras: {num_words}")
    print(f"\nComparação com janelas de contexto:")
    print(f"GPT-4 (16K tokens): {gpt4_percentage:.1f}%")
    print(f"Claude 3.5 Sonnet (200K tokens): {claude_percentage:.1f}%")

if __name__ == "__main__":
    main()
