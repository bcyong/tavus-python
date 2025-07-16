#!/usr/bin/env python3

from bullet import Bullet, YesNo
from yaspin import yaspin
from . import ModuleInterface, CommonStates
from paginated_list import PaginatedList, PaginatedListResult, PaginationAction

class ConversationModule(ModuleInterface):
    """Module for managing conversations"""
    
    def __init__(self):
        self.conversations = []
    
    def get_name(self) -> str:
        return "Conversation Management"
    
    def get_states(self) -> list:
        return [
            "work_with_conversations",
            "create_conversation", 
            "list_conversations",
            "end_conversation",
            "delete_conversation"
        ]
    
    def get_menu_options(self) -> list:
        return ["Work with Conversations"]
    
    def get_choice_to_state_mapping(self) -> dict:
        return {
            "Work with Conversations": "work_with_conversations"
        }
    
    def execute_state(self, state: str, state_machine) -> str:
        """Execute the given state and return the next state"""
        if state == "work_with_conversations":
            return self._execute_work_with_conversations(state_machine)
        elif state == "create_conversation":
            return self._execute_create_conversation(state_machine)
        elif state == "list_conversations":
            return self._execute_list_conversations(state_machine)
        elif state == "end_conversation":
            return self._execute_end_conversation(state_machine)
        elif state == "delete_conversation":
            return self._execute_delete_conversation(state_machine)
        else:
            return CommonStates.MAIN_MENU
    
    def _execute_work_with_conversations(self, state_machine) -> str:
        """Execute work with conversations functionality and return next state"""
        print("\n=== Work with Conversations ===")
        
        with yaspin(text="Loading conversations..."):
            self._update_conversations(state_machine)

        cli = Bullet(
            prompt="What would you like to do with Conversations?",
            choices=["Create a Conversation", "List Conversations", "End a Conversation", "Delete a Conversation", "Back to Main Menu"],
            bullet="💬",
            margin=2,
            shift=0,
        )
        result = cli.launch()

        if result == "Create a Conversation":
            return "create_conversation"
        elif result == "List Conversations":
            return "list_conversations"
        elif result == "End a Conversation":
            return "end_conversation"
        elif result == "Delete a Conversation":
            return "delete_conversation"
        elif result == "Back to Main Menu":
            return CommonStates.MAIN_MENU
        else:
            return "work_with_conversations"
    
    def _execute_create_conversation(self, state_machine) -> str:
        """Execute create conversation functionality and return next state"""
        print("\n=== Create Conversation ===")
        print("⚠️  This functionality is not yet implemented.")
        print("Coming soon: Create conversations with personas and replicas.")
        input("Press Enter to continue...")
        return "work_with_conversations"
    
    def _execute_list_conversations(self, state_machine) -> str:
        """Execute list conversations functionality and return next state"""
        print("\n=== List Conversations ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        return self._show_paginated_conversations(state_machine)
    
    def _execute_end_conversation(self, state_machine) -> str:
        """Execute end conversation functionality and return next state"""
        print("\n=== End Conversation ===")
        print("⚠️  This functionality is not yet implemented.")
        print("Coming soon: End active conversations.")
        input("Press Enter to continue...")
        return "work_with_conversations"
    
    def _execute_delete_conversation(self, state_machine) -> str:
        """Execute delete conversation functionality and return next state"""
        print("\n=== Delete Conversation ===")
        print("⚠️  This functionality is not yet implemented.")
        print("Coming soon: Delete conversations permanently.")
        input("Press Enter to continue...")
        return "work_with_conversations"
    
    def _update_conversations(self, state_machine) -> None:
        """Update the conversations list from the API"""
        if state_machine.api_client is None:
            return
        
        success, message, conversations = state_machine.api_client.list_conversations()
        if success:
            self.conversations = conversations
        else:
            print(f"Warning: {message}")
            self.conversations = []
    
    def _show_paginated_conversations(self, state_machine, page=0, items_per_page=10):
        """Show paginated conversations list"""
        if not self.conversations:
            print("No conversations found.")
            input("Press Enter to continue...")
            return "work_with_conversations"
        
        paginated_list = PaginatedList(self.conversations, items_per_page)
        paginated_list.set_page(page)
        
        result = paginated_list.show(
            title="Conversations",
            filter_type="all",
            on_item_select=self._handle_conversation_select,
            show_filter_option=False
        )
        
        return self._handle_conversation_pagination_result(result, items_per_page, state_machine)
    
    def _handle_conversation_select(self, conversation) -> PaginatedListResult:
        """Handle conversation selection from the list"""
        self._show_conversation_details(conversation)
        input("Press Enter to continue...")
        return PaginatedListResult(PaginationAction.NO_ACTION)
    
    def _handle_conversation_pagination_result(self, result, items_per_page, state_machine):
        """Handle pagination result for conversations"""
        if result.action == PaginationAction.PREVIOUS_PAGE:
            return self._show_paginated_conversations(state_machine, result.data, items_per_page)
        elif result.action == PaginationAction.NEXT_PAGE:
            return self._show_paginated_conversations(state_machine, result.data, items_per_page)
        elif result.action == PaginationAction.GO_BACK:
            return "work_with_conversations"
        else:
            return self._show_paginated_conversations(state_machine, 0, items_per_page)
    
    def _show_conversation_details(self, conversation):
        """Show detailed information about a conversation"""
        print("\n" + "=" * 60)
        print("CONVERSATION DETAILS")
        print("=" * 60)
        print(conversation.display_verbose())
        print("=" * 60) 