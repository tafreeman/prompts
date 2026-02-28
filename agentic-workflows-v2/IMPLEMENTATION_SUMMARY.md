# Implementation Summary: Node Configuration Overlay

## Overview
This implementation adds a complete feature for editing model selection, agent instructions, and generation parameters via a frontend overlay during workflow execution.

## Changes Made

### 1. Backend: Data Models
**File**: `agentic_v2/contracts/schemas.py`
- Added `NodeConfigOverride` Pydantic model
  - Fields: model, system_prompt, temperature, max_tokens, top_p, tool_names
  - Method: `is_empty()` to detect if config has values
- Added `NodeConfigUpdateRequest` for WebSocket messages
- Exported from `contracts/__init__.py`

### 2. Backend: State Management
**File**: `agentic_v2/langchain/state.py`
- Added `node_config_overrides` field to `WorkflowState` TypedDict
- Field type: `Annotated[dict[str, dict[str, Any]], _merge_dicts]`
- Initialized in `initial_state()` as empty dict

### 3. Backend: WebSocket Communication
**File**: `agentic_v2/server/websocket.py`
- Added `node_config_overrides` dict to `ConnectionManager`
- Added methods:
  - `set_node_config(run_id, step_name, config)`: Store override
  - `get_node_config(run_id, step_name)`: Retrieve override
  - `clear_node_configs(run_id)`: Cleanup on run completion
- Enhanced WebSocket endpoint to handle `node_config_update` messages
- Sends `node_config_ack` confirmation to client

### 4. Backend: Agent Creation
**File**: `agentic_v2/langchain/agents.py`
- Modified `create_agent()` signature to accept `node_config` parameter
- Node config overrides take precedence:
  - `system_prompt`: Full replacement if provided
  - `model`: Override model selection
  - `temperature`, `max_tokens`, `top_p`: Applied to model instance
  - `tool_names`: Override tool list
- Fallback to original behavior when config is None/empty

### 5. Backend: Graph Execution
**File**: `agentic_v2/langchain/graph.py`
- Added `_is_empty_config()` helper function
- Modified `_get_agent_for_model()` to accept node_config parameter
- Cache key includes config tuple for proper isolation
- Updated `_llm_node()` to:
  - Extract `node_config_overrides` from state
  - Pass config to agent creation
  - Track override usage in metadata
  - Flag `config_overridden=True` when used

### 6. Frontend: Config Overlay Component
**File**: `ui/src/components/live/NodeConfigOverlay.tsx`
- Right-side sliding panel modal component
- Features:
  - Model selection dropdown (default + available models)
  - System prompt textarea with copy button
  - Generation parameters: temperature, max_tokens, top_p
  - Tool selection with checkboxes
  - Reset, Cancel, Save & Apply buttons
  - Info box explaining behavior
- State management with local config tracking
- Animated panel transitions

### 7. Frontend: WebSocket Hook
**File**: `ui/src/hooks/useNodeConfigUpdate.ts`
- `useNodeConfigUpdate()` hook
- Manages WebSocket lifecycle:
  - Connect/disconnect on runId change
  - Auto-reconnect every 3 seconds on disconnect
  - Tracks connection state
- `updateNodeConfig()` method sends properly formatted messages
- Error handling for network issues

### 8. Frontend: StepNode Integration
**File**: `ui/src/components/dag/StepNode.tsx`
- Added Settings icon button on configurable nodes
- Integrated `NodeConfigOverlay` modal
- Props extended:
  - `runId`: For WebSocket communication
  - `onConfigUpdate`: Callback for parent
- Local state management for overlay visibility
- Config update callback to parent

### 9. Frontend: DAG Component
**File**: `ui/src/components/dag/WorkflowDAG.tsx`
- Props updated:
  - `runId`: Passed to nodes
  - `onConfigUpdate`: Config update handler
- Node data now includes:
  - `runId`
  - `onConfigUpdate` callback
- Dependency array updated to include new props

### 10. Frontend: LivePage Integration
**File**: `ui/src/pages/LivePage.tsx`
- Imports: Added `useCallback`, `useNodeConfigUpdate`
- Hook initialization: `useNodeConfigUpdate({ runId })`
- Handler: `handleConfigUpdate()` sends updates to WebSocket
- WorkflowDAG props:
  - `runId={runId}`
  - `onConfigUpdate={handleConfigUpdate}`

## Data Flow Diagram

