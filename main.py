import time
from pprint import pprint
import torch
from config import FLAGS
from evaluation.eval import eval
from helper.saver import Saver
from loader.load_data import load_data
from model.train import train
from visualization.visualize_gcn import plot
from helper import file_utils as file


def main():
    if FLAGS.use_wikidata:
        file.check_files()

    if FLAGS.debug:
        print("\n-- DEBUG MODE --\n")

    saver = Saver()
    train_data, val_data, test_data, raw_doc_list = load_data()

    saved_model, model = train(train_data, val_data, saver)
    assert model.num_layers == 2

    if FLAGS.plot:
        number_of_docs = len(train_data.labels)
        plot(model, number_of_docs)

    with torch.no_grad():
        test_loss_model, preds_model = model(train_data.get_pyg_graph(device=FLAGS.device), test_data)

    # Classification
    eval_res = eval(preds_model, test_data, FLAGS.use_wikidata, True, save=True)

    y_true = eval_res.pop('y_true')
    y_pred = eval_res.pop('y_pred')

    if FLAGS.show_eval:
        print("Test...")
        pprint(eval_res)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print(f"Duration: {end - start} seconds")
