import unittest

import hamcrest
import torch

from smot.doc_link.link_annotations import api_link
from smot.testlib import eggs, torch_eggs


@api_link(
    target="torch.multinomial",
    ref="https://pytorch.org/docs/stable/generated/torch.normal.html",
    note="When `std` is a cuda tensor, this function syncs with the CPU.",
)
class NormalTest(unittest.TestCase):
    def test_degenerate(self) -> None:
        torch_eggs.assert_tensor(
            torch.normal(torch.tensor([]), torch.tensor([])),
            [],
        )

        torch_eggs.assert_tensor(
            torch.normal(torch.tensor([[]]), torch.tensor([])),
            [[]],
        )

    def test_scalar(self) -> None:
        mean = 3.5
        std = 1.2
        k = 1000
        sample = torch.normal(mean, std, [k])
        eggs.assert_match(
            torch.mean(sample).item(),
            hamcrest.close_to(mean, k * 0.05),
        )
        eggs.assert_match(
            torch.std(sample).item(),
            hamcrest.close_to(std, k * 0.05),
        )

    def test_broadcast_shape(self) -> None:
        # the returned result is the broadcast shape of mean and stddev.

        torch_eggs.assert_tensor_structure(
            torch.normal(
                torch.tensor([1.0, 3.0]),
                torch.tensor([[[4.0], [3.0], [9.0]]]),
            ),
            [
                [
                    [0.0, 0.0],
                    [0.0, 0.0],
                    [0.0, 0.0],
                ]
            ],
        )

    @api_link(
        target="torch.Tensor.normal_",
        ref="https://pytorch.org/docs/stable/generated/torch.Tensor.normal_.html",
        note="`t.normal_(...)` => `torch.normal(..., out=t)`",
    )
    def test_out(self) -> None:
        seed = 12345
        mean = 3.2
        std = 1.2

        with torch_eggs.with_generator_seed(seed):
            expected = torch.normal(mean, std, (3, 4))

        with torch_eggs.with_generator_seed(seed):
            out = torch.empty(3, 4)
            original_out = out.data
            torch.normal(mean, std, (3, 4), out=out)
            torch_eggs.assert_tensor(out, expected)
            torch_eggs.assert_views(original_out, out)

        with torch_eggs.with_generator_seed(seed):
            inplace = torch.empty(3, 4)
            original_inplace = inplace.data
            inplace.normal_(mean, std)
            torch_eggs.assert_tensor(inplace, expected)
            torch_eggs.assert_views(original_inplace, inplace)
