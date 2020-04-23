/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/* This file is automatically generated using bindtool */

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/filter/firdes.h>
// pydoc.h is automatically generated in the build directory
#include <firdes_pydoc.h>

void bind_firdes(py::module& m)
{
    using firdes = gr::filter::firdes;

    py::class_<firdes, std::shared_ptr<firdes>> firdes_class(m, "firdes", D(firdes));

    py::enum_<gr::filter::firdes::win_type>(firdes_class, "win_type")
        .value("WIN_NONE", gr::filter::firdes::WIN_NONE)                       // -1
        .value("WIN_HAMMING", gr::filter::firdes::WIN_HAMMING)                 // 0
        .value("WIN_HANN", gr::filter::firdes::WIN_HANN)                       // 1
        .value("WIN_BLACKMAN", gr::filter::firdes::WIN_BLACKMAN)               // 2
        .value("WIN_RECTANGULAR", gr::filter::firdes::WIN_RECTANGULAR)         // 3
        .value("WIN_KAISER", gr::filter::firdes::WIN_KAISER)                   // 4
        .value("WIN_BLACKMAN_hARRIS", gr::filter::firdes::WIN_BLACKMAN_hARRIS) // 5
        .value("WIN_BLACKMAN_HARRIS", gr::filter::firdes::WIN_BLACKMAN_HARRIS) // 5
        .value("WIN_BARTLETT", gr::filter::firdes::WIN_BARTLETT)               // 6
        .value("WIN_FLATTOP", gr::filter::firdes::WIN_FLATTOP)                 // 7
        .export_values();


    firdes_class
        .def_static("window",
                    &firdes::window,
                    py::arg("type"),
                    py::arg("ntaps"),
                    py::arg("beta"),
                    D(firdes, window))


        .def_static("low_pass",
                    &firdes::low_pass,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("cutoff_freq"),
                    py::arg("transition_width"),
                    py::arg("window") = ::gr::filter::firdes::win_type::WIN_HAMMING,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, low_pass))


        .def_static("low_pass_2",
                    &firdes::low_pass_2,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("cutoff_freq"),
                    py::arg("transition_width"),
                    py::arg("attenuation_dB"),
                    py::arg("window") = ::gr::filter::firdes::win_type::WIN_HAMMING,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, low_pass_2))


        .def_static("high_pass",
                    &firdes::high_pass,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("cutoff_freq"),
                    py::arg("transition_width"),
                    py::arg("window") = ::gr::filter::firdes::win_type::WIN_HAMMING,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, high_pass))


        .def_static("high_pass_2",
                    &firdes::high_pass_2,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("cutoff_freq"),
                    py::arg("transition_width"),
                    py::arg("attenuation_dB"),
                    py::arg("window") = ::gr::filter::firdes::win_type::WIN_HAMMING,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, high_pass_2))


        .def_static("band_pass",
                    &firdes::band_pass,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("low_cutoff_freq"),
                    py::arg("high_cutoff_freq"),
                    py::arg("transition_width"),
                    py::arg("window") = ::gr::filter::firdes::win_type::WIN_HAMMING,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, band_pass))


        .def_static("band_pass_2",
                    &firdes::band_pass_2,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("low_cutoff_freq"),
                    py::arg("high_cutoff_freq"),
                    py::arg("transition_width"),
                    py::arg("attenuation_dB"),
                    py::arg("window") = ::gr::filter::firdes::win_type::WIN_HAMMING,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, band_pass_2))


        .def_static("complex_band_pass",
                    &firdes::complex_band_pass,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("low_cutoff_freq"),
                    py::arg("high_cutoff_freq"),
                    py::arg("transition_width"),
                    py::arg("window") = ::gr::filter::firdes::win_type::WIN_HAMMING,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, complex_band_pass))


        .def_static("complex_band_pass_2",
                    &firdes::complex_band_pass_2,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("low_cutoff_freq"),
                    py::arg("high_cutoff_freq"),
                    py::arg("transition_width"),
                    py::arg("attenuation_dB"),
                    py::arg("window") = ::gr::filter::firdes::win_type::WIN_HAMMING,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, complex_band_pass_2))


        .def_static("band_reject",
                    &firdes::band_reject,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("low_cutoff_freq"),
                    py::arg("high_cutoff_freq"),
                    py::arg("transition_width"),
                    py::arg("window") = ::gr::filter::firdes::win_type::WIN_HAMMING,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, band_reject))


        .def_static("band_reject_2",
                    &firdes::band_reject_2,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("low_cutoff_freq"),
                    py::arg("high_cutoff_freq"),
                    py::arg("transition_width"),
                    py::arg("attenuation_dB"),
                    py::arg("window") = ::gr::filter::firdes::win_type::WIN_HAMMING,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, band_reject_2))


        .def_static("hilbert",
                    &firdes::hilbert,
                    py::arg("ntaps") = 19,
                    py::arg("windowtype") =
                        ::gr::filter::firdes::win_type::WIN_RECTANGULAR,
                    py::arg("beta") = 6.7599999999999998,
                    D(firdes, hilbert))


        .def_static("root_raised_cosine",
                    &firdes::root_raised_cosine,
                    py::arg("gain"),
                    py::arg("sampling_freq"),
                    py::arg("symbol_rate"),
                    py::arg("alpha"),
                    py::arg("ntaps"),
                    D(firdes, root_raised_cosine))


        .def_static("gaussian",
                    &firdes::gaussian,
                    py::arg("gain"),
                    py::arg("spb"),
                    py::arg("bt"),
                    py::arg("ntaps"),
                    D(firdes, gaussian))

        ;
}
