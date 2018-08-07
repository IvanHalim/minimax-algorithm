/*********************************************
 * Program Filename: main.cpp
 * Author: Ivan Timothy Halim
 * Date: 07/06/2018
 * Description: This is the main file for the Tic Tac Toe program
 * Input: Action command
 * Output: Playable Tic Tac Toe game
*********************************************/

#include <iostream>
#include <limits>
#include "game.hpp"
#include "AI.hpp"

using std::cin;
using std::cout;
using std::endl;

/********************************************
 * Function: clearInput()
 * Description: This function resets the cin to prevent infinite loop due to invalid input
 * Parameters: None
 * Pre-Conditions: None
 * Post-Condition: cin working properly again
*********************************************/
void clearInput()
{
	cin.clear();
	cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
}

int main()
{
	//Declare all variables
	int input;
	game TicTac;
	bool repeat;
	bool multiplayer = true;
	int aiPlayer;
	int a, b;

	//Introduction
	cout << "Welcome to Tic-Tac-Toe!" << endl;
	cout << "Press [enter] to continue" << endl;
	clearInput();

	//This do-while loop prompts the user to enter the board size and the win condition of the game
	//Then it's going to set the board according to the user-entered values
	do
	{
		do
		{
			repeat = false;
			cout << "Please enter board size:" << endl;
			cin >> input;
			if (cin.fail() || TicTac.checkBoardSize(input) == false)
				repeat = true;

			clearInput();
			
		}while(repeat);
		TicTac.setBoard(input);

		cout << "What is the win condition? (i.e. 3 for 3-in-a-row, 5 for 5-in-a-row)" << endl;
		cin >> input;
		if (cin.fail() || TicTac.checkWinCondition(input) == false)
			repeat = true;

		clearInput();
		
	}while(repeat);
	TicTac.setWinCondition(input);

	//This do-while loop prompts the user whether they want to play against a computer opponent
	//Then it prompts them whether they want to go first or second
	do
	{
		do
		{
			repeat = false;
			cout << "Do you want to play against a computer? (1 for yes, 0 for no)" << endl;
			cin >> input;
			if (cin.fail() || input > 1 || input < 0)
			{
				cout << "Sorry I don't get that" << endl;
				repeat = true;
			}

			clearInput();
		}while(repeat);
		if (input == 1)
			multiplayer = false;

		if (!multiplayer)
		{
			cout << "Do you want to play first or second? (1 for first, 2 for second)" << endl;
			cin >> input;
			if (cin.fail() || input > 2 || input < 1)
			{
				cout << "Sorry I don't get that" << endl;
				repeat = true;
			}
			clearInput();
		}
	}while(repeat);

	//This if function initialize the aiPlayer depending on the user input
	//If the aiPlayer is going second then set the aiPlayer as 2
	//If the aiPlayer is going first then set the aiPlayer as 1
	//If the aiPlayer is not playing then set the aiPlayer as 0
	if (!multiplayer)
	{
		if (input == 1)
			aiPlayer = 2;
		else
			aiPlayer = 1;
	}
	else
		aiPlayer = 0;

	//This do-while loop runs the Tic Tac Toe game
	do
	{
		//If it is the computer's turn then it calls the performMove function
		if (TicTac.getTurn() == aiPlayer)
			TicTac.performMove();

		//If it is not the computer's turn then it prompts the user to enter an input
		//The input specifies where they want to place the piece
		else
		{
			TicTac.printBoard();
			if (multiplayer)
				cout << "Player " << TicTac.getTurn() << "'s Turn" << endl;
			else
				cout << "Your Turn" << endl;

			do
			{
				repeat = false;
				cout << "Place your piece (ex. 00, 21)" << endl;
				cin >> input;

				if (cin.fail() || TicTac.checkForLegal(input) == false)
				{
					cout << "That move is illegal" << endl;
					repeat = true;
				}
				clearInput();

			}while(repeat);

			TicTac.placePiece(input);
		}
	}while(TicTac.checkForWin() == 0);
	cout << endl;

	//This if function checks who wins the game
	if (TicTac.checkForWin() == -1)
		cout << "It's a Draw!" << endl;
	else if (multiplayer)
		cout << "Player " << TicTac.checkForWin() << " Wins! Congratulations!" << endl;
	else if (TicTac.checkForWin() == aiPlayer)
		cout << "You lose. Better luck next time." << endl;
	else
		cout << "You Win! Congratulations!" << endl;

	TicTac.printBoard();
	cin.get();

	return 0;
}
