import os
import subprocess


def is_game_running():
        # This command works on Windows
        output = subprocess.check_output('tasklist /FI "IMAGENAME eq Stardew Valley.exe" /FO CSV /NH', shell=True)
        if b"Stardew Valley.exe" in output:
            return True;
        else:
            return False;

def get_save_file_path():
    home = os.path.expanduser("~")
    base_path = os.path.join(home, "AppData", "Roaming", "StardewValley", "Saves")
    
    while True:
        # List all directories in the Saves folder
        save_dirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        
        if not save_dirs:
            print("No save directories found.")
            return None


        print("\n------------ SAVE FILES --------------\n")
        for i, dir_name in enumerate(save_dirs, 1):
            print(f"[{i}] - {dir_name}")
        print('\n--------------------------------------\n')

        try:
            choice = int(input("[OK] - Enter the number of the save directory you want to use (1, 2.. etc): ")) - 1
            if 0 <= choice < len(save_dirs):
                chosen_dir = save_dirs[choice]
                return os.path.join(base_path, chosen_dir, chosen_dir)
            else:
                print("\n[FAIL] - INVALID NUMBER!\nPlease enter a valid number.")
        except ValueError:
            print("\n[FAIL] - INVALID NUMBER!\nPlease enter a valid number.")

def find_name(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            if 'player' in line.lower():
                start = line.index('<name>') + 6
                end = line.index('</name>')
                return line[start:end]
    return None;

def ask_name():
    new_name = input('[?] - Choose your new name: ')
    if new_name != '':
        #print("[OK] - Name successfully changed.")
        return (new_name);
    else:
        print("[FAIL] - Error. Name must not be empty or can cause game-breaking bugs.")
        return None;


def modify_name(file_path, old_name, new_name):
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Replace old_name with new_name
    updated_content = content.replace(old_name, new_name)
    
    with open(file_path, 'w') as file:
        file.write(updated_content)



if __name__ == '__main__':
    game_running = is_game_running();
    if game_running == True:
        print("Stardew Valley is currently running. Please close the game before proceeding.")
        input("Press Enter to exit...")
        exit();
    file_path = get_save_file_path()
    save_directory = os.path.dirname(file_path)
    save_game_info_path = os.path.join(save_directory, 'SaveGameInfo')
    if file_path:
        name = find_name(file_path)
        if (name is None):
            print("[FAIL] - Save file is incorrect. Exiting...")
            wait = input("");
            exit();
        else:
            print("[OK] - CURRENT STARDEWVALLEY NAME :", name)

        new_name = ask_name()
        if(new_name is None):
            print("[FAIL] - New name is incorrect. Exiting ... ");
            wait = input("");
            exit(); 
        else:
            modify_name(file_path, name, new_name)

        print(f"[OK] - Name has been changed from '{name}' to '{new_name}'")
    else:
        print("[FAIL] - No valid save file selected.")

    if os.path.exists(save_game_info_path):
        modify_name(save_game_info_path, name, new_name)
    else:
        print("[OK] - SaveGameInfo file not found. Only main save file was updated.")
    
    wait = input("Press Enter to close this window...")