def get_value(intcode_list, parameter, mode='0'):
    if mode == 1:
        return parameter
    else:
        # mode == 0
        # Position mode
        return intcode_list[parameter]

def opcode_add(intcode_list, para1, para2, para3, mode1, mode2, mode3):
    # Function to execute when opcode 1 is encounted
    value1 = get_value(intcode_list, para1, mode1)
    value2 = get_value(intcode_list, para2, mode2)

    final_value = value1 + value2

    # Write to intcode_list via position
    _ = mode3
    intcode_list[para3] = final_value

    # Move pointer by 4 steps
    return 4

def opcode_mul(intcode_list, para1, para2, para3, mode1, mode2, mode3):
    # Function to execute when opcode 2 is encountered
    value1 = get_value(intcode_list, para1, mode1)
    value2 = get_value(intcode_list, para2, mode2)

    final_value = value1 * value2

    # Write to intcode_list via position
    _ = mode3
    intcode_list[para3] = final_value

    # Move pointer by 4 steps
    return 4

def opcode_input(intcode_list, para, mode):
    # Function to execute when opcode 3 is encountered
    _ = mode
    integer = int(input('Please Enter input (int): '))
    # integer = 1

    # Write to intcode_list via position
    intcode_list[para] = integer

    # Move pointer by 2 steps
    return 2

def opcode_output(intcode_list, para, mode):
    # Function to execute when opcode 4 is encountered
    # Returns a value
    print(get_value(intcode_list, para, mode))

    # Move pointer by 2 steps
    return 2

def opcode_stop():
    return False

def op_jump_true(intcode_list, para1, para2, mode1, mode2):
    value1 = get_value(intcode_list, para1, mode1)
    if value1 != 0:
        value2 = get_value(intcode_list, para2, mode2)
        # We need to change the value of the outer index
        return (value2,)
    else:
        # Otherwise, move pointer by 3 steps
        return 3

def op_jump_false(intcode_list, para1, para2, mode1, mode2):
    value1 = get_value(intcode_list, para1, mode1)
    if value1 == 0:
        value2 = get_value(intcode_list, para2, mode2)
        # We need to change the value of the outer index
        return (value2,)
    else:
        # Otherwise, move pointer by 3 steps
        return 3

def op_less_than(intcode_list, para1, para2, para3, mode1, mode2, mode3):
    value1 = get_value(intcode_list, para1, mode1)
    value2 = get_value(intcode_list, para2, mode2)

    _ = mode3
    if value1 < value2:
        intcode_list[para3] = 1
    else:
        intcode_list[para3] = 0

    # Move pointer by 4 steps
    return 4

def op_equals(intcode_list, para1, para2, para3, mode1, mode2, mode3):
    value1 = get_value(intcode_list, para1, mode1)
    value2 = get_value(intcode_list, para2, mode2)

    _ = mode3
    if value1 == value2:
        intcode_list[para3] = 1
    else:
        intcode_list[para3] = 0

    # Move pointer by 4 steps
    return 4

def instruction_parser(index, intcode_list):
    instruction = intcode_list[index]
    code = str(instruction)

    opcode = int(code[-2:])
    param_modes = code[:-2]

    if opcode == 99:
        return opcode_stop()

    opcode_meta = {
        1: (opcode_add, 3),
        2: (opcode_mul, 3),
        3: (opcode_input, 1),
        4: (opcode_output, 1),
        5: (op_jump_true, 2),
        6: (op_jump_false, 2),
        7: (op_less_than, 3),
        8: (op_equals, 3)
    }

    # Obtain the opcode function and parameter count
    # from the opcode_meta dictionary
    opcode_fn, arg_count = opcode_meta[opcode]

    # Obtain opcode parameters according to the
    # parameter count via list slicing
    params = intcode_list[index+1:index+1+arg_count]

    # Obtain parameter modes
    param_modes = '0'*(arg_count-len(param_modes)) + param_modes
    modes = [int(mode) for mode in reversed(param_modes)]

    move_pointer = opcode_fn(intcode_list, *params, *modes)
    if type(move_pointer) == tuple:
        return move_pointer[0]
    else:
        new_index = index + move_pointer
        return new_index

def intcode_to_list(intcode_str:str):
    # Converts an intcode program string to a list
    str_list = intcode_str.split(',')
    return [int(x) for x in str_list]

def process_intcode_list(intcode_list:list):
    # Executes an intcode program list and
    # returns the program final state
    index = 0 # Instruction pointer
    completed = False
    while completed is not True:
        index = instruction_parser(index, intcode_list)
        if not index:
            completed = True
            break

    return intcode_list

def compute(program):
    intcode_list = intcode_to_list(program)
    final_state = process_intcode_list(intcode_list)
    return final_state