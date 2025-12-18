from Bots.ChessBotList import register_chess_bot
from ChessRules import move_is_valid

def print_board_debug(board):
    # Print the board so that black pieces are shown at the bottom as in standard chess diagrams
    rows = []
    for x in range(board.shape[0]):
        row_strs = []
        for y in range(board.shape[1]):
            piece = board[x, y]
            if hasattr(piece, "type") and hasattr(piece, "color"):
                cell = piece.type + piece.color
            elif isinstance(piece, str):
                cell = piece if piece else "--"
            else:
                cell = "--"
            row_strs.append(cell)
        rows.append(" ".join(row_strs))
    for row in reversed(rows):  # Print so that the last row is at the bottom (black at bottom)
        print(row)

def check_friendly_fire(board, startMove, endMove, myColor):
    end_x, end_y = endMove
    target_piece = board[end_x, end_y]

    if hasattr(target_piece, "color") and target_piece.color == myColor:
        return True
    return False

def bishop_mover_bot(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]
    possible_moves = []
    capture_moves = []
    
    size_x, size_y = board.shape
    
    # Filin hareket edebileceği 4 çapraz yön
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)] 
    
    for current_x in range(size_x):
        for current_y in range(size_y):
            
            # Kendi rengindeki filleri bul
            if board[current_x, current_y] != "b" + color:
                continue 
            
            # Her bir yön için (Sol-Üst, Sağ-Üst, Sol-Alt, Sağ-Alt)
            for dx, dy in directions:
                
                # Mesafe (Sliding logic)
                for step in range(1, max(size_x, size_y)):
                    
                    # Hedef kareyi hesapla
                    target_x = current_x + (step * dx)
                    target_y = current_y + (step * dy)
                    
                    # --- SINIR KONTROLLERİ ---
                    if not (0 <= target_x < size_x and 0 <= target_y < size_y):
                        break # Bu yönde daha fazla gidilemez
                    
                    # --- DOST ATEŞİ KONTROLÜ ---
                    if check_friendly_fire(board, (current_x, current_y), (target_x, target_y), color):
                        break # Kendi taşımıza çarptık, bu yönde dur.
                    
                    # --- HAMLE EKLEME ---
                    new_move = ((current_x, current_y), (target_x, target_y))
                    
                    if move_is_valid(player_sequence, new_move, board):
                        # Rakip taşı yedik mi?
                        target_piece = board[target_x, target_y]
                        if target_piece not in ('', 'X', None): 
                            capture_moves.append(new_move)
                            break # Rakibi yedik, dur.
                        else:
                            possible_moves.append(new_move)

    if capture_moves:
        import random
        return random.choice(capture_moves)
    elif possible_moves:
        import random
        return random.choice(possible_moves)
    
    return None

def knight_mover_bot(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]
    possible_moves = []
    capture_moves = []
    
    size_x, size_y = board.shape
    # Atın L şeklinde hareketleri
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    
    for current_x in range(size_x):
        for current_y in range(size_y):
            if board[current_x, current_y] != "n" + color: 
                continue
            
            for dx, dy in directions:
                target_x = current_x + dx
                target_y = current_y + dy
                
                if 0 <= target_x < size_x and 0 <= target_y < size_y:
                    # Dost ateşi kontrolü
                    if check_friendly_fire(board, (current_x, current_y), (target_x, target_y), color):
                        continue

                    new_move = ((current_x, current_y), (target_x, target_y))
                    
                    if move_is_valid(player_sequence, new_move, board):
                        target_piece = board[target_x, target_y]
                        if target_piece not in ('', 'X', None):
                            capture_moves.append(new_move)
                        else:
                            possible_moves.append(new_move)
                            
    if capture_moves:
        import random
        return random.choice(capture_moves)
    elif possible_moves:
        import random
        return random.choice(possible_moves)
    return None

def rook_mover_bot(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1] 
    possible_moves = []
    capture_moves = []
    
    size_x, size_y = board.shape
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Yukarı, Aşağı, Sol, Sağ

    for current_x in range(size_x):
        for current_y in range(size_y):
            if board[current_x, current_y] != "r" + color:
                continue

            for dx, dy in directions:
                for step in range(1, max(size_x, size_y)):
                    
                    target_x = current_x + step * dx
                    target_y = current_y + step * dy

                    if not (0 <= target_x < size_x and 0 <= target_y < size_y):
                        break

                    if check_friendly_fire(board, (current_x, current_y), (target_x, target_y), color):
                        break 

                    new_move = ((current_x, current_y), (target_x, target_y))
                    
                    if move_is_valid(player_sequence, new_move, board):
                        target_piece = board[target_x, target_y]
                        if target_piece not in ('', 'X', None):
                            capture_moves.append(new_move)
                            break # Rakibi yedik, dur.
                        else:
                            possible_moves.append(new_move)

    if capture_moves:
        import random
        return random.choice(capture_moves)
    elif possible_moves:
        import random
        return random.choice(possible_moves)
    return None

def queen_mover_bot(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]
    possible_moves = []
    capture_moves = []
    
    size_x, size_y = board.shape
    # Vezir hem düz hem çapraz gider (8 yön)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

    for current_x in range(size_x):
        for current_y in range(size_y):
            if board[current_x, current_y] != "q" + color:
                continue

            for dx, dy in directions:
                for step in range(1, max(size_x, size_y)):
                    
                    target_x = current_x + step * dx
                    target_y = current_y + step * dy

                    if not (0 <= target_x < size_x and 0 <= target_y < size_y):
                        break

                    if check_friendly_fire(board, (current_x, current_y), (target_x, target_y), color):
                        break 

                    new_move = ((current_x, current_y), (target_x, target_y))
                    
                    if move_is_valid(player_sequence, new_move, board):
                        target_piece = board[target_x, target_y]
                        if target_piece not in ('', 'X', None):
                            capture_moves.append(new_move)
                            break 
                        else:
                            possible_moves.append(new_move)

    if capture_moves:
        import random
        return random.choice(capture_moves)
    elif possible_moves:
        import random
        return random.choice(possible_moves)
    return None

def pawn_mover_bot(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]
    possible_moves = []
    capture_moves = []
    
    size_x, size_y = board.shape
    
    # Piyonun yönü (Beyaz aşağıdan yukarı, Siyah yukarıdan aşağı gibi düşünebiliriz ama board koordinatlarına göre değişir)
    # Genelde: Beyaz (w) x artar, Siyah (b) x azalır veya tam tersi. 
    # ChessRules.py'ye göre: Pawn always move forward (end[0] != start[0] + 1) -> Demek ki x artıyor.
    # Ama renk yönü önemli. ChessRules.py'de bu kontrol biraz eksik olabilir, biz her iki yönü de deneyelim veya 
    # move_is_valid'e güvenelim.
    # Standart satrançta piyon tek adım ileri gider, ilk hamlede 2 adım gidebilir. Çapraz yer.
    
    # Basitçe tüm piyonları bulup, olası hamleleri deneyelim.
    # Piyonun gidebileceği yerler: İleri 1, İleri 2 (başlangıçsa), Çapraz (yeme)
    
    # Yönü belirlemek zor olabilir, bu yüzden basitçe etrafındaki kareleri (ileri ve çapraz) deneyip move_is_valid'e soracağız.
    # Piyon geriye gidemez, ama move_is_valid bunu halleder.
    
    # Olası piyon hamleleri (dx, dy)
    # Beyaz için dx=1, Siyah için dx=-1 (veya tam tersi). 
    # Biz tüm yakın kareleri deneyelim, move_is_valid elesin.
    directions = [
        (1, 0), (2, 0), (1, 1), (1, -1), # İleri ve çaprazlar (bir yön)
        (-1, 0), (-2, 0), (-1, 1), (-1, -1) # Diğer yön (rakip için)
    ]

    for current_x in range(size_x):
        for current_y in range(size_y):
            if board[current_x, current_y] != "p" + color:
                continue

            for dx, dy in directions:
                target_x = current_x + dx
                target_y = current_y + dy
                
                if 0 <= target_x < size_x and 0 <= target_y < size_y:
                    # Dost ateşi kontrolü
                    if check_friendly_fire(board, (current_x, current_y), (target_x, target_y), color):
                        continue

                    new_move = ((current_x, current_y), (target_x, target_y))
                    
                    if move_is_valid(player_sequence, new_move, board):
                        target_piece = board[target_x, target_y]
                        if target_piece not in ('', 'X', None):
                            capture_moves.append(new_move)
                        else:
                            possible_moves.append(new_move)

    if capture_moves:
        import random
        return random.choice(capture_moves)
    elif possible_moves:
        import random
        return random.choice(possible_moves)
    return None

def king_mover_bot(player_sequence, board, time_budget, **kwargs):
    color = player_sequence[1]
    possible_moves = []
    capture_moves = []
    
    size_x, size_y = board.shape
    # Şah her yöne 1 birim gider
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for current_x in range(size_x):
        for current_y in range(size_y):
            if board[current_x, current_y] != "k" + color:
                continue

            for dx, dy in directions:
                target_x = current_x + dx
                target_y = current_y + dy
                
                if 0 <= target_x < size_x and 0 <= target_y < size_y:
                    # Dost ateşi kontrolü
                    if check_friendly_fire(board, (current_x, current_y), (target_x, target_y), color):
                        continue

                    new_move = ((current_x, current_y), (target_x, target_y))
                    
                    if move_is_valid(player_sequence, new_move, board):
                        target_piece = board[target_x, target_y]
                        if target_piece not in ('', 'X', None):
                            capture_moves.append(new_move)
                        else:
                            possible_moves.append(new_move)

    if capture_moves:
        import random
        return random.choice(capture_moves)
    elif possible_moves:
        import random
        return random.choice(possible_moves)
    return None

#register_chess_bot("BishopMover", bishop_mover_bot)
#register_chess_bot("KnightMover", knight_mover_bot)
#register_chess_bot("RookMover", rook_mover_bot)
#register_chess_bot("QueenMover", queen_mover_bot)
#register_chess_bot("PawnMover", pawn_mover_bot)
#register_chess_bot("KingMover", king_mover_bot)