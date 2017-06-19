#!/bin/bash

#PBS -P y33
#PBS -q normal
#PBS -l ncpus=8
#PBS -l mem=8GB
#PBS -l walltime=2:00:00
#PBS -l wd
#PBS -N galeisbstdem
#PBS -o galeisbstdem.out
#PBS -e galeisbstdem.err
#PBS -j oe

module load ga-aem/1.0
mpirun galeisbstdem.exe GeomSolve.con

