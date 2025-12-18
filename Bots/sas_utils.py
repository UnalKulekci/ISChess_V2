def is_square_empty(piece):
    """
    Bir karenin boş olup olmadığını kontrol eder.
    None, boş string '' veya 'X' boş kabul edilir.
    """
    return piece in (None, '', 'X')

def is_friendly_piece(piece, my_color):
    """
    Verilen taşın (piece) benim rengimde (my_color) olup olmadığını kontrol eder.
    """
    if is_square_empty(piece): 
        return False
    
    # Eğer taş bir nesne (Object) ise .color özelliğine bak
    if hasattr(piece, "color"):
        p_color = piece.color
    else:
        # Eğer taş bir string ise (örn: "wp"), son karaktere bak ('w' veya 'b')
        p_color = piece[-1]
        
    return p_color == my_color

def is_enemy_piece(piece, my_color):
    """
    Verilen taşın rakip taş olup olmadığını kontrol eder.
    (Boş değilse ve dost değilse, rakiptir).
    """
    if is_square_empty(piece): 
        return False
    return not is_friendly_piece(piece, my_color)