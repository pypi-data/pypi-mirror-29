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
#include <pythonic/include/types/ndarray.hpp>
#include <pythonic/types/ndarray.hpp>
#include <pythonic/types/float64.hpp>
#include <pythonic/types/complex128.hpp>
#include <pythonic/include/__builtin__/tuple.hpp>
#include <pythonic/include/types/complex.hpp>
#include <pythonic/include/operator_/div.hpp>
#include <pythonic/__builtin__/tuple.hpp>
#include <pythonic/types/complex.hpp>
#include <pythonic/operator_/div.hpp>
namespace __pythran_util_pythran
{
  struct divfft_from_vecfft
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    struct type
    {
      typedef std::complex<double> __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type1;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type2;
      typedef decltype((std::declval<__type1>() * std::declval<__type2>())) __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type4;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type5;
      typedef decltype((std::declval<__type4>() * std::declval<__type5>())) __type6;
      typedef decltype((std::declval<__type3>() + std::declval<__type6>())) __type7;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type8;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type9;
      typedef decltype((std::declval<__type8>() * std::declval<__type9>())) __type10;
      typedef decltype((std::declval<__type7>() + std::declval<__type10>())) __type11;
      typedef typename pythonic::returnable<decltype((std::declval<__type0>() * std::declval<__type11>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type operator()(argument_type0&& vx_fft, argument_type1&& vy_fft, argument_type2&& vz_fft, argument_type3&& kx, argument_type4&& ky, argument_type5&& kz) const
    ;
  }  ;
  struct project_perpk3d
  {
    typedef void callable;
    typedef void pure;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 >
    struct type
    {
      typedef typename std::remove_cv<typename std::remove_reference<argument_type0>::type>::type __type0;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type3>::type>::type __type1;
      typedef decltype((std::declval<__type1>() * std::declval<__type0>())) __type2;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type4>::type>::type __type3;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type1>::type>::type __type4;
      typedef decltype((std::declval<__type3>() * std::declval<__type4>())) __type5;
      typedef decltype((std::declval<__type2>() + std::declval<__type5>())) __type6;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type5>::type>::type __type7;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type2>::type>::type __type8;
      typedef decltype((std::declval<__type7>() * std::declval<__type8>())) __type9;
      typedef decltype((std::declval<__type6>() + std::declval<__type9>())) __type10;
      typedef typename std::remove_cv<typename std::remove_reference<argument_type6>::type>::type __type11;
      typedef typename pythonic::assignable<decltype((pythonic::operator_::div(std::declval<__type10>(), std::declval<__type11>())))>::type __type12;
      typedef decltype((std::declval<__type1>() * std::declval<__type12>())) __type13;
      typedef decltype((std::declval<__type0>() - std::declval<__type13>())) __type14;
      typedef decltype((std::declval<__type3>() * std::declval<__type12>())) __type15;
      typedef decltype((std::declval<__type4>() - std::declval<__type15>())) __type16;
      typedef decltype((std::declval<__type7>() * std::declval<__type12>())) __type17;
      typedef decltype((std::declval<__type8>() - std::declval<__type17>())) __type18;
      typedef typename pythonic::returnable<decltype(pythonic::types::make_tuple(std::declval<__type14>(), std::declval<__type16>(), std::declval<__type18>()))>::type result_type;
    }  
    ;
    template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 >
    typename type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5, argument_type6>::result_type operator()(argument_type0&& vx_fft, argument_type1&& vy_fft, argument_type2&& vz_fft, argument_type3&& Kx, argument_type4&& Ky, argument_type5&& Kz, argument_type6&& K_square_nozero) const
    ;
  }  ;
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 >
  typename divfft_from_vecfft::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5>::result_type divfft_from_vecfft::operator()(argument_type0&& vx_fft, argument_type1&& vy_fft, argument_type2&& vz_fft, argument_type3&& kx, argument_type4&& ky, argument_type5&& kz) const
  {
    return (std::complex<double>(0.0, 1.0) * (((kx * vx_fft) + (ky * vy_fft)) + (kz * vz_fft)));
  }
  template <typename argument_type0 , typename argument_type1 , typename argument_type2 , typename argument_type3 , typename argument_type4 , typename argument_type5 , typename argument_type6 >
  typename project_perpk3d::type<argument_type0, argument_type1, argument_type2, argument_type3, argument_type4, argument_type5, argument_type6>::result_type project_perpk3d::operator()(argument_type0&& vx_fft, argument_type1&& vy_fft, argument_type2&& vz_fft, argument_type3&& Kx, argument_type4&& Ky, argument_type5&& Kz, argument_type6&& K_square_nozero) const
  {
    typename pythonic::assignable<decltype((pythonic::operator_::div((((Kx * vx_fft) + (Ky * vy_fft)) + (Kz * vz_fft)), K_square_nozero)))>::type tmp = (pythonic::operator_::div((((Kx * vx_fft) + (Ky * vy_fft)) + (Kz * vz_fft)), K_square_nozero));
    return pythonic::types::make_tuple((vx_fft - (Kx * tmp)), (vy_fft - (Ky * tmp)), (vz_fft - (Kz * tmp)));
  }
}
#include <pythonic/python/exception_handler.hpp>
#ifdef ENABLE_PYTHON_MODULE
typename __pythran_util_pythran::divfft_from_vecfft::type<pythonic::types::ndarray<std::complex<double>,3>, pythonic::types::ndarray<std::complex<double>,3>, pythonic::types::ndarray<std::complex<double>,3>, pythonic::types::ndarray<double,3>, pythonic::types::ndarray<double,3>, pythonic::types::ndarray<double,3>>::result_type divfft_from_vecfft0(pythonic::types::ndarray<std::complex<double>,3>&& vx_fft, pythonic::types::ndarray<std::complex<double>,3>&& vy_fft, pythonic::types::ndarray<std::complex<double>,3>&& vz_fft, pythonic::types::ndarray<double,3>&& kx, pythonic::types::ndarray<double,3>&& ky, pythonic::types::ndarray<double,3>&& kz) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::divfft_from_vecfft()(vx_fft, vy_fft, vz_fft, kx, ky, kz);
                                PyEval_RestoreThread(_save);
                                return res;
                            }
                            catch(...) {
                                PyEval_RestoreThread(_save);
                                throw;
                            }
                            ;
}
typename __pythran_util_pythran::project_perpk3d::type<pythonic::types::ndarray<std::complex<double>,3>, pythonic::types::ndarray<std::complex<double>,3>, pythonic::types::ndarray<std::complex<double>,3>, pythonic::types::ndarray<double,3>, pythonic::types::ndarray<double,3>, pythonic::types::ndarray<double,3>, pythonic::types::ndarray<double,3>>::result_type project_perpk3d0(pythonic::types::ndarray<std::complex<double>,3>&& vx_fft, pythonic::types::ndarray<std::complex<double>,3>&& vy_fft, pythonic::types::ndarray<std::complex<double>,3>&& vz_fft, pythonic::types::ndarray<double,3>&& Kx, pythonic::types::ndarray<double,3>&& Ky, pythonic::types::ndarray<double,3>&& Kz, pythonic::types::ndarray<double,3>&& K_square_nozero) 
{
  
                            PyThreadState *_save = PyEval_SaveThread();
                            try {
                                auto res = __pythran_util_pythran::project_perpk3d()(vx_fft, vy_fft, vz_fft, Kx, Ky, Kz, K_square_nozero);
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
__pythran_wrap_divfft_from_vecfft0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[6+1];
    char const* keywords[] = {"vx_fft","vy_fft","vz_fft","kx","ky","kz", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,3>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,3>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,3>>(args_obj[5]))
        return to_python(divfft_from_vecfft0(from_python<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[2]), from_python<pythonic::types::ndarray<double,3>>(args_obj[3]), from_python<pythonic::types::ndarray<double,3>>(args_obj[4]), from_python<pythonic::types::ndarray<double,3>>(args_obj[5])));
    else {
        return nullptr;
    }
}

