"""
Python model 'New EPI Aedes Months.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.statefuls import Integ
from pysd.py_backend.external import ExtData
from pysd import Component

__pysd_version__ = "3.14.3"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 611,
    "time_step": lambda: 0.0625,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP",
    units="Month",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="Additional Ae mortality",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_ae": 1, "suppression_factor": 1, "suppression_month_value": 1},
)
def additional_ae_mortality():
    return adult_ae() * suppression_factor() * suppression_month_value()


@component.add(
    name="H D Infections",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"susceptible_humans": 1, "force_of_infection_h_dengue": 1},
)
def h_d_infections():
    return susceptible_humans() * force_of_infection_h_dengue()


@component.add(
    name="H Deaths",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"susceptible_humans": 1, "life_expectancy": 1},
)
def h_deaths():
    return susceptible_humans() / life_expectancy()


@component.add(
    name="H YF Infections",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"susceptible_humans": 1, "force_of_infection_h_yellowfever": 1},
)
def h_yf_infections():
    return susceptible_humans() * force_of_infection_h_yellowfever()


@component.add(
    name="D Reproduction Number Ae",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_ae": 1,
        "human_feeding_fraction_ae": 1,
        "transmission_prob_d_h_to_m_ae": 1,
        "transmission_prob_d_m_to_h_ae": 1,
        "total_adult_ae": 1,
        "human_population_1": 1,
        "adult_mortality_rate_ae": 2,
        "eip_d_ae": 1,
        "recovery_rate_h": 1,
    },
)
def d_reproduction_number_ae():
    return (
        biting_rate_ae() ** 2
        * human_feeding_fraction_ae()
        * transmission_prob_d_h_to_m_ae()
        * transmission_prob_d_m_to_h_ae()
        * (total_adult_ae() / human_population_1())
        * float(np.exp(-adult_mortality_rate_ae() * eip_d_ae()))
        / (adult_mortality_rate_ae() * recovery_rate_h())
    )


@component.add(
    name="D Reproduction Number Albo",
    units="1/Aedes",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_albo": 1,
        "human_feeding_fraction_albo": 1,
        "transmission_prob_d_h_to_m_albo": 1,
        "transmission_prob_d_m_to_h_albo": 1,
        "human_population_1": 1,
        "total_adult_albo": 1,
        "adult_mortality_rate_albo": 2,
        "eip_d_albo": 1,
        "recovery_rate_h": 1,
    },
)
def d_reproduction_number_albo():
    return (
        biting_rate_albo() ** 2
        * human_feeding_fraction_albo()
        * transmission_prob_d_h_to_m_albo()
        * transmission_prob_d_m_to_h_albo()
        * (total_adult_albo() / human_population_1())
        * float(np.exp(-adult_mortality_rate_albo() * eip_d_albo()))
        / (adult_mortality_rate_albo() * recovery_rate_h())
    )


@component.add(
    name="Dengue become Infectious Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_dengue_ae": 1, "eip_d_ae": 1},
)
def dengue_become_infectious_ae():
    return exposed_dengue_ae() / eip_d_ae()


@component.add(
    name="Dengue become Infectious Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_dengue_albo": 1, "eip_d_albo": 1},
)
def dengue_become_infectious_albo():
    return exposed_dengue_albo() / eip_d_albo()


@component.add(
    name="Human feeding fraction ae",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def human_feeding_fraction_ae():
    return 0.9 / 30


@component.add(
    name="Human feeding fraction albo",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def human_feeding_fraction_albo():
    return 0.6 / 30


@component.add(
    name="Adult Mortality rate ae",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_life_ae": 1},
)
def adult_mortality_rate_ae():
    return 1 / adult_life_ae()


@component.add(
    name="Adult Mortality rate ae Chi",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_life_ae": 1},
)
def adult_mortality_rate_ae_chi():
    return 1 / adult_life_ae()


@component.add(
    name="Adult Mortality rate ae YF",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_life_ae": 1},
)
def adult_mortality_rate_ae_yf():
    return 1 / adult_life_ae()


@component.add(
    name="Adult Mortality rate albo",
    units="1/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_life_albo": 1},
)
def adult_mortality_rate_albo():
    return 1 / adult_life_albo()


@component.add(
    name="Adult Mortality rate albo Chi",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_life_albo": 1},
)
def adult_mortality_rate_albo_chi():
    return 1 / adult_life_albo()


@component.add(
    name="Adult Mortality rate albo YF",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_life_albo": 1},
)
def adult_mortality_rate_albo_yf():
    return 1 / adult_life_albo()


@component.add(
    name="Aedes infections Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_d_mosq_ae": 1, "susceptible_ae": 1},
)
def aedes_infections_ae():
    return foi_d_mosq_ae() * susceptible_ae()


@component.add(
    name="Aedes infections Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_d_mosq_albo": 1, "susceptible_albo": 1},
)
def aedes_infections_albo():
    return foi_d_mosq_albo() * susceptible_albo()


@component.add(
    name="Transmission potential ae",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "adult_ae": 1,
        "biting_rate_ae": 1,
        "human_feeding_fraction_ae": 1,
        "vector_competence_ae": 1,
    },
)
def transmission_potential_ae():
    return (
        adult_ae()
        * biting_rate_ae()
        * human_feeding_fraction_ae()
        * vector_competence_ae()
    )


@component.add(
    name="EIP Chi Ae",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temperature_suitability_ae": 1},
)
def eip_chi_ae():
    return (5 / temperature_suitability_ae()) / 30


@component.add(
    name="EIP Chi Albo",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temp_suitability_albo": 1},
)
def eip_chi_albo():
    return (6 / temp_suitability_albo()) / 30


@component.add(
    name="Birth rate", units="1/Month", comp_type="Constant", comp_subtype="Normal"
)
def birth_rate():
    return 0.00456


@component.add(
    name="Biting rate ae",
    units="1/Aedes/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biting_rate_ae():
    return 0.5 / 30


@component.add(
    name="Biting rate albo",
    units="1/(Aedes*Month)",
    comp_type="Constant",
    comp_subtype="Normal",
)
def biting_rate_albo():
    return 0.4 / 30


@component.add(
    name='"Mortality E-C Ae"',
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_chikungunya_ae": 1, "adult_life_ae": 1},
)
def mortality_ec_ae():
    return exposed_chikungunya_ae() / adult_life_ae()


@component.add(
    name='"Mortality E-C Albo 0"',
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_chikungunya_albo": 1, "adult_life_albo": 1},
)
def mortality_ec_albo_0():
    return exposed_chikungunya_albo() / adult_life_albo()


@component.add(
    name="Chi Infectious period",
    units="Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def chi_infectious_period():
    return 7 / 30


@component.add(
    name="Chi Recovery rate",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"chikungunya_infectious_human": 1, "chi_infectious_period": 1},
)
def chi_recovery_rate():
    return chikungunya_infectious_human() / chi_infectious_period()


@component.add(
    name="Chi Recovery rate H",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"chi_infectious_period": 1},
)
def chi_recovery_rate_h():
    return 1 / chi_infectious_period()


@component.add(
    name="Chi Reproduction Number Ae",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_ae": 1,
        "human_feeding_fraction_ae": 1,
        "transmission_prob_chik_h_to_m_ae": 1,
        "transmission_prob_chi_m_to_h_ae": 1,
        "total_adult_ae": 1,
        "human_population_1": 1,
        "eip_chi_ae": 1,
        "adult_mortality_rate_ae_chi": 2,
        "chi_recovery_rate_h": 1,
    },
)
def chi_reproduction_number_ae():
    return (
        biting_rate_ae() ** 2
        * human_feeding_fraction_ae()
        * transmission_prob_chik_h_to_m_ae()
        * transmission_prob_chi_m_to_h_ae()
        * (total_adult_ae() / human_population_1())
        * float(np.exp(-adult_mortality_rate_ae_chi() * eip_chi_ae()))
        / (adult_mortality_rate_ae_chi() * chi_recovery_rate_h())
    )


@component.add(
    name="Chi Reproduction Number Albo",
    units="1/Aedes",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_albo": 1,
        "human_feeding_fraction_albo": 1,
        "transmission_prob_chik_h_to_m_albo": 1,
        "transmission_prob_chi_m_to_h_albo": 1,
        "human_population_1": 1,
        "total_adult_albo": 1,
        "adult_mortality_rate_albo_chi": 2,
        "eip_chi_albo": 1,
        "chi_recovery_rate_h": 1,
    },
)
def chi_reproduction_number_albo():
    return (
        biting_rate_albo() ** 2
        * human_feeding_fraction_albo()
        * transmission_prob_chik_h_to_m_albo()
        * transmission_prob_chi_m_to_h_albo()
        * (total_adult_albo() / human_population_1())
        * float(np.exp(-adult_mortality_rate_albo_chi() * eip_chi_albo()))
        / (adult_mortality_rate_albo_chi() * chi_recovery_rate_h())
    )


@component.add(
    name="Chik Force of infection Mosquito",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_chik_mosq_ae": 1, "foi_chik_mosq_albo": 1},
)
def chik_force_of_infection_mosquito():
    return foi_chik_mosq_ae() + foi_chik_mosq_albo()


@component.add(
    name="Chik Infectious Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_chik_mosq_ae": 1, "susceptible_ae": 1},
)
def chik_infectious_ae():
    return foi_chik_mosq_ae() * susceptible_ae()


@component.add(
    name="Chik Infectious Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_chik_mosq_albo": 1, "susceptible_albo": 1},
)
def chik_infectious_albo():
    return foi_chik_mosq_albo() * susceptible_albo()


@component.add(
    name="Chik Prog to Infectious",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"chikungunya_exposed_humans": 1, "chiku_human_incubation_period": 1},
)
def chik_prog_to_infectious():
    return chikungunya_exposed_humans() / chiku_human_incubation_period()


@component.add(
    name="Chiku Human incubation period",
    units="Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def chiku_human_incubation_period():
    return 5 / 30


@component.add(
    name="Chikungunya become Infectious Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_chikungunya_ae": 1, "eip_chi_ae": 1},
)
def chikungunya_become_infectious_ae():
    return exposed_chikungunya_ae() / eip_chi_ae()


@component.add(
    name="Chikungunya become Infectious Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_chikungunya_albo": 1, "eip_chi_albo": 1},
)
def chikungunya_become_infectious_albo():
    return exposed_chikungunya_albo() / eip_chi_albo()


@component.add(
    name="Chikungunya Exposed Humans",
    units="People",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_chikungunya_exposed_humans": 1},
    other_deps={
        "_integ_chikungunya_exposed_humans": {
            "initial": {},
            "step": {"h_chi_infections": 1, "chik_prog_to_infectious": 1},
        }
    },
)
def chikungunya_exposed_humans():
    return _integ_chikungunya_exposed_humans()


_integ_chikungunya_exposed_humans = Integ(
    lambda: h_chi_infections() - chik_prog_to_infectious(),
    lambda: 0,
    "_integ_chikungunya_exposed_humans",
)


@component.add(
    name="Chikungunya Infectious Human",
    units="People",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_chikungunya_infectious_human": 1},
    other_deps={
        "_integ_chikungunya_infectious_human": {
            "initial": {},
            "step": {"chik_prog_to_infectious": 1, "chi_recovery_rate": 1},
        }
    },
)
def chikungunya_infectious_human():
    return _integ_chikungunya_infectious_human()


_integ_chikungunya_infectious_human = Integ(
    lambda: chik_prog_to_infectious() - chi_recovery_rate(),
    lambda: 0,
    "_integ_chikungunya_infectious_human",
)


@component.add(
    name="Chikungunya Recovered Humans",
    units="People",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_chikungunya_recovered_humans": 1},
    other_deps={
        "_integ_chikungunya_recovered_humans": {
            "initial": {},
            "step": {"chi_recovery_rate": 1},
        }
    },
)
def chikungunya_recovered_humans():
    return _integ_chikungunya_recovered_humans()


_integ_chikungunya_recovered_humans = Integ(
    lambda: chi_recovery_rate(), lambda: 0, "_integ_chikungunya_recovered_humans"
)


@component.add(
    name='"Chikungunya Reproduction Number(R0)"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"chi_reproduction_number_ae": 1, "chi_reproduction_number_albo": 1},
)
def chikungunya_reproduction_numberr0():
    return chi_reproduction_number_ae() + chi_reproduction_number_albo()


@component.add(
    name="FoI YF Mosq albo",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_albo": 1,
        "human_feeding_fraction_albo": 1,
        "transmission_prob_yf_h_to_m_albo": 1,
        "yellowfever_infectious_human": 1,
        "human_population_1": 1,
    },
)
def foi_yf_mosq_albo():
    return (
        biting_rate_albo()
        * human_feeding_fraction_albo()
        * transmission_prob_yf_h_to_m_albo()
        * (yellowfever_infectious_human() / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="Force of infection H CHikungunya",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_h_ae_d": 1, "foi_h_albo_d": 1},
)
def force_of_infection_h_chikungunya():
    return foi_h_ae_d() + foi_h_albo_d()


@component.add(
    name="Force of infection H Dengue",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_h_ae": 1, "foi_h_albo": 1},
)
def force_of_infection_h_dengue():
    return foi_h_ae() + foi_h_albo()


@component.add(
    name="D Force of infection Mosquito",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_d_mosq_ae": 1, "foi_d_mosq_albo": 1},
)
def d_force_of_infection_mosquito():
    return foi_d_mosq_ae() + foi_d_mosq_albo()


@component.add(
    name="D Infectious period",
    units="Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def d_infectious_period():
    return 7 / 30


@component.add(
    name="D Prog to Infectious",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dengue_exposed_humans": 1, "dengue_human_incubation_period": 1},
)
def d_prog_to_infectious():
    return dengue_exposed_humans() / dengue_human_incubation_period()


@component.add(
    name="D Recovery rate",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"dengue_infectious_human": 1, "d_infectious_period": 1},
)
def d_recovery_rate():
    return dengue_infectious_human() / d_infectious_period()


@component.add(
    name="D Recovery rate 1",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"yellowfever_infectious_human": 1, "yellowfever_infectious_period": 1},
)
def d_recovery_rate_1():
    return yellowfever_infectious_human() / yellowfever_infectious_period()


@component.add(
    name="Exposed Dengue Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_exposed_dengue_ae": 1},
    other_deps={
        "_integ_exposed_dengue_ae": {
            "initial": {},
            "step": {
                "aedes_infections_ae": 1,
                "dengue_become_infectious_ae": 1,
                "mortality_ed_ae": 1,
            },
        }
    },
)
def exposed_dengue_ae():
    return _integ_exposed_dengue_ae()


_integ_exposed_dengue_ae = Integ(
    lambda: aedes_infections_ae() - dengue_become_infectious_ae() - mortality_ed_ae(),
    lambda: 0,
    "_integ_exposed_dengue_ae",
)


@component.add(
    name="Exposed Dengue ALbo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_exposed_dengue_albo": 1},
    other_deps={
        "_integ_exposed_dengue_albo": {
            "initial": {},
            "step": {
                "aedes_infections_albo": 1,
                "dengue_become_infectious_albo": 1,
                "mortality_ed_albo": 1,
            },
        }
    },
)
def exposed_dengue_albo():
    return _integ_exposed_dengue_albo()


_integ_exposed_dengue_albo = Integ(
    lambda: aedes_infections_albo()
    - dengue_become_infectious_albo()
    - mortality_ed_albo(),
    lambda: 0,
    "_integ_exposed_dengue_albo",
)


@component.add(
    name="Recovery rate H",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"d_infectious_period": 1},
)
def recovery_rate_h():
    return 1 / d_infectious_period()


@component.add(
    name="Recovery rate H YF",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"yellowfever_infectious_period": 1},
)
def recovery_rate_h_yf():
    return 1 / yellowfever_infectious_period()


@component.add(
    name="Dengue Exposed Humans",
    units="People",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dengue_exposed_humans": 1},
    other_deps={
        "_integ_dengue_exposed_humans": {
            "initial": {},
            "step": {"h_d_infections": 1, "d_prog_to_infectious": 1},
        }
    },
)
def dengue_exposed_humans():
    return _integ_dengue_exposed_humans()


_integ_dengue_exposed_humans = Integ(
    lambda: h_d_infections() - d_prog_to_infectious(),
    lambda: 0,
    "_integ_dengue_exposed_humans",
)


@component.add(
    name="Dengue Human incubation period",
    units="Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def dengue_human_incubation_period():
    return 5 / 30


@component.add(
    name="Dengue Infectious Human",
    units="People",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dengue_infectious_human": 1},
    other_deps={
        "_integ_dengue_infectious_human": {
            "initial": {},
            "step": {"d_prog_to_infectious": 1, "d_recovery_rate": 1},
        }
    },
)
def dengue_infectious_human():
    return _integ_dengue_infectious_human()


_integ_dengue_infectious_human = Integ(
    lambda: d_prog_to_infectious() - d_recovery_rate(),
    lambda: 0,
    "_integ_dengue_infectious_human",
)


@component.add(
    name="Dengue Recovered Humans",
    units="People",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_dengue_recovered_humans": 1},
    other_deps={
        "_integ_dengue_recovered_humans": {
            "initial": {},
            "step": {"d_recovery_rate": 1},
        }
    },
)
def dengue_recovered_humans():
    return _integ_dengue_recovered_humans()


_integ_dengue_recovered_humans = Integ(
    lambda: d_recovery_rate(), lambda: 0, "_integ_dengue_recovered_humans"
)


@component.add(
    name='"Dengue Reproduction Number(R0)"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"d_reproduction_number_ae": 1, "d_reproduction_number_albo": 1},
)
def dengue_reproduction_numberr0():
    return d_reproduction_number_ae() + d_reproduction_number_albo()


@component.add(
    name="Infectious Chikungunya Albo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_infectious_chikungunya_albo": 1},
    other_deps={
        "_integ_infectious_chikungunya_albo": {
            "initial": {},
            "step": {"chikungunya_become_infectious_albo": 1, "mortality_ic_albo": 1},
        }
    },
)
def infectious_chikungunya_albo():
    return _integ_infectious_chikungunya_albo()


_integ_infectious_chikungunya_albo = Integ(
    lambda: chikungunya_become_infectious_albo() - mortality_ic_albo(),
    lambda: 0,
    "_integ_infectious_chikungunya_albo",
)


@component.add(
    name="Infectious Dengue Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_infectious_dengue_ae": 1},
    other_deps={
        "_integ_infectious_dengue_ae": {
            "initial": {},
            "step": {"dengue_become_infectious_ae": 1, "mortality_id_ae": 1},
        }
    },
)
def infectious_dengue_ae():
    return _integ_infectious_dengue_ae()


_integ_infectious_dengue_ae = Integ(
    lambda: dengue_become_infectious_ae() - mortality_id_ae(),
    lambda: 0,
    "_integ_infectious_dengue_ae",
)


@component.add(
    name="Total Adult Ae",
    units="Aedes",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "exposed_chikungunya_ae": 1,
        "exposed_dengue_ae": 1,
        "exposed_yellowfever_ae": 1,
        "infectious_chikungunya_ae": 1,
        "infectious_dengue_ae": 1,
        "infectious_yellowfever_ae": 1,
        "susceptible_ae": 1,
    },
)
def total_adult_ae():
    return (
        exposed_chikungunya_ae()
        + exposed_dengue_ae()
        + exposed_yellowfever_ae()
        + infectious_chikungunya_ae()
        + infectious_dengue_ae()
        + infectious_yellowfever_ae()
        + susceptible_ae()
    )


@component.add(
    name="Total Adult Albo",
    units="Aedes",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "exposed_chikungunya_albo": 1,
        "exposed_dengue_albo": 1,
        "exposed_yellowfever_albo": 1,
        "infectious_chikungunya_albo": 1,
        "infectious_dengue_albo": 1,
        "infectious_yellowfever_albo": 1,
        "susceptible_albo": 1,
    },
)
def total_adult_albo():
    return (
        exposed_chikungunya_albo()
        + exposed_dengue_albo()
        + exposed_yellowfever_albo()
        + infectious_chikungunya_albo()
        + infectious_dengue_albo()
        + infectious_yellowfever_albo()
        + susceptible_albo()
    )


@component.add(
    name="Total transmission potential",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"transmission_potential_ae": 1, "transmission_potential_albo": 1},
)
def total_transmission_potential():
    return transmission_potential_ae() + transmission_potential_albo()


@component.add(
    name="FoI YF Mosq ae",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_ae": 1,
        "human_feeding_fraction_ae": 1,
        "transmission_prob_yf_h_to_m_ae": 1,
        "yellowfever_infectious_human": 1,
        "human_population_1": 1,
    },
)
def foi_yf_mosq_ae():
    return (
        biting_rate_ae()
        * human_feeding_fraction_ae()
        * transmission_prob_yf_h_to_m_ae()
        * (yellowfever_infectious_human() / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="YellowFever Recovered Humans",
    units="People",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_yellowfever_recovered_humans": 1},
    other_deps={
        "_integ_yellowfever_recovered_humans": {
            "initial": {},
            "step": {"d_recovery_rate_1": 1},
        }
    },
)
def yellowfever_recovered_humans():
    return _integ_yellowfever_recovered_humans()


_integ_yellowfever_recovered_humans = Integ(
    lambda: d_recovery_rate_1(), lambda: 0, "_integ_yellowfever_recovered_humans"
)


@component.add(
    name="Transmission potential albo",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "adult_albo": 1,
        "biting_rate_albo": 1,
        "human_feeding_fraction_albo": 1,
        "vector_competence_albo": 1,
    },
)
def transmission_potential_albo():
    return (
        adult_albo()
        * biting_rate_albo()
        * human_feeding_fraction_albo()
        * vector_competence_albo()
    )


@component.add(
    name="EIP D Ae",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temperature_suitability_ae": 1},
)
def eip_d_ae():
    return (8 / temperature_suitability_ae()) / 30


@component.add(
    name="EIP D Albo",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temp_suitability_albo": 1},
)
def eip_d_albo():
    return (9 / temp_suitability_albo()) / 30


@component.add(
    name="EIP YF Ae",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temperature_suitability_ae": 1},
)
def eip_yf_ae():
    return (12 / temperature_suitability_ae()) / 30


@component.add(
    name="EIP YF Albo",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temp_suitability_albo": 1},
)
def eip_yf_albo():
    return (13 / temp_suitability_albo()) / 30


@component.add(
    name="Exposed Chikungunya Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_exposed_chikungunya_ae": 1},
    other_deps={
        "_integ_exposed_chikungunya_ae": {
            "initial": {},
            "step": {
                "chik_infectious_ae": 1,
                "chikungunya_become_infectious_ae": 1,
                "mortality_ec_ae": 1,
            },
        }
    },
)
def exposed_chikungunya_ae():
    return _integ_exposed_chikungunya_ae()


_integ_exposed_chikungunya_ae = Integ(
    lambda: chik_infectious_ae()
    - chikungunya_become_infectious_ae()
    - mortality_ec_ae(),
    lambda: 0,
    "_integ_exposed_chikungunya_ae",
)


@component.add(
    name="Exposed Chikungunya Albo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_exposed_chikungunya_albo": 1},
    other_deps={
        "_integ_exposed_chikungunya_albo": {
            "initial": {},
            "step": {
                "chik_infectious_albo": 1,
                "chikungunya_become_infectious_albo": 1,
                "mortality_ec_albo_0": 1,
            },
        }
    },
)
def exposed_chikungunya_albo():
    return _integ_exposed_chikungunya_albo()


_integ_exposed_chikungunya_albo = Integ(
    lambda: chik_infectious_albo()
    - chikungunya_become_infectious_albo()
    - mortality_ec_albo_0(),
    lambda: 0,
    "_integ_exposed_chikungunya_albo",
)


@component.add(
    name='"Mortality E-YF Ae"',
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_yellowfever_ae": 1, "adult_life_ae": 1},
)
def mortality_eyf_ae():
    return exposed_yellowfever_ae() / adult_life_ae()


@component.add(
    name='"Mortality E-YF Albo"',
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_yellowfever_albo": 1, "adult_life_albo": 1},
)
def mortality_eyf_albo():
    return exposed_yellowfever_albo() / adult_life_albo()


@component.add(
    name="Exposed YellowFever Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_exposed_yellowfever_ae": 1},
    other_deps={
        "_integ_exposed_yellowfever_ae": {
            "initial": {},
            "step": {
                "yf_m_infectious_ae": 1,
                "mortality_eyf_ae": 1,
                "yellowfever_become_infectious_ae": 1,
            },
        }
    },
)
def exposed_yellowfever_ae():
    return _integ_exposed_yellowfever_ae()


_integ_exposed_yellowfever_ae = Integ(
    lambda: yf_m_infectious_ae()
    - mortality_eyf_ae()
    - yellowfever_become_infectious_ae(),
    lambda: 0,
    "_integ_exposed_yellowfever_ae",
)


@component.add(
    name="Exposed YellowFever Albo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_exposed_yellowfever_albo": 1},
    other_deps={
        "_integ_exposed_yellowfever_albo": {
            "initial": {},
            "step": {
                "yf_m_infectious_albo": 1,
                "mortality_eyf_albo": 1,
                "yellowfever_become_infectious_albo": 1,
            },
        }
    },
)
def exposed_yellowfever_albo():
    return _integ_exposed_yellowfever_albo()


_integ_exposed_yellowfever_albo = Integ(
    lambda: yf_m_infectious_albo()
    - mortality_eyf_albo()
    - yellowfever_become_infectious_albo(),
    lambda: 0,
    "_integ_exposed_yellowfever_albo",
)


@component.add(
    name="FoI Chik Mosq ae",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_ae": 1,
        "human_feeding_fraction_ae": 1,
        "transmission_prob_chik_h_to_m_ae": 1,
        "chikungunya_infectious_human": 1,
        "human_population_1": 1,
    },
)
def foi_chik_mosq_ae():
    return (
        biting_rate_ae()
        * human_feeding_fraction_ae()
        * transmission_prob_chik_h_to_m_ae()
        * (chikungunya_infectious_human() / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="FoI Chik Mosq albo",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_albo": 1,
        "human_feeding_fraction_albo": 1,
        "transmission_prob_chik_h_to_m_albo": 1,
        "chikungunya_infectious_human": 1,
        "human_population_1": 1,
    },
)
def foi_chik_mosq_albo():
    return (
        biting_rate_albo()
        * human_feeding_fraction_albo()
        * transmission_prob_chik_h_to_m_albo()
        * (chikungunya_infectious_human() / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="FoI D Mosq ae",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_ae": 1,
        "human_feeding_fraction_ae": 1,
        "transmission_prob_d_h_to_m_ae": 1,
        "human_population_1": 1,
        "dengue_infectious_human": 1,
    },
)
def foi_d_mosq_ae():
    return (
        biting_rate_ae()
        * human_feeding_fraction_ae()
        * transmission_prob_d_h_to_m_ae()
        * (dengue_infectious_human() / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="FoI D Mosq albo",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_albo": 1,
        "human_feeding_fraction_albo": 1,
        "transmission_prob_d_h_to_m_albo": 1,
        "human_population_1": 1,
        "dengue_infectious_human": 1,
    },
)
def foi_d_mosq_albo():
    return (
        biting_rate_albo()
        * human_feeding_fraction_albo()
        * transmission_prob_d_h_to_m_albo()
        * (dengue_infectious_human() / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="FoI H ae",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_ae": 1,
        "human_feeding_fraction_ae": 1,
        "transmission_prob_d_m_to_h_ae": 1,
        "human_population_1": 1,
    },
)
def foi_h_ae():
    return (
        biting_rate_ae()
        * human_feeding_fraction_ae()
        * transmission_prob_d_m_to_h_ae()
        * (1 / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="FoI H ae D",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_ae": 1,
        "human_feeding_fraction_ae": 1,
        "transmission_prob_chi_m_to_h_ae": 1,
        "human_population_1": 1,
    },
)
def foi_h_ae_d():
    return (
        biting_rate_ae()
        * human_feeding_fraction_ae()
        * transmission_prob_chi_m_to_h_ae()
        * (1 / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="FoI H ae YF",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_ae": 1,
        "human_feeding_fraction_ae": 1,
        "transmission_prob_yf_m_to_h_ae": 1,
        "human_population_1": 1,
    },
)
def foi_h_ae_yf():
    return (
        biting_rate_ae()
        * human_feeding_fraction_ae()
        * transmission_prob_yf_m_to_h_ae()
        * (1 / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="FoI H albo",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_albo": 1,
        "human_feeding_fraction_albo": 1,
        "transmission_prob_d_m_to_h_albo": 1,
        "human_population_1": 1,
        "infectious_dengue_albo": 1,
    },
)
def foi_h_albo():
    return (
        biting_rate_albo()
        * human_feeding_fraction_albo()
        * transmission_prob_d_m_to_h_albo()
        * (infectious_dengue_albo() / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="FoI H albo D",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_albo": 1,
        "human_feeding_fraction_albo": 1,
        "transmission_prob_chi_m_to_h_albo": 1,
        "human_population_1": 1,
        "infectious_chikungunya_albo": 1,
    },
)
def foi_h_albo_d():
    return (
        biting_rate_albo()
        * human_feeding_fraction_albo()
        * transmission_prob_chi_m_to_h_albo()
        * (infectious_chikungunya_albo() / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="FoI H albo YF",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_albo": 1,
        "human_feeding_fraction_albo": 1,
        "transmission_prob_yf_m_to_h_albo": 1,
        "human_population_1": 1,
        "infectious_yellowfever_albo": 1,
    },
)
def foi_h_albo_yf():
    return (
        biting_rate_albo()
        * human_feeding_fraction_albo()
        * transmission_prob_yf_m_to_h_albo()
        * (infectious_yellowfever_albo() / float(np.maximum(1, human_population_1())))
    )


@component.add(
    name="YellowFever Infectious period",
    units="Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def yellowfever_infectious_period():
    return 7 / 30


@component.add(
    name="Mortality ED Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_dengue_albo": 1, "adult_life_albo": 1},
)
def mortality_ed_albo():
    return exposed_dengue_albo() / adult_life_albo()


@component.add(
    name='"YellowFever Reproduction Number(R0)"',
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"yf_reproduction_number_ae": 1, "yf_reproduction_number_albo": 1},
)
def yellowfever_reproduction_numberr0():
    return yf_reproduction_number_ae() + yf_reproduction_number_albo()


@component.add(
    name="YF Force of infection Mosquito",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_yf_mosq_ae": 1, "foi_yf_mosq_albo": 1},
)
def yf_force_of_infection_mosquito():
    return foi_yf_mosq_ae() + foi_yf_mosq_albo()


@component.add(
    name="Force of infection H YellowFever",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_h_ae_yf": 1, "foi_h_albo_yf": 1},
)
def force_of_infection_h_yellowfever():
    return foi_h_ae_yf() + foi_h_albo_yf()


@component.add(
    name="H Biirths",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"susceptible_humans": 1, "birth_rate": 1},
)
def h_biirths():
    return susceptible_humans() * birth_rate()


@component.add(
    name="H Chi Infections",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"susceptible_humans": 1, "force_of_infection_h_chikungunya": 1},
)
def h_chi_infections():
    return susceptible_humans() * force_of_infection_h_chikungunya()


@component.add(
    name="YF Reproduction Number Albo",
    units="1/Aedes",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_albo": 1,
        "human_feeding_fraction_albo": 1,
        "transmission_prob_yf_h_to_m_albo": 1,
        "transmission_prob_yf_m_to_h_albo": 1,
        "human_population_1": 1,
        "total_adult_albo": 1,
        "adult_mortality_rate_albo_yf": 2,
        "eip_yf_albo": 1,
        "recovery_rate_h_yf": 1,
    },
)
def yf_reproduction_number_albo():
    return (
        biting_rate_albo() ** 2
        * human_feeding_fraction_albo()
        * transmission_prob_yf_h_to_m_albo()
        * transmission_prob_yf_m_to_h_albo()
        * (total_adult_albo() / human_population_1())
        * float(np.exp(-adult_mortality_rate_albo_yf() * eip_yf_albo()))
        / (adult_mortality_rate_albo_yf() * recovery_rate_h_yf())
    )


@component.add(
    name="Transmission prob D H to M albo",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_d_h_to_m_albo():
    return 0.4 / 30


@component.add(
    name="Transmission prob D M to H ae",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_d_m_to_h_ae():
    return 0.45 / 30


@component.add(
    name="Transmission prob D M to H albo",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_d_m_to_h_albo():
    return 0.35 / 30


@component.add(
    name="Mortality ED Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_dengue_ae": 1, "adult_life_ae": 1},
)
def mortality_ed_ae():
    return exposed_dengue_ae() / adult_life_ae()


@component.add(
    name="Transmission prob YF H to M ae",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_yf_h_to_m_ae():
    return 0.45 / 30


@component.add(
    name='"Mortality I-C Ae"',
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"infectious_chikungunya_ae": 1, "adult_life_ae": 1},
)
def mortality_ic_ae():
    return infectious_chikungunya_ae() / adult_life_ae()


@component.add(
    name='"Mortality I-C Albo"',
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"infectious_chikungunya_albo": 1, "adult_life_albo": 1},
)
def mortality_ic_albo():
    return infectious_chikungunya_albo() / adult_life_albo()


@component.add(
    name="Susceptible Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_susceptible_ae": 1},
    other_deps={
        "_integ_susceptible_ae": {
            "initial": {},
            "step": {
                "adult_emergence_albo": 1,
                "aedes_infections_ae": 1,
                "chik_infectious_ae": 1,
                "natural_mortality_saae": 1,
                "yf_m_infectious_ae": 1,
            },
        }
    },
)
def susceptible_ae():
    return _integ_susceptible_ae()


_integ_susceptible_ae = Integ(
    lambda: adult_emergence_albo()
    - aedes_infections_ae()
    - chik_infectious_ae()
    - natural_mortality_saae()
    - yf_m_infectious_ae(),
    lambda: 100,
    "_integ_susceptible_ae",
)


@component.add(
    name="Human population 1",
    units="People",
    comp_type="Constant",
    comp_subtype="Normal",
)
def human_population_1():
    return 1000


@component.add(
    name="Infectious Chikungunya Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_infectious_chikungunya_ae": 1},
    other_deps={
        "_integ_infectious_chikungunya_ae": {
            "initial": {},
            "step": {"chikungunya_become_infectious_ae": 1, "mortality_ic_ae": 1},
        }
    },
)
def infectious_chikungunya_ae():
    return _integ_infectious_chikungunya_ae()


_integ_infectious_chikungunya_ae = Integ(
    lambda: chikungunya_become_infectious_ae() - mortality_ic_ae(),
    lambda: 0,
    "_integ_infectious_chikungunya_ae",
)


@component.add(
    name="Mortality ID Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"infectious_dengue_albo": 1, "adult_life_albo": 1},
)
def mortality_id_albo():
    return infectious_dengue_albo() / adult_life_albo()


@component.add(
    name="Natural Mortality SAae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"susceptible_ae": 1, "adult_life_ae": 1},
)
def natural_mortality_saae():
    return susceptible_ae() / adult_life_ae()


@component.add(
    name="Infectious Dengue Albo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_infectious_dengue_albo": 1},
    other_deps={
        "_integ_infectious_dengue_albo": {
            "initial": {},
            "step": {"dengue_become_infectious_albo": 1, "mortality_id_albo": 1},
        }
    },
)
def infectious_dengue_albo():
    return _integ_infectious_dengue_albo()


_integ_infectious_dengue_albo = Integ(
    lambda: dengue_become_infectious_albo() - mortality_id_albo(),
    lambda: 0,
    "_integ_infectious_dengue_albo",
)


@component.add(
    name="Infectious YellowFever Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_infectious_yellowfever_ae": 1},
    other_deps={
        "_integ_infectious_yellowfever_ae": {
            "initial": {},
            "step": {"yellowfever_become_infectious_ae": 1, "mortality_iyf_ae": 1},
        }
    },
)
def infectious_yellowfever_ae():
    return _integ_infectious_yellowfever_ae()


_integ_infectious_yellowfever_ae = Integ(
    lambda: yellowfever_become_infectious_ae() - mortality_iyf_ae(),
    lambda: 0,
    "_integ_infectious_yellowfever_ae",
)


@component.add(
    name="Infectious YellowFever Albo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_infectious_yellowfever_albo": 1},
    other_deps={
        "_integ_infectious_yellowfever_albo": {
            "initial": {},
            "step": {"yellowfever_become_infectious_albo": 1, "mortality_iyf_albo": 1},
        }
    },
)
def infectious_yellowfever_albo():
    return _integ_infectious_yellowfever_albo()


_integ_infectious_yellowfever_albo = Integ(
    lambda: yellowfever_become_infectious_albo() - mortality_iyf_albo(),
    lambda: 0,
    "_integ_infectious_yellowfever_albo",
)


@component.add(
    name="YellowFever Infectious Human",
    units="People",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_yellowfever_infectious_human": 1},
    other_deps={
        "_integ_yellowfever_infectious_human": {
            "initial": {},
            "step": {"yf_prog_to_infectious": 1, "d_recovery_rate_1": 1},
        }
    },
)
def yellowfever_infectious_human():
    return _integ_yellowfever_infectious_human()


_integ_yellowfever_infectious_human = Integ(
    lambda: yf_prog_to_infectious() - d_recovery_rate_1(),
    lambda: 0,
    "_integ_yellowfever_infectious_human",
)


@component.add(
    name="Transmission prob YF H to M albo",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_yf_h_to_m_albo():
    return 0.3 / 30


@component.add(
    name="Transmission prob YF M to H ae",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_yf_m_to_h_ae():
    return 0.45 / 30


@component.add(
    name="Transmission prob Chi M to H ae",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_chi_m_to_h_ae():
    return 0.45 / 30


@component.add(
    name="Transmission prob Chi M to H albo",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_chi_m_to_h_albo():
    return 0.35 / 30


@component.add(
    name="Transmission prob Chik H to M ae",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_chik_h_to_m_ae():
    return 0.6 / 30


@component.add(
    name="Life expectancy", units="Month", comp_type="Constant", comp_subtype="Normal"
)
def life_expectancy():
    return 70 * 12


@component.add(
    name="Transmission prob D H to M ae",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_d_h_to_m_ae():
    return 0.5 / 30


@component.add(
    name="Yellowfever become Infectious Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_yellowfever_albo": 1, "eip_yf_albo": 1},
)
def yellowfever_become_infectious_albo():
    return exposed_yellowfever_albo() / eip_yf_albo()


@component.add(
    name="Natural Mortality SAalbo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"susceptible_albo": 1, "adult_life_albo": 1},
)
def natural_mortality_saalbo():
    return susceptible_albo() / adult_life_albo()


@component.add(
    name="YellowFever Human incubation period",
    units="Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def yellowfever_human_incubation_period():
    return 5 / 30


@component.add(
    name='"Mortality I-YF Albo"',
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"infectious_yellowfever_albo": 1, "adult_life_albo": 1},
)
def mortality_iyf_albo():
    return infectious_yellowfever_albo() / adult_life_albo()


@component.add(
    name="Mortality ID Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"infectious_dengue_ae": 1, "adult_life_ae": 1},
)
def mortality_id_ae():
    return infectious_dengue_ae() / adult_life_ae()


@component.add(
    name="Yellowfever become Infectious Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"exposed_yellowfever_ae": 1, "eip_yf_ae": 1},
)
def yellowfever_become_infectious_ae():
    return exposed_yellowfever_ae() / eip_yf_ae()


@component.add(
    name="Transmission prob YF M to H albo",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_yf_m_to_h_albo():
    return 0.35 / 30


@component.add(
    name='"Mortality I-YF Ae"',
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"infectious_yellowfever_ae": 1, "adult_life_ae": 1},
)
def mortality_iyf_ae():
    return infectious_yellowfever_ae() / adult_life_ae()


@component.add(
    name="YellowFever Exposed Humans",
    units="People",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_yellowfever_exposed_humans": 1},
    other_deps={
        "_integ_yellowfever_exposed_humans": {
            "initial": {},
            "step": {"h_yf_infections": 1, "yf_prog_to_infectious": 1},
        }
    },
)
def yellowfever_exposed_humans():
    return _integ_yellowfever_exposed_humans()


_integ_yellowfever_exposed_humans = Integ(
    lambda: h_yf_infections() - yf_prog_to_infectious(),
    lambda: 0,
    "_integ_yellowfever_exposed_humans",
)


@component.add(
    name="YF M Infectious Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_yf_mosq_ae": 1, "susceptible_ae": 1},
)
def yf_m_infectious_ae():
    return foi_yf_mosq_ae() * susceptible_ae()


@component.add(
    name="YF M Infectious Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"foi_yf_mosq_albo": 1, "susceptible_albo": 1},
)
def yf_m_infectious_albo():
    return foi_yf_mosq_albo() * susceptible_albo()


@component.add(
    name="YF Reproduction Number Ae",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "biting_rate_ae": 1,
        "human_feeding_fraction_ae": 1,
        "transmission_prob_yf_h_to_m_ae": 1,
        "transmission_prob_yf_m_to_h_ae": 1,
        "total_adult_ae": 1,
        "human_population_1": 1,
        "eip_yf_ae": 1,
        "adult_mortality_rate_ae_yf": 2,
        "recovery_rate_h_yf": 1,
    },
)
def yf_reproduction_number_ae():
    return (
        biting_rate_ae() ** 2
        * human_feeding_fraction_ae()
        * transmission_prob_yf_h_to_m_ae()
        * transmission_prob_yf_m_to_h_ae()
        * (total_adult_ae() / human_population_1())
        * float(np.exp(-adult_mortality_rate_ae_yf() * eip_yf_ae()))
        / (adult_mortality_rate_ae_yf() * recovery_rate_h_yf())
    )


@component.add(
    name="Transmission prob Chik H to M albo",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def transmission_prob_chik_h_to_m_albo():
    return 0.55 / 30


@component.add(
    name="Vector competence albo",
    units="1/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def vector_competence_albo():
    return 0.5 / 30


@component.add(
    name="YF Prog to Infectious",
    units="People/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "yellowfever_exposed_humans": 1,
        "yellowfever_human_incubation_period": 1,
    },
)
def yf_prog_to_infectious():
    return yellowfever_exposed_humans() / yellowfever_human_incubation_period()


@component.add(
    name="Susceptible Humans",
    units="People",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_susceptible_humans": 1},
    other_deps={
        "_integ_susceptible_humans": {
            "initial": {},
            "step": {
                "h_biirths": 1,
                "h_chi_infections": 1,
                "h_d_infections": 1,
                "h_deaths": 1,
                "h_yf_infections": 1,
            },
        }
    },
)
def susceptible_humans():
    return _integ_susceptible_humans()


_integ_susceptible_humans = Integ(
    lambda: h_biirths()
    - h_chi_infections()
    - h_d_infections()
    - h_deaths()
    - h_yf_infections(),
    lambda: 10000,
    "_integ_susceptible_humans",
)


@component.add(
    name="Vector competence ae",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def vector_competence_ae():
    return 0.7 / 30


@component.add(
    name="Susceptible Albo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_susceptible_albo": 1},
    other_deps={
        "_integ_susceptible_albo": {
            "initial": {},
            "step": {
                "adult_emergence_albo": 1,
                "aedes_infections_albo": 1,
                "chik_infectious_albo": 1,
                "natural_mortality_saalbo": 1,
                "yf_m_infectious_albo": 1,
            },
        }
    },
)
def susceptible_albo():
    return _integ_susceptible_albo()


_integ_susceptible_albo = Integ(
    lambda: adult_emergence_albo()
    - aedes_infections_albo()
    - chik_infectious_albo()
    - natural_mortality_saalbo()
    - yf_m_infectious_albo(),
    lambda: 100,
    "_integ_susceptible_albo",
)


@component.add(
    name="Adult Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_adult_ae": 1},
    other_deps={
        "_integ_adult_ae": {
            "initial": {},
            "step": {"adult_emergence_ae": 1, "adult_mortality_ae": 1},
        }
    },
)
def adult_ae():
    return _integ_adult_ae()


_integ_adult_ae = Integ(
    lambda: adult_emergence_ae() - adult_mortality_ae(), lambda: 100, "_integ_adult_ae"
)


@component.add(
    name="Larva Albo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_larva_albo": 1},
    other_deps={
        "_integ_larva_albo": {
            "initial": {},
            "step": {
                "hatching_albo": 1,
                "larval_mortality_albo": 1,
                "pupation_albo": 1,
            },
        }
    },
)
def larva_albo():
    return _integ_larva_albo()


_integ_larva_albo = Integ(
    lambda: hatching_albo() - larval_mortality_albo() - pupation_albo(),
    lambda: 500,
    "_integ_larva_albo",
)


@component.add(
    name="Adult Emergence Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pupa_ae": 1, "pupa_duration_ae": 1},
)
def adult_emergence_ae():
    return pupa_ae() * pupa_duration_ae()


@component.add(
    name="Adult Emergence Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"pupa_albo": 1, "pupa_duration_albo": 1},
)
def adult_emergence_albo():
    return pupa_albo() * pupa_duration_albo()


@component.add(
    name="Adult life ae",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temperature_suitability_ae": 1},
)
def adult_life_ae():
    return (20 * temperature_suitability_ae()) / 30


@component.add(
    name="Adult life albo",
    units="Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temp_suitability_albo": 1},
)
def adult_life_albo():
    return (25 * temp_suitability_albo()) / 30


@component.add(
    name="Adult Mortality Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_ae": 1, "adult_life_ae": 1, "additional_ae_mortality": 1},
)
def adult_mortality_ae():
    return adult_ae() / adult_life_ae() + additional_ae_mortality()


@component.add(
    name="Adult Mortality ALbo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_albo": 1, "adult_life_albo": 1},
)
def adult_mortality_albo():
    return adult_albo() / adult_life_albo()


@component.add(
    name="Eggs per female albo",
    units="Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eggs_per_female_albo():
    return 9


@component.add(
    name="Alpha Ae", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def alpha_ae():
    """
    Effect of albopictus on Aegypti
    """
    return 0.8 / 30


@component.add(name="Alpha Albo", comp_type="Constant", comp_subtype="Normal")
def alpha_albo():
    """
    Effect of Aegypti on Albopictus. Studies suggest asymmetric competition favouring albopictus
    """
    return 0.4 / 30


@component.add(
    name="Oviposition Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_albo": 1, "eggs_per_female_albo": 1, "temp_suitability_albo": 1},
)
def oviposition_albo():
    return adult_albo() * eggs_per_female_albo() * temp_suitability_albo()


@component.add(
    name="Carrying capacity Ae",
    units="Aedes",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "container_density": 1,
        "habitat_suitability_ae": 1,
        "base_carrying_capacity": 1,
    },
)
def carrying_capacity_ae():
    return container_density() * habitat_suitability_ae() * base_carrying_capacity()


@component.add(
    name="Carrying capacity ALbo",
    units="Aedes",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "base_carrying_capacity": 1,
        "container_density": 1,
        "habitat_suitability_albo": 1,
    },
)
def carrying_capacity_albo():
    return base_carrying_capacity() * container_density() * habitat_suitability_albo()


@component.add(
    name="Competition pressure ae",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "larva_ae": 1,
        "alpha_ae": 1,
        "larva_albo": 1,
        "carrying_capacity_ae": 1,
    },
)
def competition_pressure_ae():
    return (larva_ae() + alpha_ae() * larva_albo()) / carrying_capacity_ae()


@component.add(
    name="Competition pressure albo",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "larva_albo": 1,
        "alpha_albo": 1,
        "larva_ae": 1,
        "carrying_capacity_albo": 1,
    },
)
def competition_pressure_albo():
    return (larva_albo() + alpha_albo() * larva_ae()) / carrying_capacity_albo()


@component.add(
    name="Pupa duration Albo",
    units="1/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def pupa_duration_albo():
    return 2.5 / 30


@component.add(
    name="Pupation Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"larva_ae": 1, "larva_duration_ae": 1},
)
def pupation_ae():
    return larva_ae() * larva_duration_ae()


@component.add(
    name="Egg Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_egg_ae": 1},
    other_deps={
        "_integ_egg_ae": {
            "initial": {},
            "step": {"oviposition_ae": 1, "hatching_ae": 1},
        }
    },
)
def egg_ae():
    return _integ_egg_ae()


_integ_egg_ae = Integ(
    lambda: oviposition_ae() - hatching_ae(), lambda: 1000, "_integ_egg_ae"
)


@component.add(
    name="Rainfall",
    units="Month",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_rainfall",
        "__data__": "_ext_data_rainfall",
        "time": 1,
    },
)
def rainfall():
    return _ext_data_rainfall(time())


_ext_data_rainfall = ExtData(
    r"Mombasa Climate2015_2065.xlsx",
    "Climate_monthly_ensemble",
    "C",
    "E2",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_rainfall",
)


@component.add(
    name="Egg duration Ae", units="1/Month", comp_type="Constant", comp_subtype="Normal"
)
def egg_duration_ae():
    return 5 / 30


@component.add(
    name="Egg duration Albo",
    units="1/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def egg_duration_albo():
    return 5 / 30


@component.add(
    name="Eggs per female ae",
    units="Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def eggs_per_female_ae():
    return 10


@component.add(
    name="Temperature",
    units="Month",
    comp_type="Data",
    comp_subtype="External",
    depends_on={
        "__external__": "_ext_data_temperature",
        "__data__": "_ext_data_temperature",
        "time": 1,
    },
)
def temperature():
    return _ext_data_temperature(time())


_ext_data_temperature = ExtData(
    r"Mombasa Climate2015_2065.xlsx",
    "Climate_monthly_ensemble",
    "C",
    "I2",
    "interpolate",
    {},
    _root,
    {},
    "_ext_data_temperature",
)


@component.add(
    name="Temperature Suitability Ae",
    units="1/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temperature": 1},
)
def temperature_suitability_ae():
    return float(np.exp(-((temperature() - 30) ** 2) / 50))


@component.add(
    name="Hatching Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"egg_ae": 1, "egg_duration_ae": 1},
)
def hatching_ae():
    return egg_ae() * egg_duration_ae()


@component.add(
    name="Hatching Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"egg_albo": 1, "egg_duration_albo": 1},
)
def hatching_albo():
    return egg_albo() * egg_duration_albo()


@component.add(
    name="Suppression factor",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_albo": 2, "adult_ae": 1},
)
def suppression_factor():
    return float(np.minimum(1, adult_albo() / (adult_albo() + adult_ae() + 1)))


@component.add(
    name="Larva Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_larva_ae": 1},
    other_deps={
        "_integ_larva_ae": {
            "initial": {},
            "step": {"hatching_ae": 1, "larval_mortality_ae": 1, "pupation_ae": 1},
        }
    },
)
def larva_ae():
    return _integ_larva_ae()


_integ_larva_ae = Integ(
    lambda: hatching_ae() - larval_mortality_ae() - pupation_ae(),
    lambda: 500,
    "_integ_larva_ae",
)


@component.add(
    name="Pupa duration Ae",
    units="1/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def pupa_duration_ae():
    return 2 / 30


@component.add(
    name="Larva duration Ae",
    units="1/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def larva_duration_ae():
    return 8 / 30


@component.add(
    name="Larva duration Albo",
    units="1/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def larva_duration_albo():
    return 9 / 30


@component.add(
    name="Larval mortality ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"competition_pressure_ae": 1, "larva_ae": 1, "priority_effect_ae": 1},
)
def larval_mortality_ae():
    return (competition_pressure_ae() * larva_ae() * 0.1) * priority_effect_ae()


@component.add(
    name="Larval mortality albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "competition_pressure_albo": 1,
        "larva_albo": 1,
        "priority_effect_albo": 1,
    },
)
def larval_mortality_albo():
    return (competition_pressure_albo() * larva_albo() * 0.08) * priority_effect_albo()


@component.add(
    name="Priority Index",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"adult_albo": 2, "adult_ae": 2},
)
def priority_index():
    return (adult_albo() - adult_ae()) / (adult_albo() + adult_ae() + 1)


@component.add(
    name="Pupa Ae",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pupa_ae": 1},
    other_deps={
        "_integ_pupa_ae": {
            "initial": {},
            "step": {"pupation_ae": 1, "adult_emergence_ae": 1},
        }
    },
)
def pupa_ae():
    return _integ_pupa_ae()


_integ_pupa_ae = Integ(
    lambda: pupation_ae() - adult_emergence_ae(), lambda: 200, "_integ_pupa_ae"
)


@component.add(
    name="Temp Suitability Albo",
    units="1/Day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"temperature": 1},
)
def temp_suitability_albo():
    """
    Albopictus is assigned a lower optimum temperature to reflect better adaption to cooler highland conditions
    """
    return float(np.exp(-((temperature() - 27) ** 2) / 60))


@component.add(
    name="Priority effect albo",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"priority_index": 1},
)
def priority_effect_albo():
    return float(np.maximum(0, 1 + priority_index()))


@component.add(
    name="Oviposition Ae",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "adult_ae": 1,
        "eggs_per_female_ae": 1,
        "temperature_suitability_ae": 1,
    },
)
def oviposition_ae():
    return adult_ae() * eggs_per_female_ae() * temperature_suitability_ae()


@component.add(
    name="Priority Effect Ae",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"priority_index": 1},
)
def priority_effect_ae():
    return float(np.maximum(0, 1 - priority_index()))


@component.add(
    name="Suppression Month value",
    units="1/Month",
    comp_type="Constant",
    comp_subtype="Normal",
)
def suppression_month_value():
    return 0.01


@component.add(
    name="Pupation Albo",
    units="Aedes/Month",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"larva_albo": 1, "larva_duration_albo": 1},
)
def pupation_albo():
    return larva_albo() * larva_duration_albo()


@component.add(
    name="Urbanization index", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def urbanization_index():
    return 0.5


@component.add(
    name="Base carrying capacity",
    units="Aedes",
    comp_type="Constant",
    comp_subtype="Normal",
)
def base_carrying_capacity():
    return 10000


@component.add(
    name="Container Density", units="Dmnl", comp_type="Constant", comp_subtype="Normal"
)
def container_density():
    return 100


@component.add(
    name="Habitat Suitability Ae",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"urbanization_index": 1, "rainfall": 1},
)
def habitat_suitability_ae():
    return float(
        np.minimum(1, 0.3 + 0.4 * urbanization_index() + 0.3 * (rainfall() / 100))
    )


@component.add(
    name="Habitat Suitability Albo",
    units="Dmnl",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"organic_matter_index": 1, "urbanization_index": 1, "rainfall": 1},
)
def habitat_suitability_albo():
    return float(
        np.minimum(
            1,
            0.4 * organic_matter_index()
            + 0.2 * urbanization_index()
            + 0.4 * (rainfall() / 100),
        )
    )


@component.add(
    name="Organic matter index",
    units="Dmnl",
    comp_type="Constant",
    comp_subtype="Normal",
)
def organic_matter_index():
    return 0.5


@component.add(
    name="Adult Albo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_adult_albo": 1},
    other_deps={
        "_integ_adult_albo": {
            "initial": {},
            "step": {"adult_emergence_albo": 1, "adult_mortality_albo": 1},
        }
    },
)
def adult_albo():
    return _integ_adult_albo()


_integ_adult_albo = Integ(
    lambda: adult_emergence_albo() - adult_mortality_albo(),
    lambda: 100,
    "_integ_adult_albo",
)


@component.add(
    name="Egg Albo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_egg_albo": 1},
    other_deps={
        "_integ_egg_albo": {
            "initial": {},
            "step": {"oviposition_albo": 1, "hatching_albo": 1},
        }
    },
)
def egg_albo():
    return _integ_egg_albo()


_integ_egg_albo = Integ(
    lambda: oviposition_albo() - hatching_albo(), lambda: 1000, "_integ_egg_albo"
)


@component.add(
    name="Pupa Albo",
    units="Aedes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_pupa_albo": 1},
    other_deps={
        "_integ_pupa_albo": {
            "initial": {},
            "step": {"pupation_albo": 1, "adult_emergence_albo": 1},
        }
    },
)
def pupa_albo():
    return _integ_pupa_albo()


_integ_pupa_albo = Integ(
    lambda: pupation_albo() - adult_emergence_albo(), lambda: 200, "_integ_pupa_albo"
)
