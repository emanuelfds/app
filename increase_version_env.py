import sys

def increase_version(file_path, environment):
    FILE_NAME = 1
    ENVIRONMENT = 2
    NUMBER_SPRINT = 0
    NUMBER_DEV = 1
    NUMBER_RC = 2

    if len(sys.argv) == 3:
        file_path = sys.argv[FILE_NAME]
        environment = sys.argv[ENVIRONMENT]
        separator = "."

        with open(file_path, 'r') as file:
            content = file.read()
        
        numbers_splitted = content.split(separator)
        
        if environment in ["dev", "hmg", "prd"]:
            if environment == "prd":
                numbers_splitted[NUMBER_SPRINT] = str(int(numbers_splitted[NUMBER_SPRINT]) + 1)
            elif environment == "hmg":
                numbers_splitted[NUMBER_DEV] = str(int(numbers_splitted[NUMBER_DEV]) + 1)
            elif environment == "dev":
                numbers_splitted[NUMBER_RC] = str(int(numbers_splitted[NUMBER_RC]) + 1)
            
            new_content = separator.join(numbers_splitted)

            with open(file_path, 'w') as file:
                file.write(new_content)
        else:
            print('Invalid environment name. Please provide dev, hmg, or prd.')
    else:
        print('Parameters: <file name> <environment>')
        print('For example: python increase-version.py component_version dev')

if __name__ == "__main__":
    increase_version(sys.argv[1], sys.argv[2])
