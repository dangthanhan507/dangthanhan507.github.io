---
layout: default
title: Great Lakes Cluster
parent: Cluster Notes
nav_order: 8
---

# Great Lakes Cluster

In order to get access, you have to request HPC login credentials from the IT department of your institution. In [Getting Started](https://its.umich.edu/advanced-research-computing/high-performance-computing/great-lakes/getting-started), we can find the [HPC User login](https://its.umich.edu/advanced-research-computing/high-performance-computing/login). This link allows you to request access to great lakes.

Once you get access, you can login using your uofm uniqname+password combo.

## Starting out

1. Get into UofM Network (via VPN or on-campus).
2. login via ssh

```bash
ssh [uniqname]@greatlakes.arc-ts.umich.edu
```

You'll find yourself in your home directory, which is located at `/home/[uniqname]`.

## Creating a batch job

```bash
#!/bin/bash # COMMENT: The interpreter used to execute the script
# COMMENT: #SBATCH directives that convey submission options:
#SBATCH --job-name=example_job
#SBATCH --mail-user=[uniqname]@umich.edu
#SBATCH --mail-type=BEGIN,END
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=1000m
#SBATCH --time=10:00
#SBATCH --account=test
#SBATCH --partition=standard
#SBATCH --output=/home/%u/%x-%j.log
# COMMENT: The application(s) to execute along with its input arguments and options: <insert commands here>
```

## One Node, One Processor

```bash
#!/bin/bash #SBATCH --job-name JOBNAME

#SBATCH --nodes=1

#SBATCH --cpus-per-task=1

#SBATCH --mem-per-cpu=1g

#SBATCH --time=00:15:00

#SBATCH --account=test

#SBATCH --partition=standard

#SBATCH --mail-type=NONE

# COMMENT:The application(s) to execute along with its input arguments and options:
echo "Hello World"
srun --cpu-bind=none hostname -s
```

This allocates one node with one processor, 1 GB of memory, and a time limit of 15 minutes. The `srun` command runs the `hostname` command on the allocated node. We also print "Hello World" to the console.

Output:
```console
Hello World
srun: job 29838616 queued and waiting for resources
srun: job 29838616 has been allocated resources
gl3018
```

## Batch job: Options for requesting resources

| Option | SLURM Command (#SBATCH) | Example |
| ------ | ----------------------- | ------- |
| Job name | `--job-name=<name>` | `--job-name=asdf` |
| Account | `--account=<account>` | `--account=test` This account is from the provider account  |
| Queue | `--partition=<queue>` | `--partition=standard` We can choose "standard", "gpu" (GPU jobs only), largemem (large memory), viz, debug, standard-oc (oc=on-campus software) |
| Wall time limit | `--time=<dd-hh:mm:ss>` | `--time=10:00` (10 minutes) If you want if you got the write wall time, you can try on debug partition |
| Node count | `--nodes=<count>` | `--nodes=3` |
| Process count per node | `--ntasks-per-node=<count>` | `--ntasks-per-node=1` invoke ntasks on each node |
| Core count (per process) | `--cpus-per-task=<cores>` | `--cpus-per-task=1` Without specifying, it defaults to 1 processor per task |
| Memory limit | `--mem=<limit>` (Memory per node in GiB, MiB, KiB) | `--mem=12000m` (12 GiB roughly) |
| Minimum memory per processor | `--mem-per-cpu=<memory>` | `--mem-per-cpu=1000m` (1 GiB per CPU) |
| Request GPUs | `--gres=gpu:<count>` `--gpus=[type:]<number>` | `--gres=gpu:2` `gpus=2` |
| Process count per GPU | `--ntasks-per-gpu=<count>` Must be used with `--ntasks` or `--gres=gpu:` | `--ntasks-per-gpu=1` `--gres=gpu:4` 2 tasks per GPU times 4 GPUS = 8 tasks total |

## Batch job: Environment variables and logs

| Option | SLURM Command (#SBATCH) | Example |
| ------ | ----------------------- | ------- |
| Copy environment | `--export=ALL` | `--export=ALL` This copies all environment variables to the job |
| Set Env variable | `--export=<variable=value,var2=val2>` | `--export=EDITOR=/bin/vim` |
| Standard output file | `--output=<file path>` (path must exist) | `--output=/home/%u/%x-%j.log` NOTE: %u is the user, %x is the job name, %j is the job ID |
| Standard error file | `--error=<file path>` (path must exist) | `--error=/home/%u/%x-%j.err` |


## Batch job: job control

| Option | SLURM Command (#SBATCH) | Example |
| ------ | ----------------------- | ------- |
| Job array | `--array=<array indices>` | `--array=0-15` |
| Job dependency | `--dependency=after:jobID[:jobID...]` | `--dependency=after:1234[:1233]` |
| Email address | `--mail-user=<email>` | `--mail-user=uniqname@umich.edu` |
| Defer job til time | `--begin=<date/time>` | `--begin=2020-12-25T12:30:00` |

