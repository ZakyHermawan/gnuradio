#ifndef INCLUDED_volk_32f_x3_sum_of_poly_32f_a_H
#define INCLUDED_volk_32f_x3_sum_of_poly_32f_a_H

#include<inttypes.h>
#include<stdio.h>
#include<volk/volk_complex.h>

#ifndef MAX
#define MAX(X,Y) ((X) > (Y)?(X):(Y))
#endif

#ifdef LV_HAVE_SSE3
#include<xmmintrin.h>
#include<pmmintrin.h>

static inline void volk_32f_x3_sum_of_poly_32f_a_sse3(float* target, float* src0, float* center_point_array, float* cutoff, unsigned int num_points) {

  const unsigned int num_bytes = num_points*4;

  float result = 0.0;
  float fst = 0.0;
  float sq = 0.0;
  float thrd = 0.0;
  float frth = 0.0;
  //float fith = 0.0;



  __m128 xmm0, xmm1, xmm2, xmm3, xmm4, xmm5, xmm6, xmm7, xmm8, xmm9, xmm10;// xmm11, xmm12;

  xmm9 = _mm_setzero_ps();
  xmm1 = _mm_setzero_ps();

  xmm0 = _mm_load1_ps(&center_point_array[0]);
  xmm6 = _mm_load1_ps(&center_point_array[1]);
  xmm7 = _mm_load1_ps(&center_point_array[2]);
  xmm8 = _mm_load1_ps(&center_point_array[3]);
  //xmm11 = _mm_load1_ps(&center_point_array[4]);
  xmm10 = _mm_load1_ps(cutoff);

  int bound = num_bytes >> 4;
  int leftovers = (num_bytes >> 2) & 3;
  int i = 0;

  for(; i < bound; ++i) {
    xmm2 = _mm_load_ps(src0);
    xmm2 = _mm_max_ps(xmm10, xmm2);
    xmm3 = _mm_mul_ps(xmm2, xmm2);
    xmm4 = _mm_mul_ps(xmm2, xmm3);
    xmm5 = _mm_mul_ps(xmm3, xmm3);
    //xmm12 = _mm_mul_ps(xmm3, xmm4);

    xmm2 = _mm_mul_ps(xmm2, xmm0);
    xmm3 = _mm_mul_ps(xmm3, xmm6);
    xmm4 = _mm_mul_ps(xmm4, xmm7);
    xmm5 = _mm_mul_ps(xmm5, xmm8);
    //xmm12 = _mm_mul_ps(xmm12, xmm11);

    xmm2 = _mm_add_ps(xmm2, xmm3);
    xmm3 = _mm_add_ps(xmm4, xmm5);

    src0 += 4;

    xmm9 = _mm_add_ps(xmm2, xmm9);

    xmm1 = _mm_add_ps(xmm3, xmm1);

    //xmm9 = _mm_add_ps(xmm12, xmm9);
  }

  xmm2 = _mm_hadd_ps(xmm9, xmm1);
  xmm3 = _mm_hadd_ps(xmm2, xmm2);
  xmm4 = _mm_hadd_ps(xmm3, xmm3);

  _mm_store_ss(&result, xmm4);



  for(i = 0; i < leftovers; ++i) {
    fst = src0[i];
    fst = MAX(fst, *cutoff);
    sq = fst * fst;
    thrd = fst * sq;
    frth = sq * sq;
    //fith = sq * thrd;

    result += (center_point_array[0] * fst +
	       center_point_array[1] * sq +
	       center_point_array[2] * thrd +
	       center_point_array[3] * frth);// +
	       //center_point_array[4] * fith);
  }

  result += ((float)((bound * 4) + leftovers)) * center_point_array[4]; //center_point_array[5];

  target[0] = result;
}


#endif /*LV_HAVE_SSE3*/


#ifdef LV_HAVE_AVX
#include<immintrin.h>

