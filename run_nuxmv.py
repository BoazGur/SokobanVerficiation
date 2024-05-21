from smv_writer import SMVWriter
from smv_writer_iterative import SMVWriterIterative
import time
import subprocess
import os
import re

dictonary = {
    "shtrudel": "@",
    "plus": "+",
    "dollar": "$",
    "star": "*",
    "solamit": "#",
    "dot": ".",
    "minus": "-"
}

def main():
    board_paths = os.listdir('boards/')[:-1] # Not using boardEx
    print(board_paths)
    writers = import_writers(board_paths)

    for i, writer in enumerate(writers):
        writer.write_smv()
        writer.export_smv('smvs/' + board_paths[i][:-4] + '.smv')

    run_iterative(writers[i].board, "board8")
    run_SAT('smvs/' + "board8" + '.smv')


    # for i, path in enumerate(board_paths):
    #     print(f"Working on {path[:-4]}")
    #     # run('smvs/' + path[:-4] + '.smv')
    #     run_SAT('smvs/' + path[:-4] + '.smv')
    #     run_BDD('smvs/' + path[:-4] + '.smv')
    #     run_iterative(writers[i].board, path[:-4])

def run_iterative(board, _id):
    board_copy = board.copy()
    total_time = 0
    box_counter = sum(row.count('$') for row in board_copy)
    i = 0
    while any('$' in row for row in board_copy):
        path = 'iterativeSmvs/' + _id + '_box_iteration' + str(i + 1) + '.smv'
        i += 1

        if i > box_counter:
            print(f'Board {_id} not winnable')
            break

        writer_iterative = SMVWriterIterative(specs_path='specs.txt', board=board_copy)
        writer_iterative.write_smv()
        writer_iterative.export_smv(path)

        start = time.time()

        # Run nuXmv in interactive mode
        nuxmv_process = subprocess.Popen(
            ["nuXmv", "-int", path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            universal_newlines=True
        )

        # Send commands to nuXmv
        commands = "go_bmc\ncheck_ltlspec_bmc -k 20\nquit\n"
        stdout, _ = nuxmv_process.communicate(input=commands)

        end = time.time()

        total_time += end - start

        # Save output to file
        output_filename = path.split(".")[0] + ".out"
        with open('outputIterative/' + output_filename.split('/')[1], "w") as f:
            f.write(stdout)

        print(f"Output saved to outputIterative/{output_filename}")

        board_copy = regex_proccessing(stdout, len(writer_iterative.board), len(writer_iterative.board[0]))
        if board_copy is None:
            print(f'Board {_id} not winnable')
            break

    with open('outputIterative/' + _id + '_time.txt', 'w') as f:
        f.write('time in seconds: ' + str(total_time))

    return total_time

def regex_proccessing(output, rows, cols):
    if re.search('-- specification.*is true', output) or re.search('-- no counterexample found with bound 15', output):
        return None
    
    board = [[] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            last_change = re.findall(f'v_{i}{j} = ([a-z]+)', output)[-1]
            board[i].append(dictonary[last_change])

    return board

def run(path):
    # Run nuXmv in interactive mode
    nuxmv_process = subprocess.Popen(
        ["nuXmv", "-int", path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    stdout, _ = nuxmv_process.communicate()

    # Save output to file
    output_filename = path.split(".")[0] + ".out"
    with open('output/' + output_filename.split('/')[1], "w") as f:
        f.write(stdout)

    print(f"Output saved to output/{output_filename}")

    return output_filename

def run_BDD(path):
    start = time.time()

    # Run nuXmv in interactive mode
    nuxmv_process = subprocess.Popen(
        ["nuXmv", "-int", path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    # Send commands to nuXmv
    commands = "go\ncheck_ltlspec\nquit\n"
    stdout, _ = nuxmv_process.communicate(input=commands)

    end = time.time()
    diff = end - start

    # Save output to file
    output_filename = path.split(".")[0] + ".out"
    with open('outputBDD/' + output_filename.split('/')[1], "w") as f:
        f.write(stdout)
        f.write("time in seconds: " + str(diff))
    print(f"Output saved to outputBDD/{output_filename}")

    return output_filename, diff

def run_SAT(path):
    start = time.time()
    # Run nuXmv in interactive mode
    nuxmv_process = subprocess.Popen(
        ["nuXmv", "-int", path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True
    )

    # Send commands to nuXmv
    commands = "go_bmc\ncheck_ltlspec_bmc -k 30\nquit\n"
    stdout, _ = nuxmv_process.communicate(input=commands)

    end = time.time()
    diff = end - start

    # Save output to file
    output_filename = path.split(".")[0] + ".out"
    with open('outputSAT/' + output_filename.split('/')[1], "w") as f:
        f.write(stdout)
        f.write("time in seconds: " + str(diff))
    print(f"Output saved to outputSAT/{output_filename}")

    return output_filename, diff


def import_writers(board_paths):
    writers = []

    for path in board_paths:
        writers.append(SMVWriter('boards/' + path, 'specs.txt'))

    return writers


if __name__ == '__main__':
    main()
