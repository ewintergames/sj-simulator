import numpy as np
from math_utils import pol2cart, perp, mp


class HillProfile:
    def __init__(self, type, gates, w, h, n, alpha, gamma, e, es, t, r1, betaP, betaK, betaL, s, l1, l2, rL, r2L, r2):
        self.type = type
        self.gates = gates
        self.w = w
        self.h = h
        self.n = n
        self.alpha = np.deg2rad(alpha)
        self.gamma = np.deg2rad(gamma)
        self.e = e
        self.es = es
        self.t = t
        self.r1 = r1
        self.betaP = np.deg2rad(betaP)
        self.betaK = np.deg2rad(betaK)
        self.betaL = np.deg2rad(betaL)
        self.s = s
        self.l1 = l1
        self.l2 = l2
        self.rL = rL
        self.r2L = r2L
        self.r2 = r2
        self.calculate_profile()

    def calculate_profile(self):
        if self.type == 0:
            self.betaP = self.betaL = self.betaK

        self.beta0 = self.betaP / 6
        self.betaU = 0

        E1_t = pol2cart(-self.gamma)
        E1_n = perp(E1_t)
        E2_t = pol2cart(-self.alpha)
        E2_n = perp(E2_t)

        self.E2 = -self.t * E2_t

        if self.type == 2:
            self.i_d = 2 * self.r1 * \
                np.sin(self.gamma - self.alpha) * \
                np.cos(self.gamma - self.alpha)**2
            self.i_c = np.tan(self.gamma - self.alpha) / 3 / self.i_d**2
            self.i_f = np.tan(self.gamma - self.alpha) * self.i_d / 3
            self.l = self.i_d * (1 + 0.1 * np.tan(self.gamma - self.alpha)**2)
            self.E1 = self.E2 - E1_t * self.i_d - E1_n * self.i_f
            self.E1_C = self.E1 + self.i_d / 3 * E1_t
            self.E2_C = self.E2 - self.i_d / 3 / np.dot(E1_t, E2_t) * E2_t
        else:
            self.C1 = self.E2 + E2_n * self.r1
            self.E1 = self.C1 - E1_n * self.r1
            self.l = self.r1 * (self.gamma - self.alpha)

        self.A = self.E1 - E1_t * (self.e - self.l)
        self.B = self.A + E1_t * self.es
        self.T = mp(0, 0)

        self.F = mp(0, -self.s)
        self.K = mp(self.n, -self.h)

        F_t = pol2cart(-self.beta0)
        F_n = perp(F_t)
        P_t = pol2cart(-self.betaP)
        P_n = perp(P_t)
        K_t = pol2cart(-self.betaK)
        K_n = perp(K_t)
        L_t = pol2cart(-self.betaL)
        L_n = perp(L_t)
        U_t = pol2cart(-self.betaU)
        U_n = perp(U_t)

        if self.type == 0:
            self.P = self.K - self.l1 * K_t
            self.L = self.K
        else:
            self.CL = self.K + K_n * self.rL
            self.P = self.CL - P_n * self.rL
            self.L = self.CL - L_n * self.rL

        self.F_C = self.F + (self.P[0] - self.F[0]) / 3 * F_t
        self.P_C = self.P - (self.P[0] - self.F[0]) / 3 * P_t

        self.l_u = -self.P[1] + self.F[1] - self.P[0] * np.tan(self.beta0)
        self.l_v = self.P[0] * (np.tan(self.betaP) - np.tan(self.beta0))

        if self.type == 2:
            self.tau = np.arctan(
                (np.cos(self.betaL) - (self.r2 / self.r2L)**(1/3)) / np.sin(self.betaL))
            self.o_c = 1 / (2 * self.r2 * np.cos(self.tau)**3)
            self.o_a = -np.tan(self.betaL + self.tau) / 2 / self.o_c
            self.o_b = -np.tan(self.tau) / 2 / self.o_c

            self.U = self.L + np.array([self.o_c * np.sin(self.tau) * (self.o_a - self.o_b) + np.cos(self.tau) * (self.o_b - self.o_a),
                                        - self.o_c * np.cos(self.tau) * (self.o_a**2 - self.o_b**2) + np.sin(self.tau) * (self.o_b - self.o_a)])
            self.U_C = self.L + (self.U[1] - self.L[1]) / L_t[1] * L_t
            # print(self.U_C, self.U)
        else:
            self.C2 = self.L + self.r2 * L_n
            self.U = self.C2 - self.r2 * U_n

    def inrun(self, x):
        if x >= self.E2[0]:
            return -x * np.tan(self.alpha)
        elif self.E2[0] > x and x >= self.E1[0]:
            if self.type == 2:
                i_p = 1 / (np.tan(self.gamma) * 3 * self.i_c)
                i_q = (x + self.t * np.cos(self.alpha) + self.i_f * np.sin(self.gamma) +
                       self.i_d * np.cos(self.gamma)) / 2 / self.i_c / np.sin(self.gamma)
                i_ksi = ((i_q**2 + i_p**3)**0.5 + i_q)**(1/3) - \
                    ((i_q**2 + i_p**3)**0.5 - i_q)**(1/3)
                return self.t * np.sin(self.alpha) - self.i_f * np.cos(self.gamma) + self.i_d * np.sin(self.gamma) - i_ksi * np.sin(self.gamma) + self.i_c * i_ksi**3 * np.cos(self.gamma)
            else:
                return -(self.r1**2 - (x - self.C1[0])**2)**0.5 + self.C1[1]
        else:
            return -x * np.tan(self.gamma) + self.A[1] + np.tan(self.gamma) * self.A[0]

    def landing_area(self, x):
        if x <= self.P[0]:
            return self.F[1] - x * np.tan(self.beta0) - (3 * self.l_u - self.l_v) * (x / self.P[0])**2 + (2 * self.l_u - self.l_v) * (x / self.P[0])**3
        elif self.P[0] < x and x <= self.L[0]:
            if self.type == 0:
                return np.tan(self.betaK) * (self.K[0] - x) + self.K[1]
            else:
                return -(self.rL**2 - (x - self.CL[0])**2)**0.5 + self.CL[1]
        else:
            if self.type == 2:
                ksi = (np.cos(self.tau) - (np.cos(self.tau)**2 - 4 * self.o_c *
                                           (x - self.L[0] - self.o_c * self.o_a**2 * np.sin(self.tau) + self.o_a * np.cos(self.tau)) * np.sin(self.tau))**0.5) / 2 / self.o_c / np.sin(self.tau)
                return self.L[1] - self.o_c * np.cos(self.tau) * (self.o_a**2 - ksi**2) - np.sin(self.tau) * (self.o_a - ksi)
            else:
                return -(self.r2**2 - (x - self.C2[0])**2)**0.5 + self.C2[1]

    def get_distance(self, x):
        dst = 1.005 * (x**2 + self.landing_area(x)**2)**0.5
        return np.round(2*dst)/2

    def get_tangent(self, x):
        tan = np.array([1, self.landing_area(
            x + 0.5) - self.landing_area(x - 0.5)])
        return tan / np.linalg.norm(tan)

    def get_normal(self, x):
        tan = self.get_tangent(x)
        return np.array([-tan[1], tan[0]])
