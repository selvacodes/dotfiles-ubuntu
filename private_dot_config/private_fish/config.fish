if status is-interactive
    # Commands to run in interactive sessions can go here
    atuin init fish | source
end
alias k="kubectl"
starship init fish | source
set -gx VOLTA_HOME "$HOME/.volta"
set -gx PATH "$VOLTA_HOME/bin" $PATH
set -gx PATH "/home/shri/.local/bin" $PATH
set -gx PATH $PATH $HOME/.krew/bin
set -gx PATH $PATH $HOME/go/bin
set -gx PATH $PATH /usr/local/go/bin

# bun
set --export BUN_INSTALL "$HOME/.bun"
set --export PATH $BUN_INSTALL/bin $PATH
source "$HOME/.cargo/env.fish"

function zellij_session
    set session_name (basename (pwd))
    if zellij list-sessions | grep -q $session_name
        zellij attach -c $session_name
    else
        zellij -s $session_name
    end
end

