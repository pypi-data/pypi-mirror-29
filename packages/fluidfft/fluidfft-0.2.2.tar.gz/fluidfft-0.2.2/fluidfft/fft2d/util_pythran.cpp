#define BOOST_SIMD_NO_STRICT_ALIASING 1
#include <pythonic/core.hpp>
#include <pythonic/python/core.hpp>
#include <pythonic/types/bool.hpp>
#include <pythonic/types/int.hpp>
#ifdef _OPENMP
#include <omp.h>
#endif
#include <pythonic/include/types/complex128.hpp>
#include <pythonic/include/types/float64.hpp>
#include <pythonic/include/types/uint8.hpp>
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/include/types/numpy_texpr.hpp>
#include <pythonic/include/types/int.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/uint8.hpp>
#include <pythonic/types/int.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/types/numpy_texpr.hpp>
#include <pythonic/include/types/complex.hpp>
#include <pythonic/include/__builtin__/range.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/__builtin__/None.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/include/numpy/square.hpp>
#include <pythonic/types/complex.hpp>
#include <pythonic/__builtin__/range.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/__builtin__/None.hpp>
#include <pythonic/operator_/div.hpp>
#include <pythonic/numpy/square.hpp>
namespace __pythran_util_pythran
{
  struct myfunc
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::numpy::functor::square{})>::type>::type>()(std::declval<__type0>())) __type1;
      typedef decltype((std::declval<__type1>() * std::declval<__type0>())) __type3;
      typedef decltype((std::declval<__type1>() + std::declval<__type3>())) __type4;
      typedef long __type5;
      typedef decltype((std::declval<__type4>() + std::declval<__type5>())) __type6;
      typedef double __type7;
      typedef typename pythonic::returnable<decltype((pythonic::operator_::div(std::declval<__type6>(), std::declval<__type7>())))>::type result_type;
    }  
    ;
    template <typename argument_type0 >
    typename type<argument_type0>::result_type operator()(argument_type0&& a) const
    ;
  }  ;
  struct rotfft_from_vecfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type2;
      typedef decltype((std::declval<__type1>() * std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type5;
      typedef decltype((std::declval<__type4>() * std::declval<__type5>())) __type6;
      typedef decltype((std::declval<__type3>() - std::declval<__type6>())) __type7;
      typedef typename pythonic::returnable<decltype((std::declval<__type0>() * std::declval<__type7>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& vecx_fft, argument_type1&& vecy_fft, argument_type2&& KX, argument_type3&& KY) const
    ;
  }  ;
  struct divfft_from_vecfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype((std::declval<__type1>() * std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type5;
      typedef decltype((std::declval<__type4>() * std::declval<__type5>())) __type6;
      typedef decltype((std::declval<__type3>() + std::declval<__type6>())) __type7;
      typedef typename pythonic::returnable<decltype((std::declval<__type0>() * std::declval<__type7>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& vecx_fft, argument_type1&& vecy_fft, argument_type2&& KX, argument_type3&& KY) const
    ;
  }  ;
  struct gradfft_from_fft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef decltype((std::declval<__type0>() * std::declval<__type1>())) __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type3;
      typedef decltype((std::declval<__type2>() * std::declval<__type3>())) __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type6;
      typedef decltype((std::declval<__type0>() * std::declval<__type6>())) __type7;
      typedef decltype((std::declval<__type7>() * std::declval<__type3>())) __type8;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type4>(), std::declval<__type8>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& f_fft, argument_type1&& KX, argument_type2&& KY) const
    ;
  }  ;
  struct vecfft_from_divfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type1;
      typedef decltype((std::declval<__type0>() * std::declval<__type1>())) __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type3;
      typedef decltype((std::declval<__type2>() * std::declval<__type3>())) __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type6;
      typedef decltype((std::declval<__type0>() * std::declval<__type6>())) __type7;
      typedef decltype((std::declval<__type7>() * std::declval<__type3>())) __type8;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type4>(), std::declval<__type8>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& div_fft, argument_type1&& KX_over_K2, argument_type2&& KY_over_K2) const
    ;
  }  ;
  struct vecfft_from_rotfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type1;
      typedef decltype((std::declval<__type0>() * std::declval<__type1>())) __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type3;
      typedef decltype((std::declval<__type2>() * std::declval<__type3>())) __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type6;
      typedef decltype((std::declval<__type0>() * std::declval<__type6>())) __type7;
      typedef decltype((std::declval<__type7>() * std::declval<__type3>())) __type8;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type4>(), std::declval<__type8>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
    typename type<argument_type0, argument_type1, argument_type2>::result_type operator()(argument_type0&& rot_fft, argument_type1&& KX_over_K2, argument_type2&& KY_over_K2) const
    ;
  }  ;
  struct dealiasing_variable
  {
    typedef void callable;
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    struct type
    {
      typedef double __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type1;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type1>())) __type2;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type2>::type::iterator>::value_type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type4;
      typedef decltype(std::declval<typename std::remove_cv<typename std::remove_reference<decltype(pythonic::__builtin__::functor::range{})>::type>::type>()(std::declval<__type4>())) __type5;
      typedef typename std::remove_cv<typename std::iterator_traits<typename std::remove_reference<__type5>::type::iterator>::value_type>::type __type6;
      typedef decltype(pythonic::types::make_tuple(std::declval<__type3>(), std::declval<__type6>())) __type7;
      typedef __type0 __ptype0;
      typedef __type7 __ptype1;
      typedef typename pythonic::returnable<pythonic::types::none_type>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type operator()(argument_type0&& ff_fft, argument_type1&& where, argument_type2&& nK0loc, argument_type3&& nK1loc) const
    ;
  }  ;
  template <typename argument_type0 >
  typename myfunc::type<argument_type0>::result_type myfunc::operator()(argument_type0&& a) const
  {
    return (pythonic::operator_::div(((pythonic::numpy::functor::square{}(a) + (pythonic::numpy::functor::square{}(a) * a)) + 2L), 5.0));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename rotfft_from_vecfft::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type rotfft_from_vecfft::operator()(argument_type0&& vecx_fft, argument_type1&& vecy_fft, argument_type2&& KX, argument_type3&& KY) const
  {
    return (std::complex<double>(0.0, 1.0) * ((KX * vecy_fft) - (KY * vecx_fft)));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename divfft_from_vecfft::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type divfft_from_vecfft::operator()(argument_type0&& vecx_fft, argument_type1&& vecy_fft, argument_type2&& KX, argument_type3&& KY) const
  {
    return (std::complex<double>(0.0, 1.0) * ((KX * vecx_fft) + (KY * vecy_fft)));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename gradfft_from_fft::type<argument_type0, argument_type1, argument_type2>::result_type gradfft_from_fft::operator()(argument_type0&& f_fft, argument_type1&& KX, argument_type2&& KY) const
  {
    ;
    ;
    return pythonic::types::make_tuple(((std::complex<double>(0.0, 1.0) * KX) * f_fft), ((std::complex<double>(0.0, 1.0) * KY) * f_fft));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename vecfft_from_divfft::type<argument_type0, argument_type1, argument_type2>::result_type vecfft_from_divfft::operator()(argument_type0&& div_fft, argument_type1&& KX_over_K2, argument_type2&& KY_over_K2) const
  {
    ;
    ;
    return pythonic::types::make_tuple(((std::complex<double>(-0.0, -1.0) * KX_over_K2) * div_fft), ((std::complex<double>(-0.0, -1.0) * KY_over_K2) * div_fft));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 >
  typename vecfft_from_rotfft::type<argument_type0, argument_type1, argument_type2>::result_type vecfft_from_rotfft::operator()(argument_type0&& rot_fft, argument_type1&& KX_over_K2, argument_type2&& KY_over_K2) const
  {
    ;
    ;
    return pythonic::types::make_tuple(((std::complex<double>(0.0, 1.0) * KY_over_K2) * rot_fft), ((std::complex<double>(-0.0, -1.0) * KX_over_K2) * rot_fft));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 >
  typename dealiasing_variable::type<argument_type0, argument_type1, argument_type2, argument_type3>::result_type dealiasing_variable::operator()(argument_type0&& ff_fft, argument_type1&& where, argument_type2&& nK0loc, argument_type3&& nK1loc) const
  {
    {
      long  __target1 = nK0loc;
      for (long  iK0=0L; iK0 < __target1; iK0 += 1L)
      {
        {
          long  __target2 = nK1loc;
          for (long  iK1=0L; iK1 < __target2; iK1 += 1L)
          {
            if (where.fast(pythonic::types::make_tuple(iK0, iK1)))
            {
              ff_fft.fast(pythonic::types::make_tuple(iK0, iK1)) = 0.0;
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
typename __pythran_util_pythran::myfunc::type<pythonic::types::ndarray<std::complex<double>,2>>::result_type myfunc0(pythonic::types::ndarray<std::complex<double>,2>&& a) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::myfunc()(a);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::myfunc::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>::result_type myfunc1(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& a) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::myfunc()(a);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::myfunc::type<pythonic::types::ndarray<double,2>>::result_type myfunc2(pythonic::types::ndarray<double,2>&& a) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::myfunc()(a);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::myfunc::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type myfunc3(pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& a) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::myfunc()(a);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type rotfft_from_vecfft0(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type rotfft_from_vecfft1(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type rotfft_from_vecfft2(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type rotfft_from_vecfft3(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type rotfft_from_vecfft4(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type rotfft_from_vecfft5(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type rotfft_from_vecfft6(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type rotfft_from_vecfft7(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type rotfft_from_vecfft8(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type rotfft_from_vecfft9(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type rotfft_from_vecfft10(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type rotfft_from_vecfft11(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type rotfft_from_vecfft12(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type rotfft_from_vecfft13(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type rotfft_from_vecfft14(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::rotfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type rotfft_from_vecfft15(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::rotfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type divfft_from_vecfft0(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type divfft_from_vecfft1(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type divfft_from_vecfft2(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type divfft_from_vecfft3(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type divfft_from_vecfft4(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type divfft_from_vecfft5(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type divfft_from_vecfft6(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type divfft_from_vecfft7(pythonic::types::ndarray<std::complex<double>,2>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type divfft_from_vecfft8(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type divfft_from_vecfft9(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type divfft_from_vecfft10(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type divfft_from_vecfft11(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::ndarray<std::complex<double>,2>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type divfft_from_vecfft12(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type divfft_from_vecfft13(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type divfft_from_vecfft14(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type divfft_from_vecfft15(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecx_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& vecy_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vecx_fft, vecy_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::gradfft_from_fft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type gradfft_from_fft0(pythonic::types::ndarray<std::complex<double>,2>&& f_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::gradfft_from_fft()(f_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::gradfft_from_fft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type gradfft_from_fft1(pythonic::types::ndarray<std::complex<double>,2>&& f_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::gradfft_from_fft()(f_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::gradfft_from_fft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type gradfft_from_fft2(pythonic::types::ndarray<std::complex<double>,2>&& f_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::gradfft_from_fft()(f_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::gradfft_from_fft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type gradfft_from_fft3(pythonic::types::ndarray<std::complex<double>,2>&& f_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::gradfft_from_fft()(f_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::gradfft_from_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type gradfft_from_fft4(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& f_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::gradfft_from_fft()(f_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::gradfft_from_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type gradfft_from_fft5(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& f_fft, pythonic::types::ndarray<double,2>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::gradfft_from_fft()(f_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::gradfft_from_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type gradfft_from_fft6(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& f_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::ndarray<double,2>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::gradfft_from_fft()(f_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::gradfft_from_fft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type gradfft_from_fft7(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& f_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::gradfft_from_fft()(f_fft, KX, KY);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_divfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type vecfft_from_divfft0(pythonic::types::ndarray<std::complex<double>,2>&& div_fft, pythonic::types::ndarray<double,2>&& KX_over_K2, pythonic::types::ndarray<double,2>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_divfft()(div_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_divfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type vecfft_from_divfft1(pythonic::types::ndarray<std::complex<double>,2>&& div_fft, pythonic::types::ndarray<double,2>&& KX_over_K2, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_divfft()(div_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_divfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type vecfft_from_divfft2(pythonic::types::ndarray<std::complex<double>,2>&& div_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX_over_K2, pythonic::types::ndarray<double,2>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_divfft()(div_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_divfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type vecfft_from_divfft3(pythonic::types::ndarray<std::complex<double>,2>&& div_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX_over_K2, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_divfft()(div_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_divfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type vecfft_from_divfft4(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& div_fft, pythonic::types::ndarray<double,2>&& KX_over_K2, pythonic::types::ndarray<double,2>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_divfft()(div_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_divfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type vecfft_from_divfft5(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& div_fft, pythonic::types::ndarray<double,2>&& KX_over_K2, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_divfft()(div_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_divfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type vecfft_from_divfft6(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& div_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX_over_K2, pythonic::types::ndarray<double,2>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_divfft()(div_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_divfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type vecfft_from_divfft7(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& div_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX_over_K2, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_divfft()(div_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_rotfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type vecfft_from_rotfft0(pythonic::types::ndarray<std::complex<double>,2>&& rot_fft, pythonic::types::ndarray<double,2>&& KX_over_K2, pythonic::types::ndarray<double,2>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_rotfft()(rot_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_rotfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type vecfft_from_rotfft1(pythonic::types::ndarray<std::complex<double>,2>&& rot_fft, pythonic::types::ndarray<double,2>&& KX_over_K2, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_rotfft()(rot_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_rotfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type vecfft_from_rotfft2(pythonic::types::ndarray<std::complex<double>,2>&& rot_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX_over_K2, pythonic::types::ndarray<double,2>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_rotfft()(rot_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_rotfft::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type vecfft_from_rotfft3(pythonic::types::ndarray<std::complex<double>,2>&& rot_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX_over_K2, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_rotfft()(rot_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_rotfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::ndarray<double,2>>::result_type vecfft_from_rotfft4(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& rot_fft, pythonic::types::ndarray<double,2>&& KX_over_K2, pythonic::types::ndarray<double,2>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_rotfft()(rot_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_rotfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<double,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type vecfft_from_rotfft5(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& rot_fft, pythonic::types::ndarray<double,2>&& KX_over_K2, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_rotfft()(rot_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_rotfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::ndarray<double,2>>::result_type vecfft_from_rotfft6(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& rot_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX_over_K2, pythonic::types::ndarray<double,2>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_rotfft()(rot_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::vecfft_from_rotfft::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>::result_type vecfft_from_rotfft7(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& rot_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KX_over_K2, pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>&& KY_over_K2) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::vecfft_from_rotfft()(rot_fft, KX_over_K2, KY_over_K2);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::dealiasing_variable::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::ndarray<uint8_t,2>, long, long>::result_type dealiasing_variable0(pythonic::types::ndarray<std::complex<double>,2>&& ff_fft, pythonic::types::ndarray<uint8_t,2>&& where, long&& nK0loc, long&& nK1loc) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::dealiasing_variable()(ff_fft, where, nK0loc, nK1loc);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::dealiasing_variable::type<pythonic::types::ndarray<std::complex<double>,2>, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>, long, long>::result_type dealiasing_variable1(pythonic::types::ndarray<std::complex<double>,2>&& ff_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>&& where, long&& nK0loc, long&& nK1loc) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::dealiasing_variable()(ff_fft, where, nK0loc, nK1loc);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::dealiasing_variable::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::ndarray<uint8_t,2>, long, long>::result_type dealiasing_variable2(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& ff_fft, pythonic::types::ndarray<uint8_t,2>&& where, long&& nK0loc, long&& nK1loc) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::dealiasing_variable()(ff_fft, where, nK0loc, nK1loc);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::dealiasing_variable::type<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>, long, long>::result_type dealiasing_variable3(pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>&& ff_fft, pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>&& where, long&& nK0loc, long&& nK1loc) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::dealiasing_variable()(ff_fft, where, nK0loc, nK1loc);
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
__pythran_wrap_myfunc0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    char const* keywords[] = {"a", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords, &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]))
        return to_python(myfunc0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_myfunc1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    char const* keywords[] = {"a", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords, &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]))
        return to_python(myfunc1(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_myfunc2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    char const* keywords[] = {"a", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords, &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<double,2>>(args_obj[0]))
        return to_python(myfunc2(from_python<pythonic::types::ndarray<double,2>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_myfunc3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[1+1];
    char const* keywords[] = {"a", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "O",
                                     (char**)keywords, &args_obj[0]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0]))
        return to_python(myfunc3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[0])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(rotfft_from_vecfft0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(rotfft_from_vecfft1(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(rotfft_from_vecfft2(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(rotfft_from_vecfft3(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(rotfft_from_vecfft4(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(rotfft_from_vecfft5(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(rotfft_from_vecfft6(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(rotfft_from_vecfft7(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft8(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(rotfft_from_vecfft8(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft9(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(rotfft_from_vecfft9(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft10(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(rotfft_from_vecfft10(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft11(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(rotfft_from_vecfft11(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft12(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(rotfft_from_vecfft12(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft13(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(rotfft_from_vecfft13(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft14(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(rotfft_from_vecfft14(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_rotfft_from_vecfft15(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(rotfft_from_vecfft15(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(divfft_from_vecfft0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(divfft_from_vecfft1(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(divfft_from_vecfft2(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(divfft_from_vecfft3(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(divfft_from_vecfft4(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(divfft_from_vecfft5(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(divfft_from_vecfft6(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(divfft_from_vecfft7(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft8(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(divfft_from_vecfft8(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft9(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(divfft_from_vecfft9(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft10(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(divfft_from_vecfft10(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft11(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(divfft_from_vecfft11(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft12(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(divfft_from_vecfft12(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft13(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(divfft_from_vecfft13(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft14(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[3]))
        return to_python(divfft_from_vecfft14(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::ndarray<double,2>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_divfft_from_vecfft15(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"vecx_fft","vecy_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3]))
        return to_python(divfft_from_vecfft15(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_gradfft_from_fft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"f_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(gradfft_from_fft0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_gradfft_from_fft1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"f_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(gradfft_from_fft1(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_gradfft_from_fft2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"f_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(gradfft_from_fft2(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_gradfft_from_fft3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"f_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(gradfft_from_fft3(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_gradfft_from_fft4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"f_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(gradfft_from_fft4(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_gradfft_from_fft5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"f_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(gradfft_from_fft5(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_gradfft_from_fft6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"f_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(gradfft_from_fft6(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_gradfft_from_fft7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"f_fft","KX","KY", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(gradfft_from_fft7(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_divfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"div_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(vecfft_from_divfft0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_divfft1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"div_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(vecfft_from_divfft1(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_divfft2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"div_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(vecfft_from_divfft2(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_divfft3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"div_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(vecfft_from_divfft3(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_divfft4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"div_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(vecfft_from_divfft4(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_divfft5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"div_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(vecfft_from_divfft5(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_divfft6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"div_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(vecfft_from_divfft6(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_divfft7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"div_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(vecfft_from_divfft7(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_rotfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"rot_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(vecfft_from_rotfft0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_rotfft1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"rot_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(vecfft_from_rotfft1(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_rotfft2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"rot_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(vecfft_from_rotfft2(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_rotfft3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"rot_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(vecfft_from_rotfft3(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_rotfft4(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"rot_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(vecfft_from_rotfft4(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_rotfft5(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"rot_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(vecfft_from_rotfft5(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<double,2>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_rotfft6(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"rot_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<double,2>>(args_obj[2]))
        return to_python(vecfft_from_rotfft6(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::ndarray<double,2>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_vecfft_from_rotfft7(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[3+1];
    char const* keywords[] = {"rot_fft","KX_over_K2","KY_over_K2", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2]))
        return to_python(vecfft_from_rotfft7(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[1]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<double,2>>>(args_obj[2])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_dealiasing_variable0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"ff_fft","where","nK0loc","nK1loc", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,2>>(args_obj[1]) && is_convertible<long>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(dealiasing_variable0(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,2>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_dealiasing_variable1(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"ff_fft","where","nK0loc","nK1loc", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>>(args_obj[1]) && is_convertible<long>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(dealiasing_variable1(from_python<pythonic::types::ndarray<std::complex<double>,2>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_dealiasing_variable2(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"ff_fft","where","nK0loc","nK1loc", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<uint8_t,2>>(args_obj[1]) && is_convertible<long>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(dealiasing_variable2(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::ndarray<uint8_t,2>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_dealiasing_variable3(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[4+1];
    char const* keywords[] = {"ff_fft","where","nK0loc","nK1loc", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3]))
        return nullptr;
    if(is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]) && is_convertible<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>>(args_obj[1]) && is_convertible<long>(args_obj[2]) && is_convertible<long>(args_obj[3]))
        return to_python(dealiasing_variable3(from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<std::complex<double>,2>>>(args_obj[0]), from_python<pythonic::types::numpy_texpr<pythonic::types::ndarray<uint8_t,2>>>(args_obj[1]), from_python<long>(args_obj[2]), from_python<long>(args_obj[3])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_myfunc(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_myfunc0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_myfunc1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_myfunc2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_myfunc3(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `myfunc'.\n"
                "Candidates are:\n   myfunc(ndarray<std.complex<double>,2>)\n   myfunc(numpy_texpr<ndarray<std.complex<double>,2>>)\n   myfunc(ndarray<double,2>)\n   myfunc(numpy_texpr<ndarray<double,2>>)\n"
                );
                return nullptr;
                });
            }


            static PyObject *
            __pythran_wrapall_rotfft_from_vecfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft7(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft8(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft9(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft10(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft11(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft12(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft13(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft14(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_rotfft_from_vecfft15(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `rotfft_from_vecfft'.\n"
                "Candidates are:\n   rotfft_from_vecfft(ndarray<std.complex<double>,2>,ndarray<std.complex<double>,2>,ndarray<double,2>,ndarray<double,2>)\n   rotfft_from_vecfft(ndarray<std.complex<double>,2>,ndarray<std.complex<double>,2>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   rotfft_from_vecfft(ndarray<std.complex<double>,2>,ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   rotfft_from_vecfft(ndarray<std.complex<double>,2>,ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n   rotfft_from_vecfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,ndarray<double,2>)\n   rotfft_from_vecfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   rotfft_from_vecfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   rotfft_from_vecfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n   rotfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<std.complex<double>,2>,ndarray<double,2>,ndarray<double,2>)\n   rotfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<std.complex<double>,2>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   rotfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   rotfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n   rotfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,ndarray<double,2>)\n   rotfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   rotfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   rotfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n"
                );
                return nullptr;
                });
            }


            static PyObject *
            __pythran_wrapall_divfft_from_vecfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_divfft_from_vecfft0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft7(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft8(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft9(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft10(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft11(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft12(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft13(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft14(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_divfft_from_vecfft15(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `divfft_from_vecfft'.\n"
                "Candidates are:\n   divfft_from_vecfft(ndarray<std.complex<double>,2>,ndarray<std.complex<double>,2>,ndarray<double,2>,ndarray<double,2>)\n   divfft_from_vecfft(ndarray<std.complex<double>,2>,ndarray<std.complex<double>,2>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   divfft_from_vecfft(ndarray<std.complex<double>,2>,ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   divfft_from_vecfft(ndarray<std.complex<double>,2>,ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n   divfft_from_vecfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,ndarray<double,2>)\n   divfft_from_vecfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   divfft_from_vecfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   divfft_from_vecfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n   divfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<std.complex<double>,2>,ndarray<double,2>,ndarray<double,2>)\n   divfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<std.complex<double>,2>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   divfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   divfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n   divfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,ndarray<double,2>)\n   divfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   divfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   divfft_from_vecfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n"
                );
                return nullptr;
                });
            }


            static PyObject *
            __pythran_wrapall_gradfft_from_fft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_gradfft_from_fft0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_gradfft_from_fft1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_gradfft_from_fft2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_gradfft_from_fft3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_gradfft_from_fft4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_gradfft_from_fft5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_gradfft_from_fft6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_gradfft_from_fft7(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `gradfft_from_fft'.\n"
                "Candidates are:\n   gradfft_from_fft(ndarray<std.complex<double>,2>,ndarray<double,2>,ndarray<double,2>)\n   gradfft_from_fft(ndarray<std.complex<double>,2>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   gradfft_from_fft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   gradfft_from_fft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n   gradfft_from_fft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,ndarray<double,2>)\n   gradfft_from_fft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   gradfft_from_fft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   gradfft_from_fft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n"
                );
                return nullptr;
                });
            }


            static PyObject *
            __pythran_wrapall_vecfft_from_divfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_vecfft_from_divfft0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_divfft1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_divfft2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_divfft3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_divfft4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_divfft5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_divfft6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_divfft7(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `vecfft_from_divfft'.\n"
                "Candidates are:\n   vecfft_from_divfft(ndarray<std.complex<double>,2>,ndarray<double,2>,ndarray<double,2>)\n   vecfft_from_divfft(ndarray<std.complex<double>,2>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   vecfft_from_divfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   vecfft_from_divfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n   vecfft_from_divfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,ndarray<double,2>)\n   vecfft_from_divfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   vecfft_from_divfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   vecfft_from_divfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n"
                );
                return nullptr;
                });
            }


            static PyObject *
            __pythran_wrapall_vecfft_from_rotfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_vecfft_from_rotfft0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_rotfft1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_rotfft2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_rotfft3(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_rotfft4(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_rotfft5(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_rotfft6(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_vecfft_from_rotfft7(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `vecfft_from_rotfft'.\n"
                "Candidates are:\n   vecfft_from_rotfft(ndarray<std.complex<double>,2>,ndarray<double,2>,ndarray<double,2>)\n   vecfft_from_rotfft(ndarray<std.complex<double>,2>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   vecfft_from_rotfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   vecfft_from_rotfft(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n   vecfft_from_rotfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,ndarray<double,2>)\n   vecfft_from_rotfft(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<double,2>,numpy_texpr<ndarray<double,2>>)\n   vecfft_from_rotfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,ndarray<double,2>)\n   vecfft_from_rotfft(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<double,2>>,numpy_texpr<ndarray<double,2>>)\n"
                );
                return nullptr;
                });
            }


            static PyObject *
            __pythran_wrapall_dealiasing_variable(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_dealiasing_variable0(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_dealiasing_variable1(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_dealiasing_variable2(self, args, kw))
    return obj;
PyErr_Clear();


if(PyObject* obj = __pythran_wrap_dealiasing_variable3(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `dealiasing_variable'.\n"
                "Candidates are:\n   dealiasing_variable(ndarray<std.complex<double>,2>,ndarray<uint8_t,2>,long,long)\n   dealiasing_variable(ndarray<std.complex<double>,2>,numpy_texpr<ndarray<uint8_t,2>>,long,long)\n   dealiasing_variable(numpy_texpr<ndarray<std.complex<double>,2>>,ndarray<uint8_t,2>,long,long)\n   dealiasing_variable(numpy_texpr<ndarray<std.complex<double>,2>>,numpy_texpr<ndarray<uint8_t,2>>,long,long)\n"
                );
                return nullptr;
                });
            }


static PyMethodDef Methods[] = {
    {
    "myfunc",
    (PyCFunction)__pythran_wrapall_myfunc,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - myfunc(complex128[][])\n    - myfunc(complex128[][].T)\n    - myfunc(float64[][])\n    - myfunc(float64[][].T)\n"},{
    "rotfft_from_vecfft",
    (PyCFunction)__pythran_wrapall_rotfft_from_vecfft,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - rotfft_from_vecfft(complex128[][], complex128[][], float64[][], float64[][])\n    - rotfft_from_vecfft(complex128[][], complex128[][], float64[][], float64[][].T)\n    - rotfft_from_vecfft(complex128[][], complex128[][], float64[][].T, float64[][])\n    - rotfft_from_vecfft(complex128[][], complex128[][], float64[][].T, float64[][].T)\n    - rotfft_from_vecfft(complex128[][], complex128[][].T, float64[][], float64[][])\n    - rotfft_from_vecfft(complex128[][], complex128[][].T, float64[][], float64[][].T)\n    - rotfft_from_vecfft(complex128[][], complex128[][].T, float64[][].T, float64[][])\n    - rotfft_from_vecfft(complex128[][], complex128[][].T, float64[][].T, float64[][].T)\n    - rotfft_from_vecfft(complex128[][].T, complex128[][], float64[][], float64[][])\n    - rotfft_from_vecfft(complex128[][].T, complex128[][], float64[][], float64[][].T)\n    - rotfft_from_vecfft(complex128[][].T, complex128[][], float64[][].T, float64[][])\n    - rotfft_from_vecfft(complex128[][].T, complex128[][], float64[][].T, float64[][].T)\n    - rotfft_from_vecfft(complex128[][].T, complex128[][].T, float64[][], float64[][])\n    - rotfft_from_vecfft(complex128[][].T, complex128[][].T, float64[][], float64[][].T)\n    - rotfft_from_vecfft(complex128[][].T, complex128[][].T, float64[][].T, float64[][])\n    - rotfft_from_vecfft(complex128[][].T, complex128[][].T, float64[][].T, float64[][].T)\n"},{
    "divfft_from_vecfft",
    (PyCFunction)__pythran_wrapall_divfft_from_vecfft,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - divfft_from_vecfft(complex128[][], complex128[][], float64[][], float64[][])\n    - divfft_from_vecfft(complex128[][], complex128[][], float64[][], float64[][].T)\n    - divfft_from_vecfft(complex128[][], complex128[][], float64[][].T, float64[][])\n    - divfft_from_vecfft(complex128[][], complex128[][], float64[][].T, float64[][].T)\n    - divfft_from_vecfft(complex128[][], complex128[][].T, float64[][], float64[][])\n    - divfft_from_vecfft(complex128[][], complex128[][].T, float64[][], float64[][].T)\n    - divfft_from_vecfft(complex128[][], complex128[][].T, float64[][].T, float64[][])\n    - divfft_from_vecfft(complex128[][], complex128[][].T, float64[][].T, float64[][].T)\n    - divfft_from_vecfft(complex128[][].T, complex128[][], float64[][], float64[][])\n    - divfft_from_vecfft(complex128[][].T, complex128[][], float64[][], float64[][].T)\n    - divfft_from_vecfft(complex128[][].T, complex128[][], float64[][].T, float64[][])\n    - divfft_from_vecfft(complex128[][].T, complex128[][], float64[][].T, float64[][].T)\n    - divfft_from_vecfft(complex128[][].T, complex128[][].T, float64[][], float64[][])\n    - divfft_from_vecfft(complex128[][].T, complex128[][].T, float64[][], float64[][].T)\n    - divfft_from_vecfft(complex128[][].T, complex128[][].T, float64[][].T, float64[][])\n    - divfft_from_vecfft(complex128[][].T, complex128[][].T, float64[][].T, float64[][].T)\n"},{
    "gradfft_from_fft",
    (PyCFunction)__pythran_wrapall_gradfft_from_fft,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - gradfft_from_fft(complex128[][], float64[][], float64[][])\n    - gradfft_from_fft(complex128[][], float64[][], float64[][].T)\n    - gradfft_from_fft(complex128[][], float64[][].T, float64[][])\n    - gradfft_from_fft(complex128[][], float64[][].T, float64[][].T)\n    - gradfft_from_fft(complex128[][].T, float64[][], float64[][])\n    - gradfft_from_fft(complex128[][].T, float64[][], float64[][].T)\n    - gradfft_from_fft(complex128[][].T, float64[][].T, float64[][])\n    - gradfft_from_fft(complex128[][].T, float64[][].T, float64[][].T)\nReturn the gradient of f_fft in spectral space."},{
    "vecfft_from_divfft",
    (PyCFunction)__pythran_wrapall_vecfft_from_divfft,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - vecfft_from_divfft(complex128[][], float64[][], float64[][])\n    - vecfft_from_divfft(complex128[][], float64[][], float64[][].T)\n    - vecfft_from_divfft(complex128[][], float64[][].T, float64[][])\n    - vecfft_from_divfft(complex128[][], float64[][].T, float64[][].T)\n    - vecfft_from_divfft(complex128[][].T, float64[][], float64[][])\n    - vecfft_from_divfft(complex128[][].T, float64[][], float64[][].T)\n    - vecfft_from_divfft(complex128[][].T, float64[][].T, float64[][])\n    - vecfft_from_divfft(complex128[][].T, float64[][].T, float64[][].T)\nReturn the velocity in spectral space computed from the divergence.\n"},{
    "vecfft_from_rotfft",
    (PyCFunction)__pythran_wrapall_vecfft_from_rotfft,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - vecfft_from_rotfft(complex128[][], float64[][], float64[][])\n    - vecfft_from_rotfft(complex128[][], float64[][], float64[][].T)\n    - vecfft_from_rotfft(complex128[][], float64[][].T, float64[][])\n    - vecfft_from_rotfft(complex128[][], float64[][].T, float64[][].T)\n    - vecfft_from_rotfft(complex128[][].T, float64[][], float64[][])\n    - vecfft_from_rotfft(complex128[][].T, float64[][], float64[][].T)\n    - vecfft_from_rotfft(complex128[][].T, float64[][].T, float64[][])\n    - vecfft_from_rotfft(complex128[][].T, float64[][].T, float64[][].T)\nReturn the velocity in spectral space computed from the rotational.\n"},{
    "dealiasing_variable",
    (PyCFunction)__pythran_wrapall_dealiasing_variable,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - dealiasing_variable(complex128[][], uint8[][], int, int)\n    - dealiasing_variable(complex128[][], uint8[][].T, int, int)\n    - dealiasing_variable(complex128[][].T, uint8[][], int, int)\n    - dealiasing_variable(complex128[][].T, uint8[][].T, int, int)\n"},
    {NULL, NULL, 0, NULL}
};


#if PY_MAJOR_VERSION >= 3
  static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "util_pythran",            /* m_name */
    "\n\n[pythran]\ncomplex_hook = True\n\n",         /* m_doc */
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
                                         "\n\n[pythran]\ncomplex_hook = True\n\n"
    );
    #endif
    if(! theModule)
        PYTHRAN_RETURN;
    PyObject * theDoc = Py_BuildValue("(sss)",
                                      "0.8.4",
                                      "2018-02-14 18:50:16.816101",
                                      "b03c551c0e662f410962ffa582bae69a4fb4ae2d615fbeb87fa22aaeb52482c8");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif