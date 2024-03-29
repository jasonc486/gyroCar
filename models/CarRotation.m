%This script simulates the movement of the car due to torque generated by a
%Written by Calder Leppitsch
%reaction wheel or control moment gyroscope.

g = 9.81;    %m/s^2  acceleration of gravity
m_g = 2;    %kg     mass of gyro/rotation wheel
m_c = 4;    %kg     mass of entire car including gyro
r = 0.05;   %m      radius of gyro/rw
l = 0.15;   %m      distance from rear wheel to center of mass
J_g = 0.5*m_g*r^2;  %kg*m^2     moment of inertia of the gyro/rw
J_c = m_c*l^2;      %kg*m^2     moment of inertia of car about rear wheel
p_c = 100000;   %Pa     brake caliper pressure
A_p = 0.02;     %m^2    brake pad area
mu_k = 0.56;    %       coefficient of kinetic friction between break and flywheel
d_p = 0.015;    %m      distance from center of flywheel to center of break pad
x_com = 0.1; %m     distance from rear wheel to center of mass in x direction
y_com = sqrt(l^2 - x_com^2);
theta_c_i = atan(y_com/x_com);
min_t_gen = m_c*g*x_com;

%Integration variables
dt = 0.001;     %sec
t = 0;

%Input Torque Function
T_gen = mu_k*p_c*A_p*d_p;

%Initialize Integration Results
theta_c = theta_c_i;
omega_c = 0;
alpha_c = 0;

%Numerical Integration Routine
done = 0;
while done ~= 1
    t = [t t(end)+dt];
    if theta_c <= theta_c_i
        alpha_c_n = T_gen;
    else
        alpha_c_n = T_gen-m_c*g*l*cos(theta_c(end));
    end
    alpha_c = [alpha_c alpha_c_n];
    omega_c_n = alpha_c(end)*dt+omega_c(end);
    omega_c = [omega_c omega_c_n];
    theta_c_n = omega_c(end)*dt + theta_c(end);
    theta_c = [theta_c theta_c_n];
    if theta_c(end) >= pi/2
       done = 1; 
    end
end

%Calculate Initial Rotation Speed of Rotation Wheel
t_lift = t(end);
omega_g_i = (T_gen/J_g)*t_lift; %rad/s
start_rpm = omega_g_i*60/(2*pi);
