import unittest
import chess
import pysrc
import torch

# games chosen from tcec-chess.com

class Suite(unittest.TestCase): 

    def rungame(self, moves):

        chsboard = chess.Board()
        tchboard,tchplayer = pysrc.utils.chessboard2tensor(chsboard)

        # play game on both boards
        for i,move in enumerate(moves):
            #print(i,end=" ")
            #print()
            #print(tchboard[0,:64].view(8,8))
            #print(chsboard.unicode())
            #print(tchboard[0,95])
            #print()

            # get actions in san and pwn format
            san = str(chsboard.parse_san(move))
            pwn = pysrc.utils.fen_action2pawner_action(san, chsboard, chsboard.turn)

            # advance chess and pawner boards
            rew,_ = pysrc.step(tchboard,pwn.unsqueeze(0),tchplayer)
            tchplayer = 1 - tchplayer # switch player
            chsboard.push_san(move)

            #if not torch.equal(pysrc.utils.chessboard2tensor(chsboard)[0][:,:64], tchboard[:,:64]) or rew[0,0] != 0:
            #    print("="*10,i,"="*10)
            #    print(san, pwn)
            #    print(pysrc.utils.chessboard2tensor(chsboard)[0][:,:64].view(8,8))
            #    print(tchboard[:,:64].view(8,8))
            #    print(rew)
            #    print(chsboard.unicode())


            # compare chess and pawner boards
            self.assertTrue(torch.equal(pysrc.utils.chessboard2tensor(chsboard)[0][:,:64], tchboard[:,:64]))
            self.assertTrue(rew[0,0] == 0)
            self.assertTrue(rew[0,1] == 0)

        # check no other action is possible
        for pwn_action in pysrc.utils.pawner_actions():
            #print(pwn_action)
            #print(chsboard.unicode())
            pwn = torch.tensor([[*pwn_action]], dtype=torch.int, device="cuda:0")
            rew, _ = pysrc.step(tchboard.clone(),pwn,tchplayer)
            #print(rew)
            
            self.assertTrue(rew[0,tchplayer[0].item()].item() == -1)
            
    def test_1(self):
        moves = "1. e4 e5 2. f4 exf4 3. Nf3 g5 4. d4 d6 5. g3 g4 6. Nh4 f3 7. Bf4 Nc6 8. Nc3 Bg7 9. Bb5 Kf8 10. Be3 Nce7 11. h3 c6 12. Bd3 h5 13. Qd2 Be6 14. O-O-O Qa5 15. Rde1 Rc8 16. Kb1 c5 17. d5 Bd7 18. e5 c4 19. Be4 Bxe5 20. Bf4 Bf6 21. hxg4 hxg4 22. Bxd6 Bxc3 23. Bxe7+ Nxe7 24. bxc3 Qb6+ 25. Ka1 Qf6 26. Rhf1 Qd6 27. Nxf3 gxf3 28. Rxf3 Rh6 29. Ref1 f5 30. g4 Rc5 31. gxf5 Qf6 32. d6 Qxd6 33. Qc1 Qf6 34. Bxb7 Rb5 35. Be4 Ra5 36. Bb7 Rh2 37. Re3 Ke8 38. Be4 Kd8 39. Qb1 Rb5 40. Qc1 Re2 41. Rd1 Kc8 42. a3 Rf2 43. Rd4 Nxf5 44. Rxc4+ Kb8 45. Bxf5 Qxf5 46. Rd3 a5 47. Rcd4 Be6 48. c4 Rb6 49. Qe3 Rf1+ 50. Rd1 Qxc2 51. Qe5+ Kb7 52. Rd7+ Bxd7 53. Rxf1 Qb3 54. Qd5+ Bc6 55. Qf7+ Ka6 56. Qf2 Qxa3+ 57. Qa2 Qc3+ 58. Qb2 Qb2#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_2(self):
        moves = "1. e4 Nf6 2. e5 Nd5 3. d4 d6 4. Nf3 Bg4 5. Be2 e6 6. O-O Be7 7. h3 Bh5 8. c4 Nb6 9. Nc3 O-O 10. Be3 d5 11. c5 Bxf3 12. gxf3 N6d7 13. f4 Nc6 14. b4 a6 15. Kh2 Kh8 16. Rg1 Rg8 17. Rb1 Nf8 18. a4 Qd7 19. b5 Na5 20. bxa6 bxa6 21. Qe1 Nc6 22. Qf1 Ng6 23. Bxa6 Nh4 24. Qe2 Na5 25. Bd3 g6 26. Nb5 Nc4 27. Ra1 Qc6 28. Rg3 Nf5 29. Rgg1 Nh4 30. Bc1 Rgb8 31. Ra2 Ra5 32. Be3 Raa8 33. Kh1 Nf5 34. Raa1 Nh4 35. Rgc1 Rf8 36. Bd2 Nb2 37. Bc2 Nc4 38. Bb1 Qb7 39. Bc3 f6 40. exf6 Rxf6 41. Bd3 Raf8 42. Re1 Kg8 43. Rad1 e5 44. Bxc4 dxc4+ 45. d5 Bxc5 46. Bxe5 R6f7 47. Qxc4 Bxf2 48. Rf1 Bb6 49. Rd3 Nf5 50. Qc6 Qc8 51. Kh2 Re8 52. Re1 Rfe7 53. Re2 Rf8 54. Qc3 Qe8 55. Qb4 Qa8 56. Qb3 Ref7 57. d6 cxd6 58. Nxd6 Nxd6 59. Bxd6 Re8 60. Rxe8+ Qxe8 61. Be5 Qc8 62. Rd6 Ba5 63. Rd5 Bd8 64. a5 Kf8 65. a6 Ra7 66. Qb8 Qxb8 67. Bxb8 Rxa6 68. Rxd8+ Ke7 69. Rh8 Ke6 70. Rxh7 Ra2+ 71. Kg3 Kf5 72. Rf7+ Ke6 73. Ra7 Rb2 74. f5+ Kf6 75. Ra6+ Kg5 76. Rxg6+ Kxf5 77. Rg8 Rb3+ 78. Kh4 Rb7 79. Rg5+ Ke4 80. Be5 Kf3 81. Bg7 Rb4+ 82. Kh5 Rb6 83. h4 Rb4 84. Re5 Rg4 85. Rf5+ Kg3 86. Rg5 Kf4 87. Rxg4+ Ke3 88. Kg5 Kf3 89. h5 Ke3 90. h6 Kf3 91. h7 Ke3 92. h8=Q Kf3 93. Qh2 Ke3 94. Qe2+ Kxe2 95. Kf4 Kf2 96. Bc3 Ke2 97. Ke4 Kf2 98. Bd4+ Ke2 99. Be3 Kd1 100. Kd3 Ke1 101. Rg1#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_3(self):
        moves = "1. d4 Nf6 2. c4 e6 3. Nc3 Bb4 4. e3 c5 5. Ne2 cxd4 6. exd4 O-O 7. a3 Be7 8. Nf4 d6 9. Be2 Re8 10. O-O Bf8 11. Be3 g6 12. Rc1 Bg7 13. h3 Nc6 14. d5 exd5 15. Nfxd5 Nxd5 16. cxd5 Rxe3 17. fxe3 Ne5 18. Kh1 h5 19. Nb5 Bd7 20. Nd4 Bh6 21. Nf3 Nxf3 22. Rxf3 a6 23. a4 Rb8 24. b4 Qe7 25. Rc7 Qd8 26. Qc1 Bg7 27. b5 axb5 28. Bxb5 Rc8 29. Rxc8 Bxc8 30. Bd3 Be5 31. a5 Bd7 32. Qe1 Ba4 33. Rf1 Kg7 34. Qb4 Be8 35. Rb1 Bd7 36. Qd2 Qg5 37. Qf2 Bc8 38. Rf1 Qe7 39. Rc1 Qd8 40. Kg1 Bd7 41. Qe1 Be8 42. Rb1 Qc7 43. Qb4 Qd8 44. Kf1 Qg5 45. Qd2 Qe7 46. Qc2 Kh6 47. Qc8 Bg3 48. Ke2 Bf4 49. Qc1 Be5 50. Rb6 Qg5 51. Be4 Qh4 52. Qc2 Qd8 53. Qc4 Bg3 54. Bf3 Qd7 55. Qb4 Qf5 56. Qc3 Be5 57. Qc4 Qd7 58. Kd2 Kh7 59. Qb4 Qc8 60. g4 Bd7 61. gxh5 gxh5 62. Rxb7 Bc3+ 63. Qxc3 Qxb7 64. Qa3 Bc8 65. Bxh5 Kg8 66. Qxd6 Qb5 67. Qd8+ Kh7 68. Qxc8 Qxd5+ 69. Kc1 Qxh5 70. Qc4 Kh6 71. Qb4 Qd5 72. Qb6+ Kh7 73. a6 Qc4+ 74. Kb2 Qe2+ 75. Kc3 Qe1+ 76. Kd4 Qa1+ 77. Kd5 Qa2+ 78. Kc5 Qf2 79. Qd6 Qa2 80. Kb6 Qb3+ 81. Kc7 Qc3+ 82. Kd7 Kg8 83. a7 Qa5 84. Qb8+ Kg7 85. Qb2+ Kh7 86. Qb7 Qf5+ 87. Ke8 Kg6 88. a8=Q Qe5+ 89. Qe7 Qh8+ 90. Qf8 Qe5+ 91. Kd8 Qf6+ 92. Kc7 Qc3+ 93. Qc6+ Qxc6+ 94. Kxc6 Kf5 95. Kd5 Kg6 96. Ke5 Kh7 97. Qxf7+ Kh8 98. Qb7 Kg8 99. Kf6 Kh8 100. Qg7#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_4(self):
        moves = "1. d4 Nf6 2. Nf3 e6 3. Bg5 b6 4. e4 h6 5. Bxf6 Qxf6 6. Bd3 Bb7 7. Nbd2 d6 8. Qe2 a6 9. O-O-O Nd7 10. Kb1 e5 11. c3 Be7 12. h4 c5 13. Nc4 b5 14. Ne3 Nb6 15. Rhe1 O-O-O 16. dxe5 dxe5 17. c4 Rd6 18. Nd5 Nxd5 19. exd5 bxc4 20. Bxc4 Rhd8 21. Qe4 Qe6 22. Re3 f6 23. h5 Qd7 24. Red3 Kb8 25. Nh4 Bc8 26. Ng6 Rb6 27. Nxe7 Qxe7 28. Rc3 Rd7 29. Ka1 Rdb7 30. Rd2 Qd6 31. a3 Rc7 32. Ba2 Rbb7 33. Qg6 Re7 34. Rdc2 Rbc7 35. f3 Bd7 36. Rc1 Be8 37. Qg4 Ka8 38. Bb1 Bd7 39. Qg6 Bb5 40. Qe4 Re8 41. Qe3 c4 42. Ba2 Rec8 43. Qe4 f5 44. Qxf5 Qxd5 45. Qc2 Ka7 46. Rd1 Qc6 47. Qe2 Qc5 48. Qe1 Kb8 49. Re3 e4 50. fxe4 Qxh5 51. e5 Qg5 52. e6 Qf6 53. Rc1 Qe7 54. Qc3 Be8 55. Qe5 Bb5 56. Bxc4 Qf6 57. Qxf6 gxf6 58. b3 Re7 59. Kb2 Rc5 60. Be2 Re5 61. Rxe5 fxe5 62. Bg4 Rg7 63. Bh3 Rc7 64. Re1 Bd3 65. b4 e4 66. Bf5 Rc2+ 67. Kb3 Rc7 68. g4 a5 69. bxa5 Ka7 70. a4 Bc4+ 71. Ka3 Re7 72. Rxe4 Ba6 73. Kb4 Kb7 74. Kc5 h5 75. Kd6 Re8 76. e7 Ka7 77. Bd7 Rg8 78. Rf4 Bc8 79. Bc6 Rg6+ 80. Kc5 Rg5+ 81. Kd4 Rg8 82. g5 Bb7 83. Bb5 Rc8 84. Rf8 Rc1 85. e8=Q Rc8 86. Qxc8 Bxc8 87. Rxc8 Kb7 88. Ba6+ Kxa6 89. g6 Kb7 90. Rc5 h4 91. g7 h3 92. g8=Q h2 93. Qc8+ Ka7 94. Rc7#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_5(self):
        moves = "1. c4 e6 2. d4 d5 3. Nf3 c6 4. Nc3 f5 5. Bf4 Nf6 6. e3 Be7 7. Be2 O-O 8. O-O Nh5 9. g3 Nd7 10. h4 Nhf6 11. Ng5 Nb8 12. Kg2 h6 13. Rh1 Ne4 14. Ncxe4 fxe4 15. Bh5 hxg5 16. hxg5 Bxg5 17. Bg6 Rxf4 18. gxf4 Bh6 19. Rxh6 gxh6 20. Qh5 Qf6 21. Rg1 Kf8 22. Kf1 Nd7 23. Bh7 Ke7 24. Rg6 Qf8 25. Qh4+ Nf6 26. Rxh6 b6 27. Qg5 Ba6 28. Ke1 Bxc4 29. f5 Ba6 30. a3 c5 31. fxe6 Bc8 32. Bf5 Bxe6 33. Rh7+ Ke8 34. Bg6+ Kd8 35. Bf7 Qe7 36. Rh8+ Kc7 37. Rxa8 Kb7 38. Bxe6 Kxa8 39. Bxd5+ Nxd5 40. Qxd5+ Kb8 41. dxc5 bxc5 42. a4 Qe8 43. Qd6+ Kb7 44. b3 Qh8 45. Qd7+ Ka8 46. Qc6+ Kb8 47. Qb5+ Ka8 48. Qxc5 Qh1+ 49. Kd2 Kb8 50. Qd4 Qb1 51. a5 Qa2+ 52. Kc3 Qxf2 53. a6 Qh4 54. Qd6+ Kc8 55. Qc6+ Kd8 56. Qa8+ Kc7 57. Qxa7+ Kd8 58. Qd4+ Kc8 59. Qc5+ Kb8 60. Qb6+ Kc8 61. Qc6+ Kd8 62. a7 Qe1+ 63. Kc4 Qe2+ 64. Kb4 Qa2 65. a8=Q+ Qxa8 66. Qxa8+ Ke7 67. Kc5 Ke6 68. Qg8+ Ke5 69. Qf8 Ke6 70. Kc6 Ke5 71. Kd7 Kd5 72. Qf5#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_6(self):
        moves = "1. e4 e6 2. d4 d5 3. Nc3 Bb4 4. e5 c5 5. a3 Bxc3+ 6. bxc3 Ne7 7. Qg4 Nf5 8. Bd3 h5 9. Qh3 Nc6 10. Nf3 Qa5 11. O-O cxd4 12. cxd4 Nfxd4 13. Nxd4 Nxd4 14. Rb1 Qc7 15. Bf4 Bd7 16. Rfc1 Kf8 17. Qe3 Nc6 18. c4 d4 19. Qe4 h4 20. h3 Be8 21. Rc2 Rc8 22. c5 Rh5 23. Be2 Rf5 24. Bh2 Qd8 25. Rcb2 Ne7 26. Qxh4 Bc6 27. Bd3 Kg8 28. f3 Qd7 29. Re1 Qc7 30. Rd1 Ba4 31. Rc1 Bc6 32. Qxd4 Rd8 33. Qc3 Rh5 34. Rd2 Rd5 35. Bg3 Rg5 36. Kh2 Rxg3 37. Kxg3 Rxe5 38. Kf2 Rg5 39. Qd4 Rd5 40. Qb4 a5 41. Qb2 Qf4 42. Rc4 Qg5 43. Rg4 Qh6 44. Rd1 f5 45. Rd4 Rxc5 46. Rd8+ Kf7 47. Qd4 b6 48. Re1 Bd5 49. Qb2 Rc7 50. Qxb6 Rb7 51. Qc5 Qh4+ 52. Kf1 Qf4 53. Be2 a4 54. Ra8 Bb3 55. Ra7 Rxa7 56. Qxa7 Qd6 57. Bb5 Qxa3 58. Qd4 Bd5 59. Ra1 Qb3 60. Bxa4 Qb8 61. Bc2 Nc6 62. Qc3 g5 63. Rb1 Qa7 64. Bd3 Ne7 65. Be2 Ba2 66. Rb4 Kg6 67. h4 Nd5 68. Qh8 Ne3+ 69. Kg1 g4 70. Kh2 Qg7 71. h5+ Kf6 72. Qd8+ Qe7 73. Qxe7+ Kxe7 74. Rb7+ Kf8 75. Kg3 Bd5 76. Rc7 Kg8 77. h6 Ba2 78. Kh4 Nd5 79. Ra7 Bb1 80. Kg5 f4 81. fxg4 Ne3 82. Kf6 Nd5+ 83. Ke5 Nb6 84. g5 f3 85. Bxf3 Nc8 86. Rb7 Bd3 87. Bh5 Be4 88. Rb8 Kh7 89. Rxc8 Bb7 90. Rc7+ Kh8 91. Rxb7 Kg8 92. g6 Kf8 93. Kxe6 Kg8 94. Rb8#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_7(self):
        moves = "1. d4 Nf6 2. c4 g6 3. Nc3 Bg7 4. e4 d6 5. Be2 O-O 6. Nf3 e5 7. O-O Nc6 8. d5 Ne7 9. Ne1 Ne8 10. Be3 f5 11. f3 Kh8 12. a4 Ng8 13. a5 Bh6 14. Bf2 Ngf6 15. b4 Qe7 16. Nd3 Nh5 17. exf5 gxf5 18. g3 Bg7 19. Ra3 Qg5 20. Kh1 Nef6 21. Rg1 a6 22. Nb2 Qh6 23. Be1 Nd7 24. Rg2 Re8 25. Ra2 Qg6 26. c5 dxc5 27. bxc5 Nhf6 28. Nc4 Nxc5 29. Bf2 Ncd7 30. Na4 Qf7 31. Rd2 Qf8 32. d6 b5 33. axb6 cxb6 34. Naxb6 Rb8 35. Nxc8 Rexc8 36. Ba7 Rb5 37. Bg1 Rcb8 38. Qa4 Nc5 39. Qa2 Nfd7 40. Rd1 Qf7 41. Bf1 Rb4 42. Rgd2 R4b7 43. Rc2 f4 44. Nd2 Qxa2 45. Rxa2 Bf8 46. gxf4 exf4 47. Bd4+ Bg7 48. Bxc5 Nxc5 49. Rc2 Nd7 50. Ne4 Bf6 51. Nxf6 Nxf6 52. Bh3 Rb1 53. Rxb1 Rxb1+ 54. Kg2 Rd1 55. Rc8+ Kg7 56. d7 Nxd7 57. Rc7 Rd2+ 58. Kf1 Rxh2 59. Bxd7 Kg6 60. Rc6+ Kg5 61. Rxa6 Rb2 62. Bc6 Rb1+ 63. Kg2 Rc1 64. Be4 Rc4 65. Bxh7 Rc5 66. Be4 Re5 67. Kh3 Kh5 68. Rf6 Kg5 69. Rc6 Kh5 70. Rd6 Ra5 71. Rd5+ Rxd5 72. Bxd5 Kg5 73. Bc6 Kh5 74. Be4 Kg5 75. Bd3 Kh5 76. Bf1 Kg5 77. Ba6 Kh5 78. Bc4 Kg5 79. Bd5 Kh5 80. Bb3 Kh6 81. Kh4 Kg7 82. Bc4 Kh7 83. Bf7 Kh8 84. Be6 Kh7 85. Kg5 Kg7 86. Bc4 Kh7 87. Bd3+ Kg7 88. Bb5 Kh7 89. Bd7 Kg7 90. Be6 Kf8 91. Ba2 Kg7 92. Kxf4 Kh6 93. Bd5 Kg6 94. Bb7 Kf6 95. Ba6 Kf7 96. Bb5 Ke6 97. Bc4+ Kd6 98. Ke4 Kc6 99. Ke5 Kb6 100. f4 Kc6 101. Bg8 Kd7 102. Ke4 Kd6 103. Ba2 Kc5 104. Ke5 Kc6 105. f5 Kd7 106. f6 Ke8 107. Bd5 Kd7 108. Bc6+ Kxc6 109. f7 Kb5 110. Kf6 Ka4 111. f8=Q Kb5 112. Qa3 Kc6 113. Qb4 Kd5 114. Kf5 Kc6 115. Ke6 Kc7 116. Qb5 Kc8 117. Kd6 Kd8 118. Qd7#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_8(self):
        moves = "1. d4 g6 2. c4 Bg7 3. Nc3 d6 4. e4 Nd7 5. Nf3 e5 6. Be2 c6 7. d5 Ngf6 8. Be3 cxd5 9. cxd5 O-O 10. O-O Ne8 11. Kh1 f5 12. Ng5 Nc5 13. exf5 gxf5 14. f4 Bh6 15. b4 exf4 16. bxc5 fxe3 17. Ne6 Bxe6 18. dxe6 Qe7 19. Bc4 Kh8 20. Qd4+ Bg7 21. Qxe3 Nf6 22. Rad1 dxc5 23. Qe2 a6 24. a4 Ng4 25. Nd5 Qd6 26. g3 b5 27. e7 bxc4 28. exf8=Q+ Rxf8 29. h3 Qh6 30. Kg2 Ne5 31. Ne3 f4 32. Rxf4 Qc6+ 33. Kh2 Nf3+ 34. Kh1 Nh4+ 35. Nd5 Rxf4 36. gxf4 Nf5 37. Kh2 Bd4 38. Qxc4 Nh4 39. Qb3 Qe8 40. Qd3 Qe6 41. Nb4 Qf6 42. Nc2 Qxf4+ 43. Kh1 Be5 44. Qe2 Ng6 45. Qg2 a5 46. Rd8+ Kg7 47. Rd7+ Kh8 48. Rd1 Kg7 49. Re1 Kh8 50. Re4 Qf6 51. Ne3 Qb6 52. Qg4 Qb2 53. Nf1 Qa1 54. Qf5 Kg7 55. Rg4 Bf6 56. Qd7+ Kh8 57. Rg1 Qc3 58. Qe8+ Kg7 59. Ne3 Be5 60. Qd7+ Kh8 61. Qc8+ Kg7 62. Qb7+ Kg8 63. Qf3 Bd4 64. Qd5+ Kg7 65. Nf5+ Kf8 66. Qd8+ Kf7 67. Qd7+ Kf6 68. Nxd4 cxd4 69. Rf1+ Kg5 70. Qg4+ Kh6 71. h4 Qc6+ 72. Kg1 Qc5 73. h5 d3+ 74. Kg2 Qd5+ 75. Kh3 d2 76. hxg6 Qd3+ 77. Kg2 Qd5+ 78. Qf3 Qg5+ 79. Kh3 d1=Q 80. Rxd1 Qe7 81. gxh7 Kg7 82. Rg1+ Kh8 83. Qa8+ Qf8 84. Qxf8+ Kxh7 85. Qg7#"
        moves = moves.split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_9(self):
        moves = "1. d4 Nf6 2. c4 e6 3. Nf3 b6 4. g3 Ba6 5. Qa4 c5 6. Bg2 Bb7 7. O-O Qc8 8. d5 exd5 9. Bg5 Be7 10. cxd5 Bxd5 11. Nc3 Bc6 12. Qf4 O-O 13. e4 Kh8 14. a3 Ng8 15. Bxe7 Nxe7 16. Qd6 Qd8 17. b4 cxb4 18. axb4 a6 19. Rfe1 Bb7 20. Rad1 Nbc6 21. e5 a5 22. b5 Nb4 23. Nh4 Bxg2 24. Kxg2 Rc8 25. Na4 Rb8 26. Re4 Re8 27. Qxd7 Qxd7 28. Rxd7 Kg8 29. Nf3 Ng6 30. Rd6 Ne7 31. Nd4 Ned5 32. f4 Kf8 33. Kf3 Red8 34. Nc6 Nxc6 35. Rxc6 Ne7 36. Rxb6 Rd3+ 37. Ke2 Rxb6 38. Nxb6 Rb3 39. Nd7+ Ke8 40. Nf6+ Kd8 41. Rd4+ Kc8 42. Ne4 Nf5 43. Ra4 Rb2+ 44. Kd3 Rxb5 45. Ng5 Nh6 46. Kc4 Rb2 47. h3 f6 48. exf6 gxf6 49. Nxh7 Rh2 50. Nxf6 Rxh3 51. Ra3 Kd8 52. Ne4 Rh5 53. Ng5 Rh1 54. Rxa5 Ke7 55. Kd3 Rg1 56. Ne4 Re1 57. Rh5 Nf7 58. g4 Rg1 59. g5 Kf8 60. Rh2 Ra1 61. g6 Ra3+ 62. Kd4 Ra4+ 63. Kd5 Ra5+ 64. Nc5 Nh6 65. Rxh6 Kg7 66. Rh5 Kxg6 67. Re5 Kf7 68. f5 Ra8 69. Ne4 Ra5+ 70. Kd6 Ra6+ 71. Kd7 Ra7+ 72. Kc6 Ra6+ 73. Kb7 Ra1 74. Re6 Kg8 75. Nd6 Rb1+ 76. Kc7 Rc1+ 77. Kd8 Ra1 78. Re5 Ra8+ 79. Kd7 Kg7 80. Ke6 Ra1 81. f6+ Kg8 82. Rg5+ Kf8 83. Rh5 Re1+ 84. Kd7 Rg1 85. Re5 Kg8 86. Ke7 Rf1 87. f7+ Rxf7+ 88. Nxf7 Kg7 89. Re6 Kg8 90. Ng5 Kg7 91. Rc6 Kg8 92. Kf6 Kf8 93. Rc8#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_10(self):
        moves = "1. d4 Nf6 2. c4 c5 3. d5 e5 4. Nc3 d6 5. e4 Be7 6. g3 O-O 7. Bg2 a6 8. a4 Ne8 9. Nge2 Nd7 10. O-O b6 11. Kh1 Ra7 12. Qd3 g6 13. Bh3 Ng7 14. Bd2 Kh8 15. Rab1 Bg5 16. f4 Bh6 17. Bxd7 Rxd7 18. g4 exf4 19. Nxf4 Bg5 20. Ne6 Nxe6 21. dxe6 Ra7 22. e7 Bxe7 23. Nd5 f6 24. Rf4 Kg8 25. Rbf1 Qe8 26. Bc3 Bd8 27. Bxf6 Raf7 28. g5 Bb7 29. Kg2 Qd7 30. Bxd8 Rxf4 31. Ne7+ Kf7 32. Rxf4+ Ke8 33. Nxg6 Rxf4 34. Nxf4 Qg4+ 35. Qg3 Bxe4+ 36. Kf2 Qxg3+ 37. Kxg3 Kxd8 38. Kg4 Bc2 39. a5 bxa5 40. Kh5 Ke7 41. Kh6 Kf7 42. h4 Be4 43. h5 a4 44. Ne2 Bc2 45. Nc3 Ke6 46. Nd5 Ke5 47. Nf6 Bd3 48. Nxh7 Bxc4 49. g6 Bd5 50. Kg7 c4 51. Nf6 a3 52. bxa3 c3 53. Nxd5 Kxd5 54. Kf6 c2 55. g7 c1=Q 56. g8=Q+ Kd4 57. Qg5 Qh1 58. h6 Kc3 59. Qg6 Qf3+ 60. Qf5 Qa8 61. h7 Qf8+ 62. Kg6 Qe8+ 63. Kg5 Qe3+ 64. Qf4 Qg1+ 65. Kf6 Qh1 66. Qf5 Kd2 67. Kg6 d5 68. Qf6 Qe4+ 69. Kh6 Qh1+ 70. Kg7 Qe4 71. h8=Q Ke1 72. Qh2 Qg4+ 73. Kh6 Qe2 74. Qg1+ Qf1 75. Qff2+ Kd1 76. Qgxf1#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_11(self):
        moves = "1. d4 Nf6 2. c4 b6 3. Nc3 Bb7 4. Qc2 Nc6 5. Nf3 Nb4 6. Qb1 g6 7. e4 d6 8. a3 Nc6 9. d5 Nb8 10. Qc2 Bg7 11. Be2 e6 12. Bg5 Qe7 13. Rd1 h6 14. Be3 O-O 15. O-O Re8 16. Rfe1 Nbd7 17. h3 Rac8 18. Bf1 a6 19. b4 Kh7 20. a4 c5 21. b5 Ra8 22. Bd2 Kg8 23. Bc1 e5 24. bxa6 Bxa6 25. Bd2 h5 26. Ra1 Reb8 27. Be2 Bc8 28. Kh1 Nf8 29. Rg1 Bd7 30. Ra3 N8h7 31. Qc1 Rf8 32. Nh2 Ne8 33. g4 hxg4 34. hxg4 f6 35. Nf3 Kf7 36. Kg2 Rh8 37. Rh1 Nf8 38. Rxh8 Bxh8 39. Qb1 Ra6 40. Qh1 Kg8 41. Nh4 Qf7 42. Nb5 Nh7 43. Qb1 Nf8 44. Bd1 Ra8 45. Rg3 Nh7 46. Nc3 Ra6 47. Bc2 Nf8 48. Qh1 Ra8 49. Bd1 Bg7 50. Qh2 Nh7 51. g5 Nf8 52. gxf6 Nxf6 53. Kg1 Be8 54. Qg2 Kh8 55. Nb5 Rd8 56. Bg5 Rd7 57. Kf1 Kg8 58. Kg1 Kh8 59. Bf3 Kg8 60. Be2 Kh8 61. Kf1 Kg8 62. Kg1 Kh8 63. Bd1 Kg8 64. Kf1 Kh8 65. Bf3 Kg8 66. Bd1 Kh8 67. Bf3 Kg8 68. Kg1 Kh8 69. Be2 Kg8 70. Kf1 Kh8 71. Kg1 Kg8 72. Ra3 N8h7 73. Bd2 Nf8 74. a5 bxa5 75. Rxa5 Qe7 76. Bg4 Nxg4 77. Qxg4 Kf7 78. Ra6 Bf6 79. Nf3 Kg8 80. Kg2 Rd8 81. Ba5 Rd7 82. Ra8 Bf7 83. Rc8 Be8 84. Bc7 Bf7 85. Bb8 Rd8 86. Rxd8 Qxd8 87. Bxd6 Nd7 88. Qg3 Qe8 89. Nc7 Qd8 90. Ne6 Qb6 91. Bxe5 Bxe6 92. Qxg6+ Kf8 93. Bxf6 Bh3+ 94. Kxh3 Qxf6 95. Qxf6+ Nxf6 96. e5 Nd7 97. Kg4 Ke7 98. Kf5 Nb6 99. Nd2 Nc8 100. Ne4 Nb6 101. d6+ Ke8 102. e6 Kd8 103. e7+ Kd7 104. Nf6+ Kxd6 105. e8=Q Kc7 106. Qb5 Na8 107. Nd5+ Kc8 108. Qc6+ Kd8 109. Qxa8+ Kd7 110. Qb8 Kc6 111. Qc7#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_12(self):
        moves = "1. e4 d5 2. exd5 Nf6 3. Bb5+ Bd7 4. Bc4 Bg4 5. f3 Bf5 6. g4 Bg6 7. Nc3 e5 8. h4 h5 9. d4 Bd6 10. dxe5 Bxe5 11. g5 Nfd7 12. f4 Bxc3+ 13. bxc3 O-O 14. Ne2 Bf5 15. O-O Nb6 16. Bb3 Bg4 17. Qd2 N8d7 18. Ng3 c6 19. c4 Nc5 20. Ba3 Nbd7 21. Qd4 Qb6 22. Kg2 cxd5 23. Bb2 Ne6 24. Qxb6 Nxb6 25. cxd5 Nc5 26. c4 Rfc8 27. Bd4 Nd3 28. c5 Nxc5 29. Bxc5 Rxc5 30. Ne4 Rcc8 31. Rfe1 Nc4 32. d6 Bf5 33. Rad1 b5 34. Rd5 Bd7 35. Kh2 Bc6 36. Rd3 Bd7 37. g6 Re8 38. Rd5 fxg6 39. Re5 Kf8 40. Nc5 Bg4 41. d7 Red8 42. Re7 a5 43. a4 Nd6 44. axb5 Rab8 45. Ba4 Rb6 46. Bc2 Rxb5 47. Bxg6 Rbb8 48. f5 Bxf5 49. Bxf5 Nxf5 50. R7e5 g6 51. Ne6+ Kf7 52. Rb5 Ra8 53. Rxa5 Rab8 54. Nxd8+ Rxd8 55. Rd1 Nxh4 56. Kg3 Nf5+ 57. Kf4 Nh6 58. Ra6 Ke7 59. Rxg6 Rf8+ 60. Ke4 Ng4 61. Rg7+ Ke6 62. d8=Q Nf2+ 63. Ke3 Rxd8 64. Rxd8 Nh3 65. Rg3 Nf2 66. Kxf2 Ke7 67. Rgd3 h4 68. Ke3 Kf7 69. R3d7+ Ke6 70. Rh7 h3 71. Ke4 h2 72. Kf4 h1=Q 73. Rxh1 Ke7 74. Rhh8 Kf7 75. Kf5 Kg7 76. Rh1 Kf7 77. Rh7#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_13(self):
        moves = "1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. f4 Bg7 5. Nf3 c5 6. Bb5+ Bd7 7. Bxd7+ Nfxd7 8. d5 Na6 9. O-O Nc7 10. a4 a6 11. f5 b5 12. Qe1 Ne5 13. h3 Nxf3+ 14. Rxf3 Qd7 15. Kh1 O-O 16. a5 gxf5 17. exf5 Kh8 18. Qh4 b4 19. Ne4 Nxd5 20. Ng5 Nf6 21. b3 d5 22. Bd2 Rac8 23. Raf1 Rc6 24. Rg3 Qe8 25. Bf4 d4 26. Re1 Rg8 27. Rf3 h6 28. Rf2 Rf8 29. Nf3 Ng8 30. Ne5 Bxe5 31. Rxe5 f6 32. Re4 Rf7 33. Qh5 Rf8 34. Qe2 Rf7 35. Re6 Rg7 36. Qe4 Rxe6 37. Qxe6 Qa8 38. Kg1 Qb7 39. Qc4 Qc6 40. Bd2 Qd6 41. Re2 h5 42. Rf2 Rh7 43. Bf4 Qc6 44. Bc1 Qd6 45. Bd2 Rg7 46. Kh1 d3 47. Qxd3 Qxd3 48. cxd3 Kh7 49. Be3 Nh6 50. Kh2 Rg8 51. Bxc5 Rd8 52. Bxe7 Rxd3 53. Bxf6 Rxb3 54. Rf4 Ra3 55. Rxb4 Rxa5 56. Rb7+ Kg8 57. Rg7+ Kf8 58. Rh7 Nxf5 59. Rxh5 Kg8 60. h4 Rb5 61. Rh8+ Kf7 62. Bg5 a5 63. Ra8 Nd4 64. Bd2 Nb3 65. Be3 Re5 66. Bf4 Rb5 67. Ra7+ Kg8 68. Kh3 Nc5 69. g3 Ne4 70. Bc7 Rc5 71. Bxa5 Nf2+ 72. Kg2 Ne4 73. Bc7 Nf6 74. Bf4 Ng4 75. Ra4 Rd5 76. Bc1 Nf6 77. g4 Rd3 78. h5 Rb3 79. h6 Rc3 80. Bg5 Nd7 81. Bf4 Nf8 82. Ra7 Rc6 83. g5 Ng6 84. Be3 Nh4+ 85. Kh3 Nf5 86. Bf4 Re6 87. Kg4 Ne7 88. Kh5 Re1 89. g6 Rh1+ 90. Kg5 Rg1+ 91. Kf6 Rxg6+ 92. Kxe7 Rc6 93. Rd7 Ra6 94. Bd6 Kh7 95. Kf6+ Kxh6 96. Kf5 Ra5+ 97. Be5 Rb5 98. Rd8 Rxe5+ 99. Kxe5 Kg6 100. Ke6 Kg5 101. Rd4 Kg6 102. Rd5 Kg7 103. Rg5+ Kh6 104. Kf6 Kh7 105. Kf7 Kh6 106. Ra5 Kh7 107. Rh5#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_14(self):
        moves = "1. e4 d6 2. d4 Nf6 3. Nc3 g6 4. f4 Bg7 5. Nf3 c5 6. Bb5+ Bd7 7. Bxd7+ Nfxd7 8. d5 Na6 9. O-O Nc7 10. a4 a6 11. f5 b5 12. Qe1 bxa4 13. Nxa4 Rb8 14. Kh1 O-O 15. Qh4 gxf5 16. Nc3 e6 17. Bg5 f6 18. Bh6 Bxh6 19. Qxh6 fxe4 20. Nh4 exd5 21. Ra3 Ne5 22. Ne2 e3 23. Rxe3 Kh8 24. Rxe5 dxe5 25. Ng6+ Kg8 26. Ng3 Nb5 27. Nf5 Qc7 28. Nfe7+ Kf7 29. Rxf6+ Kxf6 30. Nxd5+ Kf7 31. Qxh7+ Ke6 32. Nxc7+ Nxc7 33. Qe7+ Kd5 34. Qd7+ Kc4 35. Nxe5+ Kb4 36. h4 Rbe8 37. Qxc7 Rxe5 38. Qb6+ Ka4 39. Qxa6+ Kb4 40. Qb7+ Ka5 41. c4 Re1+ 42. Kh2 Rb8 43. Qxb8 Ka6 44. Qb5+ Ka7 45. Qa5+ Kb7 46. Qxe1 Kc7 47. h5 Kd6 48. h6 Kc7 49. h7 Kb7 50. Qe6 Kc7 51. h8=Q Kb7 52. Qg7+ Ka8 53. Qe8#".split(" ")
        del moves[::3]
        self.rungame(moves)
    
    def test_15(self):
        moves = "1. d4 d5 2. c4 c6 3. Nf3 Nf6 4. Nc3 dxc4 5. a4 Bg4 6. Ne5 Bh5 7. g3 e6 8. Bg2 Nbd7 9. Nxc4 Bb4 10. a5 Nd5 11. Qb3 O-O 12. e4 Nxc3 13. Qxb4 Nb5 14. Be3 Rc8 15. Na3 Nxa3 16. Qxa3 a6 17. O-O Be2 18. Rfe1 Bb5 19. h4 Re8 20. Bg5 Qc7 21. Qc3 Nf8 22. Rad1 h6 23. Bc1 f6 24. b3 Qf7 25. Ba3 Nd7 26. Bd6 f5 27. Qc2 Rcd8 28. exf5 exf5 29. Bc7 Ra8 30. Bf4 Nf6 31. Qxf5 Be2 32. Rc1 Bg4 33. Qd3 Rad8 34. Be5 Be6 35. b4 Nd5 36. Qd2 Rd7 37. f3 Qg6 38. Kh2 Rf7 39. g4 Rd7 40. h5 Qf7 41. Kg3 Qf8 42. Re4 Bf7 43. Bh3 Kh7 44. Rce1 Rde7 45. Qc2 Re6 46. g5 Bxh5 47. Bxe6 Qxf3+ 48. Kh2 Bg6 49. Bh3 hxg5 50. Bg2 Qh5+ 51. Kg1 Re7 52. b5 axb5 53. a6 bxa6 54. Qxc6 Nb4 55. Qd6 Rf7 56. Qxb4 Bf5 57. R4e3 Qh4 58. Rf1 a5 59. Qb3 Rf8 60. Rh3 a4 61. Rxh4+ gxh4 62. Qe3 Kg6 63. Bd5 a3 64. Kh2 Rf6 65. Rg1+ Bg4 66. Rxg4+ Kh7 67. Rxh4+ Rh6 68. Rxh6+ gxh6 69. Qe4#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_16(self):
        moves = "1. d4 d5 2. c4 c6 3. Nf3 Nf6 4. Nc3 dxc4 5. a4 Bg4 6. Ne5 Bh5 7. g3 e6 8. Bg2 Nbd7 9. Nxc4 Bb4 10. a5 O-O 11. Qb3 Nd5 12. e4 Nxc3 13. Qxb4 Nb5 14. Be3 Rc8 15. Na3 Nxa3 16. Qxa3 b6 17. O-O Be2 18. Rfe1 Bb5 19. axb6 Nxb6 20. b3 a6 21. Rac1 Re8 22. Red1 Be2 23. Rd2 Bb5 24. Rdd1 Be2 25. Rd2 Bb5 26. Bf4 h6 27. h3 Ra8 28. Qa5 Ra7 29. h4 Rd7 30. Be3 Rb7 31. Rdd1 Be2 32. Re1 Bb5 33. Rcd1 Rb8 34. Bd2 Nd7 35. Qa3 Nf6 36. Ba5 Qc8 37. Qa1 Ra8 38. Qc3 Qb7 39. Qd2 Qd7 40. Bh3 Qb7 41. Rc1 Rac8 42. Bc3 Rb8 43. Kh2 Rbc8 44. Kg1 Rb8 45. Kh2 Rbc8 46. Rcd1 Qb6 47. Kg1 Qd8 48. Rc1 Qd7 49. Bb4 Ra8 50. Ba5 Ra7 51. Bb6 Raa8 52. Ba5 Ra7 53. Rc2 Rb7 54. f4 Qe7 55. g4 c5 56. g5 hxg5 57. hxg5 Nd7 58. d5 exd5 59. Qxd5 Nf8 60. Bf5 Ne6 61. Rh2 Qd7 62. Bh7+ Kf8 63. Bf5 Kg8 64. Kf2 Qxd5 65. Bh7+ Kf8 66. exd5 Nxf4 67. Be4 Ng6 68. d6 Rbb8 69. Bc7 Rbc8 70. Rhh1 Kg8 71. Re3 Nf8 72. Reh3 Ng6 73. Bd3 Bc6 74. R1h2 a5 75. Rh7 Ra8 76. d7 Bxd7 77. Bd6 f5 78. gxf6 Kf7 79. Rxg7+ Ke6 80. f7 Kxd6 81. fxe8=Q Bxe8 82. Bxg6 Bc6 83. Rh6 Rf8+ 84. Bf7+ Kc7 85. Ke3 Rd8 86. Bd5+ Bd7 87. Kd3 Kb8 88. Kc4 Kc8 89. Kxc5 Rf8 90. Rd6 Bg4 91. Kb6 Bd7 92. Rgxd7 Re8 93. Ra7 Kb8 94. Ra8#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_17(self):
        moves = "1. d4 Nf6 2. c4 c5 3. d5 d6 4. Nf3 g6 5. g3 e5 6. Nc3 Bg7 7. e4 Na6 8. h4 Nc7 9. Be2 a6 10. a4 a5 11. Nh2 h6 12. h5 Na6 13. Bf3 Qe7 14. Nb5 Bd7 15. Bd2 b6 16. Qe2 O-O-O 17. O-O-O Nb4 18. Nf1 Kb7 19. Ne3 Rdg8 20. Kb1 Kb8 21. Ng2 Rh7 22. Rdf1 Ka8 23. Bc3 Kb7 24. Qd1 Ka6 25. Ne3 Kb7 26. Bd2 Rhh8 27. Nc3 Ka6 28. Be1 Ka7 29. Ka1 Kb7 30. Qb1 Rh7 31. Bd1 Kb8 32. Nb5 Bh8 33. Bc3 Re8 34. Ng2 Rg8 35. Nh4 Ne8 36. hxg6 fxg6 37. f4 h5 38. Nf3 Bg7 39. Rh2 Rhh8 40. Rfh1 Kb7 41. Be2 Kb8 42. Rf1 Bxb5 43. axb5 Bf6 44. Rhf2 Ka8 45. Bd3 g5 46. fxe5 dxe5 47. Qd1 Rg7 48. Ne1 h4 49. g4 Rf7 50. Ng2 Rhf8 51. Ne3 Bh8 52. Nf5 Qd8 53. Bb1 Nd6 54. Qc1 Kb8 55. Re2 Nb7 56. Bd2 Rg8 57. Rf3 Rh7 58. Ref2 Ka7 59. b3 Rg6 60. Kb2 Rg8 61. Qf1 Qe8 62. Kc1 Bf6 63. Kd1 Bd8 64. Ke2 Qg6 65. Qg2 Re8 66. Kf1 Qg8 67. Ne3 Nd6 68. Kg1 Qh8 69. Qf1 Rd7 70. Bc3 Kb8 71. Rh2 Rh7 72. Bb2 Kc8 73. Kg2 Rd7 74. Nf5 Nb7 75. Kf2 Rf7 76. Ke2 Kb8 77. Rhf2 Rf6 78. Bc3 Ka7 79. Qc1 Rff8 80. Rf1 Rg8 81. Ne3 Nd6 82. Qb2 Bc7 83. R1f2 Rg6 84. Kf1 Bd8 85. Kg1 Kb8 86. Rf1 Ka7 87. Qh2 Kb8 88. Nf5 Nb7 89. Ng3 Nd6 90. Nh5 Kb7 91. Rf5 Nxf5 92. exf5 Rd6 93. f6 Bxf6 94. Be4 Qh6 95. Rf5 Bh8 96. Rf7+ Kb8 97. Qf2 Red8 98. Qf5 Nd3 99. Rh7 Qf8 100. Rxh8 Qxh8 101. Bxd3 Re8 102. Qf7 Rc8 103. Qe7 Qd8 104. Qxe5 Qf8 105. Nf6 Ka7 106. Qxg5 Rd7 107. Nxd7 Qf3 108. Ne5 Qg3+ 109. Kf1 Rf8+ 110. Ke2 Qg2+ 111. Kd1 Qg1+ 112. Be1 Re8 113. d6 Qg2 114. d7 Rxe5 115. Qf4 Qb2 116. d8=Q Qa1+ 117. Kd2 Qxe1+ 118. Kc2 Re2+ 119. Bxe2 Qxe2+ 120. Kc1 Qe1+ 121. Kb2 Qe2+ 122. Ka3 Qb2+ 123. Kxb2 h3 124. Qfb8#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_18(self):
        moves = "1. Nf3 g6 2. c4 Bg7 3. d4 d6 4. Nc3 Nd7 5. e4 e6 6. Be2 b6 7. O-O Bb7 8. Be3 Ne7 9. Qc2 h6 10. Qd2 f5 11. d5 e5 12. exf5 gxf5 13. Rae1 Nf6 14. Bd1 Ba6 15. b3 Ng6 16. Kh1 Bc8 17. Ng1 Bd7 18. a4 a6 19. f4 e4 20. b4 h5 21. c5 bxc5 22. bxc5 Ng4 23. c6 Bc8 24. Bxg4 hxg4 25. g3 a5 26. Nge2 Bxc3 27. Nxc3 Ba6 28. Nb5 Ne7 29. Bd4 Rh7 30. Qxa5 Bxb5 31. Qxb5 Qb8 32. Qb7 Nxd5 33. Rb1 Qc8 34. a5 Ne7 35. Bf6 Nd5 36. Bh4 Kf7 37. Rfd1 Qe6 38. Rb5 Kg6 39. Qxa8 e3 40. Rb2 Rxh4 41. Re1 Rh7 42. Qb8 Nf6 43. Kg1 Qd5 44. Qb5 Qd4 45. Rbe2 Rh8 46. Qb7 Qd5 47. Qxc7 Ra8 48. Qb6 Rxa5 49. c7 Rc5 50. Qb8 Qc4 51. c8=Q Rxc8 52. Qxd6 Re8 53. Qa3 Qd4 54. Qb2 Qa7 55. Rb1 Qa6 56. Qb5 Qc8 57. Rd1 Qc7 58. Qa6 Qb8 59. h4 gxh3 60. Rd6 Rf8 61. Rxe3 Rf7 62. Kh2 Kh7 63. Ree6 Qb2+ 64. Qe2 Ng4+ 65. Kxh3 Qh8 66. Rg6 Qa8 67. Rc6 Kh8 68. Qb2+ Kh7 69. Qb3 Qe8 70. Kh4 Rf8 71. Qe6 Qxe6 72. Rcxe6 Rf7 73. Kg5 Kh8 74. Re1 Nf2 75. Rf6 Rc7 76. Kxf5 Kg8 77. g4 Kg7 78. g5 Nd3 79. Re8 Rc5+ 80. Kg4 Rc7 81. f5 Rc4+ 82. Kf3 Rc3 83. Re7+ Kg8 84. Rd6 Ne5+ 85. Kf4 Nf7 86. Rxf7 Kxf7 87. g6+ Ke8 88. Ke5 Rc8 89. Ke6 Rc1 90. g7 Re1+ 91. Kf6 Rg1 92. Re6+ Kd7 93. Kf7 Rg5 94. g8=Q Rxg8 95. Kxg8 Kc7 96. f6 Kd7 97. Ra6 Kc7 98. f7 Kb7 99. Rf6 Ka7 100. f8=Q Kb7 101. Qe7+ Ka8 102. Rf8#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_19(self):
        moves = "1. Nf3 g6 2. c4 Bg7 3. d4 d6 4. Nc3 Nd7 5. e4 e6 6. Be2 b6 7. O-O Bb7 8. Be3 Ne7 9. Qc2 h6 10. Qd2 f5 11. d5 e5 12. exf5 gxf5 13. Rae1 Nf6 14. Bd1 Ba6 15. b3 Ng6 16. Kh1 Bb7 17. Bc2 Qd7 18. Ng1 Ng4 19. Bd1 Nf6 20. f3 Ne7 21. b4 f4 22. Ba4 c6 23. Bf2 O-O 24. Nh3 Kh8 25. Re2 Qc7 26. Rfe1 cxd5 27. c5 dxc5 28. Rxe5 Ne4 29. Rxe7 Qxe7 30. fxe4 dxe4 31. Nxf4 Rxf4 32. Qxf4 Bxc3 33. Qxh6+ Qh7 34. Qf4 Qh5 35. Bg3 Bd5 36. Bd1 Qg6 37. Qh4+ Kg8 38. Rf1 Bg7 39. Bh5 Qh6 40. Qg4 Be6 41. Qxe4 Rf8 42. Bf3 cxb4 43. Qxb4 Bxa2 44. Qa4 Be6 45. Bf2 Qd2 46. Qc6 Qd7 47. Qe4 Qc8 48. Rd1 Bb3 49. Rd6 Qc2 50. Qe3 Bf7 51. Bg1 Re8 52. Qg5 Qc7 53. Rd3 a5 54. Bd5 Bxd5 55. Qxd5+ Qf7 56. Qb5 Re6 57. Rd7 Qg6 58. Rc7 Re1 59. Qb3+ Kh8 60. Qh3+ Kg8 61. Rc8+ Re8 62. Qb3+ Kh7 63. Rc4 Re4 64. Qh3+ Kg8 65. Qd3 Re6 66. Qd5 Qf7 67. h3 Rg6 68. Rc8+ Bf8 69. Qd3 Rf6 70. Rc4 Rg6 71. Rh4 Qe6 72. Bf2 Qc6 73. Bg3 Bc5 74. Kh2 Be7 75. Rd4 Kf7 76. Qf1+ Kg7 77. Qe2 Kf8 78. Rf4+ Rf6 79. Rd4 Rg6 80. Qe5 Kf7 81. Rf4+ Bf6 82. Qf5 Qe6 83. Qd3 Rg5 84. Qh7+ Rg7 85. Qh5+ Rg6 86. Qh7+ Rg7 87. Qc2 Kg8 88. Re4 Qd5 89. Rc4 Bd4 90. Rc8+ Kf7 91. Qc7+ Kg6 92. Qf4 Bf6 93. Rh8 Kf7 94. Rb8 Qe6 95. Qc7+ Kg6 96. Rxb6 Rxc7 97. Rxe6 Rc4 98. Ra6 Kf5 99. Rxa5+ Ke6 100. Ra3 Kf5 101. Rf3+ Kg6 102. Bf2 Be5+ 103. g3 Rc2 104. h4 Bd4 105. Kg2 Kh5 106. Rf5+ Kh6 107. g4 Rb2 108. h5 Be3 109. Kg3 Bd2 110. Bd4 Rb3+ 111. Rf3 Be1+ 112. Bf2 Bxf2+ 113. Kxf2 Rb5 114. Rf6+ Kh7 115. Kg3 Kg7 116. Rc6 Ra5 117. Kh4 Kg8 118. h6 Kh7 119. g5 Ra2 120. Rc7+ Kg6 121. Rg7+ Kf5 122. h7 Ra1 123. Kg3 Ra3+ 124. Kf2 Ra2+ 125. Ke1 Ra8 126. Kd1 Rh8 127. g6 Kg5 128. Rg8 Rxg8 129. hxg8=R Kh4 130. g7 Kg3 131. Rf8 Kh4 132. g8=Q Kh5 133. Qg5+ Kxg5 134. Ke1 Kg4 135. Kf2 Kg5 136. Kg3 Kg6 137. Kg4 Kg7 138. Rf1 Kg6 139. Rf2 Kh6 140. Kf5 Kg7 141. Kg5 Kh7 142. Kf6 Kg8 143. Rh2 Kf8 144. Rh8#".split(" ")
        del moves[::3]
        self.rungame(moves)

    def test_20(self):
        moves = "1. e4 Nf6 2. e5 Nd5 3. d4 d6 4. Nf3 Bg4 5. Be2 c6 6. O-O Bxf3 7. Bxf3 dxe5 8. dxe5 e6 9. Qe2 Qc7 10. c4 Ne7 11. Nc3 Nd7 12. Bf4 Rd8 13. Rac1 Ng6 14. Bg3 Bc5 15. Kh1 O-O 16. Be4 Bd4 17. f4 Nc5 18. Bc2 Qe7 19. Be1 a5 20. Rb1 b6 21. a3 f5 22. exf6 Qxf6 23. g3 Ne7 24. g4 Ng6 25. f5 Ne7 26. b4 axb4 27. axb4 Bxc3 28. bxc5 Bxe1 29. Rfxe1 bxc5 30. Qxe6+ Rf7 31. Qe3 g5 32. Qh3 Rd6 33. Rb8+ Kg7 34. Re8 Rd7 35. Qe3 h6 36. h4 gxh4 37. Re2 Ra7 38. Kh2 Rd7 39. Kg2 h3+ 40. Kh2 Ng8 41. Re6 Qd8 42. g5 hxg5 43. f6+ Nxf6 44. Qxg5+ Kf8 45. R2e3 Ng8 46. Re8+ Qxe8 47. Rxe8+ Kxe8 48. Qxg8+ Ke7 49. Qg5+ Rf6 50. Be4 Rd6 51. Kxh3 Re6 52. Qxc5+ Kf7 53. Bf5 Re8 54. Kg4 Ra8 55. Kf4 Ra1 56. Qf2 Ke7 57. c5 Rh1 58. Kg5 Rhh6 59. Qd4 Kf7 60. Qe5 Kg7 61. Bb1 Kf7 62. Ba2+ Kf8 63. Qxf6+ Rxf6 64. Kxf6 Ke8 65. Ke6 Kd8 66. Kd6 Ke8 67. Kxc6 Ke7 68. Kd5 Kf6 69. c6 Ke7 70. Ke5 Kd8 71. Kd6 Ke8 72. c7 Kf8 73. Ke5 Kg7 74. c8=Q Kg6 75. Qg4+ Kh7 76. Kf6 Kh6 77. Qh4#".split(" ")
        del moves[::3]
        self.rungame(moves)
