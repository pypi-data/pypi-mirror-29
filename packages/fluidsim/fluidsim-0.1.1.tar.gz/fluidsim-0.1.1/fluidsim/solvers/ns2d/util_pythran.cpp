#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/float.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/types/float.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
namespace __pythran_util_pythran
{
  struct compute_Frot
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 = long>
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef decltype((-std::declval<__type0>())) __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type2;
      typedef decltype((std::declval<__type1>() * std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type5;
      typedef decltype((std::declval<__type4>() * std::declval<__type5>())) __type6;
      typedef decltype((std::declval<__type3>() - std::declval<__type6>())) __type7;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type8;
      typedef decltype((std::declval<__type5>() + std::declval<__type8>())) __type9;
      typedef decltype((std::declval<__type4>() * std::declval<__type9>())) __type10;
      typedef decltype((std::declval<__type3>() - std::declval<__type10>())) __type11;
      typedef typename pythonic::returnable<typename __combined<__type7,__type11>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 = long>
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type operator()(argument_type0&& ux, argument_type1&& uy, argument_type2&& px_rot, argument_type3&& py_rot, argument_type4 beta= 0L) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
  typename compute_Frot::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type compute_Frot::operator()(argument_type0&& ux, argument_type1&& uy, argument_type2&& px_rot, argument_type3&& py_rot, argument_type4 beta) const
  {
    if ((beta == 0L))
    {
      return (((-ux) * px_rot) - (uy * py_rot));
    }
    else
    {
      return (((-ux) * px_rot) - (uy * (py_rot + beta)));
    }
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot0(pythonic::types::ndarray<double,2>&& ux, pythonic::types::ndarray<double,2>&& uy, pythonic::types::ndarray<double,2>&& px_rot, pythonic::types::ndarray<double,2>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot1(pythonic::types::ndarray<double,2>&& ux, pythonic::types::ndarray<double,2>&& uy, pythonic::types::ndarray<double,2>&& px_rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot2(pythonic::types::ndarray<double,2>&& ux, pythonic::types::ndarray<double,2>&& uy, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& px_rot, pythonic::types::ndarray<double,2>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot3(pythonic::types::ndarray<double,2>&& ux, pythonic::types::ndarray<double,2>&& uy, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& px_rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot4(pythonic::types::ndarray<double,2>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, pythonic::types::ndarray<double,2>&& px_rot, pythonic::types::ndarray<double,2>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot5(pythonic::types::ndarray<double,2>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, pythonic::types::ndarray<double,2>&& px_rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot6(pythonic::types::ndarray<double,2>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& px_rot, pythonic::types::ndarray<double,2>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot7(pythonic::types::ndarray<double,2>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& px_rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot8(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::ndarray<double,2>&& uy, pythonic::types::ndarray<double,2>&& px_rot, pythonic::types::ndarray<double,2>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot9(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::ndarray<double,2>&& uy, pythonic::types::ndarray<double,2>&& px_rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot10(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::ndarray<double,2>&& uy, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& px_rot, pythonic::types::ndarray<double,2>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot11(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::ndarray<double,2>&& uy, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& px_rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot12(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, pythonic::types::ndarray<double,2>&& px_rot, pythonic::types::ndarray<double,2>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot13(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, pythonic::types::ndarray<double,2>&& px_rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double>::result_type compute_Frot14(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& px_rot, pythonic::types::ndarray<double,2>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_Frot::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double>::result_type compute_Frot15(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& ux, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& uy, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& px_rot, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& py_rot, double&& beta) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_Frot()(ux, uy, px_rot, py_rot, beta);
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
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot0(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot1(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot2(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot3(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot4(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot5(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot6(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot7(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot8(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot8(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot9(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot9(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot10(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot10(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot11(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot11(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot12(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot12(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot13(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot13(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot14(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot14(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3]), from_python<double>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_Frot15(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"ux","uy","px_rot","py_rot","beta", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]) && is_convertible<double>(args_obj[4]))
        return to_python(compute_Frot15(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]), from_python<double>(args_obj[4])));
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
                               "compute_Frot", "   compute_Frot(float64[][],float64[][],float64[][],float64[][],float)\n   compute_Frot(float64[][],float64[][],float64[][],float64[][].T,float)\n   compute_Frot(float64[][],float64[][],float64[][].T,float64[][],float)\n   compute_Frot(float64[][],float64[][],float64[][].T,float64[][].T,float)\n   compute_Frot(float64[][],float64[][].T,float64[][],float64[][],float)\n   compute_Frot(float64[][],float64[][].T,float64[][],float64[][].T,float)\n   compute_Frot(float64[][],float64[][].T,float64[][].T,float64[][],float)\n   compute_Frot(float64[][],float64[][].T,float64[][].T,float64[][].T,float)\n   compute_Frot(float64[][].T,float64[][],float64[][],float64[][],float)\n   compute_Frot(float64[][].T,float64[][],float64[][],float64[][].T,float)\n   compute_Frot(float64[][].T,float64[][],float64[][].T,float64[][],float)\n   compute_Frot(float64[][].T,float64[][],float64[][].T,float64[][].T,float)\n   compute_Frot(float64[][].T,float64[][].T,float64[][],float64[][],float)\n   compute_Frot(float64[][].T,float64[][].T,float64[][],float64[][].T,float)\n   compute_Frot(float64[][].T,float64[][].T,float64[][].T,float64[][],float)\n   compute_Frot(float64[][].T,float64[][].T,float64[][].T,float64[][].T,float)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_Frot",
    (PyCFunction)__pythran_wrapall_compute_Frot,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - compute_Frot(float64[][], float64[][], float64[][], float64[][], float)\n    - compute_Frot(float64[][], float64[][], float64[][], float64[][].T, float)\n    - compute_Frot(float64[][], float64[][], float64[][].T, float64[][], float)\n    - compute_Frot(float64[][], float64[][], float64[][].T, float64[][].T, float)\n    - compute_Frot(float64[][], float64[][].T, float64[][], float64[][], float)\n    - compute_Frot(float64[][], float64[][].T, float64[][], float64[][].T, float)\n    - compute_Frot(float64[][], float64[][].T, float64[][].T, float64[][], float)\n    - compute_Frot(float64[][], float64[][].T, float64[][].T, float64[][].T, float)\n    - compute_Frot(float64[][].T, float64[][], float64[][], float64[][], float)\n    - compute_Frot(float64[][].T, float64[][], float64[][], float64[][].T, float)\n    - compute_Frot(float64[][].T, float64[][], float64[][].T, float64[][], float)\n    - compute_Frot(float64[][].T, float64[][], float64[][].T, float64[][].T, float)\n    - compute_Frot(float64[][].T, float64[][].T, float64[][], float64[][], float)\n    - compute_Frot(float64[][].T, float64[][].T, float64[][], float64[][].T, float)\n    - compute_Frot(float64[][].T, float64[][].T, float64[][].T, float64[][], float)\n    - compute_Frot(float64[][].T, float64[][].T, float64[][].T, float64[][].T, float)\n"},
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
                                      "2018-03-13 19:12:42.943571",
                                      "cf6c749a4de7b866f7e367901baac0224e767f024cc073bba687c25d61462c12");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif