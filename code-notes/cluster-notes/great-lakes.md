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

Keep in mind that you are in the login node. This is a place to view job results and submit new jobs. It cannot be used to run application workloads. 

We will mainly run sbatch and srun to work.

We can check if we can submit jobs by running the following command:

```console
[andang@gl-login1 ~]$ hostname -s
gl-login1
[andang@gl-login1 ~]$ srun --cpu-bind=none hostname -s
srun: job 29842513 queued and waiting for resources
srun: job 29842513 has been allocated resources
gl3051
[andang@gl-login1 ~]$
```

As you can see, srun is a fully blocking command.



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

This allocates one node with one processor, 1 GB of memory, and a time limit of 15 minutes. We print "Hello World" to the console.

Output:
```console
Hello World
srun: job 29838616 queued and waiting for resources
srun: job 29838616 has been allocated resources
gl3018
```

We can run salloc to do interafctive job. 
```shell-session
[user@gl-login1 ~]$ salloc --account=test
salloc: Pending job allocation 10081688
salloc: job 10081688 queued and waiting for resources
salloc: job 10081688 has been allocated resources
salloc: Granted job allocation 10081688
salloc: Waiting for resource configuration
salloc: Nodes gl3052 are ready for job
[user@gl3052 ~]$ hostname
gl3052.arc-ts.umich.edu
[user@gl3052 ~]$
```

## Going on interactive mode

[](https://documentation.its.umich.edu/node/4994) Check out this link for more information on how to do things interactively on Great Lakes.

