#!/bin/bash
#SBATCH --job-name=mpi-test
#SBATCH --workdir=/master/home/dabi/VC-Projects/Software/Mine/Current/mpi_map/examples/
#SBATCH --output=job.%J.out
#SBATCH --error=job.%J.err
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=8
#SBATCH --mail-user=dabi@mit.edu

$*
