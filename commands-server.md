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
module load gurobi/13.0.0
module load julia/1.12.1
export GUROBI_HOME=/usr/licensed/gurobi/13.0.0/linux64
export LD_LIBRARY_PATH=${GUROBI_HOME}/lib:${LD_LIBRARY_PATH}
export OMP_NUM_THREADS=1
cd /scratch/gpfs/JENKINS/rl8728/MacroEnergy.jl
julia --project=. ExampleSystems/aluminum_3zone/run.jl





取消所有任务：
scancel -u rl8728

更新所有结果文件：
find ./results | xargs touch


