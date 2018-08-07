/*********************************************************
 * Program Filename: game.cpp
 * Author: Iven Timothy Halim
 * Date: 07/06/2018
 * Description: This is the file that specifies the function for the game class
 * Input: None
 * Output: game class function
 * *******************************************************/
#include <iostream>
#include "game.hpp"

using std::cout;
using std::endl;

game::game()
{
	size = 3;
	board = new int*[size];
	for (int i=0;i<size;i++)
		board[i] = new int[size];
	for (int i=0;i<size;i++)
	{
		for (int j=0;j<size;j++)
			board[i][j] = 0;
	}
	turn = 1;
	wincon = 3;
	createPointArray();
}

int game::getTurn()
{
	return turn;
}

int game::getSize()
{
	return size;
}

int game::getValue(int i, int j)
{
	return board[i][j];
}

void game::setWinCondition(int w)
{
	wincon = w;
        deletePointArray();
	createPointArray();
}

void game::setBoard(int s)
{
	for (int i=0;i<size;i++)
		delete[] board[i];
	delete[] board;
	deletePointArray();
	board = new int*[s];
	for (int i=0;i<s;i++)
		board[i] = new int[s];
	for (int i=0;i<s;i++)
	{
		for (int j=0;j<s;j++)
			board[i][j] = 0;
	}
	turn = 1;
	size = s;
	wincon = s;
	createPointArray();
}

void game::deletePointArray()
{
	for (int i=0;i<size;i++)
		delete[] pointArray[i];
	delete[] pointArray;
}

/***************************************************
 * Function: createPointArray()
 * Description: This function creates the dynamic pointArray in the private data
   The pointArray is used to assigns grades to each square in the board based on
   the relative value of the square
 * Parameters: None
 * Pre-Conditions: the pointArray has been deleted. The new board size has been set.
 * Post-Conditions: The pointArray dynamic array has been created with the same size
   as the board
****************************************************/
void game::createPointArray()
{
	pointArray = new int*[size];
        for (int i=0;i<size;i++)
                pointArray[i] = new int[size];
        for (int i=0;i<size;i++)
	{
                for (int j=0;j<size;j++)
                        pointArray[i][j] = 0;
        }
        for (int x=0;x<size-wincon+1;x++)
        {
                for (int i=0;i<wincon;i++)
                {
                        for (int j=0;j<size;j++)
                                pointArray[x+i][j]++;
                }
        }

        for (int y=0;y<size-wincon+1;y++)
        {
                for (int j=0;j<wincon;j++)
                {
                        for (int i=0;i<size;i++)
                                pointArray[i][y+j]++;
                }
        }

        for (int k=0;k<size-1;k++)
        {
                for (int x=0;x<size-wincon-k+1;x++)
                {
                        for (int i=0;i<wincon;i++)
                        {
                                pointArray[i+x+k][i+x]++;
                                pointArray[i+x][i+x+k]++;
                                pointArray[i+x][size-1-i-x-k]++;
                                pointArray[i+x+k][size-1-i-x]++;
                        }
                }
        }

        for (int x=0;x<size-wincon+1;x++)
        {
                for (int i=0;i<wincon;i++)
                {
                        pointArray[i+x][i+x]--;
                        pointArray[i+x][size-1-i-x]--;
                }
        }
}

void game::printBoard()
{
	cout << " ";
	for (int i=0;i<size;i++)
		cout << " " << i;
	cout << endl;
	for (int i=0;i<size;i++)
	{
		cout << i << " ";
		for (int j=0;j<size;j++)
		{
			if (board[i][j] == 0)
				cout << ". ";
			else if (board[i][j] == 1)
				cout << "x ";
			else if (board[i][j] == 2)
				cout << "o ";
		}
		cout << endl;
	}
}

void game::printPointArray()
{
	cout << " ";
        for (int i=0;i<size;i++)
                cout << " " << i;
        cout << endl;
        for (int i=0;i<size;i++)
        {
                cout << i << " ";
                for (int j=0;j<size;j++)
                {
                        cout << pointArray[i][j] << " ";
                }
                cout << endl;
        }
}

/***********************************************************
 * Function: checkForFull()
 * Description: This function checks whether all the squares on the board has been filled
 * Parameters: None
 * Pre-Condition: The board array has been created and initialized
 * Post-Condition: Correctly checks if the board is full
 * ********************************************************/
