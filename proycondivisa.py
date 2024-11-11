import numpy as np
# Desviaciones estándar
sigma_dol = 0.004799804762366855
sigma_rem = 0.006405851857157807

# Definir el estado inicial
def Starting_State():
    s1 = 1  # Día inicial
    s2 = 100  # Capital inicial en la divisa
    divisa = 'D'  # Divisa inicial (Dólar)
    s = (s1, s2, divisa)
    return s

# Definir conjunto de acciones
def Action_Set(s):
    (s1, s2, divisa) = s
    if s2 == 0:  # Si no hay dinero, no se puede tomar acción
        AS = ['myself']
    else:  # Acciones disponibles: Mantener (M) o Cambiar de divisa (C)
        AS = ['M', 'C']
    return AS

# Conjunto de eventos basado en el comportamiento de la divisa
def Event_Set(s, a):
    ES = ['S', 'B']  # Eventos posibles: "Sube" (S) o "Baja" (B)
    return ES

# Ecuaciones de transición para el estado
def Transition_Equations(s, a, e, sigma_dol, sigma_rem):
    (s1, s2, divisa) = s
    sn1 = s1 + 1  # Avanzar al siguiente día

    # Determinar la sigma actual basada en la divisa
    sigma = sigma_dol if divisa == 'D' else sigma_rem

    # Ajuste de capital en función de la acción y el evento
    if a == 'M':  # Mantener
        sn2 = s2 * (1 + sigma) if e == 'S' else s2 * (1 - sigma)
    elif a == 'C':  # Cambiar de divisa con comisión del 1%
        sn2 = s2 * 0.99
        sn2 = sn2 * (1 + sigma) if e == 'S' else sn2 * (1 - sigma)
        # Cambiar la divisa
        divisa = 'R' if divisa == 'D' else 'D'

    sn = (sn1, round(sn2, 4), divisa)  # Redondear a 4 decimales
    return sn

# Restricciones (horizonte de planeación de 3 días)
def Constraints(s, a, sn, L):
    (s1, s2, divisa) = s
    ct = (s1 <= 3)
    return ct  # Restringe el análisis a 3 días

# Probabilidades de transición basadas en las matrices de transición
def Transition_Probabilities(s, a, e, prob_matrix):
    """
    Calcula la probabilidad de transición con base en la matriz de transición de la divisa actual.
    """
    if e == 'S' and a == 'M':
        return prob_matrix['Sube']['Sube']
    elif e == 'B' and a == 'M':
        return prob_matrix['Sube']['Baja']
    elif e == 'S' and a == 'C':
        return prob_matrix['Baja']['Sube']
    elif e == 'B' and a == 'C':
        return prob_matrix['Baja']['Baja']

# Contribución de la acción (1% de comisión al cambiar de divisa)
def Action_Contribution(s, a):
    return -0.01 * s[1] if a == 'C' else 0

# Contribución del evento basado en sigma
def Event_Contribution(s, e, sigma_dol, sigma_rem):
    (s1, s2, divisa) = s
    sigma = sigma_dol if divisa == 'D' else sigma_rem
    if e == 'S':
        ce = s2 * sigma  # Ganancia si el evento es "Sube"
    else:
        ce = -s2 * sigma  # Pérdida si el evento es "Baja"
    return ce

# Función de calidad Q(s, a)
def Quality_Function(m, p, ca, ce, V_sn):
    Q_s_a = ca + sum(p[i] * (ce[i] + V_sn[i]) for i in range(0, m))
    return Q_s_a

# Función de valor óptimo V(s)
def Optimal_Value_Function(Q_s_a):
    V_s = min(Q_s_a)
    return V_s

# Condición de contorno (valor final al término del horizonte de planificación)
def Boundary_Condition(s):
    (s1, s2, divisa) = s
    if s1 == 4:  # Si estamos en el último día del horizonte de planificación
        V_s = s2  # Tomamos el valor final de la divisa
    else:
        V_s = 0
    return V_s
