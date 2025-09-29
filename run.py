import subprocess
import os
import sys
import time

def run_script():
    # Caminho para a raiz do projeto
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Caminhos para as pastas do Backend e Frontend
    backend_dir = os.path.join(project_root, "Backend - API")

    # Comando para rodar a API
    api_command = [sys.executable, "main.py"]
    
    try:
        # Inicia a API em um novo processo
        print("Iniciando a API em segundo plano...")
        api_process = subprocess.Popen(api_command, cwd=backend_dir)
        
        # Dá um tempo para a API iniciar
        time.sleep(3)

        # Verifica se a API iniciou corretamente
        if api_process.poll() is not None:
            print("Erro ao iniciar a API. Verifique o console para mais detalhes.")
            return

        print("API iniciada com sucesso.")
        print("-" * 30)
        
        # Inicia o Front-end em um novo terminal
        print("Abrindo o Frontend...")
        subprocess.run('python Frontend/main.py', shell=True)
            
        print("Frontend aberto em uma nova janela.")

        # Mantém o script principal rodando para que a API não feche
        api_process.wait()

    except KeyboardInterrupt:
        print("Fechando a API...")
        api_process.terminate()
        api_process.wait()
        print("API fechado.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        if 'api_process' in locals():
            api_process.terminate()
            api_process.wait()

if __name__ == "__main__":
    run_script()
