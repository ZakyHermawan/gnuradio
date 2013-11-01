/* -*- c++ -*- */
/*
 * Copyright 2002,2008,2012 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifndef _FILTER_FIRDES_H_
#define _FILTER_FIRDES_H_

#include <gnuradio/filter/api.h>
#include <vector>
#include <cmath>
#include <gnuradio/gr_complex.h>

namespace gr {
  namespace filter {

    /*!
     * \brief Finite Impulse Response (FIR) filter design functions.
     * \ingroup filter_design
     */
    
    class FILTER_API firdes {
    public:
            
      enum win_type {
	WIN_NONE = -1,           //!< don't use a window
	WIN_HAMMING = 0,         //!< Hamming window; max attenuation 53 dB
	WIN_HANN = 1,            //!< Hann window; max attenuation 44 dB
	WIN_BLACKMAN = 2,        //!< Blackman window; max attenuation 74 dB
	WIN_RECTANGULAR = 3,     //!< Basic rectangular window
	WIN_KAISER = 4,          //!< Kaiser window; max attenuation a function of beta, google it
	WIN_BLACKMAN_hARRIS = 5, //!< Blackman-harris window
	WIN_BLACKMAN_HARRIS = 5, //!< alias to WIN_BLACKMAN_hARRIS for capitalization consistency
        WIN_BARTLETT = 6,        //!< Barlett (triangular) window
      };


      // ... class methods ...
      
      /*!
       * \brief use "window method" to design a low-pass FIR filter
       *
       * \param gain             overall gain of filter (typically 1.0)
       * \param sampling_freq    sampling freq (Hz)
       * \param cutoff_freq      center of transition band (Hz)
       * \param transition_width width of transition band (Hz).
       *                         The normalized width of the transition
       *                         band is what sets the number of taps
       *                         required.  Narrow --> more taps
       * \param window           What kind of window to use. Determines
       *                         maximum attenuation and passband ripple.
       * \param beta             parameter for Kaiser window
       */
      static std::vector<float>
	low_pass(double gain,
		 double sampling_freq,
		 double cutoff_freq,		// Hz center of transition band
		 double transition_width,	// Hz width of transition band
		 win_type window = WIN_HAMMING,
		 double beta = 6.76);		// used only with Kaiser
      
      /*!
       * \brief use "window method" to design a low-pass FIR filter
       *
       * \param gain             overall gain of filter (typically 1.0)
       * \param sampling_freq    sampling freq (Hz)
       * \param cutoff_freq      center of transition band (Hz)
       * \param transition_width width of transition band (Hz).
       * \param attenuation_dB   required stopband attenuation
       *                         The normalized width of the transition
       *                         band and the required stop band
       *                         attenuation is what sets the number of taps
       *                         required.  Narrow --> more taps
       *                         More attenuatin --> more taps
       * \param window           What kind of window to use. Determines
       *                         maximum attenuation and passband ripple.
       * \param beta             parameter for Kaiser window
       */
      static std::vector<float>
	low_pass_2(double gain,
		   double sampling_freq,
		   double cutoff_freq,		// Hz beginning transition band
		   double transition_width,	// Hz width of transition band
		   double attenuation_dB,       // out of band attenuation dB
		   win_type window = WIN_HAMMING,
		   double beta = 6.76);		// used only with Kaiser

      /*!
       * \brief use "window method" to design a high-pass FIR filter
       *
       * \param gain             overall gain of filter (typically 1.0)
       * \param sampling_freq    sampling freq (Hz)
       * \param cutoff_freq      center of transition band (Hz)
       * \param transition_width width of transition band (Hz).
       *			 The normalized width of the transition
       *			 band is what sets the number of taps
       *			 required.  Narrow --> more taps
       * \param window           What kind of window to use. Determines
       *                         maximum attenuation and passband ripple.
       * \param beta             parameter for Kaiser window
       */
      static std::vector<float>
	high_pass(double gain,
		  double sampling_freq,
		  double cutoff_freq,		// Hz center of transition band
		  double transition_width,	// Hz width of transition band
		  win_type window = WIN_HAMMING,
		  double beta = 6.76);		// used only with Kaiser

      /*!
       * \brief use "window method" to design a high-pass FIR filter
       *
       * \param gain             overall gain of filter (typically 1.0)
       * \param sampling_freq    sampling freq (Hz)
       * \param cutoff_freq      center of transition band (Hz)
       * \param transition_width width of transition band (Hz).
       * \param attenuation_dB   out of band attenuation
       *                         The normalized width of the transition
       *                         band and the required stop band
       *                         attenuation is what sets the number of taps
       *                         required.  Narrow --> more taps
       *                         More attenuation --> more taps
       * \param window           What kind of window to use. Determines
       *                         maximum attenuation and passband ripple.
       * \param beta             parameter for Kaiser window
       */
      static std::vector<float>
	high_pass_2(double gain,
		    double sampling_freq,
		    double cutoff_freq,		// Hz center of transition band
		    double transition_width,	// Hz width of transition band
		    double attenuation_dB,      // out of band attenuation dB
		    win_type window = WIN_HAMMING,
		    double beta = 6.76);	// used only with Kaiser
      
      /*!
       * \brief use "window method" to design a band-pass FIR filter
       *
       * \param gain             overall gain of filter (typically 1.0)
       * \param sampling_freq    sampling freq (Hz)
       * \param low_cutoff_freq  center of transition band (Hz)
       * \param high_cutoff_freq center of transition band (Hz)
       * \param transition_width width of transition band (Hz).
       *                         The normalized width of the transition
       *                         band is what sets the number of taps
       *                         required.  Narrow --> more taps
       * \param window           What kind of window to use. Determines
       *                         maximum attenuation and passband ripple.
       * \param beta             parameter for Kaiser window
       */
      static std::vector<float>
	band_pass(double gain,
		  double sampling_freq,
		  double low_cutoff_freq,	// Hz center of transition band
		  double high_cutoff_freq,	// Hz center of transition band
		  double transition_width,	// Hz width of transition band
		  win_type window = WIN_HAMMING,
		  double beta = 6.76);		// used only with Kaiser
      
      /*!
       * \brief use "window method" to design a band-pass FIR filter
       *
       * \param gain             overall gain of filter (typically 1.0)
       * \param sampling_freq    sampling freq (Hz)
       * \param low_cutoff_freq  center of transition band (Hz)
       * \param high_cutoff_freq center of transition band (Hz)
       * \param transition_width width of transition band (Hz).
       * \param attenuation_dB   out of band attenuation
       *                         The normalized width of the transition
       *                         band and the required stop band
       *                         attenuation is what sets the number of taps
       *                         required.  Narrow --> more taps
       *                         More attenuation --> more taps
       * \param window           What kind of window to use. Determines
       *                         maximum attenuation and passband ripple.
       * \param beta             parameter for Kaiser window
       */
      static std::vector<float>
	band_pass_2(double gain,
		    double sampling_freq,
		    double low_cutoff_freq,	// Hz beginning transition band
		    double high_cutoff_freq,	// Hz beginning transition band
		    double transition_width,	// Hz width of transition band
		    double attenuation_dB,      // out of band attenuation dB
		    win_type window = WIN_HAMMING,
		    double beta = 6.76);	// used only with Kaiser
      
      /*!
       * \brief use "window method" to design a complex band-pass FIR filter
       *
       * \param gain             overall gain of filter (typically 1.0)
       * \param sampling_freq    sampling freq (Hz)
       * \param low_cutoff_freq  center of transition band (Hz)
       * \param high_cutoff_freq center of transition band (Hz)
       * \param transition_width width of transition band (Hz).
       *                         The normalized width of the transition
       *                         band is what sets the number of taps
       *                         required.  Narrow --> more taps
       * \param window           What kind of window to use. Determines
       *                         maximum attenuation and passband ripple.
       * \param beta             parameter for Kaiser window
       */
      static std::vector<gr_complex>
	complex_band_pass(double gain,
			  double sampling_freq,
			  double low_cutoff_freq,	// Hz center of transition band
			  double high_cutoff_freq,	// Hz center of transition band
			  double transition_width,	// Hz width of transition band
			  win_type window = WIN_HAMMING,
			  double beta = 6.76);		// used only with Kaiser
      
      /*!
       * \brief use "window method" to design a complex band-pass FIR filter
       *
       * \param gain             overall gain of filter (typically 1.0)
       * \param sampling_freq    sampling freq (Hz)
       * \param low_cutoff_freq  center of transition band (Hz)
       * \param high_cutoff_freq center of transition band (Hz)
       * \param transition_width width of transition band (Hz).
       * \param attenuation_dB   out of band attenuation
       *                         The normalized width of the transition
       *                         band and the required stop band
       *                         attenuation is what sets the number of taps
       *                         required.  Narrow --> more taps
       *                         More attenuation --> more taps
       * \param window           What kind of window to use. Determines
       *                         maximum attenuation and passband ripple.
       * \param beta             parameter for Kaiser window
       */
      static std::vector<gr_complex>
	complex_band_pass_2(double gain,
			    double sampling_freq,
			    double low_cutoff_freq,	// Hz beginning transition band
			    double high_cutoff_freq,	// Hz beginning transition band
			    double transition_width,	// Hz width of transition band
			    double attenuation_dB,      // out of band attenuation dB
			    win_type window = WIN_HAMMING,
			    double beta = 6.76);	// used only with Kaiser
      
      /*!
       * \brief use "window method" to design a band-reject FIR filter
       *
       * \param gain             overall gain of filter (typically 1.0)
       * \param sampling_freq    sampling freq (Hz)
       * \param low_cutoff_freq  center of transition band (Hz)
       * \param high_cutoff_freq center of transition band (Hz)
       * \param transition_width width of transition band (Hz).
       *                         The normalized width of the transition
       *                         band is what sets the number of taps
       *                         required.  Narrow --> more taps
       * \param window           What kind of window to use. Determines
       *                         maximum attenuation and passband ripple.
       * \param beta             parameter for Kaiser window
       */
      static std::vector<float>
	band_reject(double gain,
		    double sampling_freq,
		    double low_cutoff_freq,	// Hz center of transition band
		    double high_cutoff_freq,	// Hz center of transition band
		    double transition_width,	// Hz width of transition band
		    win_type window = WIN_HAMMING,
		    double beta = 6.76);	// used only with Kaiser
      
      /*!
       * \brief use "window method" to design a band-reject FIR filter
       *
       * \param gain             overall gain of filter (typically 1.0)
       * \param sampling_freq    sampling freq (Hz)
       * \param low_cutoff_freq  center of transition band (Hz)
       * \param high_cutoff_freq center of transition band (Hz)
       * \param transition_width width of transition band (Hz).
       * \param attenuation_dB   out of band attenuation
       *                         The normalized width of the transition
       *                         band and the required stop band
       *                         attenuation is what sets the number of taps
       *                         required.  Narrow --> more taps
       *                         More attenuation --> more taps
       * \param window           What kind of window to use. Determines
       *                         maximum attenuation and passband ripple.
       * \param beta             parameter for Kaiser window
       */
      static std::vector<float>
	band_reject_2(double gain,
		      double sampling_freq,
		      double low_cutoff_freq,	// Hz beginning transition band
		      double high_cutoff_freq,	// Hz beginning transition band
		      double transition_width,	// Hz width of transition band
		      double attenuation_dB,    // out of band attenuation dB
		      win_type window = WIN_HAMMING,
		      double beta = 6.76);	// used only with Kaiser
      
      /*!\brief design a Hilbert Transform Filter
       *
       * \param ntaps       Number of taps, must be odd
       * \param windowtype  What kind of window to use
       * \param beta        Only used for Kaiser
       */
      static std::vector<float>
	hilbert(unsigned int ntaps = 19,
		win_type windowtype = WIN_RECTANGULAR,
		double beta = 6.76);
      
      /*!
       * \brief design a Root Cosine FIR Filter (do we need a window?)
       *
       * \param gain          overall gain of filter (typically 1.0)
       * \param sampling_freq sampling freq (Hz)
       * \param symbol_rate   symbol rate, must be a factor of sample rate
       * \param alpha         excess bandwidth factor
       * \param ntaps         number of taps
       */
      static std::vector<float>
	root_raised_cosine(double gain,
			   double sampling_freq,
			   double symbol_rate, // Symbol rate, NOT bitrate (unless BPSK)
			   double alpha,       // Excess Bandwidth Factor
			   int ntaps);
      
      /*!
       * \brief design a Gaussian filter
       *
       * \param gain  overall gain of filter (typically 1.0)
       * \param spb   samples per baud
       * \param bt    bandwidth-time product factor
       * \param ntaps number of taps
       */
      static std::vector<float>
	gaussian(double gain,
		 double spb,
		 double bt,     // Bandwidth to bitrate ratio
		 int ntaps);
      
      /*!
       * \brief build a window of a \p type and size \p ntaps.
       *
       * \param type  type of window (as a win_type)
       * \param ntaps size of the window
       * \param beta  beta value for Kaiser windows
       */
      static std::vector<float> window(win_type type, int ntaps, double beta=6.76);
      
    private:
      static double bessi0(double x);
      static void sanity_check_1f(double sampling_freq, double f1,
				  double transition_width);
      static void sanity_check_2f(double sampling_freq, double f1, double f2,
				  double transition_width);
      static void sanity_check_2f_c(double sampling_freq, double f1, double f2,
				    double transition_width);
      
      static int compute_ntaps(double sampling_freq,
			       double transition_width,
			       win_type window_type, double beta);
      
      static int compute_ntaps_windes(double sampling_freq,
				      double transition_width,
				      double attenuation_dB);
    };
    
  } /* namespace filter */
} /* namespace gr */

#endif /* _FILTER_FIRDES_H_ */
