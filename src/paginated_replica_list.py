#!/usr/bin/env python3

from typing import List, Callable, Optional, Any, Union
from paginated_list import PaginatedList, SectionedPaginatedList, PaginatedListResult, PaginationAction
from bullet import Bullet

class PaginatedReplicaList:
    """Generic paginated replica list that can be used by all modules"""
    
    def __init__(self, replicas: List[Any], items_per_page: int = 10):
        self.replicas = replicas
        self.items_per_page = items_per_page
    
    def show(self, 
             state_machine,
             page: int = 0,
             filter_type: str = "all",
             on_replica_select: Optional[Callable[[Any, Any], str]] = None,
             show_filter_option: bool = True,
             title: str = "Replicas",
             return_replica_id: bool = False) -> Optional[str]:
        """
        Show a paginated list of replicas with selection
        
        Args:
            state_machine: The state machine instance
            page: Current page number
            filter_type: Current filter type ("all", "user", "system")
            on_replica_select: Optional callback function when a replica is selected
            show_filter_option: Whether to show filter selection option
            title: Title for the list display
            return_replica_id: If True, return replica ID instead of calling callback
            
        Returns:
            Optional[str]: Next state or replica ID depending on configuration, or None to cancel
        """
        if not self.replicas:
            print("No replicas found.")
            input("Press Enter to continue...")
            return None

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
                title=title,
                filter_type=filter_type,
                on_filter_change=self._handle_filter_change,
                show_filter_option=show_filter_option
            )
            return self._handle_pagination_result(result, state_machine, page, filter_type, on_replica_select, show_filter_option, title, return_replica_id)

        # Create sectioned paginated list
        paginated_list = SectionedPaginatedList(filtered_replicas, self.items_per_page)
        paginated_list.set_sections(sectioned_replicas, section_names)
        paginated_list.set_page(page)

        def on_replica_select_wrapper(replica):
            if return_replica_id:
                # Return the replica ID for selection
                return PaginatedListResult(PaginationAction.ITEM_SELECTED, replica.replica_id)
            elif on_replica_select:
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
            title=title,
            filter_type=filter_type,
            on_item_select=on_replica_select_wrapper,
            on_filter_change=self._handle_filter_change,
            show_filter_option=show_filter_option
        )

        return self._handle_pagination_result(result, state_machine, page, filter_type, on_replica_select, show_filter_option, title, return_replica_id)
    
    def _handle_filter_change(self, filter_type):
        """Handle filter change"""
        return PaginatedListResult(PaginationAction.FILTER_CHANGED, filter_type)

    def _handle_pagination_result(self, result, state_machine, page, filter_type, on_replica_select, show_filter_option, title, return_replica_id):
        """Handle pagination result"""
        if result.action == PaginationAction.PREVIOUS_PAGE:
            return self.show(state_machine, result.data, filter_type, on_replica_select, show_filter_option, title, return_replica_id)
        elif result.action == PaginationAction.NEXT_PAGE:
            return self.show(state_machine, result.data, filter_type, on_replica_select, show_filter_option, title, return_replica_id)
        elif result.action == PaginationAction.GO_BACK:
            return None  # Cancel selection
        elif result.action == PaginationAction.FILTER_CHANGED:
            # Handle filter change - show filter selection
            return self._show_filter_selection(state_machine, on_replica_select, show_filter_option, title, return_replica_id)
        elif result.action == PaginationAction.ITEM_SELECTED:
            # Return the state from the custom callback or replica ID
            return result.data
        else:
            # Use the page from result.data if available, otherwise default to 0
            current_page = result.data if result.data is not None else 0
            return self.show(state_machine, current_page, filter_type, on_replica_select, show_filter_option, title, return_replica_id)

    def _show_filter_selection(self, state_machine, on_replica_select=None, show_filter_option=True, title="Replicas", return_replica_id=False):
        """Show filter selection for replicas"""
        print("\n=== Filter Replicas ===")
        
        cli = Bullet(
            prompt="Select filter type:",
            choices=["user", "system", "all"],
            bullet="→",
            margin=2,
            shift=0,
        )
        result = cli.launch()

        if result == "user":
            return self.show(state_machine, filter_type="user", on_replica_select=on_replica_select, show_filter_option=show_filter_option, title=title, return_replica_id=return_replica_id)
        elif result == "system":
            return self.show(state_machine, filter_type="system", on_replica_select=on_replica_select, show_filter_option=show_filter_option, title=title, return_replica_id=return_replica_id)
        elif result == "all":
            return self.show(state_machine, filter_type="all", on_replica_select=on_replica_select, show_filter_option=show_filter_option, title=title, return_replica_id=return_replica_id)
        
        return self.show(state_machine, filter_type="all", on_replica_select=on_replica_select, show_filter_option=show_filter_option, title=title, return_replica_id=return_replica_id)
    
    def _show_replica_details(self, replica):
        """Show detailed information for a specific replica"""
        print("\n" + "=" * 60)
        print("REPLICA DETAILS")
        print("=" * 60)
        print(replica.display_verbose())
        print("=" * 60) 