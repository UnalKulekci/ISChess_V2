import json
import time
import os

class MetricsLogger:
    def __init__(self, bot_name):
        self.bot_name = bot_name
        self.timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.filename = f"metrics_{self.bot_name}_{self.timestamp}.json"
        self.log_data = {
            "bot_name": bot_name,
            "timestamp": self.timestamp,
            "moves": []
        }
        
        
        log_dir = os.path.join("metrics", "Logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        self.filepath = os.path.join(log_dir, self.filename)

    def log_move(self, move_number, player_color, time_taken, nodes, nps, score, eval_time, best_move):
        """
        Saves metrics after each move.
        """
        
        move_data = {
            "move_number": int(move_number),
            "color": str(player_color),
            "time": float(time_taken),
            "nodes": int(nodes),
            "nps": float(nps),
            "score": float(score),
            "eval_time": float(eval_time),
            "best_move": str(best_move)
        }
        
        self.log_data["moves"].append(move_data)
        self._save_to_file()

    def _save_to_file(self):
    
        try:
            with open(self.filepath, 'w') as f:
                json.dump(self.log_data, f, indent=4)
        except Exception as e:
            print(f"Error saving metrics: {e}")

_logger_instance = None

def get_logger(bot_name="Unknown"):
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = MetricsLogger(bot_name)
    return _logger_instance
