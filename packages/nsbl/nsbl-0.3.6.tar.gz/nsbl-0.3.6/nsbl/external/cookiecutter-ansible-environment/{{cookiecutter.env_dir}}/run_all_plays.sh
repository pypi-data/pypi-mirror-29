#!/usr/bin/env bash

if [ -e "$HOME/.nix-profile/etc/profile.d/nix.sh" ]; then source "$HOME/.nix-profile/etc/profile.d/nix.sh"; fi

# if [ -e "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh" ]; then source "/nix/var/nix/profiles/default/etc/profile.d/nix-daemon.sh"; fi

if [ -d "$HOME/.local/inaugurate/conda/envs/inaugurate/bin" ]; then
    export PATH="$HOME/.local/inaugurate/conda/envs/inaugurate/bin:$PATH"
fi
if [ -d "$HOME/.local/inaugurate/virtualenvs/inaugurate/bin" ]; then
    export PATH="$HOME/.local/inaugurate/virtualenvs/inaugurate/bin:$PATH"
fi
if [ -d "$HOME/.local/inaugurate/conda/bin" ]; then
    export PATH="$HOME/.local/inaugurate/conda/bin:$PATH"
fi

if [ -d "$HOME/.local/inaugurate/bin" ]; then
    export PATH="$HOME/.local/inaugurate/bin:$PATH"
fi

if [ -d "$HOME/.local/bin" ]; then
    export PATH="$HOME/.local/bin:$PATH"
fi


cd {{cookiecutter.playbook_dir}}

{{cookiecutter.extra_script_commands}}

ansible-playbook {{cookiecutter.ansible_playbook_args}} {{cookiecutter.ask_sudo}} {{cookiecutter.playbook}}
