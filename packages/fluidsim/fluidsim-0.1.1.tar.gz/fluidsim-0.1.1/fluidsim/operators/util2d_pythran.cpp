#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/uint8.hpp>
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/types/uint8.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/__builtin__/None.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/__builtin__/None.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/types/str.hpp>
#include <pythonic/operator_/div.hpp>
namespace __pythran_util2d_pythran
{
  struct compute_increments_dim1
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef pythonic::types::contiguous_slice __type1;
      typedef decltype(std::declval<__type0>()(std::declval<__type1>(), std::declval<__type1>())) __type2;
      typedef typename pythonic::returnable<decltype((std::declval<__type2>() - std::declval<__type2>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& var, argument_type1&& irx) const
    ;
  }  ;
  struct invlaplacian2_fft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename pythonic::assignable<decltype((pythonic::operator_::div(std::declval<__type0>(), std::declval<__type1>())))>::type __type2;
      typedef long __type3;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type3>(), std::declval<__type3>())) __type4;
      typedef indexable<__type4> __type5;
      typedef typename __combined<__type2,__type5>::type __type6;
      typedef double __type7;
      typedef container<typename std::remove_reference<__type7>::type> __type8;
      typedef typename __combined<__type6,__type8>::type __type9;
      typedef typename __combined<__type9,__type5>::type __type10;
      typedef typename pythonic::returnable<typename __combined<__type10,__type8>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& a_fft, argument_type1&& K4_not0, argument_type2&& rank) const
    ;
  }  ;
  struct laplacian2_fft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef typename pythonic::returnable<decltype((std::declval<__type0>() * std::declval<__type1>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 >
    typename type<argument_type0, argument_type1>::result_type operator()(argument_type0&& a_fft, argument_type1&& K4) const
    ;
  }  ;
  struct dealiasing_setofvar
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
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
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type8;
      typedef decltype(std::declval<__type1>()(std::declval<__type8>())) __type9;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type11;
      typedef decltype(std::declval<__type1>()(std::declval<__type11>())) __type12;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type12>::type::iterator>::value_type>::type __type13;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type10>(), std::declval<__type13>())) __type14;
      typedef __type0 __ptype0;
      typedef __type14 __ptype1;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& setofvar_fft, argument_type1&& where, argument_type2&& n0, argument_type3&& n1) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 >
  typename compute_increments_dim1::type<argument_type0, argument_type1>::result_type compute_increments_dim1::operator()(argument_type0&& var, argument_type1&& irx) const
  {
    ;
    typename pythonic::assignable<decltype(std::get<1>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(var)))>::type n1 = std::get<1>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(var));
    ;
    ;
    return (var(pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None),pythonic::types::contiguous_slice(irx,n1)) - var(pythonic::types::contiguous_slice(pythonic::__builtin__::None,pythonic::__builtin__::None),pythonic::types::contiguous_slice(0L,(n1 - irx))));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename invlaplacian2_fft::type<argument_type0, argument_type1, argument_type2>::result_type invlaplacian2_fft::operator()(argument_type0&& a_fft, argument_type1&& K4_not0, argument_type2&& rank) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
    typedef typename pythonic::assignable<decltype((pythonic::operator_::div(std::declval<__type0>(), std::declval<__type1>())))>::type __type2;
    typedef long __type3;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type3>(), std::declval<__type3>())) __type4;
    typedef indexable<__type4> __type5;
    typedef typename __combined<__type2,__type5>::type __type6;
    typedef double __type7;
    typedef container<typename std::remove_reference<__type7>::type> __type8;
    typedef typename __combined<__type6,__type8>::type __type9;
    typename pythonic::assignable<typename __combined<__type9,__type5>::type>::type invlap2_afft = (pythonic::operator_::div(a_fft, K4_not0));
    if ((rank == 0L))
    {
      invlap2_afft.fast(pythonic::types::make_tuple(0L, 0L)) = 0.0;
    }
    return invlap2_afft;
  }
  template <typename argument_type0 , typename argument_type1 >
  typename laplacian2_fft::type<argument_type0, argument_type1>::result_type laplacian2_fft::operator()(argument_type0&& a_fft, argument_type1&& K4) const
  {
    return (a_fft * K4);
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename dealiasing_setofvar::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type dealiasing_setofvar::operator()(argument_type0&& setofvar_fft, argument_type1&& where, argument_type2&& n0, argument_type3&& n1) const
  {
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(setofvar_fft)))>::type nk = std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(setofvar_fft));
    {
      long  __target1 = n0;
      for (long  i0=0L; i0 < __target1; i0 += 1L)
      {
        {
          long  __target2 = n1;
          for (long  i1=0L; i1 < __target2; i1 += 1L)
          {
            if (where.fast(pythonic::types::make_tuple(i0, i1)))
            {
              {
                long  __target3 = nk;
                for (long  ik=0L; ik < __target3; ik += 1L)
                {
                  setofvar_fft.fast(pythonic::types::make_tuple(ik, i0, i1)) = 0.0;
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
typename __pythran_util2d_pythran::compute_increments_dim1::type<pythonic::types::ndarray<double,2>, long>::result_type compute_increments_dim10(pythonic::types::ndarray<double,2>&& var, long&& irx) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::compute_increments_dim1()(var, irx);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::compute_increments_dim1::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, long>::result_type compute_increments_dim11(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& var, long&& irx) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::compute_increments_dim1()(var, irx);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::invlaplacian2_fft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, long>::result_type invlaplacian2_fft0(pythonic::types::ndarray<std::complex<double>,2>&& a_fft, pythonic::types::ndarray<double,2>&& K4_not0, long&& rank) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::invlaplacian2_fft()(a_fft, K4_not0, rank);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::invlaplacian2_fft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, long>::result_type invlaplacian2_fft1(pythonic::types::ndarray<std::complex<double>,2>&& a_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& K4_not0, long&& rank) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::invlaplacian2_fft()(a_fft, K4_not0, rank);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::invlaplacian2_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, long>::result_type invlaplacian2_fft2(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& a_fft, pythonic::types::ndarray<double,2>&& K4_not0, long&& rank) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::invlaplacian2_fft()(a_fft, K4_not0, rank);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::invlaplacian2_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, long>::result_type invlaplacian2_fft3(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& a_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& K4_not0, long&& rank) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::invlaplacian2_fft()(a_fft, K4_not0, rank);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::laplacian2_fft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>>::result_type laplacian2_fft0(pythonic::types::ndarray<std::complex<double>,2>&& a_fft, pythonic::types::ndarray<double,2>&& K4) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::laplacian2_fft()(a_fft, K4);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::laplacian2_fft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type laplacian2_fft1(pythonic::types::ndarray<std::complex<double>,2>&& a_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& K4) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::laplacian2_fft()(a_fft, K4);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::laplacian2_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>>::result_type laplacian2_fft2(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& a_fft, pythonic::types::ndarray<double,2>&& K4) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::laplacian2_fft()(a_fft, K4);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::laplacian2_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type laplacian2_fft3(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& a_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& K4) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::laplacian2_fft()(a_fft, K4);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::dealiasing_setofvar::type<pythonic::types::ndarray<std::complex<double>,3>, pythonic::types::ndarray<uint8_t,2>, long, long>::result_type dealiasing_setofvar0(pythonic::types::ndarray<std::complex<double>,3>&& setofvar_fft, pythonic::types::ndarray<uint8_t,2>&& where, long&& n0, long&& n1) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::dealiasing_setofvar()(setofvar_fft, where, n0, n1);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util2d_pythran::dealiasing_setofvar::type<pythonic::types::ndarray<std::complex<double>,3>, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>, long, long>::result_type dealiasing_setofvar1(pythonic::types::ndarray<std::complex<double>,3>&& setofvar_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>&& where, long&& n0, long&& n1) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util2d_pythran::dealiasing_setofvar()(setofvar_fft, where, n0, n1);
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
__pythran_wrap_compute_increments_dim10(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"var","irx", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<long>(args_obj[1]))
        return to_python(compute_increments_dim10(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<long>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_increments_dim11(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"var","irx", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<long>(args_obj[1]))
        return to_python(compute_increments_dim11(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<long>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_invlaplacian2_fft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"a_fft","K4_not0","rank", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(invlaplacian2_fft0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_invlaplacian2_fft1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"a_fft","K4_not0","rank", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(invlaplacian2_fft1(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_invlaplacian2_fft2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"a_fft","K4_not0","rank", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(invlaplacian2_fft2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_invlaplacian2_fft3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"a_fft","K4_not0","rank", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<long>(args_obj[2]))
        return to_python(invlaplacian2_fft3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<long>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_laplacian2_fft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"a_fft","K4", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]))
        return to_python(laplacian2_fft0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_laplacian2_fft1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"a_fft","K4", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]))
        return to_python(laplacian2_fft1(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_laplacian2_fft2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"a_fft","K4", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]))
        return to_python(laplacian2_fft2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_laplacian2_fft3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[2+1];
    char const* keywords[] = {"a_fft","K4", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OO",
                                     (char**)keywords, &args_obj[0], &args_obj[1]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]))
        return to_python(laplacian2_fft3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_dealiasing_setofvar0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"setofvar_fft","where","n0","n1", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,2>>(args_obj[1]) && is_convertible<long>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(dealiasing_setofvar0(from_python<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,2>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_dealiasing_setofvar1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"setofvar_fft","where","n0","n1", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>>(args_obj[1]) && is_convertible<long>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(dealiasing_setofvar1(from_python<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_increments_dim1(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_increments_dim10(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_increments_dim11(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_increments_dim1", "   compute_increments_dim1(float64[][],int)\n   compute_increments_dim1(float64[][].T,int)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_invlaplacian2_fft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_invlaplacian2_fft0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_invlaplacian2_fft1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_invlaplacian2_fft2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_invlaplacian2_fft3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "invlaplacian2_fft", "   invlaplacian2_fft(complex128[][],float64[][],int)\n   invlaplacian2_fft(complex128[][],float64[][].T,int)\n   invlaplacian2_fft(complex128[][].T,float64[][],int)\n   invlaplacian2_fft(complex128[][].T,float64[][].T,int)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_laplacian2_fft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_laplacian2_fft0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_laplacian2_fft1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_laplacian2_fft2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_laplacian2_fft3(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "laplacian2_fft", "   laplacian2_fft(complex128[][],float64[][])\n   laplacian2_fft(complex128[][],float64[][].T)\n   laplacian2_fft(complex128[][].T,float64[][])\n   laplacian2_fft(complex128[][].T,float64[][].T)", args, kw);
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


if(PyObject* obj = __pythran_wrap_dealiasing_setofvar1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "dealiasing_setofvar", "   dealiasing_setofvar(complex128[][][],uint8[][],int,int)\n   dealiasing_setofvar(complex128[][][],uint8[][].T,int,int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_increments_dim1",
    (PyCFunction)__pythran_wrapall_compute_increments_dim1,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - compute_increments_dim1(float64[][], int)\n    - compute_increments_dim1(float64[][].T, int)\nCompute the increments of var over the dim 1."},{
    "invlaplacian2_fft",
    (PyCFunction)__pythran_wrapall_invlaplacian2_fft,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - invlaplacian2_fft(complex128[][], float64[][], int)\n    - invlaplacian2_fft(complex128[][], float64[][].T, int)\n    - invlaplacian2_fft(complex128[][].T, float64[][], int)\n    - invlaplacian2_fft(complex128[][].T, float64[][].T, int)\nCompute the inverse Laplace square."},{
    "laplacian2_fft",
    (PyCFunction)__pythran_wrapall_laplacian2_fft,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - laplacian2_fft(complex128[][], float64[][])\n    - laplacian2_fft(complex128[][], float64[][].T)\n    - laplacian2_fft(complex128[][].T, float64[][])\n    - laplacian2_fft(complex128[][].T, float64[][].T)\nCompute the Laplacian square."},{
    "dealiasing_setofvar",
    (PyCFunction)__pythran_wrapall_dealiasing_setofvar,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - dealiasing_setofvar(complex128[][][], uint8[][], int, int)\n    - dealiasing_setofvar(complex128[][][], uint8[][].T, int, int)\nDealiasing of a setofvar arrays"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "util2d_pythran",            /* m_name */
    "\nPythran compatible functions: 2d operators (:mod:`fluidsim.operators.util2d_pythran`)\n=====================================================================================\n\n.. autofunction:: dealiasing_setofvar\n\n.. autofunction:: laplacian2_fft\n\n.. autofunction:: invlaplacian2_fft\n\n.. autofunction:: compute_increments_dim1\n\n",         /* m_doc */
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
PYTHRAN_MODULE_INIT(util2d_pythran)(void)
#ifndef _WIN32
__attribute__ ((visibility("default")))
__attribute__ ((externally_visible))
#endif
;
PyMODINIT_FUNC
PYTHRAN_MODULE_INIT(util2d_pythran)(void) {
    #ifdef PYTHONIC_TYPES_NDARRAY_HPP
        import_array()
    #endif
    #if PY_MAJOR_VERSION >= 3
    PyObject* theModule = PyModule_Create(&moduledef);
    #else
    PyObject* theModule = Py_InitModule3("util2d_pythran",
                                         Methods,
                                         "\nPythran compatible functions: 2d operators (:mod:`fluidsim.operators.util2d_pythran`)\n=====================================================================================\n\n.. autofunction:: dealiasing_setofvar\n\n.. autofunction:: laplacian2_fft\n\n.. autofunction:: invlaplacian2_fft\n\n.. autofunction:: compute_increments_dim1\n\n"
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.8.4post0",
                                      "2018-03-13 19:12:43.773956",
                                      "ee264b7676e42c223c4e7f192cdb71155d432cc311d6d0014316e68bbabb979e");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif