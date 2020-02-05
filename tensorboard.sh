#!/bin/bash
FOLDER_NAME="option-critic-image-space"

SSH_ADDRESS="ec2-54-144-246-200.compute-1.amazonaws.com"
SUBFOLDER_NAME="exp1"
scp -i ~/Documents/research/aws/marwa_key_pair.pem -r ubuntu@$SSH_ADDRESS:/home/ubuntu/$FOLDER_NAME/results/* ~/Documents/IAP/Research/$FOLDER_NAME/results/$SUBFOLDER_NAME/

ssh -i ~/Documents/research/aws/marwa_key_pair.pem -NL 6008:localhost:6006 ubuntu@ec2-54-144-246-200.compute-1.amazonaws.com

ssh -i ~/Documents/research/aws/marwa_key_pair.pem -NL 6008:localhost:6006 ubuntu@ec2-54-144-246-200.compute-1.amazonaws.com