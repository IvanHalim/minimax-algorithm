## TicTacToe with Minimax Algorithm
This is a simple code that allows you to play a game of Tic-Tac-Toe or Five-In-A-Row against an AI opponent. However, the objective of this project is not the game itself but to gain a basic understanding of the minimax algorithm.

## Minimax
Minimax is a decision-making algorithm, typically used in a turn-based, two player games. The goal of the algorithm is to find the optimal next move. In the algorithm, one player is called the maximizer, and the other player is a minimizer. If we assign an evaluation score to the game board, one player tries to choose a game state with the maximum score, while the other chooses a state with the minimum score.

In other words, the maximizer works to get the highest score, while the minimizer tries get the lowest score by trying to counter moves.

## Things that I learned while doing this project
While doing this project I find that the minimax algorithm works perfectly for a 3x3 Tic-Tac-Toe game. However, when playing the Five-In-A-Row game on a 10x10 board, the algorithm takes forever to find the optimal move because the number of possibilities is simply too high even for a computer.

## Solution
To solve this, I implemented a heuristic algorithm that would give a good but not optimal solution in a reasonably short amount of time. This is done by creating a scoring system for the computer to use based on my understanding of the game.

## Limitation of Solution
As I said previously, the heuristic algorithm is based on my personal understanding of the game and therefore not the absolute best solution out of all possible solutions. In other words, it will find only local optima and not the global optimum.

## Alternative Solutions
Some alternative solutions would be to use the alpha-beta pruning mechanism or to make the algorithm non-recursive to improve performance.
