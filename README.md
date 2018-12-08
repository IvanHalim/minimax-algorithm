## TicTacToe with Minimax Algorithm
This is a simple code that allows you to play a game of Tic-Tac-Toe or Five-In-A-Row against an AI opponent. However, the objective of this project is not the game itself but to gain a basic understanding of the minimax algorithm.

## Minimax
Minimax is a decision-making algorithm, typically used in a turn-based, two player games. The goal of the algorithm is to find the optimal next move. In the algorithm, one player is called the maximizer, and the other player is a minimizer. If we assign an evaluation score to the game board, one player tries to choose a game state with the maximum score, while the other chooses a state with the minimum score.

In other words, the maximizer works to get the highest score, while the minimizer tries get the lowest score by trying to counter moves.

## Things that I learned while doing this project
While doing this project I find that the minimax algorithm works perfectly for a 3x3 Tic-Tac-Toe game. However, when playing the Five-In-A-Row game on a 10x10 board, the algorithm takes a very long time to find the optimal move because the number of possibilities is too high even for a computer.

## Solution
To solve this, I use a strategy called "Weighted Squares". In this strategy, the evaluation function assign points to each square based on its position on the board. Central squares are weighted highly, because it can go in any direction, while edges and corners are assigned a low score because it is not as flexible.

## Limitation of Solution
There are several problems with the "Weighted Squares" strategy. Firstly, this is not an accurate representation because the goal of the game is to form a connected line regardless of its position on the board. Secondly, sometimes the best move in a position is to make a move on a square that has a low score. The computer is unable to detect this.

## Alternative Solutions
An alternative solution would be to use the alpha-beta pruning to decrease the number of nodes that are evaluated by the minimax algorithm. Another solution is to modify the evaluation function so as to handle exception cases.
