import torch
import torch.nn as nn
import torch.nn.functional as F

class My_DNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Sequential(
            nn.SimulatedConv2d(
                in_channels=1,
                out_channels=16,
                kernel_size=5,
                stride=1,
                padding=2,
                path_to_arch_file='maeri_64mses_64_bw.cfg',
                path_to_tile='tiles_64/layer1.txt'
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        self.conv2 = nn.Sequential(
            nn.SimulatedConv2d(
                in_channels=16,
                out_channels=32,
                kernel_size=5,
                stride=1,
                padding=2,
                path_to_arch_file='maeri_64mses_64_bw.cfg',
                path_to_tile='tiles_64/layer2.txt'
            ),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2),
        )
        # fully connected layer, output 10 classes
        self.fc1 = nn.SimulatedLinear(32 * 7 * 7, 10, path_to_arch_file='maeri_64mses_64_bw.cfg', path_to_tile='tiles_64/layer3.txt', sparsity_ratio=0.0)
    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        # flatten the output of conv2 to (batch_size, 32 * 7 * 7)
        x = x.view(x.size(0), -1)
        output = self.fc1(x)
        return output

