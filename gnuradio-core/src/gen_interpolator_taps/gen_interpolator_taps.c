/* -*- c++ -*- */
/*
 * Copyright 2002 Free Software Foundation, Inc.
 * 
 * This file is part of GNU Radio
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define	NSTEPS		 10	// how many steps of mu are in the generated table
#define	MAX_NSTEPS	256
#define	NTAPS		  8	// # of taps in the interpolator
#define	MAX_NTAPS	128

extern void initpt (double x[], int ntaps);
extern double objective (double x[], int *ntaps);
extern double global_mu;
extern double global_B;

// fortran
extern double prax2_ (double (fct)(double x[], int *ntaps),
		      double initv[], int *ntaps, double result[]);

static void 
usage (char *name)
{
  fprintf (stderr, "usage: %s [-v] [-n <nsteps>] [-t <ntaps>] [-B <bw>]\n", name);
  exit (1);
}

static void
printline (double x[], int ntaps, int imu, int nsteps)
{
  int	i;
  
  printf ("  { ");
  for (i = 0; i < ntaps; i++){
    printf ("%12.5e", x[i]);
    if (i != ntaps - 1)
      printf (", ");
    else
      printf (" }, // %3d/%d\n", imu, nsteps);
  }
}

int 
main (int argc, char **argv)
{
  double	xx[MAX_NSTEPS+1][MAX_NTAPS];
  int	 	ntaps = NTAPS;
  int		nsteps = NSTEPS;
  int		i, j;
  double 	result;
  double	step_size;
  int		c;
  int		verbose = 0;

  global_B = 0.25;

  while ((c = getopt (argc, argv, "n:t:B:v")) != EOF){
    switch (c){
    case 'n':
      nsteps = strtol (optarg, 0, 0);
      break;

    case 't':
      ntaps = strtol (optarg, 0, 0);
      break;

    case 'B':
      global_B = strtod (optarg, 0);
      break;
      
    case 'v':
      verbose = 1;
      break;
      
    default:
      usage (argv[0]);
      break;
    }
  }

  if ((nsteps & 1) != 0){
    fprintf (stderr, "%s: nsteps must be even\n", argv[0]);
    exit (1);
  }

  if (nsteps > MAX_NSTEPS){
    fprintf (stderr, "%s: nsteps must be < %d\n", argv[0], MAX_NSTEPS);
    exit (1);
  }
    
  if ((ntaps & 1) != 0){
    fprintf (stderr, "%s: ntaps must be even\n", argv[0]);
    exit (1);
  }

  if (nsteps > MAX_NTAPS){
    fprintf (stderr, "%s: ntaps must be < %d\n", argv[0], MAX_NTAPS);
    exit (1);
  }

  if (global_B < 0 || global_B > 0.5){
    fprintf (stderr, "%s: bandwidth must be in the range (0, 0.5)\n", argv[0]);
    exit (1);
  }
    
  step_size = 1.0/nsteps;
  
  // the optimizer chokes on the two easy cases (0/N and N/N).  We do them by hand...

  for (i = 0; i < ntaps; i++)
    xx[0][i] = 0.0;
  xx[0][ntaps/2] = 1.0;


  // compute optimal values for mu <= 0.5

  for (j = 1; j <= nsteps/2; j++){

    global_mu = j * step_size;		// this determines the MU for which we're computing the taps

    // initialize X to a reasonable starting value

    initpt (&xx[j][0], ntaps);

    // find the value of X that minimizes the value of OBJECTIVE

    result = prax2_ (objective, &xx[j][0], &ntaps, &xx[j][0]);

    if (verbose){
      fprintf (stderr, "Mu: %10.8f\t", global_mu);
      fprintf (stderr, "Objective: %g\n", result);
    }
  }

  // now compute remaining values via symmetry

  for (j = 0; j < nsteps/2; j++){
    for (i = 0; i < ntaps; i++){
      xx[nsteps - j][i] = xx[j][ntaps-i-1];
    }
  }

  // now print out the table

  printf ("\
/*\n\
 * This file was machine generated by gen_interpolator_taps.\n\
 * DO NOT EDIT BY HAND.\n\
 */\n\n");


  printf ("static const int	NTAPS     = %4d;\n", ntaps);
  printf ("static const int	NSTEPS    = %4d;\n", nsteps);
  printf ("static const double	BANDWIDTH = %g;\n\n", global_B);
  
  printf ("static const float taps[NSTEPS+1][NTAPS] = {\n");
  printf ("  //    -4            -3            -2            -1             0             1             2             3                mu\n");


  for (i = 0; i <= nsteps; i++)
    printline (xx[i], ntaps, i, nsteps);
  
  printf ("};\n\n");

  return 0;
}
