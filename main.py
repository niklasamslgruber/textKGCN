import time
from pprint import pprint
import torch
from config import FLAGS
from create_kg_edges import create_doc2doc_edges
from evaluation.eval import eval
from helper.saver import Saver
from loader.load_data import load_data
from match_kg_data import create_wiki_mappings
from model.train import train
from visualization.visualize_gcn import plot


def main():
    use_wikidata = False
    if use_wikidata:
        # KG preparations
        create_wiki_mappings()
        # Note takes quite a while
        create_doc2doc_edges()

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
    eval_res = eval(preds_model, test_data, use_wikidata, True, save=True)

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
