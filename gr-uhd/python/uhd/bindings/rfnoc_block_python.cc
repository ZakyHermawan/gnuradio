/*
 * Copyright 2021 Free Software Foundation, Inc.
 *
 * This file is part of GNU Radio
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 */

/***********************************************************************************/
/* This file is automatically generated using bindtool and can be manually edited  */
/* The following lines can be configured to regenerate this file during cmake      */
/* If manual edits are made, the following tags should be modified accordingly.    */
/* BINDTOOL_GEN_AUTOMATIC(0)                                                       */
/* BINDTOOL_USE_PYGCCXML(0)                                                        */
/* BINDTOOL_HEADER_FILE(rfnoc_block.h)                                        */
/* BINDTOOL_HEADER_FILE_HASH(f40d30390fa95d19fae4a12893817614)                     */
/***********************************************************************************/

#include <pybind11/complex.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

#include <gnuradio/uhd/rfnoc_block.h>
// pydoc.h is automatically generated in the build directory
#include <rfnoc_block_pydoc.h>

void bind_rfnoc_block(py::module& m)
{

    using rfnoc_block = ::gr::uhd::rfnoc_block;


    py::class_<rfnoc_block, gr::block, gr::basic_block, std::shared_ptr<rfnoc_block>>(
        m, "rfnoc_block", D(rfnoc_block))


        .def_static("make_block_ref",
                    &rfnoc_block::make_block_ref,
                    py::arg("graph"),
                    py::arg("block_args"),
                    py::arg("block_name"),
                    py::arg("device_select") = -1,
                    py::arg("block_select") = -1,
                    py::arg("max_ref_count") = 1,
                    D(rfnoc_block, make_block_ref))


        .def("get_unique_id", &rfnoc_block::get_unique_id, D(rfnoc_block, get_unique_id))


        .def("set_properties",
             &rfnoc_block::set_properties,
             py::arg("props"),
             py::arg("instance") = 0,
             D(rfnoc_block, set_properties))


        // clang-format off
        .def(
            "set_property",
            [](rfnoc_block& self,
               const std::string& name,
               py::object& value,
               const size_t port,
               const std::string& type_hint) {

                // Note: set_property<> is a templated function in C++. For
                // maximum Pythonicity, we will try and keep things simple by
                // faking the templated nature of set_property.
                // This means we don't know what type 'value' is, and we have to
                // take a guess -- unless the user was kind enough to give us a
                // type hint.
                std::string type = type_hint;

                // First, we see if a type hint was provided that we understand,
                // but that C++ does not understand, and sanitize accordingly.
#define _SANITIZE_TYPE(typename, sanitized_tn) \
                if (type == #typename) { \
                    type = #sanitized_tn; \
                }
                _SANITIZE_TYPE(string, std::string)

                // If no type hint was provided, we infer the type by trying to
                // cast the py::object to various types.
#define _INFER_TYPE(typename) \
                if (type.empty()) { \
                    try { \
                        typename __val = value.cast<typename>(); \
                        type = #typename; \
                    } catch (const py::cast_error&) { \
                        /* pass */ \
                    } \
                }
                _INFER_TYPE(int)
                _INFER_TYPE(double)
                _INFER_TYPE(std::string)
                _INFER_TYPE(bool)

                // At this point, 'type' must be set or we throw an exception
                // (see the first 'if' clause). If it's set, we cast 'value' to
                // the desired type and call set_property<>() in C++-land.
#define _SET_PROP_WITH_TYPE(typename) \
                else if (type == #typename) { \
                    self.set_property<typename>(name, value.cast<typename>(), port); \
                }
                if (type.empty()) {
                    throw std::runtime_error("rfnoc_block::set_property(): Could not infer "
                                             "property type when setting property " +
                                             name + " on port " + std::to_string(port) + "!");
                }
                _SET_PROP_WITH_TYPE(bool)
                _SET_PROP_WITH_TYPE(int)
                _SET_PROP_WITH_TYPE(float)
                _SET_PROP_WITH_TYPE(double)
                _SET_PROP_WITH_TYPE(uint64_t)
                _SET_PROP_WITH_TYPE(uint32_t)
                _SET_PROP_WITH_TYPE(std::string)
                else {
                    throw std::runtime_error(
                        "rfnoc_block::set_property(): Invalid property type " + type + "!");
                }

                return;
            },
            py::arg("name"),
            py::arg("value"),
            py::arg("port") = 0,
            py::arg("typename") = "",
            D(rfnoc_block, set_property))


        .def(
            "get_property",
            [](rfnoc_block& self,
               const std::string& name,
               const size_t port,
               const std::string& type_hint) -> py::object {
                // Note: get_property<> is a templated function in C++. For
                // maximum Pythonicity, we will try and keep things simple by
                // faking the templated nature of set_property.
                // This means we don't know what type 'value' is, and we have to
                // take a guess -- unless the user was kind enough to give us a
                // type hint.
                std::string type = type_hint;

                // First, we see if a type hint was provided that we understand,
                // but that C++ does not understand, and sanitize accordingly.
#define _SANITIZE_TYPE(typename, sanitized_tn) \
                if (type == #typename) { \
                    type = #sanitized_tn; \
                }
                _SANITIZE_TYPE(string, std::string)


                if (!type.empty()) {
                    // Here, we first use the type_hint on get_property<>, before we
                    // try and infer.
#define _GET_PROP_WITH_TYPE(typename) \
                    if (type == #typename) { \
                        return py::cast(self.get_property<typename>(name, port)); \
                    }
                    _GET_PROP_WITH_TYPE(bool)
                    _GET_PROP_WITH_TYPE(int)
                    _GET_PROP_WITH_TYPE(float)
                    _GET_PROP_WITH_TYPE(double)
                    _GET_PROP_WITH_TYPE(uint64_t)
                    _GET_PROP_WITH_TYPE(uint32_t)
                    _GET_PROP_WITH_TYPE(std::string)
                    // If type wasn't empty, but we reach this line, that means
                    // the user gave us a type hint we can't handle.
                    throw std::runtime_error(
                        "rfnoc_block::get_property(): Invalid property type " + type + "!");
                }

                // If we're here, that means the user didn't give us a type hint
                // and we need to guess the type using RTTI.
#define _RETURN_INFERRED_TYPE(typename) \
                try { \
                    typename value = self.get_property<typename>(name, port); \
                    return py::cast(value); \
                } catch (const uhd::type_error&) { \
                    /* pass */ \
                }
                _RETURN_INFERRED_TYPE(double)
                _RETURN_INFERRED_TYPE(int)
                _RETURN_INFERRED_TYPE(bool)

                // If none of these worked, we give up.
                throw std::runtime_error("rfnoc_block::get_property(): Could not infer "
                                         "property type when setting property " +
                                         name + " on port " + std::to_string(port) + "!");

                return py::none{}; // For some linters
            },
            py::arg("name"),
            py::arg("port") = 0,
            py::arg("typename") = "",
            D(rfnoc_block, set_property))
        // clang-format on


        ;
}
