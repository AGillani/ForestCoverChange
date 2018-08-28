

from __future__ import print_function
from __future__ import division
import torch
import random
random.seed(74)
import numpy as np
import matplotlib.pyplot as pl
from json_parser import get_values, interpolate_and_scale, smooth
from torch.utils.data import Dataset, DataLoader


def get_dataloaders(file_path, in_seq_len, out_seq_len, batch_size, data_type='func_to_func'):
    print('inside dataloading code...')

    class dataset(Dataset):
        def __init__(self, data, in_seq_len, out_seq_len, mode='train'):
            super(dataset, self).__init__()
            self.in_seq_len, self.out_seq_len = in_seq_len, out_seq_len
            self.data, self.mode = data, mode
            pass

        def __getitem__(self, k):
            if self.mode != 'train':
                this_example = self.data[:500]
                this_label = self.data[500:]
                this_example = torch.Tensor(this_example)
                this_label = torch.Tensor(this_label)
                return {'input': this_example, 'label': this_label}
            start = k + self.in_seq_len
            end_ = start + self.out_seq_len
            this_example = self.data[k:start]
            this_label = self.data[start:end_]
            this_example = torch.Tensor(this_example)
            this_label = torch.Tensor(this_label)
            return {'input': this_example, 'label': this_label}

        def __len__(self):
            if self.mode != 'train':
                return 1
            # print(len(self.data)-self.in_seq_len-self.out_seq_len)
            return len(self.data)-self.in_seq_len-self.out_seq_len

    # sample, Fs, f = 80000, 500, 5
    # dataset_list = 100*np.sin(2 * np.pi * f * np.arange(sample) / Fs)
    dataset_list = get_values(this_file=file_path, all_values=['value_mean'])['value_mean']
    dataset_list = interpolate_and_scale(smooth(np.asarray(dataset_list), window_len=8),
                                                new_length=5e6, order=3, scale=100)
    # split them into train and test
    split_ratio = 0.8
    num_train = int(split_ratio*len(dataset_list))
    num_val = num_train+(len(dataset_list)-num_train)//2
    train, val, test = dataset_list[:num_train], dataset_list[num_train:num_val], dataset_list[num_val:]
    train_data = dataset(data=train, in_seq_len=in_seq_len, out_seq_len=out_seq_len, mode='train')
    val_data = dataset(data=val, in_seq_len=in_seq_len, out_seq_len=out_seq_len, mode='no_train')
    test_data = dataset(data=test, in_seq_len=in_seq_len, out_seq_len=out_seq_len, mode='no_train')
    print('train examples =', len(train), 'val examples =', len(val), 'test examples =', len(test))
    train_dataloader = DataLoader(dataset=train_data, batch_size=batch_size,
                                  shuffle=True, num_workers=4)
    val_dataloader = DataLoader(dataset=val_data, batch_size=batch_size,
                                shuffle=False, num_workers=4)
    test_dataloader = DataLoader(dataset=test_data, batch_size=batch_size,
                                 shuffle=False, num_workers=4)
    return train_dataloader, val_dataloader, test_dataloader


def main():
    this_file = 'statistics_250m_16_days_NDVI.json'
    train_dataloader, val_dataloader, test_dataloader = get_dataloaders(file_path=this_file, in_seq_len=1,
                                                                        out_seq_len=5, batch_size=4)
    count = 0
    count += 1
    for idx, data in enumerate(train_dataloader):
        examples, labels = data['input'], data['label']
        print('{} -> on batch {}/{}, {}'.format(count, idx+1, len(train_dataloader), examples.size()))
        if True:
            print(examples)


if __name__ == '__main__':
    main()














