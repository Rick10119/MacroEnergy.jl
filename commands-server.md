@ -1,81 +0,0 @@
l214365l@PU202502


cd /scratch/gpfs/JENKINS/rl8728/MacroEnergy.jl



git restore .
git pull
snakemake --unlock
sbatch job_scenario_analysis.slurm


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
