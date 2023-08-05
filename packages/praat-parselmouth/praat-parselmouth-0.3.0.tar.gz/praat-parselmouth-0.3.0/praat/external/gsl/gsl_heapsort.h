/* sort/gsl_heapsort.h
 * 
 * Copyright (C) 1996, 1997, 1998, 1999, 2000, 2007 Thomas Walter, Brian Gough
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

#ifndef __GSL_HEAPSORT_H__
#define __GSL_HEAPSORT_H__

#include "gsl_permutation.h"

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

typedef int (*gsl_comparison_fn_t) (const void *, const void *);

void gsl_heapsort (void * array, size_t count, size_t size, gsl_comparison_fn_t compare);
int gsl_heapsort_index (size_t * p, const void * array, size_t count, size_t size, gsl_comparison_fn_t compare);

__END_DECLS

#endif /* __GSL_HEAPSORT_H__ */
