#include "AI.hpp"
#include <vector>

using std::vector;

AI::AI()
{
	aiPlayer = 0;
	humanPlayer = 0;
}

void AI::initialize(int player)
{
	aiPlayer = player;
	if (aiPlayer == 1)
		humanPlayer = 2;
	else
		humanPlayer = 1;
}

int AI::getAiPlayer()
{
	return aiPlayer;
}

void AI::performMove(game& game)
{
	AiMove bestMove = getBestMove(game, aiPlayer);
	game.setValue(bestMove.x, bestMove.y, aiPlayer);
}

AiMove AI::getBestMove(game& game, int player)
{
	//Base case, check for end state
	int rv = game.checkForWin();
	if (rv == aiPlayer)
	{
		return AiMove(10);
	}
	else if (rv == humanPlayer)
	{
		return AiMove(-10);
	}
	else if (rv == -1)
	{
		return AiMove(0);
	}
	
	vector<AiMove> moves;

	//Do the recursive function calls and construct the moves vector
	for (int i=0;i<game.getSize();i++)
	{
		for (int j=0;j<game.getSize();j++)
		{
			if (game.getValue(i, j) == 0)
			{
				AiMove move;
				move.x = i;
				move.y = j;
				game.setValue(i, j, player);

				if (player == aiPlayer)
					move.score = getBestMove(game, humanPlayer).score;
				else
					move.score = getBestMove(game, aiPlayer).score;
				moves.push_back(move);
				game.setValue(i, j, 0);
			}
		}
	}

	//Pick the best move for the current player
	int bestMove = 0;
	if (player == aiPlayer)
	{
		int bestScore = -1000000;
		for (int i=0;i<moves.size();i++)
		{
			if (moves[i].score > bestScore)
			{
				bestMove = i;
				bestScore = moves[i].score;
			}
		}
	}
	else
	{
		int bestScore = 1000000;
		for (int i=0;i<moves.size();i++)
		{
			if (moves[i].score < bestScore)
			{
				bestMove = i;
				bestScore = moves[i].score;
			}
		}
	}

	//return the best move
	return moves[bestMove];
}
