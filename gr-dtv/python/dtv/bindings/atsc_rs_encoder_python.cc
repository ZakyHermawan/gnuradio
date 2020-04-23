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

#include <gnuradio/dtv/atsc_rs_encoder.h>
// pydoc.h is automatically generated in the build directory
#include <atsc_rs_encoder_pydoc.h>

void bind_atsc_rs_encoder(py::module& m)
{

    using atsc_rs_encoder = ::gr::dtv::atsc_rs_encoder;


    py::class_<atsc_rs_encoder,
               gr::sync_block,
               gr::block,
               gr::basic_block,
               std::shared_ptr<atsc_rs_encoder>>(m, "atsc_rs_encoder", D(atsc_rs_encoder))

        .def(py::init(&atsc_rs_encoder::make), D(atsc_rs_encoder, make))


        ;
}
