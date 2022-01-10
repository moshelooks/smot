import unittest

import hamcrest
import torch

from smot.pytorch_tree.testlib import torch_eggs
from smot.testlib import eggs


class SparseCooTensorTest(unittest.TestCase):
    def test_coalesce_add(self):
        # duplicate indexes add under .coalesce()
        coo = torch.tensor([[0, 0], [2, 2]])
        vals = torch.tensor([3, 4])

        t = torch.sparse_coo_tensor(coo, vals)
        c = t.coalesce()

        torch_eggs.assert_tensor(
            t.to_dense(),
            torch.tensor(
                [
                    [0, 0, 7],
                ]
            ),
        )

    def test_explicit_size(self):
        coo = torch.tensor([[0, 1, 1], [2, 0, 2]])
        vals = torch.tensor([3, 4, 5])
        size = [2, 4]

        t = torch.sparse_coo_tensor(coo, vals, size)
        # https://pytorch.org/docs/stable/sparse.html#working-with-sparse-coo-tensors
        c = t.coalesce()

        eggs.assert_match(
            c.size(),
            torch.Size(size),
        )

        torch_eggs.assert_tensor(c.indices(), coo)
        torch_eggs.assert_tensor(c.values(), vals)

        torch_eggs.assert_tensor(
            t.to_dense(),
            torch.tensor(
                [
                    [0, 0, 3, 0],
                    [4, 0, 5, 0],
                ]
            ),
        )

    def test_infered_size(self):
        coo = torch.tensor([[0, 1, 1], [2, 0, 2]])
        vals = torch.tensor([3, 4, 5])

        t = torch.sparse_coo_tensor(coo, vals)
        # https://pytorch.org/docs/stable/sparse.html#working-with-sparse-coo-tensors
        c = t.coalesce()

        eggs.assert_match(
            c.size(),
            torch.Size([2, 3]),
        )

        torch_eggs.assert_tensor(c.indices(), coo)
        torch_eggs.assert_tensor(c.values(), vals)

        torch_eggs.assert_tensor(
            t.to_dense(),
            torch.tensor(
                [
                    [0, 0, 3],
                    [4, 0, 5],
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
