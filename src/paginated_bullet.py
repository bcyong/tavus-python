#!/usr/bin/env python3

from typing import List
import sys
import tty
import termios

class PaginatedBullet:
    """Custom Bullet implementation with left/right arrow key navigation for pagination, with in-place redraw like Bullet."""
    
    def __init__(self, prompt: str, choices: List[str], bullet: str = "→", margin: int = 2, shift: int = 0,
                 bullet_color: str = '\x1b[39m', word_color: str = '\x1b[39m', 
                 word_on_switch: str = '\x1b[7m', background_color: str = '\x1b[49m', 
                 background_on_switch: str = '\x1b[7m'):
        self.prompt = prompt
        self.choices = choices
        self.bullet = bullet
        self.margin = margin
        self.shift = shift
        self.current_index = 0
        self.has_previous_page = any("Previous Page" in choice for choice in choices)
        self.has_next_page = any("Next Page" in choice for choice in choices)
        
        # Color codes for highlighting
        self.bullet_color = bullet_color
        self.word_color = word_color
        self.word_on_switch = word_on_switch
        self.background_color = background_color
        self.background_on_switch = background_on_switch
        self.reset_color = '\x1b[0m'
        self._lines_printed = 0
        self._first_draw = True
    
    def launch(self) -> str:
        """Launch the interactive menu with arrow key navigation"""
        while True:
            self._display()
            key = self._get_key()
            
            if key == 'up' or key == 'k':
                self.current_index = (self.current_index - 1) % len(self.choices)
            elif key == 'down' or key == 'j':
                self.current_index = (self.current_index + 1) % len(self.choices)
            elif key == 'left' and self.has_previous_page:
                return "← Previous Page"
            elif key == 'right' and self.has_next_page:
                return "→ Next Page"
            elif key == 'enter':
                return self.choices[self.current_index]
            elif key == 'q':
                return "← Go Back"
    
    def _move_cursor_up(self, n):
        """Move cursor up by n lines"""
        if n > 0:
            sys.stdout.write(f"\x1b[{n}A")
            sys.stdout.flush()
    
    def _display(self):
        """Display the current menu state with in-place redraw like Bullet"""
        menu_lines = 2 + len(self.choices) + 2  # prompt + blank + choices + blank + nav
        
        if not self._first_draw:
            self._move_cursor_up(self._lines_printed)
        else:
            self._first_draw = False
        
        self._lines_printed = 0
        
        print(self.prompt)
        self._lines_printed += 1
        print()
        self._lines_printed += 1
        
        for i, choice in enumerate(self.choices):
            if i == self.current_index:
                print(f"{' ' * self.margin}{self.bullet_color}{self.bullet}{self.reset_color} {self.word_on_switch}{choice}{self.reset_color}")
            else:
                print(f"{' ' * (self.margin + len(self.bullet) + 1)}{self.word_color}{choice}{self.reset_color}")
            self._lines_printed += 1
        
        print()
        self._lines_printed += 1
        print("Navigation: ↑/↓ to select, ←/→ for pages, Enter to confirm, Q to go back")
        self._lines_printed += 1
    
    def _get_key(self) -> str:
        """Get a single keypress from the user"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            
            # Handle CTRL-C (ASCII 3)
            if ch == '\x03':
                # Restore terminal settings before exiting
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                sys.exit(0)
            
            # Handle arrow keys and other special keys
            if ch == '\x1b':
                next_ch = sys.stdin.read(1)
                if next_ch == '[':
                    third_ch = sys.stdin.read(1)
                    if third_ch == 'A':
                        return 'up'
                    elif third_ch == 'B':
                        return 'down'
                    elif third_ch == 'C':
                        return 'right'
                    elif third_ch == 'D':
                        return 'left'
            
            # Handle other keys
            if ch == 'k':
                return 'up'
            elif ch == 'j':
                return 'down'
            elif ch == 'h':
                return 'left'
            elif ch == 'l':
                return 'right'
            elif ch == '\r' or ch == '\n':
                return 'enter'
            elif ch == 'q':
                return 'q'
            
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings) 