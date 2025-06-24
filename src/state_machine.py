#!/usr/bin/env python3

from bullet import Input, Bullet, YesNo
from yaspin import yaspin
from enum import Enum
from api_client import TavusAPIClient
from models import Replica, Persona, Video
from paginated_list import PaginatedList, SectionedPaginatedList, PaginatedListResult, PaginationAction

# State enum
class State(Enum):
  MAIN_MENU = "main_menu"
  SET_API_KEY = "set_api_key"
  WORK_WITH_REPLICAS = "work_with_replicas"
  WORK_WITH_PERSONAS = "work_with_personas"
  WORK_WITH_VIDEOS = "work_with_videos"
  CREATE_REPLICA = "create_replica"
  LIST_REPLICAS = "list_replicas"
  MODIFY_REPLICA = "modify_replica"
  DELETE_REPLICA = "delete_replica"
  CREATE_PERSONA = "create_persona"
  LIST_PERSONAS = "list_personas"
  SELECT_PERSONA_TYPE = "select_persona_type"
  DELETE_PERSONA = "delete_persona"
  CREATE_VIDEO = "create_video"
  LIST_VIDEOS = "list_videos"
  DELETE_VIDEO = "delete_video"
  RENAME_VIDEO = "rename_video"
  EXIT = "exit"

