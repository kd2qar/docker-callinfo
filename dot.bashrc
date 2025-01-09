# ~/.bashrc: executed by bash(1) for non-login shells.

PS1='${debian_chroot:+($debian_chroot)}\h:\w\$ '

alias ls='ls --color'
alias ll='ls --color -Alh'
alias l='ls --color -lA'
#
# Some more alias to avoid making mistakes:
# alias rm='rm -i'
# alias cp='cp -i'
# alias mv='mv -i'

if [ ! -f /bin/vim ]; then
  apt-get -q update
  DEBIAN_FRONTEND="noninteractive" apt-get -y -q install vim vim-common locate
  updatedb &
fi

