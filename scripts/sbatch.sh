#!/bin/bash

#SBATCH -A "danielk80_gpu"               # Set the account name, assuming this is correct
#SBATCH --partition=a100                 # Use the A100 GPU partition
#SBATCH --gres=gpu:1                     # Request one GPU
#SBATCH --nodes=1                        # Request one node
#SBATCH --ntasks-per-node=1              # Run one task per node
#SBATCH --mem-per-gpu=40G                 # Memory per CPU
#SBATCH --job-name="TNAYAK_DPOK_TEST"    # Set the job name
#SBATCH --output=slurm-%j.out            # Standard output and error log

source ~/.bashrc
conda activate dpok # activate the Python environment

# runs your code
accelerate launch train_online_pg.py --p_batch_size 4 --reward_weight 10 --kl_weight 0.01  --learning_rate 1e-5 --single_flag 1 --single_prompt "A green colored rabbit." --gradient_accumulation_steps 12 --clip_norm 0.1 --g_batch_size 10 --multi_gpu 0 --v_flag 1 --num_train_epochs 10 