static PyObject *
__pythran_wrap_project_perpk3d0(PyObject *self, PyObject *args, PyObject *kw)
{
    PyObject* args_obj[7+1];
    char const* keywords[] = {"vx_fft","vy_fft","vz_fft","Kx","Ky","Kz","K_square_nozero", nullptr};
    if(! PyArg_ParseTupleAndKeywords(args, kw, "OOOOOOO",
                                     (char**)keywords, &args_obj[0], &args_obj[1], &args_obj[2], &args_obj[3], &args_obj[4], &args_obj[5], &args_obj[6]))
        return nullptr;
    if(is_convertible<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[0]) && is_convertible<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[1]) && is_convertible<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[2]) && is_convertible<pythonic::types::ndarray<double,3>>(args_obj[3]) && is_convertible<pythonic::types::ndarray<double,3>>(args_obj[4]) && is_convertible<pythonic::types::ndarray<double,3>>(args_obj[5]) && is_convertible<pythonic::types::ndarray<double,3>>(args_obj[6]))
        return to_python(project_perpk3d0(from_python<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[0]), from_python<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[1]), from_python<pythonic::types::ndarray<std::complex<double>,3>>(args_obj[2]), from_python<pythonic::types::ndarray<double,3>>(args_obj[3]), from_python<pythonic::types::ndarray<double,3>>(args_obj[4]), from_python<pythonic::types::ndarray<double,3>>(args_obj[5]), from_python<pythonic::types::ndarray<double,3>>(args_obj[6])));
    else {
        return nullptr;
    }
}

            static PyObject *
            __pythran_wrapall_divfft_from_vecfft(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_divfft_from_vecfft0(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `divfft_from_vecfft'.\n"
                "Candidates are:\n   divfft_from_vecfft(ndarray<std.complex<double>,3>,ndarray<std.complex<double>,3>,ndarray<std.complex<double>,3>,ndarray<double,3>,ndarray<double,3>,ndarray<double,3>)\n"
                );
                return nullptr;
                });
            }


            static PyObject *
            __pythran_wrapall_project_perpk3d(PyObject *self, PyObject *args, PyObject *kw)
            {
                return pythonic::handle_python_exception([self, args, kw]()
                -> PyObject* {

if(PyObject* obj = __pythran_wrap_project_perpk3d0(self, args, kw))
    return obj;
PyErr_Clear();

                PyErr_SetString(PyExc_TypeError,
                "Invalid argument type for pythranized function `project_perpk3d'.\n"
                "Candidates are:\n   project_perpk3d(ndarray<std.complex<double>,3>,ndarray<std.complex<double>,3>,ndarray<std.complex<double>,3>,ndarray<double,3>,ndarray<double,3>,ndarray<double,3>,ndarray<double,3>)\n"
                );
                return nullptr;
                });
            }


static PyMethodDef Methods[] = {
    {
    "divfft_from_vecfft",
    (PyCFunction)__pythran_wrapall_divfft_from_vecfft,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - divfft_from_vecfft(complex128[][][], complex128[][][], complex128[][][], float64[][][], float64[][][], float64[][][])\nCompute the divergence of a vector (in spectral space)\n"},{
    "project_perpk3d",
    (PyCFunction)__pythran_wrapall_project_perpk3d,
    METH_VARARGS | METH_KEYWORDS,
    "Supported prototypes:\n    - project_perpk3d(complex128[][][], complex128[][][], complex128[][][], float64[][][], float64[][][], float64[][][], float64[][][])\n"},
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
                                      "0.8.4",
                                      "2018-02-14 18:50:17.123327",
                                      "683d586f6a44ece9d68c748626c672a90c957c4a37dd399eb8557611a5223177");
    if(! theDoc)
        PYTHRAN_RETURN;
    PyModule_AddObject(theModule,
                       "__pythran__",
                       theDoc);


    PYTHRAN_RETURN;
}

#endif