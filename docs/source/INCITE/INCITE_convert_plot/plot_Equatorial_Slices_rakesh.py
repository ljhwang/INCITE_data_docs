#
#  Copyright (C) 2018 by the authors of the RAYLEIGH code.
#
#  This file is part of RAYLEIGH.
#
#  RAYLEIGH is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3, or (at your option)
#  any later version.
#
#  RAYLEIGH is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with RAYLEIGH; see the file LICENSE.  If not see
#  <http://www.gnu.org/licenses/>.
#

# VII.1  Equatorial Slices
# --------------------------
# 
# **Summary:**    2-D profiles of selected output variables in the equatorial plane. 
# 
# **Subdirectory:**  Equatorial_Slices
# 
# **main_input prefix:** equatorial
# 
# **Python Class:** Equatorial_Slices
# 
# **Additional Namelist Variables:**  
# None
# 
# The equatorial-slice output type allows us to examine how the fluid properties vary in longitude and radius.
# 
# Examining the *main_input* file, we see that the following output values have been denoted for the Equatorial Slices (see *rayleigh_output_variables.png* for mathematical formulae):
# 
# 
# | Menu Code  | Description |
# |------------|-------------|
# | 1          | Radial Velocity |
# | 2          | Theta Velocity |
# | 3          | Phi Velocity  |
# 
# 
# 
# 
# In the example that follows, we demonstrate how to create a 2-D plot of radial velocity in the equatorial plane (at a single time step).
# 
# We begin with the usual preamble.  Examining the data structure, we see that the *vals* array is dimensioned to account for longitudinal variation, and that we have the new coordinate attribute *phi*.

# In[31]:

from rayleigh_diagnostics import Equatorial_Slices
import sys
import os
import numpy
import matplotlib.pyplot as plt
from matplotlib import ticker, font_manager




def plot_each_Equatorial_Slices_rakesh(istring, init_time):
  es = Equatorial_Slices(istring)
  tindex =0 # Grab first time index from this file
  
################################
# Equatorial Slice 
#Set up the grid
  
  niter = es.niter
  iters = es.iters[tindex]
  time = es.time[tindex] - init_time
  
#  print('niter: ', niter)
#  print('iters: ', iters)
#  print('time: ', time)
  
  remove_mean = False # Remove the m=0 mean
  nr = es.nr
  nphi = es.nphi
  r = es.radius/numpy.max(es.radius)
  phi = numpy.zeros(nphi+1,dtype='float64')
  phi[0:nphi] = es.phi
  phi[nphi] = numpy.pi*2  # For display purposes, it is best to have a redunant data point at 0,2pi

#We need to generate a cartesian grid of x-y coordinates (both X & Y are 2-D)
  radius_matrix, phi_matrix = numpy.meshgrid(r,phi)
  X = radius_matrix * numpy.cos(phi_matrix)
  Y = radius_matrix * numpy.sin(phi_matrix)
  
  qindex = es.lut[1] # radial velocity
  field_u = numpy.zeros((nphi+1,nr),dtype='float64')
  field_u[0:nphi,:] =es.vals[:,:,qindex,tindex]
  field_u[nphi,:] = field_u[0,:]  #replicate phi=0 values at phi=2pi
  
  qindex = es.lut[802] # B_theta
  field_B = numpy.zeros((nphi+1,nr),dtype='float64')
  field_B[0:nphi,:] = -es.vals[:,:,qindex,tindex]  # B_z = -B_theta
  field_B[nphi,:] = field_B[0,:]  #replicate phi=0 values at phi=2pi
  
  qindex = es.lut[501] # temperature
  field_T = numpy.zeros((nphi+1,nr),dtype='float64')
  field_T[0:nphi,:] = es.vals[:,:,qindex,tindex]
  field_T[nphi,:] = field_T[0,:]  #replicate phi=0 values at phi=2pi

#remove the mean if desired (usually a good idea, but not always)
  if (remove_mean):
    for i in range(nr):
      the_mean = numpy.mean(field_u[:,i])
      field_u[:,i] = field_u[:,i]-the_mean
  
  if (remove_mean):
    for i in range(nr):
      the_mean = numpy.mean(field_B[:,i])
      field_B[:,i] = field_B[:,i]-the_mean
  
  if (remove_mean):
    for i in range(nr):
      the_mean = numpy.mean(field_T[:,i])
      field_T[:,i] = field_T[:,i]-the_mean

#Plot
  figdpi=300
  sizetuple=(8,8)
 
#Plot Ur
  fig, ax = plt.subplots(figsize=sizetuple,dpi=figdpi)
  tsize = 20     # title font size
  cbfsize = 10   # colorbar font size
  v_max = numpy.std(field_u)
  v_min = -v_max
  img = ax.pcolormesh(X,Y,field_u,cmap='seismic',vmin=v_min,vmax=v_max)
  ax.axis('equal')  # Ensure that x & y axis ranges have a 1:1 aspect ratio
  ax.axis('off')    # Do not plot x & y axes
  