bool game::checkForFull()
{
	bool full = true;
	for (int i=0;i<size;i++)
	{
		for (int j=0;j<size;j++)
		{
			if (board[i][j] == 0)
				full = false;
		}
	}

	return full;
}

/***********************************************************
 * Function: checkBoardSize
 * Description: This function sanitize the user entered board size. It checks whether the board
   size is valid (that is between 2 and 10
 * Parameters: user entered integer s
 * Pre-Condition: None
 * Post-condition: Return true if the input is valid, false if the input is invalid
 * ********************************************************/
bool game::checkBoardSize(int s)
{
	bool legal = true;

	if (s < 2)
	{
		cout << "Board size must be at least 2" << endl;
		legal = false;
	}
	if (s > 10)
	{
		cout << "Board size cannot be greater than 10" << endl;
		legal = false;
	}

	return legal;
}

/***********************************************************
 * Function: checkWinCondition
 * Description: This function sanitize the user entered win condition. It checks wheter the win
   condition is valid (that is between 2 and the board size)
 * Parameters: user entered integer w
 * Pre-Condition: The board size has been initialized
 * Post-condition: Return true if the input is valid, false if the input is invalid
 * ********************************************************/
bool game::checkWinCondition(int w)
{
	bool legal = true;

	if (w < 2)
	{
		cout << "Win condition must be at least 2" << endl;
		legal = false;
	}

	else if (w > size)
	{
		cout << "Win condition cannot be greater than board size" << endl;
		legal = false;
	}

	return legal;
}

/***************************************************************************
 * Function: checkForWin
 * Description: This function checks if a player has won the game
 * Parameter: None
 * Pre-condition: The board array and the turn number has been declared and initialized
 * Post-condition: Return 2 if player 2 won, 1 if player 1 won, -1 if it's a draw, 0 if the game is not over
 * *************************************************************************/
int game::checkForWin()
{
	int win = 0;
	int sum;

	//Check the horizontal portion
	for (int i=0;i<size;i++)
	{
		sum = 0;
		for (int j=1;j<size;j++)
		{
			if (board[i][j] == board[i][j-1] && board[i][j] != 0)
				sum++;
			else if (sum < wincon - 1)
				sum = 0;
		}
		if (sum >= wincon - 1)
		{
			if (turn == 1)
				win = 2;
			else
				win = 1;
		}
	}

	//Check the vertical portion
	for (int j=0;j<size;j++)
	{
		sum = 0;
		for (int i=1;i<size;i++)
		{
			if (board[i][j] == board[i-1][j] && board[i][j] != 0)
				sum++;
			else if (sum < wincon - 1)
				sum = 0;
		}
		if (sum >= wincon - 1)
		{
			if (turn == 1)
				win = 2;
			else
				win = 1;
		}
	}

	//Check the first diagonal
	for (int k=0;k<size-1;k++)
	{
		sum = 0;
		for (int i=1;i<size-k;i++)
		{
			if (board[i][i+k] == board[i-1][i-1+k] && board[i][i+k] != 0)
				sum++;
			else if (sum < wincon - 1)
				sum = 0;
		}
		if (sum >= wincon - 1)
		{
			if (turn == 1)
				win = 2;
			else
				win = 1;
		}
		sum = 0;
		for (int j=1;j<size-k;j++)
		{
			if (board[j+k][j] == board[j-1+k][j-1] && board[j+k][j] != 0)
				sum++;
			else if (sum < wincon - 1)
				sum = 0;
		}
		if (sum >= wincon - 1)
		{
			if (turn == 1)
				win = 2;
			else
				win = 1;
		}
	}

	//Check the second diagonal
	for (int k=0;k<size-1;k++)
	{
		sum = 0;
		for (int i=1;i<size-k;i++)
		{
			if (board[i][size-1-i-k] == board[i-1][size-1-(i-1)-k] && board[i][size-1-i-k] != 0)
				sum++;
			else if (sum < wincon - 1)
				sum = 0;
		}
		if (sum >= wincon - 1)
		{
			if (turn == 1)
				win = 2;
			else
				win = 1;
		}
		sum = 0;
		for (int j=1;j<size-k;j++)
		{
			if (board[j+k][size-1-j] == board[j-1+k][size-1-(j-1)] && board[j+k][size-1-j] != 0)
				sum++;
			else if (sum < wincon - 1)
				sum = 0;
		}
		if (sum >= wincon - 1)
		{
			if (turn == 1)
				win = 2;
			else
				win = 1;
		}
	}

	//If the board is full and nobody has won then it's a raw
	if (win == 0 && checkForFull() == true)
		win = -1;

	return win;
}

