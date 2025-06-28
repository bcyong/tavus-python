#!/usr/bin/env python3

from bullet import Bullet, YesNo
from yaspin import yaspin
from . import ModuleInterface, CommonStates
from models import Replica
from paginated_list import PaginatedList, SectionedPaginatedList, PaginatedListResult, PaginationAction

class ReplicaModule(ModuleInterface):
    """Module for handling replica management"""
    
    def __init__(self):
        self.replicas = []  # Local storage for replicas
    
    def get_name(self) -> str:
        return "replica"
    
    def get_states(self) -> list:
        return [
            "work_with_replicas",
            "create_replica",
            "list_replicas",
            "rename_replica",
            "delete_replica"
        ]
    
    def get_menu_options(self) -> list:
        return ["Work with Replicas"]
    
    def get_choice_to_state_mapping(self) -> dict:
        return {
            "Work with Replicas": "work_with_replicas"
        }
    
    def execute_state(self, state: str, state_machine) -> str:
        if state == "work_with_replicas":
            return self._execute_work_with_replicas(state_machine)
        elif state == "create_replica":
            return self._execute_create_replica(state_machine)
        elif state == "list_replicas":
            return self._execute_list_replicas(state_machine)
        elif state == "rename_replica":
            return self._execute_rename_replica(state_machine)
        elif state == "delete_replica":
            return self._execute_delete_replica(state_machine)
        return CommonStates.MAIN_MENU
    
    def _execute_work_with_replicas(self, state_machine) -> str:
        """Execute work with replicas menu and return next state"""
        print("\n=== Work with Replicas ===")
        
        with yaspin(text="Loading replicas..."):
            self._update_replicas(state_machine)

        cli = Bullet(
            prompt="What would you like to do with Replicas?",
            choices=["Create a Replica", "List Replicas", "Rename a Replica", "Delete a Replica", "Back to Main Menu"],
            bullet="🧑",
            margin=2,
            shift=0,
        )
        result = cli.launch()

        if result == "Create a Replica":
            return "create_replica"
        elif result == "List Replicas":
            return "list_replicas"
        elif result == "Rename a Replica":
            return "rename_replica"
        elif result == "Delete a Replica":
            return "delete_replica"
        elif result == "Back to Main Menu":
            return CommonStates.MAIN_MENU
        else:
            return "work_with_replicas"
    
    def _execute_create_replica(self, state_machine) -> str:
        """Execute create replica functionality and return next state"""
        print("\n=== Create Replica ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        # Collect replica creation parameters
        replica_name = input("Replica Name: ")
        
        if not replica_name or not replica_name.strip():
            print("Replica name cannot be empty. Please try again.")
            input("Press Enter to continue...")
            return "work_with_replicas"

        training_video_url = input("Training Video URL: ")
        
        if not training_video_url or not training_video_url.strip():
            print("Video URL cannot be empty. Please try again.")
            input("Press Enter to continue...")
            return "work_with_replicas"

        consent_video_url = input("Consent Video URL: ")
        
        if not consent_video_url or not consent_video_url.strip():
            print("Video URL cannot be empty. Please try again.")
            input("Press Enter to continue...")
            return "work_with_replicas"
        
        # Show final confirmation
        print(f"\nConfirm replica creation:")
        print(f"  Name: {replica_name}")
        print(f"  Training Video URL: {training_video_url}")
        print(f"  Consent Video URL: {consent_video_url}")
        print("=" * 50)
        
        cli = YesNo("Proceed with replica creation? ", default="n")
        if not cli.launch():
            print("Replica creation cancelled.")
            input("Press Enter to continue...")
            return "work_with_replicas"
        
        # Prepare replica data
        replica_data = {
            "replica_name": replica_name,
            "train_video_url": training_video_url,
            "consent_video_url": consent_video_url
        }
        
        with yaspin(text="Creating replica..."):
            success, message, response_data = state_machine.api_client.create_replica(replica_data)
        
        if success:
            print(f"\n✅ {message}")
            if response_data:
                print(f"Replica ID: {response_data.get('replica_id', 'N/A')}")
                print(f"Status: {response_data.get('status', 'N/A')}")
            else:
                print("Replica ID: N/A")
                print("Status: N/A")
            print("\nNote: Replica training is now in progress. You can check the status later.")
        else:
            print(f"\n❌ {message}")
        
        input("Press Enter to continue...")
        return "work_with_replicas"
    
    def _execute_list_replicas(self, state_machine) -> str:
        """Execute list replicas functionality and return next state"""
        print("\n=== List Replicas ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        return self._show_paginated_replicas(state_machine)
    
    def _execute_rename_replica(self, state_machine) -> str:
        """Execute rename replica functionality and return next state"""
        print("\n=== Rename Replica ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        # Only show user replicas since system replicas cannot be renamed
        print("Only user replicas can be renamed. System replicas cannot be modified.")
        return self._show_paginated_replicas(state_machine, on_replica_select=self._handle_replica_rename, filter_type="user", show_filter_option=False)
    
    def _execute_delete_replica(self, state_machine) -> str:
        """Execute delete replica functionality and return next state"""
        print("\n=== Delete Replica ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        # Only show user replicas since system replicas cannot be deleted
        print("Only user replicas can be deleted. System replicas cannot be modified.")
        return self._show_paginated_replicas(state_machine, on_replica_select=self._handle_replica_delete, filter_type="user", show_filter_option=False)
    
    def _handle_replica_rename(self, replica, state_machine) -> str:
        """Handle replica rename when a replica is selected from the list"""
        print(f"\nRenaming replica: {replica.replica_name} ({replica.replica_id})")
        print("=" * 50)
        
        # Additional safety check - ensure only user replicas can be renamed
        if replica.replica_type != "user":
            print(f"Error: Cannot rename system replicas. This replica is of type '{replica.replica_type}'.")
            print("Only user replicas can be renamed.")
            input("Press Enter to continue...")
            return None  # Return to replica list
        
        # Show full replica details first
        self._show_replica_details(replica)
        print("=" * 50)
        
        if state_machine.api_client is None:
            print("Error: API client not initialized.")
            input("Press Enter to continue...")
            return "work_with_replicas"
        
        new_name = input("New name: ")
        
        if not new_name or not new_name.strip():
            print("Replica name cannot be empty. Please try again.")
            input("Press Enter to continue...")
            return None  # Return to replica list
        
        # Show confirmation dialog
        print(f"\nConfirm rename operation:")
        print(f"  From: {replica.replica_name}")
        print(f"  To:   {new_name}")
        print("=" * 50)
        
        cli = YesNo("Are you sure you want to rename this replica?", default="n")
        if not cli.launch():
            print("Rename operation cancelled.")
            input("Press Enter to continue...")
            return None  # Return to replica list
        
        with yaspin(text="Renaming replica..."):
            success, message = state_machine.api_client.rename_replica(replica.replica_id, new_name)
        
        if success:
            print(f"Replica renamed successfully to: {new_name}")
            # Update the replica object in our list
            replica.replica_name = new_name
        else:
            print(f"Error renaming replica: {message}")
        
        input("Press Enter to continue...")
        return "work_with_replicas"
    
    def _handle_replica_delete(self, replica, state_machine) -> str:
        """Handle replica delete when a replica is selected from the list"""
        print(f"\nDeleting replica: {replica.replica_name} ({replica.replica_id})")
        print("=" * 50)
        
        # Additional safety check - ensure only user replicas can be deleted
        if replica.replica_type != "user":
            print(f"Error: Cannot delete system replicas. This replica is of type '{replica.replica_type}'.")
            print("Only user replicas can be deleted.")
            input("Press Enter to continue...")
            return None  # Return to replica list
        
        # Show full replica details first
        self._show_replica_details(replica)
        print("=" * 50)
        
        if state_machine.api_client is None:
            print("Error: API client not initialized.")
            input("Press Enter to continue...")
            return "work_with_replicas"
        
        # Show confirmation dialog
        print(f"\nConfirm delete operation:")
        print(f"  Replica Name: {replica.replica_name}")
        print(f"  Replica ID: {replica.replica_id}")
        print(f"  Replica Type: {replica.replica_type}")
        print("=" * 50)
        print("WARNING: This action cannot be undone!")
        print("=" * 50)
        
        cli = YesNo("Are you sure you want to delete this replica?", default="n")
        if not cli.launch():
            print("Delete operation cancelled.")
            input("Press Enter to continue...")
            return None  # Return to replica list
        
        with yaspin(text="Deleting replica..."):
            success, message = state_machine.api_client.delete_replica(replica.replica_id)
        
        if success:
            print(f"Replica deleted successfully: {replica.replica_name}")
            # Remove the replica from our local list
            self.replicas = [r for r in self.replicas if r.replica_id != replica.replica_id]
        else:
            print(f"Error deleting replica: {message}")
        
        input("Press Enter to continue...")
        return "work_with_replicas"
    
    def _update_replicas(self, state_machine) -> None:
        """Update the replicas list from API"""
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return

        success, message, fetched_replicas = state_machine.api_client.list_replicas()
        if success:
            # Convert dictionary data to Replica objects
            self.replicas = fetched_replicas
        else:
            print(message)
    
    def _show_paginated_replicas(self, state_machine, page=0, items_per_page=10, filter_type="all", on_replica_select=None, show_filter_option=True):
        """Show paginated list of replicas with selection"""
        if not self.replicas:
            print("No replicas found.")
            input("Press Enter to continue...")
            return "work_with_replicas"

        # Filter replicas based on type
        if filter_type == "user":
            filtered_replicas = [r for r in self.replicas if r.replica_type == "user"]
            sectioned_replicas = [filtered_replicas]
            section_names = ["User Replicas"]
        elif filter_type == "system":
            filtered_replicas = [r for r in self.replicas if r.replica_type == "system"]
            sectioned_replicas = [filtered_replicas]
            section_names = ["System Replicas"]
        else:  # "all"
            user_replicas = [r for r in self.replicas if r.replica_type == "user"]
            system_replicas = [r for r in self.replicas if r.replica_type == "system"]
            filtered_replicas = user_replicas + system_replicas
            sectioned_replicas = [user_replicas, system_replicas]
            section_names = ["User Replicas", "System Replicas"]

        if not filtered_replicas:
            # Create empty paginated list for proper empty state handling
            paginated_list = PaginatedList([])
            result = paginated_list.show(
                title="Replicas",
                filter_type=filter_type,
                on_filter_change=self._handle_replica_filter_change,
                show_filter_option=show_filter_option
            )
            return self._handle_replica_pagination_result(result, items_per_page, filter_type, on_replica_select, show_filter_option, state_machine)

        # Create sectioned paginated list
        paginated_list = SectionedPaginatedList(filtered_replicas, items_per_page)
        paginated_list.set_sections(sectioned_replicas, section_names)
        paginated_list.set_page(page)

        def on_replica_select_wrapper(replica):
            if on_replica_select:
                # Call the custom callback function
                result_state = on_replica_select(replica, state_machine)
                if result_state:
                    return PaginatedListResult(PaginationAction.ITEM_SELECTED, result_state)
                # If callback returns None, continue showing the list
                return PaginatedListResult(PaginationAction.NO_ACTION, paginated_list.get_current_page())
            else:
                # Default behavior: show replica details
                self._show_replica_details(replica)
                input("Press Enter to continue...")
                # Return the current page so we stay on the same page
                return PaginatedListResult(PaginationAction.NO_ACTION, paginated_list.get_current_page())

        result = paginated_list.show(
            title="Replicas",
            filter_type=filter_type,
            on_item_select=on_replica_select_wrapper,
            on_filter_change=self._handle_replica_filter_change,
            show_filter_option=show_filter_option
        )

        return self._handle_replica_pagination_result(result, items_per_page, filter_type, on_replica_select, show_filter_option, state_machine)
    
    def _handle_replica_filter_change(self, filter_type):
        """Handle replica filter change"""
        return PaginatedListResult(PaginationAction.FILTER_CHANGED, filter_type)

    def _handle_replica_pagination_result(self, result, items_per_page, filter_type, on_replica_select, show_filter_option, state_machine):
        """Handle pagination result for replicas"""
        if result.action == PaginationAction.PREVIOUS_PAGE:
            return self._show_paginated_replicas(state_machine, result.data, items_per_page, filter_type, on_replica_select, show_filter_option)
        elif result.action == PaginationAction.NEXT_PAGE:
            return self._show_paginated_replicas(state_machine, result.data, items_per_page, filter_type, on_replica_select, show_filter_option)
        elif result.action == PaginationAction.GO_BACK:
            return "work_with_replicas"
        elif result.action == PaginationAction.FILTER_CHANGED:
            # Handle filter change while preserving the callback
            return self._show_replica_filter_selection_with_callback(on_replica_select, state_machine)
        elif result.action == PaginationAction.ITEM_SELECTED:
            # Return the state from the custom callback
            return result.data
        else:
            # Use the page from result.data if available, otherwise default to 0
            current_page = result.data if result.data is not None else 0
            return self._show_paginated_replicas(state_machine, current_page, items_per_page, filter_type, on_replica_select, show_filter_option)

    def _show_replica_filter_selection_with_callback(self, on_replica_select=None, state_machine=None):
        """Show filter selection for replicas with optional callback preservation"""
        print("\n=== Filter Replicas ===")
        
        # If we have a callback, preserve it through filter selection
        if on_replica_select:
            cli = Bullet(
                prompt="Select filter type:",
                choices=["user", "system", "all"],
                bullet="→",
                margin=2,
                shift=0,
            )
            result = cli.launch()

            if result == "user":
                return self._show_paginated_replicas(state_machine, filter_type="user", on_replica_select=on_replica_select, show_filter_option=True)
            elif result == "system":
                return self._show_paginated_replicas(state_machine, filter_type="system", on_replica_select=on_replica_select, show_filter_option=True)
            elif result == "all":
                return self._show_paginated_replicas(state_machine, filter_type="all", on_replica_select=on_replica_select, show_filter_option=True)
        else:
            # Standard filter selection for normal browsing
            cli = Bullet(
                prompt="Select filter type:",
                choices=["user", "system", "all"],
                bullet="→",
                margin=2,
                shift=0,
            )
            result = cli.launch()

            if result == "user":
                return self._show_paginated_replicas(state_machine, filter_type="user", show_filter_option=True)
            elif result == "system":
                return self._show_paginated_replicas(state_machine, filter_type="system", show_filter_option=True)
            elif result == "all":
                return self._show_paginated_replicas(state_machine, filter_type="all", show_filter_option=True)
        
        return self._show_paginated_replicas(state_machine, show_filter_option=True)
    
    def _show_replica_details(self, replica):
        """Show detailed information for a specific replica"""
        print("\n" + "=" * 60)
        print("REPLICA DETAILS")
        print("=" * 60)
        print(replica.display_verbose())
        print("=" * 60) 