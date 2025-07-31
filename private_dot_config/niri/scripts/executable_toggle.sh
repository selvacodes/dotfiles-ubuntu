#!/bin/bash

# Script to toggle the current focused floating window to/from the "hidden" workspace.
# If no focused floating window, it checks "hidden" for one and brings it back.

HIDDEN_WS_NAME="hidden"

# Get windows and workspaces as JSON
WINDOWS=$(niri msg -j windows)
WORKSPACES=$(niri msg -j workspaces)

# Find the active workspace ID (the one you're currently on)
ACTIVE_WS_ID=$(echo "$WORKSPACES" | jq -r 'to_entries[] | select(.value.is_active) | .key')

echo "Active workspace: $ACTIVE_WS_ID"

# Find the hidden workspace ID
HIDDEN_WS_ID=$(echo "$WORKSPACES" | jq -r --arg name "$HIDDEN_WS_NAME" 'to_entries[] | select(.value.name == $name) | .value.idx')
echo "Hidden workspace: $HIDDEN_WS_ID"

if [ -z "$HIDDEN_WS_ID" ]; then
    echo "Hidden workspace not found!"
    exit 1
fi

# Find the focused window ID
FOCUSED_WINDOW_ID=$(echo "$WINDOWS" | jq -r 'to_entries[] | select(.value.is_focused) | .value.id')

echo "Focused window: $FOCUSED_WINDOW_ID"

if [ -n "$FOCUSED_WINDOW_ID" ]; then
    # Check if it's floating (Niri exposes "size" and "position" for floating windows; assume floating if not tiled)
    # Note: Niri doesn't have a direct "is_floating" flag in JSON, but we can infer by checking if it's not in a column.
    # For simplicity, we'll assume the user ensures it's floating; customize if needed (e.g., check geometry).
    CURRENT_WS_ID=$(echo "$ACTIVE_WS_ID") 
    echo "Current WS ID: $CURRENT_WS_ID"

    if [ "$CURRENT_WS_ID" = "$HIDDEN_WS_ID" ]; then
        # Already on hidden: Move to active workspace and focus
        niri msg action move-window-to-workspace --window-id "$FOCUSED_WINDOW_ID" "$ACTIVE_WS_ID" --focus false
        # niri msg action focus-window --window-id "$FOCUSED_WINDOW_ID"
    else
        # On active: Move to hidden
        echo "IN ELSE"
        niri msg action move-window-to-workspace --window-id "$FOCUSED_WINDOW_ID" "$HIDDEN_WS_ID" --focus false
    fi
else
    # No focused window: Check for a floating window on hidden and bring the first one back
    # (Infer "floating" by app_id or title if needed; here we just grab the first window on hidden)
    HIDDEN_WINDOW_ID=$(echo "$WINDOWS" | jq -r --arg ws "$HIDDEN_WS_ID" 'to_entries[] | select(.value.workspace.id == ($ws | tonumber)) | .key' | head -n 1)

    if [ -n "$HIDDEN_WINDOW_ID" ]; then
        niri msg action move-window-to-workspace --window-id "$HIDDEN_WINDOW_ID" "$ACTIVE_WS_ID" --focus false
        # niri msg action focus-window --window-id "$HIDDEN_WINDOW_ID" 
    else
        echo "No floating window found on hidden workspace."
        # Optional: Add a notification here, e.g., notify-send "Nothing to show"
    fi
fi
