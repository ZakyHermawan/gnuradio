#!/usr/bin/env python

from gnuradio import gr
from gnuradio import audio
from gnuradio import trellis
from gnuradio import eng_notation
import math
import sys
import random
import fsm_utils



def make_rx(fg,fo,fi,dimensionality,constellation,K,interleaver,IT,Es,N0,type):
    metrics_in = trellis.metrics_f(fi.O(),dimensionality,constellation,trellis.TRELLIS_EUCLIDEAN) # data preprocessing to generate metrics for innner Viterbi
    scale = gr.multiply_const_ff(1.0/N0)
    gnd = gr.vector_source_f([0],True);

    inter=[]
    deinter=[]
    siso_in=[]
    siso_out=[]

    for it in range(IT-1):
      inter.append( trellis.permutation(interleaver.K(),interleaver.INTER(),fi.I(),gr.sizeof_float) )
      siso_in.append( trellis.siso_f(fi,K,0,3,True,False,type) )
      deinter.append( trellis.permutation(interleaver.K(),interleaver.DEINTER(),fi.I(),gr.sizeof_float) )
      siso_out.append( trellis.siso_f(fo,K,0,3,False,True,type) )
      fg.connect (inter[it],(siso_in[it],0))
      fg.connect (gnd,(siso_out[it],0))
      fg.connect (siso_in[it],deinter[it],(siso_out[it],1))

    inter.append( trellis.permutation(interleaver.K(),interleaver.INTER(),fi.I(),gr.sizeof_float) )
    siso_in.append( trellis.siso_f(fi,K,0,-1,True,False,type) )
    deinter.append( trellis.permutation(interleaver.K(),interleaver.DEINTER(),fi.I(),gr.sizeof_float) )
    siso_out.append( trellis.viterbi_s(fo,K,0,-1) )
    fg.connect (inter[IT-1],(siso_in[IT-1],0))
    fg.connect (siso_in[IT-1],deinter[IT-1],siso_out[IT-1])

    # connect first stage
    fg.connect (gnd,inter[0])
    fg.connect (metrics_in,scale)
    fg.connect (scale,(siso_in[0],1))
    for it in range(IT-1):
      fg.connect (siso_out[it],inter[it+1])
      fg.connect (metrics_in,(siso_in[it+1],1))
    return (metrics_in,siso_out[IT-1])


def run_test (fo,fi,interleaver,Kb,bitspersymbol,K,dimensionality,constellation,Es,N0,IT,seed):
    fg = gr.flow_graph ()


    # TX
    src = gr.lfsr_32k_source_s()
    src_head = gr.head (gr.sizeof_short,Kb/16) # packet size in shorts
    s2fsmi = gr.packed_to_unpacked_ss(bitspersymbol,gr.GR_MSB_FIRST) # unpack shorts to symbols compatible with the outer FSM input cardinality
    enc_out = trellis.encoder_ss(fo,0) # initial state = 0
    inter = trellis.permutation(interleaver.K(),interleaver.INTER(),1,gr.sizeof_short)
    enc_in = trellis.encoder_ss(fi,0) # initial state = 0
    mod = gr.chunks_to_symbols_sf(constellation,dimensionality)

    # CHANNEL
    add = gr.add_ff()
    noise = gr.noise_source_f(gr.GR_GAUSSIAN,math.sqrt(N0/2),seed)

    # RX
    (head,tail) = make_rx(fg,fo,fi,dimensionality,constellation,K,interleaver,IT,Es,N0,trellis.TRELLIS_MIN_SUM)
    #(head,tail) = make_rx(fg,fo,fi,dimensionality,constellation,K,interleaver,IT,Es,N0,trellis.TRELLIS_SUM_PRODUCT)
    fsmi2s = gr.unpacked_to_packed_ss(bitspersymbol,gr.GR_MSB_FIRST) # pack FSM input symbols to shorts
    dst = gr.check_lfsr_32k_s()
    
    fg.connect (src,src_head,s2fsmi,enc_out,inter,enc_in,mod)
    fg.connect (mod,(add,0))
    fg.connect (noise,(add,1))
    fg.connect (add,head)
    fg.connect (tail,fsmi2s,dst)

    fg.run()
 
    #print enc_out.ST(), enc_in.ST()
    
    ntotal = dst.ntotal ()
    nright = dst.nright ()
    runlength = dst.runlength ()
    return (ntotal,ntotal-nright)


def main(args):
    nargs = len (args)
    if nargs == 4:
        fname_out=args[0]
        fname_in=args[1]
        esn0_db=float(args[2]) # Es/No in dB
        rep=int(args[3]) # number of times the experiment is run to collect enough errors
    else:
        sys.stderr.write ('usage: test_tcm.py fsm_name_out fsm_fname_in Es/No_db  repetitions\n')
        sys.exit (1)

    # system parameters
    Kb=1024*16  # packet size in bits (make it multiple of 16 so it can be packed in a short)
    fo=trellis.fsm(fname_out) # get the outer FSM specification from a file
    fi=trellis.fsm(fname_in) # get the innner FSM specification from a file
    bitspersymbol = int(round(math.log(fo.I())/math.log(2))) # bits per FSM input symbol
    if fo.O() != fi.I():
        sys.stderr.write ('Incompatible cardinality between outer and inner FSM.\n')
        sys.exit (1)
    K=Kb/bitspersymbol # packet size in trellis steps
    interleaver=trellis.interleaver(K,666) # construct a random interleaver
    modulation = fsm_utils.psk8 # see fsm_utlis.py for available predefined modulations
    dimensionality = modulation[0]
    constellation = modulation[1] 
    if len(constellation)/dimensionality != fi.O():
        sys.stderr.write ('Incompatible FSM output cardinality and modulation size.\n')
        sys.exit (1)
    # calculate average symbol energy
    Es = 0
    for i in range(len(constellation)):
        Es = Es + constellation[i]**2
    Es = Es / (len(constellation)/dimensionality)
    N0=Es/pow(10.0,esn0_db/10.0); # calculate noise variance
    IT = 3 # number of turbo iterations
    
    tot_s=0 # total number of transmitted shorts
    terr_s=0 # total number of shorts in error
    terr_p=0 # total number of packets in error
    for i in range(rep):
        (s,e)=run_test(fo,fi,interleaver,Kb,bitspersymbol,K,dimensionality,constellation,Es,N0,IT,-long(666+i)) # run experiment with different seed to get different noise realizations
        tot_s=tot_s+s
        terr_s=terr_s+e
        terr_p=terr_p+(terr_s!=0)
        if ((i+1)%10==0): # display progress
            print i+1,terr_p, '%.2e' % ((1.0*terr_p)/(i+1)),tot_s,terr_s, '%.2e' % ((1.0*terr_s)/tot_s)
    # estimate of the (short or bit) error rate
    print rep,terr_p, '%.2e' % ((1.0*terr_p)/(i+1)),tot_s,terr_s, '%.2e' % ((1.0*terr_s)/tot_s)


if __name__ == '__main__':
    main (sys.argv[1:])
