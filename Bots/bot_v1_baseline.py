import random
from Bots.ChessBotList import register_chess_bot
from .sas_move_gen import get_all_moves
from .sas_board_ops import make_move, undo_move
from .sas_evaluation import evaluate_board

def baseline_chess_bot(player_sequence, board, time_budget, **kwargs):
    """
    V1 Baseline Bot:
    - Derinlik: 1 (Sadece o anı görür)
    - Strateji: Greedy (En yüksek puanlı hamleyi seçer)
    - Amaç: Modüler yapının (Make/Undo) çalıştığını kanıtlamak.
    """
    my_color = player_sequence[1]
    
    # 1. Tüm yasal hamleleri al
    capture_moves, quiet_moves = get_all_moves(board, player_sequence)
    all_moves = capture_moves + quiet_moves
    
    # Eğer yapacak hamle yoksa (Mat veya Pat)
    if not all_moves:
        return ((0,0), (0,0))

    best_move = None
    # Başlangıç skoru olarak çok küçük bir sayı veriyoruz (-sonsuz)
    best_score = -float('inf')
    
    # Hamleleri karıştır ki puanlar eşitse hep aynı hamleyi yapmasın
    random.shuffle(all_moves)
    
    # 2. Simülasyon Döngüsü
    for move in all_moves:
        # A) Hamleyi Yap (Make)
        # captured_piece'i saklıyoruz ki geri alabilelim
        captured = make_move(move, board)
        
        # B) Durumu Değerlendir (Evaluate)
        # Hamleyi yaptıktan sonra oluşan tahtanın puanına bakıyoruz
        score = evaluate_board(board, my_color)
        
        # C) Hamleyi Geri Al (Undo)
        # Tahtayı bozmamak için mutlaka geri almalıyız!
        undo_move(move, captured, board)
        
        # D) Karşılaştır
        if score > best_score:
            best_score = score
            best_move = move
            
    # Eğer bir hata olur da hamle seçilemezse rastgele oyna
    if best_move is None:
        best_move = random.choice(all_moves)

    return best_move

# Botu sisteme "V1_Baseline" adıyla kaydediyoruz
register_chess_bot("V1_Baseline", baseline_chess_bot)