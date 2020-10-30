import shutil
import os

available_datasets = ["r8", "20ng", "mr", "ohsumed", "r52"]
# max = [26, 83, 6, 23, 11]
configuration = {
    "r8": [7, 9, 13, 18, 24],
    "20ng": [10, 20, 30, 40, 50, 60],
    "mr": [4, 5],
    "ohsumed": [7, 9, 13, 16, 19, 20],
    "r52": [6, 7, 8, 9]
    }


def generate_prep_scripts():
    folder_path = "scripts/prep"
    clear(folder_path)

    exec_code = []
    for dataset in available_datasets:
        name = f"{dataset}_prep"
        header = get_header(name)
        py_call = f"python prep_graph.py --dataset {dataset}"
        code = header + py_call

        write_script(code, f"{folder_path}/{name}.sh")
        exec_code.append(f"sbatch {name}.sh")

    script = " && sleep 1 && ".join(exec_code)
    write_script(script, f"{folder_path}/prep_all.sh")


def generate_train_scripts(n=1):
    folder_path = "scripts/train"
    clear(folder_path)

    windows = ["15"]
    method = ["count", "idf", "idf_wiki"]
    exec_code = []

    for index, dataset in enumerate(available_datasets):
        threshold = configuration[dataset]
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
                for r in method:
                    name = f"{'raw' if r else 'idf'}_w{w}_t{t}_{r}_{dataset}"
                    arguments = f"--word_window_size {w} --threshold {t} --dataset {dataset} --method {r}"

                    header = get_header(name)
                    py_call = f"python main.py --show_eval --plot {arguments}"
                    code = header + multiply(n, py_call)

                    write_script(code, f"{folder_path}/{name}.sh")
                    exec_code.append(f"sbatch {name}.sh")
                    dataset_exec.append(f"sbatch {name}.sh")

        dataset_script = " && sleep 1 && ".join(dataset_exec)
        if len(dataset_exec) > 25:
            print(f"WARNING: Too many scripts for {dataset}")

        write_script(dataset_script, f"{folder_path}/train_{dataset}.sh")

    script = " && sleep 1 && ".join(exec_code)
    write_script(script, f"{folder_path}/train_all.sh")


def get_header(name):
    code = "#!/bin/bash" \
           f"\n#SBATCH --job-name={name}" \
           "\n#SBATCH --comment='Train model'" \
           "\n#SBATCH --mail-type=END,FAIL" \
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
