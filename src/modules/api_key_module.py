#!/usr/bin/env python3

from bullet import YesNo
from . import ModuleInterface, CommonStates

class APIKeyModule(ModuleInterface):
    """Module for handling API key management"""
    
    def get_name(self) -> str:
        return "api_key"
    
    def get_states(self) -> list:
        return ["set_api_key"]
    
    def get_menu_options(self) -> list:
        return ["Set API Key"]
    
    def get_choice_to_state_mapping(self) -> dict:
        return {
            "Set API Key": "set_api_key"
        }
    
    def execute_state(self, state: str, state_machine) -> str:
        if state == "set_api_key":
            return self._execute_set_api_key(state_machine)
        return CommonStates.MAIN_MENU
    
    def _execute_set_api_key(self, state_machine) -> str:
        """Execute set API key and return next state"""
        print("\n=== Set API Key ===")
        print("Currently set API key: ", state_machine.api_key)
        cli = YesNo(prompt="Would you like to set a new API key?", default="n")
        if cli.launch():
            print("Enter your Tavus API Key:")
            state_machine.api_key = input("API Key: ")
            print(f"Tavus API key: {state_machine.api_key}")
            
            from api_client import TavusAPIClient
            state_machine.api_client = TavusAPIClient(state_machine.api_key)

        return CommonStates.MAIN_MENU 