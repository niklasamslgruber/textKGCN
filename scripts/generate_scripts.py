available_datasets = ["r8", "20ng", "mr", "ohsumed", "r52"]


def generate_prep_scripts():
    datasets = available_datasets[1:]
    exec_code = []
    for dataset in datasets:

        code = "#!/bin/bash" \
               f"\n#SBATCH --job-name={dataset}_prep" \
               "\n#SBATCH --comment='Prepare datasets'" \
               "\n#SBATCH --mail-type=ALL" \
               "\n#SBATCH --mail-user='niklas.amslgruber@campus.lmu.de'" \
               "\n#SBATCH --ntasks=1" \
               f"\n#SBATCH --output=out/{dataset}_prep.%j.out" \
               "\n#SBATCH --partition=All" \
               "\n" \
               "\nsource ~/miniconda3/bin/activate thesis" \
               "\n" \
               "\ncd ~/Desktop/textKGCN" \
               f"\npython prep_data.py --dataset {dataset} && python prep_graph.py --dataset {dataset}"

        file = open(f"scripts/prep/{dataset}_prep.sh", "w")
        file.writelines(code)
        file.close()
        print(f"Generated script: 'scripts/{dataset}_prep.sh'")
        exec_code.append(f"sbatch {dataset}_prep.sh")

    script = " && ".join(exec_code)
    file = open(f"scripts/prep/prep_all.sh", "w")
    file.writelines(script)
    file.close()


def generate_train_scripts():
    windows = ["15"]
    threshold = ["2", "3"]
    raw_count = [True, False]
    exec_code = []

    for dataset in available_datasets:
        for w in windows:
            for t in threshold:
                for r in raw_count:
                    name = f"{'raw' if r else 'idf'}_w{w}_t{t}_{dataset}"
                    arguments = f"--word_window_size {w} --threshold {t} --dataset {dataset}"
                    if r:
                        arguments += " --raw_count"
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
                        "\ncd ~/Desktop/textKGCN" \
                        f"\npython main.py --show_eval --plot {arguments}"
                    file = open(f"scripts/train/{name}.sh", "w")
                    file.writelines(code)
                    file.close()
                    print(f"Generated script: 'scripts/train/{name}.sh'")
                    exec_code.append(f"sbatch {name}.sh")

    script = " && sleep 5 && ".join(exec_code)
    file = open(f"scripts/train/train_all.sh", "w")
    file.writelines(script)
    print(len(exec_code))
    file.close()


if __name__ == '__main__':
    generate_prep_scripts()
    generate_train_scripts()