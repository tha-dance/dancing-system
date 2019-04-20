import pandas as pd 
import numpy as np 
from scipy import stats

def min(segment):
	arr = []
	for i in range(9):
		arr.append(np.min(segment[:,i]))
	return arr

def max(segment):
	arr = []
	for i in range(9):
		arr.append(np.max(segment[:,i]))
	return arr

def mean(segment):
	arr = []
	for i in range(9):
		arr.append(np.mean(segment[:,i]))
	return arr

def standard_dev(segment):
	arr = []
	for i in range(9):
		arr.append(np.std(segment[:,i]))
	return arr

def rms(segment):
	square = 0
	for i in range(9):
		square+=(segment[i]**2)
	mean = (square/float(9))
	root =math.sqrt(mean)
	return root

def entropy(segment):
	arr = []
	for i in range(0,9):
		freq = np.abs(np.fft.rfft(segment[:,i]))
		arr.append(stats.entropy(freq,base =2))
	return arr

def energy(segment):
	arr = []
	for i in range(0,9):
		freq = np.abs(np.fft.rfft(segment[:,i]))
		arr.append(np.sum(freq**2)/len(freq))
	return arr

def extract(segment):
	final = []
	final.extend(min(segment))
	final.extend(max(segment))
	final.extend(mean(segment))
	final.extend(standard_dev(segment))
	final.extend(energy(segment))
	final.extend(entropy(segment))
	return final