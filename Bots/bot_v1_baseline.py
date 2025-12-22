import random
import time
from Bots.ChessBotList import register_chess_bot

from .sas_move_gen import get_all_moves
from .sas_board_ops import make_move, undo_move
from .sas_evaluation import evaluate_board
from .sas_metrics_logger import get_logger 

def baseline_chess_bot(player_sequence, board, time_budget, **kwargs):
    """
    V1 Baseline Bot:
    - Depth: 1 (Looks only one move ahead)
    - Strategy: Greedy (Selects the move with the highest immediate score)
    - Purpose: To prove the modular structure (Make/Undo/Evaluate) works.
    """
    my_color = player_sequence[1]
    
    # --- METRICS START ---
    start_time = time.perf_counter() 
    eval_time = 0 
    # ---------------------
    
    # 1. Get all legal moves
    capture_moves, quiet_moves = get_all_moves(board, player_sequence)
    all_moves = capture_moves + quiet_moves

    # METRIC: Node Count (For V1, node count = move count)
    nodes_visited = len(all_moves)
    
    # If no moves available (Checkmate or Stalemate)
    if not all_moves:
        return ((0,0), (0,0))

    best_move = None
    # Initialize best score with a very small number
    best_score = -float('inf')
    
    # Shuffle moves to avoid deterministic behavior on equal scores
    random.shuffle(all_moves)
    
    # 2. Simulation Loop
    for move in all_moves:
        # Debug: Get piece info before making the move
        start_pos = move[0]
        piece_obj = board[start_pos[0], start_pos[1]]
        
        if hasattr(piece_obj, 'type'):
            p_name = f"{piece_obj.color}{piece_obj.type}" # e.g. wp, bk
        else:
            p_name = str(piece_obj)

        # A) Make Move
        captured = make_move(move, board)
        
        # B) Evaluate Position
        t0 = time.perf_counter()
        score = evaluate_board(board, my_color)
        t1 = time.perf_counter()
        eval_time += (t1 - t0)
        
        # C) Undo Move
        undo_move(move, captured, board)
        
        # D) Compare Scores
        # DEBUG: Print each move's score
        # print(f"[DEBUG] Piece: {p_name} | Move: {move} | Score: {score}")
        
        if score > best_score:
            best_score = score
            best_move = move
            
    # Fallback: If no best move found (should not happen), pick random
    if best_move is None:
        best_move = random.choice(all_moves)

    # --- METRICS END AND REPORTING ---
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    
    # Prevent division by zero
    if elapsed_time == 0: elapsed_time = 0.000001
    
    nps = nodes_visited / elapsed_time
    
    # Ratio of eval time to total time
    eval_ratio = (eval_time / elapsed_time) * 100 if elapsed_time > 0 else 0

    print(f"[{my_color.upper()} BOT V1] "
          f"Time: {elapsed_time:.4f}s | "
          f"Nodes: {nodes_visited} | "
          f"NPS: {nps:.0f} | "
          f"Score: {best_score} | "
          f"Eval Time: {eval_time:.4f}s ({eval_ratio:.1f}%)")
    
    # --- LOGGING ---
    logger = get_logger("V1_Baseline")
    logger.log_move(
        move_number=-1, # Bot is stateless, so we pass -1
        player_color=my_color,
        time_taken=elapsed_time,
        nodes=nodes_visited,
        nps=nps,
        score=best_score,
        eval_time=eval_time,
        best_move=best_move
    )


    return best_move

register_chess_bot("V1_Baseline", baseline_chess_bot)