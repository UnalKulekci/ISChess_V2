
from .sas_constant import PIECE_VALUES
from .sas_utils import is_square_empty, is_friendly_piece

def get_piece_value(piece):

    if is_square_empty(piece): 
        return 0
    
    # Taş tipini al (örn: 'p', 'n', 'k')
    p_type = piece.type if hasattr(piece, "type") else piece[0]
    
    # Sabitlerden değerini çek, bulamazsan 0 döndür
    return PIECE_VALUES.get(p_type, 0)

def evaluate_board(board, my_color):
    """
    Tahtanın o anki durumunu puanlar.
    Pozitif Puan (+) -> Ben öndeyim.
    Negatif Puan (-) -> Rakip önde.
    """
    total_score = 0
    size_x, size_y = board.shape
    
    for x in range(size_x):
        for y in range(size_y):
            piece = board[x, y]
            
            # Boş kareleri atla
            if is_square_empty(piece):
                continue
                
            val = get_piece_value(piece)
            
            # Eğer benim taşımsa puan ekle, rakibimse çıkar
            if is_friendly_piece(piece, my_color):
                total_score += val
            else:
                total_score -= val
                    
    return total_score