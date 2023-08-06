#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/int32.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/int32.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/include/types/str.hpp>
#include <pythonic/include/numpy/complex128.hpp>
#include <pythonic/include/numpy/zeros.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/__builtin__/getattr.hpp>
#include <pythonic/include/numpy/conj.hpp>
#include <pythonic/include/__builtin__/len.hpp>
#include <pythonic/types/str.hpp>
#include <pythonic/numpy/complex128.hpp>
#include <pythonic/numpy/zeros.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/__builtin__/getattr.hpp>
#include <pythonic/numpy/conj.hpp>
#include <pythonic/__builtin__/len.hpp>
namespace __pythran_util_pythran
{
  struct compute_correl2_seq
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type1;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type1>(), std::declval<__type1>())) __type2;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type3;
      typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type2>(), std::declval<__type3>()))>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type5;
      typedef decltype(std::declval<__type5>()(std::declval<__type1>())) __type6;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type6>::type::iterator>::value_type>::type __type7;
      typedef long __type8;
      typedef decltype((std::declval<__type7>() + std::declval<__type8>())) __type9;
      typedef decltype(std::declval<__type5>()(std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type11>())) __type12;
      typedef indexable<__type12> __type13;
      typedef typename __combined<__type4,__type13>::type __type14;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type11>(), std::declval<__type7>())) __type15;
      typedef indexable<__type15> __type16;
      typedef typename __combined<__type14,__type16>::type __type17;
      typedef typename __combined<__type17,__type13>::type __type18;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type19;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<__type19>())) __type20;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type20>::type>::type __type21;
      typedef typename pythonic::lazy<__type21>::type __type22;
      typedef decltype(std::declval<__type5>()(std::declval<__type22>())) __type23;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type23>::type::iterator>::value_type>::type __type24;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type24>(), std::declval<__type7>())) __type25;
      typedef decltype(std::declval<__type19>()[std::declval<__type25>()]) __type26;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type __type27;
      typedef typename pythonic::assignable<decltype(std::declval<__type27>()(std::declval<__type19>()))>::type __type28;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type24>(), std::declval<__type11>())) __type29;
      typedef decltype(std::declval<__type28>()[std::declval<__type29>()]) __type30;
      typedef decltype((std::declval<__type26>() * std::declval<__type30>())) __type31;
      typedef container<typename std::remove_reference<__type31>::type> __type32;
      typedef typename __combined<__type18,__type32>::type __type33;
      typedef typename __combined<__type14,__type32>::type __type34;
      typedef decltype(std::declval<__type34>()[std::declval<__type12>()]) __type35;
      typedef decltype(std::declval<__type27>()(std::declval<__type35>())) __type36;
      typedef container<typename std::remove_reference<__type36>::type> __type37;
      typedef typename __combined<__type33,__type37>::type __type38;
      typedef typename __combined<__type38,__type16>::type __type39;
      typedef typename pythonic::returnable<typename __combined<__type39,__type37>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& q_fftt, argument_type1&& iomegas1, argument_type2&& nb_omegas, argument_type3&& nb_xs_seq) const
    ;
  }  ;
  struct compute_correl4_seq
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type1;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<__type0>())) __type2;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type2>::type>::type __type3;
      typedef typename pythonic::lazy<__type3>::type __type4;
      typedef decltype(std::declval<__type1>()(std::declval<__type4>())) __type5;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type5>::type::iterator>::value_type>::type __type6;
      typedef decltype(std::declval<__type0>()[std::declval<__type6>()]) __type7;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type8;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::len{})>::type>::type __type9;
      typedef decltype(std::declval<__type9>()(std::declval<__type0>())) __type10;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type11;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type10>(), std::declval<__type11>(), std::declval<__type11>())) __type12;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type13;
      typedef typename pythonic::assignable<decltype(std::declval<__type8>()(std::declval<__type12>(), std::declval<__type13>()))>::type __type14;
      typedef decltype(std::declval<__type1>()(std::declval<__type11>())) __type15;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type15>::type::iterator>::value_type>::type __type16;
      typedef long __type17;
      typedef decltype((std::declval<__type16>() + std::declval<__type17>())) __type18;
      typedef decltype(std::declval<__type1>()(std::declval<__type18>())) __type19;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type19>::type::iterator>::value_type>::type __type20;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type6>(), std::declval<__type16>(), std::declval<__type20>())) __type21;
      typedef indexable<__type21> __type22;
      typedef typename __combined<__type14,__type22>::type __type23;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type6>(), std::declval<__type20>(), std::declval<__type16>())) __type24;
      typedef indexable<__type24> __type25;
      typedef typename __combined<__type23,__type25>::type __type26;
      typedef typename __combined<__type26,__type22>::type __type27;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type28;
      typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<__type28>())) __type29;
      typedef typename std::tuple_element<0,typename std::remove_reference<__type29>::type>::type __type30;
      typedef typename pythonic::lazy<__type30>::type __type31;
      typedef decltype(std::declval<__type1>()(std::declval<__type31>())) __type32;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type32>::type::iterator>::value_type>::type __type33;
      typedef typename pythonic::assignable<decltype(std::declval<__type0>()[std::declval<__type6>()])>::type __type34;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type34>())) __type35;
      typedef decltype(std::declval<__type28>()[std::declval<__type35>()]) __type36;
      typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type __type37;
      typedef typename pythonic::assignable<decltype(std::declval<__type37>()(std::declval<__type28>()))>::type __type38;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type16>())) __type39;
      typedef decltype(std::declval<__type38>()[std::declval<__type39>()]) __type40;
      typedef decltype((std::declval<__type36>() * std::declval<__type40>())) __type41;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type20>())) __type42;
      typedef decltype(std::declval<__type38>()[std::declval<__type42>()]) __type43;
      typedef decltype((std::declval<__type41>() * std::declval<__type43>())) __type44;
      typedef decltype((std::declval<__type16>() + std::declval<__type20>())) __type45;
      typedef typename pythonic::assignable<decltype((std::declval<__type45>() - std::declval<__type34>()))>::type __type46;
      typedef typename pythonic::assignable<decltype((-std::declval<__type46>()))>::type __type47;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type47>())) __type48;
      typedef decltype(std::declval<__type38>()[std::declval<__type48>()]) __type49;
      typedef decltype((std::declval<__type44>() * std::declval<__type49>())) __type50;
      typedef container<typename std::remove_reference<__type50>::type> __type51;
      typedef typename __combined<__type27,__type51>::type __type52;
      typedef typename __combined<__type52,__type22>::type __type53;
      typedef decltype((std::declval<__type17>() * std::declval<__type11>())) __type54;
      typedef decltype((std::declval<__type54>() - std::declval<__type17>())) __type55;
      typedef typename pythonic::assignable<decltype((std::declval<__type55>() - std::declval<__type46>()))>::type __type56;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type56>())) __type57;
      typedef decltype(std::declval<__type38>()[std::declval<__type57>()]) __type58;
      typedef decltype((std::declval<__type44>() * std::declval<__type58>())) __type59;
      typedef container<typename std::remove_reference<__type59>::type> __type60;
      typedef typename __combined<__type53,__type60>::type __type61;
      typedef typename __combined<__type61,__type22>::type __type62;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type33>(), std::declval<__type46>())) __type63;
      typedef decltype(std::declval<__type28>()[std::declval<__type63>()]) __type64;
      typedef decltype((std::declval<__type44>() * std::declval<__type64>())) __type65;
      typedef container<typename std::remove_reference<__type65>::type> __type66;
      typedef typename __combined<__type62,__type66>::type __type67;
      typedef typename __combined<__type23,__type51>::type __type68;
      typedef typename __combined<__type68,__type22>::type __type69;
      typedef typename __combined<__type69,__type60>::type __type70;
      typedef typename __combined<__type70,__type22>::type __type71;
      typedef typename __combined<__type71,__type66>::type __type72;
      typedef decltype(std::declval<__type72>()[std::declval<__type21>()]) __type73;
      typedef container<typename std::remove_reference<__type73>::type> __type74;
      typedef typename __combined<__type67,__type74>::type __type75;
      typedef typename __combined<__type75,__type25>::type __type76;
      typedef __type7 __ptype0;
      typedef typename pythonic::returnable<typename __combined<__type76,__type74>::type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& q_fftt, argument_type1&& iomegas1, argument_type2&& nb_omegas, argument_type3&& nb_xs_seq) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename compute_correl2_seq::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type compute_correl2_seq::operator()(argument_type0&& q_fftt, argument_type1&& iomegas1, argument_type2&& nb_omegas, argument_type3&& nb_xs_seq) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type1;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type1>(), std::declval<__type1>())) __type2;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type3;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type2>(), std::declval<__type3>()))>::type __type4;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type5;
    typedef decltype(std::declval<__type5>()(std::declval<__type1>())) __type6;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type6>::type::iterator>::value_type>::type __type7;
    typedef long __type8;
    typedef decltype((std::declval<__type7>() + std::declval<__type8>())) __type9;
    typedef decltype(std::declval<__type5>()(std::declval<__type9>())) __type10;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type10>::type::iterator>::value_type>::type __type11;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type7>(), std::declval<__type11>())) __type12;
    typedef indexable<__type12> __type13;
    typedef typename __combined<__type4,__type13>::type __type14;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type11>(), std::declval<__type7>())) __type15;
    typedef indexable<__type15> __type16;
    typedef typename __combined<__type14,__type16>::type __type17;
    typedef typename __combined<__type17,__type13>::type __type18;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type19;
    typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<__type19>())) __type20;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type20>::type>::type __type21;
    typedef typename pythonic::lazy<__type21>::type __type22;
    typedef decltype(std::declval<__type5>()(std::declval<__type22>())) __type23;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type23>::type::iterator>::value_type>::type __type24;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type24>(), std::declval<__type7>())) __type25;
    typedef decltype(std::declval<__type19>()[std::declval<__type25>()]) __type26;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type __type27;
    typedef typename pythonic::assignable<decltype(std::declval<__type27>()(std::declval<__type19>()))>::type __type28;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type24>(), std::declval<__type11>())) __type29;
    typedef decltype(std::declval<__type28>()[std::declval<__type29>()]) __type30;
    typedef decltype((std::declval<__type26>() * std::declval<__type30>())) __type31;
    typedef container<typename std::remove_reference<__type31>::type> __type32;
    typedef typename __combined<__type18,__type32>::type __type33;
    typedef typename __combined<__type14,__type32>::type __type34;
    typedef decltype(std::declval<__type34>()[std::declval<__type12>()]) __type35;
    typedef decltype(std::declval<__type27>()(std::declval<__type35>())) __type36;
    typedef container<typename std::remove_reference<__type36>::type> __type37;
    typedef typename __combined<__type33,__type37>::type __type38;
    typename pythonic::assignable<decltype(pythonic::numpy::functor::conj{}(q_fftt))>::type q_fftt_conj = pythonic::numpy::functor::conj{}(q_fftt);
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(q_fftt)))>::type nx = std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(q_fftt));
    typename pythonic::assignable<typename __combined<__type38,__type16>::type>::type corr2 = pythonic::numpy::functor::zeros{}(pythonic::types::make_tuple(nb_omegas, nb_omegas), pythonic::numpy::functor::complex128{});
    {
      long  __target1 = nb_omegas;
      for (long  io3=0L; io3 < __target1; io3 += 1L)
      {
        {
          long  __target2 = (io3 + 1L);
          for (long  io4=0L; io4 < __target2; io4 += 1L)
          {
            {
              long  __target3 = nx;
              for (long  ix=0L; ix < __target3; ix += 1L)
              {
                corr2.fast(pythonic::types::make_tuple(io3, io4)) += (q_fftt.fast(pythonic::types::make_tuple(ix, io3)) * q_fftt_conj.fast(pythonic::types::make_tuple(ix, io4)));
              }
            }
            corr2.fast(pythonic::types::make_tuple(io4, io3)) = pythonic::numpy::functor::conj{}(corr2.fast(pythonic::types::make_tuple(io3, io4)));
          }
        }
      }
    }
    return corr2;
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename compute_correl4_seq::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type compute_correl4_seq::operator()(argument_type0&& q_fftt, argument_type1&& iomegas1, argument_type2&& nb_omegas, argument_type3&& nb_xs_seq) const
  {
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::zeros{})>::type>::type __type0;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::len{})>::type>::type __type1;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
    typedef decltype(std::declval<__type1>()(std::declval<__type2>())) __type3;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type4;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type3>(), std::declval<__type4>(), std::declval<__type4>())) __type5;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::complex128{})>::type>::type __type6;
    typedef typename pythonic::assignable<decltype(std::declval<__type0>()(std::declval<__type5>(), std::declval<__type6>()))>::type __type7;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type __type8;
    typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<__type2>())) __type9;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type9>::type>::type __type10;
    typedef typename pythonic::lazy<__type10>::type __type11;
    typedef decltype(std::declval<__type8>()(std::declval<__type11>())) __type12;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type12>::type::iterator>::value_type>::type __type13;
    typedef decltype(std::declval<__type8>()(std::declval<__type4>())) __type14;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type14>::type::iterator>::value_type>::type __type15;
    typedef long __type16;
    typedef decltype((std::declval<__type15>() + std::declval<__type16>())) __type17;
    typedef decltype(std::declval<__type8>()(std::declval<__type17>())) __type18;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type18>::type::iterator>::value_type>::type __type19;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type13>(), std::declval<__type15>(), std::declval<__type19>())) __type20;
    typedef indexable<__type20> __type21;
    typedef typename __combined<__type7,__type21>::type __type22;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type13>(), std::declval<__type19>(), std::declval<__type15>())) __type23;
    typedef indexable<__type23> __type24;
    typedef typename __combined<__type22,__type24>::type __type25;
    typedef typename __combined<__type25,__type21>::type __type26;
    typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type27;
    typedef decltype(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(std::declval<__type27>())) __type28;
    typedef typename std::tuple_element<0,typename std::remove_reference<__type28>::type>::type __type29;
    typedef typename pythonic::lazy<__type29>::type __type30;
    typedef decltype(std::declval<__type8>()(std::declval<__type30>())) __type31;
    typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type31>::type::iterator>::value_type>::type __type32;
    typedef typename pythonic::assignable<decltype(std::declval<__type2>()[std::declval<__type13>()])>::type __type33;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type33>())) __type34;
    typedef decltype(std::declval<__type27>()[std::declval<__type34>()]) __type35;
    typedef typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::conj{})>::type>::type __type36;
    typedef typename pythonic::assignable<decltype(std::declval<__type36>()(std::declval<__type27>()))>::type __type37;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type15>())) __type38;
    typedef decltype(std::declval<__type37>()[std::declval<__type38>()]) __type39;
    typedef decltype((std::declval<__type35>() * std::declval<__type39>())) __type40;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type19>())) __type41;
    typedef decltype(std::declval<__type37>()[std::declval<__type41>()]) __type42;
    typedef decltype((std::declval<__type40>() * std::declval<__type42>())) __type43;
    typedef decltype((std::declval<__type15>() + std::declval<__type19>())) __type44;
    typedef typename pythonic::assignable<decltype((std::declval<__type44>() - std::declval<__type33>()))>::type __type45;
    typedef typename pythonic::assignable<decltype((-std::declval<__type45>()))>::type __type46;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type46>())) __type47;
    typedef decltype(std::declval<__type37>()[std::declval<__type47>()]) __type48;
    typedef decltype((std::declval<__type43>() * std::declval<__type48>())) __type49;
    typedef container<typename std::remove_reference<__type49>::type> __type50;
    typedef typename __combined<__type26,__type50>::type __type51;
    typedef decltype((std::declval<__type16>() * std::declval<__type4>())) __type52;
    typedef decltype((std::declval<__type52>() - std::declval<__type16>())) __type53;
    typedef typename pythonic::assignable<decltype((std::declval<__type53>() - std::declval<__type45>()))>::type __type54;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type54>())) __type55;
    typedef decltype(std::declval<__type37>()[std::declval<__type55>()]) __type56;
    typedef decltype((std::declval<__type43>() * std::declval<__type56>())) __type57;
    typedef container<typename std::remove_reference<__type57>::type> __type58;
    typedef typename __combined<__type51,__type58>::type __type59;
    typedef decltype(pythonic::types::make_tuple(std::declval<__type32>(), std::declval<__type45>())) __type60;
    typedef decltype(std::declval<__type27>()[std::declval<__type60>()]) __type61;
    typedef decltype((std::declval<__type43>() * std::declval<__type61>())) __type62;
    typedef container<typename std::remove_reference<__type62>::type> __type63;
    typedef typename __combined<__type59,__type63>::type __type64;
    typedef typename __combined<__type22,__type50>::type __type65;
    typedef typename __combined<__type65,__type21>::type __type66;
    typedef typename __combined<__type66,__type58>::type __type67;
    typedef typename __combined<__type67,__type21>::type __type68;
    typedef typename __combined<__type68,__type63>::type __type69;
    typedef decltype(std::declval<__type69>()[std::declval<__type20>()]) __type70;
    typedef container<typename std::remove_reference<__type70>::type> __type71;
    typedef typename __combined<__type64,__type71>::type __type72;
    typename pythonic::assignable<decltype(pythonic::numpy::functor::conj{}(q_fftt))>::type q_fftt_conj = pythonic::numpy::functor::conj{}(q_fftt);
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(q_fftt)))>::type nx = std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(q_fftt));
    typename pythonic::lazy<decltype(std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(iomegas1)))>::type n0 = std::get<0>(pythonic::__builtin__::getattr<pythonic::types::attr::SHAPE>(iomegas1));
    typename pythonic::assignable<typename __combined<__type72,__type24>::type>::type corr4 = pythonic::numpy::functor::zeros{}(pythonic::types::make_tuple(pythonic::__builtin__::functor::len{}(iomegas1), nb_omegas, nb_omegas), pythonic::numpy::functor::complex128{});
    {
      long  __target1 = n0;
      for (long  i1=0L; i1 < __target1; i1 += 1L)
      {
        typename pythonic::assignable<decltype(iomegas1.fast(i1))>::type io1 = iomegas1.fast(i1);
        {
          long  __target2 = nb_omegas;
          for (long  io3=0L; io3 < __target2; io3 += 1L)
          {
            {
              long  __target3 = (io3 + 1L);
              for (long  io4=0L; io4 < __target3; io4 += 1L)
              {
                typename pythonic::assignable<decltype(((io3 + io4) - io1))>::type io2 = ((io3 + io4) - io1);
                if ((io2 < 0L))
                {
                  typename pythonic::assignable<decltype((-io2))>::type io2_ = (-io2);
                  {
                    long  __target4 = nx;
                    for (long  ix=0L; ix < __target4; ix += 1L)
                    {
                      corr4.fast(pythonic::types::make_tuple(i1, io3, io4)) += (((q_fftt[pythonic::types::make_tuple(ix, io1)] * q_fftt_conj.fast(pythonic::types::make_tuple(ix, io3))) * q_fftt_conj.fast(pythonic::types::make_tuple(ix, io4))) * q_fftt_conj[pythonic::types::make_tuple(ix, io2_)]);
                    }
                  }
                }
                else
                {
                  if ((io2 >= nb_omegas))
                  {
                    typename pythonic::assignable<decltype((((2L * nb_omegas) - 1L) - io2))>::type io2__ = (((2L * nb_omegas) - 1L) - io2);
                    {
                      long  __target4 = nx;
                      for (long  ix_=0L; ix_ < __target4; ix_ += 1L)
                      {
                        corr4.fast(pythonic::types::make_tuple(i1, io3, io4)) += (((q_fftt[pythonic::types::make_tuple(ix_, io1)] * q_fftt_conj.fast(pythonic::types::make_tuple(ix_, io3))) * q_fftt_conj.fast(pythonic::types::make_tuple(ix_, io4))) * q_fftt_conj[pythonic::types::make_tuple(ix_, io2__)]);
                      }
                    }
                  }
                  else
                  {
                    {
                      long  __target4 = nx;
                      for (long  ix__=0L; ix__ < __target4; ix__ += 1L)
                      {
                        corr4.fast(pythonic::types::make_tuple(i1, io3, io4)) += (((q_fftt[pythonic::types::make_tuple(ix__, io1)] * q_fftt_conj.fast(pythonic::types::make_tuple(ix__, io3))) * q_fftt_conj.fast(pythonic::types::make_tuple(ix__, io4))) * q_fftt[pythonic::types::make_tuple(ix__, io2)]);
                      }
                    }
                  }
                }
                corr4.fast(pythonic::types::make_tuple(i1, io4, io3)) = corr4.fast(pythonic::types::make_tuple(i1, io3, io4));
              }
            }
          }
        }
      }
    }
    return corr4;
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_util_pythran::compute_correl2_seq::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<int32_t,1>, long, long>::result_type compute_correl2_seq0(pythonic::types::ndarray<std::complex<double>,2>&& q_fftt, pythonic::types::ndarray<int32_t,1>&& iomegas1, long&& nb_omegas, long&& nb_xs_seq) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_correl2_seq()(q_fftt, iomegas1, nb_omegas, nb_xs_seq);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_correl2_seq::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<int32_t,1>, long, long>::result_type compute_correl2_seq1(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& q_fftt, pythonic::types::ndarray<int32_t,1>&& iomegas1, long&& nb_omegas, long&& nb_xs_seq) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_correl2_seq()(q_fftt, iomegas1, nb_omegas, nb_xs_seq);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_correl4_seq::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<int32_t,1>, long, long>::result_type compute_correl4_seq0(pythonic::types::ndarray<std::complex<double>,2>&& q_fftt, pythonic::types::ndarray<int32_t,1>&& iomegas1, long&& nb_omegas, long&& nb_xs_seq) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_correl4_seq()(q_fftt, iomegas1, nb_omegas, nb_xs_seq);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::compute_correl4_seq::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<int32_t,1>, long, long>::result_type compute_correl4_seq1(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& q_fftt, pythonic::types::ndarray<int32_t,1>&& iomegas1, long&& nb_omegas, long&& nb_xs_seq) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::compute_correl4_seq()(q_fftt, iomegas1, nb_omegas, nb_xs_seq);
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
__pythran_wrap_compute_correl2_seq0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"q_fftt","iomegas1","nb_omegas","nb_xs_seq", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[1]) && is_convertible<long>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_correl2_seq0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_correl2_seq1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"q_fftt","iomegas1","nb_omegas","nb_xs_seq", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[1]) && is_convertible<long>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_correl2_seq1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_correl4_seq0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"q_fftt","iomegas1","nb_omegas","nb_xs_seq", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[1]) && is_convertible<long>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_correl4_seq0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_compute_correl4_seq1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"q_fftt","iomegas1","nb_omegas","nb_xs_seq", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<int32_t,1>>(args_obj[1]) && is_convertible<long>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(compute_correl4_seq1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<int32_t,1>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_compute_correl2_seq(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_correl2_seq0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_correl2_seq1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_correl2_seq", "   compute_correl2_seq(complex128[][],int32[],int,int)\n   compute_correl2_seq(complex128[][].T,int32[],int,int)", args, kw);
                });
            }


            static PyObject *
            __pythran_wrapall_compute_correl4_seq(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_compute_correl4_seq0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_compute_correl4_seq1(self, args, kw))
    return obj;
