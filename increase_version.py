import os

FILE_NAME = "version.txt"
# BRANCH_NAME = "main"
# BRANCH_NAME = "develop"
BRANCH_NAME = "rc"

if __name__ == "__main__":
    if os.path.isfile(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            version_numbers = file.read().strip().split('.')
        
        if len(version_numbers) == 3:
            if BRANCH_NAME == "main":
                new_version = f"{int(version_numbers[0]) + 1}.{version_numbers[1]}.{version_numbers[2]}"
                with open(FILE_NAME, "w") as file:
                    file.write(new_version)
            elif BRANCH_NAME == "develop":
                new_version = f"{version_numbers[0]}.{int(version_numbers[1]) + 1}.{version_numbers[2]}"
                with open(FILE_NAME, "w") as file:
                    file.write(new_version)
            elif BRANCH_NAME == "rc":
                new_version = f"{version_numbers[0]}.{version_numbers[1]}.{int(version_numbers[2]) + 1}"
                with open(FILE_NAME, "w") as file:
                    file.write(new_version)
if os.path.isfile(FILE_NAME):
    with open(FILE_NAME, "r") as file:
        current_version = file.read().strip()
    print("Valor atual de version.txt:", current_version)
else:
    print("Arquivo 'version.txt' não encontrado.")