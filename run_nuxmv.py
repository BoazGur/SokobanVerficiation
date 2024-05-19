from smv_writer import SMVWriter
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
    writers = import_writers(board_paths)

    for i, writer in enumerate(writers):
        writer.write_smv()
        writer.export_smv('smvs/' + board_paths[i][:-4] + '.smv')

    for i, path in enumerate(board_paths):
        # run('smvs/' + path[:-4] + '.smv')
        # run_SAT('smvs/' + path[:-4] + '.smv')
        # run_BDD('smvs/' + path[:-4] + '.smv')
        run_iterative(writers[i].board, path[:-4])

def run_iterative(board, _id):
    box_indices = []

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '$':
                box_indices.append((i, j))

    start = time.time()

    partial_board = board.copy()
    total_time = 0

    n_boxes = len(box_indices)

    for i in range(n_boxes):
        for j, idx in enumerate(box_indices):
            # replace all boxes to wall except one box
            if box_indices[j]:
                if i != j:
                    partial_board[idx[0]][idx[1]] = '#'
                else:
                    partial_board[idx[0]][idx[1]] = '$'

        box_indices[i] = None

        path = 'iterativeSmvs/' + _id + '_box_number' + str(i + 1) + '.smv'

        writer = SMVWriter(specs_path='specs.txt', board=partial_board)
        writer.write_smv()
        writer.export_smv(path)

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

        total_time += end - start

        # Save output to file
        output_filename = path.split(".")[0] + ".out"
        with open('outputIterative/' + output_filename.split('/')[1], "w") as f:
            f.write(stdout)

        print(f"Output saved to outputIterative/{output_filename}")

        partial_board = regex_proccessing(stdout, len(writer.board), len(writer.board[0]))
        if partial_board is None:
            print(f'Board {_id} not winnable')
            break


    with open('outputIterative/' + _id + '_time.txt', 'w') as f:
        f.write('time in seconds: ' + str(total_time))

    return total_time

def regex_proccessing(output, rows, cols):
    if re.search('-- specification.*is true', output):
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
    commands = "go_bmc\ncheck_ltlspec_bmc -k 15\nquit\n"
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
