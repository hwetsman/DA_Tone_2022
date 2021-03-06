""" this attempt to create DAtone over time taking into account genetic polymorphism
.02 tries to make all variable global"""

import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import pandas as pd


def Get_ICtyr(btyr,VtyricKmax,VtyricVmax):
    """btyr and Kmax are in µM,Vmax in µM/hr
    returns the change in the tyrpool in µM
    """
    change = (VtyricVmax*btyr)/(VtyricKmax+btyr)
    return change

def Calculate_Vth(tyr,Ki_tyr):
    """ this ignores the effect of eda and cda"""
    Vth = .56/(1+(tyr/Ki_tyr))
    return Vth

# def Calc_DA_Pro(mthfr, th, da_pro_constant):
#     produced = da_pro_constant*mthfr*th/ic_da
#     return produced


def Calc_Packaged(pack_constant, ic_da, iv_da, vmat):
    packaged = (ic_da * pack_constant) * vmat/iv_da
    return packaged


# def Calc_Reuptake(ec_da, dat, reuptake_constant):
#     reuptake = max(dat * ec_da/ic_da * reuptake_constant, 0)
#     return reuptake


def Calc_IC(ic_da, reuptake, produced, ic_loss, packaged):
    ic_da = ic_da + reuptake + produced - ic_loss - packaged
    return ic_da


# def Calc_Released(iv_da, ec_end, ec_da, s_receptors, htr2a, htr2c, opir, nic):
#     if iv_da > 30:
#         rel = max(0, da_rel_constant * htr2a * htr2a_constant * htr2c * htr2c_constant *
#                   opir * opir_constant * nic * nic_constant * ec_end / (s_receptors*ec_da))
#     if iv_da <= 30:
#         rel = 0
#     return rel


# def Calc_IV(iv_da, released, packaged):
#     iv_da = iv_da - released + packaged - iv_loss
#     #iv_da = iv_da - released + packaged
#     return iv_da


def Calc_EC(ec_da, released, ec_loss, reuptake):
    ec_da = ec_da + released - ec_loss - reuptake
    return ec_da


# def Calc_DA_Recep(i, ec_da, da_threshold, da_receptors, max_receptors):
#     if i < 2000:
#         trigger = 10
#     else:
#         avg_extra = np.array(extracellular[i-1000:i])
#         trigger = np.mean(avg_extra) * da_threshold
#     if ec_da > trigger:
#         da_receptors = max(da_receptors * .99, 0)
#         # print(da_receptors,'recptors')
#     else:
#         da_receptors = min(da_receptors * 1.001, max_receptors)

#         # print(da_receptors,'receptors')
#     return da_receptors


def Calc_DA_Tone(l_receptors,ec_da):
    tone = l_receptors * ec_da
    return tone


def Calc_IC_End(ic_end, end_pro, end_rel, ic_end_loss):
    ic_end = ic_end + end_pro - end_rel - ic_end_loss
    return ic_end


def Calc_EC_End(ec_end, end_rel, ec_end_loss):
    ec_end = ec_end + end_rel - ec_end_loss
    return ec_end


# Backbone Model
# pro = []
# extracellular = []
time = []
str_tyr = []
Vth_calc = []
# intravesicular = []
# da_release = []
# intracellular = []
# toneset = []
# icend = []
# ecend = []
# endtone = []
# recept_list = []
# reup = []
# start with set amounts for compartments
#produced = 1.2

# iv_da = 50
# ic_da = 1
# ec_da = 1

#set cycles
cycles = st.sidebar.slider('Cycles', 10, 25000, 10000)

#blood tyrosine in microMoles
btyr = st.sidebar.slider('Serum Tyrosine',min_value=39,max_value=180,value=97)

#params for calculating intracellular tyr
VtyricKmax = 64 #mMole
VtyricVmax = 400 #mMole/hr
tyrpool = 1260 #brain tyrosine pool in microMole
tyrpoolK1 = 6 #K of tyrpool to tyr
tyrpoolK_1=0.6 #K of tyr to tyrpool
Ktyrcat = 0.2 #K of catabolism of tyr
tyr = 0 #start with no tyrosine

#tyr hydroxylase
Ki_tyr = st.sidebar.slider('Ki(tyr)',max_value=160,min_value=37,value=160) #µM




#production
# mthfr = st.sidebar.slider('MTHFR', .3, 1.0, 1.0)
# th = st.sidebar.slider('TH', 1.0, 1.1, 1.0)
# da_pro_constant = st.sidebar.slider('____________________DA Production Constant', 10, 200, 150)

#packaging
# vmat = st.sidebar.slider('VMAT', .35, 1.0, 1.0)
# pack_constant = st.sidebar.slider('________________________Packaging Constant', .01, 2.0, 0.3)
# iv_loss = st.sidebar.slider("Intraventricular Loss", .1, .9, .1)

# Release
# da_rel_constant = st.sidebar.slider('_______________________DA Release Constant', 1.0, 5.0, 3.5)
# htr2a = 1
# htr2a_constant = 1
# htr2c = 1
# htr2c_constant = 1
# nic = 1
# nic_constant = 1
# opir = 1
# opir_constant = 1

# Reuptake
# dat = st.sidebar.slider("DAT", 1.0, 1.1, 1.0)
# reuptake_constant = st.sidebar.slider('_________________________Reuptake Constant', .01, 1.0, .24)

##################3 Intracellular ###############################
# maob_constant = st.sidebar.slider('____________________________MAOB Constant', .01, 1.0, .1)
# maob = st.sidebar.slider('MAOB', 1.0, 1.1, 1.0)

