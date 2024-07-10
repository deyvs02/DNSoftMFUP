# DNSoftMFUP.py - MediaFire uploader
Media Fire Upload
Quick python3 script to upload files to MediaFire

# Usage:
Python.exe DNSoftMFUP.py -e "MediaFireEMail" -p "MediaFirePassword" -u "RemoteUploadFolder" -f "Filepath"

# Notes
* use double quotes if e.g. your password contains special characters
* redirect stderr to null to only print the final download URL
* the MediaFire API is pretty buggy, and you might receive an error, because the server hasn't finished calculating the file's checksum yet; in that case, wait a couple of seconds (depending on the filesize) and repeat the command: it will not upload, but instead detect the already uploaded file and return the download URL

# Requisites
* python3 (might also work with python@2)
* pymediafire (REST API)
* mediafire (SDK)

# More information
* https://www.mediafire.com/developers/core_api/1.5
* https://pypi.org/project/mediafire/
* https://github.com/MediaFire/mediafire-python-open-sdk


---------------------------------------------------------------------------------------------------------------------

# DNSoftMFUP - MediaFire uploader
Upload Média Fire
Script python3 rápido para fazer upload de arquivos para o MediaFire

# Como Usar:
Python.exe DNSoftMFUP.py -e "E-Mail mediafire" -p "Senha mediafire" -u "Nome pasta upload mediafire" -f "Caminho do arquivo no pc para upload"

# Notas
* use aspas duplas se, por ex. sua senha contém caracteres especiais
* redirecione stderr para null para imprimir apenas o URL de download final
* a API MediaFire tem muitos bugs e você pode receber um erro, porque o servidor ainda não terminou de calcular a soma de verificação do arquivo; nesse caso, espere alguns segundos (dependendo do tamanho do arquivo) e repita o comando: ele não fará o upload, mas detectará o arquivo já enviado e retornará o URL de download

# Requisitos
* python3 (também pode funcionar com python@2)
* pymediafire (API REST)
* mediafire (SDK)

# Mais Informações
* https://www.mediafire.com/developers/core_api/1.5
* https://pypi.org/project/mediafire/
* https://github.com/MediaFire/mediafire-python-open-sdk
