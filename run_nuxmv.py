from smv_writer import SMVWriter
import time
import subprocess
import os


def main():
    board_paths = os.listdir('boards/')[:-1] # Not using boardEx
    writers = import_writers(board_paths)

    for i, writer in enumerate(writers):
        writer.write_smv()
        writer.export_smv('smvs/' + board_paths[i][:-4] + '.smv')

    for path in board_paths:
        # run('smvs/' + path[:-4] + '.smv')
        run_SAT('smvs/' + path[:-4] + '.smv')
        run_BDD('smvs/' + path[:-4] + '.smv')

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
