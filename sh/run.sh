#!/bin/bash
tmux new-session -d -s job_$2 "htop"
for i in {1..1};
    do
        sleep_time=$((i*6)) # seconds
	tmux new-window -t job_$2 -n seed_$i
	tmux send-keys -t job_$2:seed_$i "sleep $sleep_time && ./train.sh --seed $i" Enter;
done

