# 服务器命令记录
# 用户: rl8728@PU202502

# ========== MacroEnergy.jl 相关命令 ==========

# 进入 MacroEnergy.jl 目录
cd /scratch/gpfs/JENKINS/rl8728/MacroEnergy.jl
git restore .
git pull

module purge
module load gurobi/13.0.0
module load julia/1.12.1

export OMP_NUM_THREADS=4
sbatch ExampleSystems/china_elec_8760_one_stage/china_elec_8760_one_stage_benders.slurm

sbatch ExampleSystems/china_elec_8760_one_stage/china_elec_8760_one_stage.slurm




# 更新gurobi
julia --project=@. -e '
    using Pkg;
    Pkg.add("Gurobi");
    Pkg.build("Gurobi"; verbose=true);
'

julia --project=@. -e '
    using Pkg;
    Pkg.update();
'

取消所有任务：
scancel -u rl8728

更新所有结果文件：
find ./results | xargs touch


