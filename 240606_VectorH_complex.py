# In[1]:

from matplotlib import *
from pylab import *
from numpy import *
from pyspecdata import *

# Provide file names, start making figlist

filename1 = 'VectorH_240606_fixed.fld' #90 deg phase
filename2 = 'VectorH_240523.fld' #0 deg phase
fl = figlist_var()

# Define how axes are constructed based on which dimension fields are plotted on, pop() to remove irrelevant dimension

def construct_axes_from_positions(positions):
    #{{{ construct the axes
    list_of_axes = [unique(positions[:,j]) for j in range(0,3)]
    list_of_indeces = [0,1,2]
    for j in range(0,len(list_of_axes)):
        if len(list_of_axes[j]) == 1:
            list_of_axes.pop(j)
            list_of_indeces.pop(j)
            break
    [u_axis,v_axis] = list_of_axes
    [u_index,v_index] = list_of_indeces
    return u_index,v_index,u_axis,v_axis
    #}}}

# Defines how a vector file is opened, read, enumerated to individual values, and NAN separated from #s

def load_hfss_vectors(filename,show_valid = True):
    fp = open(filename,'r')
    data = fp.readlines()
    fp.close()
    header = data[0:2]
    print("the second line tells me what's in the file -- x,y,z, followed by the 3 positions of vector data and the final part tells me what it is")
    print('header is',r'\begin{verbatim}', header, r'\end{verbatim}')
    data = data[2:]
    positions = empty((len(data),3),dtype = 'double')
    vec_vals = empty((len(data),3),dtype = 'double')
    for j,line in enumerate(data):
        vals = [double(x) for x in line.strip().split(" ") if len(x)>0]
        positions[j,:] = vals[0:3]
        vec_vals[j,:] = vals[3:]
    u_index,v_index,u_axis,v_axis = construct_axes_from_positions(positions)
    #{{{ show the datapoints and which are valid
    if show_valid:
        fl.next('show valid values')
        thismask = isnan(vec_vals[:,u_index])
        print("invalid/valid",sum(thismask), sum(~thismask))
        fl.plot(positions[:,u_index][thismask],positions[:,v_index][thismask],'r.')
        fl.plot(positions[:,u_index][~thismask],positions[:,v_index][~thismask],'b.') # '~' = 'not'
        xlabel('u')
        ylabel('v')
        gca().set_aspect('equal', 'datalim')
    #}}}
    data = empty((len(u_axis),len(v_axis),3),dtype = 'double')
    for j in range(0,positions.shape[0]):
        u_i = where(u_axis == positions[j,u_index])[0][0]
        v_i = where(v_axis == positions[j,v_index])[0][0]
        data[u_i,v_i,:] = vec_vals[j,:]
    return u_index,u_axis,v_index,v_axis,data

# Test out function, see where there are field values and NAN for first file

load_hfss_vectors(filename1, show_valid = True)

# Use function to show valid field values for file 1

u_index, u_axis, v_index, v_axis, data1 = load_hfss_vectors(filename1, show_valid = True)
print(shape(data1))

# Same as above for file 2

u_index, u_axis, v_index, v_axis, data2 = load_hfss_vectors(filename2, show_valid = True)
print(shape(data2))

# In[2]:


# In[3]:

# first, let's do this with raw matplotlib
for j in range(3):
    figure(j+1)
    data2[:,:,j] = 1j*data2[:,:,j]
    print(shape(data2))
    data_c = data1 + data2
    imshow(data_c[:,:,j])

# In[4]:


# In[5]:

# I could manually set the "extent" kwarg of imshow, but I'm going to load this as an nddata
# to get a plot with coordinates
axis_names = ['x','y','z']
for j in range(3):
    figure(j+1)
    d1 = nddata(data1[:,:,j], data1.shape[:2], [axis_names[u_index], axis_names[v_index]]).setaxis(
        axis_names[u_index], u_axis).setaxis(axis_names[v_index], v_axis)
    data2[:,:,j] = 1j*data2[:,:,j]
    d2 = nddata(data2[:,:,j], data2.shape[:2], [axis_names[u_index], axis_names[v_index]]).setaxis(
        axis_names[u_index], u_axis).setaxis(axis_names[v_index], v_axis)
    d_c = d1+d2
    fl.image(d_c)
fl.show()
# In[6]:


# In[7]:


# In[8]:


# In[9]:


# In[10]:


