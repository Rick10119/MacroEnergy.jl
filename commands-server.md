# 服务器命令记录
# 用户: rl8728@PU202502

# ========== MacroEnergy.jl 相关命令 ==========

# 进入 MacroEnergy.jl 目录
cd /scratch/gpfs/JENKINS/rl8728/MacroEnergy.jl

# 更新代码并提交作业
git restore .
git pull
sbatch aluminum_3zone.slurm

# 或者直接运行（用于测试）
module purge
module load gurobi/12.0.0
module load julia/1.12.1
export GUROBI_HOME=/usr/licensed/gurobi/12.0.0/linux64
export LD_LIBRARY_PATH=${GUROBI_HOME}/lib:${LD_LIBRARY_PATH}
export OMP_NUM_THREADS=1
cd /scratch/gpfs/JENKINS/rl8728/MacroEnergy.jl
julia --project=. ExampleSystems/aluminum_3zone/run.jl


cd /scratch/gpfs/rl8728/PyPSA-China-0
module load anaconda3/2024.6
conda activate pypsa-plot

git restore .
git pull
snakemake --unlock
sbatch job_plot_capacity.slurm

sbatch job_plot_optimal_point.slurm

sbatch job_scenario_analysis.slurm


sbatch job_plot_optimal_point.slurm
sbatch job_plot_capacity.slurm

sbatch job_scenario_analysis.slurm
sbatch job_plot_capacity.slurm

sbatch jobs/job_HMM_2050_100p.slurm

snakemake --configfile configs/config_LMM_2040_60p.yaml -np

snakemake --configfile configs/config_HMM_2050_20p.yaml -np --rerun-incomplete --ignore-incomplete --rerun-triggers mtime

snakemake --configfile configs/config_LMM_2050_20p.yaml --cores 6 --rerun-incomplete --ignore-incomplete --rerun-triggers mtime

snakemake --configfile configs/config_HMM_2050_non_flexible.yaml --cores 6 --rerun-incomplete --ignore-incomplete --rerun-triggers mtime

snakemake --cores 6 --rerun-incomplete --ignore-incomplete --rerun-triggers mtime

Sep 2 run the jobs:

cd /scratch/gpfs/rl8728/PyPSA-China-1
module load anaconda3/2024.6
conda activate pypsa-plot

git restore .
git pull
find ./results | xargs touch
snakemake --unlock
chmod +x submit_multiple_jobs.sh 
./submit_multiple_jobs.sh


取消所有任务：
scancel -u rl8728

更新所有结果文件：
find ./results | xargs touch


Sep 2, plot:

find ./results | xargs touch
snakemake --unlock
snakemake --configfile configs/config_HMM_2050_20p.yaml --cores 6 --rerun-incomplete --ignore-incomplete --rerun-triggers mtime
