#ifndef INCLUDED_VOLK_32f_NORMALIZE_ALIGNED16_H
#define INCLUDED_VOLK_32f_NORMALIZE_ALIGNED16_H

#include <inttypes.h>
#include <stdio.h>

#if LV_HAVE_SSE
#include <xmmintrin.h>
/*!
  \brief Normalizes all points in the buffer by the scalar value ( divides each data point by the scalar value )
  \param vecBuffer The buffer of values to be vectorized
  \param num_points The number of values in vecBuffer
  \param scalar The scale value to be applied to each buffer value
*/
static inline void volk_32f_normalize_aligned16_sse(float* vecBuffer, const float scalar, unsigned int num_points){
  unsigned int number = 0;
  float* inputPtr = vecBuffer;

  const float invScalar = 1.0 / scalar;
  __m128 vecScalar = _mm_set_ps1(invScalar);

  __m128 input1;

  const uint64_t quarterPoints = num_points / 4;
  for(;number < quarterPoints; number++){

    input1 = _mm_load_ps(inputPtr);

    input1 = _mm_mul_ps(input1, vecScalar);

    _mm_store_ps(inputPtr, input1);

    inputPtr += 4;
  }

  number = quarterPoints*4;
  for(; number < num_points; number++){
    *inputPtr *= invScalar;
    inputPtr++;
  }
}
#endif /* LV_HAVE_SSE */

#if LV_HAVE_GENERIC
/*!
  \brief Normalizes the two input vectors and store their results in the third vector
  \param cVector The vector where the results will be stored
  \param aVector One of the vectors to be normalizeed
  \param bVector One of the vectors to be normalizeed
  \param num_points The number of values in aVector and bVector to be normalizeed together and stored into cVector
*/
static inline void volk_32f_normalize_aligned16_generic(float* vecBuffer, const float scalar, unsigned int num_points){
  unsigned int number = 0;
  float* inputPtr = vecBuffer;
  const float invScalar = 1.0 / scalar;
  for(number = 0; number < num_points; number++){
    *inputPtr *= invScalar;
    inputPtr++;
  }
}
#endif /* LV_HAVE_GENERIC */




#endif /* INCLUDED_VOLK_32f_NORMALIZE_ALIGNED16_H */
