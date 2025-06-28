# Modular Architecture for Tavus Python Client

## Overview

This document describes the modular architecture for the Tavus Python client, which replaces the monolithic `state_machine.py` with a plugin-based system that allows for easy extension and maintenance.

## Architecture Components

### 1. Core State Machine (`state_machine_modular.py`)
- **Purpose**: Central orchestrator that manages state transitions and module coordination
- **Responsibilities**:
  - Maintains current state
  - Routes state execution to appropriate modules
  - Provides common state constants via `CommonStates`
  - Manages module registration and discovery
  - Uses module-defined choice-to-state mappings (no hardcoding)
  - Provides API client access to modules

### 2. Module Interface (`modules/__init__.py`)
- **Purpose**: Defines the contract that all modules must implement
- **Key Components**:
  - `ModuleInterface`: Abstract base class for all modules
  - `CommonStates`: Constants for common states to avoid hardcoding
  - `ModuleRegistry`: Manages module registration and state routing

### 3. Individual Modules
Each module is self-contained and implements the `ModuleInterface`:

#### API Key Module (`modules/api_key_module.py`)
- **States**: `set_api_key`
- **Functionality**: API key management and validation
- **Menu Option**: "Set API Key" → `set_api_key`

#### Replica Module (`modules/replica_module.py`)
- **States**: `work_with_replicas`, `create_replica`, `list_replicas`, `rename_replica`, `delete_replica`
- **Functionality**: Complete replica lifecycle management
  - Create replicas with name, description, and video file
  - List replicas with pagination and filtering (user/system/all)
  - Rename existing replicas
  - Delete user replicas (system replicas cannot be deleted)
  - Sectioned display for "all" filter (User Replicas / System Replicas)
- **Menu Option**: "Work with Replicas" → `work_with_replicas`

#### Persona Module (`modules/persona_module.py`)
- **States**: `work_with_personas`, `create_persona`, `list_personas`, `delete_persona`
- **Functionality**: Complete persona lifecycle management
  - Create personas with name, system prompt, context, and optional default replica
  - List personas with pagination and filtering (user/system)
  - Delete user personas (system personas cannot be deleted)
  - Default to user personas for listing
  - Replica selection during creation with sectioned display
- **Menu Option**: "Work with Personas" → `work_with_personas`

#### Video Module (`modules/video_module.py`)
- **States**: `work_with_videos`, `generate_video`, `list_videos`, `rename_video`, `delete_video`
- **Functionality**: Complete video lifecycle management
  - Generate videos with name, replica selection, and script
  - List videos with pagination (no filtering - only user videos shown)
  - Rename existing videos
  - Delete videos
  - Replica selection during creation with sectioned display
- **Menu Option**: "Work with Videos" → `work_with_videos`

## Key Design Principles

### 1. String-Based States
- **Approach**: All states are represented as strings
- **Benefits**:
  - Simple and readable
  - Easy to debug and log
  - No enum import complexity
  - Flexible for dynamic state creation
- **Trade-offs**:
  - No compile-time validation
  - Potential for typos
- **Mitigation**: Use `CommonStates` constants to avoid hardcoding

### 2. Common States Constants
- **Purpose**: Eliminate hardcoded string literals in modules
- **Implementation**: `CommonStates` class provides constants like `MAIN_MENU` and `EXIT`
- **Benefits**:
  - Modules don't need to know about state machine internals
  - Centralized state name management
  - Easy refactoring if state names change

### 3. Module-Defined Choice-to-State Mapping
- **Purpose**: Eliminate hardcoded mappings in the state machine
- **Implementation**: Each module defines its own `get_choice_to_state_mapping()` method
- **Benefits**:
  - State machine doesn't need to know about module internals
  - Modules control their own menu-to-state relationships
  - Easy to add new modules without modifying state machine
  - Complete encapsulation of module behavior

### 4. Module Autonomy
- **Principle**: Each module defines its own states and handles its own logic
- **Benefits**:
  - Clear separation of concerns
  - Independent development and testing
  - Easy to add/remove functionality

### 5. State Machine Coordination
- **Principle**: State machine routes states to appropriate modules
- **Implementation**: Registry pattern for state-to-module mapping
- **Benefits**:
  - Centralized state management
  - Easy to add new modules
  - Clear state ownership

### 6. Local Data Management
- **Principle**: Each module manages its own data lists independently
- **Implementation**: Modules maintain local storage for their entities (replicas, personas, videos)
- **Benefits**:
  - No centralized data dependencies
  - Modules can cache data for performance
  - Independent data refresh cycles
  - Better encapsulation

### 7. Update Method Pattern
- **Principle**: Modules call state machine update methods instead of directly manipulating data
- **Implementation**: State machine provides `update_*()` and `remove_*()` methods
- **Benefits**:
  - Centralized data management
  - Consistent update patterns
  - Better error handling
  - Easier debugging

## Module Interface Contract

```python
class ModuleInterface(ABC):
    def get_name(self) -> str:
        """Return the module name"""
    
    def get_states(self) -> List[str]:
        """Return list of state names this module handles"""
    
    def get_menu_options(self) -> List[str]:
        """Return menu options this module provides"""
    
    def get_choice_to_state_mapping(self) -> Dict[str, str]:
        """Return mapping from menu choices to states"""
    
    def execute_state(self, state: str, state_machine) -> str:
        """Execute a specific state and return the next state"""
```

## State Flow

1. **Main Menu**: State machine shows menu options from all registered modules
2. **Choice Selection**: User selects an option, state machine looks up state using module-defined mapping
3. **State Execution**: Module executes the state and returns the next state
4. **State Transition**: State machine updates current state and continues the loop

## Pagination and Filtering System

### PaginatedList Component
- **Purpose**: Provides consistent pagination across all modules
- **Features**:
  - Configurable items per page
  - Navigation controls (next/previous page)
  - Filter option support
  - Custom item selection callbacks
  - Empty state handling

### SectionedPaginatedList Component
- **Purpose**: Enhanced pagination with sectioned display
- **Features**:
  - Sections with headers (e.g., "User Replicas", "System Replicas")
  - Automatic section detection and display
  - Consistent with regular pagination interface
  - Used for "all" filter views

### Filter System
- **Implementation**: Consistent filtering across modules
- **Replica Filters**: "user", "system", "all" (with sections)
- **Persona Filters**: "user", "system" (API-level filtering)
- **Video Filters**: No filtering (user videos only)

## Benefits of This Architecture

### 1. **Modularity**
- Each feature is self-contained in its own module
- Easy to add new features without modifying existing code
- Clear separation of concerns

### 2. **Maintainability**
- Smaller, focused files are easier to understand and modify
- Changes to one module don't affect others
- Clear interfaces between components

### 3. **Extensibility**
- New modules can be added without changing core state machine
- Modules can be developed independently
- Easy to implement feature flags or conditional loading

### 4. **Testability**
- Each module can be tested in isolation
- Mock state machine for unit testing
- Clear interfaces make testing straightforward

### 5. **No Hardcoded Dependencies**
- Modules use `CommonStates` constants instead of string literals
- State machine uses module-defined choice-to-state mappings
- Complete decoupling between modules and state machine

### 6. **User Experience**
- Consistent pagination and filtering across all modules
- Sectioned displays for better organization
- Intuitive navigation and selection patterns
- Proper error handling and user feedback

## Migration Status

### Phase 1: Core Infrastructure ✅
- [x] Create module interface and registry
- [x] Implement core state machine
- [x] Create API key module
- [x] Create replica module
- [x] Implement choice-to-state mapping system
- [x] Remove centralized state definitions
- [x] Implement string-only states
- [x] Add CommonStates constants

### Phase 2: Feature Migration ✅
- [x] Extract persona management into module
- [x] Extract video management into module
- [x] Remove old state machine (`state_machine.py` deleted)
- [x] Implement local data management in modules
- [x] Add update method pattern
- [x] Implement pagination and filtering system
- [x] Add sectioned display for replica selection

### Phase 3: Enhancement ✅
- [x] Add comprehensive pagination system
- [x] Implement filtering with API integration
- [x] Add sectioned displays for better UX
- [x] Implement replica selection in persona creation
- [x] Add video rename functionality
- [x] Optimize persona listing (no reload on page change)
- [x] Fix filter labels and API integration
- [x] Remove redundant print statements

## Current Features

### API Key Management
- Set and validate API keys
- Persistent storage
- Error handling for invalid keys

### Replica Management
- **Create**: Upload video files with name and description
- **List**: Paginated view with user/system/all filters
- **Rename**: Update replica names
- **Delete**: Remove user replicas (system replicas protected)
- **Sections**: User/System sections when viewing all replicas

### Persona Management
- **Create**: Define personas with system prompts and optional default replicas
- **List**: Paginated view with user/system filters (defaults to user)
- **Delete**: Remove user personas (system personas protected)
- **Replica Selection**: Choose default replica during creation with sectioned display

### Video Management
- **Generate**: Create videos with replica selection and scripts
- **List**: Paginated view of user videos
- **Rename**: Update video names
- **Delete**: Remove videos
- **Replica Selection**: Choose replica during creation with sectioned display

## Usage Example

```python
# Create state machine
state_machine = ModularStateMachine()

# Register modules (done automatically in main.py)
state_machine.register_module(ApiKeyModule())
state_machine.register_module(ReplicaModule())
state_machine.register_module(PersonaModule())
state_machine.register_module(VideoModule())

# Run the state machine
while not state_machine.is_exit_state():
    state_machine.execute_current_state()
```

## Best Practices

### 1. **State Naming**
- Use descriptive, lowercase names with underscores
- Prefix module-specific states with module name if needed
- Use `CommonStates` constants for common states

### 2. **Module Design**
- Keep modules focused on a single responsibility
- Return `CommonStates.MAIN_MENU` or `CommonStates.EXIT` for navigation
- Handle errors gracefully and return to appropriate state
- Define clear choice-to-state mappings in `get_choice_to_state_mapping()`
- Manage local data storage for performance
- Use update methods for data manipulation

### 3. **State Machine Integration**
- Use the registry for state routing
- Provide clear interfaces for module communication
- Handle unknown states gracefully
- Never hardcode choice-to-state mappings in the state machine

### 4. **Error Handling**
- Modules should handle their own errors
- Return to safe states on errors
- Provide clear error messages to users
- Use try-catch blocks for API calls

### 5. **User Experience**
- Provide consistent pagination and filtering
- Use sectioned displays for better organization
- Give clear feedback for all operations
- Handle empty states gracefully

### 6. **Performance**
- Cache data locally in modules
- Fetch data only when needed
- Use pagination to handle large datasets
- Optimize API calls with proper filtering

This architecture provides a solid foundation for a maintainable and extensible Tavus Python client while eliminating all hardcoded dependencies between modules and the state machine. The modular design allows for easy feature additions and modifications while maintaining a consistent user experience across all functionality. 