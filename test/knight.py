import unittest
import chess
import torch

from pysrc.pawner import knight
from pysrc.utils import str2chs, chs2pwn

def move(stringboard,turn,rights,mv):
    chessboard = str2chs(stringboard, turn, rights)
    torchboard = chs2pwn(chessboard)
    torchboard = torchboard.to("cuda:0")
    torchaction = torch.tensor(mv[1], dtype=torch.int).unsqueeze(1)
    torch_err = knight(torchboard, torchaction.to("cuda:0")).item()

    try:
        chess.Move.from_uci(mv[0])
        chessboard.push_uci(mv[0])
        chess_err = 0
    except Exception as e:
        chess_err = 1
    
    return torch_err, chess_err, torchboard[:64], chs2pwn(chessboard)[:64]


class Suite(unittest.TestCase): 

    def test_black(self):
        stringboard,turn,rights,action = """
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ♞ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        """, chess.BLACK, "", ("f5h6",[3,5,2,7,0])

        torch_err, chess_err, torch_board, chess_board = move(stringboard,turn,rights,action)
        self.assertTrue(torch_err == chess_err == 0)
        self.assertEqual(torch_board.tolist(), chess_board.tolist())

    def test_black_fail(self):
        stringboard,turn,rights,action = """
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ♞ 
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        """, chess.BLACK, "", ("h5b5",[3,7,3,1,0])

        torch_err, chess_err, torch_board, chess_board = move(stringboard,turn,rights,action)
        self.assertTrue(torch_err == chess_err == 1)
        self.assertEqual(torch_board.tolist(), chess_board.tolist())

    def test_white(self):
        stringboard,turn,rights,action = """
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ♘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘ ⭘
        """, chess.WHITE, "", ("f5h6",[3,5,2,7,0])

        torch_err, chess_err, torch_board, chess_board = move(stringboard,turn,rights,action)
        self.assertTrue(torch_err == chess_err == 0)
        self.assertEqual(torch_board.tolist(), chess_board.tolist())


