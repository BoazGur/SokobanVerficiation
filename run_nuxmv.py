from smv_writer import SMVWriter
import subprocess
import os


def main():
    board_paths = os.listdir('boards/')
    writers = import_writers(board_paths)

    for i, writer in enumerate(writers):
        writer.write_smv()
        writer.export_smv('smvs/' + board_paths[i][:-4] + '.smv')

    for path in board_paths:
        run('smvs/' + path[:-4] + '.smv')


def run(path):
    # Run the command
    nuxmv_process = subprocess.Popen(
        ["nuXmv", path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True)

    output_filename = path.split(".")[0] + ".out"

    stdout, _ = nuxmv_process.communicate()

    # Save output to file
    with open('output/' + output_filename.split('/')[1], "w") as f:
        f.write(stdout)
    print(f"Output saved to {output_filename}")

    return output_filename


def import_writers(board_paths):
    writers = []

    for path in board_paths:
        writers.append(SMVWriter('boards/' + path, 'specs.txt'))

    return writers


if __name__ == '__main__':
    main()
