#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/uint8.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/types/uint8.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/__builtin__/None.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/__builtin__/None.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/types/str.hpp>
namespace __pythran_util3d_pythran
{
  struct dealiasing_variable
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<__type2>())) __type3;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type3>::type>::type __type4;
      typedef typename pythonic::lazy<__type4>::type __type5;
      typedef decltype(std::declval<__type1>()(std::declval<__type5>())) __type6;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type6>::type::iterator>::value_type>::type __type7;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type __type8;
      typedef typename pythonic::lazy<__type8>::type __type9;
      typedef decltype(std::declval<__type1>()(std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type3>::type>::type __type12;
      typedef typename pythonic::lazy<__type12>::type __type13;
      typedef decltype(std::declval<__type1>()(std::declval<__type13>())) __type14;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type11>(), std::declval<__type15>())) __type16;
      typedef __type0 __ptype0;
      typedef __type16 __ptype1;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& ff_fft, argument_type1&& where_dealiased) const
    ;
  }  ;
  struct dealiasing_setofvar
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<__type2>())) __type3;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type3>::type>::type __type4;
      typedef typename pythonic::lazy<__type4>::type __type5;
      typedef decltype(std::declval<__type1>()(std::declval<__type5>())) __type6;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type6>::type::iterator>::value_type>::type __type7;
      typedef typename std::tuple_element<1,typename std::remove_reference<__type3>::type>::type __type8;
      typedef typename pythonic::lazy<__type8>::type __type9;
      typedef decltype(std::declval<__type1>()(std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
      typedef typename std::tuple_element<2,typename std::remove_reference<__type3>::type>::type __type12;
      typedef typename pythonic::lazy<__type12>::type __type13;
      typedef decltype(std::declval<__type1>()(std::declval<__type13>())) __type14;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
      typedef typename std::tuple_element<3,typename std::remove_reference<__type3>::type>::type __type16;
      typedef typename pythonic::lazy<__type16>::type __type17;
      typedef decltype(std::declval<__type1>()(std::declval<__type17>())) __type18;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type18>::type::iterator>::value_type>::type __type19;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type11>(), std::declval<__type15>(), std::declval<__type19>())) __type20;
      typedef __type0 __ptype4;
      typedef __type20 __ptype5;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& sov, argument_type1&& where_dealiased) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 >
  typename dealiasing_variable::type<argument_type0, argument_type1>::result_type dealiasing_variable::operator()(argument_type0&& ff_fft, argument_type1&& where_dealiased) const
  {
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(ff_fft)))>::type n0 = std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(ff_fft));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(ff_fft)))>::type n1 = std::get<1>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(ff_fft));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(ff_fft)))>::type n2 = std::get<2>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(ff_fft));
    {
      long  __target1 = n0;
      for (long  i0=0L; i0 < __target1; i0 += 1L)
      {
        {
          long  __target2 = n1;
          for (long  i1=0L; i1 < __target2; i1 += 1L)
          {
            {
              long  __target3 = n2;
              for (long  i2=0L; i2 < __target3; i2 += 1L)
              {
                if (where_dealiased.fast(pythonic::types::make_tuple(i0, i1, i2)))
                {
                  ff_fft.fast(pythonic::types::make_tuple(i0, i1, i2)) = 0.0;
                }
              }
            }
          }
        }
      }
    }
    return pythonic::__builtin__::None;
  }
  template <typename argument_type0 , typename argument_type1 >
  typename dealiasing_setofvar::type<argument_type0, argument_type1>::result_type dealiasing_setofvar::operator()(argument_type0&& sov, argument_type1&& where_dealiased) const
  {
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(sov)))>::type nk = std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(sov));
    typename pythonic::lazy<decltype(std::get<1>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(sov)))>::type n0 = std::get<1>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(sov));
    typename pythonic::lazy<decltype(std::get<2>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(sov)))>::type n1 = std::get<2>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(sov));
    typename pythonic::lazy<decltype(std::get<3>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(sov)))>::type n2 = std::get<3>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(sov));
    {
      long  __target1 = n0;
      for (long  i0=0L; i0 < __target1; i0 += 1L)
      {
        {
          long  __target2 = n1;
          for (long  i1=0L; i1 < __target2; i1 += 1L)
          {
            {
              long  __target3 = n2;
              for (long  i2=0L; i2 < __target3; i2 += 1L)
              {
                if (where_dealiased.fast(pythonic::types::make_tuple(i0, i1, i2)))
                {
                  {
                    long  __target4 = nk;
                    for (long  ik=0L; ik < __target4; ik += 1L)
                    {
                      sov.fast(pythonic::types::make_tuple(ik, i0, i1, i2)) = 0.0;
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    return pythonic::__builtin__::None;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_util3d_pythran::dealiasing_variable::type<pythonic::types::ndarray<std::complex<double>,3>, pythonic::types::ndarray<uint8_t,3>>::result_type dealiasing_variable0(pythonic::types::ndarray<std::complex<double>,3>&& ff_fft, pythonic::types::ndarray<uint8_t,3>&& where_dealiased) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util3d_pythran::dealiasing_variable()(ff_fft, where_dealiased);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util3d_pythran::dealiasing_setofvar::type<pythonic::types::ndarray<std::complex<double>,4>, pythonic::types::ndarray<uint8_t,3>>::result_type dealiasing_setofvar0(pythonic::types::ndarray<std::complex<double>,4>&& sov, pythonic::types::ndarray<uint8_t,3>&& where_dealiased) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util3d_pythran::dealiasing_setofvar()(sov, where_dealiased);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}

static PyObject *
__pythran_wrap_dealiasing_variable0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"ff_fft","where_dealiased", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,3>>(args_obj[1]))
        return to_python(dealiasing_variable0(from_python<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,3>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_dealiasing_setofvar0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"sov","where_dealiased", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,4>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,3>>(args_obj[1]))
        return to_python(dealiasing_setofvar0(from_python<pythonic::types::ndarray<std::complex<double>,4>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,3>>(args_obj[1])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_dealiasing_variable(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_dealiasing_variable0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "dealiasing_variable", "   dealiasing_variable(complex128[][][],uint8[][][])", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_dealiasing_setofvar(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_dealiasing_setofvar0(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "dealiasing_setofvar", "   dealiasing_setofvar(complex128[][][][],uint8[][][])", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "dealiasing_variable",
    (PyCFunction)__pythran_wrapall_dealiasing_variable,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - dealiasing_variable(complex128[][][], uint8[][][])\ndealiasing 3d array"},{
    "dealiasing_setofvar",
    (PyCFunction)__pythran_wrapall_dealiasing_setofvar,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - dealiasing_setofvar(complex128[][][][], uint8[][][])\ndealiasing 3d setofvar object"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "util3d_pythran",            /* m_name */
    "\nPythran compatible functions: 3d operators (:mod:`fluidsim.operators.util3d_pythran`)\n=====================================================================================\n\n.. autofunction:: dealiasing_setofvar\n\n.. autofunction:: dealiasing_variable\n\n",         /* m_doc */
    -1,                  /* m_size */
    Methods,             /* m_methods */
    NULL,                /* m_reload */
    NULL,                /* m_traverse */
    NULL,                /* m_clear */
    NULL,                /* m_free */
  };
#define PYTHRAN_RETURN return theModule
#define PYTHRAN_MODULE_INIT(s) PyInit_##s
#else
#define PYTHRAN_RETURN return
#define PYTHRAN_MODULE_INIT(s) init##s
#endif
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(util3d_pythran)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(util3d_pythran)(void) {
    #ifdef PYTHONIC_TYPES_NDARRAY_HPP
        import_array()
    #endif
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("util3d_pythran",
                                         Methods,
                                         "\nPythran compatible functions: 3d operators (:mod:`fluidsim.operators.util3d_pythran`)\n=====================================================================================\n\n.. autofunction:: dealiasing_setofvar\n\n.. autofunction:: dealiasing_variable\n\n"
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.8.4post0",
                                      "2018-03-13 19:12:44.184982",
                                      "aadadbef22297f66c636e094f0ab009e2b9a3a9b2025f9c078807eb63ae79bfd");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif