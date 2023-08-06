#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/float.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/__builtin__/tuple.hpp>
namespace __pythran_util_pythran
{
  struct compute_Frot
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type1;
      typedef typename pythonic::assignable<decltype((std::declval<__type0>() + std::declval<__type1>()))>::type __type2;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type3;
      typedef typename __combined<__type2,__type3>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type5;
      typedef decltype((std::declval<__type4>() * std::declval<__type5>())) __type6;
      typedef decltype((-std::declval<__type4>())) __type7;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type8;
      typedef decltype((std::declval<__type7>() * std::declval<__type8>())) __type9;
      typedef __type0 __ptype0;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type6>(), std::declval<__type9>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& rot, argument_type1&& ux, argument_type2&& uy, argument_type3&& f) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename compute_Frot::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type compute_Frot::operator()(argument_type0&& rot, argument_type1&& ux, argument_type2&& uy, argument_type3&& f) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type1;
    typedef typename pythonic::assignable<decltype((std::declval<__type0>() + std::declval<__type1>()))>::type __type2;
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type>::type __type3;
    typename pythonic::assignable<typename __combined<__type2,__type3>::type>::type rot_abs;
    if ((f != 0L))
    {
      rot_abs = (rot + f);
    }
    else
    {
      rot_abs = rot;
    }
    ;
    ;
    return pythonic::types::make_tuple((rot_abs * uy), ((-rot_abs) * ux));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot0(pythonic::types::ndarray<double,2>&& rot, pythonic::types::ndarray<double,2>&& ux, pythonic::types::ndarray<double,2>&& uy, double&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot1(pythonic::types::ndarray<double,2>&& rot, pythonic::types::ndarray<double,2>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, double&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot2(pythonic::types::ndarray<double,2>&& rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::ndarray<double,2>&& uy, double&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot3(pythonic::types::ndarray<double,2>&& rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, double&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot4(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rot, pythonic::types::ndarray<double,2>&& ux, pythonic::types::ndarray<double,2>&& uy, double&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot5(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rot, pythonic::types::ndarray<double,2>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, double&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot6(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::ndarray<double,2>&& uy, double&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot7(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, double&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, long>::result_type compute_Frot8(pythonic::types::ndarray<double,2>&& rot, pythonic::types::ndarray<double,2>&& ux, pythonic::types::ndarray<double,2>&& uy, long&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, long>::result_type compute_Frot9(pythonic::types::ndarray<double,2>&& rot, pythonic::types::ndarray<double,2>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, long&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, long>::result_type compute_Frot10(pythonic::types::ndarray<double,2>&& rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::ndarray<double,2>&& uy, long&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, long>::result_type compute_Frot11(pythonic::types::ndarray<double,2>&& rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, long&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, long>::result_type compute_Frot12(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rot, pythonic::types::ndarray<double,2>&& ux, pythonic::types::ndarray<double,2>&& uy, long&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, long>::result_type compute_Frot13(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rot, pythonic::types::ndarray<double,2>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, long&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, long>::result_type compute_Frot14(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::ndarray<double,2>&& uy, long&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, long>::result_type compute_Frot15(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, long&& f) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(rot, ux, uy, f);
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
__pythran_wrap_compute_Frot0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<double>(args_obj[3]))
        return to_python(compute_Frot0(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<double>(args_obj[3]))
        return to_python(compute_Frot1(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<double>(args_obj[3]))
        return to_python(compute_Frot2(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<double>(args_obj[3]))
        return to_python(compute_Frot3(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<double>(args_obj[3]))
        return to_python(compute_Frot4(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<double>(args_obj[3]))
        return to_python(compute_Frot5(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<double>(args_obj[3]))
        return to_python(compute_Frot6(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<double>(args_obj[3]))
        return to_python(compute_Frot7(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot8(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_Frot8(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot9(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_Frot9(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot10(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_Frot10(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot11(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_Frot11(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot12(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_Frot12(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot13(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_Frot13(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot14(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_Frot14(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot15(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"rot","ux","uy","f", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_Frot15(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_Frot(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_Frot0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot7(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot8(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot9(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot10(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot11(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot12(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot13(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot14(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_Frot15(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_Frot", "   compute_Frot(float64[][],float64[][],float64[][],float)\n   compute_Frot(float64[][],float64[][],float64[][].T,float)\n   compute_Frot(float64[][],float64[][].T,float64[][],float)\n   compute_Frot(float64[][],float64[][].T,float64[][].T,float)\n   compute_Frot(float64[][].T,float64[][],float64[][],float)\n   compute_Frot(float64[][].T,float64[][],float64[][].T,float)\n   compute_Frot(float64[][].T,float64[][].T,float64[][],float)\n   compute_Frot(float64[][].T,float64[][].T,float64[][].T,float)\n   compute_Frot(float64[][],float64[][],float64[][],int)\n   compute_Frot(float64[][],float64[][],float64[][].T,int)\n   compute_Frot(float64[][],float64[][].T,float64[][],int)\n   compute_Frot(float64[][],float64[][].T,float64[][].T,int)\n   compute_Frot(float64[][].T,float64[][],float64[][],int)\n   compute_Frot(float64[][].T,float64[][],float64[][].T,int)\n   compute_Frot(float64[][].T,float64[][].T,float64[][],int)\n   compute_Frot(float64[][].T,float64[][].T,float64[][].T,int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_Frot",
    (PyCFunction)__pythran_wrapall_compute_Frot,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - compute_Frot(float64[][], float64[][], float64[][], float)\n    - compute_Frot(float64[][], float64[][], float64[][].T, float)\n    - compute_Frot(float64[][], float64[][].T, float64[][], float)\n    - compute_Frot(float64[][], float64[][].T, float64[][].T, float)\n    - compute_Frot(float64[][].T, float64[][], float64[][], float)\n    - compute_Frot(float64[][].T, float64[][], float64[][].T, float)\n    - compute_Frot(float64[][].T, float64[][].T, float64[][], float)\n    - compute_Frot(float64[][].T, float64[][].T, float64[][].T, float)\n    - compute_Frot(float64[][], float64[][], float64[][], int)\n    - compute_Frot(float64[][], float64[][], float64[][].T, int)\n    - compute_Frot(float64[][], float64[][].T, float64[][], int)\n    - compute_Frot(float64[][], float64[][].T, float64[][].T, int)\n    - compute_Frot(float64[][].T, float64[][], float64[][], int)\n    - compute_Frot(float64[][].T, float64[][], float64[][].T, int)\n    - compute_Frot(float64[][].T, float64[][].T, float64[][], int)\n    - compute_Frot(float64[][].T, float64[][].T, float64[][].T, int)\nCompute cross-product of absolute potential vorticity with velocity."},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "util_pythran",            /* m_name */
    "",         /* m_doc */
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
PYTHRAN_MODULE_INIT(util_pythran)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(util_pythran)(void) {
    #ifdef PYTHONIC_TYPES_NDARRAY_HPP
        import_array()
    #endif
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("util_pythran",
                                         Methods,
                                         ""
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.8.4post0",
                                      "2018-03-11 15:14:23.864108",
                                      "4bb05a458d88c75200005ec8594c65a67cc3fb8319cd0efe65addebe842a7afb");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif