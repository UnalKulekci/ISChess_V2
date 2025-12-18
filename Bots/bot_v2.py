import random
from Bots.ChessBotList import register_chess_bot
from ChessRules import move_is_valid
from Bots.sas_constant import piece_values


# =============================================================================
# YARDIMCI FONKSİYONLAR (Hareket Mantıkları)
# =============================================================================

def get_sliding_moves(board, pos, directions, color, size_x, size_y):
    """Kale, Fil ve Vezir için (Kayarak giden taşlar)"""
    moves = []
    x, y = pos
    
    for dx, dy in directions:
        for step in range(1, max(size_x, size_y)):
            tx, ty = x + (step * dx), y + (step * dy)
            
            # 1. Tahta dışına çıktı mı?
            if not (0 <= tx < size_x and 0 <= ty < size_y):
                break
            
            target = board[tx, ty]
            
            # 2. Dost Ateşi (Kendi taşımız varsa dur)
            if is_friendly_piece(target, color):
                break

            # 3. Hamle Ekle (Validasyon sonra yapılacak)
            moves.append(((x, y), (tx, ty)))
            
            # 4. Rakip varsa (Ye ve Dur) - Üzerinden atlayamaz
            if is_enemy_piece(target, color):
                break
                
    return moves

def get_stepping_moves(board, pos, offsets, color, size_x, size_y):
    """At ve Şah için (Sıçrayan/Tek adım giden taşlar)"""
    moves = []
    x, y = pos
    
    for dx, dy in offsets:
        tx, ty = x + dx, y + dy
        
        if 0 <= tx < size_x and 0 <= ty < size_y:
            target = board[tx, ty]
            
            # Sadece dost taşı değilse ekle (Boş veya Rakip)
            if not is_friendly_piece(target, color):
                moves.append(((x, y), (tx, ty)))
                
    return moves

def get_pawn_moves(board, pos, color, size_x, size_y):
    """Piyon için özel mantık (Yön, Çift Adım, Çapraz Yeme)"""
    moves = []
    x, y = pos
    
    # --- Yön Belirleme ---
    # Beyaz (w) genelde tahtanın altındadır ve yukarı (index azalır) gider.
    # Siyah (b) genelde tahtanın üstündedir ve aşağı (index artar) gider.
    if color == 'w':
        dx = -1
        start_row = 6 # (0-7 arası indexte, beyazlar genelde 6. satırdadır)
    else:
        dx = 1
        start_row = 1 # (Siyahlar genelde 1. satırdadır)

    # 1. İLERİ GİTME (Yeme Yok)
    fwd_x = x + dx
    if 0 <= fwd_x < size_x:
        # Tek Adım
        if is_square_empty(board[fwd_x, y]):
            moves.append(((x, y), (fwd_x, y)))
            
            # Çift Adım (Sadece başlangıç satırındaysa ve yol boşsa)
            step2_x = x + (2 * dx)
            if x == start_row and 0 <= step2_x < size_x:
                if is_square_empty(board[step2_x, y]):
                    moves.append(((x, y), (step2_x, y)))

    # 2. ÇAPRAZ YEME
    capture_offsets = [(dx, -1), (dx, 1)]
    for cx, cy in capture_offsets:
        cap_x, cap_y = x + cx, y + cy
        
        if 0 <= cap_x < size_x and 0 <= cap_y < size_y:
            target = board[cap_x, cap_y]
            # Sadece RAKİP varsa hamle ekle
            if is_enemy_piece(target, color):
                moves.append(((x, y), (cap_x, cap_y)))

    return moves

# =============================================================================
# HELPER CHECKS (Kod tekrarını önlemek için)
# =============================================================================

def is_square_empty(piece):
    return piece in (None, '', 'X')

def is_friendly_piece(piece, my_color):
    if is_square_empty(piece): return False
    # Nesne ise .color, String ise "wp" -> 'w'
    p_color = piece.color if hasattr(piece, "color") else piece[-1]
    return p_color == my_color

def is_enemy_piece(piece, my_color):
    if is_square_empty(piece): return False
    return not is_friendly_piece(piece, my_color)

# =============================================================================
# ANA BOT FONKSİYONU (UNIFIED BOT)
# =============================================================================

def unified_chess_bot(player_sequence, board, time_budget, **kwargs):
    my_color = player_sequence[1] # 'w' or 'b'
    size_x, size_y = board.shape
    
    capture_moves = []
    quiet_moves = []

    
    # Hareket Vektörleri
    orth = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Kale
    diag = [(-1, -1), (-1, 1), (1, -1), (1, 1)] # Fil
    knight_dirs = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    king_dirs = orth + diag

    # --- TEK GEÇİŞLİ TARAMA (O(NxM)) ---
    for x in range(size_x):
        for y in range(size_y):
            piece = board[x, y]
            
            # Boşsa veya benim taşım değilse geç
            if not is_friendly_piece(piece, my_color):
                continue

            # Taş tipini al ("wp" -> "p" veya piece.type)
            p_type = piece.type if hasattr(piece, "type") else piece[0]
            
            candidate_moves = []
            
            # --- MATCH CASE YAPISI (Python 3.10+) ---
            match p_type:
                case 'r':  # Kale (Rook)
                    candidate_moves = get_sliding_moves(board, (x, y), orth, my_color, size_x, size_y)
                
                case 'b':  # Fil (Bishop)
                    candidate_moves = get_sliding_moves(board, (x, y), diag, my_color, size_x, size_y)
                
                case 'q':  # Vezir (Queen)
                    candidate_moves = get_sliding_moves(board, (x, y), orth + diag, my_color, size_x, size_y)
                
                case 'n':  # At (Knight)
                    candidate_moves = get_stepping_moves(board, (x, y), knight_dirs, my_color, size_x, size_y)
                
                case 'k':  # Şah (King)
                    candidate_moves = get_stepping_moves(board, (x, y), king_dirs, my_color, size_x, size_y)
                
                case 'p':  # Piyon (Pawn)
                    candidate_moves = get_pawn_moves(board, (x, y), my_color, size_x, size_y)
                
                case _:    # Bilinmeyen bir taş tipi varsa (Önlem amaçlı)
                    continue
            
            # --- VALİDASYON VE SINIFLANDIRMA ---
            for move in candidate_moves:
                # Oyun kurallarına (Şah durumu vb.) uygun mu?
                if move_is_valid(player_sequence, move, board):
                    target_x, target_y = move[1]
                    target_piece = board[target_x, target_y]
                    
                    # Hedefte rakip varsa Capture Listesine, yoksa Quiet Listesine
                    if is_enemy_piece(target_piece, my_color):
                        capture_moves.append(move)
                    else:
                        quiet_moves.append(move)

    # --- HAMLE SEÇİMİ ---

    # Basit Puanlama Sözlüğü
    piece_values = {
        'p': 10,  # Piyon
        'n': 30,  # At
        'b': 30,  # Fil
        'r': 50,  # Kale
        'q': 90,  # Vezir
        'k': 900  # Şah
    }

    def get_piece_value(piece):
        """Taşın puanını döndürür"""
        if is_square_empty(piece):
            return 0
        p_type = piece.type if hasattr(piece, "type") else piece[0]
        return piece_values.get(p_type, 0)

    # 1. EN İYİ TAŞI YE (Capture Logic)
    if capture_moves:
        best_capture = None
        max_score = -1

        for move in capture_moves:
            # Hedef karedeki taşı bul
            target_pos = move[1]
            target_piece = board[target_pos[0], target_pos[1]]
            
            # Puanı hesapla
            score = get_piece_value(target_piece)
            
            # En yüksek puanlıyı sakla
            if score > max_score:
                max_score = score
                best_capture = move
        
        print(f"En iyi yeme hamlesi: {best_capture} (Puan: {max_score})")
        return best_capture
    
    # 2. Yeme yoksa Rastgele Oyna (Şimdilik)
    if quiet_moves:
        return random.choice(quiet_moves)
    
    # 3. Hiç Hamle Yoksa (Mat veya Pat)
    print(f"Bot ({my_color}) yapacak hamle bulamadı! Oyun bitmiş olabilir.")
    return ((0,0), (0,0)) 

# =============================================================================
# BOTU SİSTEME KAYDET
# =============================================================================

register_chess_bot("UnifiedBot", unified_chess_bot)