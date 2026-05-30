#!/bin/bash
#SBATCH -D /users/adgz422/GameTheoryIMATMT
#SBATCH --job-name=GameTheoryBayes
#SBATCH --partition=gengpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --cpus-per-task=6
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=viseshakbari@gmail.com
#SBATCH --mem=94GB
#SBATCH --time=24:00:00
#SBATCH --gres=gpu:2
#SBATCH -o results/Llama3_Bayes.o
#SBATCH -e results/Llama3_Bayes.e
#SBATCH --licenses=anshpc:176		     # Number of ansys hpc licenses needed (4 * 48 - 16)

#enable modules
source /opt/flight/etc/setup.sh
flight env activate gridware

#remove any unwanted modules
module purge

#Modules required
module load fluent
module load libs/nvidia-cuda/11.2.0/bin
module add gnu

python --version
python Bayes_Player.py
