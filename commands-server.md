# 服务器命令记录
# 用户: rl8728@PU202502

# ========== MacroEnergy.jl 相关命令 ==========

# 进入 MacroEnergy.jl 目录
cd /scratch/gpfs/JENKINS/rl8728/MacroEnergy.jl

# 更新代码并提交作业
git restore .
git pull
sbatch aluminum_3zone.slurm


取消所有任务：
scancel -u rl8728

更新所有结果文件：
find ./results | xargs touch