static inline void volk_32f_x3_sum_of_poly_32f_a_avx(float* target, float* src0, float* center_point_array, float* cutoff, unsigned int num_points)
{
  const unsigned int eighth_points = num_points / 8;
  float fst = 0.0;
  float sq = 0.0;
  float thrd = 0.0;
  float frth = 0.0;

  __m256 cpa0, cpa1, cpa2, cpa3, cutoff_vec;
  __m256 target_vec;
  __m256 x_to_1, x_to_2, x_to_3, x_to_4;

  cpa0 = _mm256_set1_ps(center_point_array[0]);
  cpa1 = _mm256_set1_ps(center_point_array[1]);
  cpa2 = _mm256_set1_ps(center_point_array[2]);
  cpa3 = _mm256_set1_ps(center_point_array[3]);
  cutoff_vec = _mm256_set1_ps(*cutoff);
  target_vec = _mm256_setzero_ps();

  unsigned int i;

  for(i = 0; i < eighth_points; ++i) {
    x_to_1 = _mm256_load_ps(src0);
    x_to_1 = _mm256_max_ps(x_to_1, cutoff_vec);
    x_to_2 = _mm256_mul_ps(x_to_1, x_to_1); // x^2
    x_to_3 = _mm256_mul_ps(x_to_1, x_to_2); // x^3
    // x^1 * x^3 is slightly faster than x^2 * x^2
    x_to_4 = _mm256_mul_ps(x_to_1, x_to_3); // x^4

    x_to_1 = _mm256_mul_ps(x_to_1, cpa0); // cpa[0] * x^1
    x_to_2 = _mm256_mul_ps(x_to_2, cpa1); // cpa[1] * x^2
    x_to_3 = _mm256_mul_ps(x_to_3, cpa2); // cpa[2] * x^3
    x_to_4 = _mm256_mul_ps(x_to_4, cpa3); // cpa[3] * x^4

    x_to_1 = _mm256_add_ps(x_to_1, x_to_2);
    x_to_3 = _mm256_add_ps(x_to_3, x_to_4);
    // this is slightly faster than result += (x_to_1 + x_to_3)
    target_vec = _mm256_add_ps(x_to_1, target_vec);
    target_vec = _mm256_add_ps(x_to_3, target_vec);

    src0 += 8;
  }

  // the hadd for vector reduction has very very slight impact @ 50k iters
  __VOLK_ATTR_ALIGNED(32) float temp_results[8];
  target_vec = _mm256_hadd_ps(target_vec, target_vec); // x0+x1 | x2+x3 | x0+x1 | x2+x3 || x4+x5 | x6+x7 | x4+x5 | x6+x7
  _mm256_store_ps(temp_results, target_vec);
  *target = temp_results[0] + temp_results[1] + temp_results[4] + temp_results[5];


  for(i = eighth_points*8; i < num_points; ++i) {
    fst = *(src0++);
    fst = MAX(fst, *cutoff);
    sq = fst * fst;
    thrd = fst * sq;
    frth = sq * sq;

    *target += (center_point_array[0] * fst +
	       center_point_array[1] * sq +
	       center_point_array[2] * thrd +
	       center_point_array[3] * frth);
  }

  *target += ((float)(num_points)) * center_point_array[4];

}
#endif // LV_HAVE_AVX


#ifdef LV_HAVE_GENERIC

static inline void volk_32f_x3_sum_of_poly_32f_generic(float* target, float* src0, float* center_point_array, float* cutoff, unsigned int num_points) {

  const unsigned int num_bytes = num_points*4;

  float result = 0.0;
  float fst = 0.0;
  float sq = 0.0;
  float thrd = 0.0;
  float frth = 0.0;
  //float fith = 0.0;



  unsigned int i = 0;

  for(; i < num_bytes >> 2; ++i) {
    fst = src0[i];
    fst = MAX(fst, *cutoff);

    sq = fst * fst;
    thrd = fst * sq;
    frth = sq * sq;
    //fith = sq * thrd;

    result += (center_point_array[0] * fst +
	       center_point_array[1] * sq +
	       center_point_array[2] * thrd +
	       center_point_array[3] * frth); //+
	       //center_point_array[4] * fith);
    /*printf("%f12...%d\n", (center_point_array[0] * fst +
		  center_point_array[1] * sq +
		  center_point_array[2] * thrd +
			 center_point_array[3] * frth) +
	   //center_point_array[4] * fith) +
	   (center_point_array[4]), i);
    */
  }

  result += ((float)(num_bytes >> 2)) * (center_point_array[4]);//(center_point_array[5]);



  *target = result;
}

#endif /*LV_HAVE_GENERIC*/


#ifdef LV_HAVE_AVX
#include<immintrin.h>

static inline void volk_32f_x3_sum_of_poly_32f_u_avx(float* target, float* src0, float* center_point_array, float* cutoff, unsigned int num_points)
{
  const unsigned int eighth_points = num_points / 8;
  float fst = 0.0;
  float sq = 0.0;
  float thrd = 0.0;
  float frth = 0.0;

  __m256 cpa0, cpa1, cpa2, cpa3, cutoff_vec;
  __m256 target_vec;
  __m256 x_to_1, x_to_2, x_to_3, x_to_4;

  cpa0 = _mm256_set1_ps(center_point_array[0]);
  cpa1 = _mm256_set1_ps(center_point_array[1]);
  cpa2 = _mm256_set1_ps(center_point_array[2]);
  cpa3 = _mm256_set1_ps(center_point_array[3]);
  cutoff_vec = _mm256_set1_ps(*cutoff);
  target_vec = _mm256_setzero_ps();

  unsigned int i;

  for(i = 0; i < eighth_points; ++i) {
    x_to_1 = _mm256_loadu_ps(src0);
    x_to_1 = _mm256_max_ps(x_to_1, cutoff_vec);
    x_to_2 = _mm256_mul_ps(x_to_1, x_to_1); // x^2
    x_to_3 = _mm256_mul_ps(x_to_1, x_to_2); // x^3
    // x^1 * x^3 is slightly faster than x^2 * x^2
    x_to_4 = _mm256_mul_ps(x_to_1, x_to_3); // x^4

    x_to_1 = _mm256_mul_ps(x_to_1, cpa0); // cpa[0] * x^1
    x_to_2 = _mm256_mul_ps(x_to_2, cpa1); // cpa[1] * x^2
    x_to_3 = _mm256_mul_ps(x_to_3, cpa2); // cpa[2] * x^3
    x_to_4 = _mm256_mul_ps(x_to_4, cpa3); // cpa[3] * x^4

    x_to_1 = _mm256_add_ps(x_to_1, x_to_2);
    x_to_3 = _mm256_add_ps(x_to_3, x_to_4);
    // this is slightly faster than result += (x_to_1 + x_to_3)
    target_vec = _mm256_add_ps(x_to_1, target_vec);
    target_vec = _mm256_add_ps(x_to_3, target_vec);

    src0 += 8;
  }

  // the hadd for vector reduction has very very slight impact @ 50k iters
  __VOLK_ATTR_ALIGNED(32) float temp_results[8];
  target_vec = _mm256_hadd_ps(target_vec, target_vec); // x0+x1 | x2+x3 | x0+x1 | x2+x3 || x4+x5 | x6+x7 | x4+x5 | x6+x7
  _mm256_store_ps(temp_results, target_vec);
  *target = temp_results[0] + temp_results[1] + temp_results[4] + temp_results[5];


  for(i = eighth_points*8; i < num_points; ++i) {
    fst = *(src0++);
    fst = MAX(fst, *cutoff);
    sq = fst * fst;
    thrd = fst * sq;
    frth = sq * sq;

    *target += (center_point_array[0] * fst +
	       center_point_array[1] * sq +
	       center_point_array[2] * thrd +
	       center_point_array[3] * frth);
  }

  *target += ((float)(num_points)) * center_point_array[4];

}
#endif // LV_HAVE_AVX




#endif /*INCLUDED_volk_32f_x3_sum_of_poly_32f_a_H*/
