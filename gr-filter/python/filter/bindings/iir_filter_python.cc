/*
 * Copyright 2020 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(iir_filter.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(13dec42f09e2dd232a8c7872db83c6a8)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/filter/iir_filter.h>
// pydoc.h is automatically generated in the build directory
#include <iir_filter_pydoc.h>

void bind_iir_filter(py::module& m)
{


    py::module m_kernel = m.def_submodule("kernel");

    using iir_filter<std::complex<float>,
                     std::complex<float>,
                     float,
                     std::complex<float>> = ::gr::filter::kernel::
        iir_filter<std::complex<float>, std::complex<float>, float, std::complex<float>>;
    using iir_filter<std::complex<float>,
                     std::complex<float>,
                     double,
                     std::complex<double>> =
        ::gr::filter::kernel::iir_filter<std::complex<float>,
                                         std::complex<float>,
                                         double,
                                         std::complex<double>>;
    using iir_filter<std::complex<float>,
                     std::complex<float>,
                     std::complex<double>,
                     std::complex<double>> =
        ::gr::filter::kernel::iir_filter<std::complex<float>,
                                         std::complex<float>,
                                         std::complex<double>,
                                         std::complex<double>>;


    py::class_<
        iir_filter<std::complex<float>, std::complex<float>, float, std::complex<float>>,
        std::shared_ptr<iir_filter<std::complex<float>,
                                   std::complex<float>,
                                   float,
                                   std::complex<float>>>>(
        m_kernel,
        "iir_filter<std::complex<float>, std::complex<float>, float, std::complex<float> "
        ">",
        D(kernel,
          iir_filter<std::complex<float>,
                     std::complex<float>,
                     float,
                     std::complex<float>>))


        .def("filter",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         float,
                         std::complex<float>>::filter,
             py::arg("input"),
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          float,
                          std::complex<float>>,
               filter))


        .def("filter_n",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         float,
                         std::complex<float>>::filter_n,
             py::arg("output"),
             py::arg("input"),
             py::arg("n"),
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          float,
                          std::complex<float>>,
               filter_n))


        .def("ntaps_ff",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         float,
                         std::complex<float>>::ntaps_ff,
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          float,
                          std::complex<float>>,
               ntaps_ff))


        .def("ntaps_fb",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         float,
                         std::complex<float>>::ntaps_fb,
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          float,
                          std::complex<float>>,
               ntaps_fb))


        .def("set_taps",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         float,
                         std::complex<float>>::set_taps,
             py::arg("fftaps"),
             py::arg("fbtaps"),
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          float,
                          std::complex<float>>,
               set_taps))

        ;


    py::class_<iir_filter<std::complex<float>,
                          std::complex<float>,
                          double,
                          std::complex<double>>,
               std::shared_ptr<iir_filter<std::complex<float>,
                                          std::complex<float>,
                                          double,
                                          std::complex<double>>>>(
        m_kernel,
        "iir_filter<std::complex<float>, std::complex<float>, double, "
        "std::complex<double> >",
        D(kernel,
          iir_filter<std::complex<float>,
                     std::complex<float>,
                     double,
                     std::complex<double>>))


        .def("filter",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         double,
                         std::complex<double>>::filter,
             py::arg("input"),
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          double,
                          std::complex<double>>,
               filter))


        .def("filter_n",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         double,
                         std::complex<double>>::filter_n,
             py::arg("output"),
             py::arg("input"),
             py::arg("n"),
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          double,
                          std::complex<double>>,
               filter_n))


        .def("ntaps_ff",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         double,
                         std::complex<double>>::ntaps_ff,
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          double,
                          std::complex<double>>,
               ntaps_ff))


        .def("ntaps_fb",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         double,
                         std::complex<double>>::ntaps_fb,
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          double,
                          std::complex<double>>,
               ntaps_fb))


        .def("set_taps",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         double,
                         std::complex<double>>::set_taps,
             py::arg("fftaps"),
             py::arg("fbtaps"),
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          double,
                          std::complex<double>>,
               set_taps))

        ;


    py::class_<iir_filter<std::complex<float>,
                          std::complex<float>,
                          std::complex<double>,
                          std::complex<double>>,
               std::shared_ptr<iir_filter<std::complex<float>,
                                          std::complex<float>,
                                          std::complex<double>,
                                          std::complex<double>>>>(
        m_kernel,
        "iir_filter<std::complex<float>, std::complex<float>, std::complex<double>, "
        "std::complex<double> >",
        D(kernel,
          iir_filter<std::complex<float>,
                     std::complex<float>,
                     std::complex<double>,
                     std::complex<double>>))


        .def("filter",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         std::complex<double>,
                         std::complex<double>>::filter,
             py::arg("input"),
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          std::complex<double>,
                          std::complex<double>>,
               filter))


        .def("filter_n",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         std::complex<double>,
                         std::complex<double>>::filter_n,
             py::arg("output"),
             py::arg("input"),
             py::arg("n"),
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          std::complex<double>,
                          std::complex<double>>,
               filter_n))


        .def("ntaps_ff",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         std::complex<double>,
                         std::complex<double>>::ntaps_ff,
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          std::complex<double>,
                          std::complex<double>>,
               ntaps_ff))


        .def("ntaps_fb",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         std::complex<double>,
                         std::complex<double>>::ntaps_fb,
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          std::complex<double>,
                          std::complex<double>>,
               ntaps_fb))


        .def("set_taps",
             &iir_filter<std::complex<float>,
                         std::complex<float>,
                         std::complex<double>,
                         std::complex<double>>::set_taps,
             py::arg("fftaps"),
             py::arg("fbtaps"),
             D(kernel,
               iir_filter<std::complex<float>,
                          std::complex<float>,
                          std::complex<double>,
                          std::complex<double>>,
               set_taps))

        ;
}
