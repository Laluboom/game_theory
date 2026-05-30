echo I work well
#!/bin/bash
#SBATCH --job-name=adgz422Trial
#SBATCH --partition=gengpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=24GB
#SBATCH --time=24:00:00
#SBATCH --gres=gpu:1                               # Use one gpu.
#SBATCH -e results/%x_%j.e                         # Standard output and error log [%j is replaced with the jobid]
#SBATCH -o results/%x_%j.o                         # [%x with the job n

openssl version

export LD_LIBRARY_PATH=/path/to/openssl/lib:$LD_LIBRARY_PATH
export CFLAGS="-I/usr/bin/openssl/include"
export LDFLAGS="-L/usr/bin/openssl/lib"

#Enable modules command
source /opt/flight/etc/setup.sh
flight env activate gridware

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$HOME/.pyenv/bin:$PATH"

eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"

export https_proxy=http://hpc-proxy00.city.ac.uk:3128
export CPPFLAGS="-I/opt/apps/gnu/include"
export LDFLAGS="-L/opt/apps/gnu/lib -L/opt/apps/gnu/lib64 -ltinfo"

module add compilers/gcc gnu
https_proxy=http://hpc-proxy00.city.ac.uk:3128 CPPFLAGS="-I/opt/apps/gnu/include" LDFLAGS="-L/opt/apps/gnu/lib -L/opt/apps/gnu/lib64 -ltinfo"   pyenv install 3.11

pyenv virtualenv 3.11 AI_Run

#Remove any unwanted modules
module purge
module load openssl
module load libs/nvidia-cuda/11.2.0/bin

python -c "import ssl; print(ssl.OPENSSL_VERSION)"
python --version
python trial/trial.py

