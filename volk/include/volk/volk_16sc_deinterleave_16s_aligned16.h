#ifndef INCLUDED_VOLK_16sc_DEINTERLEAVE_16S_ALIGNED16_H
#define INCLUDED_VOLK_16sc_DEINTERLEAVE_16S_ALIGNED16_H

#include <inttypes.h>
#include <stdio.h>

#if LV_HAVE_SSSE3
#include <tmmintrin.h>
/*!
  \brief Deinterleaves the complex 16 bit vector into I & Q vector data
  \param complexVector The complex input vector
  \param iBuffer The I buffer output data
  \param qBuffer The Q buffer output data
  \param num_points The number of complex data values to be deinterleaved
*/
static inline void volk_16sc_deinterleave_16s_aligned16_ssse3(int16_t* iBuffer, int16_t* qBuffer, const lv_16sc_t* complexVector, unsigned int num_points){
  unsigned int number = 0;
  const int8_t* complexVectorPtr = (int8_t*)complexVector;
  int16_t* iBufferPtr = iBuffer;
  int16_t* qBufferPtr = qBuffer;

  __m128i iMoveMask1 = _mm_set_epi8(0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 13, 12, 9, 8, 5, 4, 1, 0);
  __m128i iMoveMask2 = _mm_set_epi8(13, 12, 9, 8, 5, 4, 1, 0, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80);

  __m128i qMoveMask1 = _mm_set_epi8(0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 15, 14, 11, 10, 7, 6, 3, 2);
  __m128i qMoveMask2 = _mm_set_epi8(15, 14, 11, 10, 7, 6, 3, 2, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80, 0x80);

  __m128i complexVal1, complexVal2, iOutputVal, qOutputVal;

  unsigned int eighthPoints = num_points / 8;

  for(number = 0; number < eighthPoints; number++){
    complexVal1 = _mm_load_si128((__m128i*)complexVectorPtr);  complexVectorPtr += 16;
    complexVal2 = _mm_load_si128((__m128i*)complexVectorPtr);  complexVectorPtr += 16;

    iOutputVal = _mm_or_si128( _mm_shuffle_epi8(complexVal1, iMoveMask1) , _mm_shuffle_epi8(complexVal2, iMoveMask2));
    qOutputVal = _mm_or_si128( _mm_shuffle_epi8(complexVal1, qMoveMask1) , _mm_shuffle_epi8(complexVal2, qMoveMask2));

    _mm_store_si128((__m128i*)iBufferPtr, iOutputVal);
    _mm_store_si128((__m128i*)qBufferPtr, qOutputVal);

    iBufferPtr += 8;
    qBufferPtr += 8;
  }

  number = eighthPoints * 8;
  int16_t* int16ComplexVectorPtr = (int16_t*)complexVectorPtr;
  for(; number < num_points; number++){
    *iBufferPtr++ = *int16ComplexVectorPtr++;
    *qBufferPtr++ = *int16ComplexVectorPtr++;
  }
}
#endif /* LV_HAVE_SSSE3 */

#if LV_HAVE_SSE2
#include <emmintrin.h>
/*!
  \brief Deinterleaves the complex 16 bit vector into I & Q vector data
  \param complexVector The complex input vector
  \param iBuffer The I buffer output data
  \param qBuffer The Q buffer output data
  \param num_points The number of complex data values to be deinterleaved
*/
static inline void volk_16sc_deinterleave_16s_aligned16_sse2(int16_t* iBuffer, int16_t* qBuffer, const lv_16sc_t* complexVector, unsigned int num_points){
  unsigned int number = 0;
  const int16_t* complexVectorPtr = (int16_t*)complexVector;
  int16_t* iBufferPtr = iBuffer;
  int16_t* qBufferPtr = qBuffer;
  __m128i complexVal1, complexVal2, iComplexVal1, iComplexVal2, qComplexVal1, qComplexVal2, iOutputVal, qOutputVal;
  __m128i lowMask = _mm_set_epi32(0x0, 0x0, 0xFFFFFFFF, 0xFFFFFFFF);
  __m128i highMask = _mm_set_epi32(0xFFFFFFFF, 0xFFFFFFFF, 0x0, 0x0);

  unsigned int eighthPoints = num_points / 8;
 
  for(number = 0; number < eighthPoints; number++){
    complexVal1 = _mm_load_si128((__m128i*)complexVectorPtr);  complexVectorPtr += 8;
    complexVal2 = _mm_load_si128((__m128i*)complexVectorPtr);  complexVectorPtr += 8;

    iComplexVal1 = _mm_shufflelo_epi16(complexVal1, _MM_SHUFFLE(3,1,2,0));

    iComplexVal1 = _mm_shufflehi_epi16(iComplexVal1, _MM_SHUFFLE(3,1,2,0));

    iComplexVal1 = _mm_shuffle_epi32(iComplexVal1, _MM_SHUFFLE(3,1,2,0));

    iComplexVal2 = _mm_shufflelo_epi16(complexVal2, _MM_SHUFFLE(3,1,2,0));

    iComplexVal2 = _mm_shufflehi_epi16(iComplexVal2, _MM_SHUFFLE(3,1,2,0));

    iComplexVal2 = _mm_shuffle_epi32(iComplexVal2, _MM_SHUFFLE(2,0,3,1));

    iOutputVal = _mm_or_si128(_mm_and_si128(iComplexVal1, lowMask), _mm_and_si128(iComplexVal2, highMask));

    _mm_store_si128((__m128i*)iBufferPtr, iOutputVal);

    qComplexVal1 = _mm_shufflelo_epi16(complexVal1, _MM_SHUFFLE(2,0,3,1));

    qComplexVal1 = _mm_shufflehi_epi16(qComplexVal1, _MM_SHUFFLE(2,0,3,1));

    qComplexVal1 = _mm_shuffle_epi32(qComplexVal1, _MM_SHUFFLE(3,1,2,0));

    qComplexVal2 = _mm_shufflelo_epi16(complexVal2, _MM_SHUFFLE(2,0,3,1));

    qComplexVal2 = _mm_shufflehi_epi16(qComplexVal2, _MM_SHUFFLE(2,0,3,1));

    qComplexVal2 = _mm_shuffle_epi32(qComplexVal2, _MM_SHUFFLE(2,0,3,1));

    qOutputVal = _mm_or_si128(_mm_and_si128(qComplexVal1, lowMask), _mm_and_si128(qComplexVal2, highMask));

    _mm_store_si128((__m128i*)qBufferPtr, qOutputVal);

    iBufferPtr += 8;
    qBufferPtr += 8;
  }

  number = eighthPoints * 8;
  for(; number < num_points; number++){
    *iBufferPtr++ = *complexVectorPtr++;
    *qBufferPtr++ = *complexVectorPtr++;
  }
}
#endif /* LV_HAVE_SSE2 */

#if LV_HAVE_GENERIC
/*!
  \brief Deinterleaves the complex 16 bit vector into I & Q vector data
  \param complexVector The complex input vector
  \param iBuffer The I buffer output data
  \param qBuffer The Q buffer output data
  \param num_points The number of complex data values to be deinterleaved
*/
static inline void volk_16sc_deinterleave_16s_aligned16_generic(int16_t* iBuffer, int16_t* qBuffer, const lv_16sc_t* complexVector, unsigned int num_points){
  const int16_t* complexVectorPtr = (const int16_t*)complexVector;
  int16_t* iBufferPtr = iBuffer;
  int16_t* qBufferPtr = qBuffer;
  unsigned int number;
  for(number = 0; number < num_points; number++){
    *iBufferPtr++ = *complexVectorPtr++;
    *qBufferPtr++ = *complexVectorPtr++;
  }
}
#endif /* LV_HAVE_GENERIC */




#endif /* INCLUDED_VOLK_16sc_DEINTERLEAVE_16S_ALIGNED16_H */