```
Frontend UI
    │
    ├─ User clicks ⚙️ icon on running step
    │
    ├─ NodeConfigOverlay opens
    │
    ├─ User modifies: model, prompt, temperature, etc.
    │
    ├─ User clicks "Save & Apply"
    │
    └─→ useNodeConfigUpdate().updateNodeConfig()
           │
           └─→ Send JSON via WebSocket:
               {
                 type: "node_config_update",
                 step_name: "...",
                 config: {...}
               }
                 │
                 Backend WebSocket Handler
                 │
                 └─→ ConnectionManager.set_node_config()
                      │
                      └─→ Update state.node_config_overrides
                           │
                           └─→ Send acknowledgment to frontend
                                │
                                Next step execution:
                                │
                                └─→ _llm_node() fetches overrides
                                     │
                                     └─→ Pass to create_agent()
                                          │
                                          └─→ Agent uses custom model/prompt
                                               │
                                               └─→ Metadata tracked
                                                    config_overridden: true
```

## Files Modified/Created

### Modified Files:
1. `agentic_v2/contracts/schemas.py` - Added node config models
2. `agentic_v2/contracts/__init__.py` - Export new models
3. `agentic_v2/langchain/state.py` - Added config overrides field
4. `agentic_v2/server/websocket.py` - Enhanced for config updates
5. `agentic_v2/langchain/agents.py` - Accept node config parameter
6. `agentic_v2/langchain/graph.py` - Use node config in execution
7. `ui/src/components/dag/StepNode.tsx` - Add config overlay integration
8. `ui/src/components/dag/WorkflowDAG.tsx` - Pass config props to nodes
9. `ui/src/pages/LivePage.tsx` - Initialize hook and pass props

### Created Files:
1. `ui/src/components/live/NodeConfigOverlay.tsx` - Overlay component
2. `ui/src/hooks/useNodeConfigUpdate.ts` - WebSocket hook
3. `docs/NODE_CONFIG_OVERLAY.md` - Feature documentation

## Key Design Decisions

1. **WebSocket for Real-Time Updates**: Enables immediate application without page reload
2. **Per-Step Granularity**: Users configure individual steps, not entire workflow
3. **Non-Persistent by Design**: Changes apply to current run only (no YAML modification)
4. **Immutable Agent Caching**: Different configs create separate agent instances
5. **State-Based Architecture**: Config travels through LangGraph state for consistency
6. **Client-Side Validation**: Frontend validates ranges, backend trusts frontend
7. **Graceful Degradation**: Invalid/missing config falls back to defaults

## Testing Recommendations

### Unit Tests
- Node config model validation (Pydantic)
- Agent creation with/without config overrides
- WebSocket message parsing and handling
- React hook lifecycle (connect/disconnect/reconnect)

### Integration Tests
- Full workflow execution with config updates
- WebSocket reconnection scenarios
- Agent behavior with overridden parameters
- Metadata tracking of config usage

### End-to-End Tests
1. Start workflow execution
2. Click config overlay on running step
3. Modify: model (gpt-4o), temperature (0.2), custom prompt
4. Save & Apply
5. Verify next step uses overrides
6. Check run output includes metadata flag

## Performance Considerations

- **Memory**: Node config dict added to state (~100-500 bytes per override)
- **CPU**: Config lookup on step start (O(1) dict access)
- **Network**: WebSocket messages typically <2KB each
- **Caching**: Agent cache may grow with different configs (mitigated by cleanup)

## Security Considerations

- **Input Validation**: Client validates ranges, backend should validate too (future)
- **Authorization**: No explicit auth check (inherits from WebSocket connection)
- **Injection**: System prompt is passed to LLM, could enable prompt injection (see notes)
- **Limits**: No rate limiting on config updates (could add if needed)

## Future Improvements

1. **Backend Validation**: Validate all config values server-side
2. **Config History**: Track and display config changes during run
3. **Presets**: Save/load common configurations
4. **Batch Operations**: Update multiple steps at once
5. **Persistence**: Option to save config changes to YAML
6. **Undo/Redo**: Navigate through config change history
7. **Diff View**: See exactly what changed before applying
8. **Telemetry**: Track which overrides users apply and their outcomes

## Notes

- Settings icon visibility depends on step status (not shown for completed steps)
- Config applies to next execution within same run, not retroactively
- WebSocket hook manages connection separately per runId
- Overlay slides from right side of screen (responsive design)
- No breaking changes to existing YAML or API contracts