PyErr_Clear();

                return pythonic::python::raise_invalid_argument(
                               "compute_correl4_seq", "   compute_correl4_seq(complex128[][],int32[],int,int)\n   compute_correl4_seq(complex128[][].T,int32[],int,int)", args, kw);
                });
            }


static PyMethodDef Methods[] = {
    {
    "compute_correl2_seq",
    (PyCFunction)__pythran_wrapall_compute_correl2_seq,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - compute_correl2_seq(complex128[][], int32[], int, int)\n    - compute_correl2_seq(complex128[][].T, int32[], int, int)\nCompute the correlations 2.\n\n    .. math::\n       C_2(\omega_1, \omega_2) =\n       \langle\n       \tilde w(\omega_1, \mathbf{x})\n       \tilde w(\omega_2, \mathbf{x})^*\n       \rangle_\mathbf{x},\n\n    where :math:`\omega_1 = \omega_2`. Thus, this function\n    produces an array :math:`C_2(\omega)`.\n\n"},{
    "compute_correl4_seq",
    (PyCFunction)__pythran_wrapall_compute_correl4_seq,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - compute_correl4_seq(complex128[][], int32[], int, int)\n    - compute_correl4_seq(complex128[][].T, int32[], int, int)\nCompute the correlations 4.\n\n    .. math::\n       C_4(\omega_1, \omega_2, \omega_3, \omega_4) =\n       \langle\n       \tilde w(\omega_1, \mathbf{x})\n       \tilde w(\omega_2, \mathbf{x})\n       \tilde w(\omega_3, \mathbf{x})^*\n       \tilde w(\omega_4, \mathbf{x})^*\n       \rangle_\mathbf{x},\n\n    where\n\n    .. math::\n       \omega_2 = \omega_3 + \omega_4 - \omega_1\n\n    and :math:`\omega_1 > 0`, :math:`\omega_3 > 0` and\n    :math:`\omega_4 > 0`. Thus, this function produces an array\n    :math:`C_4(\omega_1, \omega_3, \omega_4)`.\n\n"},
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
                                      "2018-03-11 15:21:40.589484",
                                      "0457aa8a7fb0558353c85f19d1ef2d300c5e96fccfab6a5a6d8f186bafb57af1");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif