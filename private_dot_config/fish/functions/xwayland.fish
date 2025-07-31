
function xwayland
 sleep 1  # Give it a moment to start
 killall xwayland-satellite || true
 xwayland-satellite &
 sleep 1  # Give it a moment to start
 if pgrep xwayland > /dev/null
     notify-send "xwayland started successfully"
 else
     notify-send "xwayland failed to start"
 end
end
