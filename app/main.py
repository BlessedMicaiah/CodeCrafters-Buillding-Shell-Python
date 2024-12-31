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
        current_dir = os.getcwd()
        user_input = input().strip()

        if user_input == "exit 0":
            break

        # Split the command and check for redirection
        command_parts = shlex.split(user_input)
        if ">" in command_parts:
            cmd_index = command_parts.index(">")
            command = command_parts[:cmd_index]
            if len(command_parts) > cmd_index + 1:
                output_file = command_parts[cmd_index + 1].strip()
            else:
                output_file = None  # Handle error or default action
        else:
            command = command_parts
            output_file = None

        main_command = command[0] if command else ""
        args = command[1:] if len(command) > 1 else []

        # Built-in commands implementation
        if main_command == "pwd":
            print(current_dir)
        elif main_command == "cd":
            try:
                if args:
                    path = args[0]
                    if path == "..":
                        os.chdir(os.path.dirname(current_dir))
                    elif path == "~":
                        os.chdir(os.path.expanduser("~"))
                    else:
                        os.chdir(path)
                else:
                    os.chdir(os.path.expanduser("~"))
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
            # External command execution with optional redirection
            full_path = next((f"{path}/{main_command}" for path in PATH if os.path.isfile(f"{path}/{main_command}")), main_command)
            try:
                if os.path.isfile(main_command):  
                    result = subprocess.run(["./" + main_command] + args, capture_output=True, text=True)
                else:
                    if output_file:
                        with open(output_file, 'w') as f:
                            result = subprocess.run([full_path] + args, stdout=f, stderr=subprocess.STDOUT, text=True)
                    else:
                        result = subprocess.run([full_path] + args, capture_output=True, text=True)
                    if result.stdout:
                        print(result.stdout, end="")
                    if result.stderr:
                        print(result.stderr, end="")
            except FileNotFoundError:
                print(f"{main_command}: command not found")

if __name__ == "__main__":
    main()