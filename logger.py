from colorama import Fore, init
import datetime
import time
import os
import traceback
from pathlib import Path

class Logger:
    def __init__(self, colors=True, frame=50, version='test', save=False, min_level=0, days = 7):
        # State management
        self.log_colors = {'info': Fore.BLUE, 'debug': Fore.GREEN, 'warning': Fore.RED, 'error': Fore.RED}
        self.version = version
        self.days = days
        self.config = {
            'colors': colors,
            'frame': frame,
            'debug': False if version == 'full' else True,
            'save': save,
            'min_level': min_level
        }
        
        if colors:
            init(autoreset=True)
            
        if save:
            self.base_name = Path(__file__).stem
            self.log_timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.folder = f'logs/{self.base_name}'
            os.makedirs(self.folder, exist_ok=True)

            self.cleanup_old_logs(self.folder, self.days)
            self.log_file = open(f'{self.folder}/{self.base_name}_{self.log_timestamp}.txt', 'a')

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def cleanup_old_logs(self, folder, days):
        now = time.time()
        seconds_limit = days * 24 * 60 * 60
        if not os.path.exists(folder): return
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            if now - os.path.getmtime(path) > seconds_limit:
                os.remove(path)

    def log(self, prefix, message, color_key, level):
        if self.config['min_level'] > level: return
        
        color = self.log_colors[color_key] if self.config['colors'] else ""
        frame = self.config['frame']
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        line = color + ('—' * frame if frame > 0 else "")
        msg_str = f"[{timestamp}] {message}" if self.config['debug'] else message
        output = f"{color}| {prefix:<12} {msg_str}"

        if frame > 0: print(line)
        print(output)
        if frame > 0: print(line)

        if self.config['save']:
            self.log_file.write(f'[{timestamp}] | {message.strip()}\n')
            self.log_file.flush()

    def close(self):
        if self.config['save'] and not self.log_file.closed:
            self.log_file.close()

    # Logging methods
    def info(self, msg): self.log('💡 [INFO]', msg, 'info', 1)
    def debug(self, msg): 
        if self.config['debug']: self.log('🐛 [DEBUG]', msg, 'debug', 0)
    def debug_p(self, msg): 
        if self.config['debug'] and self.version == 'test_advance':  self.log('🐛 + [DEBUG]', msg, 'debug', -1) 
    def warning(self, msg): self.log('❗ [WARNING]', msg.upper(), 'warning', 2)
    def error(self, msg):
        self.log(f'🛑 [ERROR] ', msg.upper(), 'error', 3)
        error_details = traceback.format_exc()
        print(error_details)
        if self.config['save']:
            self.log_file.write(f"--- TRACEBACK ---\n{error_details}\n-----------------\n")
            self.log_file.flush()

if __name__ == "__main__":
    with Logger(save=False) as demo:
        demo.info("Debugger module is working correctly!")