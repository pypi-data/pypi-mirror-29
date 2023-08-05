#compdef globus
_globus() {
    if type globus > /dev/null;
    then
        eval "$(env COMMANDLINE="${words[1,$CURRENT]}" globus --shell-complete ZSH)"
    fi
}
compdef _globus globus
