#!/usr/bin/env python3

from bullet import Bullet
from modules import ModuleRegistry, ModuleInterface, CommonStates
from modules.api_key_module import APIKeyModule
from modules.replica_module import ReplicaModule
from modules.persona_module import PersonaModule
from modules.video_module import VideoModule
from modules.conversation_module import ConversationModule

class StateMachineModular:
    """Modular state machine that uses plugins for functionality"""
    
    # Centralized list of modules
    MODULES = [
        APIKeyModule,
        ReplicaModule,
        PersonaModule,
        VideoModule,
        ConversationModule,
    ]
    
    def __init__(self):
        self.api_client = None
        self.api_key = None
        self.current_state = CommonStates.MAIN_MENU  # Use CommonStates instead of string literal
        
        # Initialize module registry
        self.module_registry = ModuleRegistry()
        
        # Register modules
        self._register_modules()
    
    def _register_modules(self):
        """Register the modules with the state machine"""
        for module_class in self.MODULES:
            self.register_module(module_class())
    
    def register_module(self, module: ModuleInterface):
        """Register a new module with the state machine"""
        self.module_registry.register_module(module)
    
    def execute_current_state(self):
        """Execute the current state and update the next state"""
        if self.current_state == CommonStates.MAIN_MENU:
            self.current_state = self._execute_main_menu()
        elif self.current_state == CommonStates.EXIT:
            # Exit state - do nothing, let the main loop handle it
            pass
        else:
            # Try to find a module that handles this state
            handler = self.module_registry.get_state_handler(self.current_state)
            if handler:
                self.current_state = handler.execute_state(self.current_state, self)
            else:
                print(f"Unknown state: {self.current_state}")
                self.current_state = CommonStates.MAIN_MENU
    
    def _execute_main_menu(self):
        """Execute main menu and return next state"""
        print("\n=== Main Menu ===")
        print(f"Tavus API key: {self.api_key}")
        
        # Get menu options from registered modules
        menu_options = self.module_registry.get_menu_options()
        menu_options.append("Exit")
        
        cli = Bullet(
            prompt="What would you like to do?",
            choices=menu_options,
            bullet="→",
            margin=2,
            shift=0,
        )
        result = cli.launch()

        # Use module registry's choice-to-state mapping
        choice_to_state_mapping = self.module_registry.get_choice_to_state_mapping()
        
        if result == "Exit":
            return CommonStates.EXIT
        elif result in choice_to_state_mapping:
            return choice_to_state_mapping[result]
        else:
            return CommonStates.MAIN_MENU
    
    def set_api_client(self, api_client):
        """Set the API client instance"""
        self.api_client = api_client

    def set_api_key(self, api_key):
        """Set the API key"""
        self.api_key = api_key

    def is_exit_state(self):
        """Check if current state is exit"""
        return self.current_state == CommonStates.EXIT 