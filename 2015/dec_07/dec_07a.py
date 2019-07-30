class inst:
    def __init__(self, signal_in, signal_out, value, operator):
        self.signal_in = signal_in
        self.signal_out = signal_out
        self.value = value
        self.operator = operator
        self.shift = None

    def get_nbr_signals_in(self):
        return len(self.signal_in)

    def get_signal_in(self):
        return self.signal_in

    def get_signal_out(self):
        return self.signal_out.rstrip("\n\r")

    def get_value(self):
        return self.value

    def get_operator(self):
        return self.operator
    
    def set_shift(self,shift):
        self.shift = shift

    def get_shift(self):
        return self.shift

def read_file(filename):
    f = open(filename)
    raw_data  = []
    for line in f:
        raw_data.append(line)
    f.close()
    return raw_data


def parse_data(raw_data):
    instructions = []

    for instruction in raw_data:

        # Debug print the instruction
        # print("Instruction: {}".format(instruction), end = '')

        # Instruction NOT
        if "NOT" in instruction:
            # print("Found NOT instruction")
            tmp = instruction.split(" -> ")
            signal_out = tmp[1].rstrip("\r\n")
            tmp[0] = tmp[0].split(" ")
            signal_in = tmp[0][1]
            if signal_in.isnumeric():
                instructions.append(inst([], signal_out, signal_in, "NOT"))
            else:
                instructions.append(inst([signal_in], signal_out, None, "NOT"))
            # print("in: {signal_in}, out: {out}".format(signal_in=signal_in, out=signal_out))
        # Instruction SHIFT
        elif ("RSHIFT" in instruction) or ("LSHIFT" in instruction):
            #print("Found SHIFT instruction")
            tmp = instruction.split(' -> ')
            signal_out = tmp[1]
            tmp = tmp[0].split(" ")
            signal_in = tmp[0]
            instr =     tmp[1]
            shift =     tmp[2]

            if signal_in.isnumeric():
                instructions.append(inst([], signal_out, signal_in, instr))
            else:
                instructions.append(inst([signal_in], signal_out, None, instr))
            instructions[-1].set_shift = shift
                
            #print("in: {signal_in}, shift: {shift}, out: {signal_out}".format(signal_in=signal_in, shift=shift, signal_out=signal_out))
        # Instruction AND/OR
        elif ("AND" in instruction) or ("OR" in instruction):
            #print("Found AND/OR instruction")
            tmp = instruction.split(' -> ')
            signal_out = tmp[1]
            tmp = tmp[0].split(" ")
            signal_in = [tmp[0], tmp[2]]
            instr =     tmp[1]
            
            #print("in_1: {in_1}, in_2: {in_2}, out: {out}".format(in_1=signal_in[0], in_2=signal_in[1], out=signal_out))
            if signal_in[0].isnumeric():
                instructions.append(inst([signal_in[1]], signal_out, signal_in[0], instr))
            elif signal_in[1].isnumeric():
                instructions.append(inst([signal_in[0]], signal_out, signal_in[1], instr))
            else:
                instructions.append(inst(signal_in, signal_out, None, instr))
            
        # Instruction Assignment
        else:
            # print("Direct assignment")
            tmp = instruction.split(' -> ')
            if tmp[0].isnumeric():
                #print("Numeric value")
                instructions.append(inst([], tmp[1], tmp[0], "assignment"))
            else:
                #print("Signal assignment")
                instructions.append(inst([tmp[0]], tmp[1], None, "assignment"))

    return instructions

def missing_signals_in_network(signals_in, network):
    tmp = ""
    if len(signals_in) > 1:
        tmp = signals_in[0]
    for signal in signals_in:
        if not signal in network:
            return False
    print("Found: {signal1} {signal2}".format(signal1=tmp, signal2=signal))
    return True


def main(filename):
    network = dict()  # store every new signal in the network in this dict.
    raw_data = read_file(filename)
    instructions = parse_data(raw_data)

    instructions_left = 1000

    for dummy in range(400):
        if instructions_left == len(instructions) or len(instructions) == 0:
            print("Instructions not decreasing, qutiting")
            break
        instructins_left = len(instructions)
        print("Going through instructions, iter: ({dummy}), instructions left: {length}".format(dummy=dummy, length=len(instructions)))
        # print("Signals in network: {}".format(network.keys()))
        for idx, instruction in enumerate(instructions):

            if instruction.get_nbr_signals_in() == 0:
                # Debug print the instruction
                print("- {instruction}\t- in: {signals_in}, out: {signals_out}, value: {value}".format(instruction=instruction.get_operator(), signals_in=instruction.get_signal_in(), signals_out=instruction.get_signal_out(), value=instruction.get_value()))
                # print("-- No input signals, output: {signal_out} ".format(signal_out=instruction.get_signal_out()))
                network[instruction.get_signal_out()] = instruction.get_value()
                instructions.pop(idx)
            elif missing_signals_in_network(instruction.get_signal_in(), network):
                print("- {instruction}     \t- in: {signals_in}, out: {signals_out}, value: {value}, shift: {shift}".format(instruction=instruction.get_operator(), signals_in=instruction.get_signal_in(), signals_out=instruction.get_signal_out(), value=instruction.get_value(), shift=instruction.get_shift()))
                # print("-- All missing signals found in network")
                network[instruction.get_signal_out()] = instruction.get_value()
                instructions.pop(idx)

    print("--- Signals in network (count: {})---".format(len(network.keys())))
    for key in network.keys():
        print("{key}: {value}".format(key=key, value=network[key]))

    print("--- Length of array with instrucitons ---\n Lenght: {length}".format(
        length=len(instructions)))

    tmp = []
    for instruction in instructions:
        for signal in instruction.get_signal_in():
            if not signal in tmp:
                tmp.append(signal)
        # print("{signal}".format(signal=instruction.get_signal_in()))
    print("--- Missing in signals (count: {}) ---".format(len(tmp)))
    print(tmp)
    
''' # This is to be used in the final solution for formating the output correctly
        # Debug print content of the network dictionary
        for key in network.keys():
            print("key: -{}-".format(key))
            if network[key] < 0:
                tmp = network[key] + 2**16
            else:
                tmp = network[key]
'''

if __name__ == "__main__":
    filename = "input"
    main(filename)
