import scipy as scipy
from scipy import stats
import numpy as np
import math
import matplotlib
import cv2 as cv


def DFT(input_img):
    row_in, col_in = input_img.shape
    
    rows = row_in+col_in
    cols = row_in+col_in
    tmp = np.zeros((rows,cols))
    tmp[0:row_in,0:col_in] = input_img  
    input_img = tmp
    
    output_img = np.fft.fftshift(np.fft.fft2(input_img))
    return output_img

def reconstruct(mag,ang):
    combined = np.multiply(mag, np.exp(1j*ang))
    fftx = combined
    fftx = np.fft.ifftshift(combined)
    ffty = np.fft.ifft2(fftx)
    imgCombined = np.abs(ffty)
    u,v = imgCombined.shape
    return imgCombined



###################################### Avoid Usage


def median_fil(ima, n):
    u, v = ima.shape
    padd =  np.zeros((u+n,v+n))
    bor = n // 2
    padd[bor:bor+u, bor:bor+v] = ima
    out = np.empty((u,v))
    for i in range(u):
        for j in range(v):
            temp = padd[ bor + (i-bor) : bor + (i-bor) + n,  bor + (j-bor) : bor + (j-bor) + n]
            med = np.median(temp)
            out[i,j] =  med
                
    return out
    
def Gauss_BR(ima, r, order):
    u, v = ima.shape
    len_y = max(u,v)+1
    mid = len_y//2
    
    x = np.linspace(-10-r,10-r,len_y)
    
    Y = scipy.stats.norm.pdf(x, 0, order)
       
    
    Y = Y[mid:len_y-1]
    Y = Y/np.linalg.norm(Y)
    
    len_y = len(Y)
    mid_y = len_y//2
    len_x = round(len_y*v//u)
    mid_x = len_x//2
    
    filtr = np.zeros(( len_y, len_x))
    
    for i in range(2*len_y):
        for j in range(2*len_x):
            val = round(np.sqrt((i-mid_y)**2 + (j-mid_x)**2)) 
            if mid_y - val > 0 :
                filtr[i,j]= Y[  val]
    
    y4=round(len_y//4)
    x4=round(len_x//4)
    filtr = filtr[y4:3*y4, x4: 3*x4]           
    filtr =  cv.resize(filtr, (u,v))
            
    return filtr
    
def notch_reject_filter(ima, d0, u_k , v_k):
    P, Q = ima.shape
    # Initialize filter with zeros
    H = np.zeros((P, Q))

    # Traverse through filter
    for u in range(0, P):
        for v in range(0, Q):
            # Get euclidean distance from point D(u,v) to the center
            D_uv = np.sqrt((u - P / 2 + u_k) ** 2 + (v - Q / 2 + v_k) ** 2)
            D_muv = np.sqrt((u - P / 2 - u_k) ** 2 + (v - Q / 2 - v_k) ** 2)

            if D_uv <= d0 or D_muv <= d0:
                H[u, v] = 0.0
            else:
                H[u, v] = 1.0

    return H
    
    
def Gauss_BR(ima, r, order):
    u, v = ima.shape
    len_y = 2000
    mid = len_y//2
    
    x = np.linspace(-10-r,10-r,len_y)
    
    Y = stats.norm.pdf(x, 0, order)
       
    
    Y = Y[mid:len_y-1]
    Y = Y/np.linalg.norm(Y)
    
    len_y = len(Y)
    mid_y = len_y//2
    len_x = round(len_y*v//u)
    mid_x = len_x//2
    
    filtr = np.zeros(( len_y, len_x))
    
    for i in range(2*len_y):
        for j in range(2*len_x):
            val = round(np.sqrt((i-mid_y)**2 + (j-mid_x)**2)) 
            if mid_y - val > 0 :
                filtr[i,j]= Y[  val]
    
    y4=round(len_y//4)
    x4=round(len_x//4)
    filtr = filtr[y4:3*y4, x4: 3*x4]           
    filtr =  cv.resize(filtr, (u,v))
            
    return filtr

def notch_reject_filter(ima, d0, u_k , v_k):
    P, Q = ima.shape
    # Initialize filter with zeros
    H = np.zeros((P, Q))

    # Traverse through filter
    for u in range(0, P):
        for v in range(0, Q):
            # Get euclidean distance from point D(u,v) to the center
            D_uv = np.sqrt((u - P / 2 + u_k) ** 2 + (v - Q / 2 + v_k) ** 2)
            D_muv = np.sqrt((u - P / 2 - u_k) ** 2 + (v - Q / 2 - v_k) ** 2)

            if D_uv <= d0 or D_muv <= d0:
                H[u, v] = 0.0
            else:
                H[u, v] = 1.0

    return H