# Plot bounding circles
  ax.plot(r[nr-1]*numpy.cos(phi), r[nr-1]*numpy.sin(phi), color='black')  # Inner circle
  ax.plot(r[0]*numpy.cos(phi), r[0]*numpy.sin(phi), color='black')  # Outer circle
  
  ax.set_title(r'$u_r$', fontsize=20)
  
#colorbar ...
  cbar = plt.colorbar(img,orientation='horizontal', shrink=0.5, aspect = 15, ax=ax)
  cbar.set_label(r'$u_r$')
  
  tick_locator = ticker.MaxNLocator(nbins=5)
  cbar.locator = tick_locator
  cbar.update_ticks()
  cbar.ax.tick_params(labelsize=cbfsize)   #font size for the ticks
  
  t = cbar.ax.xaxis.label
  t.set_fontsize(cbfsize)  # font size for the axis title
  
  
  plt.tight_layout()
  savefile = 'images/Equatorial_Slice_Ur.png'
  print('Saving figure to: ', savefile)
  plt.savefig(savefile)

#Plot Bz
  fig, ax = plt.subplots(figsize=sizetuple,dpi=figdpi)
  tsize = 20     # title font size
  cbfsize = 10   # colorbar font size
  v_max = numpy.max(field_B)
  v_min = -v_max
  img = ax.pcolormesh(X,Y,field_B,cmap='seismic',vmin=v_min,vmax=v_max)
  ax.axis('equal')  # Ensure that x & y axis ranges have a 1:1 aspect ratio
  ax.axis('off')    # Do not plot x & y axes
  
# Plot bounding circles
  ax.plot(r[nr-1]*numpy.cos(phi), r[nr-1]*numpy.sin(phi), color='black')  # Inner circle
  ax.plot(r[0]*numpy.cos(phi), r[0]*numpy.sin(phi), color='black')  # Outer circle
  
  ax.set_title(r'$B_z$', fontsize=20)
  
#colorbar ...
  cbar = plt.colorbar(img,orientation='horizontal', shrink=0.5, aspect = 15, ax=ax)
  cbar.set_label(r'$B_z$')
  
  tick_locator = ticker.MaxNLocator(nbins=5)
  cbar.locator = tick_locator
  cbar.update_ticks()
  cbar.ax.tick_params(labelsize=cbfsize)   #font size for the ticks
  
  t = cbar.ax.xaxis.label
  t.set_fontsize(cbfsize)  # font size for the axis title
  
  
  plt.tight_layout()
  savefile = 'images/Equatorial_Slice_Bz.png'
  print('Saving figure to: ', savefile)
  plt.savefig(savefile)
  
  
  #Plot T
  fig, ax = plt.subplots(figsize=sizetuple,dpi=figdpi)
  tsize = 20     # title font size
  cbfsize = 10   # colorbar font size
  v_max = numpy.max(field_T)
  v_min = numpy.min(field_T)
  img = ax.pcolormesh(X,Y,field_T,cmap='hot',vmin=v_min,vmax=v_max)
  ax.axis('equal')  # Ensure that x & y axis ranges have a 1:1 aspect ratio
  ax.axis('off')    # Do not plot x & y axes
  
# Plot bounding circles
  ax.plot(r[nr-1]*numpy.cos(phi), r[nr-1]*numpy.sin(phi), color='black')  # Inner circle
  ax.plot(r[0]*numpy.cos(phi), r[0]*numpy.sin(phi), color='black')  # Outer circle
  
  ax.set_title(r'Temperature $T$', fontsize=20)
  bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=1.0)
  ttxt = "$z = 0.0$ \n $t = $ {:.3f}".format(time)
  ax.text(0.78, -0.95, ttxt, ha="center", va="center", size=14, bbox=bbox_props)
#colorbar ...
  cbar = plt.colorbar(img,orientation='horizontal', shrink=0.5, aspect = 15, ax=ax)
  cbar.set_label(r'$T$')
  
  tick_locator = ticker.MaxNLocator(nbins=5)
  cbar.locator = tick_locator
  cbar.update_ticks()
  cbar.ax.tick_params(labelsize=cbfsize)   #font size for the ticks
  
  t = cbar.ax.xaxis.label
  t.set_fontsize(cbfsize)  # font size for the axis title
  
  
  plt.tight_layout()
  savefile = 'images/Equatorial_Slice_temp.png'
  print('Saving figure to: ', savefile)
  plt.savefig(savefile)


def s_plot_Equatorial_Slices_rakesh(dir_name):
  filelist = []
  filelist = os.listdir(dir_name)
  nfile=len(filelist)
  max_step = int(filelist[0])
  lastfile = filelist[0]
  for fname in filelist:
    istep = int(fname)
    if(istep > max_step):
      max_step = istep
      lastfile = fname
  
  plot_each_Equatorial_Slices_rakesh(lastfile, init_time)
  return

if __name__ == '__main__':
  dir_Equatorial_Slices =  'Equatorial_Slices/'
  s_plot_Equatorial_Slices_rakesh(dir_Equatorial_Slices)

