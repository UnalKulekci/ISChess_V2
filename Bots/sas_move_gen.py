# Dosya Adı: move_gen.py

from .sas_constant import ORTHOGONAL, DIAGONAL, KNIGHT_DIRS, KING_DIRS
from .sas_utils import is_friendly_piece, is_enemy_piece, is_square_empty
# from ChessRules import move_is_valid

def get_sliding_moves(board, pos, directions, color, size_x, size_y):
    moves = []
    x, y = pos
    
    for dx, dy in directions:
        for step in range(1, max(size_x, size_y)):
            tx, ty = x + (step * dx), y + (step * dy)
            
            if not (0 <= tx < size_x and 0 <= ty < size_y):
                break
            
            target = board[tx, ty]
            
            if is_friendly_piece(target, color):
                break

            moves.append(((x, y), (tx, ty)))
            
            if is_enemy_piece(target, color):
                break
                
    return moves

def get_stepping_moves(board, pos, offsets, color, size_x, size_y):
    moves = []
    x, y = pos
    
    for dx, dy in offsets:
        tx, ty = x + dx, y + dy
        
        if 0 <= tx < size_x and 0 <= ty < size_y:
            target = board[tx, ty]
            if not is_friendly_piece(target, color):
                moves.append(((x, y), (tx, ty)))
                
    return moves

def get_pawn_moves(board, pos, color, size_x, size_y):
    moves = []
    x, y = pos
    
    dx = 1 

    fwd_x = x + dx
    if 0 <= fwd_x < size_x:
        if is_square_empty(board[fwd_x, y]):
            moves.append(((x, y), (fwd_x, y)))
            
    capture_offsets = [(dx, -1), (dx, 1)]
    for cx, cy in capture_offsets:
        cap_x, cap_y = x + cx, y + cy
        
        if 0 <= cap_x < size_x and 0 <= cap_y < size_y:
            target = board[cap_x, cap_y]
            
            if is_enemy_piece(target, color):
                moves.append(((x, y), (cap_x, cap_y)))

    return moves

def get_all_moves(board, player_sequence):
    my_color = player_sequence[1]
    size_x, size_y = board.shape
    
    capture_moves = []
    quiet_moves = []

    for x in range(size_x):
        for y in range(size_y):
            piece = board[x, y]
            
            if not is_friendly_piece(piece, my_color):
                continue

            p_type = piece.type if hasattr(piece, "type") else piece[0]
            
            candidate_moves = []
            
            match p_type:
                case 'r': candidate_moves = get_sliding_moves(board, (x, y), ORTHOGONAL, my_color, size_x, size_y)
                case 'b': candidate_moves = get_sliding_moves(board, (x, y), DIAGONAL, my_color, size_x, size_y)
                case 'q': candidate_moves = get_sliding_moves(board, (x, y), ORTHOGONAL + DIAGONAL, my_color, size_x, size_y)
                case 'n': candidate_moves = get_stepping_moves(board, (x, y), KNIGHT_DIRS, my_color, size_x, size_y)
                case 'k': candidate_moves = get_stepping_moves(board, (x, y), KING_DIRS, my_color, size_x, size_y)
                case 'p': candidate_moves = get_pawn_moves(board, (x, y), my_color, size_x, size_y)
                case _: continue
            
            for move in candidate_moves:
                target_x, target_y = move[1]
                target_piece = board[target_x, target_y]
                
                if is_enemy_piece(target_piece, my_color):
                    capture_moves.append(move)
                else:
                    quiet_moves.append(move)
                        
    return capture_moves, quiet_moves