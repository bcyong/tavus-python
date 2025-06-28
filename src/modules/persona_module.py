#!/usr/bin/env python3

from bullet import Bullet, YesNo
from yaspin import yaspin
from . import ModuleInterface, CommonStates
from models import Persona
from paginated_list import PaginatedList, PaginatedListResult, PaginationAction, SectionedPaginatedList
from paginated_replica_list import PaginatedReplicaList

class PersonaModule(ModuleInterface):
    """Module for handling persona management"""
    
    def __init__(self):
        self.personas = []  # Local storage for personas
        self.current_filter = "user"  # Default to user personas
    
    def get_name(self) -> str:
        return "persona"
    
    def get_states(self) -> list:
        return [
            "work_with_personas",
            "create_persona",
            "list_personas",
            "delete_persona"
        ]
    
    def get_menu_options(self) -> list:
        return ["Work with Personas"]
    
    def get_choice_to_state_mapping(self) -> dict:
        return {
            "Work with Personas": "work_with_personas"
        }
    
    def execute_state(self, state: str, state_machine) -> str:
        if state == "work_with_personas":
            return self._execute_work_with_personas(state_machine)
        elif state == "create_persona":
            return self._execute_create_persona(state_machine)
        elif state == "list_personas":
            return self._execute_list_personas(state_machine)
        elif state == "delete_persona":
            return self._execute_delete_persona(state_machine)
        return CommonStates.MAIN_MENU
    
    def _execute_work_with_personas(self, state_machine) -> str:
        """Execute work with personas menu and return next state"""
        print("\n=== Work with Personas ===")
        
        with yaspin(text="Loading personas..."):
            self._update_personas(state_machine)

        cli = Bullet(
            prompt="What would you like to do with Personas?",
            choices=["Create a Persona", "List Personas", "Delete a Persona", "Back to Main Menu"],
            bullet="👤",
            margin=2,
            shift=0,
        )
        result = cli.launch()

        if result == "Create a Persona":
            return "create_persona"
        elif result == "List Personas":
            return "list_personas"
        elif result == "Delete a Persona":
            return "delete_persona"
        elif result == "Back to Main Menu":
            return CommonStates.MAIN_MENU
        else:
            return "work_with_personas"
    
    def _execute_create_persona(self, state_machine) -> str:
        """Execute create persona functionality and return next state"""
        print("\n=== Create Persona ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        # Collect persona creation parameters
        persona_name = input("Persona Name: ")
        
        if not persona_name or not persona_name.strip():
            print("Persona name cannot be empty. Please try again.")
            input("Press Enter to continue...")
            return "work_with_personas"

        system_prompt = input("System Prompt: ")
        if not system_prompt or not system_prompt.strip():
            print("System prompt cannot be empty. Please try again.")
            input("Press Enter to continue...")
            return "work_with_personas"
        
        context = input("Context: ").strip()
        
        # Select default replica
        print("Select a default replica for this persona (optional):")
        default_replica_id = self._show_paginated_replicas_for_selection(state_machine)
        if default_replica_id is None:
            print("No default replica selected.")
            default_replica_id = None
        
        # Show final confirmation
        print(f"\nConfirm persona creation:")
        print(f"  Name: {persona_name}")
        print(f"  System Prompt: {system_prompt}")
        print(f"  Context: {context}")
        print(f"  Default Replica: {default_replica_id or 'None'}")
        print("=" * 50)
        
        cli = YesNo("Proceed with persona creation? ", default="n")
        if not cli.launch():
            print("Persona creation cancelled.")
            input("Press Enter to continue...")
            return "work_with_personas"
        
        # Prepare persona data
        persona_data = {
            "persona_name": persona_name,
            "system_prompt": system_prompt
        }
        
        if context:
            persona_data["context"] = context
        
        if default_replica_id:
            persona_data["default_replica_id"] = default_replica_id
        
        with yaspin(text="Creating persona..."):
            success, message, response_data = state_machine.api_client.create_persona(persona_data)
        
        if success:
            print(f"\n✅ {message}")
            if response_data:
                print(f"Persona ID: {response_data.persona_id}")
                print(f"Persona Name: {response_data.persona_name}")
            else:
                print("Persona ID: N/A")
                print("Persona Name: N/A")
        else:
            print(f"\n❌ {message}")
        
        input("Press Enter to continue...")
        return "work_with_personas"
    
    def _execute_list_personas(self, state_machine) -> str:
        """Execute list personas functionality and return next state"""
        print("\n=== List Personas ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        # Fetch personas once when entering list view - default to user personas
        with yaspin(text="Loading personas..."):
            self._update_personas(state_machine, persona_type="user")

        return self._show_paginated_personas(state_machine, filter_type="user")
    
    def _execute_delete_persona(self, state_machine) -> str:
        """Execute delete persona functionality and return next state"""
        print("\n=== Delete Persona ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        # Only show user personas since system personas cannot be deleted
        print("Only user personas can be deleted. System personas cannot be modified.")
        
        # Fetch user personas once for deletion
        with yaspin(text="Loading user personas..."):
            self._update_personas(state_machine, persona_type="user")
            
        return self._show_paginated_personas(state_machine, on_persona_select=self._handle_persona_delete, filter_type="user", show_filter_option=False)
    
    def _handle_persona_delete(self, persona, state_machine) -> str:
        """Handle persona delete when a persona is selected from the list"""
        print(f"\nDeleting persona: {persona.persona_name} ({persona.persona_id})")
        print("=" * 50)
        
        # Show full persona details first
        self._show_persona_details(persona)
        print("=" * 50)
        
        if state_machine.api_client is None:
            print("Error: API client not initialized.")
            input("Press Enter to continue...")
            return "work_with_personas"
        
        # Show confirmation dialog
        print(f"\nConfirm delete operation:")
        print(f"  Persona Name: {persona.persona_name}")
        print(f"  Persona ID: {persona.persona_id}")
        print("=" * 50)
        print("WARNING: This action cannot be undone!")
        print("=" * 50)
        
        cli = YesNo("Are you sure you want to delete this persona?", default="n")
        if not cli.launch():
            print("Delete operation cancelled.")
            input("Press Enter to continue...")
            return None  # Return to persona list
        
        with yaspin(text="Deleting persona..."):
            success, message = state_machine.api_client.delete_persona(persona.persona_id)
        
        if success:
            print(f"Persona deleted successfully: {persona.persona_name}")
            # Remove the persona from our local list
            self.personas = [p for p in self.personas if p.persona_id != persona.persona_id]
        else:
            print(f"Error deleting persona: {message}")
        
        input("Press Enter to continue...")
        return "work_with_personas"
    
    def _update_personas(self, state_machine, persona_type: str = "user") -> None:
        """Update the personas list from API"""
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return

        success, message, fetched_personas = state_machine.api_client.list_personas(persona_type=persona_type)
        if success:
            self.personas = fetched_personas
        else:
            print(message)
    
    def _show_paginated_personas(self, state_machine, page=0, items_per_page=10, filter_type=None, on_persona_select=None, show_filter_option=True):
        """Show paginated list of personas with selection"""
        # Use current filter if none specified
        if filter_type is None:
            filter_type = self.current_filter
        
        if not self.personas:
            print(f"No {filter_type} personas found.")
            input("Press Enter to continue...")
            return "work_with_personas"

        # Create paginated list
        paginated_list = PaginatedList(self.personas, items_per_page)
        paginated_list.set_page(page)

        def on_persona_select_wrapper(persona):
            if on_persona_select:
                # Call the custom callback function
                result_state = on_persona_select(persona, state_machine)
                if result_state:
                    return PaginatedListResult(PaginationAction.ITEM_SELECTED, result_state)
                # If callback returns None, continue showing the list
                return PaginatedListResult(PaginationAction.NO_ACTION, paginated_list.get_current_page())
            else:
                # Default behavior: show persona details
                self._show_persona_details(persona)
                input("Press Enter to continue...")
                # Return the current page so we stay on the same page
                return PaginatedListResult(PaginationAction.NO_ACTION, paginated_list.get_current_page())

        result = paginated_list.show(
            title="Personas",
            filter_type=filter_type,
            on_item_select=on_persona_select_wrapper,
            on_filter_change=self._handle_persona_filter_change,
            show_filter_option=show_filter_option
        )

        return self._handle_persona_pagination_result(result, items_per_page, filter_type, on_persona_select, show_filter_option, state_machine)
    
    def _handle_persona_filter_change(self, filter_type):
        """Handle persona filter change"""
        return PaginatedListResult(PaginationAction.FILTER_CHANGED, filter_type)

    def _handle_persona_pagination_result(self, result, items_per_page, filter_type, on_persona_select, show_filter_option, state_machine):
        """Handle pagination result for personas"""
        if result.action == PaginationAction.PREVIOUS_PAGE:
            return self._show_paginated_personas(state_machine, result.data, items_per_page, filter_type, on_persona_select, show_filter_option)
        elif result.action == PaginationAction.NEXT_PAGE:
            return self._show_paginated_personas(state_machine, result.data, items_per_page, filter_type, on_persona_select, show_filter_option)
        elif result.action == PaginationAction.GO_BACK:
            return "work_with_personas"
        elif result.action == PaginationAction.FILTER_CHANGED:
            # Handle filter change while preserving the callback
            return self._show_persona_filter_selection_with_callback(on_persona_select, state_machine)
        elif result.action == PaginationAction.ITEM_SELECTED:
            # Return the state from the custom callback
            return result.data
        else:
            # Use the page from result.data if available, otherwise default to 0
            current_page = result.data if result.data is not None else 0
            return self._show_paginated_personas(state_machine, current_page, items_per_page, filter_type, on_persona_select, show_filter_option)

    def _show_persona_filter_selection_with_callback(self, on_persona_select=None, state_machine=None):
        """Show filter selection for personas with optional callback preservation"""
        print("\n=== Filter Personas ===")
        
        # If we have a callback, preserve it through filter selection
        if on_persona_select:
            cli = Bullet(
                prompt="Select filter type:",
                choices=["user", "system"],
                bullet="→",
                margin=2,
                shift=0,
            )
            result = cli.launch()

            if result == "user":
                # Fetch user personas for the new filter
                with yaspin(text="Loading user personas..."):
                    self._update_personas(state_machine, persona_type="user")
                return self._show_paginated_personas(state_machine, filter_type="user", on_persona_select=on_persona_select, show_filter_option=True)
            elif result == "system":
                # Fetch system personas for the new filter
                with yaspin(text="Loading system personas..."):
                    self._update_personas(state_machine, persona_type="system")
                return self._show_paginated_personas(state_machine, filter_type="system", on_persona_select=on_persona_select, show_filter_option=True)
        else:
            # Standard filter selection for normal browsing
            cli = Bullet(
                prompt="Select filter type:",
                choices=["user", "system"],
                bullet="→",
                margin=2,
                shift=0,
            )
            result = cli.launch()

            if result == "user":
                # Fetch user personas for the new filter
                with yaspin(text="Loading user personas..."):
                    self._update_personas(state_machine, persona_type="user")
                self.current_filter = "user"
                return self._show_paginated_personas(state_machine, filter_type="user", show_filter_option=True)
            elif result == "system":
                # Fetch system personas for the new filter
                with yaspin(text="Loading system personas..."):
                    self._update_personas(state_machine, persona_type="system")
                self.current_filter = "system"
                return self._show_paginated_personas(state_machine, filter_type="system", show_filter_option=True)
        
        # Default fallback
        with yaspin(text="Loading user personas..."):
            self._update_personas(state_machine, persona_type="user")
        self.current_filter = "user"
        return self._show_paginated_personas(state_machine, filter_type="user", show_filter_option=True)
    
    def _show_persona_details(self, persona):
        """Show detailed information for a specific persona"""
        print("\n" + "=" * 60)
        print("PERSONA DETAILS")
        print("=" * 60)
        print(persona.display_verbose())
        print("=" * 60)
    
    def _show_paginated_replicas_for_selection(self, state_machine, page=0, filter_type="all"):
        """Show paginated list of replicas for selection and return the selected replica ID"""
        # Update replicas if needed
        if not hasattr(self, 'replicas') or not self.replicas:
            with yaspin(text="Loading replicas..."):
                self._update_replicas_for_selection(state_machine)
        
        if not hasattr(self, 'replicas') or not self.replicas:
            print("No replicas found. Please create a replica first.")
            input("Press Enter to continue...")
            return None

        # Use the generic paginated replica list
        paginated_list = PaginatedReplicaList(self.replicas, 10)
        result = paginated_list.show(
            state_machine=state_machine,
            page=page,
            filter_type=filter_type,
            show_filter_option=True,
            title="Select Replica",
            return_replica_id=True
        )
        
        return result
    
    def _update_replicas_for_selection(self, state_machine) -> None:
        """Update the replicas list from API for selection"""
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return

        success, message, fetched_replicas = state_machine.api_client.list_replicas()
        if success:
            self.replicas = fetched_replicas
        else:
            print(message) 