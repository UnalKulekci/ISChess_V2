
from .sas_constant import (
    PIECE_VALUES,
    pawn_evaluation_white, pawn_evaluation_black,
    knight_evaluation,
    bishop_evaluation_white, bishop_evaluation_black,
    rook_evaluation_white, rook_evaluation_black,
    queen_evaluation,
    king_evaluation_white, king_evaluation_black
)
from .sas_utils import is_square_empty, is_friendly_piece

def get_piece_value(piece, x, y):
    """
    Calculates both the material value and the positional value (PST) of a piece.
    """
    if is_square_empty(piece): 
        return 0
    
    # Get piece type and color
    if hasattr(piece, "type"):
        p_type = piece.type
        p_color = piece.color
    else:
        p_type = piece[0] # 'p' from 'pw'
        p_color = piece[1] # 'w' from 'pw'
    
    # 1. Material Value
    material_value = PIECE_VALUES.get(p_type, 0)
    
    # 2. Positional Value (Piece-Square Table)
    position_value = 0
    
    # Table Selection
    # Note: Matrix dimensions (8x8) must match table dimensions.
    try:
        if p_type == 'p':
            table = pawn_evaluation_white if p_color == 'w' else pawn_evaluation_black
        elif p_type == 'n':
            table = knight_evaluation # Knights are generally symmetric
        elif p_type == 'b':
            table = bishop_evaluation_white if p_color == 'w' else bishop_evaluation_black
        elif p_type == 'r':
            table = rook_evaluation_white if p_color == 'w' else rook_evaluation_black
        elif p_type == 'q':
            table = queen_evaluation # Queen table is generally symmetric
        elif p_type == 'k':
            # Endgame check can be added later, currently using standard table
            table = king_evaluation_white if p_color == 'w' else king_evaluation_black
        else:
            table = None

        if table is not None:
            # x = Row, y = Col
            position_value = table[x][y]
            
    except IndexError:
        # Prevent errors if board size is different from 8x8
        position_value = 0
    
    return material_value + position_value

def evaluate_board(board, my_color):
    """
    Evaluates the current state of the board.
    Positive Score (+) -> I am winning.
    Negative Score (-) -> Opponent is winning.
    """
    total_score = 0
    size_x, size_y = board.shape
    
    for x in range(size_x):
        for y in range(size_y):
            piece = board[x, y]
            
            # Skip empty squares
            if is_square_empty(piece):
                continue
                
            # Pass x, y coordinates as well
            val = get_piece_value(piece, x, y)
            
            # Add score if friendly piece, subtract if enemy
            if is_friendly_piece(piece, my_color):
                total_score += val
            else:
                total_score -= val
                    
    return total_score