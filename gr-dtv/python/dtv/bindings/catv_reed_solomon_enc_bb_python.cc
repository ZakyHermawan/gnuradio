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

#include <gnuradio/dtv/catv_reed_solomon_enc_bb.h>
// pydoc.h is automatically generated in the build directory
#include <catv_reed_solomon_enc_bb_pydoc.h>

void bind_catv_reed_solomon_enc_bb(py::module& m)
{

    using catv_reed_solomon_enc_bb = ::gr::dtv::catv_reed_solomon_enc_bb;


    py::class_<catv_reed_solomon_enc_bb,
               gr::block,
               gr::basic_block,
               std::shared_ptr<catv_reed_solomon_enc_bb>>(
        m, "catv_reed_solomon_enc_bb", D(catv_reed_solomon_enc_bb))

        .def(py::init(&catv_reed_solomon_enc_bb::make), D(catv_reed_solomon_enc_bb, make))


        ;
}