/***********************************************************************
 * Function: checkForLegal
 * Description: This function checks whether the move is legal, that is if the square is
   inside the board and the square is empty
 * Parameter: User entered integer of the square where the user wants to place a piece
 * Pre-Condition: The board array and the size number has been declared and initialized
 * Post-Condition: Return true if the move is legal, false if the move is illegal
 * *********************************************************************/
bool game::checkForLegal(int input)
{
	bool legal = true;
	int x = input/10;
	int y = (input+10)%10;

	if (input < 0)
		legal = false;
	else if (x>(size-1) || y>(size-1))
		legal = false;
	else if (board[x][y] != 0)
		legal = false;

	return legal;
}

/******************************************************************
 * Function: placePiece
 * Description: This function place a piece on the square that the user specify
   The value of the piece is automatically determined based on the turn number
 * Parameters: User-entered integer (12 for row 1 and column 2)
 * Pre-Condition: The input value has been sanitized
 * Post-condition: The piece has been placed on the square
 * ****************************************************************/
void game::placePiece(int input)
{
	int x = input/10;
	int y = (input+10)%10;

	board[x][y] = turn;

	turn++;
	if (turn > 2)
		turn = 1;
}

/***********************************************************************
 * Function: setValue
 * Description: This function place a piece on a square. Unlike the placePiece function
   the value of the piece is not automatically determined based on the turn number
 * Parameters: Integer i for row, integer j for column, integer value for the value of the piece
 * Pre-Condition: The parameters has been sanitized so that it is legal
 * Post-Condition: The piece has been placed on the square
 * ********************************************************************/
void game::setValue(int i, int j, int value)
{
	board[i][j] = value;

	turn++;
	if (turn > 2)
		turn = 1;
}

