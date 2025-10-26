"""
MidianText RPG - Launcher Principal
====================================

Este módulo é responsável por iniciar tanto o backend (API FastAPI) quanto o
frontend (Interface CustomTkinter) do jogo MidianText RPG.

O script gerencia o ciclo de vida completo da aplicação, incluindo:
- Inicialização do servidor API em processo separado
- Lançamento da interface gráfica do usuário
- Tratamento de erros e encerramento gracioso

Author: Carlo Terzaghi
Version: 1.3
Date: 2025
"""

import subprocess
import os
import sys
import time


def run_script():
    """
    Inicia o backend e frontend do MidianText RPG.
    
    Esta função é o ponto de entrada principal da aplicação. Ela:
    1. Localiza os diretórios do projeto
    2. Inicia o servidor API FastAPI em processo separado
    3. Aguarda a inicialização completa do backend
    4. Lança a interface gráfica do frontend
    5. Gerencia o encerramento gracioso de ambos os processos
    
    Raises:
        KeyboardInterrupt: Quando o usuário pressiona Ctrl+C
        Exception: Para quaisquer outros erros durante a execução
    
    Notes:
        - O backend inicia na porta 8000 por padrão
        - Há um delay de 3 segundos entre iniciar a API e o frontend
        - O processo principal aguarda até que ambos os componentes sejam encerrados
    
    Example:
        >>> run_script()
        Iniciando a API em segundo plano...
        API iniciada com sucesso.
        Abrindo o Frontend...
    """
    # Determina o caminho absoluto para a raiz do projeto
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Define o caminho para o diretório do backend
    backend_dir = os.path.join(project_root, "Backend - API")

    # Comando para executar o servidor API usando o interpretador Python atual
    api_command = [sys.executable, "main.py"]
    
    try:
        # Inicia o servidor API em um processo separado (em background)
        print("Iniciando a API em segundo plano...")
        api_process = subprocess.Popen(api_command, cwd=backend_dir)
        
        # Aguarda 3 segundos para garantir que a API inicialize completamente
        time.sleep(3)

        # Verifica se o processo da API está rodando corretamente
        if api_process.poll() is not None:
            print("Erro ao iniciar a API. Verifique o console para mais detalhes.")
            return

        print("API iniciada com sucesso.")
        print("-" * 30)
        
        # Inicia a interface gráfica do frontend
        print("Abrindo o Frontend...")
        subprocess.run('python Frontend/main.py', shell=True)
            
        print("Frontend aberto em uma nova janela.")

        # Mantém o script rodando e aguarda o encerramento do processo da API
        api_process.wait()

    except KeyboardInterrupt:
        # Tratamento para interrupção pelo usuário (Ctrl+C)
        print("\nFechando a API...")
        api_process.terminate()
        api_process.wait()
        print("API fechada com sucesso.")
        
    except Exception as e:
        # Tratamento genérico para quaisquer outros erros
        print(f"Ocorreu um erro: {e}")
        if 'api_process' in locals():
            api_process.terminate()
            api_process.wait()

if __name__ == "__main__":
    """
    Ponto de entrada do script quando executado diretamente.
    
    Garante que a função run_script() só seja executada quando o arquivo
    é rodado diretamente, não quando importado como módulo.
    """
    run_script()
