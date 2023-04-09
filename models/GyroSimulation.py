#This code was written by Calder Leppitsch for ME363 Independent Study, taught by Professor Dirk Luchtenburg.
#This work is in collaboration with Benjamin Meiner, Eunkyu Kim, Daniel Zaretsky, Jason Chen.

#This code simulates the motion of a single-axis gimbal and gyroscope using moving frames of reference
#The goal is to generate output torque in desired directions

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#Initial Orientation Matrices for all frames
e0 = np.array([[1.,0.,0.],  #Inertial Frame
               [0.,1.,0.],
               [0.,0.,1.]])
e1 = e0 #Gimbal Frame
e2 = e0 #Gyroscope / Flywheel Frame
#The matrix is made up of three direction vectors [ex1 , ex2 , ex3].
#The matrices rotate over time with each component being represented in the inertial frame.

#Moment of intertia matrix in the 2 frame
#Assuming it is a thin disk of uniform density
m = 10.0 #kg, mass of flywheel
r = 0.5 #m, radius of flywheel
J_spin = 0.5*m*r**2
J2 = np.array([[0.25*m*r**2, 0, 0],
               [0, 0.25*m*r**2, 0],
               [0, 0, 0.5*m*r**2]])

#Time Scale of Integration
ts = 0.01
t_start = 0.0
t_end = 6.0
n = np.int((t_end-t_start)/ts)+1
t = np.linspace(t_start,t_end,n)

#Rotation Velocity Functions
#Constant Velocity Functions
theta_dot = 2. #rad/s
phi_dot = 3. #rad/s

#Non-constant velocity function (only for theta)
vel_curve = np.zeros(314)
curve1_t_end = 0.52
curve2_t_end = 2.62
curve3_t_end = 3.14
n1 = np.int((curve1_t_end/ts))
for i in range(0,n1):
    vel_curve[i] = 3.2597*t[i]
n2 = np.int(((curve2_t_end-curve1_t_end)/ts))
for i in range(0,n2):
    vel_curve[i+n1] = 0.8534/(np.sin(t[i+n1]))
n3 = np.int(((curve3_t_end-curve2_t_end)/ts))
for i in range(0,n3):
    vel_curve[i+n2+n1] = -3.2597*(t[i+n2+n1]-np.pi)
theta_vel = np.array([])
theta_vel = np.append(theta_vel,vel_curve[157:314])
theta_vel = np.append(theta_vel,vel_curve)
theta_vel = np.append(theta_vel,vel_curve)

#Rotation of the gimbal about the vertical e11
#A1: Constant Theta Dot
#theta = theta_dot*t
#A2: Non-Constant Theta Dot
theta = np.zeros(n)
for i in range(0,n-1):
    theta[i+1] = theta[i]+theta_vel[i]*ts
    
#Rotation of the gyro about the horizontal e23
phi = phi_dot*t

#Rotation Vectors
omega_gimbal = np.array([[theta_dot],[0.],[0.]])
omega_gyro = np.array([[0.],[0.],[phi_dot]])

#Initialize Momentum Vector
H01 = np.array([])
H02 = np.array([])
H03 = np.array([])

#Initialize Torque Vector
T01 = np.array([])
T02 = np.array([])
T03 = np.array([])

#Find desired values at every time step
for i in range(0,n):
    #Calculate the rotation matrices
    R01 = np.array([[1., 0., 0.],
                    [0., np.cos(theta[i]), np.sin(theta[i])],
                    [0., -np.sin(theta[i]), np.cos(theta[i])]])
    R12 = np.array([[np.cos(phi[i]), np.sin(phi[i]), 0.],
                    [-np.sin(phi[i]), np.cos(phi[i]), 0.],
                    [0., 0., 1.]])
    e1 = e0 @ R01
    e2 = e1 @ R12
    J1 = R12 @ J2 @ np.transpose(R12)
    J0 = R01 @ J1 @ np.transpose(R01)
    omega_0 = e1 @ omega_gimbal + e2 @ omega_gyro
    #Calculate the momentum in the inertial frame
    Hstep = J0 @ omega_0
    H01 = np.append(H01, Hstep[0])
    H02 = np.append(H02, Hstep[1])
    H03 = np.append(H03, Hstep[2])
    #Calculate the torque generated
    #B1: Single Gyroscope & Gimbal
    # rot = np.array([0., np.cos(theta[i]), np.sin(theta[i])])
    #B2: Dual Gyroscope and & Gimbal with cancelling phase
    rot = np.array([0., 2*np.cos(theta[i]), 0.])
    #A1: Constant Theta Dot
    #Tstep = -1*J_spin*theta_dot*phi_dot*rot
    #A2: Non-Constant Theta Dot
    Tstep = -1*J_spin*theta_vel[i]*phi_dot*rot
    T01 = np.append(T01, Tstep[0])
    T02 = np.append(T02, Tstep[1])
    T03 = np.append(T03, Tstep[2])

plt.close()
plt.figure()
plt.plot(t,H01,label='e1 direction')
plt.plot(t,H02,label='e2 direction')
plt.plot(t,H03,label='e3 direction')
plt.legend()
plt.title('Momentum in Inertial Frame')
plt.xlabel('Time (sec)')
plt.ylabel('Momentum (kg*m^2/s)')

plt.figure()
plt.plot(t,T01,label='e1 direction')
plt.plot(t,T02,label='e2 direction')
plt.plot(t,T03,label='e3 direction')
plt.legend()
plt.title('Torque in Inertial Frame')
plt.xlabel('Time (sec)')
plt.ylabel('Torque (kg*m^2/s^2)')





