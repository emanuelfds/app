import sys

def increase_version(file_path, branch_name):
    FILE_NAME = 1
    BRANCH_NAME = 2
    NUMBER_SPRINT = 0
    NUMBER_DEV = 1
    NUMBER_RC = 2

    if len(sys.argv) == 3:
        file_path = sys.argv[FILE_NAME]
        branch_name = sys.argv[BRANCH_NAME]
        separator = "."

        with open(file_path, 'r') as file:
            content = file.read()
        
        numbers_splitted = content.split(separator)
        
        if branch_name in ["main", "develop", "rc"]:
            if branch_name == "main":
                numbers_splitted[NUMBER_SPRINT] = str(int(numbers_splitted[NUMBER_SPRINT]) + 1)
            elif branch_name == "develop":
                numbers_splitted[NUMBER_DEV] = str(int(numbers_splitted[NUMBER_DEV]) + 1)
            elif branch_name == "rc":
                numbers_splitted[NUMBER_RC] = str(int(numbers_splitted[NUMBER_RC]) + 1)
            
            new_content = separator.join(numbers_splitted)

            with open(file_path, 'w') as file:
                file.write(new_content)
        else:
            print('Invalid branch name.')
    else:
        print('Parameters: <file name> <branch name>')
        print('For example: python increase-version.py component_version main')

if __name__ == "__main__":
    increase_version(sys.argv[1], sys.argv[2])
