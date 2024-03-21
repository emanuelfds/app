import sys
import re

FILE_NAME = 1
BRANCH_NAME = 2
NUMBER_SPRINT = 0
NUMBER_DEV = 1
NUMBER_RC = 2

def increase_version(file_path, branch_name):
    # Abrir o arquivo component_version
    with open(file_path, 'r') as file:
        content = file.read()


if len(sys.argv) == 3:
    fileInput = open(sys.argv[FILE_NAME], 'r')
    branchName = sys.argv[BRANCH_NAME]
    separator = "."
    content = fileInput.read()
    fileInput.close()
    numbersSplitted = content.split(separator)
    if branchName == "main":
        numbersSplitted[NUMBER_SPRINT] = str(int(numbersSplitted[NUMBER_SPRINT]) + 1)
        newContent = separator.join(numbersSplitted)
        fileOutput = open(sys.argv[FILE_NAME], 'w')
        fileOutput.write(newContent)
        fileOutput.close()
    if branchName == "develop":
        numbersSplitted[NUMBER_DEV] = str(int(numbersSplitted[NUMBER_DEV]) + 1)
        newContent = separator.join(numbersSplitted)
        fileOutput = open(sys.argv[FILE_NAME], 'w')
        fileOutput.write(newContent)
        fileOutput.close()
    if branchName == "rc":
        numbersSplitted[NUMBER_RC] = str(int(numbersSplitted[NUMBER_RC]) + 1)
        newContent = separator.join(numbersSplitted)
        fileOutput = open(sys.argv[FILE_NAME], 'w')
        fileOutput.write(newContent)
        fileOutput.close()
elif BRANCH_NAME not in ["main", "develop", "rc"]:      
    print('Parameters: <file name>')
    print('For example: python increase-version.py component_version')

    # Salvar o arquivo de volta
    with open(file_path, 'w') as file:
        file.write(content)

# Capturar argumentos da linha de comando
file_path = sys.argv[1]
branch_name = sys.argv[2]

# Chamar a função para aumentar a versão
increase_version(file_path, branch_name)