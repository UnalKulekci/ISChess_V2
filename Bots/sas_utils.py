# To check if a square is empty
def is_square_empty(piece):
      return piece in (None, '', 'X', '--')

# To check if a piece is friendly
def is_friendly_piece(piece, my_color):
 
    if is_square_empty(piece): 
        return False
    
    if hasattr(piece, "color"):
        p_color = piece.color
    else:
        p_color = piece[-1]
        
    return p_color == my_color

# To check if a piece is enemy
def is_enemy_piece(piece, my_color):
    if is_square_empty(piece): 
        return False
    return not is_friendly_piece(piece, my_color)