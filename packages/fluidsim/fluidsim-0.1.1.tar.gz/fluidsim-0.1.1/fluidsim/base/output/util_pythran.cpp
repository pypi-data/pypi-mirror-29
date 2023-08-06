#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/int32.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/bool.hpp>
#include <pythonic/include/types/float.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/float.hpp>
#include <pythonic/types/int32.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/include/numpy/empty.hpp>
#include <pythonic/include/__builtin__/abs.hpp>
#include <pythonic/include/__builtin__/pow.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/__builtin__/False.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/numpy/sum.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/numpy/empty.hpp>
#include <pythonic/__builtin__/abs.hpp>
#include <pythonic/__builtin__/pow.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/__builtin__/False.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/numpy/sum.hpp>
#include <pythonic/types/str.hpp>
#include <pythonic/__builtin__/getattr.hpp>
namespace __pythran_util_pythran
{
  struct strfunc_from_pdf
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 = bool>
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<__type2>())) __type3;
      typedef typename pythonic::assignable<decltype(std::declval<__type1>()(std::declval<__type3>()))>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type5;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SIZE>(std::declval<__type2>())) __type6;
      typedef decltype(std::declval<__type5>()(std::declval<__type6>())) __type7;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type7>::type::iterator>::value_type>::type __type8;
      typedef indexable<__type8> __type9;
      typedef typename __combined<__type4,__type9>::type __type10;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::abs{})>::type>::type __type11;
      typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type>::type __type12;
      typedef typename pythonic::assignable<decltype(std::declval<__type11>()(std::declval<__type12>()))>::type __type13;
      typedef typename __combined<__type12,__type13>::type __type14;
      typedef long __type15;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type8>(), std::declval<__type15>())) __type16;
      typedef decltype(std::declval<__type14>()[std::declval<__type16>()]) __type17;
      typedef decltype((std::declval<__type17>() - std::declval<__type17>())) __type18;
      typedef decltype(std::declval<__type11>()(std::declval<__type18>())) __type19;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type20;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type21;
      typedef decltype(std::declval<__type21>()[std::declval<__type8>()]) __type22;
      typedef decltype(std::declval<__type14>()[std::declval<__type8>()]) __type23;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type24;
      typedef decltype((pythonic::__builtin__::pow(std::declval<__type23>(), std::declval<__type24>()))) __type25;
      typedef decltype((std::declval<__type22>() * std::declval<__type25>())) __type26;
      typedef decltype(std::declval<__type20>()(std::declval<__type26>())) __type27;
      typedef decltype((std::declval<__type19>() * std::declval<__type27>())) __type28;
      typedef container<typename std::remove_reference<__type28>::type> __type29;
      typedef typename __combined<__type10,__type29>::type __type30;
      typedef typename __combined<__type30,__type9>::type __type31;
      typedef __type0 __ptype0;
      typedef typename pythonic::returnable<typename __combined<__type31,__type29>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 = bool>
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type operator()(argument_type0&& rxs, argument_type1&& pdf, argument_type2&& values, argument_type3&& order, argument_type4 absolute= pythonic::__builtin__::False) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 >
  typename strfunc_from_pdf::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4>::result_type strfunc_from_pdf::operator()(argument_type0&& rxs, argument_type1&& pdf, argument_type2&& values, argument_type3&& order, argument_type4 absolute) const
  {
    typedef typename pythonic::assignable<typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::abs{})>::type>::type __type1;
    typedef typename pythonic::assignable<decltype(std::declval<__type1>()(std::declval<__type0>()))>::type __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::empty{})>::type>::type __type3;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type4;
    typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<__type4>())) __type5;
    typedef typename pythonic::assignable<decltype(std::declval<__type3>()(std::declval<__type5>()))>::type __type6;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type7;
    typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SIZE>(std::declval<__type4>())) __type8;
    typedef decltype(std::declval<__type7>()(std::declval<__type8>())) __type9;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type9>::type::iterator>::value_type>::type __type10;
    typedef indexable<__type10> __type11;
    typedef typename __combined<__type6,__type11>::type __type12;
    typedef typename __combined<__type0,__type2>::type __type13;
    typedef long __type14;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type10>(), std::declval<__type14>())) __type15;
    typedef decltype(std::declval<__type13>()[std::declval<__type15>()]) __type16;
    typedef decltype((std::declval<__type16>() - std::declval<__type16>())) __type17;
    typedef decltype(std::declval<__type1>()(std::declval<__type17>())) __type18;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::sum{})>::type>::type __type19;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type20;
    typedef decltype(std::declval<__type20>()[std::declval<__type10>()]) __type21;
    typedef decltype(std::declval<__type13>()[std::declval<__type10>()]) __type22;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type23;
    typedef decltype((pythonic::__builtin__::pow(std::declval<__type22>(), std::declval<__type23>()))) __type24;
    typedef decltype((std::declval<__type21>() * std::declval<__type24>())) __type25;
    typedef decltype(std::declval<__type19>()(std::declval<__type25>())) __type26;
    typedef decltype((std::declval<__type18>() * std::declval<__type26>())) __type27;
    typedef container<typename std::remove_reference<__type27>::type> __type28;
    typedef typename __combined<__type12,__type28>::type __type29;
    typename pythonic::assignable<typename __combined<__type0,__type2>::type>::type values_ = values;
    typename pythonic::assignable<typename __combined<__type29,__type11>::type>::type S_order = pythonic::numpy::functor::empty{}(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(rxs));
    if (absolute)
    {
      values_ = pythonic::__builtin__::functor::abs{}(values_);
    }
    {
      long  __target1 = pythonic::__builtin__::getattr<pythonic::types::attr::SIZE>(rxs);
      for (long  irx=0L; irx < __target1; irx += 1L)
      {
        ;
        S_order.fast(irx) = (pythonic::__builtin__::functor::abs{}((values_.fast(pythonic::types::make_tuple(irx, 1L)) - values_.fast(pythonic::types::make_tuple(irx, 0L)))) * pythonic::numpy::functor::sum{}((pdf.fast(irx) * (pythonic::__builtin__::pow(values_.fast(irx), order)))));
      }
    }
    return S_order;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<int32_t,1>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double, bool>::result_type strfunc_from_pdf0(pythonic::types::ndarray<int32_t,1>&& rxs, pythonic::types::ndarray<double,2>&& pdf, pythonic::types::ndarray<double,2>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<int32_t,1>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double, bool>::result_type strfunc_from_pdf1(pythonic::types::ndarray<int32_t,1>&& rxs, pythonic::types::ndarray<double,2>&& pdf, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<int32_t,1>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double, bool>::result_type strfunc_from_pdf2(pythonic::types::ndarray<int32_t,1>&& rxs, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& pdf, pythonic::types::ndarray<double,2>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<int32_t,1>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double, bool>::result_type strfunc_from_pdf3(pythonic::types::ndarray<int32_t,1>&& rxs, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& pdf, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double, bool>::result_type strfunc_from_pdf4(pythonic::types::ndarray<double,2>&& rxs, pythonic::types::ndarray<double,2>&& pdf, pythonic::types::ndarray<double,2>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double, bool>::result_type strfunc_from_pdf5(pythonic::types::ndarray<double,2>&& rxs, pythonic::types::ndarray<double,2>&& pdf, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double, bool>::result_type strfunc_from_pdf6(pythonic::types::ndarray<double,2>&& rxs, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& pdf, pythonic::types::ndarray<double,2>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double, bool>::result_type strfunc_from_pdf7(pythonic::types::ndarray<double,2>&& rxs, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& pdf, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>, double, bool>::result_type strfunc_from_pdf8(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rxs, pythonic::types::ndarray<double,2>&& pdf, pythonic::types::ndarray<double,2>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double, bool>::result_type strfunc_from_pdf9(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rxs, pythonic::types::ndarray<double,2>&& pdf, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>, double, bool>::result_type strfunc_from_pdf10(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rxs, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& pdf, pythonic::types::ndarray<double,2>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::strfunc_from_pdf::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, double, bool>::result_type strfunc_from_pdf11(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& rxs, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& pdf, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& values, double&& order, bool&& absolute) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::strfunc_from_pdf()(rxs, pdf, values, order, absolute);
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
__pythran_wrap_strfunc_from_pdf0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf0(from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf1(from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf2(from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf3(from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf4(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf5(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf6(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf7(from_python<pythonic::types::ndarray<double,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf8(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf8(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf9(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf9(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf10(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf10(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_strfunc_from_pdf11(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[5+1];
    char const* keywords[] = {"rxs","pdf","values","order","absolute", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<double>(args_obj[3]) && is_convertible<bool>(args_obj[4]))
        return to_python(strfunc_from_pdf11(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<double>(args_obj[3]), from_python<bool>(args_obj[4])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_strfunc_from_pdf(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_strfunc_from_pdf0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf7(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf8(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf9(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf10(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_strfunc_from_pdf11(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "strfunc_from_pdf", "   strfunc_from_pdf(int32[],float64[][],float64[][],float,bool)\n   strfunc_from_pdf(int32[],float64[][],float64[][].T,float,bool)\n   strfunc_from_pdf(int32[],float64[][].T,float64[][],float,bool)\n   strfunc_from_pdf(int32[],float64[][].T,float64[][].T,float,bool)\n   strfunc_from_pdf(float64[][],float64[][],float64[][],float,bool)\n   strfunc_from_pdf(float64[][],float64[][],float64[][].T,float,bool)\n   strfunc_from_pdf(float64[][],float64[][].T,float64[][],float,bool)\n   strfunc_from_pdf(float64[][],float64[][].T,float64[][].T,float,bool)\n   strfunc_from_pdf(float64[][].T,float64[][],float64[][],float,bool)\n   strfunc_from_pdf(float64[][].T,float64[][],float64[][].T,float,bool)\n   strfunc_from_pdf(float64[][].T,float64[][].T,float64[][],float,bool)\n   strfunc_from_pdf(float64[][].T,float64[][].T,float64[][].T,float,bool)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "strfunc_from_pdf",
    (PyCFunction)__pythran_wrapall_strfunc_from_pdf,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - strfunc_from_pdf(int32[], float64[][], float64[][], float, bool)\n    - strfunc_from_pdf(int32[], float64[][], float64[][].T, float, bool)\n    - strfunc_from_pdf(int32[], float64[][].T, float64[][], float, bool)\n    - strfunc_from_pdf(int32[], float64[][].T, float64[][].T, float, bool)\n    - strfunc_from_pdf(float64[][], float64[][], float64[][], float, bool)\n    - strfunc_from_pdf(float64[][], float64[][], float64[][].T, float, bool)\n    - strfunc_from_pdf(float64[][], float64[][].T, float64[][], float, bool)\n    - strfunc_from_pdf(float64[][], float64[][].T, float64[][].T, float, bool)\n    - strfunc_from_pdf(float64[][].T, float64[][], float64[][], float, bool)\n    - strfunc_from_pdf(float64[][].T, float64[][], float64[][].T, float, bool)\n    - strfunc_from_pdf(float64[][].T, float64[][].T, float64[][], float, bool)\n    - strfunc_from_pdf(float64[][].T, float64[][].T, float64[][].T, float, bool)\nCompute structure function of specified order from pdf for increments\n    module.\n\n"},
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
                                      "2018-03-13 21:36:54.381175",
                                      "a2e56fc3347b1056f92d0e16e1a79784b1d85c2e2c28b8754f250c054371a020");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif