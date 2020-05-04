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

#include <gnuradio/trellis/encoder.h>
// pydoc.h is automatically generated in the build directory
#include <encoder_pydoc.h>

template <class IN_T, class OUT_T>
void bind_encoder_template(py::module& m, const char* classname)
{
    using encoder = gr::trellis::encoder<IN_T, OUT_T>;

    py::class_<encoder,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<encoder>>(m, classname)
        .def(py::init(&gr::trellis::encoder<IN_T, OUT_T>::make),
             py::arg("FSM"),
             py::arg("ST"),
             py::arg("K") = 0)
        .def("FSM", &gr::trellis::encoder<IN_T, OUT_T>::FSM)
        .def("ST", &gr::trellis::encoder<IN_T, OUT_T>::ST)
        .def("K", &gr::trellis::encoder<IN_T, OUT_T>::K)
        .def("set_FSM", &gr::trellis::encoder<IN_T, OUT_T>::set_FSM)
        .def("set_ST", &gr::trellis::encoder<IN_T, OUT_T>::set_ST)
        .def("set_K", &gr::trellis::encoder<IN_T, OUT_T>::set_K);
}

void bind_encoder(py::module& m)
{
    bind_encoder_template<std::uint8_t, std::uint8_t>(m, "encoder_bb");
    bind_encoder_template<std::uint8_t, std::int16_t>(m, "encoder_bs");
    bind_encoder_template<std::uint8_t, std::int32_t>(m, "encoder_bi");
    bind_encoder_template<std::int16_t, std::int16_t>(m, "encoder_ss");
    bind_encoder_template<std::int16_t, std::int32_t>(m, "encoder_si");
    bind_encoder_template<std::int32_t, std::int32_t>(m, "encoder_ii");
}
