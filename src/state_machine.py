#!/usr/bin/env python3

from bullet import Input, Bullet, YesNo
from yaspin import yaspin
from enum import Enum
from api_client import TavusAPIClient
from models import Replica, Persona, Video

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
    
    cli = Input("Replica ID: ")
    replica_id = cli.launch()

    cli = Input("Script: ")
    script = cli.launch()

    cli = YesNo("Fast Render [optional]: ", default="n")
    fast = cli.launch()
    
    video_data = {
      "replica_id": replica_id,
      "script": script,
      "fast": "true" if fast else "false"
    }

    with yaspin(text="Submitting video request..."):
      success, message, created_video = self.api_client.generate_video(video_data)

    if success and created_video:
      print(f"Request submitted successfully. Video ID: {created_video['video_id']}")
    else:
      print(f"Error creating video: {message}")

    return State.WORK_WITH_VIDEOS

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
    print("Delete video functionality will be implemented here...")
    # TODO: Implement delete video logic
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
      self.replicas = [Replica.from_dict(replica_data) for replica_data in fetched_replicas]
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
      self.personas = [Persona.from_dict(persona_data) for persona_data in fetched_personas]
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
      self.videos = [Video.from_dict(video_data) for video_data in fetched_videos]
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
      print(f"\nNo replicas found.")
      print("=" * 50)
      
      # Build choices list with just go back option
      choices = []
      choices.append(f"Current filter: {filter_type}")
      choices.append("← Go Back")
      
      # Show menu
      cli = Bullet(
        prompt="No replicas found. What would you like to do?",
        choices=choices,
        bullet="→",
        margin=2,
        shift=0,
      )
      result = cli.launch()
      
      # Handle filter selection
      if result == f"Current filter: {filter_type}":
        return self.show_replica_filter_selection()
      elif result == "← Go Back":
        return State.WORK_WITH_REPLICAS
      
      return self.show_paginated_replicas(page, items_per_page, filter_type)

    total_pages = (len(filtered_replicas) - 1) // items_per_page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(filtered_replicas))
    current_replicas = filtered_replicas[start_idx:end_idx]

    print(f"\nPage {page + 1} of {total_pages + 1} ({len(filtered_replicas)} {filter_type} replicas)")
    print("=" * 50)

    # Build choices list
    choices = []
    
    # Add filter options at the top
    choices.append(f"Current filter: {filter_type}")
    
    # Add navigation options
    if page > 0:
      choices.append("← Previous Page")
    
    # Add replica items with section headers for "all" view
    if filter_type == "all":
      # Get all replicas in order: user first, then system
      user_replicas = [r for r in self.replicas if r.replica_type == "user"]
      system_replicas = [r for r in self.replicas if r.replica_type == "system"]
      all_replicas = user_replicas + system_replicas
      
      # Get the replicas for current page
      page_replicas = all_replicas[start_idx:end_idx]
      
      # Track which section we're in
      user_count = len(user_replicas)
      current_user_idx = 0
      current_system_idx = 0
      
      for i, replica in enumerate(page_replicas):
        global_idx = start_idx + i + 1
        
        # Check if we need to add section headers
        if replica.replica_type == "user":
          if current_user_idx == 0:
            choices.append("--- User Replicas ---")
          current_user_idx += 1
        else:  # system replica
          if current_system_idx == 0:
            choices.append("--- System Replicas ---")
          current_system_idx += 1
        
        choices.append(f"{global_idx}. {replica.display_short()}")
    else:
      # Single section view (user or system only)
      for i, replica in enumerate(current_replicas, start_idx + 1):
        choices.append(f"{i}. {replica.display_short()}")
    
    # Add navigation options
    if page < total_pages:
      choices.append("→ Next Page")
    
    choices.append("← Go Back")

    # Show menu
    cli = Bullet(
      prompt="Select a replica to view details or navigate:",
      choices=choices,
      bullet="→",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    # Handle filter selection
    if result == f"Current filter: {filter_type}":
      return self.show_replica_filter_selection()
    
    # Handle navigation
    if result == "← Previous Page":
      return self.show_paginated_replicas(page - 1, items_per_page, filter_type)
    elif result == "→ Next Page":
      return self.show_paginated_replicas(page + 1, items_per_page, filter_type)
    elif result == "← Go Back":
      return State.WORK_WITH_REPLICAS
    
    # Handle replica selection
    if result.startswith("→") or result.startswith("---"):
      return self.show_paginated_replicas(page, items_per_page, filter_type)
    
    # Extract replica index from selection
    try:
      replica_idx = int(result.split('.')[0]) - 1
      if 0 <= replica_idx < len(filtered_replicas):
        self.show_replica_details(filtered_replicas[replica_idx])
        input("Press Enter to continue...")
        return self.show_paginated_replicas(page, items_per_page, filter_type)
    except (ValueError, IndexError):
      pass
    
    return self.show_paginated_replicas(page, items_per_page, filter_type)

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
      print(f"\nNo {filter_type} personas found.")
      print("=" * 50)
      
      # Build choices list with options to change filter or go back
      choices = []
      choices.append(f"Current filter: {filter_type}")
      choices.append("← Go Back")
      
      # Show menu
      cli = Bullet(
        prompt="No personas found. What would you like to do?",
        choices=choices,
        bullet="→",
        margin=2,
        shift=0,
      )
      result = cli.launch()
      
      # Handle filter selection
      if result == f"Current filter: {filter_type}":
        return State.SELECT_PERSONA_TYPE
      elif result == "← Go Back":
        return State.WORK_WITH_PERSONAS
      
      return self.show_paginated_personas(page, items_per_page, filter_type)

    # Filter personas based on type (if we had persona_type field, we would filter here)
    # For now, we'll show all personas since the API call already filtered them
    filtered_personas = self.personas

    if not filtered_personas:
      print(f"\nNo personas found.")
      print("=" * 50)
      
      # Build choices list with options to change filter or go back
      choices = []
      choices.append(f"Current filter: {filter_type}")
      choices.append("← Go Back")
      
      # Show menu
      cli = Bullet(
        prompt="No personas found. What would you like to do?",
        choices=choices,
        bullet="→",
        margin=2,
        shift=0,
      )
      result = cli.launch()
      
      # Handle filter selection
      if result == f"Current filter: {filter_type}":
        return State.SELECT_PERSONA_TYPE
      elif result == "← Go Back":
        return State.WORK_WITH_PERSONAS
      
      return self.show_paginated_personas(page, items_per_page, filter_type)

    total_pages = (len(filtered_personas) - 1) // items_per_page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(filtered_personas))
    current_personas = filtered_personas[start_idx:end_idx]

    print(f"\nPage {page + 1} of {total_pages + 1} ({len(filtered_personas)} {filter_type} personas)")
    print("=" * 50)

    # Build choices list
    choices = []
    
    # Add filter options at the top
    choices.append(f"Current filter: {filter_type}")
    
    # Add navigation options
    if page > 0:
      choices.append("← Previous Page")
    
    # Add persona items
    for i, persona in enumerate(current_personas, start_idx + 1):
      choices.append(f"{i}. {persona.display_short()}")
    
    # Add navigation options
    if page < total_pages:
      choices.append("→ Next Page")
    
    choices.append("← Go Back")

    # Show menu
    cli = Bullet(
      prompt="Select a persona to view details or navigate:",
      choices=choices,
      bullet="→",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    # Handle filter selection
    if result == f"Current filter: {filter_type}":
      return State.SELECT_PERSONA_TYPE
    
    # Handle navigation
    if result == "← Previous Page":
      return self.show_paginated_personas(page - 1, items_per_page, filter_type)
    elif result == "→ Next Page":
      return self.show_paginated_personas(page + 1, items_per_page, filter_type)
    elif result == "← Go Back":
      return State.WORK_WITH_PERSONAS
    
    # Handle persona selection
    if result.startswith("→"):
      return self.show_paginated_personas(page, items_per_page, filter_type)
    
    # Extract persona index from selection
    try:
      persona_idx = int(result.split('.')[0]) - 1
      if 0 <= persona_idx < len(filtered_personas):
        self.show_persona_details(filtered_personas[persona_idx])
        input("Press Enter to continue...")
        return self.show_paginated_personas(page, items_per_page, filter_type)
    except (ValueError, IndexError):
      pass
    
    return self.show_paginated_personas(page, items_per_page, filter_type)

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

    total_pages = (len(self.videos) - 1) // items_per_page
    start_idx = page * items_per_page
    end_idx = min(start_idx + items_per_page, len(self.videos))
    current_videos = self.videos[start_idx:end_idx]

    print(f"\nPage {page + 1} of {total_pages + 1} ({len(self.videos)} videos)")
    print("=" * 50)

    # Build choices list
    choices = []
    
    # Add navigation options
    if page > 0:
      choices.append("← Previous Page")
    
    # Add video items
    for i, video in enumerate(current_videos, start_idx + 1):
      choices.append(f"{i}. {video.display_short()}")
    
    # Add navigation options
    if page < total_pages:
      choices.append("→ Next Page")
    
    choices.append("← Go Back")

    # Show menu
    cli = Bullet(
      prompt="Select a video to view details or navigate:",
      choices=choices,
      bullet="→",
      margin=2,
      shift=0,
    )
    result = cli.launch()

    # Handle navigation
    if result == "← Previous Page":
      return self.show_paginated_videos(page - 1, items_per_page, on_video_select)
    elif result == "→ Next Page":
      return self.show_paginated_videos(page + 1, items_per_page, on_video_select)
    elif result == "← Go Back":
      return State.WORK_WITH_VIDEOS
    
    # Handle video selection
    if result.startswith("→"):
      return self.show_paginated_videos(page, items_per_page, on_video_select)
    
    # Extract video index from selection
    try:
      video_idx = int(result.split('.')[0]) - 1
      if 0 <= video_idx < len(self.videos):
        selected_video = self.videos[video_idx]
        
        if on_video_select:
          # Call the custom callback function
          result_state = on_video_select(selected_video)
          if result_state:
            return result_state
          # If callback returns None, continue showing the list
          return self.show_paginated_videos(page, items_per_page, on_video_select)
        else:
          # Default behavior: show video details
          self.show_video_details(selected_video)
          input("Press Enter to continue...")
          return self.show_paginated_videos(page, items_per_page, on_video_select)
    except (ValueError, IndexError):
      pass
    
    return self.show_paginated_videos(page, items_per_page, on_video_select)