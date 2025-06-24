#!/usr/bin/env python3

from typing import List, Callable, Optional, Any
from bullet import Bullet
from enum import Enum

class PaginationAction(Enum):
    """Actions that can be returned from paginated list interactions"""
    PREVIOUS_PAGE = "previous_page"
    NEXT_PAGE = "next_page"
    GO_BACK = "go_back"
    ITEM_SELECTED = "item_selected"
    FILTER_CHANGED = "filter_changed"
    NO_ACTION = "no_action"

class PaginatedListResult:
    """Result object returned from paginated list interactions"""
    def __init__(self, action: PaginationAction, data: Any = None):
        self.action = action
        self.data = data

class PaginatedList:
    """Generic paginated list display component"""
    
    def __init__(self, items: List[Any], items_per_page: int = 10):
        self.items = items
        self.items_per_page = items_per_page
        self.current_page = 0
    
    def show(self, 
             title: str = "Items",
             filter_type: str = "all",
             on_item_select: Optional[Callable[[Any], PaginatedListResult]] = None,
             on_filter_change: Optional[Callable[[str], PaginatedListResult]] = None,
             show_filter_option: bool = True,
             custom_choices: Optional[List[str]] = None) -> PaginatedListResult:
        """
        Show a paginated list of items
        
        Args:
            title: Title for the list display
            filter_type: Current filter type (e.g., "all", "user", "system")
            on_item_select: Callback function when an item is selected
            on_filter_change: Callback function when filter is changed
            show_filter_option: Whether to show filter selection option
            custom_choices: Custom choices to add to the menu
            
        Returns:
            PaginatedListResult: Result indicating the action taken
        """
        if not self.items:
            return self._show_empty_list(title, filter_type, on_filter_change)
        
        total_pages = (len(self.items) - 1) // self.items_per_page
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.items))
        current_items = self.items[start_idx:end_idx]
        
        print(f"\nPage {self.current_page + 1} of {total_pages + 1} ({len(self.items)} {filter_type} {title.lower()})")
        print("=" * 50)
        
        # Build choices list
        choices = []
        
        # Add filter option if enabled
        if show_filter_option:
            choices.append(f"Current filter: {filter_type}")
        
        # Add custom choices if provided
        if custom_choices:
            choices.extend(custom_choices)
        
        # Add navigation options
        if self.current_page > 0:
            choices.append("← Previous Page")
        
        # Add item choices
        for i, item in enumerate(current_items, start_idx + 1):
            if hasattr(item, 'display_short'):
                choices.append(f"{i}. {item.display_short()}")
            else:
                choices.append(f"{i}. {str(item)}")
        
        # Add navigation options
        if self.current_page < total_pages:
            choices.append("→ Next Page")
        
        choices.append("← Go Back")
        
        # Show menu
        cli = Bullet(
            prompt=f"Select a {title.lower()} to view details or navigate:",
            choices=choices,
            bullet="→",
            margin=2,
            shift=0,
        )
        result = cli.launch()
        
        # Handle filter selection
        if show_filter_option and result == f"Current filter: {filter_type}":
            if on_filter_change:
                return on_filter_change(filter_type)
            return PaginatedListResult(PaginationAction.FILTER_CHANGED, filter_type)
        
        # Handle navigation
        if result == "← Previous Page":
            self.current_page -= 1
            return PaginatedListResult(PaginationAction.PREVIOUS_PAGE, self.current_page)
        elif result == "→ Next Page":
            self.current_page += 1
            return PaginatedListResult(PaginationAction.NEXT_PAGE, self.current_page)
        elif result == "← Go Back":
            return PaginatedListResult(PaginationAction.GO_BACK)
        
        # Handle item selection
        if result.startswith("→") or result.startswith("---"):
            return PaginatedListResult(PaginationAction.NO_ACTION)
        
        # Extract item index from selection
        try:
            item_idx = int(result.split('.')[0]) - 1
            if 0 <= item_idx < len(self.items):
                selected_item = self.items[item_idx]
                
                if on_item_select:
                    return on_item_select(selected_item)
                else:
                    # Default behavior: show item details
                    self._show_item_details(selected_item)
                    input("Press Enter to continue...")
                    return PaginatedListResult(PaginationAction.NO_ACTION)
        except (ValueError, IndexError):
            pass
        
        return PaginatedListResult(PaginationAction.NO_ACTION)
    
    def _show_empty_list(self, title: str, filter_type: str, 
                        on_filter_change: Optional[Callable[[str], PaginatedListResult]]) -> PaginatedListResult:
        """Show empty list with options"""
        print(f"\nNo {filter_type} {title.lower()} found.")
        print("=" * 50)
        
        choices = []
        choices.append(f"Current filter: {filter_type}")
        choices.append("← Go Back")
        
        cli = Bullet(
            prompt=f"No {title.lower()} found. What would you like to do?",
            choices=choices,
            bullet="→",
            margin=2,
            shift=0,
        )
        result = cli.launch()
        
        if result == f"Current filter: {filter_type}":
            if on_filter_change:
                return on_filter_change(filter_type)
            return PaginatedListResult(PaginationAction.FILTER_CHANGED, filter_type)
        elif result == "← Go Back":
            return PaginatedListResult(PaginationAction.GO_BACK)
        
        return PaginatedListResult(PaginationAction.NO_ACTION)
    
    def _show_item_details(self, item: Any):
        """Show detailed information for a specific item"""
        print("\n" + "=" * 60)
        print(f"{type(item).__name__.upper()} DETAILS")
        print("=" * 60)
        
        if hasattr(item, 'display_verbose'):
            print(item.display_verbose())
        else:
            print(str(item))
        
        print("=" * 60)
    
    def set_page(self, page: int):
        """Set the current page"""
        self.current_page = max(0, page)
    
    def get_current_page(self) -> int:
        """Get the current page number"""
        return self.current_page
    
    def get_total_pages(self) -> int:
        """Get the total number of pages"""
        return (len(self.items) - 1) // self.items_per_page
    
    def get_items_count(self) -> int:
        """Get the total number of items"""
        return len(self.items)


class FilteredPaginatedList(PaginatedList):
    """Paginated list with filtering capabilities"""
    
    def __init__(self, items: List[Any], items_per_page: int = 10):
        super().__init__(items, items_per_page)
        self.filtered_items = items
        self.current_filter = "all"
    
    def set_filter(self, filter_func: Callable[[Any], bool], filter_name: str = "filtered"):
        """Set a filter function to filter items"""
        self.filtered_items = [item for item in self.items if filter_func(item)]
        self.current_filter = filter_name
        self.current_page = 0  # Reset to first page when filter changes
    
    def clear_filter(self):
        """Clear the current filter"""
        self.filtered_items = self.items
        self.current_filter = "all"
        self.current_page = 0
    
    def show(self, 
             title: str = "Items",
             filter_type: str = "all",
             on_item_select: Optional[Callable[[Any], PaginatedListResult]] = None,
             on_filter_change: Optional[Callable[[str], PaginatedListResult]] = None,
             show_filter_option: bool = True,
             custom_choices: Optional[List[str]] = None) -> PaginatedListResult:
        """Show filtered paginated list"""
        # Temporarily replace items with filtered items
        original_items = self.items
        self.items = self.filtered_items
        
        try:
            result = super().show(title, filter_type, on_item_select, on_filter_change, 
                                show_filter_option, custom_choices)
            return result
        finally:
            # Restore original items
            self.items = original_items
    
    def get_filtered_items_count(self) -> int:
        """Get the count of filtered items"""
        return len(self.filtered_items)
    
    def get_current_filter(self) -> str:
        """Get the current filter name"""
        return self.current_filter


class SectionedPaginatedList(PaginatedList):
    """Paginated list with sections (e.g., User Replicas, System Replicas)"""
    
    def __init__(self, items: List[Any], items_per_page: int = 10):
        super().__init__(items, items_per_page)
        self.sections = []
        self.section_names = []
    
    def set_sections(self, sections: List[List[Any]], section_names: List[str]):
        """Set sections for the list"""
        self.sections = sections
        self.section_names = section_names
        # Flatten sections into items for pagination
        self.items = []
        for section in sections:
            self.items.extend(section)
    
    def show(self, 
             title: str = "Items",
             filter_type: str = "all",
             on_item_select: Optional[Callable[[Any], PaginatedListResult]] = None,
             on_filter_change: Optional[Callable[[str], PaginatedListResult]] = None,
             show_filter_option: bool = True,
             custom_choices: Optional[List[str]] = None) -> PaginatedListResult:
        """Show sectioned paginated list"""
        if not self.items:
            return self._show_empty_list(title, filter_type, on_filter_change)
        
        total_pages = (len(self.items) - 1) // self.items_per_page
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.items))
        current_items = self.items[start_idx:end_idx]
        
        print(f"\nPage {self.current_page + 1} of {total_pages + 1} ({len(self.items)} {filter_type} {title.lower()})")
        print("=" * 50)
        
        # Build choices list
        choices = []
        
        # Add filter option if enabled
        if show_filter_option:
            choices.append(f"Current filter: {filter_type}")
        
        # Add custom choices if provided
        if custom_choices:
            choices.extend(custom_choices)
        
        # Add navigation options
        if self.current_page > 0:
            choices.append("← Previous Page")
        
        # Add sectioned items with headers
        if len(self.sections) > 1:
            # Multi-section view
            for i, item in enumerate(current_items):
                global_idx = start_idx + i + 1
                
                # Find which section this item belongs to
                section_idx = self._find_item_section(item, start_idx + i)
                if section_idx >= 0 and section_idx < len(self.section_names):
                    # Check if this is the first item in this section on this page
                    if self._is_first_item_in_section_on_page(item, start_idx + i, start_idx):
                        choices.append(f"--- {self.section_names[section_idx]} ---")
                
                if hasattr(item, 'display_short'):
                    choices.append(f"{global_idx}. {item.display_short()}")
                else:
                    choices.append(f"{global_idx}. {str(item)}")
        else:
            # Single section view
            for i, item in enumerate(current_items, start_idx + 1):
                if hasattr(item, 'display_short'):
                    choices.append(f"{i}. {item.display_short()}")
                else:
                    choices.append(f"{i}. {str(item)}")
        
        # Add navigation options
        if self.current_page < total_pages:
            choices.append("→ Next Page")
        
        choices.append("← Go Back")
        
        # Show menu
        cli = Bullet(
            prompt=f"Select a {title.lower()} to view details or navigate:",
            choices=choices,
            bullet="→",
            margin=2,
            shift=0,
        )
        result = cli.launch()
        
        # Handle filter selection
        if show_filter_option and result == f"Current filter: {filter_type}":
            if on_filter_change:
                return on_filter_change(filter_type)
            return PaginatedListResult(PaginationAction.FILTER_CHANGED, filter_type)
        
        # Handle navigation
        if result == "← Previous Page":
            self.current_page -= 1
            return PaginatedListResult(PaginationAction.PREVIOUS_PAGE, self.current_page)
        elif result == "→ Next Page":
            self.current_page += 1
            return PaginatedListResult(PaginationAction.NEXT_PAGE, self.current_page)
        elif result == "← Go Back":
            return PaginatedListResult(PaginationAction.GO_BACK)
        
        # Handle item selection
        if result.startswith("→") or result.startswith("---"):
            return PaginatedListResult(PaginationAction.NO_ACTION)
        
        # Extract item index from selection
        try:
            item_idx = int(result.split('.')[0]) - 1
            if 0 <= item_idx < len(self.items):
                selected_item = self.items[item_idx]
                
                if on_item_select:
                    return on_item_select(selected_item)
                else:
                    # Default behavior: show item details
                    self._show_item_details(selected_item)
                    input("Press Enter to continue...")
                    return PaginatedListResult(PaginationAction.NO_ACTION)
        except (ValueError, IndexError):
            pass
        
        return PaginatedListResult(PaginationAction.NO_ACTION)
    
    def _find_item_section(self, item: Any, global_idx: int) -> int:
        """Find which section an item belongs to based on its global index"""
        if not self.sections:
            return -1
        
        # Calculate which section this item belongs to based on the flattened sections
        current_idx = 0
        for section_idx, section in enumerate(self.sections):
            if current_idx <= global_idx < current_idx + len(section):
                return section_idx
            current_idx += len(section)
        
        return -1
    
    def _is_first_item_in_section_on_page(self, item: Any, global_idx: int, page_start_idx: int) -> bool:
        """Check if this is the first item of its section on the current page"""
        if not self.sections:
            return False
        
        # Find which section this item belongs to
        section_idx = self._find_item_section(item, global_idx)
        if section_idx < 0:
            return False
        
        # Check if this is the first item of this section on this page
        current_idx = 0
        for i, section in enumerate(self.sections):
            if i == section_idx:
                # This is the section we're looking for
                section_start_idx = current_idx
                section_end_idx = current_idx + len(section)
                
                # Check if this item is the first item of this section on this page
                if (section_start_idx <= global_idx < section_end_idx and 
                    (global_idx == page_start_idx or 
                     self._find_item_section(self.items[global_idx - 1], global_idx - 1) != section_idx)):
                    return True
                break
            current_idx += len(section)
        
        return False 