# Extracellular###########################3
# comt_constant = st.sidebar.slider('___________________________COMT Constant', .01, .05, .03)
# comt = st.sidebar.slider('COMT', 1.0, 1.1, 1.0)

#################### DA Receptors ################################
# max_da_receptors = st.sidebar.slider('Maximum DA Receptors', 10, 100, 30)
# da_receptors = st.sidebar.slider('Beginning DA Receptors', 1.0, 30.0, 11.0)
# percent_s = st.sidebar.slider('Percent D2s', .01, 1.0, .9)
# s_receptors = da_receptors * percent_s
# da_threshold = st.sidebar.slider('DA Threshold for Receptor Drop', 1.01, 1.5, 1.15)

#################### endorphin production ########################
# end_pro = st.sidebar.slider('POMC Constant', .1, 3.0, 1.25)
# ic_end = 1
# ec_end = 10
# end_tone = 10
# end_rel_constant = st.sidebar.slider('Endorphin Release Constant', .01, .5, .01)
# end_rec = st.sidebar.slider('Endorphin Receptor Constant', .01, 5.0, 1.0)


# r = 5000
# s = 2000
# t = 7500


for i in range(cycles):
    time.append(i)
    #tyr
    dICtyr = Get_ICtyr(btyr,VtyricKmax,VtyricVmax) #tyr in the brain
    tyrpool = tyrpool+dICtyr #tyrosine pool in brain
    tyr = tyrpool*tyrpoolK1-tyr*tyrpoolK_1-tyr*Ktyrcat #try available for DA
    str_tyr.append(tyr)
    Vth = Calculate_Vth(tyr, Ki_tyr)
    Vth_calc.append(Vth)
    # ic_da
    # produced = Calc_DA_Pro(mthfr, th, da_pro_constant)
    # pro.append(produced)
    # packaged = max(Calc_Packaged(pack_constant, ic_da, iv_da, vmat), 0)
    # ic_loss = max(ic_da * maob_constant * maob, 0)
    # if i > r and i < r+100:
    #     reuptake = 0
    # elif i > t and i < t+100:
    #     reuptake = -Calc_Reuptake(ec_da, dat, reuptake_constant)
    # else:
    #     reuptake = Calc_Reuptake(ec_da, dat, reuptake_constant)
    # reup.append(reuptake)
    # ic_da = Calc_IC(ic_da, reuptake, produced, ic_loss, packaged)
    # intracellular.append(ic_da)

    # # iv_da
    # if i > s and i < s+100:
    #     released = 1.1*Calc_Released(iv_da, ec_end, ec_da, s_receptors, htr2a, htr2c, opir, nic)
    # else:
    #     released = Calc_Released(iv_da, ec_end, ec_da, s_receptors, htr2a, htr2c, opir, nic)
    # da_release.append(released)
    # iv_da = Calc_IV(iv_da, released, packaged)
    # intravesicular.append(iv_da)

    # # ec_da
    # ec_loss = max(comt_constant * comt * ec_da, 0)
    # ec_da = Calc_EC(ec_da, released, ec_loss, reuptake)
    # extracellular.append(ec_da)
    

    # #da_receptors = 3
    # da_receptors = Calc_DA_Recep(i, ec_da, da_threshold, da_receptors, max_da_receptors)
    # s_receptors = da_receptors * percent_s

    # # tone
    # l_receptors = min(da_receptors, max_da_receptors) * (1-percent_s)
    # recept_list.append(l_receptors)

    # da_tone = Calc_DA_Tone(l_receptors)
    # toneset.append(da_tone)

######### ENDORPHIN SIDE ###################################################
    # ic_end_loss = max(0, .01 * ic_end)
    # end_rel = end_rel_constant * da_tone
    # ic_end = max(0, Calc_IC_End(ic_end, end_pro, end_rel, ic_end_loss))
    # icend.append(ic_end)

    # ec_end_loss = max(0, .1 * ec_end)
    # ec_end = max(0, Calc_EC_End(ec_end, end_rel, ec_end_loss))
    # ecend.append(ec_end)

    # end_tone = ec_end * end_rec
    # endtone.append(end_tone)
    
    
# st.write(round(produced, 2), 'produced', '\t', round(ic_da, 2), 'intracellular',
          # round(packaged, 2), 'packaged', '\t', round(iv_da, 2), 'intravesicular')
# st.write(round(released, 2), 'released', '\t', round(ec_da, 2), 'extracelllular')
# st.write(round(l_receptors, 2), 'D2l', '\t', round(s_receptors, 2), 'D2s', '\t',
#           round(da_receptors, 2), 'DA receptors', round(da_tone, 2), 'tone')
# horizontal = np.full(cycles-1000, 3.5)
# linedata = pd.DataFrame([recept_list[1000:cycles], toneset[1000:cycles], horizontal]).T
# st.write('Receptors, Tone and Reward Line')
# st.write('_ _ _ _ _ _ _ _Normal Reward_ _ _ _ _  _ _ _ _ _ _ _ _ _  _Cocaine_ _ _ _ _ _ _ _ _ _ _ _Amphetamine')
# st.line_chart(linedata, width=900, height=500)
fig, ax = plt.subplots()
ax.scatter(time[1000:cycles],str_tyr[1000:cycles],color = 'green',s=1)
ax.scatter(time[1000:cycles],Vth_calc[1000:cycles],color = 'b',s=1)
# ax.scatter(time[1000:cycles], horizontal, color='green', alpha=.1, s=1)
# ax.scatter(time[1000:cycles], recept_list[1000:cycles], color='red', s=1)
# ax.scatter(time[1000:cycles], toneset[1000:cycles], color='cyan', s=1)

st.pyplot(fig)