class StateMachine:
  def __init__(self):
    self.api_client = None
    self.api_key = None
    self.current_state = State.MAIN_MENU
    self.replicas = []  # List of Replica objects
    self.personas = []  # List of Persona objects
    self.videos = []  # List of Video objects
  
  def execute_current_state(self):
    """Execute the current state and update the next state"""
    if self.current_state == State.MAIN_MENU:
      self.current_state = self.execute_main_menu()
    elif self.current_state == State.SET_API_KEY:
      self.current_state = self.execute_set_api_key()
    elif self.current_state == State.WORK_WITH_REPLICAS:
      self.current_state = self.execute_work_with_replicas()
    elif self.current_state == State.WORK_WITH_PERSONAS:
      self.current_state = self.execute_work_with_personas()
    elif self.current_state == State.WORK_WITH_VIDEOS:
      self.current_state = self.execute_work_with_videos()
    elif self.current_state == State.CREATE_REPLICA:
      self.current_state = self.execute_create_replica()
    elif self.current_state == State.LIST_REPLICAS:
      self.current_state = self.execute_list_replicas()
    elif self.current_state == State.MODIFY_REPLICA:
      self.current_state = self.execute_modify_replica()
    elif self.current_state == State.DELETE_REPLICA:
      self.current_state = self.execute_delete_replica()
    elif self.current_state == State.CREATE_PERSONA:
      self.current_state = self.execute_create_persona()
    elif self.current_state == State.LIST_PERSONAS:
      self.current_state = self.execute_list_personas()
    elif self.current_state == State.SELECT_PERSONA_TYPE:
      self.current_state = self.execute_select_persona_type()
    elif self.current_state == State.DELETE_PERSONA:
      self.current_state = self.execute_delete_persona()
    elif self.current_state == State.CREATE_VIDEO:
      self.current_state = self.execute_create_video()
    elif self.current_state == State.LIST_VIDEOS:
      self.current_state = self.execute_list_videos()
    elif self.current_state == State.DELETE_VIDEO:
      self.current_state = self.execute_delete_video()
    elif self.current_state == State.RENAME_VIDEO:
      self.current_state = self.execute_rename_video()
    else:
      print(f"Unknown state: {self.current_state}")
      self.current_state = State.MAIN_MENU
  
  def execute_main_menu(self):
    """Execute main menu and return next state"""
    print("\n=== Main Menu ===")
    print(f"Tavus API key: {self.api_key}")
    
    cli = Bullet(
      prompt="What would you like to do?",
      choices=["Set API Key", "Work with Replicas", "Work with Personas", "Work with Videos", "Exit"],
      bullet="→",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    if result == "Set API Key":
      return State.SET_API_KEY
    elif result == "Work with Replicas":
      return State.WORK_WITH_REPLICAS
    elif result == "Work with Personas":
      return State.WORK_WITH_PERSONAS
    elif result == "Work with Videos":
      return State.WORK_WITH_VIDEOS
    elif result == "Exit":
      return State.EXIT
    else:
      return State.MAIN_MENU

  def execute_set_api_key(self):
    """Execute set API key and return next state"""
    print("\n=== Set API Key ===")
    print("Currently set API key: ", self.api_key)
    cli = YesNo(prompt="Would you like to set a new API key?", default="n")
    if cli.launch():
      cli = Input(prompt="Enter your new Tavus API Key: ")
      self.api_key = cli.launch()
      print(f"Tavus API key: {self.api_key}")
      
      self.api_client = TavusAPIClient(self.api_key)

    return State.MAIN_MENU

  def execute_work_with_replicas(self):
    """Execute work with replicas menu and return next state"""
    print("\n=== Work with Replicas ===")
    
    with yaspin(text="Loading replicas..."):
      self.update_replicas()

    cli = Bullet(
      prompt="What would you like to do with Replicas?",
      choices=["Create a Replica", "List Replicas", "Modify a Replica", "Delete a Replica", "Back to Main Menu"],
      bullet="🧑",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    if result == "Create a Replica":
      return State.CREATE_REPLICA
    elif result == "List Replicas":
      return State.LIST_REPLICAS
    elif result == "Modify a Replica":
      return State.MODIFY_REPLICA
    elif result == "Delete a Replica":
      return State.DELETE_REPLICA
    elif result == "Back to Main Menu":
      return State.MAIN_MENU
    else:
      return State.WORK_WITH_REPLICAS

  def execute_work_with_personas(self):
    """Execute work with personas menu and return next state"""
    print("\n=== Work with Personas ===")

    cli = Bullet(
      prompt="What would you like to do with Personas?",
      choices=["Create a Persona", "List Personas", "Delete a Persona", "Back to Main Menu"],
      bullet="🧑",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    if result == "Create a Persona":
      return State.CREATE_PERSONA
    elif result == "List Personas":
      return State.LIST_PERSONAS
    elif result == "Delete a Persona":
      return State.DELETE_PERSONA
    elif result == "Back to Main Menu":
      return State.MAIN_MENU
    else:
      return State.WORK_WITH_PERSONAS

  def execute_work_with_videos(self):
    """Execute work with videos menu and return next state"""
    print("\n=== Work with Videos ===")

    with yaspin(text="Loading videos..."):
      self.update_videos()

    cli = Bullet(
      prompt="What would you like to do with Videos?",
      choices=["Create a Video", "List Videos", "Delete a Video", "Rename a Video", "Back to Main Menu"],
      bullet="📼",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    if result == "Create a Video":
      return State.CREATE_VIDEO
    elif result == "List Videos":
      return State.LIST_VIDEOS
    elif result == "Delete a Video":
      return State.DELETE_VIDEO
    elif result == "Rename a Video":
      return State.RENAME_VIDEO
    elif result == "Back to Main Menu":
      return State.MAIN_MENU
    else:
      return State.WORK_WITH_VIDEOS

  def execute_create_replica(self):
    """Execute create replica functionality and return next state"""
    print("\n=== Create Replica ===")
    print("Create replica functionality will be implemented here...")
    # TODO: Implement create replica logic
    return State.WORK_WITH_REPLICAS

  def execute_list_replicas(self):
    """Execute list replicas functionality and return next state"""
    print("\n=== List Replicas ===")
    
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return State.MAIN_MENU

    return self.show_paginated_replicas()

  def execute_modify_replica(self):
    """Execute modify replica functionality and return next state"""
    print("\n=== Modify Replica ===")
    print("Modify replica functionality will be implemented here...")
    # TODO: Implement modify replica logic
    return State.WORK_WITH_REPLICAS

  def execute_delete_replica(self):
    """Execute delete replica functionality and return next state"""
    print("\n=== Delete Replica ===")
    print("Delete replica functionality will be implemented here...")
    # TODO: Implement delete replica logic
    return State.WORK_WITH_REPLICAS

  def execute_create_persona(self):
    """Execute create persona functionality and return next state"""
    print("\n=== Create Persona ===")
    print("Create persona functionality will be implemented here...")
    # TODO: Implement create persona logic
    return State.WORK_WITH_PERSONAS

  def execute_list_personas(self):
    """Execute list personas functionality and return next state"""
    print("\n=== List Personas ===")
    
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return State.MAIN_MENU

    return State.SELECT_PERSONA_TYPE

  def execute_delete_persona(self):
    """Execute delete persona functionality and return next state"""
    print("\n=== Delete Persona ===")
    print("Delete persona functionality will be implemented here...")
    # TODO: Implement delete persona logic
    return State.WORK_WITH_PERSONAS

  def execute_select_persona_type(self):
    """Execute select persona type functionality and return next state"""
    print("\n=== Select Persona Type ===")
    
    cli = Bullet(
      prompt="Select persona type:",
      choices=["user", "system"],
      bullet="→",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    if result == "user":
      with yaspin(text="Loading user personas..."):
        self.update_personas("user")
      return self.show_paginated_personas(filter_type="user")
    elif result == "system":
      with yaspin(text="Loading system personas..."):
        self.update_personas("system")
      return self.show_paginated_personas(filter_type="system")
    
    return State.WORK_WITH_PERSONAS

  def execute_create_video(self):
    """Execute create video functionality and return next state"""
    print("\n=== Create Video ===")
    
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return State.MAIN_MENU
    
    # Choose replica selection method
    cli = Bullet(
      prompt="How would you like to select a replica?",
      choices=["Enter Replica ID manually", "Select from replica list"],
      bullet="→",
      margin=2,
      shift=0,
    )
    selection_method = cli.launch()
    
    replica_id = None
    
    if selection_method == "Enter Replica ID manually":
      cli = Input("Replica ID: ")
      replica_id = cli.launch()
    elif selection_method == "Select from replica list":
      # Fetch and show replicas for selection
      with yaspin(text="Loading replicas..."):
        self.update_replicas()
      
      if not self.replicas:
        print("No replicas found. Please create a replica first.")
        input("Press Enter to continue...")
        return State.WORK_WITH_VIDEOS
      
      # Show paginated replica selection
      selected_replica = self._select_replica_for_video()
      if selected_replica is None:
        print("No replica selected. Returning to video creation.")
        return State.WORK_WITH_VIDEOS
      
      replica_id = selected_replica.replica_id
    
    if not replica_id or not replica_id.strip():
      print("Replica ID cannot be empty. Please try again.")
      input("Press Enter to continue...")
      return State.WORK_WITH_VIDEOS

    cli = Input("Script: ")
    script = cli.launch()
    
    if not script or not script.strip():
      print("Script cannot be empty. Please try again.")
      input("Press Enter to continue...")
      return State.WORK_WITH_VIDEOS

    cli = YesNo("Fast Render [optional]: ", default="n")
    fast = cli.launch()
    
    # Show final confirmation
    print(f"\nConfirm video creation:")
    print(f"  Replica ID: {replica_id}")
    print(f"  Script: {script[:100]}{'...' if len(script) > 100 else ''}")
    print(f"  Fast Render: {'Yes' if fast else 'No'}")
    print("=" * 50)
    
    cli = YesNo("Are you sure you want to create this video?", default="n")
    if not cli.launch():
      print("Video creation cancelled.")
      input("Press Enter to continue...")
      return State.WORK_WITH_VIDEOS
    
    video_data = {
      "replica_id": replica_id,
      "script": script,
      "fast": "true" if fast else "false"
    }

    with yaspin(text="Submitting video request..."):
      success, message, created_video = self.api_client.generate_video(video_data)

    if success and created_video:
      print(f"Request submitted successfully. Video ID: {created_video.video_id}")
    else:
      print(f"Error creating video: {message}")

    input("Press Enter to continue...")
    return State.WORK_WITH_VIDEOS

  def _select_replica_for_video(self, page=0, filter_type="all"):
    """Show paginated replica list for video creation selection"""
    # Create a custom paginated list for replica selection
    if not self.replicas:
      return None
    
    # Filter replicas based on type
    if filter_type == "user":
      filtered_replicas = [r for r in self.replicas if r.replica_type == "user"]
    elif filter_type == "system":
      filtered_replicas = [r for r in self.replicas if r.replica_type == "system"]
    else:  # "all"
      filtered_replicas = self.replicas
    
    if not filtered_replicas:
      # Show empty state with option to change filter
      print(f"\nNo {filter_type} replicas found.")
      print("=" * 50)
      
      choices = []
      choices.append(f"Current filter: {filter_type}")
      choices.append("← Go Back")
      
      cli = Bullet(
        prompt="No replicas found. What would you like to do?",
        choices=choices,
        bullet="→",
        margin=2,
        shift=0,
      )
      result = cli.launch()
      
      if result == f"Current filter: {filter_type}":
        # User wants to change filter, show filter selection
        return self._select_replica_for_video_with_filter()
      elif result == "← Go Back":
        # User wants to go back, return None
        return None
      
      # Default case - show filter selection
      return self._select_replica_for_video_with_filter()
    
    # Create paginated list with filtered replicas
    paginated_list = PaginatedList(filtered_replicas, 10)
    paginated_list.set_page(page)
    
    def on_replica_select(replica):
      # Return the selected replica for video creation
      return PaginatedListResult(PaginationAction.ITEM_SELECTED, replica)
    
    def on_filter_change(filter_type):
      # Handle filter change by returning to video creation to restart with new filter
      return PaginatedListResult(PaginationAction.FILTER_CHANGED, filter_type)
    
    result = paginated_list.show(
      title="Replicas",
      filter_type=filter_type,
      on_item_select=on_replica_select,
      on_filter_change=on_filter_change,
      show_filter_option=True
    )
    
    # Handle the result
    if result.action == PaginationAction.ITEM_SELECTED:
      return result.data
    elif result.action == PaginationAction.PREVIOUS_PAGE:
      # Stay in replica selection with previous page
      return self._select_replica_for_video(result.data, filter_type)
    elif result.action == PaginationAction.NEXT_PAGE:
      # Stay in replica selection with next page
      return self._select_replica_for_video(result.data, filter_type)
    elif result.action == PaginationAction.FILTER_CHANGED:
      # Handle filter change by showing filter selection
      return self._select_replica_for_video_with_filter()
    elif result.action == PaginationAction.GO_BACK:
      # User chose to go back, return None
      return None
    
    # Default case - stay in replica selection
    return self._select_replica_for_video(paginated_list.get_current_page(), filter_type)

  def _select_replica_for_video_with_filter(self):
    """Show replica selection with filter handling"""
    # Show filter selection
    print("\n=== Filter Replicas for Video Creation ===")
    
    cli = Bullet(
      prompt="Select filter type:",
      choices=["user only", "system only", "all replicas"],
      bullet="→",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    # Map filter selection to filter type
    if result == "user only":
      filter_type = "user"
    elif result == "system only":
      filter_type = "system"
    else:  # "all replicas"
      filter_type = "all"
    
    # Start replica selection with the selected filter
    return self._select_replica_for_video(page=0, filter_type=filter_type)

  def execute_list_videos(self):
    """Execute list videos functionality and return next state"""
    print("\n=== List Videos ===")
    
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return State.MAIN_MENU

    return self.show_paginated_videos()

  def execute_delete_video(self):
    """Execute delete video functionality and return next state"""
    print("\n=== Delete Video ===")
    
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return State.MAIN_MENU

    return self.show_paginated_videos(on_video_select=self._handle_video_delete)

  def _handle_video_delete(self, video):
    """Handle video delete when a video is selected from the list"""
    print(f"\nDeleting video: {video.video_name} ({video.video_id})")
    print("=" * 50)
    
    # Show full video details first
    self.show_video_details(video)
    print("=" * 50)

    cli = YesNo("Are you sure you want to delete this video?", default="n")
    if cli.launch():
      with yaspin(text="Deleting video..."):
        if self.api_client:
          success, message = self.api_client.delete_video(video.video_id)
        else:
          success, message = False, "API client not initialized"

      if success:
        print(f"Video deleted successfully")
      else:
        print(f"Error deleting video: {message}")

    return State.WORK_WITH_VIDEOS

  def execute_rename_video(self):
    """Execute rename video functionality and return next state"""
    print("\n=== Rename Video ===")
    
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return State.MAIN_MENU

    return self.show_paginated_videos(on_video_select=self._handle_video_rename)

  def _handle_video_rename(self, video):
    """Handle video rename when a video is selected from the list"""
    print(f"\nRenaming video: {video.video_name} ({video.video_id})")
    print("=" * 50)
    
    # Show full video details first
    self.show_video_details(video)
    print("=" * 50)
    
    if self.api_client is None:
      print("Error: API client not initialized.")
      input("Press Enter to continue...")
      return State.WORK_WITH_VIDEOS
    
    cli = Input("Enter new video name: ")
    new_name = cli.launch()
    
    if not new_name.strip():
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
      success, message = self.api_client.rename_video(video.video_id, new_name)
    
    if success:
      print(f"Video renamed successfully to: {new_name}")
      # Update the video object in our list
      video.video_name = new_name
    else:
      print(f"Error renaming video: {message}")
    
    input("Press Enter to continue...")
    return State.WORK_WITH_VIDEOS

  def update_replicas(self):
    """Update the replicas list from API"""
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return

    success, message, fetched_replicas = self.api_client.list_replicas()
    if success:
      # Convert dictionary data to Replica objects
      self.replicas = fetched_replicas
    else:
      print(message)

  def update_personas(self, persona_type: str = "system"):
    """Update the personas list from API"""
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return

    success, message, fetched_personas = self.api_client.list_personas(persona_type)
    if success:
      # Convert dictionary data to Persona objects
      self.personas = fetched_personas
    else:
      print(message)

  def update_videos(self):
    """Update the videos list from API"""
    if self.api_client is None:
      print("Error: API client not initialized. Please set your API key first.")
      return

    success, message, fetched_videos = self.api_client.list_videos()
    if success:
      # Convert dictionary data to Video objects
      self.videos = fetched_videos
    else:
      print(message)

  def set_api_client(self, api_client):
    """Set the API client instance"""
    self.api_client = api_client

  def set_api_key(self, api_key):
    """Set the API key"""
    self.api_key = api_key

  def is_exit_state(self):
    """Check if current state is exit"""
    return self.current_state == State.EXIT 

  def show_paginated_replicas(self, page=0, items_per_page=10, filter_type="all"):
    """Show paginated list of replicas with selection"""
    if not self.replicas:
      print("No replicas found.")
      input("Press Enter to continue...")
      return State.WORK_WITH_REPLICAS

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
        on_filter_change=self._handle_replica_filter_change
      )
      return self._handle_replica_pagination_result(result, items_per_page, filter_type)

    # Create sectioned paginated list
    paginated_list = SectionedPaginatedList(filtered_replicas, items_per_page)
    paginated_list.set_sections(sectioned_replicas, section_names)
    paginated_list.set_page(page)

    def on_replica_select(replica):
      self.show_replica_details(replica)
      input("Press Enter to continue...")
      # Return the current page so we stay on the same page
      return PaginatedListResult(PaginationAction.NO_ACTION, paginated_list.get_current_page())

    result = paginated_list.show(
      title="Replicas",
      filter_type=filter_type,
      on_item_select=on_replica_select,
      on_filter_change=self._handle_replica_filter_change
    )

    return self._handle_replica_pagination_result(result, items_per_page, filter_type)

  def _handle_replica_filter_change(self, filter_type):
    """Handle replica filter change"""
    return PaginatedListResult(PaginationAction.FILTER_CHANGED, filter_type)

  def _handle_replica_pagination_result(self, result, items_per_page, filter_type):
    """Handle pagination result for replicas"""
    if result.action == PaginationAction.PREVIOUS_PAGE:
      return self.show_paginated_replicas(result.data, items_per_page, filter_type)
    elif result.action == PaginationAction.NEXT_PAGE:
      return self.show_paginated_replicas(result.data, items_per_page, filter_type)
    elif result.action == PaginationAction.GO_BACK:
      return State.WORK_WITH_REPLICAS
    elif result.action == PaginationAction.FILTER_CHANGED:
      return self.show_replica_filter_selection()
    else:
      # Use the page from result.data if available, otherwise default to 0
      current_page = result.data if result.data is not None else 0
      return self.show_paginated_replicas(current_page, items_per_page, filter_type)

  def show_replica_filter_selection(self):
    """Show filter selection for replicas"""
    print("\n=== Filter Replicas ===")
    
    cli = Bullet(
      prompt="Select filter type:",
      choices=["user only", "system only", "all replicas"],
      bullet="→",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    if result == "user only":
      return self.show_paginated_replicas(filter_type="user")
    elif result == "system only":
      return self.show_paginated_replicas(filter_type="system")
    elif result == "all replicas":
      return self.show_paginated_replicas(filter_type="all")
    
    return self.show_paginated_replicas()

  def show_paginated_personas(self, page=0, items_per_page=10, filter_type="system"):
    """Show paginated list of personas with selection"""
    if not self.personas:
      # Create empty paginated list for proper empty state handling
      paginated_list = PaginatedList([])
      result = paginated_list.show(
        title="Personas",
        filter_type=filter_type,
        on_filter_change=self._handle_persona_filter_change
      )
      return self._handle_persona_pagination_result(result, items_per_page, filter_type)

    # Create paginated list
    paginated_list = PaginatedList(self.personas, items_per_page)
    paginated_list.set_page(page)

    def on_persona_select(persona):
      self.show_persona_details(persona)
      input("Press Enter to continue...")
      # Return the current page so we stay on the same page
      return PaginatedListResult(PaginationAction.NO_ACTION, paginated_list.get_current_page())

    result = paginated_list.show(
      title="Personas",
      filter_type=filter_type,
      on_item_select=on_persona_select,
      on_filter_change=self._handle_persona_filter_change
    )

    return self._handle_persona_pagination_result(result, items_per_page, filter_type)

  def _handle_persona_filter_change(self, filter_type):
    """Handle persona filter change"""
    return PaginatedListResult(PaginationAction.FILTER_CHANGED, filter_type)

  def _handle_persona_pagination_result(self, result, items_per_page, filter_type):
    """Handle pagination result for personas"""
    if result.action == PaginationAction.PREVIOUS_PAGE:
      return self.show_paginated_personas(result.data, items_per_page, filter_type)
    elif result.action == PaginationAction.NEXT_PAGE:
      return self.show_paginated_personas(result.data, items_per_page, filter_type)
    elif result.action == PaginationAction.GO_BACK:
      return State.WORK_WITH_PERSONAS
    elif result.action == PaginationAction.FILTER_CHANGED:
      return State.SELECT_PERSONA_TYPE
    else:
      # Use the page from result.data if available, otherwise default to 0
      current_page = result.data if result.data is not None else 0
      return self.show_paginated_personas(current_page, items_per_page, filter_type)

  def show_replica_details(self, replica):
    """Show detailed information for a specific replica"""
    print("\n" + "=" * 60)
    print("REPLICA DETAILS")
    print("=" * 60)
    print(replica.display_verbose())
    print("=" * 60)

  def show_persona_details(self, persona):
    """Show detailed information for a specific persona"""
    print("\n" + "=" * 60)
    print("PERSONA DETAILS")
    print("=" * 60)
    print(persona.display_verbose())
    print("=" * 60)

  def show_video_details(self, video):
    """Show detailed information for a specific video"""
    print("\n" + "=" * 60)
    print("VIDEO DETAILS")
    print("=" * 60)
    print(video.display_verbose())
    print("=" * 60)

  def show_paginated_videos(self, page=0, items_per_page=10, on_video_select=None):
    """Show paginated list of videos with selection
    
    Args:
      page: Current page number (0-based)
      items_per_page: Number of items per page
      on_video_select: Optional callback function to call when a video is selected.
                      Should accept a Video object and return a State or None.
                      If None, shows video details and returns to list.
    """
    if not self.videos:
      print("No videos found.")
      input("Press Enter to continue...")
      return State.WORK_WITH_VIDEOS

    # Create paginated list
    paginated_list = PaginatedList(self.videos, items_per_page)
    paginated_list.set_page(page)

    def on_video_select_wrapper(video):
      if on_video_select:
        # Call the custom callback function
        result_state = on_video_select(video)
        if result_state:
          return PaginatedListResult(PaginationAction.ITEM_SELECTED, result_state)
        # If callback returns None, continue showing the list
        return PaginatedListResult(PaginationAction.NO_ACTION, paginated_list.get_current_page())
      else:
        # Default behavior: show video details
        self.show_video_details(video)
        input("Press Enter to continue...")
        # Return the current page so we stay on the same page
        return PaginatedListResult(PaginationAction.NO_ACTION, paginated_list.get_current_page())

    result = paginated_list.show(
      title="Videos",
      on_item_select=on_video_select_wrapper,
      show_filter_option=False
    )

    return self._handle_video_pagination_result(result, items_per_page, on_video_select)

  def _handle_video_pagination_result(self, result, items_per_page, on_video_select):
    """Handle pagination result for videos"""
    if result.action == PaginationAction.PREVIOUS_PAGE:
      return self.show_paginated_videos(result.data, items_per_page, on_video_select)
    elif result.action == PaginationAction.NEXT_PAGE:
      return self.show_paginated_videos(result.data, items_per_page, on_video_select)
    elif result.action == PaginationAction.GO_BACK:
      return State.WORK_WITH_VIDEOS
    elif result.action == PaginationAction.ITEM_SELECTED:
      # Return the state from the custom callback
      return result.data
    else:
      # Use the page from result.data if available, otherwise default to 0
      current_page = result.data if result.data is not None else 0
      return self.show_paginated_videos(current_page, items_per_page, on_video_select)