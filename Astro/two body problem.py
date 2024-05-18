#!/usr/bin/env python
# coding: utf-8

# # Jupiter and Sun

# In[23]:


import numpy as np
import matplotlib.pyplot as plt

G = 6.67e-11  #universal gravitational constant

#mass of two bodies
m_sun = 1.9891e30 #kg
m_jupiter = 1.89813e27 #kg

#initial position
r_sun = np.array([0,0,0], dtype = float)[None,:] #2Darray
r_jupiter = np.array([7.7792e11,0,0], dtype = float)[None,:] #5.2AU in m

v_sun = np.array([0,0,0], dtype = float)[None,:]
v_jupiter = np.array([0,12430,0], dtype = float)[None,:] #velocity in m/s

#time parameter
dt = 36000 #1 hour in sec
t = 3.465e8 #1 year of jupiter in sec (total time)

N = t/dt

#to store values of position and velocity over time
r_sun_history = np.zeros((int(N),3))
r_jupiter_history = np.zeros((int(N),3))

#initial values
r_sun_history[0] = r_sun
r_jupiter_history[0] = r_jupiter

for i in range(1, int(N)):
    r = r_jupiter - r_sun #relative position vector
    r_mag = np.linalg.norm(r)
    a_sun = G*m_jupiter*r/r_mag**3 #acc. of sun
    a_jupiter = -G*m_sun*r/r_mag**3 #acc. of jupiter
    
    #velocity incriment over time 
    v_sun += a_sun*dt  
    v_jupiter += a_jupiter*dt
    
    #position incriment over time
    r_sun += v_sun*dt
    r_jupiter += v_jupiter*dt
    
    r_sun_history[i] = r_sun
    r_jupiter_history[i] = r_jupiter
    
#plot
plt.plot(r_jupiter_history[:,0], r_jupiter_history[:,1], label = 'jupiter')
plt.scatter(r_sun_history[:,0], r_sun_history[:,0], s=50, label ='sun' , color = 'yellow')
plt.xlabel('x(m)')
plt.ylabel('y(m)')
plt.title('jupiter orbit around sun')
plt.xlim(-8e11,8e11)
plt.ylim(-8e11,8e11)
plt.legend()
plt.show()






# In[24]:


# Calculate eccentricity
r_distances = np.linalg.norm(r_jupiter_history - r_sun_history, axis=1)  # Distances from Sun at each time step
r_perihelion = np.min(r_distances)
r_aphelion = np.max(r_distances)
r_semimajor = (r_perihelion + r_aphelion) / 2
eccentricity = (r_aphelion - r_perihelion) / (2 * r_semimajor)

print("Eccentricity of Earth's orbit:", eccentricity)


# In[ ]:



