def make_move(move, board):
    """
    Hamleyi tahta üzerinde uygular ve varsa yenen taşı geri döndürür.
    
    Parametreler:
    move: ((start_x, start_y), (end_x, end_y)) formatında tuple.
    board: Satranç tahtası nesnesi.
    
    Dönüş:
    captured_piece: Hedef karede yenen taş (veya boşsa None/0).
    """
    start_pos, end_pos = move[0], move[1]
    
    # 1. Gidilen karedeki taşı sakla (Geri alma işlemi için kritik!)
    captured_piece = board[end_pos[0], end_pos[1]]

    # 2. Taşı yeni yerine taşı
    board[end_pos[0], end_pos[1]] = board[start_pos[0], start_pos[1]]
    
    # 3. Eski yeri boşalt (None yapıyoruz)
    board[start_pos[0], start_pos[1]] = None 
    
    return captured_piece

def undo_move(move, captured_piece, board):
    """
    Yapılan hamleyi geri alır ve tahtayı eski haline getirir.
    
    Parametreler:
    move: Geri alınacak hamle.
    captured_piece: make_move fonksiyonundan dönen yenen taş.
    board: Satranç tahtası nesnesi.
    """
    start_pos, end_pos = move[0], move[1]
    
    # 1. Bizim taşı hedef kareden alıp eski yerine (start_pos) geri koy
    board[start_pos[0], start_pos[1]] = board[end_pos[0], end_pos[1]]
    
    # 2. Hedef kareye (end_pos), sakladığımız yenen taşı geri koy
    board[end_pos[0], end_pos[1]] = captured_piece