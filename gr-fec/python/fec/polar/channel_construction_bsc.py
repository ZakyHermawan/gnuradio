#!/usr/bin/env python
#
# Copyright 2015 Free Software Foundation, Inc.
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

'''
Based on 2 papers:
[1] Ido Tal, Alexander Vardy: 'How To Construct Polar Codes', 2013
for an in-depth description of a widely used algorithm for channel construction.

[2] Harish Vangala, Emanuele Viterbo, Yi Hong: 'A Comparative Study of Polar Code Constructions for the AWGN Channel', 2015
for an overview of different approaches
'''


from scipy.optimize import fsolve
from scipy.special import erfc
from helper_functions import *
import matplotlib.pyplot as plt
from channel_construction_bec import bhattacharyya_bounds


def bsc_channel(p):
    '''
    binary symmetric channel (BSC)
    output alphabet Y = {0, 1} and
    W(0|0) = W(1|1) and W(1|0) = W(0|1)

    this function returns a prob's vector for a BSC
    p denotes an erroneous transistion
    '''
    if not (p >= 0.0 and p <= 1.0):
        print "given p is out of range!"
        return np.array([], dtype=float)

    # 0 -> 0, 0 -> 1, 1 -> 0, 1 -> 1
    W = np.array([[1 - p, p], [p, 1 - p]], dtype=float)
    return W


def get_Bn(n):
    # this is a bit reversal matrix.
    lw = int(np.log2(n))  # number of used bits
    indexes = [bit_reverse(i, lw) for i in range(n)]
    Bn = np.zeros((n, n), type(n))
    for i, index in enumerate(indexes):
        Bn[i][index] = 1
    return Bn


def get_Fn(n):
    # this matrix defines the actual channel combining.
    if n == 1:
        return np.array([1, ])
    F2 = np.array([[1, 0], [1, 1]], np.int)
    nump = int(np.log2(n)) - 1  # number of Kronecker products to calculate
    Fn = F2
    for i in range(nump):
        Fn = np.kron(Fn, F2)
    return Fn

def get_Gn(n):
    # this matrix is called generator matrix
    if not is_power_of_two(n):
        print "invalid input"
        return None
    if n == 1:
        return np.array([1, ])
    Bn = get_Bn(n)
    Fn = get_Fn(n)
    Gn = np.dot(Bn, Fn)
    return Gn


def mutual_information(w):
    '''
    calculate mutual information I(W)
    I(W) = sum over y e Y ( sum over x e X ( ... ) )
    .5 W(y|x) log frac { W(y|x) }{ .5 W(y|0) + .5 W(y|1) }
    '''
    ydim, xdim = np.shape(w)
    i = 0.0
    for y in range(ydim):
        for x in range(xdim):
            v = w[y][x] * np.log2(w[y][x] / (0.5 * w[y][0] + 0.5 * w[y][1]))
            i += v
    i /= 2.0
    return i


def solver_equation(val, s):
    cw_lambda = codeword_lambda_callable(s)
    ic_lambda = instantanious_capacity_callable()
    return lambda y: ic_lambda(cw_lambda(y)) - val


def solve_capacity(a, s):
    eq = solver_equation(a, s)
    res = fsolve(eq, 1)
    return np.abs(res[0])  # only positive values needed.


def codeword_lambda_callable(s):
    return lambda y: np.exp(-2 * y * np.sqrt(2 * s))


def codeword_lambda(y, s):
    return codeword_lambda_callable(s)(y)


def instantanious_capacity_callable():
    return lambda x : 1 - np.log2(1 + x) + (x * np.log2(x) / (1 + x))


def instantanious_capacity(x):
    return instantanious_capacity_callable()(x)


def q_function(x):
    # Q(x) = (1 / sqrt(2 * pi) ) * integral (x to inf) exp(- x ^ 2 / 2) dx
    return .5 * erfc(x / np.sqrt(2))


