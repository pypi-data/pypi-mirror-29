/* gimarshallingtestsextra.h
 *
 * Copyright (C) 2016 Thibault Saunier <tsaunier@gnome.org>
 *
 * This file is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as
 * published by the Free Software Foundation; either version 3 of the
 * License, or (at your option) any later version.
 *
 * This file is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef EXTRA_TESTS
#define EXTRA_TESTS

#include <glib-object.h>

typedef enum
{
  GI_MARSHALLING_TESTS_EXTRA_ENUM_VALUE1,
  GI_MARSHALLING_TESTS_EXTRA_ENUM_VALUE2,
  GI_MARSHALLING_TESTS_EXTRA_ENUM_VALUE3 = 42
} GIMarshallingTestsExtraEnum;


typedef enum
{
  GI_MARSHALLING_TESTS_EXTRA_FLAGS_VALUE1 = 0,
  GI_MARSHALLING_TESTS_EXTRA_FLAGS_VALUE2 = (gint)(1 << 31),
} GIMarshallingTestsExtraFlags;

GType gi_marshalling_tests_extra_flags_get_type (void) G_GNUC_CONST;
#define GI_MARSHALLING_TESTS_TYPE_EXTRA_FLAGS (gi_marshalling_tests_extra_flags_get_type ())

void gi_marshalling_tests_compare_two_gerrors_in_gvalue (GValue *v, GValue *v1);
void gi_marshalling_tests_ghashtable_enum_none_in (GHashTable *hash_table);
GHashTable * gi_marshalling_tests_ghashtable_enum_none_return (void);

gchar * gi_marshalling_tests_filename_copy (gchar *path_in);
gboolean gi_marshalling_tests_filename_exists (gchar *path);
gchar * gi_marshalling_tests_filename_to_glib_repr (gchar *path_in, gsize *len);

GIMarshallingTestsExtraEnum * gi_marshalling_tests_enum_array_return_type (gsize *n_members);

void gi_marshalling_tests_extra_flags_large_in (GIMarshallingTestsExtraFlags value);

#endif /* EXTRA_TESTS */
