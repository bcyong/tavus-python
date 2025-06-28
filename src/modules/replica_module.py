#!/usr/bin/env python3

from bullet import Bullet, YesNo
from yaspin import yaspin
from . import ModuleInterface, CommonStates
from paginated_replica_list import PaginatedReplicaList

class ReplicaModule(ModuleInterface):
    """Module for managing replicas"""
    
    def __init__(self):
        self.replicas = []
    
    def get_name(self) -> str:
        return "Replica Management"
    
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
        """Execute the given state and return the next state"""
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
        else:
            return CommonStates.MAIN_MENU
    
    def _execute_work_with_replicas(self, state_machine) -> str:
        """Execute work with replicas functionality and return next state"""
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
            return "work_with_replicas"  # Return to replica list
        
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
            return "work_with_replicas"  # Return to replica list
        
        # Show confirmation dialog
        print(f"\nConfirm rename operation:")
        print(f"  From: {replica.replica_name}")
        print(f"  To:   {new_name}")
        print("=" * 50)
        
        cli = YesNo("Are you sure you want to rename this replica?", default="n")
        if not cli.launch():
            print("Rename operation cancelled.")
            input("Press Enter to continue...")
            return "work_with_replicas"  # Return to replica list
        
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
            return "work_with_replicas"  # Return to replica list
        
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
            return "work_with_replicas"  # Return to replica list
        
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
        """Show paginated list of replicas with selection using the generic class"""
        if not self.replicas:
            print("No replicas found.")
            input("Press Enter to continue...")
            return "work_with_replicas"

        # Use the generic paginated replica list
        paginated_list = PaginatedReplicaList(self.replicas, items_per_page)
        result = paginated_list.show(
            state_machine=state_machine,
            page=page,
            filter_type=filter_type,
            on_replica_select=on_replica_select,
            show_filter_option=show_filter_option,
            title="Replicas"
        )
        
        # Handle the result
        if result is None:
            return "work_with_replicas"
        elif isinstance(result, str):
            return result
        else:
            return "work_with_replicas"
    
    def _show_replica_details(self, replica):
        """Show detailed information for a specific replica"""
        print("\n" + "=" * 60)
        print("REPLICA DETAILS")
        print("=" * 60)
        print(replica.display_verbose())
        print("=" * 60) 