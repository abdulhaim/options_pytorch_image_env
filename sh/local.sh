#!/bin/bash

FOLDER_NAME="option-critic-pytorch"
declare -a arr=(
    "ec2-54-144-246-200.compute-1.amazonaws.com"
    )

for SSH_ADDRESS in "${arr[@]}"
do
    echo $SSH_ADDRESS

    # Pass folder that I want to train
    ssh -i ~/Documents/research/aws/marwa_key_pair.pem ubuntu@$SSH_ADDRESS "mkdir /home/ubuntu/$FOLDER_NAME"
    scp -i ~/Documents/research/aws/marwa_key_pair.pem ~/Documents/IAP/Research/$FOLDER_NAME/*.py ubuntu@$SSH_ADDRESS:/home/ubuntu/$FOLDER_NAME/
    scp -i ~/Documents/research/aws/marwa_key_pair.pem ~/Documents/IAP/Research/$FOLDER_NAME/*.md ubuntu@$SSH_ADDRESS:/home/ubuntu/$FOLDER_NAME/
    scp -i ~/Documents/research/aws/marwa_key_pair.pem ~/Documents/IAP/Research/$FOLDER_NAME/*.txt ubuntu@$SSH_ADDRESS:/home/ubuntu/$FOLDER_NAME/
    scp -i ~/Documents/research/aws/marwa_key_pair.pem ~/Documents/IAP/Research/$FOLDER_NAME/*.sh ubuntu@$SSH_ADDRESS:/home/ubuntu/$FOLDER_NAME/
    scp -i ~/Documents/research/aws/marwa_key_pair.pem ~/Documents/IAP/Research/$FOLDER_NAME/.gitignore ubuntu@$SSH_ADDRESS:/home/ubuntu/$FOLDER_NAME/
    scp -i ~/Documents/research/aws/marwa_key_pair.pem -r ~/Documents/IAP/Research/$FOLDER_NAME/.git ubuntu@$SSH_ADDRESS:/home/ubuntu/$FOLDER_NAME/.git
    scp -i ~/Documents/research/aws/marwa_key_pair.pem -r ~/Documents/IAP/Research/$FOLDER_NAME/runs/ ubuntu@$SSH_ADDRESS:/home/ubuntu/$FOLDER_NAME/results

    # Pass dependency shell script
    scp -i ~/Documents/research/aws/marwa_key_pair.pem  -r ~/Documents/IAP/Research/$FOLDER_NAME/dependencies.sh ubuntu@$SSH_ADDRESS:/home/ubuntu/dependencies.sh
done
