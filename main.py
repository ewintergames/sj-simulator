import numpy as np
from math_utils import pol2cart, perp, mp


angles = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20,
          22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44]
kw_pts = [[0.00185, 0.00204, 0.00223, 0.00243, 0.00261, 0.00281, 0.00301, 0.00319,
           0.00338, 0.00355, 0.00372, 0.00388, 0.00403, 0.00418, 0.00432, 0.00447,
           0.00462, 0.00479, 0.00502, 0.00537, 0.00614, 0.00691, 0.00767],
          [0.00232, 0.00245, 0.00258, 0.00272, 0.00285, 0.00298, 0.00311, 0.00325,
           0.00337, 0.00350, 0.00362, 0.00374, 0.00386, 0.00398, 0.00410, 0.00422,
           0.00436, 0.00453, 0.00474, 0.00504, 0.00553, 0.00602, 0.00651],
          [0.00261, 0.00271, 0.00282, 0.00293, 0.00304, 0.00315, 0.00326, 0.00337,
           0.00347, 0.00357, 0.00367, 0.00376, 0.00386, 0.00396, 0.00407, 0.00419,
           0.00432, 0.00449, 0.00471, 0.00503, 0.00555, 0.00606, 0.00658]]

ka_pts = [[0.00093, 0.00139, 0.00185, 0.00231, 0.00275, 0.00316, 0.00354, 0.00390,
           0.00424, 0.00455, 0.00484, 0.00511, 0.00534, 0.00555, 0.00574, 0.00591,
           0.00605, 0.00617, 0.00628, 0.00638, 0.00655, 0.00672, 0.00689],
          [0.00116, 0.00180, 0.00244, 0.00308, 0.00365, 0.00396, 0.00424, 0.00450,
           0.00472, 0.00492, 0.00508, 0.00522, 0.00534, 0.00543, 0.00550, 0.00555,
           0.00560, 0.00565, 0.00571, 0.00582, 0.00606, 0.00629, 0.00652],
          [0.00130, 0.00177, 0.00224, 0.00270, 0.00316, 0.00350, 0.00382, 0.00411,
           0.00436, 0.00459, 0.00479, 0.00496, 0.00510, 0.00521, 0.00531, 0.00538,
           0.00545, 0.00551, 0.00558, 0.00569, 0.00590, 0.00611, 0.00632]]

kw = [np.poly1d(np.polyfit(angles, kw_pt, 4)) for kw_pt in kw_pts]
ka = [np.poly1d(np.polyfit(angles, ka_pt, 4)) for ka_pt in ka_pts]


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
        self.T = mp(0,0)

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
            print(self.U_C, self.U)
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