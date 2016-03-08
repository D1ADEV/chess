#!/bin/bash

url=$(curl --silent http://localhost:8000/createnewgame)
echo "url : $url"
firstId=$(curl --silent http://localhost:8000/joingame/$url)
echo "first Id : $firstId"
secondId=$(curl --silent http://localhost:8000/joingame/$url)
echo "second Id : $secondId"
thirdId=$(curl --silent http://localhost:8000/joingame/$url)
if [ "False" != "$thirdId" ];
then
echo "could request a third id, NOT GOOD"
else
echo "couldn't request a third id, GOOD"
fi
status=$(curl --silent http://localhost:8000/debug)
games=$(echo "$status" | tr " " "\n" | grep -c "Game.Game") #http://stackoverflow.com/questions/26212889/bash-counting-substrings-in-a-string
echo "$games games"

