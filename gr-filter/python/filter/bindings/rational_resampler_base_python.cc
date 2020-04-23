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

#include <gnuradio/filter/rational_resampler_base.h>

template <class IN_T, class OUT_T, class TAP_T>
void bind_rational_resampler_base_template(py::module& m, const char* classname)
{
    using rational_resampler_base =
        gr::filter::rational_resampler_base<IN_T, OUT_T, TAP_T>;

    py::class_<rational_resampler_base,
               gr::block,
               gr::basic_block,
               std::shared_ptr<rational_resampler_base>>(m, classname)
        .def(py::init(&gr::filter::rational_resampler_base<IN_T, OUT_T, TAP_T>::make),
             py::arg("interpolation"),
             py::arg("decimation"),
             py::arg("taps"))

        .def("set_taps", &rational_resampler_base::set_taps, py::arg("taps"))
        .def("taps", &rational_resampler_base::taps)
        .def("interpolation", &rational_resampler_base::interpolation)
        .def("decimation", &rational_resampler_base::decimation);
}

void bind_rational_resampler_base(py::module& m)
{
    bind_rational_resampler_base_template<gr_complex, gr_complex, gr_complex>(
        m, "rational_resampler_base_ccc");
    bind_rational_resampler_base_template<gr_complex, gr_complex, float>(
        m, "rational_resampler_base_ccf");
    bind_rational_resampler_base_template<float, gr_complex, gr_complex>(
        m, "rational_resampler_base_fcc");
    bind_rational_resampler_base_template<float, float, float>(
        m, "rational_resampler_base_fff");
    bind_rational_resampler_base_template<float, std::int16_t, float>(
        m, "rational_resampler_base_fsf");
    bind_rational_resampler_base_template<std::int16_t, gr_complex, gr_complex>(
        m, "rational_resampler_base_scc");
}
