/********************************************
 * Program Filename: game.hpp
 * Author: Ivan Timothy Halim
 * Date: 07/06/2018
 * Description: This is the header file for the game class
 * Input: None
 * Output: Declarations for the game class
 * ******************************************/
#ifndef GAME_HPP
#define GAME_HPP

class game
{
	protected:
		int** board;
		int turn;
		int size;
		int wincon;
		int** pointArray;
		int a, b;
	public:
		game();
		~game();
		int getTurn();
		int getSize();
		int getValue(int,int);
		void setBoard(int);
		void setWinCondition(int);
		void printBoard();
		void printPointArray();
		void deletePointArray();
		void createPointArray();
		void placePiece(int);
		void setValue(int,int,int);
		void performMove();
		int checkForWin();
		bool checkForLegal(int);
		bool checkForFull();
		bool checkBoardSize(int);
		bool checkWinCondition(int);
		bool checkForThreat(int,int&,int&,int);
};
#endif
