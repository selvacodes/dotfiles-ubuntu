if status is-interactive
    # Commands to run in interactive sessions can go here
    atuin init fish | source
end
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
# Aliases

alias k="kubectl"
alias nv="/home/shri/nvim/nvim-linux-x86_64/bin/nvim"
alias ls='eza -lh --group-directories-first --icons=auto'
alias lsa='ls -a'
alias lt='eza --tree --level=2 --long --icons --git'
alias lta='lt -a'
alias ff='fzf --preview "bat --style=numbers --color=always {}"'

# zd function
function zd
    if test (count $argv) -eq 0
        cd ~
        return
    else if test -d $argv[1]
        cd $argv[1]
    else
        z $argv
        and printf " \U000F17A9 "
        and pwd
        or echo "Error: Directory not found"
    end
end

# open function
function open
    xdg-open $argv >/dev/null 2>&1
end

# Directory shortcuts
alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'

# Tools
alias n='nvim'
alias g='git'

# Git
alias gcm='git commit -m'
alias gcam='git commit -a -m'
alias gcad='git commit -a --amend'

# opencode
fish_add_path /home/shri/.opencode/bin
~/.local/bin/mise activate fish | source

# Added by LM Studio CLI (lms)
set -gx PATH $PATH /home/shri/.lmstudio/bin
# End of LM Studio CLI section

function y
	set tmp (mktemp -t "yazi-cwd.XXXXXX")
	yazi $argv --cwd-file="$tmp"
	if read -z cwd < "$tmp"; and [ -n "$cwd" ]; and [ "$cwd" != "$PWD" ]
		builtin cd -- "$cwd"
	end
	rm -f -- "$tmp"
end
