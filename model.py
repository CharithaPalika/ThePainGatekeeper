import numpy as np
from scipy.integrate import odeint
# def gate_control(variables, t, params):
#     S, T, P = variables # slow pain, Touch stimulus, Pain total

#     # parameters
#     alpha_S = params['alpha_S']  # rate of slow pain input
#     beta_S = params['beta_S']    # rate of slow pain decay
#     input_S = params['input_S']  # slow pain input level at given time t
#     alpha_T = params['alpha_T']  # rate of touch stimulus input
#     beta_T = params['beta_T']    # rate of touch stimulus decay
#     input_T = params['input_T']  # touch stimulus input level at given time t
#     alpha_SP = params['alpha_SP']  # rate of slow pain contribution to total pain
#     alpha_TP = params['alpha_TP']  # rate of touch stimulus contribution to
#     # total pain
#     beta_P = params['beta_P']    # rate of total pain decay
#     gamma_T = params['gamma_T']  # threshold for touch stimulus to contribute to pain

#     # Slow pain dynamics
#     dSdt = alpha_S * input_S(t) - beta_S * S

#     # Touch stimulus dynamics
#     dTdt = alpha_T * input_T(t) - beta_T * T

#     # Total perception of pain
#     dPdt = alpha_SP * S - alpha_TP * np.maximum(0, T - gamma_T) - beta_P * P

#     if S <= 0 and dSdt < 0:
#         dSdt = 0
#     if T <= 0 and dTdt < 0:
#         dTdt = 0
#     if P <= 0 and dPdt < 0: # This is the crucial one for P
#         dPdt = 0

#     return [dSdt, dTdt, dPdt]

# def Slowpain_input(t):
#     if t > 10 and t < 25:
#         return 1.0
#     return 0.0

# def Touch_input(t):
#     if t > 14 and t < 18:
#         return 4.0
#     if t > 20 and t < 24:
#         return 4.0
#     return 0.0

# def get_default_params():
#     return {
#         'alpha_S': 0.8,
#         'beta_S': 0.3,
#         'alpha_T': 2.0,
#         'beta_T': 1.5,
#         'alpha_SP': 0.5,
#         'alpha_TP': 0.5,
#         'gamma_T': 1.0,
#         'beta_P': 0.1,
#         'input_S': Slowpain_input,
#         'input_T': Touch_input
#     }

class GateControl:
    def __init__(self, params = None, tactile_stimulus = True):

        # loading params
        if params is None:
            self.model_params = self.get_default_params()
        else:
            self.model_params = params
        
        # Defining the initial conditions
        self.initial_conditions = [0.0, 0.0, 0.0] 
        
        # Defining time for simulation
        t_start = 0
        t_end = 40
        num_points = 100
        self.time_points = np.linspace(t_start, t_end, num_points)

        if tactile_stimulus:
            self.model_params['input_S'] = self.get_slow_pain_input # Input function for slow pain stimulus
            self.model_params['input_T'] =self.get_tactile_input # Input function for touch stimulus
        else:
            self.model_params['input_S'] = self.get_slow_pain_input # Input function for slow pain stimulus
            self.model_params['input_T'] =lambda x: 0 # Input function for touch stimulus


    def model_ODE(self, variables, t, params):
        S, T, P = variables # slow pain, Touch stimulus, Pain total

        # parameters
        alpha_S = params['alpha_S']  # rate of slow pain input
        beta_S = params['beta_S']    # rate of slow pain decay
        input_S = params['input_S']  # slow pain input level at given time t
        alpha_T = params['alpha_T']  # rate of touch stimulus input
        beta_T = params['beta_T']    # rate of touch stimulus decay
        input_T = params['input_T']  # touch stimulus input level at given time t
        alpha_SP = params['alpha_SP']  # rate of slow pain contribution to total pain
        alpha_TP = params['alpha_TP']  # rate of touch stimulus contribution to
        # total pain
        beta_P = params['beta_P']    # rate of total pain decay
        gamma_T = params['gamma_T']  # threshold for touch stimulus to contribute to pain

        # Slow pain dynamics
        dSdt = alpha_S * input_S(t) - beta_S * S

        # Touch stimulus dynamics
        dTdt = alpha_T * input_T(t) - beta_T * T

        # Total perception of pain
        dPdt = alpha_SP * S - alpha_TP * np.maximum(0, T - gamma_T) - beta_P * P

        if S <= 0 and dSdt < 0:
            dSdt = 0
        if T <= 0 and dTdt < 0:
            dTdt = 0
        if P <= 0 and dPdt < 0: 
            dPdt = 0

        return [dSdt, dTdt, dPdt]

    def get_default_params(self):
        return {
                'alpha_S': 0.8,
                'beta_S': 0.3,
                'alpha_T': 2.0,
                'beta_T': 1.5,
                'alpha_SP': 0.5,
                'alpha_TP': 0.5,
                'gamma_T': 1.0,
                'beta_P': 0.1,
                }
    
    def get_slow_pain_input(self, t):
        # Applies slow pain between 10-25 min
        if t > 10 and t < 25:
            return 1.0
        return 0.0
    
    def get_tactile_input(self, t):
        if t > 14 and t < 18:
            return 4.0
        if t > 20 and t < 24:
            return 4.0
        return 0.0

    def simulate_ODE(self):
        solution = odeint(self.model_ODE, self.initial_conditions, self.time_points, args=(self.model_params,))
        S, T, P = solution.T
        return S, T, P
    