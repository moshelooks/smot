import unittest

import torch

from smot.testlib import eggs, torch_eggs


class CatTest(unittest.TestCase):
    # https://pytorch.org/docs/stable/generated/torch.cat.html

    def test_scalar(self):
        eggs.assert_raises(
            lambda: torch.cat(
                (
                    torch.tensor(1),
                    torch.tensor(2),
                ),
            ),
            RuntimeError,
            "zero-dimensional tensor .* cannot be",
        )

    def test_1d(self):
        torch_eggs.assert_tensor(
            torch.cat(
                (
                    torch.tensor([]),
                    torch.tensor([1.0, 2.0]),
                    torch.tensor([]),
                    torch.tensor([3.0]),
                    torch.tensor([4.0]),
                    torch.tensor([]),
                ),
            ),
            torch.tensor([1.0, 2.0, 3.0, 4.0]),
        )

    def test_2d(self):
        torch_eggs.assert_tensor(
            torch.cat(
                (
                    torch.tensor([[1, 2], [3, 4]]),
                    torch.tensor([], dtype=torch.int),
                    torch.tensor([[5, 6]]),
                    torch.tensor([[7, 8]]),
                ),
            ),
            torch.tensor([[1, 2], [3, 4], [5, 6], [7, 8]]),
        )

        torch_eggs.assert_tensor(
            torch.cat(
                (
                    torch.tensor([[1, 2], [3, 4]]),
                    torch.tensor([], dtype=torch.int),
                    torch.tensor([[5, 6], [7, 8]]),
                ),
                dim=1,
            ),
            torch.tensor([[1, 2, 5, 6], [3, 4, 7, 8]]),
        )
