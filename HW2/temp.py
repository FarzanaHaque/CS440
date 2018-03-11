def alphabeta_vs_minimax():
    # Initialize board
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")

    # Load Agents
    player1 = MiniMaxAgent('R', 'B', True, 'AlphaBeta')
    player2 = MiniMaxAgent('B', 'R', False, 'MiniMax')

    # Play
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")

    # Print Winner
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()

    player1.print_nodes_expanded()
    player2.print_nodes_expanded()

def minimax_vs_alphabeta():
    # Initialize board
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")

    # Load Agents
    player1 = MiniMaxAgent('R', 'B', False, 'MiniMax')
    player2 = MiniMaxAgent('B', 'R', True, 'AlphaBeta')

    # Play
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")

    # Print Winner
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()

    player1.print_nodes_expanded()
    player2.print_nodes_expanded()


def alphabeta_vs_reflex():
    # Initialize board
    b = Board()
    print("Initial State")
    print("------------------------------")
    b.print_board()
    print("")

    # Load Agents
    player1 = MiniMaxAgent('R', 'B', True, 'AlphaBeta')
    player2 = ReflexAgent('B', 'R')


    # Play
    while b.winner == '.':
        print("Turn " + str(b.turn_number))
        print("------------------------------")
        player1.make_move(b)
        player2.make_move(b)
        b.print_board()
        b.turn_number += 1
        print("")

    # Print Winner
    print("Finished! Winner is " + b.winner)
    print("------------------------------")
    b.print_board()
