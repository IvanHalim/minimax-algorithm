#ifndef AI_HPP
#define AI_HPP

#include "game.hpp"

struct AiMove
{
	AiMove() {};
	AiMove(int Score) : score(Score) {};
	int x;
	int y;
	int score;
};

class AI
{
	private:
		int aiPlayer;
		int humanPlayer;
	public:
		AI();
		int getAiPlayer();
		void initialize(int);
		void performMove(game&);
		AiMove getBestMove(game&, int);
};
#endif
