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

#include <gnuradio/digital/constellation_decoder_cb.h>
// pydoc.h is automatically generated in the build directory
#include <constellation_decoder_cb_pydoc.h>

void bind_constellation_decoder_cb(py::module& m)
{

    using constellation_decoder_cb = ::gr::digital::constellation_decoder_cb;


    py::class_<constellation_decoder_cb,
               gr::block,
               gr::basic_block,
               std::shared_ptr<constellation_decoder_cb>>(
        m, "constellation_decoder_cb", D(constellation_decoder_cb))

        .def(py::init(&constellation_decoder_cb::make),
             py::arg("constellation"),
             D(constellation_decoder_cb, make))


        ;
}
