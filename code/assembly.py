import sys

def mod(num):
    if num == 0:
        return 0
    sign = num // abs(num)
    return abs(num) % 1000000 * sign

def isnum(string):
    if len(string) == 0:
        return False
    if string.isnumeric():
        return True
    if string[0] == "-" and string[1:].isnumeric():
        return True
    return False

def value(variables, loc):
    if loc[0] == "=":
        if not isnum(loc[1:]):
            sys.stdout.write("Error: LOC is not an integer.\n")
            return None
        res = int(loc[1:])
    elif loc not in variables:
        sys.stdout.write("Error: LOC is not defined.\n")
        return None
    else:
        res = variables[loc]
    return res

def instruction_index(labels, loc):
    if loc not in labels:
        return None
    return labels[loc]

def run(commands):
    opcodes = {"LOAD", "STORE", "ADD", "SUB", "MULT", "DIV", "BE", "BG", "BL", "BU", "END", "READ", "PRINT", "DC"}
    variables = {}
    labels = {}
    acc = 0
    for i in range(len(commands)):
        if commands[i][0] not in opcodes and commands[i][1] != "DC":
            labels[commands[i][0]] = i
            commands[i].pop(0)
    i = 0
    while i < len(commands):
        if commands[i][0] in opcodes:
            opcode = commands[i][0]
            if len(commands[i]) > 1:
                loc = commands[i][1]
        elif commands[i][1] in opcodes:
            if commands[i][1] == "DC":
                if not isnum(commands[i][2]):
                    sys.stdout.write("Error: LOC is not an integer.\n")
                    return
                variables[commands[i][0]] = int(commands[i][2])
                i += 1
                continue
            else:
                sys.stdout.write("Syntax Error\n")
                return
        else:
            sys.stdout.write("Syntax Error\n")
            return
        if opcode == "LOAD":
            loc_value = value(variables, loc)
            if loc_value == None:
                return
            acc = loc_value
        elif opcode == "STORE":
            variables[loc] = acc
        elif opcode == "ADD":
            loc_value = value(variables, loc)
            if loc_value == None:
                return
            acc = mod(acc + loc_value)
        elif opcode == "SUB":
            loc_value = value(variables, loc)
            if loc_value == None:
                return
            acc = mod(acc - loc_value)
        elif opcode == "MULT":
            loc_value = value(variables, loc)
            if loc_value == None:
                return
            acc = mod(acc * loc_value)
        elif opcode == "DIV":
            loc_value = value(variables, loc)
            if loc_value == None:
                return
            elif loc_value == 0:
                sys.stdout.write("Error: Cannot divide by 0.\n")
                return
            acc //= loc_value
        elif opcode == "BE":
            if acc == 0:
                i = instruction_index(labels, loc)
                if i == None:
                    return
                continue
        elif opcode == "BG":
            if acc > 0:
                i = instruction_index(labels, loc)
                if i == None:
                    return
                continue
        elif opcode == "BL":
            if acc < 0:
                i = instruction_index(labels, loc)
                if i == None:
                    return
                continue
        elif opcode == "BU":
            i = instruction_index(labels, loc)
            if i == None:
                return
            continue
        elif opcode == "END":
            return
        elif opcode == "READ":
            read = sys.stdin.readline().strip()
            if not isnum(read):
                sys.stdout.write("Error: Invalid number.\n")
                return
            variables[loc] = mod(int(read))
        elif opcode == "PRINT":
            loc_value = value(variables, loc)
            if loc_value == None:
                return
            sys.stdout.write(str(loc_value) + "\n")
        i += 1
    while True:
        sys.stdin.readline()

if __name__ == "__main__":
    files = sys.argv[1:]
    if len(files) == 0:
        sys.stdout.write("Please enter files to run!\n")
        raise SystemExit
    for file in files:
        try:
            with open(file, "r") as fin:
                commands = [line.strip().split() for line in fin]
        except:
            sys.stdout.write("Error: Cannot read file.\n")
            continue
        run(commands)
