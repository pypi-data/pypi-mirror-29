/* block/gsl_block_complex_float.h
 * 
 * Copyright (C) 1996, 1997, 1998, 1999, 2000, 2007 Gerard Jungman, Brian Gough
 * 
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or (at
 * your option) any later version.
 * 
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 */

#ifndef __GSL_BLOCK_COMPLEX_FLOAT_H__
#define __GSL_BLOCK_COMPLEX_FLOAT_H__

#include <stdlib.h>
#include "gsl_errno.h"

#undef __BEGIN_DECLS
#undef __END_DECLS
#ifdef __cplusplus
# define __BEGIN_DECLS extern "C" {
# define __END_DECLS }
#else
# define __BEGIN_DECLS /* empty */
# define __END_DECLS /* empty */
#endif

__BEGIN_DECLS

struct gsl_block_complex_float_struct
{
  size_t size;
  float *data;
};

typedef struct gsl_block_complex_float_struct gsl_block_complex_float;

gsl_block_complex_float *gsl_block_complex_float_alloc (const size_t n);
gsl_block_complex_float *gsl_block_complex_float_calloc (const size_t n);
void gsl_block_complex_float_free (gsl_block_complex_float * b);

int gsl_block_complex_float_fread (FILE * stream, gsl_block_complex_float * b);
int gsl_block_complex_float_fwrite (FILE * stream, const gsl_block_complex_float * b);
int gsl_block_complex_float_fscanf (FILE * stream, gsl_block_complex_float * b);
int gsl_block_complex_float_fprintf (FILE * stream, const gsl_block_complex_float * b, const char *format);

int gsl_block_complex_float_raw_fread (FILE * stream, float * b, const size_t n, const size_t stride);
int gsl_block_complex_float_raw_fwrite (FILE * stream, const float * b, const size_t n, const size_t stride);
int gsl_block_complex_float_raw_fscanf (FILE * stream, float * b, const size_t n, const size_t stride);
int gsl_block_complex_float_raw_fprintf (FILE * stream, const float * b, const size_t n, const size_t stride, const char *format);

size_t gsl_block_complex_float_size (const gsl_block_complex_float * b);
float * gsl_block_complex_float_data (const gsl_block_complex_float * b);

__END_DECLS

#endif /* __GSL_BLOCK_COMPLEX_FLOAT_H__ */
