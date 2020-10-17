import shutil
import os

available_datasets = ["r8", "20ng", "mr", "ohsumed", "r52"]


def generate_prep_scripts():
    folder_path = "scripts/prep"
    clear(folder_path)

    datasets = available_datasets[1:]
    exec_code = []
    for dataset in datasets:
        name = f"{dataset}_prep"
        header = get_header(name)
        py_call = f"python prep_data.py --dataset {dataset} && python prep_graph.py --dataset {dataset}"
        code = header + py_call

        write_script(code, f"{folder_path}/{name}.sh")
        exec_code.append(f"sbatch {name}.sh")

    script = " && ".join(exec_code)
    write_script(script, f"{folder_path}/prep_all.sh")


def generate_train_scripts(n=1):
    folder_path = "scripts/train"
    clear(folder_path)

    windows = ["15"]
    threshold = ["3", "4", "5"]
    raw_count = [True, False]
    exec_code = []
    suffix = " &&\n" if n > 1 else ""

    for dataset in available_datasets:
        dataset_exec = []
        for w in windows:
            name = f"no_wiki_w{w}_{dataset}"
            header = get_header(name)
            py_call = f"python main.py --no_wiki --dataset {dataset} --word_window_size {w}"
            code = header + multiply(n, py_call)

            write_script(code, f"{folder_path}/{name}.sh")
            exec_code.append(f"sbatch {name}.sh")
            dataset_exec.append(f"sbatch {name}.sh")

            for t in threshold:
                for r in raw_count:
                    name = f"{'raw' if r else 'idf'}_w{w}_t{t}_{dataset}"
                    arguments = f"--word_window_size {w} --threshold {t} --dataset {dataset}"
                    if r:
                        arguments += " --raw_count"

                    header = get_header(name)
                    py_call = f"python main.py --show_eval --plot {arguments}"
                    code = header + multiply(n, py_call)

                    write_script(code, f"{folder_path}/{name}.sh")
                    exec_code.append(f"sbatch {name}.sh")
                    dataset_exec.append(f"sbatch {name}.sh")

        dataset_script = " && sleep 5 && ".join(dataset_exec)
        if len(dataset_exec) > 25:
            print(f"WARNING: Too many scripts for {dataset}")

        write_script(dataset_script, f"{folder_path}/train_{dataset}.sh")

    script = " && sleep 5 && ".join(exec_code)
    write_script(script, f"{folder_path}/train_all.sh")


def get_header(name):
    code = "#!/bin/bash" \
           f"\n#SBATCH --job-name={name}" \
           "\n#SBATCH --comment='Train model'" \
           "\n#SBATCH --mail-type=ALL" \
           "\n#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'" \
           "\n#SBATCH --ntasks=1" \
           f"\n#SBATCH --output=out/{name}.%j.out" \
           "\n#SBATCH --partition=All" \
           "\n" \
           "\nsource ~/miniconda3/bin/activate thesis" \
           "\n" \
           "\ncd ~/Desktop/textKGCN\n"
    return code


def clear(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.mkdir(path)


def write_script(data, path):
    assert path.endswith(".sh")
    file = open(path, "w")
    file.writelines(data)
    file.close()


def multiply(n, code):
    stmt = ""
    for x in range(0, n - 1):
        stmt += code + " &&\n"
    stmt += code
    return stmt


if __name__ == '__main__':
    generate_prep_scripts()
    generate_train_scripts(3)