def discretize_awgn(mu, design_snr):
    '''
    needed for Binary-AWGN channels.
    in [1] described in Section VI
    in [2] described as a function of the same name.
    in both cases reduce infinite output alphabet to a finite output alphabet of a given channel.
    idea:
    1. instantaneous capacity C(x) in interval [0, 1]
    2. split into mu intervals.
    3. find corresponding output alphabet values y of likelihood ratio function lambda(y) inserted into C(x)
    4. Calculate probability for each value given that a '0' or '1' is was transmitted.
    '''
    s = 10 ** (design_snr / 10)
    a = np.zeros(mu + 1, dtype=float)
    a[-1] = np.inf
    for i in range(1, mu):
        a[i] = solve_capacity(1. * i / mu, s)

    factor = np.sqrt(2 * s)
    tpm = np.zeros((2, mu))
    for j in range(mu):
        tpm[0][j] = q_function(factor + a[j]) - q_function(factor + a[j + 1])
        tpm[1][j] = q_function(-1. * factor + a[j]) - q_function(-1. * factor + a[j + 1])
    return tpm


def instant_capacity_delta_callable():
    return lambda a, b: -1. * (a + b) * np.log2((a + b) / 2) + a * np.log2(a) + b * np.log2(b)


def capacity_delta_callable():
    c = instant_capacity_delta_callable()
    return lambda a, b, at, bt: c(a, b) + c(at, bt) - c(a + at, b + bt)


def quantize_to_size(tpm, mu):
    # This is a degrading merge, compare [1]
    calculate_delta_I = capacity_delta_callable()
    L = np.shape(tpm)[1]
    if not mu < L:
        print('WARNING: This channel gets too small!')

    # lambda works on vectors just fine. Use Numpy vector awesomeness.
    delta_i_vec = calculate_delta_I(tpm[0, 0:-1], tpm[1, 0:-1], tpm[0, 1:], tpm[1, 1:])

    for i in range(L - mu):
        d = np.argmin(delta_i_vec)
        ap = tpm[0, d] + tpm[0, d + 1]
        bp = tpm[1, d] + tpm[1, d + 1]
        if d > 0:
            delta_i_vec[d - 1] = calculate_delta_I(tpm[0, d - 1], tpm[1, d - 1], ap, bp)
        if d < delta_i_vec.size - 1:
            delta_i_vec[d + 1] = calculate_delta_I(ap, bp, tpm[0, d + 1], tpm[1, d + 1])
        delta_i_vec = np.delete(delta_i_vec, d)
        tpm = np.delete(tpm, d, axis=1)
        tpm[0, d] = ap
        tpm[1, d] = bp
    return tpm


def upper_bound_z_params(z, block_size, design_snr):
    upper_bound = bhattacharyya_bounds(design_snr, block_size)
    z = np.minimum(z, upper_bound)
    return z


def tal_vardy_tpm_algorithm(block_size, design_snr, mu):
    block_power = power_of_2_int(block_size)
    channels = np.zeros((block_size, 2, mu))
    channels[0] = discretize_awgn(mu, design_snr) * 2

    print('Constructing polar code with Tal-Vardy algorithm')
    print('(block_size = {0}, design SNR = {1}, mu = {2}'.format(block_size, design_snr, mu))
    show_progress_bar(0, block_size)
    for j in range(0, block_power):
        u = 2 ** j
        for t in range(u):
            show_progress_bar(u + t, block_size)
            # print("(u={0}, t={1}) = {2}".format(u, t, u + t))
            ch1 = upper_convolve(channels[t], mu)
            ch2 = lower_convolve(channels[t], mu)
            channels[t] = quantize_to_size(ch1, mu)
            channels[u + t] = quantize_to_size(ch2, mu)

    z = np.zeros(block_size)
    for i in range(block_size):
        # z[i] = np.sum(channels[i][1])
        z[i] = bhattacharyya_parameter(channels[i])

    z = z[bit_reverse_vector(np.arange(block_size), block_power)]
    z = upper_bound_z_params(z, block_size, design_snr)
    show_progress_bar(block_size, block_size)
    print('')
    print('channel construction DONE')
    return z


