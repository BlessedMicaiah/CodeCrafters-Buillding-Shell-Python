import sys
import os
import subprocess
import shlex

def main():
    builtin_cmds = ["echo", "exit", "type", "pwd", "cd"]
    PATH = os.environ.get("PATH", "").split(':')

    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()
        user_input = input().strip()

        if user_input == "exit 0":
            break

        
        command_parts = shlex.split(user_input)
        if ">" in command_parts:
            cmd_index = command_parts.index(">")
            command = command_parts[:cmd_index]
            if len(command_parts) > cmd_index + 1:
                output_file = command_parts[cmd_index + 1].strip()
            else:
                output_file = None  
        else:
            command = command_parts
            output_file = None

        main_command = command[0] if command else ""
        args = command[1:] if len(command) > 1 else []

    
        if main_command == "pwd":
            print(os.getcwd())
        elif main_command == "cd":
            try:
                if args:
                    path = args[0]
                    if path == "..":
                        os.chdir(os.path.dirname(os.getcwd()))
                    elif path == "~":
                        os.chdir(os.path.expanduser("~"))
                    else:
                        os.chdir(path)
            except Exception as e:
                print(f"cd: {e}")
        elif main_command == "echo":
            echo_output = " ".join(args)
            if output_file:
                with open(output_file, 'w') as f:
                    f.write(echo_output + "\n")
            else:
                print(echo_output)
        elif main_command == "type":
            if not args:
                print("type: missing operand")
            else:
                cmd = args[0]
                if cmd in builtin_cmds:
                    print(f"{cmd} is a shell builtin")
                else:
                    cmd_path = next((f"{path}/{cmd}" for path in PATH if os.path.isfile(f"{path}/{cmd}")), None)
                    if cmd_path:
                        print(f"{cmd} is {cmd_path}")
                    else:
                        print(f"{cmd}: not found")
        else:
        
            full_path = next((f"{path}/{main_command}" for path in PATH if os.path.isfile(f"{path}/{main_command}")), main_command)
            try:
                if os.path.isfile(main_command):  
                    subprocess.run([main_command] + args, check=True, capture_output=True, text=True)
                else:
                    if output_file:
                        with open(output_file, 'w') as f:
                            subprocess.run([full_path] + args, stdout=f, stderr=subprocess.STDOUT, check=True, text=True)
                    else:
                        result = subprocess.run([full_path] + args, capture_output=True, text=True)
                        if result.stdout:
                            print(result.stdout, end="")
                        if result.stderr:
                            print(result.stderr, end="")
            except FileNotFoundError:
                print(f"{main_command}: command not found")
            except subprocess.CalledProcessError as e:
                print(e.output)  

if __name__ == "__main__":
    main()