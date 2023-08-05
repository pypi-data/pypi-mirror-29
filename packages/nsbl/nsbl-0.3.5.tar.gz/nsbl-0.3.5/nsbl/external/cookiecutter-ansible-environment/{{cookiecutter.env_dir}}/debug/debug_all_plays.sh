#!/usr/bin/env bash

if [ -e "$HOME/.nix-profile/etc/profile.d/nix.sh" ]; then source "$HOME/.nix-profile/etc/profile.d/nix.sh"; fi

if [ -d "$HOME/.local/bin" ]; then
    export PATH="$HOME/.local/bin:$PATH"
fi

if [ -d "$HOME/.local/inaugurate/bin" ]; then
    export PATH="$HOME/.local/inaugurate/bin:$PATH"
fi

if [ -d "$HOME/.local/inaugurate/conda/bin" ]; then
    export PATH="$PATH:$HOME/.local/inaugurate/conda/bin"
fi

cd {{cookiecutter.playbook_dir}}/../debug

{{cookiecutter.extra_script_commands}}

ANSIBLE_CONFIG=./ansible.cfg ansible-playbook -vvvv {{cookiecutter.ask_sudo}} ../plays/{{cookiecutter.playbook}}
