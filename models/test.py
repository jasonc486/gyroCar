# Written by Eunkyu Kim
from sympy import *
import matplotlib.pyplot as plt

#Functions for skew-symmetric matrices and rotation matrices

def skew(a):
	return Matrix([
		[0, -a[2], a[1]],
		[a[2], 0, -a[0]],
		[-a[1],a[0],0]])

def unskew(a):
	return Matrix([
		[a[2,1]],
		[a[0,2]],
		[a[1,0]]])

def rot1(t):
	return Matrix([
		[1, 0, 0],
		[0, cos(t), -sin(t)],
		[0, sin(t), cos(t)]])

def rot2(t):
	return Matrix([
		[cos(t), 0, sin(t)],
		[0, 1, 0],
		[-sin(t), 0, cos(t)]])

def rot3(t):
	return Matrix([
		[cos(t), -sin(t), 0],
		[sin(t), cos(t), 0],
		[0, 0, 1]])

def diagonal(a):
	return Matrix([
		[a[0], 0, 0],
		[0, a[1], 0],
		[0, 0, a[2]]])

#Defining variables
t = symbols('t')
J1, J2, J3 = symbols('J1 J2 J3')
p, q, r = symbols('p q r')
psi = Function('psi')(t)
theta = Function('theta')(t)
phi = Function('phi')(t)
psidot = diff(psi,t)
thetadot = diff(theta,t)
phidot = diff(phi,t)
eulerrates = [phidot, thetadot, psidot]

#Formulating Rotation Matrices
R01 = rot3(phi)
R12 = rot1(theta)
R23 = rot3(psi)
R = R01*R12*R23
R03 = simplify(R)


#Angular Velocity
Omega03 = simplify(R03.T * diff(R03,t)) #skew symmetric matrix 3x3
omega03 = unskew(Omega03) #angular velocity matrix 3x1

#Mass moment of inertia
J = [J1, J2, J3]
Jc = diagonal(J)

#Calculating A matrix for A*euler_rates = angular velocity
A= zeros(3,3)
for i, angledot in enumerate(eulerrates):
	for j in range(3):
		A[j,i] = omega03[j].coeff(angledot)

detA = simplify(det(A))
invA = simplify(A.inv())


Hdot = simplify(Omega03*Jc*omega03+Jc*diff(omega03,t).subs(psi,0))
print(Hdot)
