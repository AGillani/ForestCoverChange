

from __future__ import print_function
from __future__ import division
from training_functions import *
from model import *
import argparse

if __name__ == '__main__':

    # parse
    parser = argparse.ArgumentParser()
    parser.add_argument('--function', dest='function', default='train_net')
    parser.add_argument('--data_path', dest='data_path', default=None)
    parser.add_argument('-p', '--pretrained_model', dest='pre_model', default=None)
    parser.add_argument('-s', '--save_dir', dest='save_dir', default=None)
    parser.add_argument('-b', '--batch_size', dest='batch_size', default=4)
    parser.add_argument('-l', '--lr', dest='lr', default=1e-3)
    parser.add_argument('-log', '--log_after', dest='log_after', default=10)
    parser.add_argument('-c', '--cuda', dest='cuda', default=0)
    parser.add_argument('--device', dest='device', default=0)
    args = parser.parse_args()

    function = args.function
    data_path = args.data_path
    pre_model = args.pre_model
    save_dir = args.save_dir
    batch_size = int(args.batch_size)
    lr = float(args.lr)
    log_after = int(args.log_after)
    cuda = int(args.cuda)
    device = int(args.device)

    function_to_call = eval(function)
    net = HyperSpectral_Resnet(in_channels=5)

    function_to_call(model=net,
                     base_folder=data_path,
                     pre_model=pre_model,
                     save_dir=save_dir,
                     batch_size=batch_size,
                     lr=lr,
                     log_after=log_after,
                     cuda=cuda,
                     device=device)
