def merge_lr_based(q, mu):
    lrs = q[0] / q[1]
    vals, indices, inv_indices = np.unique(lrs, return_index=True, return_inverse=True)
    # compare [1] (20). Ordering of representatives according to LRs.
    temp = np.zeros((2, len(indices)), dtype=float)
    if vals.size < mu:
        return q
    for i in range(len(indices)):
        merge_pos = np.where(inv_indices == i)[0]
        sum_items = q[:, merge_pos]
        if merge_pos.size > 1:
            sum_items = np.sum(q[:, merge_pos], axis=1)
        temp[0, i] = sum_items[0]
        temp[1, i] = sum_items[1]
    return temp


def upper_convolve(tpm, mu):
    q = np.zeros((2, mu ** 2))
    idx = -1
    for i in range(mu):
        idx += 1
        q[0, idx] = (tpm[0, i] ** 2 + tpm[1, i] ** 2) / 2
        q[1, idx] = tpm[0, i] * tpm[1, i]
        for j in range(i + 1, mu):
            idx += 1
            q[0, idx] = tpm[0, i] * tpm[0, j] + tpm[1, i] * tpm[1, j]
            q[1, idx] = tpm[0, i] * tpm[1, j] + tpm[1, i] * tpm[0, j]
            if q[0, idx] < q[1, idx]:
                q[0, idx], q[1, idx] = swap_values(q[0, idx], q[1, idx])

    idx += 1
    q = np.delete(q, np.arange(idx, np.shape(q)[1]), axis=1)
    q = merge_lr_based(q, mu)
    q = normalize_q(q, tpm)
    return q


def lower_convolve(tpm, mu):
    q = np.zeros((2, mu * (mu + 1)))
    idx = -1
    for i in range(0, mu):
        idx += 1
        q[0, idx] = (tpm[0, i] ** 2) / 2
        q[1, idx] = (tpm[1, i] ** 2) / 2
        if q[0, idx] < q[1, idx]:
            q[0, idx], q[1, idx] = swap_values(q[0, idx], q[1, idx])
        idx += 1
        q[0, idx] = tpm[0, i] * tpm[1, i]
        q[1, idx] = q[0, idx]

        for j in range(i + 1, mu):
            idx += 1
            q[0, idx] = tpm[0, i] * tpm[0, j]
            q[1, idx] = tpm[1, i] * tpm[1, j]
            if q[0, idx] < q[1, idx]:
                q[0, idx], q[1, idx] = swap_values(q[0, idx], q[1, idx])
            idx += 1
            q[0, idx] = tpm[0, i] * tpm[1, j]
            q[1, idx] = tpm[1, i] * tpm[0, j]
            if q[0, idx] < q[1, idx]:
                q[0, idx], q[1, idx] = swap_values(q[0, idx], q[1, idx])
    idx += 1
    q = np.delete(q, np.arange(idx, np.shape(q)[1]), axis=1)
    q = merge_lr_based(q, mu)
    q = normalize_q(q, tpm)
    return q


def swap_values(first, second):
    return second, first


def normalize_q(q, tpm):
    original_factor = np.sum(tpm)
    next_factor = np.sum(q)
    factor = original_factor / next_factor
    return q * factor


def main():
    print 'channel construction BSC main'
    n = 10
    m = 2 ** n
    k = m // 2
    design_snr = 0.5
    mu = 32


    z_params = tal_vardy_tpm_algorithm(m, design_snr, mu)
    print(z_params)
    plt.plot(z_params)
    plt.show()

    # q = discretize_awgn(mu, design_snr)


    # print('discretized:', np.sum(q))
    # qu = upper_convolve(q, mu)
    # print('upper_convolve:', np.sum(qu))
    # q0 = lower_convolve(q, mu)
    # print('lower_convolve:', np.sum(q0))


if __name__ == '__main__':
    main()
