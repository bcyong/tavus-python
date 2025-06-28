#!/usr/bin/env python3

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

# Common state constants to avoid hardcoding string literals
class CommonStates:
    """Common states that modules can reference without hardcoding"""
    MAIN_MENU = "main_menu"
    EXIT = "exit"

class ModuleInterface(ABC):
    """Base interface for all state machine modules"""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return the module name"""
        pass
    
    @abstractmethod
    def get_states(self) -> List[str]:
        """Return list of state names this module handles"""
        pass
    
    @abstractmethod
    def get_menu_options(self) -> List[str]:
        """Return menu options this module provides"""
        pass
    
    @abstractmethod
    def get_choice_to_state_mapping(self) -> Dict[str, str]:
        """Return mapping from menu choices to states"""
        pass
    
    @abstractmethod
    def execute_state(self, state: str, state_machine) -> str:
        """Execute a specific state and return the next state"""
        pass

class ModuleRegistry:
    """Registry for managing state machine modules"""
    
    def __init__(self):
        self.modules: Dict[str, ModuleInterface] = {}
        self.state_handlers: Dict[str, ModuleInterface] = {}
        self.menu_options: List[str] = []
        self.choice_to_state_mapping: Dict[str, str] = {}
    
    def register_module(self, module: ModuleInterface) -> None:
        """Register a module with the registry"""
        self.modules[module.get_name()] = module
        
        # Register states
        for state_name in module.get_states():
            self.state_handlers[state_name] = module
        
        # Register menu options
        self.menu_options.extend(module.get_menu_options())
        
        # Register choice-to-state mappings
        self.choice_to_state_mapping.update(module.get_choice_to_state_mapping())
    
    def get_state_handler(self, state: str) -> Optional[ModuleInterface]:
        """Get the module that handles a specific state"""
        return self.state_handlers.get(state)
    
    def get_menu_options(self) -> List[str]:
        """Get all menu options from registered modules"""
        return self.menu_options.copy()
    
    def get_choice_to_state_mapping(self) -> Dict[str, str]:
        """Get the complete choice-to-state mapping"""
        return self.choice_to_state_mapping.copy()
    
    def get_modules(self) -> Dict[str, ModuleInterface]:
        """Get all registered modules"""
        return self.modules.copy()
    
    def get_all_states(self) -> List[str]:
        """Get all registered state names"""
        return list(self.state_handlers.keys()) 