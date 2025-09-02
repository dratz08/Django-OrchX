import os
import magic
import zipfile
from hashlib import sha256
from rest_framework import serializers

# Constantes de segurança
MAX_TAMANHO_ZIP = 50 * 1024 * 1024      # 50 MB
MAX_TAMANHO_ARQUIVO = 10 * 1024 * 1024  # 10 MB por arquivo interno
MAX_ARQUIVOS = 100                      # Máximo de arquivos internos
EXTENSOES_PERMITIDAS = {".py", ".txt", ".csv", ".xlsx", ".json", ".jpg", ".png", ".robot"}


def calcular_sha256(file_path):
    sha = sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha.update(chunk)
    return sha.hexdigest()


def validar_arquivo_zip(upload_file):
    """Valida criteriosamente um arquivo ZIP enviado pelo usuário."""

    # 1. Verificar extensão do arquivo
    if not upload_file.name.lower().endswith(".zip"):
        raise serializers.ValidationError("Apenas arquivos ZIP são aceitos.")

    # 2. Verificar MIME real do arquivo
    mime = magic.from_buffer(upload_file.read(2048), mime=True)
    upload_file.seek(0)
    if mime not in ["application/zip", "application/x-zip-compressed"]:
        raise serializers.ValidationError("Tipo de arquivo inválido. Envie um ZIP válido.")

    # 3. Salvar arquivo temporariamente para análises
    dir_tmp = "C:/tmp" if os.name == "nt" else "/tmp"
    os.makedirs(dir_tmp, exist_ok=True)
    temp_path = os.path.join(dir_tmp, upload_file.name)

    with open(temp_path, "wb") as buffer:
        content = upload_file.read()
        if len(content) > MAX_TAMANHO_ZIP:
            raise serializers.ValidationError("Arquivo ZIP excede o tamanho máximo permitido.")
        buffer.write(content)
    upload_file.seek(0)

    # 4. Calcular hash para auditoria (opcional, mas recomendado)
    file_hash = calcular_sha256(temp_path)
    print(f"📦 Hash do arquivo recebido: {file_hash}")

    # 5. Validar conteúdo do ZIP
    try:
        with zipfile.ZipFile(temp_path, 'r') as zf:
            # 5.1. Quantidade máxima de arquivos internos
            if len(zf.infolist()) > MAX_ARQUIVOS:
                raise serializers.ValidationError("O arquivo ZIP contém arquivos demais.")

            for member in zf.infolist():
                # 5.2. Verificar tamanho individual dos arquivos
                if member.file_size > MAX_TAMANHO_ARQUIVO:
                    raise serializers.ValidationError(
                        f"Arquivo '{member.filename}' é muito grande ({member.file_size} bytes)."
                    )

                # 5.3. Prevenir Zip Slip (exploração de caminhos)
                extracted_path = os.path.abspath(os.path.join(temp_path, member.filename))
                if not extracted_path.startswith(os.path.abspath(dir_tmp)):
                    raise serializers.ValidationError("Tentativa de Zip Slip detectada!")

                # 5.4. Verificar extensões permitidas
                _, ext = os.path.splitext(member.filename)
                if ext and ext.lower() not in EXTENSOES_PERMITIDAS:
                    raise serializers.ValidationError(f"Extensão não permitida: {ext}")

    except zipfile.BadZipFile:
        raise serializers.ValidationError("O arquivo ZIP está corrompido ou inválido.")

    return upload_file
