import shutil
import os
import random
from helper import file_utils
from analyze_results import number_of_logs

available_datasets = ["r8", "mr", "ohsumed", "r52", "20ng"]

# TODO: Update configuration thresholds
configuration = {
    "r8": range(1, 7),
    "20ng": [10, 20, 30, 40, 50, 60],
    "mr": range(1, 3),
    "ohsumed": range(1, 22),
    "r52": range(1, 7)
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

    method = ["count", "idf", "idf_wiki", "count_norm", "count_norm_pmi", "idf_norm", "idf_wiki_norm", "idf_norm_pmi", "idf_wiki_norm_pmi"]
    exec_code = []
    partitions = ["Antarktis", "Gobi", "Kalahari", "Luna", "Sibirien"]

    for index, dataset in enumerate(available_datasets):
        if "20ng" in dataset:
            continue
        threshold = configuration[dataset]
        dataset_exec = []
        name = f"no_wiki_{dataset}"
        config = create_needed_scripts(dataset)
        # if "ohsumed" in dataset or "20ng" in dataset:
        #     partition = random.choice(partitions)
        # else:
        #     partition = "All"
        header = get_header(name, random.choice(partitions))
        py_call = f"python main.py --no_wiki --plot --dataset {dataset}"
        code = header + multiply(n, py_call)
        if "20ng" in dataset:
            write_script(code, f"{folder_path}/{name}.sh")
            exec_code.append(f"sbatch {name}.sh")
            dataset_exec.append(f"sbatch {name}.sh")

        for t in threshold:
            all_types = []
            if "ohsumed" in dataset and t > 16:
                continue

            for r in method:
                needed, count = is_needed(config, True, t, r)
                if needed:
                    name = f"t{t}_{dataset}"
                    header = get_header(name, random.choice(partitions))
                    arguments = f"--threshold {t} --dataset {dataset} --plot --method {r}"
                    py_call = f"python main.py {arguments}"
                    py_call = multiply(number_of_logs - count, py_call)
                    all_types.append(py_call)

            if len(all_types) > 0:
                code = header + concat_code(all_types)
                write_script(code, f"{folder_path}/{name}.sh")
                exec_code.append(f"sbatch {name}.sh")
                dataset_exec.append(f"sbatch {name}.sh")

        dataset_script = " && sleep 1 && ".join(dataset_exec)
        if len(dataset_exec) > 25:
            print(f"WARNING: Too many scripts for {dataset}")
        if len(dataset_exec) > 0:
            write_script(dataset_script, f"{folder_path}/train_{dataset}.sh")

    script = " && sleep 1 && ".join(exec_code)
    write_script(script, f"{folder_path}/train_all.sh")


def get_header(name, partition="All"):
    code = "#!/bin/bash" \
           f"\n#SBATCH --job-name={name}" \
           "\n#SBATCH --comment='Train model'" \
           "\n#SBATCH --mail-type=END,FAIL" \
           "\n#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'" \
           "\n#SBATCH --ntasks=1" \
           f"\n#SBATCH --output=out/{name}.%j.out" \
           f"\n#SBATCH --partition={partition}" \
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


def concat_code(code_array):
    return " &&\n".join(code_array)


def create_needed_scripts(dataset):
    counts = file_utils.get_result_log_counts(dataset)
    needed = {}
    for key in counts.keys():
        count = counts[key]
        needed[key] = count

    return needed


def is_needed(config, wiki_enabled, threshold, edge_type):
    key = f"{wiki_enabled}:15:{edge_type}:{threshold}"
    if key in config:
        if config[key] >= number_of_logs:
            return False, config[key]
        else:
            return True, config[key]
    else:
        return True, 0


if __name__ == '__main__':
    generate_prep_scripts()
    generate_train_scripts(5)