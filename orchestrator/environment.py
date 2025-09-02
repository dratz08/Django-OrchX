import os
import shutil
from rest_framework.validators import ValidationError
from django.db import transaction

DIRETORIO_USUARIOS = os.getenv("DIRETORIO_USUARIOS_ORCHX")


def deletar_diretorio(path):
    try:
        shutil.rmtree(path)
        print(f"Diretório {os.path.basename(path)} e conteúdos removidos com sucesso")
    except OSError as e:
        raise ValidationError(code=400, detail=f"Erro ao deletar o diretório {os.path.basename(path)}: {e}")


def limpar_diretorio(path):
    try:
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) or os.path.islink(item):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        print("Diretório limpo com sucesso")
    except Exception as e:
        raise ValidationError(code=400, detail=f"Erro ao limpar o diretório {os.path.basename(path)}: {e}")


def criar_diretorios_usuario(id_cliente):
    novo_dir_bots = os.path.join(DIRETORIO_USUARIOS, str(id_cliente), "Bots")
    os.makedirs(novo_dir_bots, exist_ok=True)
    print("Diretórios de usuário criados com sucesso")


def criar_diretorio_robo(id_bot, id_cliente, zip_path):
    novo_robo_dir = os.path.join(DIRETORIO_USUARIOS, str(id_cliente), "Bots", str(id_bot))
    caminho_move_zip = os.path.join(novo_robo_dir, os.path.basename(zip_path))
    try:
        os.mkdir(novo_robo_dir)
        print("Diretório de robô criado com sucesso")
        os.rename(zip_path, caminho_move_zip)
        print("Arquivo zip movido para pasta do robô com sucesso")
    except Exception as e:
        deletar_diretorio(novo_robo_dir)
        try:
            os.remove(zip_path)
        except OSError:
            pass
        raise transaction.TransactionManagementError(
            f"Erro ao criar diretório e mover zip: {e}"
        )


def deletar_ambiente_usuario(id_cliente):
    try:
        env_path = os.path.join(DIRETORIO_USUARIOS, str(id_cliente))
        shutil.rmtree(env_path)
        print("Ambiente removido com sucesso")
    except Exception as e:
        raise ValidationError(code=400, detail=f"Erro ao remover ambiente do usuário: {e}")


def mover_arquivo_zip(path, id_cliente, id_bot):
    path_zip = os.path.join(DIRETORIO_USUARIOS, str(id_cliente), "Bots", str(id_bot), os.path.basename(path))
    try:
        os.rename(path, path_zip)
        print("Arquivo zip movido com sucesso")
    except Exception as e:
        print(f"Erro ao mover o arquivo zip: {e}")