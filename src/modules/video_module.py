#!/usr/bin/env python3

from bullet import Bullet, YesNo
from yaspin import yaspin
from . import ModuleInterface, CommonStates
from models import Video
from paginated_list import PaginatedList, PaginatedListResult, PaginationAction, SectionedPaginatedList

class VideoModule(ModuleInterface):
    """Module for handling video management"""
    
    def __init__(self):
        self.videos = []  # Local storage for videos
        self.replicas = []  # Local storage for replicas (needed for video creation)
    
    def get_name(self) -> str:
        return "video"
    
    def get_states(self) -> list:
        return [
            "work_with_videos",
            "generate_video",
            "list_videos",
            "rename_video",
            "delete_video"
        ]
    
    def get_menu_options(self) -> list:
        return ["Work with Videos"]
    
    def get_choice_to_state_mapping(self) -> dict:
        return {
            "Work with Videos": "work_with_videos"
        }
    
    def execute_state(self, state: str, state_machine) -> str:
        if state == "work_with_videos":
            return self._execute_work_with_videos(state_machine)
        elif state == "generate_video":
            return self._execute_generate_video(state_machine)
        elif state == "list_videos":
            return self._execute_list_videos(state_machine)
        elif state == "rename_video":
            return self._execute_rename_video(state_machine)
        elif state == "delete_video":
            return self._execute_delete_video(state_machine)
        return CommonStates.MAIN_MENU
    
    def _execute_work_with_videos(self, state_machine) -> str:
        """Execute work with videos menu and return next state"""
        print("\n=== Work with Videos ===")
        
        with yaspin(text="Loading videos..."):
            self._update_videos(state_machine)

        cli = Bullet(
            prompt="What would you like to do with Videos?",
            choices=["Generate a Video", "List Videos", "Rename a Video", "Delete a Video", "Back to Main Menu"],
            bullet="🎬",
            margin=2,
            shift=0,
        )
        result = cli.launch()

        if result == "Generate a Video":
            return "generate_video"
        elif result == "List Videos":
            return "list_videos"
        elif result == "Rename a Video":
            return "rename_video"
        elif result == "Delete a Video":
            return "delete_video"
        elif result == "Back to Main Menu":
            return CommonStates.MAIN_MENU
        else:
            return "work_with_videos"
    
    def _execute_generate_video(self, state_machine) -> str:
        """Execute generate video functionality and return next state"""
        print("\n=== Generate Video ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        # Collect video generation parameters
        video_name = input("Video Name: ")
        
        if not video_name or not video_name.strip():
            print("Video name cannot be empty. Please try again.")
            input("Press Enter to continue...")
            return "work_with_videos"

        # Select replica from paginated list
        print("Select a replica for this video:")
        replica_selection_result = self._show_paginated_replicas_for_selection(state_machine)
        if replica_selection_result is None:
            print("Replica selection cancelled.")
            input("Press Enter to continue...")
            return "work_with_videos"
        
        replica_id = replica_selection_result

        script = input("Script: ")
        
        if not script or not script.strip():
            print("Script cannot be empty. Please try again.")
            input("Press Enter to continue...")
            return "work_with_videos"
        
        # Show final confirmation
        print(f"\nConfirm video generation:")
        print(f"  Name: {video_name}")
        print(f"  Replica ID: {replica_id}")
        print(f"  Script: {script[:100]}{'...' if len(script) > 100 else ''}")
        print("=" * 50)
        
        cli = YesNo("Proceed with video generation? ", default="n")
        if not cli.launch():
            print("Video generation cancelled.")
            input("Press Enter to continue...")
            return "work_with_videos"
        
        # Prepare video data
        video_data = {
            "video_name": video_name,
            "replica_id": replica_id,
            "script": script
        }
        
        with yaspin(text="Generating video..."):
            success, message, response_data = state_machine.api_client.generate_video(video_data)
        
        if success:
            print(f"\n✅ {message}")
            if response_data:
                print(f"Video ID: {response_data.video_id}")
                print(f"Video Name: {response_data.video_name}")
                print(f"Status: {response_data.status}")
            else:
                print("Video ID: N/A")
                print("Video Name: N/A")
                print("Status: N/A")
            print("\nNote: Video generation is now in progress. You can check the status later.")
        else:
            print(f"\n❌ {message}")
        
        input("Press Enter to continue...")
        return "work_with_videos"
    
    def _execute_list_videos(self, state_machine) -> str:
        """Execute list videos functionality and return next state"""
        print("\n=== List Videos ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        return self._show_paginated_videos(state_machine)
    
    def _execute_rename_video(self, state_machine) -> str:
        """Execute rename video functionality and return next state"""
        print("\n=== Rename Video ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        return self._show_paginated_videos(state_machine, on_video_select=self._handle_video_rename)
    
    def _execute_delete_video(self, state_machine) -> str:
        """Execute delete video functionality and return next state"""
        print("\n=== Delete Video ===")
        
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return CommonStates.MAIN_MENU

        return self._show_paginated_videos(state_machine, on_video_select=self._handle_video_delete)
    
    def _handle_video_rename(self, video, state_machine) -> str:
        """Handle video rename when a video is selected from the list"""
        print(f"\nRenaming video: {video.video_name} ({video.video_id})")
        print("=" * 50)
        
        # Show full video details first
        self._show_video_details(video)
        print("=" * 50)
        
        if state_machine.api_client is None:
            print("Error: API client not initialized.")
            input("Press Enter to continue...")
            return "work_with_videos"
        
        new_name = input("New name: ")
        
        if not new_name or not new_name.strip():
            print("Video name cannot be empty. Please try again.")
            input("Press Enter to continue...")
            return None  # Return to video list
        
        # Show confirmation dialog
        print(f"\nConfirm rename operation:")
        print(f"  From: {video.video_name}")
        print(f"  To:   {new_name}")
        print("=" * 50)
        
        cli = YesNo("Are you sure you want to rename this video?", default="n")
        if not cli.launch():
            print("Rename operation cancelled.")
            input("Press Enter to continue...")
            return None  # Return to video list
        
        with yaspin(text="Renaming video..."):
            success, message = state_machine.api_client.rename_video(video.video_id, new_name)
        
        if success:
            print(f"Video renamed successfully to: {new_name}")
            # Update the video object in our list
            video.video_name = new_name
        else:
            print(f"Error renaming video: {message}")
        
        input("Press Enter to continue...")
        return "work_with_videos"
    
    def _handle_video_delete(self, video, state_machine) -> str:
        """Handle video delete when a video is selected from the list"""
        print(f"\nDeleting video: {video.video_name} ({video.video_id})")
        print("=" * 50)
        
        # Show full video details first
        self._show_video_details(video)
        print("=" * 50)
        
        if state_machine.api_client is None:
            print("Error: API client not initialized.")
            input("Press Enter to continue...")
            return "work_with_videos"
        
        # Show confirmation dialog
        print(f"\nConfirm delete operation:")
        print(f"  Video Name: {video.video_name}")
        print(f"  Video ID: {video.video_id}")
        print(f"  Status: {video.status}")
        print("=" * 50)
        print("WARNING: This action cannot be undone!")
        print("=" * 50)
        
        cli = YesNo("Are you sure you want to delete this video?", default="n")
        if not cli.launch():
            print("Delete operation cancelled.")
            input("Press Enter to continue...")
            return None  # Return to video list
        
        with yaspin(text="Deleting video..."):
            success, message = state_machine.api_client.delete_video(video.video_id)
        
        if success:
            print(f"Video deleted successfully: {video.video_name}")
            # Remove the video from our local list
            self.videos.remove(video)
        else:
            print(f"Error deleting video: {message}")
        
        input("Press Enter to continue...")
        return "work_with_videos"
    
    def _update_videos(self, state_machine) -> None:
        """Update the videos list from API"""
        if state_machine.api_client is None:
            print("Error: API client not initialized. Please set your API key first.")
            return

        success, message, fetched_videos = state_machine.api_client.list_videos()
        if success:
            self.videos = fetched_videos
        else:
            print(message)
    
    def _show_paginated_videos(self, state_machine, page=0, items_per_page=10, on_video_select=None):
        """Show paginated list of videos with selection"""
        if not self.videos:
            print("No videos found.")
            input("Press Enter to continue...")
            return "work_with_videos"

        # Create paginated list
        paginated_list = PaginatedList(self.videos, items_per_page)
        paginated_list.set_page(page)

        def on_video_select_wrapper(video):
            if on_video_select:
                # Call the custom callback function
                result_state = on_video_select(video, state_machine)
                if result_state:
                    return PaginatedListResult(PaginationAction.ITEM_SELECTED, result_state)
                # If callback returns None, continue showing the list
                return PaginatedListResult(PaginationAction.NO_ACTION, paginated_list.get_current_page())
            else:
                # Default behavior: show video details
                self._show_video_details(video)
                input("Press Enter to continue...")
                # Return the current page so we stay on the same page
                return PaginatedListResult(PaginationAction.NO_ACTION, paginated_list.get_current_page())

        result = paginated_list.show(
            title="Videos",
            on_item_select=on_video_select_wrapper,
            show_filter_option=False
        )

        return self._handle_video_pagination_result(result, items_per_page, on_video_select, state_machine)
    
    def _handle_video_pagination_result(self, result, items_per_page, on_video_select, state_machine):
        """Handle pagination result for videos"""
        if result.action == PaginationAction.PREVIOUS_PAGE:
            return self._show_paginated_videos(state_machine, result.data, items_per_page, on_video_select)
        elif result.action == PaginationAction.NEXT_PAGE:
            return self._show_paginated_videos(state_machine, result.data, items_per_page, on_video_select)
        elif result.action == PaginationAction.GO_BACK:
            return "work_with_videos"
        elif result.action == PaginationAction.ITEM_SELECTED:
            # Return the state from the custom callback
            return result.data
        else:
            # Use the page from result.data if available, otherwise default to 0
            current_page = result.data if result.data is not None else 0
            return self._show_paginated_videos(state_machine, current_page, items_per_page, on_video_select)
    
    def _show_video_details(self, video):
        """Show detailed information for a specific video"""
        print("\n" + "=" * 60)
        print("VIDEO DETAILS")
        print("=" * 60)
        print(video.display_verbose())
        print("=" * 60)
    
    def _show_paginated_replicas_for_selection(self, state_machine, page=0, filter_type="all"):
        """Show paginated list of replicas for selection and return the selected replica ID"""
        # Update replicas if needed
        if not self.replicas:
            with yaspin(text="Loading replicas..."):
                self._update_replicas_for_selection(state_machine)
        
        if not self.replicas:
            print("No replicas found. Please create a replica first.")
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
            print(f"No {filter_type} replicas found.")
            input("Press Enter to continue...")
            return None

        # Create paginated list - use sectioned list for "all" filter
        if filter_type == "all":
            paginated_list = SectionedPaginatedList(filtered_replicas, 10)
            paginated_list.set_sections(sectioned_replicas, section_names)
        else:
            paginated_list = PaginatedList(filtered_replicas, 10)
        
        paginated_list.set_page(page)

        def on_replica_select_wrapper(replica):
            # Return the replica ID for selection
            return PaginatedListResult(PaginationAction.ITEM_SELECTED, replica.replica_id)

        def on_filter_change_wrapper(filter_type):
            return PaginatedListResult(PaginationAction.FILTER_CHANGED, filter_type)

        result = paginated_list.show(
            title="Select Replica",
            filter_type=filter_type,
            on_item_select=on_replica_select_wrapper,
            on_filter_change=on_filter_change_wrapper,
            show_filter_option=True
        )

        return self._handle_replica_selection_result(result, state_machine, page, filter_type)
    
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
    
    def _handle_replica_selection_result(self, result, state_machine, current_page=0, current_filter="all"):
        """Handle pagination result for replica selection"""
        if result.action == PaginationAction.PREVIOUS_PAGE:
            return self._show_paginated_replicas_for_selection(state_machine, result.data, current_filter)
        elif result.action == PaginationAction.NEXT_PAGE:
            return self._show_paginated_replicas_for_selection(state_machine, result.data, current_filter)
        elif result.action == PaginationAction.GO_BACK:
            return None  # Cancel selection
        elif result.action == PaginationAction.FILTER_CHANGED:
            # Handle filter change - show filter selection
            return self._show_replica_filter_selection_for_video(state_machine)
        elif result.action == PaginationAction.ITEM_SELECTED:
            # Return the selected replica ID
            return result.data
        else:
            # Use the page from result.data if available, otherwise default to 0
            current_page = result.data if result.data is not None else 0
            return self._show_paginated_replicas_for_selection(state_machine, current_page, current_filter)
    
    def _show_replica_filter_selection_for_video(self, state_machine):
        """Show filter selection for replicas when creating a video"""
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
            return self._show_paginated_replicas_for_selection(state_machine, filter_type="user")
        elif result == "system":
            return self._show_paginated_replicas_for_selection(state_machine, filter_type="system")
        elif result == "all":
            return self._show_paginated_replicas_for_selection(state_machine, filter_type="all")
        
        return self._show_paginated_replicas_for_selection(state_machine, filter_type="all") 