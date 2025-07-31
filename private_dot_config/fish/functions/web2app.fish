function web2app
    if test (count $argv) -ne 3
        echo "Usage: web2app <AppName> <AppURL> <IconURL> (IconURL must be in PNG -- use https://dashboardicons.com)"
        return 1
    end

    set APP_NAME $argv[1]
    set APP_URL $argv[2]
    set ICON_URL $argv[3]
    set ICON_DIR "$HOME/.local/share/applications/icons"
    set DESKTOP_FILE "$HOME/.local/share/applications/$APP_NAME.desktop"
    set ICON_PATH "$ICON_DIR/$APP_NAME.png"

    mkdir -p $ICON_DIR

    mkdir -p  $HOME/.config/zen-apps/$APP_NAME

    if not curl -sL -o $ICON_PATH $ICON_URL
        echo "Error: Failed to download icon."
        return 1
    end

    begin
     echo "[Desktop Entry]"
     echo "Version=1.0"
     echo "Name=$APP_NAME"
     echo "Comment=$APP_NAME"
     # echo "Exec=flatpak run app.zen_browser.zen -P Apps --new-window \"$APP_URL\" --name=\"$APP_NAME\" --class=\"$APP_NAME\""
     echo "Exec=qutebrowser --desktop-file-name \"$APP_NAME\" --target window \"$APP_URL\""
     echo "Terminal=false"
     echo "Type=Application"
     echo "Icon=$ICON_PATH"
     echo "StartupNotify=true"
   end > $DESKTOP_FILE
    chmod +x $DESKTOP_FILE
end
