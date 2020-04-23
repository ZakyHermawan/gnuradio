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

#include <gnuradio/digital/packet_headergenerator_bb.h>
// pydoc.h is automatically generated in the build directory
#include <packet_headergenerator_bb_pydoc.h>

void bind_packet_headergenerator_bb(py::module& m)
{
    using packet_headergenerator_bb = gr::digital::packet_headergenerator_bb;


    py::class_<packet_headergenerator_bb,
               gr::tagged_stream_block,
               std::shared_ptr<packet_headergenerator_bb>>(m, "packet_headergenerator_bb")

        .def(py::init((std::shared_ptr<packet_headergenerator_bb>(*)(
                          const gr::digital::packet_header_default::sptr&,
                          const std::string&)) &
                      packet_headergenerator_bb::make),
             py::arg("header_formatter"),
             py::arg("len_tag_key") = "packet_len",
             D(packet_headergenerator_bb, make, 0))

        .def(py::init((std::shared_ptr<packet_headergenerator_bb>(*)(
                          long, const std::string&)) &
                      packet_headergenerator_bb::make),
             py::arg("header_len"),
             py::arg("len_tag_key") = "packet_len",
             D(packet_headergenerator_bb, make, 1))

        .def("set_header_formatter",
             &packet_headergenerator_bb::set_header_formatter,
             py::arg("header_formatter"),
             D(packet_headergenerator_bb, set_header_formatter));
}