/*************************************************************************
 * Function: checkForThreat
 * Description: This function checks whether a player threatens to win on the spot
 * Parameters: player number, varible a for the returned row number, variable b for the returned column number,
   integer w for the win condition
 * Pre-Condition: The board array and the pointArray has been created and sanitized
 * Post-Condition: Return false if there is no threat, return true if there is a threat and it also returns
   the row number and the column number of where the player should place a piece in order to prevent the threat
*************************************************************************/
bool game::checkForThreat(int player, int& a, int& b, int w)
{
	bool threat = false;
	int sum = 0;
	int max = w-1;
	int max2 = 0;

	//Checks the diagonals in the south east direction
	for (int k=0;k<size-1;k++)
        {
                for (int x=0;x<size-wincon-k+1;x++)
                {
			sum = 0;
                        for (int i=0;i<wincon;i++)
                        {
                                if (board[i+x+k][i+x] != player && board[i+x+k][i+x] != 0)
					sum++;
				else if (board[i+x+k][i+x] == player)
					sum-=10;
			}
			if (sum > max)
			{
				max = sum;
				max2 = 0;
                                for (int i=0;i<wincon;i++)
                                {
                                        if (board[i+x+k][i+x] == 0 && pointArray[i+x+k][i+x] > max2)
                                        {
						max2 = pointArray[i+x+k][i+x];
                                                a = i+x+k;
                                                b = i+x;
                                        }
                                }
                                threat = true;
                        }
			sum = 0;
			for (int i=0;i<wincon;i++)
			{
                               	if (board[i+x][i+x+k] != player && board[i+x][i+x+k] != 0)
					sum++;
				else if (board[i+x][i+x+k] == player)
					sum-=10;
			}
			if (sum > max)
			{
				max = sum;
				max2 = 0;
                                for (int i=0;i<wincon;i++)
                                {
                                        if (board[i+x][i+x+k] == 0 && pointArray[i+x][i+x+k] > max2)
                                        {
						max2 = pointArray[i+x][i+x+k];
                                                a = i+x;
                                                b = i+x+k;
                                        }
                                }
                                threat = true;
                        }
                }
        }

	//Check the diagonals in the north east direction
        for (int k=0;k<size-1;k++)
        {
                for (int x=0;x<size-wincon-k+1;x++)
                {
			sum = 0;
                        for (int i=0;i<wincon;i++)
                        {
                                if (board[i+x][size-1-i-x-k] != player && board[i+x][size-1-i-x-k] != 0)
					sum++;
				else if (board[i+x][size-1-i-x-k] == player)
					sum-=10;
			}
			if (sum > max)
			{
				max = sum;
				max2 = 0;
                                for (int i=0;i<wincon;i++)
                                {
                                        if (board[i+x][size-1-i-x-k] == 0 && pointArray[i+x][size-1-i-x-k] > max2)
                                        {
						max2 = pointArray[i+x][size-1-i-x-k];
                                                a = i+x;
                                                b = size-1-i-x-k;
                                        }
                                }
                                threat = true;
                        }
			sum = 0;
			for (int i=0;i<wincon;i++)
			{
                                if (board[i+x+k][size-1-i-x] != player && board[i+x+k][size-1-i-x] != 0)
					sum++;
				else if (board[i+x+k][size-1-i-x] == player)
					sum-=10;
			}
			if (sum > max)
			{
				max = sum;
				max2 = 0;
                                for (int i=0;i<wincon;i++)
                                {
                                        if (board[i+x+k][size-1-i-x] == 0 && pointArray[i+x+k][size-1-i-x] > max2)
                                        {
						max2 = pointArray[i+x+k][size-1-i-x];
                                                a = i+x+k;
                                                b = size-1-i-x;
                                        }
                                }
                                threat = true;
                        }
                }
        }

	//Check the verticals
	for (int j=0;j<size;j++)
        {
                for (int x=0;x<size-wincon+1;x++)
                {
                        sum = 0;
                        for (int i=0;i<wincon;i++)
                        {
                                if (board[x+i][j] != player && board[x+i][j] != 0)
                                        sum++;
                                else if (board[x+i][j] == player)
                                        sum-=10;
                        }
                        if (sum > max)
                        {
                                max = sum;
                                max2 = 0;
                                for (int i=0;i<wincon;i++)
                                {
                                        if (board[x+i][j] == 0 && pointArray[x+i][j] > max2)
                                        {
                                                max2 = pointArray[x+i][j];
                                                a = x+i;
                                                b = j;
                                        }
                                }
                                threat = true;
                        }
                }
        }

	//Check the horizontals
	for (int i=0;i<size;i++)
        {
                for (int y=0;y<size-wincon+1;y++)
                {
                        sum = 0;
                        for (int j=0;j<wincon;j++)
                        {
                                if (board[i][y+j] != player && board[i][y+j] != 0)
                                        sum++;
                                else if (board[i][y+j] == player)
                                        sum-=10;
                        }
                        if (sum > max)
                        {
                                max = sum;
                                max2 = 0;
                                for (int j=0;j<wincon;j++)
                                {
                                        if (board[i][y+j] == 0 && pointArray[i][y+j] > max2)
                                        {
                                                max2 = pointArray[i][y+j];
                                                a = i;
                                                b = y+j;
                                        }
                                }
                                threat = true;
                        }
                }
        }

	return threat;
}

/*********************************************************************************
 * Function: performMove
 * Description: This function performs the move that the computer considers is the best move
 * Parameters: None
 * Pre-Condition: the board array, pointArray and the turn number has been declared and initialized
 * Post-Condition: A piece has been placed on the square that the computer considers as the best move
 * ******************************************************************************/
void game::performMove()
{
	int max = 0;
	int a = -1;
	int b = -1;
	int player = turn;
	int opponent;
	if (player == 1)
		opponent = 2;
	else
		opponent = 1;

	checkForThreat(opponent, a, b, wincon-1);
	if (a == -1)
	{
		checkForThreat(player, a, b, wincon-1);
		if (a == -1)
		{
			checkForThreat(opponent, a, b, wincon-2);
			if (a == -1)
			{
				checkForThreat(player, a, b, wincon-2);
				if (a == -1)
				{
					for (int i=0;i<size;i++)
					{
						for (int j=0;j<size;j++)
						{
							if (pointArray[i][j] > max && board[i][j] == 0)
							{
								max = pointArray[i][j];
								a = i;
								b = j;
							}
						}
					}
				}
			}
		}
	}

	setValue(a, b, player);
}

game::~game()
{
	for (int i=0;i<size;i++)
	{
		delete[] board[i];
		delete[] pointArray[i];
	}
	delete[] board;
	delete[] pointArray;
}
