from config import FLAGS
from eval import eval
from load_data import load_data
from saver import Saver
from train import train
import torch
from pprint import pprint
from visualize_gcn import plot


def main():
    saver = Saver()
    train_data, val_data, test_data, raw_doc_list = load_data()

    saved_model, model = train(train_data, val_data, saver)
    assert model.num_layers == 2

    if FLAGS.plot:
        plot(model)

    with torch.no_grad():
        test_loss_model, preds_model = model(train_data.get_pyg_graph(device=FLAGS.device), test_data)

    # Classification
    eval_res = eval(preds_model, test_data, True)
    y_true = eval_res.pop('y_true')
    y_pred = eval_res.pop('y_pred')

    if FLAGS.show_eval:
        print("Test...")
        pprint(eval_res)


if __name__ == "__main__":
    main()
